
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
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css">
    <meta charset="UTF-8">
    <title>نتائج جامعة أسيوط</title>
    <style>
    

    nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 5%;
        background-color: #000000;
        box-shadow: 0px 0px 30px #ffeebe;
    }
    
    a {
        background-color: transparent;
    }
    
    nav {
        direction: ltr;
        align-items: center;
        justify-content: space-between;
        background-color: #000000;
        box-shadow: 0px 0px 30px #ffeebe;
    }
    
    .logo {
        color: #ffeebe;
        background-color: transparent;
        font-size: 25px;
        letter-spacing: 1px;
        cursor: pointer;
    }
    
    a {
        background-color: transparent;
    }


    .buttonnn {
        text-align: center;
        display: flex;
        flex-direction: column;
        background-color: #ffeebe;
        color: #000000;
        text-decoration: none;
        border: 2px solid #ffeebe;
        font-size: 20px;
        font-weight: bold;
        padding: 5px 15px;
        margin: 2px;
        border-radius: 30px;
        transition: .4s;
    }

    .buttonnn:hover {
        background-color: #000000;
        color: #ffeebe;
        border: 2px solid #ffeebe;
    }


    .resolto {
        direction: rtl;
        height: 100%;
        padding-bottom: 6%;

    }

    body {
        padding: 0;
        margin: 0;
        box-sizing: border-box;
        scroll-behavior: smooth;
        font-family: 'Segoe UI', Tahoma, sans-serif;
        background: #ffeebe;
        text-align: right;
        max-width: 100%;
        color: #333;
    }
    h2 {
        color: #000000;
        text-align: center;
        margin-bottom: 6%;
        font-size: 45px;
    }
    p {
        font-size: 25px;
    }
    form {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-left: 18%;
        margin-right: 18%;
        margin-bottom: 2%;
        background: #000000;
        padding: 4rem;
        border-radius: 30px;
        box-shadow: 0px 0px 30px #000000;
    }
    label {
        color: #ffeebe;
        font-size: 25px;
        font-weight: bold;
        margin-bottom: 20px;
        display: flex;
    }
    input[type="text"], select {
        padding: 0.5rem;
        font-size: 23px;
        border: 2px solid #ccc;
        border-radius: 30px;
        margin-bottom: 3%;
    }

    select {
        width: 100%;
    }

    input{
        width: 97.45%;
    }
    button {
        background-color: #ffeebe;
        color: black;
        border: 2px solid transparent;
        border-radius: 30px;
        font-size: 20px;
        font-weight: bold;
        padding: 10px 40px;
        transition: transform .4s;
        cursor: pointer;
    }
    button:hover {
        background-color: #000000;
        color: #ffeebe;
        border: 2px solid #ffeebe;
        cursor: pointer;
    }
    .result {
        margin-left: 20%;
        margin-right: 20%;
        background: #ffeebe;
        padding: 2rem;
        border: 3px solid #000;
        border-radius: 30px;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
        margin-top: 2%;
    }
    .congrats {
        text-align: center;
        background-color: #d4edda;
        color: #155724;
        border: 2px solid #c3e6cb;
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 15px;
        font-size: 35px;
        box-shadow: 0 0 10px #aaa;
    }
    ul {
        list-style-type: none;
        padding: 0;
        font-size: 20px;
        border: 3px solid #000;
        border-radius: 30px;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
        margin-top: 1rem;
    }
    li {
        margin-bottom: 0.3rem;
        display: flex;
        justify-content: space-between;
        padding: 0.4rem 0.8rem;
        border-bottom: 4px solid #ccc;
    }
    .subject-name {
        margin-right: 20%;
        font-weight: bold;
    }
    .grade {
        margin-left: 20%;   
        min-width: 100px;
        text-align: left;
        direction: ltr;
    }
    .error {
        color: red;
        font-weight: bold;
    }


    #contact {
        font-size: 50px;
    }

    .contact-me {
        width: 100%;
        height: 150px;
        background: #000000;
        display: flex;
        align-items: center;
        flex-direction: column;
        justify-content: center;
    }
    
    .contact-me p {
        color: #ffeebe;
        background-color: #000000;
        font-size: 35px;
        font-weight: bold;
        margin-bottom: 25px;
    }
    
    .contact-me .button-two {
        background-color: #ffeebe;
        color: #000000;
        text-decoration: none;
        border: 2px solid transparent;
        font-weight: bold;
        padding: 13px 30px;
        border-radius: 30px;
        transition: .6s;
    }
    
    .contact-me .button-two:hover {
        color: #ffeebe;
        background-color: transparent;
        border: 2px solid white;
        cursor: pointer;
    }

    footer::after {
        content: "";
        width: 100%;
        height: 100%;
        background-color: #ffeebe;
        position: absolute; 
        clip-path: circle(14% at right 38%);
    }
    
    
    footer::before {
        content: "";
        width: 100%;
        height: 100%;
        background-color: #ffeebe;
        position: absolute; 
        clip-path: circle(14% at left 38%);
    }

    .contact-me {
        width: 100%;
        height: 150px;
        background: #000000;
        display: flex;
        align-items: center;
        flex-direction: column;
        justify-content: center;
    }
    
    .contact-me p {
        color: #ffeebe;
        background-color: #000000;
        font-size: 30px;
        font-weight: bold;
        margin-bottom: 25px;
    }
    
    .contact-me .button-two {
        background-color: #ffeebe;
        color: #000000;
        text-decoration: none;
        border: 2px solid transparent;
        font-weight: bold;
        padding: 13px 30px;
        border-radius: 30px;
        transition: .6s;
    }
    
    .contact-me .button-two:hover {
        color: #ffeebe;
        background-color: transparent;
        border: 2px solid white;
        cursor: pointer;
    }
    
    footer {
        position: relative;
        width: 100%;
        height: 350px;
        background: #000000;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    footer p:nth-child(1) {
        font-size: 30px;
        color: #ffeebe;
        background-color: #000000;
        margin-bottom: 20px;
        font-weight: bold;
    }
    
    footer p:nth-child(2) {
        color: #ffeebe;
        background-color: #000000;
        font-size: 17px;
        width: 500px;
        text-align: center;
        line-height: 26px;
    }
    
    .social {
        display: flex;
        color: #ffeebe;
    }
    
    .social a {
        width: 45px;
        height: 45px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        margin: 22px 35px;
        color: #ffeebe;
        text-decoration: none;
        font-size: 50px;
    }
    
    .social a:hover {
        transform: scale(1.3);
        transition: .3s;
    }
    
    .end {  
        margin-top: 20px;
        position: absolute;
        color: white;
        background-color: #000000;
        bottom: 35px;
        font-size: 14px;
    }
    


    @media (max-width: 1500px) {

    form {
        margin-left: 7%;
        margin-right: 7%;
    }

    footer {
        height: 500px;
    }

    h2 {
        font-size: 90px;
        margin-bottom: 3%;
    }

    p, label {
        font-size: 45px;
    }

    input[type="text"], select {
        font-size: 50px;
    }

    .result {
        margin-left: 7.5%;
        margin-right: 7.5%;
    }

    button {
        margin-top: 2%;
        font-size: 50px;
        padding: 10px 30px;
    }


    .subject-name {
        margin-right: 15%;
    }

    .grade {
        margin-left: 15%;
    }   

    li {
        font-size: 45px;
    }

    .container {
        width: 100%;
        align-items: center;
    }
    
    .logo {
        font-size: 50px;
        margin-left: 3%;
        padding: 5px 10px;
    }
    

    contact p {
        font-size: 40px;
    }

    nav {
        font-size: 20px;
        padding-left: 0px;
        padding-right: 0px;
        text-align: center;
    }
    
    .buttonnn {
        font-size: 45px;
        border-radius: 30px;
        font-weight: bold;
        padding: 8px 20px;
        margin-top: 7px;
        margin-right: 7px;
        display: inline-block;
        top: 8px;
        right: 16px;
    }
    
    footer::after {
        clip-path: circle(8% at right 44%);
    }
    
    
    footer::before {
        clip-path: circle(8% at left 44%);
    }

    
    
    
    footer p:nth-child(1) {
        font-size: 30px;
    }
    
    footer p:nth-child(2) {
        font-size: 17px;
    }

    
    .end {  
        font-size: 25px;
    }
}
</style>
</head>
<body>
    <nav>
        <h3 class="logo"> El-Da7e7a </h3>
        <a class="buttonnn" href="https://www.ahmed-hassan.tech/"> زور موقعنا </a>
    </nav>
    <div class="resolto">
        <h2>نتائج جامعة أسيوط</h2>
        <form method="post">
            <!-- أضف داخل <form> بعد اختيار الكلية مباشرة -->
        <label for="faculty_id">الكلية:</label>
        <select name="faculty_id" id="faculty_id" required onchange="updateGroups()">
            <option value="">اختر الكلية ...</option>
            <option value="1">تمريض</option>
            <option value="2">حقوق</option>
            <option value="3">التربية للطفولة المبكرة</option>
            <option value="4">الخدمة الاجتماعية</option>
            <option value="5">فنون جميلة</option>
            <option value="6">تربية رياضية</option>
            <option value="7">طب بيطري</option>
            <option value="9">معهد تمريض</option>
            <option value="17">التجارة</option>
        </select>

        <label for="group_id">الفرقة:</label>
        <select name="group_id" id="group_id" required disabled>
            <option value="">اختر الفرقة...</option>
        </select>
