#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template_string
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

# الرابط الخاص بك لجلب الترتيب وزيادة عداد البحث
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxnBQKwXKpxDfLPL9lMaDwQHYTTpz9AViyLeLyTpXcwlXZYqAt_zk0jzDCyAtlCDKix/exec"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css">
    <meta charset="UTF-8">
    <title>نتائج كلية التجارة - جامعة أسيوط</title>
    <style>
    body {
        padding: 0;
        margin: 0;
        box-sizing: border-box;
        scroll-behavior: smooth;
        font-family: 'Segoe UI', Tahoma, sans-serif;
        background: #f4f8f9;
        text-align: right;
        max-width: 100%;
        color: #333;
    }
    
    nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 15px 8%;
        background-color: #ffffff;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
        direction: ltr;
    }
    
    .logo {
        color: #0f4c9c;
        font-size: 24px;
        font-weight: bold;
        letter-spacing: 0.5px;
        margin: 0;
    }

    .buttonnn {
        text-align: center;
        background-color: #0f4c9c;
        color: #ffffff;
        text-decoration: none;
        font-size: 16px;
        font-weight: 600;
        padding: 8px 24px;
        border-radius: 20px;
        transition: .3s;
        border: 1px solid #0f4c9c;
    }

    .buttonnn:hover {
        background-color: #1d5cb3;
        color: #ffffff;
    }

    .resolto {
        direction: rtl;
        min-height: calc(100vh - 400px);
        padding: 40px 0;
    }

    h2 {
        color: #0f4c9c;
        text-align: center;
        margin-bottom: 30px;
        font-size: 36px;
        font-weight: bold;
    }
    
    p {
        font-size: 20px;
    }
    
    form {
        display: flex;
        flex-direction: column;
        align-items: center;
        max-width: 600px;
        margin: 0 auto 30px auto;
        background: #ffffff;
        padding: 3rem;
        border-radius: 24px;
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.05);
        border: 1px solid #e1e8ed;
    }
    
    label {
        color: #333333;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 10px;
        display: flex;
        align-self: flex-start;
        width: 100%;
    }
    
    input[type="text"], select {
        width: 100%;
        padding: 12px 20px;
        font-size: 18px;
        border: 1.5px solid #d1dbe5;
        border-radius: 12px;
        margin-bottom: 25px;
        box-sizing: border-box;
        background-color: #fcfdfe;
        transition: border-color 0.3s;
    }

    input[type="text"]:focus, select:focus {
        border-color: #0f4c9c;
        outline: none;
    }
    
    button {
        background-color: #0f4c9c;
        color: white;
        border: none;
        border-radius: 25px;
        font-size: 18px;
        font-weight: bold;
        padding: 12px 50px;
        transition: background-color 0.3s, transform 0.2s;
        cursor: pointer;
        margin-top: 10px;
    }
    
    button:hover {
        background-color: #1d5cb3;
    }
    
    button:active {
        transform: scale(0.98);
    }

    .result {
        max-width: 700px;
        margin: 30px auto;
        background: #ffffff;
        padding: 2.5rem;
        border-radius: 24px;
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.05);
        border: 1px solid #e1e8ed;
    }
    
    .congrats {
        text-align: center;
        background-color: #e6f4ea;
        color: #137333;
        border: 1px solid #ceead6;
        padding: 1rem;
        margin-bottom: 1.5rem;
        border-radius: 16px;
        font-size: 24px;
        font-weight: bold;
    }
    
    ul {
        list-style-type: none;
        padding: 0;
        font-size: 18px;
        border: 1px solid #e1e8ed;
        border-radius: 16px;
        overflow: hidden;
        margin-top: 1.5rem;
    }
    
    li {
        display: flex;
        justify-content: space-between;
        padding: 1rem 1.5rem;
        border-bottom: 1px solid #e1e8ed;
        background-color: #fcfdfe;
    }
    
    li:last-child {
        border-bottom: none;
    }

    li:nth-child(even) {
        background-color: #ffffff;
    }
    
    .subject-name {
        font-weight: 600;
        color: #4a5568;
    }
    
    .grade {
        font-weight: bold;
        color: #0f4c9c;
        direction: ltr;
    }
    
    .error {
        color: #c5221f;
        background-color: #fce8e6;
        border: 1px solid #fad2cf;
        padding: 1rem;
        border-radius: 16px;
        text-align: center;
        font-size: 18px;
        max-width: 600px;
        margin: 20px auto;
        font-weight: bold;
    }
    
    footer {
        width: 100%;
        padding: 40px 0;
        background: #111111;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    footer p:nth-child(1) {
        font-size: 20px;
        color: #ffffff;
        margin-bottom: 15px;
        font-weight: bold;
    }
    
    .social {
        display: flex;
        gap: 25px;
        margin: 15px 0;
    }
    
    .social a {
        color: #a0aec0;
        text-decoration: none;
        font-size: 32px;
        transition: color 0.3s, transform 0.3s;
    }
    
    .social a:hover {
        color: #ffffff;
        transform: scale(1.15);
    }
    
    .end {  
        margin-top: 20px;
        color: #718096;
        font-size: 14px;
    }
    
    @media (max-width: 768px) {
        form, .result, .error { width: 90%; padding: 2rem 1.5rem; }
        h2 { font-size: 28px; }
        nav { padding: 15px 4%; }
    }
    </style>
