# Library Management System (Flask + PostgreSQL)

A modern, full-stack **Library Management System** built using **Flask** and **PostgreSQL**, featuring a clean UI, CRUD functionality, and production-grade deployment on **Render**.

---

## 🚀 Live Demo

🔗 **Live URL:** (https://library-manager-0rlg.onrender.com/add)

---

## 📌 Features

- Add books with title, author, genre, and location
- View all books in a clean, responsive table
- Delete books with instant updates
- Persistent data storage using PostgreSQL
- Modern SaaS-style UI with clean typography and layout
- Production deployment on Render (Free Tier)

---

## 🛠 Tech Stack

**Backend**
- Python
- Flask
- Gunicorn

**Database**
- PostgreSQL (Render Managed)

**Frontend**
- HTML5
- CSS3 (custom modern UI)

**Deployment**
- Render Web Service
- Render PostgreSQL

**Version Control**
- Git
- GitHub


---

## 🗄 Database Schema

```sql
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    genre TEXT,
    location TEXT NOT NULL
);


