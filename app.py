#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template_string
import requests
from bs4 import BeautifulSoup
import concurrent.futures
import pandas as pd
import os
from tqdm import tqdm

app = Flask(__name__)

URL = "https://services.aun.edu.eg/results/public/ar/exam-result"
START = 23000000
END = 23011000

# ---------------------------
# HTML
# ---------------------------
HTML = """
<h2 style="text-align:center;">🏆 أوائل تجارة - ثالثة انتظام</h2>
<ul style="width:60%;margin:auto;list-style:none;">
{% for s in students %}
<li style="background:#000;color:#ffeebe;margin:10px;padding:15px;border-radius:10px;">
{{ loop.index }} - {{ s.name }} <br>
رقم الجلوس: {{ s.number }} <br>
المجموع: {{ s.total }}
</li>
{% endfor %}
</ul>
"""

# ---------------------------
# Token
# ---------------------------
def get_session():
    session = requests.Session()
    r = session.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")

    token = soup.find("input", {"name": "_token"})
    token = token["value"] if token else None

    cookies = "; ".join([f"{k}={v}" for k, v in session.cookies.get_dict().items()])

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": URL,
        "Origin": "https://services.aun.edu.eg",
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": cookies
    }

    return session, headers, token

# ---------------------------
# Fetch Student
# ---------------------------
def fetch_student(student_number):
    try:
        session, headers, token = get_session()

        payload = {
            "_token": token,
            "exam_year_id": "3",
            "faculty_id": "17",
            "group_id": "164",
            "department_id": "",
            "division_id": "",
            "student_name_number": str(student_number)
        }

        res = session.post(URL, headers=headers, data=payload, timeout=10)
        data = res.json()

        if data.get("status") == "true":
            for item in data.get("result_total_degrees", []):
                if item["column_name"] == "المجموع":
                    total = float(item["column_value"].replace('%', ''))

                    return {
                        "name": data.get("student_name"),
                        "number": student_number,
                        "total": total
                    }
    except:
        return None

# ---------------------------
# Main Logic
# ---------------------------
def get_top_students():
    # لو فيه cache
    if os.path.exists("top50.xlsx"):
        df = pd.read_excel("top50.xlsx")
        return df.to_dict(orient="records")

    students = []

    numbers = list(range(START, END + 1))

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = list(tqdm(executor.map(fetch_student, numbers), total=len(numbers)))

    for r in results:
        if r:
            students.append(r)

    # ترتيب
    students.sort(key=lambda x: x["total"], reverse=True)

    top50 = students[:50]

    # حفظ Excel
    df = pd.DataFrame(top50)
    df.to_excel("top50.xlsx", index=False)

    return top50

# ---------------------------
# Routes
# ---------------------------
@app.route("/")
def home():
    return "<h2>ادخل /top50</h2>"

@app.route("/top50")
def top50():
    students = get_top_students()
    return render_template_string(HTML, students=students)

# ---------------------------
# Run
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
