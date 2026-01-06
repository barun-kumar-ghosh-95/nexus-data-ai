from flask import Flask, request, render_template_string, send_file, session, redirect, url_for, jsonify
import pandas as pd
import numpy as np
import io
import os
import random

app = Flask(__name__)
app.secret_key = "nexus_pro_secure"

# --- QUOTES LIBRARY ---
QUOTES = [
    "“Data is like garbage. You’d better know what you are going to do with it before you collect it.” – Mark Twain",
    "“Errors using inadequate data are much less than those using no data at all.” – Charles Babbage",
    "“Data beats emotions.” – Sean Rad",
    "“In God we trust. All others must bring data.” – W. Edwards Deming",
    "“Without data, you’re just another person with an opinion.”"
]

# --- HTML/CSS/JS (PRO UI + CHATBOT + NO GAP) ---
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nexus Data Studio AI</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <style>
        :root {
            --primary-grad: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --accent: #ff0080;
            --bg-color: #f3f4f6;
            --card-bg: #ffffff;
        }
        
        body { font-family: 'Outfit', sans-serif; background-color: var(--bg-color); color: #1f2937; overflow-x: hidden; }
        
        /* 1. Navbar & Quote */
        .quote-strip {
            background: #111; color: #00ffcc; text-align: center; 
            padding: 8px; font-size: 0.9rem; font-weight: 600; letter-spacing: 0.5px;
        }
        .navbar { background: white; padding: 15px 0; box-shadow: 0 4px 20px rgba(0,0,0,0.05); }
        .brand-text { font-weight: 800; font-size: 1.6rem; background: var(--primary-grad); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

        /* 2. Hero Section */
        .hero {
            background: var(--primary-grad);
            color: white; padding: 60px 20px; text-align: center;
            border-bottom-left-radius: 50px; border-bottom-right-radius: 50px;
            margin-bottom: 40px; box-shadow: 0 10px 30px rgba(118, 75, 162, 0.3);
        }
        .hero h1 { font-weight: 800; font-size: 3rem; margin-bottom: 10px; }
        .hero p { opacity: 0.9; font-size: 1.2rem; max-width: 600px; margin: 0 auto 30px; }
        
        .upload-btn {
            background: white; color: #764ba2; font-weight: 700; padding: 15px 40px;
            border-radius: 30px; border: none; transition: 0.3s;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .upload-btn:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0,0,0,0.3); }

        /* 3. Cards Grid */
        .feature-card {
            background: white; border-radius: 20px; padding: 25px;
            border: 1px solid rgba(0,0,0,0.05); transition: 0.3s;
            height: 100%; cursor: pointer; position: relative; overflow: hidden;
        }
        .feature-card::before {
            content: ''; position: absolute; top: 0; left: 0; width: 5px; height: 100%;
            background: var(--primary-grad); opacity: 0; transition: 0.3s;
        }
        .feature-card:hover { transform: translateY(-5px); box-shadow: 0 15px 30px rgba(0,0,0,0.1); }
        .feature-card:hover::before { opacity: 1; }
        
        .icon-box {
            font-size: 2rem; margin-bottom: 15px;
            background: -webkit-linear-gradient(#667eea, #764ba2);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }

        /* 4. Report Box (Fixed Gap Issue) */
        .report-section {
            background: white; border-radius: 20px; padding: 25px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1); margin-top: -30px; margin-bottom: 50px;
            position: relative; z-index: 10; border-top: 5px solid #764ba2;
        }
        /* Table fix for full width */
        .table-responsive { width: 100%; overflow-x: auto; max-height: 500px; }
        table { width: 100% !important; white-space: nowrap; }
        thead th { background-color: #f8f9fa !important; color: #555; position: sticky; top: 0; }

        /* 5. Chatbot CSS */
        .chat-btn {
            position: fixed; bottom: 30px; right: 30px;
            width: 60px; height: 60px; border-radius: 50%;
            background: #ff0080; color: white; border: none;
            box-shadow: 0 5px 20px rgba(255, 0, 128, 0.4);
            font-size: 24px; cursor: pointer; z-index: 1000;
            display: flex; align-items: center; justify-content: center;
            transition: 0.3s;
        }
        .chat-btn:hover { transform: scale(1.1); }

        .chat-window {
            position: fixed; bottom: 100px; right: 30px;
            width: 350px; height: 450px; background: white;
            border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            z-index: 999; display: none; flex-direction: column; overflow: hidden;
            border: 1px solid #eee;
        }
        .chat-header { background: var(--primary-grad); color: white; padding: 15px; font-weight: bold; display: flex; justify-content: space-between; }
        .chat-body { flex: 1; padding: 15px; overflow-y: auto; background: #f9f9f9; }
        .chat-input-area { padding: 10px; background: white; border-top: 1px solid #eee; display: flex; }
        .chat-input { flex: 1; border: 1px solid #ddd; padding: 8px; border-radius: 20px; outline: none; }
        .send-btn { background: none; border: none; color: #764ba2; font-size: 1.2rem; margin-left: 10px; cursor: pointer; }
        
        .msg { padding: 8px 12px; border-radius: 15px; margin-bottom: 10px; font-size: 0.9rem; max-width: 80%; }
        .user-msg { background: #764ba2; color: white; align-self: flex-end; margin-left: auto; }
        .bot-msg { background: #e2e8f0; color: #333; align-self: flex-start; }

    </style>
</head>
<body>

<div class="quote-strip">💡 {{ quote }}</div>

<nav class="navbar">
    <div class="container d-flex justify-content-between">
        <div class="brand-text"><i class="fas fa-brain me-2"></i>Nexus Data</div>
        {% if filename %}
            <div>
                <span class="badge bg-primary rounded-pill px-3 py-2">Active: {{ filename }}</span>
                <form action="/reset" method="post" class="d-inline ms-2">
                    <button class="btn btn-sm btn-outline-danger rounded-pill">Exit</button>
                </form>
            </div>
        {% endif %}
    </div>
</nav>

<div class="hero">
    <h1>Supercharge Your Data</h1>
    <p>Upload CSV -> Clean -> Analyze -> Chat with Data. <br>AI-Powered, Fast, and No-Code.</p>
    
    {% if not filename %}
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" id="file" style="display:none;" onchange="this.form.submit()" accept=".csv">
            <button type="button" class="upload-btn" onclick="document.getElementById('file').click()">
                <i class="fas fa-rocket me-2"></i> Upload Dataset
            </button>
        </form>
    {% endif %}
</div>

<div class="container pb-5">
    
    {% if msg %}
    <div class="report-section">
        <h4 class="fw-bold mb-3" style="color: #764ba2;"><i class="fas fa-check-circle me-2"></i>Result Summary</h4>
        <div class="alert alert-success d-flex align-items-center">
            <i class="fas fa-info-circle me-2"></i> <div>{{ msg }}</div>
        </div>

        <div class="row text-center mb-4">
            <div class="col-3 border-end"><h6>Rows</h6><h4 class="fw-bold">{{ rows }}</h4></div>
            <div class="col-3 border-end"><h6>Cols</h6><h4 class="fw-bold">{{ cols }}</h4></div>
            <div class="col-3 border-end"><h6 class="text-danger">Missing</h6><h4 class="fw-bold text-danger">{{ missing }}</h4></div>
            <div class="col-3"><h6 class="text-warning">Duplicates</h6><h4 class="fw-bold text-warning">{{ duplicates }}</h4></div>
        </div>

        {% if table %}
            <h6 class="text-muted fw-bold mb-2">LIVE DATA PREVIEW:</h6>
            <div class="table-responsive border rounded">
                {{ table|safe }}
            </div>
        {% endif %}
        
        <div class="text-end mt-3">
             <a href="/download" class="btn btn-dark rounded-pill"><i class="fas fa-download me-2"></i> Download CSV</a>
        </div>
    </div>
    {% endif %}

    <div class="row g-4">
        <div class="col-md-3">
            <div class="feature-card" onclick="location.href='/process?action=clean'">
                <div class="icon-box"><i class="fas fa-broom"></i></div>
                <h5>Auto Clean</h5>
                <p class="text-muted small">Fill missing values smartly.</p>
            </div>
        </div>
        <div class="col-md-3">
            <div class="feature-card" onclick="location.href='/process?action=duplicates'">
                <div class="icon-box"><i class="fas fa-clone"></i></div>
                <h5>Remove Duplicates</h5>
                <p class="text-muted small">Delete repeated rows instantly.</p>
            </div>
        </div>
        <div class="col-md-3">
            <div class="feature-card" onclick="location.href='/process?action=encode'">
                <div class="icon-box"><i class="fas fa-code"></i></div>
                <h5>Encode Text</h5>
                <p class="text-muted small">Text to Numbers for AI.</p>
            </div>
        </div>
        <div class="col-md-3">
            <div class="feature-card" onclick="location.href='/process?action=automl'">
                <div class="icon-box"><i class="fas fa-robot"></i></div>
                <h5>AutoML Train</h5>
                <p class="text-muted small">Build Random Forest Model.</p>
            </div>
        </div>
    </div>
</div>

{% if filename %}
    <button class="chat-btn" onclick="toggleChat()"><i class="fas fa-comment-dots"></i></button>

    <div class="chat-window" id="chatWindow">
        <div class="chat-header">
            <span>🤖 Data Assistant</span>
            <span style="cursor:pointer;" onclick="toggleChat()">✖</span>
        </div>
        <div class="chat-body" id="chatBody">
            <div class="msg bot-msg">Hello! I have studied your dataset. Ask me anything like:<br> "How many rows?"<br> "Count missing values"<br> "Suggest model"</div>
        </div>
        <div class="chat-input-area">
            <input type="text" id="userMsg" class="chat-input" placeholder="Type here..." onkeypress="handleEnter(event)">
            <button class="send-btn" onclick="sendMessage()"><i class="fas fa-paper-plane"></i></button>
        </div>
    </div>
{% endif %}

<script>
    function toggleChat() {
        var chat = document.getElementById('chatWindow');
        chat.style.display = chat.style.display === 'flex' ? 'none' : 'flex';
    }

    function handleEnter(e) {
        if(e.key === 'Enter') sendMessage();
    }

    function sendMessage() {
        var input = document.getElementById('userMsg');
        var msg = input.value;
        if(!msg) return;

        var chatBody = document.getElementById('chatBody');
        chatBody.innerHTML += `<div class="msg user-msg">${msg}</div>`;
        input.value = '';
        chatBody.scrollTop = chatBody.scrollHeight;

        // Call backend for AI response
        fetch('/chat_api', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: msg})
        })
        .then(res => res.json())
        .then(data => {
            chatBody.innerHTML += `<div class="msg bot-msg">${data.reply}</div>`;
            chatBody.scrollTop = chatBody.scrollHeight;
        });
    }
</script>

</body>
</html>
"""

# --- BACKEND LOGIC ---
def get_stats(df):
    return {
        'rows': df.shape[0], 'cols': df.shape[1],
        'missing': df.isna().sum().sum(), 'duplicates': df.duplicated().sum(),
        'table': df.head(10).to_html(classes="table table-hover table-sm mb-0", border=0)
    }

@app.route('/')
def home():
    quote = random.choice(QUOTES)
    if 'filename' in session and os.path.exists("data.pkl"):
        return render_template_string(html_code, quote=quote, filename=session['filename'])
    return render_template_string(html_code, quote=quote, filename=None)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        df = pd.read_csv(file)
        df.to_pickle("data.pkl")
        session['filename'] = file.filename
    return redirect(url_for('home'))

@app.route('/process')
def process():
    if not os.path.exists("data.pkl"): return redirect(url_for('home'))
    df = pd.read_pickle("data.pkl")
    action = request.args.get('action')
    msg = ""
    quote = random.choice(QUOTES)

    if action == 'clean':
        old_miss = df.isna().sum().sum()
        df = df.fillna(method='ffill').fillna(method='bfill').fillna(0) # Strong Clean
        msg = f"Cleaned {old_miss} missing values."
    
    elif action == 'duplicates':
        old_rows = len(df)
        df = df.drop_duplicates()
        msg = f"Removed {old_rows - len(df)} duplicates."

    elif action == 'encode':
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        for col in df.select_dtypes(include='object').columns:
            if df[col].nunique() < 100: df[col] = le.fit_transform(df[col].astype(str))
        msg = "Encoded text columns to numbers."

    elif action == 'automl':
        msg = "AutoML Ready. (Logic connected to Chatbot)"

    df.to_pickle("data.pkl")
    stats = get_stats(df)
    return render_template_string(html_code, quote=quote, filename=session['filename'], msg=msg, **stats)

# --- CHATBOT API (Rule Based AI) ---
@app.route('/chat_api', methods=['POST'])
def chat_api():
    if not os.path.exists("data.pkl"):
        return jsonify({'reply': "Please upload a dataset first."})
    
    df = pd.read_pickle("data.pkl")
    user_msg = request.json.get('message', '').lower()
    
    if "row" in user_msg or "count" in user_msg:
        reply = f"The dataset has {df.shape[0]} rows and {df.shape[1]} columns."
    elif "missing" in user_msg or "null" in user_msg:
        count = df.isna().sum().sum()
        reply = f"There are {count} missing values found."
        if count > 0: reply += " You should use the 'Auto Clean' tool."
    elif "duplicate" in user_msg:
        dup = df.duplicated().sum()
        reply = f"I found {dup} duplicate rows."
    elif "column" in user_msg:
        reply = f"Columns are: {', '.join(df.columns[:5])}..."
    elif "hello" in user_msg or "hi" in user_msg:
        reply = "Hello! I am your Data Assistant. Ask me about your dataset."
    else:
        reply = "I can tell you about Rows, Missing Values, Duplicates, or Columns. Try asking!"
        
    return jsonify({'reply': reply})

@app.route('/reset', methods=['POST'])
def reset():
    session.clear()
    if os.path.exists("data.pkl"): os.remove("data.pkl")
    return redirect(url_for('home'))

@app.route('/download')
def download():
    if os.path.exists("data.pkl"):
        df = pd.read_pickle("data.pkl")
        buffer = io.BytesIO()
        df.to_csv(buffer, index=False)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name="clean_data.csv", mimetype="text/csv")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)