from flask import Flask, render_template, request, redirect, url_for
import gspread
from google.oauth2.service_account import Credentials
import os
import traceback

app = Flask(__name__)

# Google Sheets باستخدام Environment Variables
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

try:
    # التحقق من وجود كل environment variables
    required_env_vars = [
        "GOOGLE_TYPE",
        "GOOGLE_PROJECT_ID",
        "GOOGLE_PRIVATE_KEY",
        "GOOGLE_CLIENT_EMAIL",
        "GOOGLE_CLIENT_ID",
        "GOOGLE_CLIENT_X509_CERT_URL"
    ]
    for var in required_env_vars:
        if not os.environ.get(var):
            raise ValueError(f"Environment variable {var} غير موجود!")

    creds_info = {
        "type": os.environ.get("GOOGLE_TYPE"),
        "project_id": os.environ.get("GOOGLE_PROJECT_ID"),
        "private_key_id": os.environ.get("GOOGLE_PRIVATE_KEY_ID", ""),
        "private_key": os.environ.get("GOOGLE_PRIVATE_KEY").replace('\\n', '\n'),
        "client_email": os.environ.get("GOOGLE_CLIENT_EMAIL"),
        "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": os.environ.get("GOOGLE_CLIENT_X509_CERT_URL")
    }

    creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
    gc = gspread.authorize(creds)
    SPREADSHEET_NAME = "Job Applications"
    sheet = gc.open(SPREADSHEET_NAME).sheet1
    print("✅ Google Sheets جاهز للكتابة في", SPREADSHEET_NAME)
except Exception as e:
    print("❌ خطأ أثناء تهيئة Google Sheets:")
    traceback.print_exc()
    sheet = None

# بيانات الوظائف والمدن
jobs_list = ["مندوب مبيعات", "مروج", "عامل مخزن", "كاش فان"]
cities_list = [
    "رام الله والبيرة", "القدس", "الخليل", "بيت لحم",
    "نابلس", "جنين", "طولكرم", "قلقيلية", "طوباس",
    "سلفيت", "أريحا"
]

@app.route('/', methods=['GET', 'POST'])
def index():
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

        if sheet:
            try:
                sheet.insert_row(form_data, 2)
                print("✅ أضيفت بيانات جديدة إلى Google Sheet:", form_data)
            except Exception as e:
                print("❌ خطأ أثناء append_row:")
                traceback.print_exc()
        else:
            print("❌ لم يتم تهيئة sheet — راجع رسالة الإقلاع أعلاه.")

        # بعد الإرسال، إعادة التوجيه إلى صفحة Thank You لتجنب إعادة الإرسال عند Refresh
        return redirect(url_for('thank_you'))

    return render_template('jobs_formm.html', jobs=jobs_list, cities=cities_list)

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
