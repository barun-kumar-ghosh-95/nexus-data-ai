Nexus Data Studio - AI-Powered AutoML Tool

**Nexus Data Studio** ek professional, no-code data science platform hai jo manual data cleaning aur preprocessing ko automate karta hai. Isse users bina coding ke apne raw datasets ko ML-ready bana sakte hain aur AI chatbot se interact karke insights nikal sakte hain.

### 🌐link-https://huggingface.co/spaces/barunkumar9905/Nexus-Data-AI

---

## ✨ Features

* Smart Data Cleaning:** Missing values ko fill karne ke liye AI-driven Mean/Mode strategies ka use.
* Duplicate Removal:** 1-click mein redundant rows ko identify aur remove karne ki suvidha.
* Auto Encoding:** Categorical text data ko machine learning ke liye numerical format mein convert karna.
* AI Data Assistant (Chatbot):** Dataset se related sawal poochne ke liye built-in intelligent assistant (e.g., "How many rows?", "Show missing values").
* Real-time Analysis Report:** Har action ke baad 'Before vs After' ki detail report aur live data preview.

## Tech Stack

| Library/Tool | Role |
| --- | --- |
| **Flask** | Backend server aur URL routing handle karne ke liye. |
| **Pandas** | High-performance data manipulation aur analysis ke liye. |
| **Scikit-Learn** | ML algorithms (Random Forest) aur preprocessing (Encoding/Scaling) ke liye. |
| **NumPy** | Numerical computations aur array operations ke liye. |
| **Bootstrap 5** | Responsive aur modern web design ke liye. |
| **Gunicorn** | Production-level server par app run karne ke liye. |

---

##Project Structure

```text
nexus-data-studio/
│
├── app.py              # Main Flask application logic
├── requirements.txt    # List of dependencies for deployment
├── README.md           # Project documentation
└── data.pkl            # Temporary data storage (Pickle format)

```

---

##How to Run Locally

1. **Repository Clone**
```bash
git clone https://github.com/your-username/nexus-data-studio.git
cd nexus-data-studio

```


2. **Dependencies Install**
```bash
pip install -r requirements.txt

```


3. **App Start**
```bash
python app.py

```


4. Browser open:-  `http://127.0.0.1:5000`
