from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "universal_reviewer_2026"

@app.route('/')
@app.route('/login')
def home():
    return render_template('index.html')

@app.route('/login_action', methods=['POST'])
def login_action():
    user = request.form.get('username')
    pw = request.form.get('password')
    if user == 'admin' and pw == '123':
        session['user'] = user
        return redirect(url_for('dashboard'))
    return "Invalid! <a href='/'>Retry</a>"

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('home'))
    return render_template('dashboard.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    code = data.get("code", "").strip()
    lang = data.get("language", "").lower()
    issues = []
    score = 100

    if not code:
        return jsonify({"score": 0, "label": "EMPTY", "color": "#94a3b8", "issues": []})

    lines = code.split('\n')

    # --- 🐍 PYTHON STRICT LOGIC ---
    if lang == "python":
        headers = ["def ", "if ", "for ", "while ", "class ", "elif "]
        for line in lines:
            clean_line = line.strip()
            for h in headers:
                if clean_line.startswith(h) and not clean_line.endswith(':'):
                    issues.append({
                        "type": "CRITICAL",
                        "msg": f"Python Syntax Error: Missing ':'",
                        "explain": f"Line '{clean_line}' must end with a colon (:).",
                        "color": "#ff0000"
                    })
                    score = 30
        if "Print(" in code or "PRINT(" in code:
            issues.append({"type": "WARNING", "msg": "Casing Issue", "explain": "Use 'print()' in lowercase.", "color": "#ffcc00"})
            if score > 70: score = 70

    # --- ☕ JAVA STRICT LOGIC ---
    elif lang == "java":
        for line in lines:
            clean_line = line.strip()
            # Logic to check missing semicolons in variable/print lines
            if any(x in clean_line for x in ["System.out", "int ", "String ", "float "]) and not clean_line.endswith(';'):
                issues.append({
                    "type": "CRITICAL",
                    "msg": "Missing Semicolon",
                    "explain": f"In Java, '{clean_line}' requires a semicolon (;) at the end.",
                    "color": "#ff0000"
                })
                score = 30
        if "printLn" in code:
            issues.append({"type": "WARNING", "msg": "Method Casing", "explain": "Use 'println' with a lowercase 'l'.", "color": "#ffcc00"})
            if score > 70: score = 70

    # --- ⚡ JAVASCRIPT STRICT LOGIC ---
    elif lang == "javascript":
        for line in lines:
            clean_line = line.strip()
            if clean_line.startswith("function") and not clean_line.endswith("{") and "{" not in code:
                issues.append({
                    "type": "CRITICAL",
                    "msg": "Missing Braces",
                    "explain": "JS functions must open with curly braces '{'.",
                    "color": "#ff0000"
                })
                score = 30
        if "Console.log" in code:
            issues.append({"type": "WARNING", "msg": "Casing Issue", "explain": "Use 'console.log' with lowercase 'c'.", "color": "#ffcc00"})
            if score > 70: score = 70

    # --- 🎯 COLOR & LABEL GRADING ---
    if score <= 40:
        label, color = "CRITICAL FAILURE", "#ff0000" # RED GLOW TRIGGER
    elif score <= 75:
        label, color = "MODERATE ISSUES", "#ffcc00" # YELLOW GLOW
    else:
        label, color = "EXCELLENT", "#00ff88" # GREEN GLOW

    return jsonify({"score": score, "label": label, "color": color, "issues": issues})

if __name__ == '__main__':
    app.run(debug=True)