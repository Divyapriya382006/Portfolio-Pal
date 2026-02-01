# PortfolioPal

## 📌 Project Overview
**PortfolioPal** is a web application designed to help users create a personal portfolio website **without needing to know coding**.

Users simply enter their details into the platform, and PortfolioPal dynamically generates a complete portfolio website for them. The project focuses on accessibility, security, and ease of use, making portfolio creation simple and efficient.

---

## 🎯 Key Features
- No-code portfolio website creation
- User authentication (signup & login)
- Dynamic portfolio generation
- Secure access using **username + private key**
- Shareable portfolio access for recruiters and peers
- Clean and structured UI

---

## 🔐 Secure Portfolio Access
One of the standout features of PortfolioPad is its **private key system**:
- Each user is assigned a private key
- Only users with the **correct username and private key** can view a portfolio
- Ensures privacy and controlled sharing of portfolio data

---

## 🧱 Technology Stack

### Frontend
- HTML
- CSS
- Jinja Templates

### Backend
- Python
- Flask

### Database
- SQLite

---

## ⚙️ Application Workflow
1. User signs up and logs in
2. User enters personal, academic, and professional details
3. Data is stored in the database
4. Flask and Jinja templates dynamically generate a portfolio website
5. Portfolio can be accessed securely using username and private key

---

## 🗂️ Project Structure
├── app.py
├── templates/
│ ├── index.html
│ ├── login.html
│ ├── signup.html
│ ├── dashboard.html
│ └── portfolio.html
├── static/
│ └── css/
├── database/
│ └── portfolio.db
├── README.md
└── requirements.txt


---

## ⚠️ Known Limitation
During deployment, a major limitation was identified:

- SQLite is not supported for persistent storage on platforms like Render
- Application data (login credentials and portfolio details) gets reset on refresh or redeploy
- This causes loss of user-entered data

This limitation was due to the ephemeral filesystem used by the deployment platform.

---

## 🚧 Future Enhancements
- Migrate from SQLite to a cloud-based database (PostgreSQL / MySQL)
- Improve deployment stability
- Add portfolio templates
- Enable custom domain support
- Enhance UI responsiveness
- Add export/download portfolio feature

---

## 🏁 Conclusion
PortfolioPad demonstrates a full-stack web application built using Flask, focusing on usability, security, and dynamic content generation. Despite deployment limitations, the project showcases strong backend logic, templating integration, and thoughtful feature design.

This project serves as a foundation for a scalable portfolio-building platform.

