"""
Car Garage Billing System 

Features
- Data-driven price lists (edit SERVICES / PARTS / settings below)
- Live totals: the bill updates as you type, no need to press TOTAL
- Input validation (digits-only quantities, numeric money fields, 10-digit phone)
- GST calculated AFTER discount (the correct way)
- Sequential bill numbers stored in a SQLite database
- Bill history window: search by bill no / name / phone / vehicle, view, print, delete
- Payment status (PAID / PARTIAL / UNPAID) and today's sales on the status bar
- Resizable window, keyboard shortcuts, safe printing via temp file
"""

import os
import re
import sys
import sqlite3
import tempfile
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ====================== SETTINGS ======================

APP_TITLE = "Car Garage Billing System"
GARAGE_NAME = "CAR GARAGE"
GARAGE_TAGLINE = "SERVICE CENTER"
GST_RATE = 18            # percent
DB_FILE = "garage_billing.db"
BILL_DIR = "garage_bills"
BILL_WIDTH = 42          # characters per line on the printed bill

SERVICES = {
    "General Service": 800,
    "Oil Change": 500,
    "Car Washing": 300,
    "Engine Service": 2500,
    "Brake Service": 1200,
    "Tyre Service": 700,
    "Battery Service": 500,
}

PARTS = {
    "Engine Oil": 650,
    "Oil Filter": 250,
    "Air Filter": 350,
    "Brake Pad": 1800,
    "Spark Plug": 400,
    "Coolant": 500,
    "Battery": 4500,
}

# Colours
BG = "#17202A"
PRIMARY = "#2874A6"
LIGHT = "#D6EAF8"
DARK = "#154360"
GOLD = "#F4D03F"


