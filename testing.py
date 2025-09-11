from flask import Flask, render_template, request
import gspread
from google.oauth2.service_account import Credentials
import traceback

app = Flask(__name__)

# ملف الـ Service Account اللي نزلته (اسمه credentials.json)
SERVICE_ACCOUNT_FILE = "credentials.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"]

# تهيئة Google Sheets (مع طباعة خطأ واضح لو فشل)
try:
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    gc = gspread.authorize(creds)
    SPREADSHEET_NAME = "Job Applications"   # اسم الشيت بالضبط
    sheet = gc.open(SPREADSHEET_NAME).sheet1
    print("✅ Google Sheets: جاهز للكتابة في", SPREADSHEET_NAME)
except Exception as e:
    print("❌ خطأ أثناء تهيئة Google Sheets (Credentials أو فتح الشيت):")
    traceback.print_exc()
    sheet = None

# بيانات الوظائف والمدن (مثل ما عندك)
jobs_list = ["مندوب مبيعات","مروج","عامل مخزن","كاش فان"]
cities_list = [
    "رام الله والبيرة","القدس","الخليل","بيت لحم",
    "نابلس","جنين","طولكرم","قلقيلية","طوباس",
    "سلفيت","أريحا"
]

@app.route('/', methods=['GET', 'POST'])
def index():
    submitted = 'false'
    if request.method == 'POST':
        form_data = [
            request.form.get('name'),
            request.form.get('email'),
            request.form.get('job'),
            request.form.get('phone'),
            request.form.get('age'),
            request.form.get('school'),
            request.form.get('university'),
            request.form.get('major'),
            request.form.get('city'),
            request.form.get('address'),
            request.form.get('experience'),
            request.form.get('references')
        ]

        # إذا sheet معرف (تمت تهيئته)، نضيف السطر؛ وإلا نطبع خطأ
        if sheet:
            try:
                sheet.append_row(form_data)
                print("✅ أضيفت بيانات جديدة إلى Google Sheet:", form_data)
                submitted = 'true'
            except Exception as e:
                print("❌ خطأ أثناء append_row:")
                traceback.print_exc()
        else:
            print("❌ لم يتم تهيئة sheet — راجع رسالة الإقلاع أعلاه.")

    return render_template('jobs_formm.html', submitted=submitted, jobs=jobs_list, cities=cities_list)

if __name__ == '__main__':
    app.run(debug=True)
