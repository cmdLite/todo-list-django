# Smart Todo App 📝✨

A classic Django-based Todo application, completely refactored to use robust Class-Based Views, augmented with an integrated Google Gemini AI engine that automatically breaks down or suggests new tasks. 

## Features

- **Classic CRUD**: Easily add, delete, update, and patch tasks.
- **Toggle State**: Tasks can be marked complete right from the main dashboard via interactive checkboxes without needing a page refresh wait (native HTML form submission over CBVs).
- **AI Task Suggestions**: Stuck on a project? Type a goal (e.g. "Plan a wedding") and hit "Suggest". The Google Gemini 2.0 Flash model will suggest actionable step-by-step tasks, which you can simply click to ingest right into your list!
- **Clean Architecture**: Designed strictly using Django Class-Based Views (CBV) for maximum extensibility.

---

## 🛠️ How to Run the App (Locally)

### 1. Prerequisites
- Python 3.10+ installed.
- Ensure you have a standard terminal (CMD, PowerShell, or bash) open in the project root directory.

### 2. Setup a Virtual Environment
It is heavily recommended to use a virtual environment so the app's dependencies don't collide with your PC.

**On Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```
**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Once your virtual environment is active (you'll see `(venv)` in your terminal prompt), run:
```bash
pip install -r requirements.txt
```

### 4. Setting up the Built-in Database
Django relies on an SQLite database out of the box. Initialize it with:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Setup your AI API Key
The AI feature depends on the free Google Gemini platform.
1. Get a **FREE API Key** from [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Set it as an environment variable in your console BEFORE running the server.

**On Windows (Powershell):**
```powershell
$env:GEMINI_API_KEY="your-api-key-here"
```
**On macOS/Linux:**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

### 6. Run the Server
Start the development server using:
```bash
python manage.py runserver
```

Navigate to [http://127.0.0.1:8000/task/](http://127.0.0.1:8000/task/) in your browser to see the app in action! It handles everything out of the box gracefully. 
