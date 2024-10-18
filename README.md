## HMart: Full-Stack E-Commerce Web Application
![Screenshot (343)](https://github.com/user-attachments/assets/02ac8938-17b1-4579-87df-4ba2bc99a60d)



HMARt is a full-stack e-commerce platform built using Django, specifically designed for electronics shopping. It features user authentication, product listings, a shopping cart, and secure payment integration with Razorpay. This README will guide you through setting up, installing, and using the HMARt application.

### Table of Contents

* Introduction
* Prerequisites
* Installation
* Getting Started
* Usage
* Features

### Introduction

HMARt is designed to provide users with a seamless online shopping experience for electronic products. It allows users to browse products, add them to a shopping cart, and securely make payments using Razorpay.

### Prerequisites

Before setting up HMARt, ensure you have the following installed:

* Python 3.8 or higher
* Django 3.x or higher
* Required Python packages:
    * django
    * djangorestframework
    * razorpay
    * pillow (for image handling)
* Any other dependencies mentioned in `requirements.txt`

### Installation

**Clone the repository:**

* git clone [invalid URL removed]
* cd HMART-ecommerce


**Create a Python virtual environment (optional but recommended):**

* python -m venv venv
* source venv/bin/activate  # On Windows: venv\Scripts\activate

**Install Required Packages:**

* pip install -r requirements.txt   

**Set Up the Django Project:**

* python manage.py migrate
* python manage.py createsuperuser

**Configure Razorpay Payment Gateway:**
* Add your Razorpay API keys in the project's settings (settings.py):

    * RAZORPAY_API_KEY = 'your_api_key'
    * RAZORPAY_API_SECRET = 'your_api_secret'

**Start the Development Server:**

* python manage.py runserver

### Getting Started

To get started with HMARt:

1. Clone the repository and install the required dependencies as described in the Installation section.
2. Configure Razorpay by adding your API keys.
3. Run the server and access the application through `http://localhost:8000`.

### Usage

Once the development server is running:

* **Sign up/Login:** Users can register or log in to their accounts.
* **Browse Products:** Explore a variety of electronic products available for purchase.
* **Add to Cart:** Add items to the shopping cart.
* **Checkout:** Complete the purchase by making a payment via Razorpay.

### Features

* **User Authentication:** Secure login and registration functionality.
* **Product Listing:** View and filter electronics products.
* **Shopping Cart:** Add, remove, and update items in the cart.
* **Razorpay Payment Gateway:** Integrated payment system for seamless transactions.
