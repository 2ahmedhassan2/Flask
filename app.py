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
            max-width: 800px;
            margin: auto;
            color: #333;
        }
        h2 {
            color: #000000;
            text-align: center;
            margin-bottom: 80px;
            font-size: 40px;
        }
        p {
            font-size: 25px;
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
            font-size: 25px;
            margin-bottom: 20px;
            display: flex;
        }
        input[type="text"], select {
            padding: 0.5rem;
            font-size: 1rem;
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
            margin-top: 5%;
            margin-left: 40%;
            margin-right: 40%;
            background-color: #ffeebe;
            color: black;
            border: 2px solid transparent;
            border-radius: 30px;
            font-size: 20px;
            font-weight: bold;
            padding: 10px 50px;
            transition: transform .4s;
        }
        button:hover {
            background-color: #000000;
            color: #ffeebe;
            border: 2px solid #ffeebe;
            cursor: pointer;
        }
        .result {
            background: #ffeebe;
            padding: 2rem;
            border: 3px solid #000;
            border-radius: 30px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
            margin-top: 2rem;
        }
        .congrats {
            text-align: center;
            background-color: #d4edda;
            color: #155724;
            border: 2px solid #c3e6cb;
            padding: 2rem;
            margin-bottom: 1rem;
            border-radius: 15px;
            font-size: 30px;
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
            border-bottom: 2.5px solid #ccc;
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

        @media (max-width: 1000px) {

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

        button {
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
    }
</style>
    </style>
</head>
<body>
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
    <option value="10">التجارة</option>
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
        "10": [
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
