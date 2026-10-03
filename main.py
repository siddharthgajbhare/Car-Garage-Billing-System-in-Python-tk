//littlbit done
from tkinter import *
from tkinter import messagebox, filedialog
from datetime import datetime
import random
import os
import sys
import subprocess


class Garage_Billing_System:

    def __init__(self, root):

        self.root = root
        self.root.geometry("1350x760+0+0")
        self.root.configure(bg="#17202A")
        self.root.title("Car Garage Billing System")
        self.root.resizable(False, False)

        # ================= VARIABLES =================

        self.customer_name = StringVar()
        self.phone = StringVar()
        self.vehicle_no = StringVar()
        self.car_model = StringVar()
        self.bill_no = StringVar()
        self.service_date = StringVar()

        self.generate_bill_number()

        # Services
        self.general_service = IntVar()
        self.oil_change = IntVar()
        self.car_wash = IntVar()
        self.engine_service = IntVar()
        self.brake_service = IntVar()
        self.tyre_service = IntVar()
        self.battery_service = IntVar()

        # Parts
        self.engine_oil = IntVar()
        self.oil_filter = IntVar()
        self.air_filter = IntVar()
        self.brake_pad = IntVar()
        self.spark_plug = IntVar()
        self.coolant = IntVar()
        self.battery = IntVar()

        # Billing
        self.service_total = StringVar(value="0 Rs")
        self.parts_total = StringVar(value="0 Rs")
        self.labour_charge = StringVar(value="0 Rs")
        self.gst = StringVar(value="0 Rs")
        self.discount = StringVar(value="0")
        self.grand_total = StringVar(value="0 Rs")

        self.payment_method = StringVar(value="Cash")
        self.amount_paid = StringVar(value="0")
        self.balance = StringVar(value="0 Rs")

        # ================= TITLE =================

        Label(
            self.root,
            text="CAR GARAGE BILLING SYSTEM",
            font=("Arial Black", 22),
            bg="#2874A6",
            fg="white",
            bd=10,
            relief=RIDGE
        ).pack(fill=X)

        # ================= CUSTOMER DETAILS =================

        details = LabelFrame(
            self.root,
            text="Customer & Vehicle Details",
            font=("Arial Black", 12),
            bg="#2874A6",
            fg="white",
            bd=8,
            relief=GROOVE
        )

        details.place(
            x=0,
            y=75,
            relwidth=1,
            height=100
        )

        Label(
            details,
            text="Customer Name",
            font=("Arial Black", 11),
            bg="#2874A6",
            fg="white"
        ).grid(row=0, column=0, padx=8, pady=5)

        Entry(
            details,
            width=20,
            textvariable=self.customer_name
        ).grid(row=0, column=1)

        Label(
            details,
            text="Phone",
            font=("Arial Black", 11),
            bg="#2874A6",
            fg="white"
        ).grid(row=0, column=2, padx=8)

        Entry(
            details,
            width=18,
            textvariable=self.phone
        ).grid(row=0, column=3)

        Label(
            details,
            text="Vehicle No.",
            font=("Arial Black", 11),
            bg="#2874A6",
            fg="white"
        ).grid(row=0, column=4, padx=8)

        Entry(
            details,
            width=18,
            textvariable=self.vehicle_no
        ).grid(row=0, column=5)

        Label(
            details,
            text="Car Model",
            font=("Arial Black", 11),
            bg="#2874A6",
            fg="white"
        ).grid(row=0, column=6, padx=8)

        Entry(
            details,
            width=18,
            textvariable=self.car_model
        ).grid(row=0, column=7)

        Label(
            details,
            text="Bill No.",
            font=("Arial Black", 11),
            bg="#2874A6",
            fg="white"
        ).grid(row=1, column=0, padx=8)

        Entry(
            details,
            width=20,
            textvariable=self.bill_no,
            state="readonly"
        ).grid(row=1, column=1)

        Label(
            details,
            text="Date",
            font=("Arial Black", 11),
            bg="#2874A6",
            fg="white"
        ).grid(row=1, column=2, padx=8)

        Label(
            details,
            text=datetime.now().strftime("%d-%m-%Y %I:%M %p"),
            font=("Arial Black", 10),
            bg="#2874A6",
            fg="white"
        ).grid(row=1, column=3)

        # ================= SERVICES =================

        services = LabelFrame(
            self.root,
            text="Garage Services",
            font=("Arial Black", 12),
            bg="#D6EAF8",
            fg="#154360",
            bd=8,
            relief=GROOVE
        )

        services.place(
            x=5,
            y=185,
            width=330,
            height=370
        )

        service_items = [

            ("General Service", self.general_service),
            ("Oil Change", self.oil_change),
            ("Car Washing", self.car_wash),
            ("Engine Service", self.engine_service),
            ("Brake Service", self.brake_service),
            ("Tyre Service", self.tyre_service),
            ("Battery Service", self.battery_service)
        ]

        for row, (name, variable) in enumerate(service_items):

            Label(
                services,
                text=name,
                font=("Arial Black", 10),
                bg="#D6EAF8",
                fg="#154360"
            ).grid(
                row=row,
                column=0,
                padx=5,
                pady=10
            )

            Entry(
                services,
                width=10,
                textvariable=variable
            ).grid(
                row=row,
                column=1,
                padx=10
            )

        # ================= PARTS =================

        parts = LabelFrame(
            self.root,
            text="Parts / Materials",
            font=("Arial Black", 12),
            bg="#D6EAF8",
            fg="#154360",
            bd=8,
            relief=GROOVE
        )

        parts.place(
            x=345,
            y=185,
            width=330,
            height=370
        )

        parts_items = [

            ("Engine Oil", self.engine_oil),
            ("Oil Filter", self.oil_filter),
            ("Air Filter", self.air_filter),
            ("Brake Pad", self.brake_pad),
            ("Spark Plug", self.spark_plug),
            ("Coolant", self.coolant),
            ("Battery", self.battery)
        ]

        for row, (name, variable) in enumerate(parts_items):

            Label(
                parts,
                text=name,
                font=("Arial Black", 10),
                bg="#D6EAF8",
                fg="#154360"
            ).grid(
                row=row,
                column=0,
                padx=5,
                pady=10
            )

            Entry(
                parts,
                width=10,
                textvariable=variable
            ).grid(
                row=row,
                column=1,
                padx=10
            )

        # ================= BILL AREA =================

        bill_frame = Frame(
            self.root,
            bd=8,
            relief=GROOVE,
            bg="white"
        )

        bill_frame.place(
            x=1010,
            y=185,
            width=330,
            height=370
        )

        Label(
            bill_frame,
            text="SERVICE BILL",
            font=("Arial Black", 16),
            bg="#D6EAF8",
            fg="#154360",
            bd=5,
            relief=GROOVE
        ).pack(fill=X)

        scrollbar = Scrollbar(
            bill_frame,
            orient=VERTICAL
        )

        scrollbar.pack(
            side=RIGHT,
            fill=Y
        )

        self.bill_area = Text(
            bill_frame,
            font=("Consolas", 9),
            yscrollcommand=scrollbar.set
        )

        self.bill_area.pack(
            fill=BOTH,
            expand=True
        )

        scrollbar.config(
            command=self.bill_area.yview
        )

        # ================= BILLING SUMMARY =================

        summary = LabelFrame(
            self.root,
            text="Billing Summary",
            font=("Arial Black", 12),
            bg="#2874A6",
            fg="white",
            bd=8,
            relief=GROOVE
        )

        summary.place(
            x=0,
            y=565,
            relwidth=1,
            height=185
        )

        # Column 1

        Label(
            summary,
            text="Service Total",
            font=("Arial Black", 10),
            bg="#2874A6",
            fg="white"
        ).grid(row=0, column=0, padx=8, pady=5)

        Entry(
            summary,
            width=18,
            textvariable=self.service_total,
            state="readonly"
        ).grid(row=0, column=1)

        Label(
            summary,
            text="Parts Total",
            font=("Arial Black", 10),
            bg="#2874A6",
            fg="white"
        ).grid(row=1, column=0, padx=8)

        Entry(
            summary,
            width=18,
            textvariable=self.parts_total,
            state="readonly"
        ).grid(row=1, column=1)

        Label(
            summary,
            text="Labour Charge",
            font=("Arial Black", 10),
            bg="#2874A6",
            fg="white"
        ).grid(row=2, column=0, padx=8)

        Entry(
            summary,
            width=18,
            textvariable=self.labour_charge
        ).grid(row=2, column=1)

        # Column 2

        Label(
            summary,
            text="GST %",
            font=("Arial Black", 10),
            bg="#2874A6",
            fg="white"
        ).grid(row=0, column=2, padx=8)

        Label(
            summary,
            text="18%",
            font=("Arial Black", 10),
            bg="#2874A6",
            fg="white"
        ).grid(row=0, column=3)

        Label(
            summary,
            text="GST Amount",
            font=("Arial Black", 10),
            bg="#2874A6",
            fg="white"
        ).grid(row=1, column=2)

        Entry(
            summary,
            width=18,
            textvariable=self.gst,
            state="readonly"
        ).grid(row=1, column=3)

        Label(
            summary,
            text="Discount %",
            font=("Arial Black", 10),
            bg="#2874A6",
            fg="white"
        ).grid(row=2, column=2)

        Entry(
            summary,
            width=18,
            textvariable=self.discount
        ).grid(row=2, column=3)

        # Column 3

        Label(
            summary,
            text="Grand Total",
            font=("Arial Black", 11),
            bg="#2874A6",
            fg="white"
        ).grid(row=0, column=4, padx=10)

        Entry(
            summary,
            width=18,
            font=("Arial Black", 11),
            textvariable=self.grand_total,
            state="readonly"
        ).grid(row=0, column=5)

        Label(
            summary,
            text="Payment",
            font=("Arial Black", 10),
            bg="#2874A6",
            fg="white"
        ).grid(row=1, column=4)

        OptionMenu(
            summary,
            self.payment_method,
            "Cash",
            "UPI",
            "Card"
        ).grid(row=1, column=5)

        Label(
            summary,
            text="Amount Paid",
            font=("Arial Black", 10),
            bg="#2874A6",
            fg="white"
        ).grid(row=2, column=4)

        Entry(
            summary,
            width=18,
            textvariable=self.amount_paid
        ).grid(row=2, column=5)

        Label(
            summary,
            text="Balance / Change",
            font=("Arial Black", 10),
            bg="#2874A6",
            fg="white"
        ).grid(row=3, column=4)

        Entry(
            summary,
            width=18,
            textvariable=self.balance,
            state="readonly"
        ).grid(row=3, column=5)

        # ================= BUTTONS =================

        button_frame = Frame(
            summary,
            bg="#154360",
            bd=5,
            relief=GROOVE
        )

        button_frame.place(
            x=760,
            y=75,
            width=555,
            height=90
        )

        Button(
            button_frame,
            text="TOTAL",
            font=("Arial Black", 10),
            width=10,
            bg="#D6EAF8",
            fg="#154360",
            command=self.calculate_total
        ).grid(row=0, column=0, padx=5, pady=8)

        Button(
            button_frame,
            text="SAVE",
            font=("Arial Black", 10),
            width=10,
            bg="#D6EAF8",
            fg="#154360",
            command=self.save_bill
        ).grid(row=0, column=1, padx=5)

        Button(
            button_frame,
            text="PRINT",
            font=("Arial Black", 10),
            width=10,
            bg="#D6EAF8",
            fg="#154360",
            command=self.print_bill
        ).grid(row=0, column=2, padx=5)

        Button(
            button_frame,
            text="SEARCH",
            font=("Arial Black", 10),
            width=10,
            bg="#D6EAF8",
            fg="#154360",
            command=self.search_bill
        ).grid(row=0, column=3, padx=5)

        Button(
            button_frame,
            text="CLEAR",
            font=("Arial Black", 10),
            width=10,
            bg="#D6EAF8",
            fg="#154360",
            command=self.clear
        ).grid(row=0, column=4, padx=5)

        self.show_intro()

        self.root.bind(
            "<Control-s>",
            lambda event: self.save_bill()
        )

        self.root.bind(
            "<Control-p>",
            lambda event: self.print_bill()
        )

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.exit_app
        )

    # ================= BILL NUMBER =================

    def generate_bill_number(self):

        self.bill_no.set(
            str(random.randint(10000, 99999))
        )

    # ================= INTRO =================

    def show_intro(self):

        self.bill_area.delete(
            1.0,
            END
        )

        self.bill_area.insert(
            END,
            "\tCAR GARAGE\n"
        )

        self.bill_area.insert(
            END,
            "\tSERVICE CENTER\n"
        )

        self.bill_area.insert(
            END,
            "================================\n"
        )

        self.bill_area.insert(
            END,
            "Bill No : "
            + self.bill_no.get()
            + "\n"
        )

        self.bill_area.insert(
            END,
            "Date    : "
            + datetime.now().strftime(
                "%d-%m-%Y %I:%M %p"
            )
            + "\n"
        )

        self.bill_area.insert(
            END,
            "================================\n"
        )

        self.bill_area.insert(
            END,
            "Service\t\tQty\tAmount\n"
        )

        self.bill_area.insert(
            END,
            "--------------------------------\n"
        )

    # ================= TOTAL =================

    def calculate_total(self):

        try:

            # Service Prices

            service_prices = {

                "General Service":
                    self.general_service.get() * 800,

                "Oil Change":
                    self.oil_change.get() * 500,

                "Car Washing":
                    self.car_wash.get() * 300,

                "Engine Service":
                    self.engine_service.get() * 2500,

                "Brake Service":
                    self.brake_service.get() * 1200,

                "Tyre Service":
                    self.tyre_service.get() * 700,

                "Battery Service":
                    self.battery_service.get() * 500
            }

            service_total = sum(
                service_prices.values()
            )

            # Parts Prices

            parts_prices = {

                "Engine Oil":
                    self.engine_oil.get() * 650,

                "Oil Filter":
                    self.oil_filter.get() * 250,

                "Air Filter":
                    self.air_filter.get() * 350,

                "Brake Pad":
                    self.brake_pad.get() * 1800,

                "Spark Plug":
                    self.spark_plug.get() * 400,

                "Coolant":
                    self.coolant.get() * 500,

                "Battery":
                    self.battery.get() * 4500
            }

            parts_total = sum(
                parts_prices.values()
            )

            # Labour

            labour = float(
                self.labour_charge.get() or 0
            )

            # GST

            taxable_amount = (
                service_total +
                parts_total +
                labour
            )

            gst_amount = round(
                taxable_amount * 0.18,
                2
            )

            # Discount

            discount_percent = float(
                self.discount.get() or 0
            )

            if discount_percent < 0 or discount_percent > 100:

                messagebox.showerror(
                    "Error",
                    "Discount must be between 0 and 100."
                )

                return

            discount_amount = round(
                taxable_amount *
                discount_percent /
                100,
                2
            )

            grand_total = round(
                taxable_amount +
                gst_amount -
                discount_amount,
                2
            )

            # Set values

            self.service_total.set(
                f"{service_total:.2f} Rs"
            )

            self.parts_total.set(
                f"{parts_total:.2f} Rs"
            )

            self.gst.set(
                f"{gst_amount:.2f} Rs"
            )

            self.grand_total.set(
                f"{grand_total:.2f} Rs"
            )

            # Payment

            paid = float(
                self.amount_paid.get() or 0
            )

            difference = paid - grand_total

            if difference >= 0:

                self.balance.set(
                    f"Change: {difference:.2f} Rs"
                )

            else:

                self.balance.set(
                    f"Due: {abs(difference):.2f} Rs"
                )

            self.create_bill(
                service_prices,
                parts_prices,
                labour,
                gst_amount,
                discount_amount,
                grand_total
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Please enter valid numeric values."
            )

    # ================= CREATE BILL =================

    def create_bill(
        self,
        services,
        parts,
        labour,
        gst,
        discount,
        total
    ):

        self.show_intro()

        self.bill_area.insert(
            END,
            f"Customer : {self.customer_name.get()}\n"
        )

        self.bill_area.insert(
            END,
            f"Phone    : {self.phone.get()}\n"
        )

        self.bill_area.insert(
            END,
            f"Vehicle  : {self.vehicle_no.get()}\n"
        )

        self.bill_area.insert(
            END,
            f"Model    : {self.car_model.get()}\n"
        )

        self.bill_area.insert(
            END,
            "================================\n"
        )

        # Services

        for name, amount in services.items():

            if amount > 0:

                quantity = 0

                if name == "General Service":
                    quantity = self.general_service.get()

                elif name == "Oil Change":
                    quantity = self.oil_change.get()

                elif name == "Car Washing":
                    quantity = self.car_wash.get()

                elif name == "Engine Service":
                    quantity = self.engine_service.get()

                elif name == "Brake Service":
                    quantity = self.brake_service.get()

                elif name == "Tyre Service":
                    quantity = self.tyre_service.get()

                elif name == "Battery Service":
                    quantity = self.battery_service.get()

                self.bill_area.insert(
                    END,
                    f"{name[:15]:15} {quantity:3} {amount:.2f}\n"
                )

        # Parts

        self.bill_area.insert(
            END,
            "\nPARTS\n"
        )

        for name, amount in parts.items():

            if amount > 0:

                quantity = 0

                if name == "Engine Oil":
                    quantity = self.engine_oil.get()

                elif name == "Oil Filter":
                    quantity = self.oil_filter.get()

                elif name == "Air Filter":
                    quantity = self.air_filter.get()

                elif name == "Brake Pad":
                    quantity = self.brake_pad.get()

                elif name == "Spark Plug":
                    quantity = self.spark_plug.get()

                elif name == "Coolant":
                    quantity = self.coolant.get()

                elif name == "Battery":
                    quantity = self.battery.get()

                self.bill_area.insert(
                    END,
                    f"{name[:15]:15} {quantity:3} {amount:.2f}\n"
                )

        self.bill_area.insert(
            END,
            "--------------------------------\n"
        )

        self.bill_area.insert(
            END,
            f"Service Total : {self.service_total.get()}\n"
        )

        self.bill_area.insert(
            END,
            f"Parts Total   : {self.parts_total.get()}\n"
        )

        self.bill_area.insert(
            END,
            f"Labour        : {labour:.2f} Rs\n"
        )

        self.bill_area.insert(
            END,
            f"GST (18%)     : {gst:.2f} Rs\n"
        )

        self.bill_area.insert(
            END,
            f"Discount      : {discount:.2f} Rs\n"
        )

        self.bill_area.insert(
            END,
            "--------------------------------\n"
        )

        self.bill_area.insert(
            END,
            f"GRAND TOTAL   : {total:.2f} Rs\n"
        )

        self.bill_area.insert(
            END,
            f"Payment       : {self.payment_method.get()}\n"
        )

        self.bill_area.insert(
            END,
            f"Paid          : {self.amount_paid.get()} Rs\n"
        )

        self.bill_area.insert(
            END,
            f"{self.balance.get()}\n"
        )

        self.bill_area.insert(
            END,
            "================================\n"
        )

        self.bill_area.insert(
            END,
            "\tTHANK YOU!\n"
        )

        self.bill_area.insert(
            END,
            "\tVISIT AGAIN\n"
        )

    # ================= SAVE =================

    def save_bill(self):

        if not self.bill_area.get(
            1.0,
            END
        ).strip():

            messagebox.showerror(
                "Error",
                "Please generate the bill first."
            )

            return

        os.makedirs(
            "garage_bills",
            exist_ok=True
        )

        filename = (
            "garage_bills/Garage_Bill_"
            + self.bill_no.get()
            + ".txt"
        )

        try:

            with open(
                filename,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(
                    self.bill_area.get(
                        1.0,
                        END
                    )
                )

            messagebox.showinfo(
                "Success",
                f"Bill saved successfully.\n\n{filename}"
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

    # ================= SEARCH =================

    def search_bill(self):

        bill_number = filedialog.askstring(
            "Search Bill",
            "Enter Bill Number:"
        )

        if not bill_number:
            return

        filename = (
            "garage_bills/Garage_Bill_"
            + bill_number
            + ".txt"
        )

        if os.path.exists(filename):

            with open(
                filename,
                "r",
                encoding="utf-8"
            ) as file:

                data = file.read()

            self.bill_area.delete(
                1.0,
                END
            )

            self.bill_area.insert(
                END,
                data
            )

        else:

            messagebox.showerror(
                "Not Found",
                "Bill not found."
            )

    # ================= PRINT =================

    def print_bill(self):

        if not self.bill_area.get(
            1.0,
            END
        ).strip():

            messagebox.showerror(
                "Error",
                "Generate a bill first."
            )

            return

        filename = (
            "Garage_Print_"
            + self.bill_no.get()
            + ".txt"
        )

        try:

            with open(
                filename,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(
                    self.bill_area.get(
                        1.0,
                        END
                    )
                )

            if sys.platform == "win32":

                os.startfile(
                    os.path.abspath(filename),
                    "print"
                )

            else:

                subprocess.run(
                    ["lp", filename]
                )

        except Exception as error:

            messagebox.showerror(
                "Print Error",
                str(error)
            )

    # ================= CLEAR =================

    def clear(self):

        if not messagebox.askyesno(
            "Clear",
            "Clear all information?"
        ):
            return

        variables = [

            self.general_service,
            self.oil_change,
            self.car_wash,
            self.engine_service,
            self.brake_service,
            self.tyre_service,
            self.battery_service,

            self.engine_oil,
            self.oil_filter,
            self.air_filter,
            self.brake_pad,
            self.spark_plug,
            self.coolant,
            self.battery
        ]

        for variable in variables:
            variable.set(0)

        self.customer_name.set("")
        self.phone.set("")
        self.vehicle_no.set("")
        self.car_model.set("")

        self.service_total.set("0 Rs")
        self.parts_total.set("0 Rs")
        self.labour_charge.set("0")
        self.gst.set("0 Rs")
        self.discount.set("0")
        self.grand_total.set("0 Rs")

        self.payment_method.set("Cash")
        self.amount_paid.set("0")
        self.balance.set("0 Rs")

        self.generate_bill_number()

        self.show_intro()

    # ================= EXIT =================

    def exit_app(self):

        if messagebox.askyesno(
            "Exit",
            "Are you sure you want to exit?"
        ):

            self.root.destroy()


# ================= MAIN =================

if __name__ == "__main__":

    root = Tk()

    app = Garage_Billing_System(root)

    root.mainloop()
