# 🚗 Car Garage Billing System

A **Python-based desktop billing application** for car garages and service centers. The system provides an easy-to-use GUI for creating bills, calculating GST and discounts, managing payments, storing bill history, and printing invoices.

## 📌 Features

- 🧾 Create professional garage bills
- 🚘 Customer and vehicle details management
- 🔧 Predefined garage services and spare parts
- 🔢 Quantity-based automatic billing
- 💰 Automatic service, parts, labour, and subtotal calculation
- 🎯 Discount calculation
- 🧮 GST calculation after discount
- 💳 Payment methods:
  - Cash
  - UPI
  - Card
- 💵 Payment status:
  - PAID
  - PARTIAL
  - UNPAID
- 🔄 Live bill calculation while entering data
- 📱 10-digit phone number validation
- 🔢 Quantity and money input validation
- 🗃️ SQLite database for bill storage
- 🔢 Automatic sequential bill numbers
- 🔍 Bill history search
- 👁️ View previous bills
- 🖨️ Print bills
- 🗑️ Delete bills from history
- 📊 Today's bill count and total sales
- ⌨️ Keyboard shortcuts
- 🪟 Resizable GUI
- 📄 Bills are also saved as `.txt` files

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Application development |
| Tkinter | Graphical User Interface |
| SQLite3 | Database management |
| Regular Expressions | Input validation |
| OS / Subprocess | File handling and printing |

## 📂 Project Structure

```text
Car-Garage-Billing-System/
│
├── garage_billing.py
├── garage_billing.db
├── garage_bills/
│   ├── Garage_Bill_10001.txt
│   ├── Garage_Bill_10002.txt
│   └── ...
│
└── README.md
```

> `garage_billing.db` and `garage_bills/` are created automatically when the application runs.

## ⚙️ Requirements

- Python 3.8 or higher
- Tkinter
- SQLite3

Most Python installations already include **Tkinter** and **SQLite3**.

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/car-garage-billing-system.git
```

### 2. Open the project directory

```bash
cd car-garage-billing-system
```

### 3. Run the application

```bash
python garage_billing.py
```

For some systems:

```bash
python3 garage_billing.py
```

## 🖥️ How to Use

### 1. Enter Customer Details

Enter:

- Customer Name
- Phone Number
- Vehicle Number
- Car Model

### 2. Select Services

Choose the required quantity for services such as:

- General Service
- Oil Change
- Car Washing
- Engine Service
- Brake Service
- Tyre Service
- Battery Service

### 3. Select Parts

Add required parts such as:

- Engine Oil
- Oil Filter
- Air Filter
- Brake Pad
- Spark Plug
- Coolant
- Battery

### 4. Add Billing Details

Enter:

- Labour Charge
- Discount percentage
- Payment method
- Amount paid

The application automatically calculates:

```text
Service Total
+ Parts Total
+ Labour
----------------
Subtotal
- Discount
----------------
Taxable Amount
+ GST
----------------
Grand Total
```

### 5. Save the Bill

Click **SAVE** or press:

```text
Ctrl + S
```

The bill is stored in the SQLite database and also saved as a text file.

### 6. Print the Bill

Click **PRINT** or press:

```text
Ctrl + P
```

### 7. View Bill History

Click **HISTORY** or press:

```text
Ctrl + H
```

Bills can be searched using:

- Bill Number
- Customer Name
- Phone Number
- Vehicle Number

### 8. Create a New Bill

Click **NEW / CLEAR** or press:

```text
Ctrl + N
```

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + S` | Save Bill |
| `Ctrl + P` | Print Bill |
| `Ctrl + N` | New Bill |
| `Ctrl + H` | Open History |
| `F5` | Calculate Total |

## 💰 GST Calculation

The system calculates GST **after applying the discount**.

Example:

```text
Subtotal       = ₹10,000
Discount 10%   = ₹1,000
Taxable Amount = ₹9,000
GST 18%        = ₹1,620
Grand Total    = ₹10,620
```

## 💳 Payment Status

The application automatically determines the payment status.

```text
Paid Amount >= Grand Total
        ↓
      PAID
```

```text
Paid Amount > 0
        ↓
     PARTIAL
```

```text
Paid Amount = 0
        ↓
     UNPAID
```

The system also displays either the **change** or **balance due**.

## 🗃️ Database

The application uses **SQLite** to store bill information.

Database file:

```text
garage_billing.db
```

The database stores:

- Bill number
- Date and time
- Customer details
- Vehicle details
- Services
- Parts
- Subtotal
- Labour
- Discount
- GST
- Total
- Payment method
- Amount paid
- Payment status
- Bill text

## 🧾 Bill Storage

Saved bills are automatically stored inside:

```text
garage_bills/
```

Example:

```text
Garage_Bill_10001.txt
Garage_Bill_10002.txt
Garage_Bill_10003.txt
```

## ⚙️ Customization

Services and parts can easily be modified in the Python file.

### Services

```python
SERVICES = {
    "General Service": 800,
    "Oil Change": 500,
    "Car Washing": 300,
}
```

### Parts

```python
PARTS = {
    "Engine Oil": 650,
    "Oil Filter": 250,
    "Brake Pad": 1800,
}
```

### GST

GST can be changed using:

```python
GST_RATE = 18
```

### Garage Name

```python
GARAGE_NAME = "CAR GARAGE"
GARAGE_TAGLINE = "SERVICE CENTER"
```

## 🔐 Input Validation

The system includes validation for:

- Phone numbers
- Quantity fields
- Money fields
- Discount percentage
- Negative values
- Required customer name
- Required vehicle number

This helps prevent incorrect billing information.

## 🖨️ Printing

The application creates a temporary text file and sends it to the system's default printer.

On Windows, it uses the default Windows printing mechanism.

On Linux, it uses the `lp` command.

## 🔮 Future Enhancements

Possible improvements include:

- 📄 PDF invoice generation
- 🧾 Professional invoice templates
- 📧 Email bill to customers
- 📱 WhatsApp bill sharing
- 📊 Monthly sales reports
- 📈 Sales dashboard
- 👨‍🔧 Employee management
- 📦 Spare-parts inventory management
- 🔐 Admin login system
- ☁️ Cloud database backup
- 📱 Mobile application
- 💳 Online payment integration

## 👨‍💻 Author

**Siddharth Gajbhare**

### Project

**Car Garage Billing System**

Built using **Python, Tkinter, and SQLite**.

## 📜 License

This project is created for **educational and project purposes**. You are free to modify and improve it according to your requirements.
