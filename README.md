# 🚗 Car Garage Billing System

A desktop-based **Car Garage Billing System** developed using **Python and Tkinter**.
The application helps garage/service-center staff manage customer and vehicle details, calculate service and parts charges, generate invoices, save bills, search previous bills, and print invoices.

---

## 📖 Overview

The **Car Garage Billing System** is a user-friendly desktop application designed to simplify the billing process for automobile service centers.

Users can enter customer and vehicle information, select required garage services and parts, calculate labour charges, apply discounts, calculate **18% GST**, record payments, and generate a complete service bill.

The application provides a simple graphical interface with separate sections for customer details, services, parts, billing summary, and invoice generation.

---

## ✨ Features

* 🚗 Customer & vehicle information management
* 🧾 Automatic bill number generation
* 🔧 Garage service selection
* ⚙️ Vehicle parts/material selection
* 💰 Automatic service and parts calculation
* 👨‍🔧 Labour charge management
* 🧮 Automatic **18% GST calculation**
* 🎁 Discount calculation
* 💳 Multiple payment methods
* 💵 Amount paid and balance/change calculation
* 📄 Invoice generation
* 💾 Save bills as text files
* 🔍 Search previously saved bills
* 🖨️ Print generated bills
* 🔄 Clear/reset all information
* ❌ Safe application exit
* ⌨️ Keyboard shortcuts for Save and Print

---

## 🛠️ Technologies Used

| Technology       | Purpose                         |
| ---------------- | ------------------------------- |
| 🐍 Python 3.x    | Core programming language       |
| 🖼️ Tkinter      | GUI development                 |
| 💬 MessageBox    | Alerts and confirmation dialogs |
| 📂 OS Module     | File and directory management   |
| 🎲 Random Module | Bill number generation          |
| 🕒 Datetime      | Date and time generation        |
| 🖨️ Subprocess   | Printing support                |
| 🧱 OOP           | Application structure           |

---

## 📋 Garage Services

The application supports the following services:

* General Service
* Oil Change
* Car Washing
* Engine Service
* Brake Service
* Tyre Service
* Battery Service

### 💰 Service Pricing

| Service         |  Price |
| --------------- | -----: |
| General Service |   ₹800 |
| Oil Change      |   ₹500 |
| Car Washing     |   ₹300 |
| Engine Service  | ₹2,500 |
| Brake Service   | ₹1,200 |
| Tyre Service    |   ₹700 |
| Battery Service |   ₹500 |

---

## 🔩 Parts & Materials

The system supports the following vehicle parts:

* Engine Oil
* Oil Filter
* Air Filter
* Brake Pad
* Spark Plug
* Coolant
* Battery

### 💰 Parts Pricing

| Part       |  Price |
| ---------- | -----: |
| Engine Oil |   ₹650 |
| Oil Filter |   ₹250 |
| Air Filter |   ₹350 |
| Brake Pad  | ₹1,800 |
| Spark Plug |   ₹400 |
| Coolant    |   ₹500 |
| Battery    | ₹4,500 |

---

## 🧮 Billing Calculation

The system calculates the final bill using:

```text
Service Total
      +
Parts Total
      +
Labour Charge
      =
Taxable Amount
```

### GST

The application applies **18% GST** to the taxable amount.

```text
GST = Taxable Amount × 18%
```

### Discount

The user can enter a discount percentage from **0% to 100%**.

```text
Discount = Taxable Amount × Discount% / 100
```

### Grand Total

```text
Grand Total =
Taxable Amount + GST - Discount
```

The code validates the discount range and displays an error for invalid values.

---

## 💳 Payment Management

The application supports three payment methods:

* 💵 Cash
* 📱 UPI
* 💳 Card

Users can enter the amount paid, and the system automatically calculates either the customer's change or remaining amount due.

Example:

```text
Grand Total : ₹5,000
Amount Paid : ₹5,500

Change      : ₹500
```

---

## 🧾 Generated Invoice

The generated invoice contains:

