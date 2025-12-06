Portfolio Pal

A No-Code Portfolio Generator with Secure Viewer Access

Overview

Portfolio Pal is a web application that allows users to create and view portfolio pages without writing any code. Users enter their information through a form, and the system generates a structured portfolio. Each user receives a unique visitor key that can be shared with others for secure viewing. The platform also supports complete data deletion for a fresh start.

Features

  Create a portfolio by entering personal and academic details

  View your generated portfolio after login

  Share your portfolio securely using a visitor key

  Allow others to access your portfolio only through a Visitor Key

  Delete all stored user data and restart

  User authentication system

Tech Stack

  Frontend: HTML, CSS

  Backend: Flask (Python)

  Templating: Jinja2

  Database: SQLite3

Installation
  git clone <repository-url>
  cd project
  python -m venv venv
  venv\Scripts\activate   # Windows
  pip install -r requirements.txt
  python app.py


Project Structure
project/
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── images/
│   │   ├── da1.png
│   │   ├── da2.png
│   │   ├── da3.png
│   │   ├── da4.png
│   │   ├── da5.png
│   │   ├── da6.png
│   │   ├── da7.png
│   │   ├── github.png
│   │   ├── gmail.png
│   │   ├── insta.jpg
│   │   ├── linkedin.jpg
│   │   ├── phone.png
│   │   └── website.png
│   │
│   └── js/
│       └── main.js
│
├── templates/
│   ├── index.html
│   ├── input.html
│   ├── login.html
│   ├── portfolio.html
│   ├── portfoliodownloadable.html
│   ├── signup.html
│   ├── visitor.html
│   └── visitorview.html
│
├── app.py
└── users.db


Usage

  Register and log in

  Enter your details to generate the portfolio

  View your portfolio from the dashboard

  Share your visitor key with others to let them view it

  Delete your data anytime if you want to start again

License

  This repository is intended for educational and personal use.

A No-Code Portfolio Generator with Secure Viewer Access

