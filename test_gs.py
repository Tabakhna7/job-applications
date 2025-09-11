# test_gs.py
import gspread
from google.oauth2.service_account import Credentials
import traceback

SERVICE_ACCOUNT_FILE = "credentials.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"]

try:
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    gc = gspread.authorize(creds)
    sh = gc.open("Job Applications")   # اسم الشيت كما في حسابك
    ws = sh.sheet1
    ws.append_row(["TEST", "test@example.com", "تجربة اتصال"])
    print("✅ نجح: تمت إضافة صف اختبار إلى Google Sheet")
except Exception as e:
    print("❌ فشل الاتصال / إضافة صف. الخطأ:")
    traceback.print_exc()