* Bill number
* Date and time
* Customer name
* Phone number
* Vehicle number
* Car model
* Selected services
* Selected parts
* Service total
* Parts total
* Labour charge
* GST
* Discount
* Grand total
* Payment method
* Amount paid
* Balance/change

The invoice is displayed directly inside the application's billing area.

---

## 💾 Save Bill

Generated bills can be saved automatically inside the:

```text
garage_bills/
```

directory.

The bill is saved using the bill number:

```text
garage_bills/Garage_Bill_<BillNumber>.txt
```

For example:

```text
garage_bills/Garage_Bill_58241.txt
```

---

## 🔍 Search Bill

Previously saved bills can be searched using their **Bill Number**.

The application looks for the corresponding file inside the `garage_bills` directory and displays the saved invoice if it exists.

---

## 🖨️ Print Bill

The system provides a **PRINT** option for generated invoices.

* Windows uses the system print command.
* Linux/Unix systems use the `lp` printing command.

---

## ⌨️ Keyboard Shortcuts

| Shortcut   | Action     |
| ---------- | ---------- |
| `Ctrl + S` | Save Bill  |
| `Ctrl + P` | Print Bill |

---

## 📂 Project Structure

```text
Car-Garage-Billing-System/
│
├── billing.py
├── garage_bills/
│   └── Garage_Bill_XXXXX.txt
│
├── screenshots/
│   ├── home.png
│   ├── billing.png
│   └── invoice.png
│
└── README.md
```

> `garage_bills/` is created automatically when the first bill is saved.

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/siddharthgajbhare/Car-Garage-Billing-System.git
```

### 2. Navigate to the Project

```bash
cd Car-Garage-Billing-System
```

### 3. Run the Application

```bash
python billing.py
```

No external Python packages are required because the application uses Python's built-in modules.

---

## 🖥️ Application Interface

The application contains:

### 👤 Customer & Vehicle Details

Users can enter:

* Customer Name
* Phone Number
* Vehicle Number
* Car Model

A unique five-digit bill number is automatically generated.

### 🔧 Garage Services

Enter the quantity required for each garage service.

### 🔩 Parts / Materials

Enter the quantity of required vehicle parts.

### 🧾 Service Bill

The generated invoice is displayed in a scrollable billing area.

### 📊 Billing Summary

The summary displays:

* Service Total
* Parts Total
* Labour Charge
* GST
* Discount
* Grand Total
* Payment
* Amount Paid
* Balance/Change

---

## 🔄 Reset / Clear

The **CLEAR** button resets:

* Customer details
* Vehicle details
* Services
* Parts
* Billing values
* Payment details
* Bill number
* Generated invoice

The application also asks for confirmation before clearing the information.

---

## 🎯 Future Enhancements

Possible improvements include:

* 🗄️ MySQL database integration
* 👤 User login & authentication
* 📊 Admin dashboard
* 📦 Inventory management
* 👨‍🔧 Mechanic management
* 📅 Service appointment booking
* 📱 Customer service history
* 📄 PDF invoice generation
* 🧾 Professional GST invoice
* 📧 Invoice sharing through email
* 📱 WhatsApp invoice sharing
* 📷 Barcode/QR code support
* ☁️ Cloud database integration
* 📈 Sales and revenue reports
* 🔐 Role-based access control

---

## 🤝 Contributing

Contributions are welcome!

### 1. Fork the repository

### 2. Create a feature branch

```bash
git checkout -b feature-name
```

### 3. Make your changes

### 4. Commit your changes

```bash
git add .
git commit -m "Added new feature"
```

### 5. Push your branch

```bash
git push origin feature-name
```

### 6. Create a Pull Request

---

## 📄 License

This project is developed for **educational and learning purposes**.

---

## 👨‍💻 Owner & Developer

### **Siddharth Gajbhare**

💻 Python Developer
🛠️ Project Owner & Developer

**GitHub:**
https://github.com/siddharthgajbhare

---

## ⭐ Support

If you found this project useful, please consider giving the repository a ⭐ **Star**.

Thank you for visiting! 🚗🔧

**Car Garage Billing System — Making Garage Billing Simple & Efficient.**
