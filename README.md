# 🟠 Hacker News Clone (Django)

A **Hacker News–style web application** built using **Django**, inspired by the core features of  
[https://news.ycombinator.com](https://news.ycombinator.com).

This project focuses on **server-rendered pages**, **clean UI**, and **core community features**
like posts, comments, karma, jobs, and search.

---

## 🚀 Features

### 🔐 Authentication
- User signup & login
- Custom user model
- User profiles with karma and bio

### 📰 Submissions (Articles)
- Submit links or text posts
- Upvote articles
- Edit & delete **only your own posts**
- Comment count per article

### 💬 Comments
- Nested (threaded) comments
- Reply to comments
- Edit & delete **only your own comments**

### 🧑 User Profiles
- View user profile (`/user/<username>/`)
- Joined date
- Karma score
- Number of posts
- Editable bio (owner only)

### ⭐ Karma System
- Karma increases via upvotes
- Displayed on user profiles
- Used as a reputation score

### 💼 Jobs Section
- Submit job posts
- List job postings
- Jobs older than **30 days are auto-deleted**

### 🔍 Search
- Search by **username**
- Search by **article title/text**
- Username search shows **all articles by that user**
- Search term highlighted in results

### 🎨 UI & UX
- Hacker News–style minimal UI
- Consistent layout across pages
- Sticky footer using Flexbox
- Clean pagination

---

## 🛠 Tech Stack

- **Backend:** Django
- **Frontend:** Django Templates + CSS
- **Database:** SQLite (default)
- **Auth:** Custom Django User Model
- **Language:** Python 3

---

## 📁 Project Structure

```
Hackernews/
├── core/ # Submissions, users, profiles
├── comments/ # Comments & replies
├── jobs/ # Job posts
├── templates/ # HTML templates
├── static/ # CSS, images
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

git clone <your-repo-url>
cd Hackernews

### 2️⃣ Create virtual environment
python -m venv venv
source venv/bin/activate

### 3️⃣ Install dependencies
pip install -r requirements.txt

### 4️⃣ Apply migrations

python manage.py makemigrations
python manage.py migrate

### 5️⃣ Create superuser (optional)

python manage.py createsuperuser

### 6️⃣ Run development server

python manage.py runserver
Open in browser:

    http://127.0.0.1:8000/
    
## 🔑 Key Design Decisions

- Uses CustomUser instead of default auth.User

- Permissions enforced in templates and views

- No frontend frameworks (pure Django)

- Clean, readable, maintainable code

- Focused on learning real-world Django patterns

## 🔒 Security & Permissions

- Only authors can edit/delete their posts

- Only authors can edit/delete their comments

- Profile editing restricted to owner

- Job deletion restricted to poster

- Backend checks prevent unauthorized access

## 🎯 Learning Outcomes

- This project demonstrates:

- Django ORM

- Custom authentication

- Template inheritance

- Access control

- Search logic

- Real-world feature design

## 📜 License

This project is for learning and educational purposes.