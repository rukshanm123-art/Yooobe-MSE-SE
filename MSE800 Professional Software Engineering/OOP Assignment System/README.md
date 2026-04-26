# Car Rental Management System (CUI)

**Course:** MSE800 Professional Software Engineering  
**Assessment:** Assignment 1 – Object-Oriented Programming  
**Developer:** Rukshan De Silva  
**Student ID:** 270802602  
**Programme:** Master of Software Engineering  
**Language:** Python 3.10+  

---

## 1. Project Overview
The **Car Rental Management System** is a command-line-based application developed using Python and advanced Object-Oriented Programming (OOP) principles. It automates the rental workflow of a car rental company by enabling **Admins** to manage vehicles and booking approvals, while **Customers** can browse available cars and request bookings with automated validation and pricing.

**Version 2** of the system extends the initial implementation by introducing intelligent business logic such as **dynamic pricing with long-term rental discounts**, **explainable pricing breakdowns**, **smart alternative car recommendations**, and **risk-aware booking management**. The system remains **self-contained, robust, and easy to run**, requiring no manual configuration.

The application addresses real-world issues including **input typos** (e.g., `"admisw"`), **invalid data symbols** (e.g., `"$"`), and booking constraint violations, while maintaining stability and usability.

---

## 2. Key Features

**User Management**
* Secure user registration and login.
* Role-based access control (**Admin / Customer**).
* **Factory Method pattern** for controlled and validated user creation.
* Prevention of unauthorized role assignment and registration errors.

**Car Management (Admin)**
* **Add, view, update, and remove** vehicles (Full CRUD).
* Track mileage, pricing, and availability status.
* Enforce **minimum and maximum rental duration constraints**.

### Admin Registration Secret Key
To prevent unauthorised Admin account creation, the system requires a secret key during Admin registration.

* **Admin Secret Key:** `yoobee`

This key is validated using the Factory Method pattern and ensures that only authorised users can register as Admins. This mechanism is implemented for educational purposes and demonstrates controlled role assignment.


**Rental Booking (Customer)**
* View available cars with clear feedback when no vehicles are available.
* Request bookings with **automated validation** of rental duration limits.
* **Dynamic rental fee calculation** based on daily rate and rental duration.
* **Long-term rental discounts**:
  * 5% discount for rentals of 7 days or more  
  * 10% discount for rentals of 14 days or more
* **Explainable pricing breakdown**, displaying base cost, applied discount, and final payable amount.
* **Smart alternative car recommendations** when booking requests fail due to availability or rental constraints.

**Booking Management (Admin)**
* View all pending booking requests.
* **Approve or reject** booking requests with immediate confirmation messages.
* Automatic update of vehicle availability upon approval.
* **Risk-aware booking management**, displaying customer risk levels to support informed decisions.

**System Reliability**
* **Robust input validation** and error handling to prevent terminal crashes.
* Centralized system logging in the `logs/` directory.
* Partial **data persistence** using SQLite for users and vehicles.

---

## 3. Object-Oriented Design
The system demonstrates all core OOP principles:
* **Encapsulation**: Sensitive data such as passwords and system state are protected using private and protected attributes.
* **Abstraction**: The `User` abstract base class defines mandatory behaviour for all user types.
* **Inheritance**: `Admin` and `Customer` inherit common functionality from the `User` class.
* **Polymorphism**: Role-specific menu behaviour is implemented through method overriding.

Version 2 enhancements were implemented through behavioural extensions of existing classes, preserving structural stability and maintainability.

---

## 4. Design Patterns Used
* **Singleton Pattern**: Ensures only one instance of `RentalSystem` exists to centrally manage users, vehicles, bookings, and persistence logic.
* **Factory Method Pattern**: Centralizes and validates the creation of Admin and Customer objects to prevent unauthorized access or role typos.

---

## 5. Database Integration (SQLite)
* The system uses **SQLite** for lightweight data persistence.
* The database file (`rental.db`) is stored in the `database/` directory.
* User and vehicle records are **automatically restored on system startup**.
* No manual database setup is required.
* Booking records are maintained in memory for this submission.

---

## 6. Project Structure
**CarRentalProject/**
* **main.py**: Application entry point (CLI logic).
* **requirements.txt**: Project dependency declaration (Standard Library only).
* **README.md**: User & developer documentation.
* **logs/**: Automatically generated system logs.
* **database/**: Contains `rental.db` SQLite database.
* **src/**: Contains `models.py`, `factory.py`, and `system.py`.

---

## 7. Installation & Execution

**Prerequisites**
* Python 3.10 or higher.
* No external libraries required.

**Running the System**
1. Extract the project folder.
2. Navigate to the project root directory.
3. Run the application: `python main.py`.

---

## 8. Known Limitations & Future Enhancements
* **Known Limitations**: Passwords are stored in plain text (educational scope). Booking history is not persisted across sessions.
* **Future Enhancements**: Password hashing, full booking persistence, analytics, AI-driven demand forecasting, a Graphical User Interface (GUI), and cloud deployment.

---

## 9. Licensing
This project is developed for **educational purposes only** as part of the MSE800 module at Yoobee College.

**Credits:** Developed by **Rukshan De Silva**, 2026.