</head>
<body>
    <nav>
        <h3 class="logo">El-Da7e7a</h3>
        <a class="buttonnn" href="https://elda7e7a.vercel.app/">زور موقعنا</a>
    </nav>
    <div class="resolto">
        <h2>نتائج الفرقة الثالثة كلية التجارة - جامعة أسيوط</h2>
        <form method="post">
            <label for="group_id">الفرقة:</label>
            <select name="group_id" id="group_id" required>
                <option value="">اختر الفرقة...</option>
                <option value="164">الثالثة أنُتظام</option>
                <option value="165">الثالثة أنُتساب</option>
                <option value="166">الثالثة سياسة انتظام</option>
                <option value="167">الثالثة سياسة انتساب</option>
            </select>

            <label>رقم الجلوس:</label>
            <input type="text" name="student_number" placeholder="اكتب رقم الجلوس" required>
            
            <label>إكتب الإسم الرابع:</label>
            <input type="text" name="fourth_name" placeholder="اكتب إسمك الرابع فقط" required>

            <button type="submit">بحث</button>
        </form>

        {% if result %}
        <div class="result">
            {% if result.general_grade in ["ممتاز", "جيد جدا", "جيد", "مقبول"] %}
            <div class="congrats">
                🎉 تهانينا {{ result.student_name.split(' ')[0] }}! لقد حصلت على تقدير <strong>{{ result.general_grade }}</strong>. بالتوفيق!
            </div>
            <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
            <script>
                confetti({ particleCount: 200, spread: 100, origin: { y: 0.6 } });
            </script>
            {% endif %}
            
            <p> الاسم: {{ result.student_name }}</p>
            <p> رقم الجلوس: {{ result.student_number }}</p>
            
            <div class="congrats" style="background-color: #f4f8f9; color: #0f4c9c; border: 1px solid #d1dbe5;">
                ترتيبك على الدفعة: <strong>{{ result.rank }}</strong>
            </div>

            {% if result.general_grade %}
                <p>📊 التقدير العام: {{ result.general_grade }}</p>
            {% endif %}
            {% if result.total_result %}
                <p>📈 المجموع الكلي: {{ result.total_result.replace('%', '') }}</p>
            {% endif %}
            
            <h4>📚 الدرجات بالتفصيل:</h4>
            <ul>
            {% for subject in result.result_subjects_details %}
                <li>
                    <span class="subject-name">{{ subject.subject_name }}</span>
                    <span class="grade">{{ subject["0"][0].column_value }}</span>
                </li>
            {% endfor %}
            </ul>
        </div>
        {% elif error %}
            <p class="error">{{ error }}</p>
        {% endif %}
    </div>

    <footer>
        <p>تواصل معنا</p>
        <div class="social">
            <a href="http://wa.me/201128641717"><i class="fa-brands fa-whatsapp"></i></a>
            <a href="https://www.facebook.com/2ahmedhassan2"><i class="fa-brands fa-facebook"></i></a>
            <a href="https://github.com/2ahmedhassan2/"><i class="fa-brands fa-github"></i></a>
            <a href="https://www.linkedin.com/in/201128641717/"><i class="fa-brands fa-linkedin-in"></i></a>
            <a href="https://www.instagram.com/2ahmedhassan2/"><i class="fa-brands fa-instagram"></i></a>
        </div>
        <p class="end"> &copy; 2026 Ahmed Hassan. All rights reserved. </p>
    </footer>