<script>
const groupOptions = {
    "1": [
        { value: "1", text: "الفرقة الأولى" },
        { value: "2", text: "الفرقة الثانية" },
        { value: "10", text: "المستوى الثاني - لائحة حديثة" },
        { value: "17", text: "الفرقة الثالثة - لائحة قديمة" },
        { value: "76", text: "المستوى الثالث - غير نظامي - لائحة حديثة" },
        { value: "77", text: "المستوى الثالث - لائحة قديمة" },
        { value: "79", text: "المستوى الثالث - نظامي" }
    ],
    "2": [
        { value: "53", text: "الفرقة الأولى - لغة إنجليزية" },
        { value: "65", text: "الفرقة الأولى - انتظام" },
        { value: "66", text: "الفرقة الأولى - انتساب" },
        { value: "61", text: "الفرقة الثانية - لغة إنجليزية" },
        { value: "73", text: "الفرقة الثانية - انتظام" },
        { value: "74", text: "الفرقة الثانية - انتساب" },
        { value: "60", text: "الفرقة الثالثة - لغة إنجليزية" },
        { value: "31", text: "الفرقة الثالثة - انتظام" },
        { value: "72", text: "الفرقة الثالثة - انتساب" },
        { value: "54", text: "الفرقة الرابعة - لغة إنجليزية - مستجدون" },
        { value: "56", text: "الفرقة الرابعة - لغة إنجليزية - تسجيلات 2019" },
        { value: "58", text: "الفرقة الرابعة - لغة إنجليزية - تسجيلات 2020" },
        { value: "59", text: "الفرقة الرابعة - لغة إنجليزية - فصل" },
        { value: "68", text: "الفرقة الرابعة - انتظام" },
        { value: "70", text: "الفرقة الرابعة - انتساب" },
        ],
        "4": [
        { value: "1", text: "الفرقة الأولى" },
        { value: "2", text: "الفرقة الثانية" },
        { value: "10", text: "المستوى الثاني - لائحة حديثة" },
        { value: "17", text: "الفرقة الثالثة - لائحة قديمة" },
        { value: "76", text: "المستوى الثالث - غير نظامي - لائحة حديثة" },
        { value: "77", text: "المستوى الثالث - لائحة قديمة" },
        { value: "79", text: "المستوى الثالث - نظامي" }
        ],
        "5": [],
        "6": [
        { value: "3", text: "الفرقة الثالثة" },
        ],
        "7": [
        { value: "75", text: "المستوى الخامس" }
        ],
        "9": [
        { value: "11", text: "الفرقة الأولى - لائحة قديمة" },
        { value: "12", text: "الفرقة الأولى - لائحة قديمة - نظام الساعات الدراسية" }
        ],
        "17": [
        { value: "22", text: "الفرقة الأولى - لغة إنجليزية - انتساب" },
        { value: "23", text: "الفرقة الأولى - انتساب" },
        { value: "28", text: "الفرقة الأولى - لغة إنجليزية - فتظلم" },
        { value: "29", text: "الفرقة الأولى - انتظام" },
        { value: "24", text: "الفرقة الثانية - لغة إنجليزية - انتظام" },
        { value: "25", text: "الفرقة الثانية - لغة إنجليزية - انتساب" },
        { value: "26", text: "الفرقة الثانية - انتظام" },
        { value: "27", text: "الفرقة الثانية - انتساب" },
        { value: "30", text: "الفرقة الثالثة - انتساب" },
        { value: "31", text: "الفرقة الثالثة - انتظام" },
        { value: "33", text: "الفرقة الرابعة - محاسبة - انتظام" },
        { value: "34", text: "الفرقة الرابعة - محاسبة - انتساب" },
        { value: "35", text: "الفرقة الرابعة - لغة إنجليزية - انتظام" },
        { value: "36", text: "الفرقة الرابعة - لغة إنجليزية - انتساب" },
        { value: "37", text: "الفرقة الرابعة - لغة إنجليزية - إدارة - انتظام" },
        { value: "38", text: "الفرقة الرابعة - إدارة - انتظام" },
        { value: "39", text: "الفرقة الرابعة - إدارة - انتساب" }
    ],
    
    };

    function updateGroups() {
        const facultySelect = document.getElementById("faculty_id");
        const groupSelect = document.getElementById("group_id");
        const facultyId = facultySelect.value;

        groupSelect.innerHTML = '<option value="">اختر الفرقة...</option>';
        groupSelect.disabled = !facultyId;

        if (facultyId && groupOptions[facultyId]) {
            groupOptions[facultyId].forEach(option => {
                const opt = document.createElement("option");
                opt.value = option.value;
                opt.textContent = option.text;
                groupSelect.appendChild(opt);
            });
        }
    }
    </script>

        <label>إسم الطالب أو رقم الجلوس:</label>
        <input type="text" name="student_number" required>
        <button type="submit">بحث</button>
    </form>

    {% if result %}
    <div class="result">
        {% if result.general_grade in ["ممتاز", "جيد جدا", "جيد", "مقبول"] %}
        <div class="congrats">
            🎉 تهانينا {{ result.student_name.split(' ')[0] }}! لقد حصلت على تقدير <strong>{{ result.general_grade }}</strong> بمجموع <strong>{{ result.total_result.replace('%', '') }}</strong>. بالتوفيق!
        </div>
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
        <script>
            confetti({
                particleCount: 200,
                spread: 100,
                origin: { y: 0.6 }
            });
        </script>
        {% endif %}
        <p>👤 الاسم: {{ result.student_name }}</p>
        <p>🆔 رقم الطالب: {{ result.student_number }}</p>
        <p>🎓 الفرقة: {{ result.group }}</p>
        {% if result.general_grade %}
            <p>📊 التقدير العام: {{ result.general_grade }}</p>
        {% endif %}
        {% if result.total_result %}
            <p>📈 المجموع الكلي: {{ result.total_result.replace('%', '') }}</p>
        {% endif %}
        <h4>📚 الدرجات:</h4>
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

    <footer id="contact" class="clip">
            <p> تواصل معنا </p>
            <div class="social">
                <a href="http://wa.me/201128641717"> <i class="fa-brands fa-whatsapp"></i> </a>
                <a href="https://www.facebook.com/2ahmedhassan2"> <i class="fa-brands fa-facebook"></i> </a>
                <a href="https://github.com/2ahmedhassan2/"> <i class="fa-brands fa-github"></i> </a>
                <a href="https://www.linkedin.com/in/2ahmedhassan2/"> <i class="fa-brands fa-linkedin-in"></i> </a>
                <a href="https://www.instagram.com/2ahmedhassan2/"> <i class="fa-brands fa-instagram"></i> </a>
            </div>
            <p class="end"> &copy; 2025 Ahmed Hassan. All rights reserved. </p>
    </footer>
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
            "faculty_id": request.form["faculty_id"],
            "group_id": group_id,
            "department_id": "",
            "division_id": "",
            "student_name_number": student_number
        }
        try:
            res = session.post("https://services.aun.edu.eg/results/public/ar/exam-result", headers=headers, data=payload)
            data = res.json()
            if data.get("status") == "true":
                total_result = None
                general_grade = None
                for item in data.get("result_total_degrees", []):
                    if item["column_name"] == "المجموع":
                        total_result = item["column_value"]
                    elif item["column_name"] == "التقدير العام":
                        general_grade = item["column_value"]
                data["total_result"] = total_result
                data["general_grade"] = general_grade
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
