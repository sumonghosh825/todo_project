
# 🧾 To-Do List Web Application – User Manual

Welcome to the To-Do List Web App! This guide will walk you through all the features and how to use them.

---

## 📌 Features Overview
- ✅ **User Registration & Login**
- 👤 **Profile Management**
- 🔐 **Account Security Settings**
- 🗂️ **Task Management (Add, Edit, Delete)**
- 📂 **Filter Tasks by Category or Status**

---

## 🚀 Getting Started

### 1. **Visit the Home Page**
URL: `http://localhost:8000/`

From the home page, you can:
- Register for a new account
- Login if you already have one

---

## 👥 User Authentication

### ➕ Register
- Go to `/register/`
- Fill in your username, email, and password
- Click `Register`

### 🔐 Login
- Go to `/login/`
- Enter your credentials and log in
- You will be redirected to the dashboard

### 🚪 Logout
- Click the `Logout` link or go to `/logout/`

---

## 👤 Profile Management

### 📝 View/Update Profile
- Go to `/profile/`
- Your basic info will be shown
- To update, click `Edit` and submit the form

---

## 🔐 Security Settings

### 🔄 Update Security Info
- Go to `/load_security_content/` to view current info
- Use `/update_security/` to update your password or security details

---

## 📋 Task Management

### ➕ Add a Task
- Go to `/tasks/add/`
- Enter title, description, due date, category, and status
- Click `Save`

### 📝 Edit a Task
- Go to `/tasks/edit/<task_id>/`
- Modify task details and submit

### ❌ Delete a Task
- Go to `/tasks/delete/<task_id>/`
- Confirm to delete the task permanently

---

## 🗂️ Task Filtering

### 📁 By Category
- Go to `/tasks/load/<category>/` (e.g. `/tasks/load/work/`)
- View only tasks from the selected category

### 🚦 By Status
- Go to `/tasks/status/<status>/` (e.g. `/tasks/status/pending/`)
- Filter tasks by their status

---

## 🧑‍💻 Developer Info (Optional Section)
- Framework: Django
- Frontend: HTML, CSS, JS (with optional AJAX)
- Database: SQLite (default, can be switched)
- Compatible with Python 3.x

---

## 🆘 Need Help?
If something isn’t working, you can:
- Check console logs or Django error logs
- Make sure you’ve run all migrations (`python manage.py migrate`)
- Run the server using: `python manage.py runserver`
