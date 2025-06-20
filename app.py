#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>نتيجة الطالب - جامعة أسيوط</title>
    <style>
    body {
        font-family: 'Segoe UI', Tahoma, sans-serif;
        background: #ffeebe;
        direction: rtl;
        text-align: right;
        padding: 2rem;
        max-width: 100%;
        margin: auto;
        color: #333;
    }

    h2 {
        color: #000000;
        text-align: center;
        margin-bottom: 2rem;
        font-size: 2rem;
    }

    form {
        margin-bottom: 2rem;
        background: #000000;
        padding: 1rem;
        border-radius: 30px;
        box-shadow: 0px 0px 30px #000000;
    }

    label {
        color: #ffeebe;
        font-size: 1.2rem;
        margin-bottom: 10px;
        display: flex;
    }

    input[type="text"], select {
        padding: 0.5rem;
        font-size: 1rem;
        width: 100%;
        border: 2px solid #ccc;
        border-radius: 20px;
        margin-bottom: 1rem;
        box-sizing: border-box;
    }

    button {
        display: block;
        margin: 1rem auto;
        background-color: #ffeebe;
        color: black;
        border: 2px solid transparent;
        border-radius: 30px;
        font-size: 1.2rem;
        font-weight: bold;
        padding: 0.5rem 2rem;
        transition: all 0.3s ease;
    }

    button:hover {
        background-color: #000000;
        color: #ffeebe;
        border: 2px solid #ffeebe;
        cursor: pointer;
    }

    .result {
        background: #ffeebe;
        padding: 1.5rem;
        border: 3px solid #000;
        border-radius: 30px;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
        margin-top: 2rem;
    }

    ul {
        list-style-type: none;
        padding: 0;
        font-size: 1.2rem;
        border: 3px solid #000;
        border-radius: 30px;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
    }

    li {
        margin-bottom: 0.5rem;
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 1rem;
        border-bottom: 1px solid #ccc;
    }

    .error {
        color: red;
        font-weight: bold;
        text-align: center;
        margin-top: 1rem;
    }

    @media (max-width: 600px) {
        h2 {
            font-size: 1.5rem;
        }

        button {
            width: 100%;
            padding: 0.75rem;
            font-size: 1rem;
        }

        li {
            flex-direction: column;
            align-items: flex-start;
        }
    }
</style>

</head>
<body>
    <h2>نتيجة الطالب - كلية التجارة | جامعة أسيوط</h2>
    <form method="post">
        <label for="group_id">الفرقة:</label>
        <select name="group_id" id="group_id" class="form-control" required>
            <option value="">اختر الفرقة...</option>
            <option value="22">أولى لغة انتساب</option>
            <option value="23">أولى انتساب</option>
            <option value="24">الثانية لغة انتظام</option>
            <option value="25">الثانية لغة انتساب</option>
            <option value="26">الثانية انتظام</option>
            <option value="27">الثانية انتساب</option>
            <option value="28">أولى لغة فتظلم</option>
            <option value="29">أولى انتظام</option>
            <option value="30">الثالثة انتساب</option>
            <option value="31">تالتة انتظام</option>
            <option value="33">رابعة محاسبة انتظام</option>
            <option value="34">رابعة محاسبة انتساب</option>
            <option value="35">رابعة لغة انتظام</option>
            <option value="36">رابعة لغة انتساب</option>
            <option value="37">رابعة لغة ادارة انتظام</option>
            <option value="38">رابعة أدارة انتظام</option>
            <option value="39">رابعة أدارة انتساب</option>
            <option value="40">رابعة علوم ساسة انتظام</option>
            <option value="44">الثالثة لغة انتساب</option>
            <option value="45">الثالثة لغة انتظام</option>
            <option value="46">التالتة سياسة انتساب</option>
            <option value="48">تالتة سياسة انتظام</option>
            <option value="51">الثانية انتظام علوم سياسية</option>
            <option value="52">الثانية انتساب علوم سياسية</option>
        </select>

        <label>إسم الطالب أو رقم الجلوس:</label>
        <input type="text" name="student_number" required>
        <button type="submit">بحث</button>
    </form>

    {% if result %}
    <div class="result">
        <p>👤 الاسم: {{ result.student_name }}</p>
        <p>🆔 رقم الطالب: {{ result.student_number }}</p>
        <p>🎓 الفرقة: {{ result.group }}</p>
        <p>📅 الفصل الدراسي: {{ result.semester }}</p>
        <h4>📚 الدرجات:</h4>
        <ul>
        {% for subject in result.result_subjects_details %}
            <li>{{ subject.subject_name }}: {{ subject["0"][0].column_value }}</li>
        {% endfor %}
        </ul>
    </div>
    {% elif error %}
        <p class="error">{{ error }}</p>
    {% endif %}
</body>
</html>
"""

def get_token_and_cookies():
    session = requests.Session()
    url = "https://services.aun.edu.eg/results/public/ar/exam-result"
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    token_input = soup.find("input", {"name": "_token"})
    token = token_input["value"] if token_input else None
    cookies = "; ".join([f"{k}={v}" for k, v in session.cookies.get_dict().items()])
    return token, cookies, session

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    if request.method == "POST":
        student_number = request.form["student_number"]
        group_id = request.form["group_id"]
        token, cookies, session = get_token_and_cookies()
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://services.aun.edu.eg/results/public/ar/exam-result",
            "Origin": "https://services.aun.edu.eg",
            "X-Requested-With": "XMLHttpRequest",
            "Cookie": cookies
        }
        payload = {
            "_token": token,
            "exam_year_id": "1",
            "faculty_id": "10",
            "group_id": group_id,
            "department_id": "",
            "division_id": "",
            "student_name_number": student_number
        }
        try:
            res = session.post("https://services.aun.edu.eg/results/public/ar/exam-result", headers=headers, data=payload)
            data = res.json()
            if data.get("status") == "true":
                result = data
            else:
                error = "❌ لا توجد نتيجة لهذا الطالب."
        except Exception:
            error = "⚠️ فشل في الاتصال أو التحليل. تأكد من اتصال الإنترنت وأن الموقع يعمل."
    return render_template_string(HTML_TEMPLATE, result=result, error=error)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
