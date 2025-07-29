# 📚 Placement Preparation Platform

A full-stack web application designed for IITM BS Data Science students to share placement preparation tips, peer advice, and engage in mentorship activities.

---

## ⚙️ Tech Stack

- **Frontend:** Vue.js
- **Backend:** Flask (Python)
- **Database:** SQLite (can be extended)
- **Asynchronous Tasks:** Celery + Redis
- **Email Notifications:** SMTP via MailHog (for testing)

---

## 🚀 Getting Started

### 🔧 Backend Setup

1. Navigate to the backend folder:

```bash
cd path/to/server
```
2. Install dependencies:

```bash
pip install -r requirements.txt
```
3. Start the backend server:

```bash
python main.py
```
4. Start Redis (for Celery):

```bash

redis-server
```

5. Start Celery worker (in a new terminal):

```bash
celery -A main.cel_app worker -l info
```
6. Start MailHog (for email testing):

```bash
mailhog
```
Access MailHog dashboard at http://localhost:8025

### 🌐 Frontend Setup
1. Navigate to the frontend folder:

```bash
cd path/to/client
```
2. Install dependencies:

```bash
npm install
```
3. Start the frontend dev server:

```bash
npm run dev
```
Access the app at http://localhost:5173

### 🔄 Features
- JWT-based authentication

- Follow/unfollow users

- Post creation, editing, deletion

- Asynchronous export of user posts (CSV + image zip)

- Daily reminder emails if inactive

- Monthly engagement reports (PDF via email)

- Redis caching for feed and posts

- Modular and scalable backend

### 📌 Notes
- Daily and monthly email jobs use Celery + Redis with smtplib and MailHog for email testing.

- All background tasks are asynchronous where applicable.

- Deployment-ready with minimal changes (e.g., replace MailHog with production SMTP).

### ✅ Future Improvements

- Switch to PostgreSQL or MongoDB for production

- Deploy to cloud with Docker and CI/CD