class GarageBillingSystem:

    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("1280x790")
        self.root.minsize(1150, 720)
        self.root.configure(bg=BG)

        self._after_id = None
        self.current = None          # last calculated bill (dict)
        self.bill_dt = datetime.now()

        self.init_db()
        self.init_variables()
        self.setup_style()
        self.build_ui()
        self.bind_events()

        self.new_bill(ask=False)
        self.tick()

    # ====================== DATABASE ======================

    def init_db(self):
        self.db = sqlite3.connect(DB_FILE)
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS bills (
                bill_no   INTEGER PRIMARY KEY,
                date      TEXT NOT NULL,
                customer  TEXT,
                phone     TEXT,
                vehicle   TEXT,
                model     TEXT,
                subtotal  REAL,
                labour    REAL,
                discount  REAL,
                gst       REAL,
                total     REAL,
                method    TEXT,
                paid      REAL,
                status    TEXT,
                bill_text TEXT
            )"""
        )
        self.db.commit()

    def next_bill_no(self):
        row = self.db.execute("SELECT MAX(bill_no) FROM bills").fetchone()[0]
        return str((row or 10000) + 1)

    # ====================== VARIABLES ======================

    def init_variables(self):
        self.customer_name = tk.StringVar()
        self.phone = tk.StringVar()
        self.vehicle_no = tk.StringVar()
        self.car_model = tk.StringVar()
        self.bill_no = tk.StringVar()
        self.clock = tk.StringVar()

        self.service_qty = {n: tk.StringVar(value="0") for n in SERVICES}
        self.part_qty = {n: tk.StringVar(value="0") for n in PARTS}
        self.service_amt = {n: tk.StringVar(value="0.00") for n in SERVICES}
        self.part_amt = {n: tk.StringVar(value="0.00") for n in PARTS}

        self.labour = tk.StringVar(value="0")
        self.discount = tk.StringVar(value="0")
        self.payment_method = tk.StringVar(value="Cash")
        self.amount_paid = tk.StringVar(value="0")

        # Outputs
        self.service_total = tk.StringVar(value="0.00")
        self.parts_total = tk.StringVar(value="0.00")
        self.discount_amt = tk.StringVar(value="0.00")
        self.gst_amt = tk.StringVar(value="0.00")
        self.grand_total = tk.StringVar(value="Rs 0.00")
        self.balance = tk.StringVar(value="-")
        self.status = tk.StringVar(value="-")
        self.today_info = tk.StringVar(value="")

        # Any input change -> debounced recalculation
        watched = [
            self.customer_name, self.phone, self.vehicle_no, self.car_model,
            self.labour, self.discount, self.payment_method, self.amount_paid,
            *self.service_qty.values(), *self.part_qty.values(),
        ]
        for var in watched:
            var.trace_add("write", self.schedule_update)

        # Validators
        reg = self.root.register
        self.vcmd_int = (reg(lambda s: s == "" or (s.isdigit() and len(s) <= 2)), "%P")
        self.vcmd_money = (reg(lambda s: re.fullmatch(r"\d{0,7}(\.\d{0,2})?", s) is not None), "%P")
        self.vcmd_phone = (reg(lambda s: s == "" or (s.isdigit() and len(s) <= 10)), "%P")

    # ====================== STYLE ======================

    def setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Treeview", rowheight=24, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    # ====================== UI HELPERS ======================

    def lbl(self, parent, text, bg=PRIMARY, fg="white", font=("Segoe UI", 10, "bold"), **kw):
        return tk.Label(parent, text=text, bg=bg, fg=fg, font=font, **kw)

    def ro_entry(self, parent, var, width=18):
        return ttk.Entry(parent, textvariable=var, width=width,
                         state="readonly", justify="right")

    def money_entry(self, parent, var, width=18):
        return ttk.Entry(parent, textvariable=var, width=width, justify="right",
                         validate="key", validatecommand=self.vcmd_money)

    def action_button(self, parent, text, command, col):
        tk.Button(
            parent, text=text, command=command, width=12,
            font=("Segoe UI", 10, "bold"), bg=LIGHT, fg=DARK,
            activebackground="white", relief=tk.RAISED, bd=3, cursor="hand2",
        ).grid(row=0, column=col, padx=6, pady=6)

    # ====================== UI ======================

    def build_ui(self):
        r = self.root
        r.grid_columnconfigure(0, weight=1)
        r.grid_rowconfigure(2, weight=1)

        # ---- Title
        tk.Label(r, text="CAR GARAGE BILLING SYSTEM", font=("Segoe UI Black", 20),
                 bg=PRIMARY, fg="white", bd=6, relief=tk.RIDGE
                 ).grid(row=0, column=0, sticky="ew")

        # ---- Customer details
        details = tk.LabelFrame(r, text="Customer & Vehicle Details", bg=PRIMARY, fg="white",
                                font=("Segoe UI", 11, "bold"), bd=5, relief=tk.GROOVE)
        details.grid(row=1, column=0, sticky="ew", padx=4, pady=(4, 0))

        fields = [
            (0, 0, "Customer Name *", self.customer_name, 20, None),
            (0, 2, "Phone", self.phone, 16, self.vcmd_phone),
            (0, 4, "Vehicle No. *", self.vehicle_no, 16, None),
            (0, 6, "Car Model", self.car_model, 16, None),
        ]
        for row, col, text, var, width, vcmd in fields:
            self.lbl(details, text).grid(row=row, column=col, padx=8, pady=6, sticky="e")
            kw = {"validate": "key", "validatecommand": vcmd} if vcmd else {}
            ttk.Entry(details, width=width, textvariable=var, **kw
                      ).grid(row=row, column=col + 1, padx=(0, 8))

        self.lbl(details, "Bill No.").grid(row=1, column=0, padx=8, pady=4, sticky="e")
        ttk.Entry(details, width=20, textvariable=self.bill_no, state="readonly"
                  ).grid(row=1, column=1, sticky="w")

        # ---- Main area
        main = tk.Frame(r, bg=BG)
        main.grid(row=2, column=0, sticky="nsew", padx=4, pady=4)
        main.grid_rowconfigure(0, weight=1)
        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=1)

        self.build_item_panel(main, 0, "Garage Services", SERVICES,
                              self.service_qty, self.service_amt)
        self.build_item_panel(main, 1, "Parts / Materials", PARTS,
                              self.part_qty, self.part_amt)
        self.build_bill_panel(main, 2)

        # ---- Summary
        self.build_summary(r, 3)

        # ---- Status bar
        bar = tk.Frame(r, bg=DARK)
        bar.grid(row=4, column=0, sticky="ew")
        tk.Label(bar, textvariable=self.today_info, bg=DARK, fg="white",
                 font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=10, pady=3)
        tk.Label(bar, textvariable=self.clock, bg=DARK, fg="white",
                 font=("Segoe UI", 10)).pack(side=tk.RIGHT, padx=10)
        tk.Label(bar, text="Ctrl+S Save  |  Ctrl+P Print  |  Ctrl+N New  |  Ctrl+H History",
                 bg=DARK, fg=LIGHT, font=("Segoe UI", 9)).pack(side=tk.RIGHT, padx=20)

    def build_item_panel(self, parent, col, title, catalog, qty_vars, amt_vars):
        frame = tk.LabelFrame(parent, text=title, bg=LIGHT, fg=DARK,
                              font=("Segoe UI", 11, "bold"), bd=5, relief=tk.GROOVE)
        frame.grid(row=0, column=col, sticky="nsew", padx=4)
        frame.grid_columnconfigure(0, weight=1)

        for c, head in enumerate(("Item", "Rate (Rs)", "Qty", "Amount (Rs)")):
            self.lbl(frame, head, bg=DARK, fg="white").grid(
                row=0, column=c, sticky="ew", padx=1, pady=(2, 6))

        for i, (name, rate) in enumerate(catalog.items(), start=1):
            self.lbl(frame, name, bg=LIGHT, fg=DARK, anchor="w").grid(
                row=i, column=0, sticky="w", padx=8, pady=7)
            self.lbl(frame, f"{rate:,}", bg=LIGHT, fg=DARK,
                     font=("Segoe UI", 10)).grid(row=i, column=1, padx=8)
            ttk.Spinbox(frame, from_=0, to=99, width=5, textvariable=qty_vars[name],
                        validate="key", validatecommand=self.vcmd_int, justify="center"
                        ).grid(row=i, column=2, padx=8)
            self.lbl(frame, "", bg=LIGHT, fg=DARK, font=("Consolas", 10, "bold"),
                     textvariable=amt_vars[name], width=11, anchor="e"
                     ).grid(row=i, column=3, padx=8)

    def build_bill_panel(self, parent, col):
        frame = tk.Frame(parent, bd=5, relief=tk.GROOVE, bg="white")
        frame.grid(row=0, column=col, sticky="ns", padx=4)

        tk.Label(frame, text="SERVICE BILL", font=("Segoe UI Black", 14),
                 bg=LIGHT, fg=DARK, bd=3, relief=tk.GROOVE).pack(fill=tk.X)

        scroll = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.bill_area = tk.Text(frame, font=("Consolas", 10), width=BILL_WIDTH + 2,
                                 yscrollcommand=scroll.set, state="disabled", wrap="none")
        self.bill_area.pack(fill=tk.BOTH, expand=True)
        scroll.config(command=self.bill_area.yview)

    def build_summary(self, parent, row):
        s = tk.LabelFrame(parent, text="Billing Summary", bg=PRIMARY, fg="white",
                          font=("Segoe UI", 11, "bold"), bd=5, relief=tk.GROOVE)
        s.grid(row=row, column=0, sticky="ew", padx=4, pady=(0, 4))

        # Column group 1
        self.lbl(s, "Service Total (Rs)").grid(row=0, column=0, padx=8, pady=4, sticky="e")
        self.ro_entry(s, self.service_total).grid(row=0, column=1)
        self.lbl(s, "Parts Total (Rs)").grid(row=1, column=0, padx=8, pady=4, sticky="e")
        self.ro_entry(s, self.parts_total).grid(row=1, column=1)
        self.lbl(s, "Labour Charge (Rs)").grid(row=2, column=0, padx=8, pady=4, sticky="e")
        self.money_entry(s, self.labour).grid(row=2, column=1)

        # Column group 2
        self.lbl(s, "Discount %").grid(row=0, column=2, padx=8, sticky="e")
        self.money_entry(s, self.discount).grid(row=0, column=3)
        self.lbl(s, "Discount Amount (Rs)").grid(row=1, column=2, padx=8, sticky="e")
        self.ro_entry(s, self.discount_amt).grid(row=1, column=3)
        self.lbl(s, f"GST {GST_RATE}% (Rs)").grid(row=2, column=2, padx=8, sticky="e")
        self.ro_entry(s, self.gst_amt).grid(row=2, column=3)

        # Column group 3
        self.lbl(s, "GRAND TOTAL", font=("Segoe UI", 11, "bold")).grid(
            row=0, column=4, padx=8, sticky="e")
        tk.Label(s, textvariable=self.grand_total, bg=DARK, fg=GOLD, width=16,
                 font=("Consolas", 15, "bold"), bd=3, relief=tk.SUNKEN
                 ).grid(row=0, column=5, padx=4, pady=4)

        self.lbl(s, "Payment").grid(row=1, column=4, padx=8, sticky="e")
        ttk.Combobox(s, textvariable=self.payment_method, state="readonly", width=16,
                     values=("Cash", "UPI", "Card")).grid(row=1, column=5)
        self.lbl(s, "Amount Paid (Rs)").grid(row=2, column=4, padx=8, sticky="e")
        self.money_entry(s, self.amount_paid, width=19).grid(row=2, column=5)

        self.lbl(s, "Balance").grid(row=0, column=6, padx=8, sticky="e")
        self.ro_entry(s, self.balance, width=20).grid(row=0, column=7)
        self.lbl(s, "Status").grid(row=1, column=6, padx=8, sticky="e")
        self.ro_entry(s, self.status, width=20).grid(row=1, column=7)

        # Buttons
        bf = tk.Frame(s, bg=DARK, bd=4, relief=tk.GROOVE)
        bf.grid(row=3, column=0, columnspan=8, pady=6)
        self.action_button(bf, "TOTAL", self.show_total, 0)
        self.action_button(bf, "SAVE", self.save_bill, 1)
        self.action_button(bf, "PRINT", self.print_bill, 2)
        self.action_button(bf, "HISTORY", self.open_history, 3)
        self.action_button(bf, "NEW / CLEAR", lambda: self.new_bill(ask=True), 4)

    def bind_events(self):
        self.root.bind("<Control-s>", lambda e: self.save_bill())
        self.root.bind("<Control-p>", lambda e: self.print_bill())
        self.root.bind("<Control-n>", lambda e: self.new_bill(ask=True))
        self.root.bind("<Control-h>", lambda e: self.open_history())
        self.root.bind("<F5>", lambda e: self.show_total())
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)

    # ====================== CLOCK / STATUS ======================

    def tick(self):
        self.clock.set(datetime.now().strftime("%d-%m-%Y  %I:%M:%S %p"))
        self.root.after(1000, self.tick)

    def refresh_today(self):
        today = datetime.now().strftime("%Y-%m-%d")
        count, total = self.db.execute(
            "SELECT COUNT(*), COALESCE(SUM(total), 0) FROM bills WHERE date LIKE ?",
            (today + "%",),
        ).fetchone()
        self.today_info.set(f"Today: {count} bill(s)  |  Sales: Rs {total:,.2f}")

    # ====================== CALCULATION ======================

    def schedule_update(self, *_):
        if self._after_id:
            self.root.after_cancel(self._after_id)
        self._after_id = self.root.after(150, self.live_update)

    def live_update(self):
        self._after_id = None
        try:
            self.calculate()
        except ValueError:
            pass  # user is mid-typing; stay quiet

    def show_total(self):
        try:
            self.calculate()
        except ValueError as err:
            messagebox.showerror("Invalid Input", str(err))

    def _collect(self, catalog, qty_vars, amt_vars):
        lines = []
        for name, rate in catalog.items():
            raw = qty_vars[name].get().strip()
            try:
                qty = int(raw or 0)
            except ValueError:
                raise ValueError(f"Invalid quantity for {name}.")
            amount = qty * rate
            amt_vars[name].set(f"{amount:,.2f}")
            if qty > 0:
                lines.append({"name": name, "qty": qty, "rate": rate, "amount": amount})
        return lines

    @staticmethod
    def _money(var, label):
        raw = var.get().strip()
        try:
            value = float(raw or 0)
        except ValueError:
            raise ValueError(f"{label} must be a number.")
        if value < 0:
            raise ValueError(f"{label} cannot be negative.")
        return value

    def calculate(self):
        services = self._collect(SERVICES, self.service_qty, self.service_amt)
        parts = self._collect(PARTS, self.part_qty, self.part_amt)

        labour = self._money(self.labour, "Labour charge")
        disc_pct = self._money(self.discount, "Discount")
        paid = self._money(self.amount_paid, "Amount paid")
        if disc_pct > 100:
            raise ValueError("Discount must be between 0 and 100.")

        service_total = sum(l["amount"] for l in services)
        parts_total = sum(l["amount"] for l in parts)
        subtotal = service_total + parts_total + labour

        discount_amt = round(subtotal * disc_pct / 100, 2)
        taxable = subtotal - discount_amt
        gst = round(taxable * GST_RATE / 100, 2)       # GST on discounted amount
        total = round(taxable + gst, 2)
        balance = round(paid - total, 2)

        if total <= 0:
            status = "-"
        elif paid >= total:
            status = "PAID"
        elif paid > 0:
            status = "PARTIAL"
        else:
            status = "UNPAID"

        d = {
            "bill_no": self.bill_no.get(),
            "datetime": self.bill_dt,
            "customer": self.customer_name.get().strip(),
            "phone": self.phone.get().strip(),
            "vehicle": self.vehicle_no.get().strip().upper(),
            "model": self.car_model.get().strip(),
            "services": services, "parts": parts,
            "service_total": service_total, "parts_total": parts_total,
            "labour": labour, "subtotal": subtotal,
            "discount_pct": disc_pct, "discount_amt": discount_amt,
            "gst": gst, "total": total,
            "method": self.payment_method.get(), "paid": paid,
            "balance": balance, "status": status,
        }

        # Update summary widgets
        self.service_total.set(f"{service_total:,.2f}")
        self.parts_total.set(f"{parts_total:,.2f}")
        self.discount_amt.set(f"{discount_amt:,.2f}")
        self.gst_amt.set(f"{gst:,.2f}")
        self.grand_total.set(f"Rs {total:,.2f}")
        self.status.set(status)
        if total <= 0:
            self.balance.set("-")
        elif balance >= 0:
            self.balance.set(f"Change: {balance:,.2f}")
        else:
            self.balance.set(f"Due: {abs(balance):,.2f}")

        self.current = d
        self.render_preview(self.build_bill_text(d))
        return d

    # ====================== BILL TEXT ======================

    def build_bill_text(self, d):
        w = BILL_WIDTH
        sep, thin = "=" * w, "-" * w

        def kv(label, value):
            return f"{label:<20}{value:>{w - 20}}"

        L = [
            GARAGE_NAME.center(w),
            GARAGE_TAGLINE.center(w),
            sep,
            f"Bill No : {d['bill_no']}",
            f"Date    : {d['datetime']:%d-%m-%Y %I:%M %p}",
            sep,
            f"Customer: {d['customer']}",
            f"Phone   : {d['phone']}",
            f"Vehicle : {d['vehicle']}",
            f"Model   : {d['model']}",
            sep,
            f"{'Item':<18}{'Qty':>4}{'Rate':>9}{'Amount':>11}",
            thin,
        ]

        if not d["services"] and not d["parts"]:
            L.append("No items added yet".center(w))

        for title, lines in (("SERVICES", d["services"]), ("PARTS", d["parts"])):
            if lines:
                L.append(title)
                for l in lines:
                    L.append(f"{l['name'][:18]:<18}{l['qty']:>4}{l['rate']:>9,.0f}{l['amount']:>11,.2f}")

        L += [
            thin,
            kv("Services", f"{d['service_total']:,.2f}"),
            kv("Parts", f"{d['parts_total']:,.2f}"),
            kv("Labour", f"{d['labour']:,.2f}"),
            kv("Sub Total", f"{d['subtotal']:,.2f}"),
            kv(f"Discount ({d['discount_pct']:g}%)", f"- {d['discount_amt']:,.2f}"),
            kv(f"GST ({GST_RATE}%)", f"{d['gst']:,.2f}"),
            sep,
            kv("GRAND TOTAL (Rs)", f"{d['total']:,.2f}"),
            sep,
            kv("Payment", d["method"]),
            kv("Paid", f"{d['paid']:,.2f}"),
        ]
        if d["total"] > 0:
            if d["balance"] >= 0:
                L.append(kv("Change", f"{d['balance']:,.2f}"))
            else:
                L.append(kv("Balance Due", f"{abs(d['balance']):,.2f}"))
        L += [kv("Status", d["status"]), sep,
              "THANK YOU!".center(w), "VISIT AGAIN".center(w)]
        return "\n".join(L) + "\n"

    def render_preview(self, text):
        self.bill_area.config(state="normal")
        self.bill_area.delete("1.0", tk.END)
        self.bill_area.insert(tk.END, text)
        self.bill_area.config(state="disabled")

    # ====================== NEW / CLEAR ======================

    def has_data(self):
        if any(v.get().strip() for v in
               (self.customer_name, self.phone, self.vehicle_no, self.car_model)):
            return True
        qtys = [*self.service_qty.values(), *self.part_qty.values()]
        return any(v.get().strip() not in ("", "0") for v in qtys)

    def new_bill(self, ask=True):
        if ask and self.has_data():
            if not messagebox.askyesno("New Bill", "Clear all information and start a new bill?"):
                return

        for v in (self.customer_name, self.phone, self.vehicle_no, self.car_model):
            v.set("")
        for v in (*self.service_qty.values(), *self.part_qty.values()):
            v.set("0")
        self.labour.set("0")
        self.discount.set("0")
        self.amount_paid.set("0")
        self.payment_method.set("Cash")

        self.bill_dt = datetime.now()
        self.bill_no.set(self.next_bill_no())
        if self._after_id:
            self.root.after_cancel(self._after_id)
            self._after_id = None
        self.live_update()
        self.refresh_today()

    # ====================== SAVE ======================

    def validate_for_save(self, d):
        if not d["customer"]:
            messagebox.showerror("Missing Data", "Please enter the customer name.")
            return False
        if not d["vehicle"]:
            messagebox.showerror("Missing Data", "Please enter the vehicle number.")
            return False
        if d["phone"] and not re.fullmatch(r"\d{10}", d["phone"]):
            messagebox.showerror("Invalid Phone", "Phone number must be exactly 10 digits.")
            return False
        if d["total"] <= 0:
            messagebox.showerror("Empty Bill", "Add at least one service, part or labour charge.")
            return False
        return True

    def save_bill(self):
        try:
            d = self.calculate()
        except ValueError as err:
            messagebox.showerror("Invalid Input", str(err))
            return
        if not self.validate_for_save(d):
            return

        text = self.build_bill_text(d)
        try:
            self.db.execute(
                "INSERT OR REPLACE INTO bills VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (int(d["bill_no"]), d["datetime"].strftime("%Y-%m-%d %H:%M:%S"),
                 d["customer"], d["phone"], d["vehicle"], d["model"],
                 d["subtotal"], d["labour"], d["discount_amt"], d["gst"], d["total"],
                 d["method"], d["paid"], d["status"], text),
            )
            self.db.commit()

            os.makedirs(BILL_DIR, exist_ok=True)
            path = os.path.join(BILL_DIR, f"Garage_Bill_{d['bill_no']}.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
        except (sqlite3.Error, OSError) as err:
            messagebox.showerror("Save Error", str(err))
            return

        self.refresh_today()
        if messagebox.askyesno("Saved",
                               f"Bill {d['bill_no']} saved successfully.\n\nStart a new bill?"):
            self.new_bill(ask=False)

    # ====================== PRINT ======================

    def print_bill(self):
        try:
            d = self.calculate()
        except ValueError as err:
            messagebox.showerror("Invalid Input", str(err))
            return
        if d["total"] <= 0:
            messagebox.showerror("Empty Bill", "Generate a bill first.")
            return
        self.print_text(self.build_bill_text(d), d["bill_no"])

    def print_text(self, text, bill_no):
        path = os.path.join(tempfile.gettempdir(), f"Garage_Print_{bill_no}.txt")
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            if sys.platform == "win32":
                os.startfile(path, "print")
            else:
                subprocess.run(["lp", path], check=True)
        except (OSError, subprocess.CalledProcessError) as err:
            messagebox.showerror("Print Error", str(err))

    # ====================== HISTORY ======================

    def open_history(self):
        win = tk.Toplevel(self.root)
        win.title("Bill History")
        win.geometry("940x500")
        win.configure(bg=BG)
        win.transient(self.root)

        search = tk.StringVar()
        top = tk.Frame(win, bg=BG)
        top.pack(fill=tk.X, padx=8, pady=8)
        tk.Label(top, text="Search (bill no / name / phone / vehicle):",
                 bg=BG, fg="white").pack(side=tk.LEFT)
        entry = ttk.Entry(top, textvariable=search, width=30)
        entry.pack(side=tk.LEFT, padx=8)
        entry.focus_set()

        cols = ("bill", "date", "customer", "phone", "vehicle", "total", "status")
        heads = ("Bill No", "Date", "Customer", "Phone", "Vehicle", "Total (Rs)", "Status")
        widths = (80, 140, 170, 110, 110, 100, 90)

        tree = ttk.Treeview(win, columns=cols, show="headings", selectmode="browse")
        for c, h, w in zip(cols, heads, widths):
            tree.heading(c, text=h)
            tree.column(c, width=w, anchor="e" if c == "total" else "w")
        tree.tag_configure("UNPAID", foreground="#C0392B")
        tree.tag_configure("PARTIAL", foreground="#CA6F1E")
        sb = ttk.Scrollbar(win, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True, padx=(8, 0))

        info = tk.StringVar()
        tk.Label(win, textvariable=info, bg=BG, fg=GOLD,
                 font=("Segoe UI", 10, "bold")).pack(side=tk.BOTTOM, pady=6)

        def refresh(*_):
            tree.delete(*tree.get_children())
            q = f"%{search.get().strip()}%"
            rows = self.db.execute(
                """SELECT bill_no, date, customer, phone, vehicle, total, status FROM bills
                   WHERE CAST(bill_no AS TEXT) LIKE ? OR customer LIKE ?
                      OR phone LIKE ? OR vehicle LIKE ?
                   ORDER BY bill_no DESC""", (q, q, q, q)).fetchall()
            for r in rows:
                tree.insert("", tk.END, iid=str(r[0]), tags=(r[6],),
                            values=(r[0], r[1], r[2], r[3], r[4], f"{r[5]:,.2f}", r[6]))
            info.set(f"{len(rows)} bill(s)  |  Total: Rs {sum(r[5] for r in rows):,.2f}")

        def selected_text():
            sel = tree.selection()
            if not sel:
                messagebox.showinfo("History", "Select a bill first.", parent=win)
                return None, None
            row = self.db.execute("SELECT bill_text FROM bills WHERE bill_no=?",
                                  (int(sel[0]),)).fetchone()
            return sel[0], row[0] if row else None

        def view(event=None):
            bill_no, text = selected_text()
            if text is None:
                return
            v = tk.Toplevel(win)
            v.title(f"Bill {bill_no}")
            t = tk.Text(v, font=("Consolas", 10), width=BILL_WIDTH + 2, height=38)
            t.insert(tk.END, text)
            t.config(state="disabled")
            t.pack(padx=8, pady=8)
            ttk.Button(v, text="Print", command=lambda: self.print_text(text, bill_no)
                       ).pack(pady=(0, 8))

        def delete():
            bill_no, text = selected_text()
            if text is None:
                return
            if messagebox.askyesno("Delete", f"Permanently delete bill {bill_no}?", parent=win):
                self.db.execute("DELETE FROM bills WHERE bill_no=?", (int(bill_no),))
                self.db.commit()
                refresh()
                self.refresh_today()

        ttk.Button(top, text="Search", command=refresh).pack(side=tk.LEFT)
        ttk.Button(top, text="View / Print", command=view).pack(side=tk.RIGHT, padx=4)
        ttk.Button(top, text="Delete", command=delete).pack(side=tk.RIGHT)

        entry.bind("<Return>", refresh)
        search.trace_add("write", refresh)
        tree.bind("<Double-1>", view)
        refresh()

    # ====================== EXIT ======================

    def exit_app(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.db.close()
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    GarageBillingSystem(root)
    root.mainloop()