</body>
</html>
"""

def get_token_and_cookies():
    session = requests.Session()
    url = "https://services.aun.edu.eg/results/public/ar/exam-result"
    try:
        response = session.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        token_input = soup.find("input", {"name": "_token"})
        token = token_input["value"] if token_input else None
        cookies = "; ".join([f"{k}={v}" for k, v in session.cookies.get_dict().items()])
        return token, cookies, session
    except Exception:
        return None, None, session

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    if request.method == "POST":
        student_number = request.form["student_number"].strip()
        fourth_name_input = request.form["fourth_name"].strip()
        faculty_id = "17"  
        group_id = request.form["group_id"]
        
        token, cookies, session = get_token_and_cookies()
        if not token:
            return render_template_string(HTML_TEMPLATE, error="فشل الاتصال بالسيرفر الرئيسي حاول تاني او استني شوية.")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://services.aun.edu.eg/results/public/ar/exam-result",
            "Origin": "https://services.aun.edu.eg",
            "X-Requested-With": "XMLHttpRequest",
            "Cookie": cookies
        }
        
        payload = {
            "_token": token,
            "exam_year_id": "3",
            "faculty_id": faculty_id,
            "group_id": group_id,
            "department_id": "",
            "division_id": "",
            "student_name_number": student_number
        }
        
        try:
            res = session.post("https://services.aun.edu.eg/results/public/ar/exam-result", headers=headers, data=payload, timeout=12)
            data = res.json()
            
            if data.get("status") == "true" or data.get("status") is True:
                student_name = data.get("student_name", "").strip()
                
                total_result = None
                general_grade = None
                for item in data.get("result_total_degrees", []):
                    if item["column_name"] == "المجموع":
                        total_result = item["column_value"]
                    elif item["column_name"] == "التقدير العام":
                        general_grade = item["column_value"]
                
                data["total_result"] = total_result
                data["general_grade"] = general_grade
                data["student_number"] = student_number

                # 🚀 إرسال البيانات فوراً إلى Apps Script (التحقق والعد والتفريق يقع على عاتق الشيت الآن)
                try:
                    sheet_response = requests.get(
                        APPS_SCRIPT_URL, 
                        params={"seat": student_number, "fourthName": fourth_name_input}, 
                        timeout=10
                    )
                    sheet_data = sheet_response.json()
                    
                    if "success" in sheet_data and sheet_data["success"] is True:
                        # الحالة الأولى: رقم الجلوس صح والاسم الرابع صح
                        data["rank"] = sheet_data.get("rank", "N/A")
                        result = data  # عرض البيانات بنجاح
                    else:
                        # الحالة الثانية: رقم الجلوس صح ولكن الاسم الرابع غلط (تم الاحتساب وزيادة العداد في الشيت كـ "اسم خاطئ")
                        error = "الاسم الرابع غلط (تأكيد الهوية فشل لحماية الخصوصية)، ولكن تم تسجيل المحاولة في النظام."
                
                except Exception:
                    error = "الاسم الرابع غلط (تأكيد الهوية فشل لحماية الخصوصية)."
            else:
                error = "رقم الجلوس خطأ أو غير موجود، راجع بياناتك."
        except Exception as e:
            error = "فشل في الاتصال بالسيرفر (إتأكد من استقرار الشبكة)."
            
    return render_template_string(HTML_TEMPLATE, result=result, error=error)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
