#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template_string, request
import requests
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<title>أفضل 50 طالب - كلية التجارة</title>
<style>
body { font-family: Arial, sans-serif; background: #ffeebe; text-align: center; }
h2 { margin-top: 20px; color: #000; }
.result { margin: 20px auto; width: 80%; background: #fff; padding: 20px; border-radius: 15px; box-shadow: 0 0 20px rgba(0,0,0,0.3); }
ul { list-style: none; padding: 0; }
li { display: flex; justify-content: space-between; padding: 8px; border-bottom: 1px solid #ccc; font-size: 18px; }
li:nth-child(odd) { background: #f9f9f9; }
</style>
</head>
<body>
<h2>أفضل 50 طالب - كلية التجارة - الفرقة الثالثة انتظام</h2>
{% if top_students %}
<div class="result">
    <ul>
    {% for student in top_students %}
        <li>
            <span>{{ loop.index }}. {{ student.name }}</span>
            <span>المجموع: {{ student.total }}</span>
        </li>
    {% endfor %}
    </ul>
</div>
{% else %}
<p>لا توجد نتائج حالياً أو جاري التحميل ...</p>
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

def get_top_students(start, end, faculty_id, group_id):
    token, cookies, session = get_token_and_cookies()

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://services.aun.edu.eg/results/public/ar/exam-result",
        "Origin": "https://services.aun.edu.eg",
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": cookies
    }

    students = []

    for num in range(start, end + 1):
        payload = {
            "_token": token,
            "exam_year_id": "3",
            "faculty_id": faculty_id,
            "group_id": group_id,
            "department_id": "",
            "division_id": "",
            "student_name_number": str(num)
        }

        try:
            res = session.post(
                "https://services.aun.edu.eg/results/public/ar/exam-result",
                headers=headers,
                data=payload
            )

            data = res.json()
            if data.get("status") == "true":
                total = 0
                for item in data.get("result_total_degrees", []):
                    if item["column_name"] == "المجموع":
                        total = float(item["column_value"].replace('%', '').strip())
                students.append({
                    "name": data.get("student_name"),
                    "number": num,
                    "total": total
                })
                print(f"✔ {num} تم")
            else:
                print(f"❌ {num} لا توجد نتيجة")
        except Exception:
            print(f"❌ {num} فشل الاتصال")
        time.sleep(0.1)  # delay بسيط لتجنب الحظر

    students_sorted = sorted(students, key=lambda x: x["total"], reverse=True)
    return students_sorted[:50]

@app.route("/")
def index():
    top_students = get_top_students(
        23000000,
        23011000,
        "17",   # كلية التجارة
        "164"   # الفرقة الثالثة انتظام
    )
    return render_template_string(HTML_TEMPLATE, top_students=top_students)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
