# 🚗 Car Garage Billing System

A desktop-based **Car Garage Billing System** built using **Python and Tkinter**.
The application helps garage/service-center staff manage customer and vehicle details, calculate service and spare-parts charges, generate bills, save bills, search previous bills, and print invoices.

---

## 📌 Features

* 👤 Customer information management
* 🚘 Vehicle number and car model management
* 🧾 Automatic bill number generation
* 📅 Automatic date and time
* 🔧 Garage service billing
* 🛠️ Spare parts/material billing
* 👨‍🔧 Labour charge calculation
* 💰 GST calculation
* 🎁 Discount calculation
* 💳 Cash / UPI / Card payment options
* 💵 Amount paid and balance/change calculation
* 🧾 Professional bill preview
* 💾 Save bills as `.txt` files
* 🔍 Search previously saved bills
* 🖨️ Print generated bills
* 🧹 Clear billing form
* ❌ Exit confirmation
* ⌨️ Keyboard shortcuts

---

## 🛠️ Technologies Used

| Technology | Purpose                     |
| ---------- | --------------------------- |
| Python     | Main programming language   |
| Tkinter    | GUI development             |
| Random     | Bill number generation      |
| OS         | File and directory handling |
| Datetime   | Date and time               |
| Subprocess | Printing support            |

## The application uses Tkinter widgets such as `Label`, `Entry`, `Button`, `LabelFrame`, `Text`, `Scrollbar`, and `OptionMenu`.

## 📂 Project Structure

```text
Car-Garage-Billing-System/
│
├── garage_billing.py
├── garage_bills/
│   └── Garage_Bill_XXXXX.txt
│
├── README.md
└── screenshots/
    └── garage-billing.png
```

---

## 🔧 Garage Services

The system supports the following services:

* General Service
* Oil Change
* Car Washing
* Engine Service
* Brake Service
* Tyre Service
* Battery Service

These services are defined in the application as selectable quantity-based billing items.

---

## 🛠️ Parts & Materials

The system includes:

* Engine Oil
* Oil Filter
* Air Filter
* Brake Pad
* Spark Plug
* Coolant
* Battery

Parts are entered with quantities and included automatically in the bill calculation.

---

## 💰 Billing Calculation

The application calculates:

```text
Service Total
      +
Parts Total
      +
Labour Charge
      +
GST
      -
Discount
      =
Grand Total
```

The current implementation calculates GST at **18%** and allows the user to enter a discount percentage.

---

## 💳 Payment System

Supported payment methods:

```text
Cash
UPI
Card
```

The application also accepts the amount paid and calculates either:

```text
Change
```

or

```text
Due Amount
```

## depending on the payment amount.

## 🧾 Bill Generation

The generated bill contains:

```text
CAR GARAGE
SERVICE CENTER

Bill No
Date
Customer
Phone
Vehicle Number
Car Model

Services
Parts

Service Total
Parts Total
Labour
GST
Discount

GRAND TOTAL
Payment Method
Amount Paid
Balance / Change
```

## The bill is displayed inside the application's dedicated service-bill area.

## 💾 Save Bill

Generated bills can be saved as text files.

Bills are stored inside:

```text
garage_bills/
```

Example:

```text
garage_bills/
└── Garage_Bill_12345.txt
```

The application automatically creates the `garage_bills` directory if it doesn't already exist.

---

## 🔍 Search Bill

Previously saved bills can be searched using their bill number.

Example:

```text
Enter Bill Number:
12345
```

The application searches:

```text
garage_bills/Garage_Bill_12345.txt
```

and displays the saved bill in the bill area.

---

## 🖨️ Print Bill

The generated bill can be sent to the system printer.

On Windows, the application uses the operating system's print command, while other systems use the `lp` command.

---

## 🚀 Installation

### 1. Install Python

Download and install Python 3.x.

Check your installation:

```bash
python --version
```

---

### 2. Clone the Repository

```bash
git clone https://github.com/yourusername/car-garage-billing-system.git
```

```bash
cd car-garage-billing-system
```

---

### 3. Run the Application

```bash
python garage_billing.py
```

No external Python packages are required because the application uses Python's built-in Tkinter and standard-library modules.

---

## ⌨️ Keyboard Shortcuts

| Shortcut   | Action     |
| ---------- | ---------- |
| `Ctrl + S` | Save Bill  |
| `Ctrl + P` | Print Bill |

These shortcuts are registered directly by the application.

---

## 🖥️ Application Workflow

```text
Start Application
       ↓
Enter Customer Details
       ↓
Enter Vehicle Details
       ↓
Select Services
       ↓
Add Parts / Materials
       ↓
Enter Labour Charge
       ↓
Apply Discount
       ↓
Calculate GST
       ↓
Calculate Grand Total
       ↓
Enter Payment Details
       ↓
Generate Bill
       ↓
 ┌─────┼─────┐
 ↓     ↓     ↓
Save  Print Search
```

---

## 📸 Screenshots

Add your application screenshot here:

```markdown
![Car Garage Billing System](screenshots/garage-billing.png)
```

Recommended screenshot:

```text
screenshots/
└── garage-billing.png
```

---

## 🎯 Project Objectives

The main objectives of this project are:

* Automate garage billing operations
* Reduce manual calculation errors
* Maintain customer and vehicle information
* Calculate service and parts charges quickly
* Generate professional bills
* Save previous bills for future reference
* Provide a simple and user-friendly desktop interface

---

## 🔮 Future Enhancements

Possible future improvements:

* 📊 Garage dashboard
* 👥 Customer database
* 🚘 Vehicle service history
