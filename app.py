from flask import Flask, render_template, request
import csv
import os

app = Flask(__name__)

CSV_FILE = os.path.join(os.path.dirname(__file__), "submissions.csv")

# إنشاء ملف CSV إذا لم يكن موجود
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'name','age','phone','email','job','school','university',
            'major','city','address','experience','references'
        ])

@app.route('/', methods=['GET', 'POST'])
def job_form():
    message = None
    form_submitted = False

    if request.method == 'POST':
        form_data = {
            'name': request.form.get('name'),
            'age': request.form.get('age'),
            'phone': request.form.get('phone'),
            'email': request.form.get('email'),
            'job': request.form.get('job'),
            'school': request.form.get('school'),
            'university': request.form.get('university'),
            'major': request.form.get('major'),
            'city': request.form.get('city'),
            'address': request.form.get('address'),
            'experience': request.form.get('experience'),
            'references': request.form.get('references')
        }

        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=form_data.keys())
            writer.writerow(form_data)

        message = "تم إرسال طلبك بنجاح!"
        form_submitted = True

    # إضافة قيمة عشوائية لتجنب الكاش للـ CSS
    version = os.urandom(4).hex()
    return render_template('jobs_form.html', message=message, form_submitted=form_submitted, version=version)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
