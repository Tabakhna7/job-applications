import gspread
from google.oauth2.service_account import Credentials
from flask import Flask, render_template, request


app = Flask(__name__)

# --- إعداد Google Sheets ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("google-credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Job Applications").sheet1  # تأكد أن اسم الـ Sheet مطابق

# --- بيانات الوظائف والمدن ---
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
        # جمع البيانات من النموذج
        form_data = {
            'Name': request.form.get('name'),
            'Email': request.form.get('email'),
            'Job': request.form.get('job'),
            'Phone': request.form.get('phone'),
            'Age': request.form.get('age'),
            'School': request.form.get('school'),
            'University': request.form.get('university'),
            'Major': request.form.get('major'),
            'City': request.form.get('city'),
            'Address': request.form.get('address'),
            'Experience': request.form.get('experience'),
            'References': request.form.get('references')
        }

        # --- أرسل البيانات إلى Google Sheets ---
        row = [
            form_data['Name'], form_data['Email'], form_data['Job'], form_data['Phone'],
            form_data['Age'], form_data['School'], form_data['University'], form_data['Major'],
            form_data['City'], form_data['Address'], form_data['Experience'], form_data['References']
        ]
        try:
            sheet.append_row(row)
            submitted = 'true'
        except Exception as e:
            print("❌ Error appending row to Google Sheets:", e)

    return render_template('jobs_formm.html', submitted=submitted, jobs=jobs_list, cities=cities_list)

if __name__ == '__main__':
    app.run(debug=True)
