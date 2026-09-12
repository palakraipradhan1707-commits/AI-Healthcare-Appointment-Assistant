# 🏥 AI Healthcare Appointment Assistant

An AI-powered healthcare appointment assistant that helps users identify the appropriate healthcare department based on their symptoms and provides an available doctor and appointment slot.

The project uses **Python Flask**, **Groq Llama AI**, **Pandas**, and a simple **HTML/CSS/JavaScript** frontend.

> ⚠️ **Disclaimer:** This project is an academic prototype and is not a replacement for professional medical advice or emergency medical services.

---

## 📌 Project Overview

The **AI Healthcare Appointment Assistant** is designed to make the initial healthcare appointment process easier.

A user enters:

* Name
* Age
* Symptoms or health problem

The system processes the information using an AI model and identifies the appropriate department:

* 🩺 General
* 🚑 Emergency
* 🧠 Mental Health

After identifying the department, the system checks the doctor data stored in a CSV file and displays an available doctor and appointment slot.

---

## ✨ Features

* 🤖 AI-based symptom classification
* 🏥 Automatic department/ward selection
* 👨‍⚕️ Doctor availability checking
* 📅 Appointment slot suggestion
* 🚑 Emergency symptom detection
* 🧠 Mental-health related query detection
* 🌐 Web-based user interface
* 🔄 Frontend and backend communication using REST API
* 📊 Doctor information stored using CSV
* 📱 Responsive interface
* 🔐 API key kept outside the source code

---

## 🛠️ Technologies Used

| Technology   | Purpose                    |
| ------------ | -------------------------- |
| Python       | Backend programming        |
| Flask        | Web framework              |
| Groq         | AI API                     |
| Llama 3.3    | AI language model          |
| LangChain    | AI model integration       |
| Pandas       | Doctor data management     |
| HTML         | Webpage structure          |
| CSS          | User interface design      |
| JavaScript   | Frontend functionality     |
| CSV          | Doctor information storage |
| Git & GitHub | Version control            |

---

## 🏗️ Project Structure

```text
AI-Healthcare-Appointment-Assistant/
│
├── app.py
├── doctors.csv
├── requirements.txt
├── .gitignore
├── README.md
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    └── script.js
```

---

## 🔄 How the Project Works

```text
User
  ↓
HTML/CSS/JavaScript Frontend
  ↓
POST /api/triage
  ↓
Flask Backend
  ↓
Groq + Llama AI
  ↓
Symptom Classification
  ↓
Department Selection
  ↓
Doctor Availability Check
  ↓
JSON Response
  ↓
Frontend Displays Result
```

---

## 🧠 AI Classification

The AI assistant classifies a patient's query into one of three categories:

### 1. General

For common health problems such as:

* Mild fever
* Headache
* Cold
* Minor stomach problems

### 2. Emergency

For potentially serious symptoms such as:

* Severe chest pain
* Difficulty breathing
* Severe bleeding
* Unconsciousness
* Major accidents

### 3. Mental Health

For concerns such as:

* Anxiety
* Panic attacks
* Stress
* Other mental-health related concerns

The application also performs basic emergency and crisis keyword checks before using the AI classification.

---

## 👨‍⚕️ Doctor Data

Doctor information is stored in `doctors.csv`.

Example:

```csv
doctor_name,ward,status,next_slot,slot_minutes
Dr. Sharma,general,active,09:00,20
Dr. Iyer,general,active,09:15,20
Dr. Khan,emergency,active,08:30,10
Dr. Rao,emergency,active,08:30,10
Dr. Mehta,mental_health,active,10:00,30
Dr. Gupta,mental_health,active,10:00,30
```

The backend reads this information using Pandas and selects an available doctor for the required department.

---

## 🚀 Installation

### Step 1: Clone the repository

```bash
git clone https://github.com/palakraipradhan1707-commits/AI-Healthcare-Appointment-Assistant.git
```

### Step 2: Enter the project folder

```bash
cd AI-Healthcare-Appointment-Assistant
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Configure the Groq API Key

Do **not** put your API key directly inside `app.py`.

Create a `.env` file in the project folder:

```text
GROQ_API_KEY=YOUR_GROQ_API_KEY
```

Make sure `.env` is included in `.gitignore`:

```text
.env
```

Never upload your API key to GitHub.

---

## ▶️ Run the Application

Start the Flask server:

```bash
python app.py
```

The terminal should show a local address similar to:

```text
http://127.0.0.1:5000
```

Open this address in your browser.

---

## 🧪 Example Input

### General Health

```text
Name: Rahul
Age: 22
Problem: I have mild fever and headache
```

Expected department:

```text
General
```

### Emergency

```text
Name: Amit
Age: 45
Problem: I have severe chest pain
```

Expected department:

```text
Emergency
```

### Mental Health

```text
Name: Priya
Age: 21
Problem: I am having anxiety and panic attacks
```

Expected department:

```text
Mental Health
```

---

## 🔌 API Endpoint

The main backend API is:

```text
POST /api/triage
```

Example request:

```json
{
    "name": "Rahul",
    "age": 22,
    "query": "I have mild fever and headache"
}
```

The Flask backend processes the request and returns a JSON response containing:

* Patient information
* Selected department
* AI reasoning
* Doctor information
* Next appointment slot
* Appointment duration

---

## 🔐 Security

The Groq API key should be stored as an environment variable and should never be committed to GitHub.

The `.gitignore` file prevents sensitive files such as `.env` from being uploaded.

If an API key is accidentally exposed, it should be revoked and replaced immediately.

---

## ⚠️ Limitations

This project is currently an academic prototype.

Some limitations include:

* Doctor availability is stored in memory.
* Appointment data is not stored in a permanent database.
* Restarting the Flask server resets doctor availability.
* The AI classification is not a medical diagnosis.
* The application should not be used for real medical decision-making.
* Authentication and user accounts are not implemented.

---

## 🔮 Future Improvements

Possible future improvements include:

* 🗄️ SQLite/MySQL database
* 👨‍⚕️ Doctor dashboard
* 👤 Patient login and registration
* 📅 Real appointment booking
* 📧 Email/SMS appointment notifications
* 🔐 User authentication
* 🏥 Multiple hospital support
* 📊 Admin dashboard
* 💬 AI chatbot interface
* 📱 Mobile application
* ☁️ Cloud deployment
* 📈 Appointment history and analytics

---

## 🎓 Academic Project

**Project Name:** AI Healthcare Appointment Assistant

**Domain:** Artificial Intelligence / Healthcare / Automation

**Technologies:** Python, Flask, Groq, Llama, Pandas, HTML, CSS, JavaScript

**Purpose:** To demonstrate how AI and web technologies can be combined to automate the initial healthcare appointment and department-selection process.

---

## 👩‍💻 Author

**Palak Pradhan**

GitHub:
https://github.com/palakraipradhan1707-commits

---

## 📄 License

This project is created for educational and academic purposes.
