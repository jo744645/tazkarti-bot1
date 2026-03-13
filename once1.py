# -*- coding: utf-8 -*-
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# إعدادات تليجرام
BOT_TOKEN = '7204967716:AAGJZ5lGRqcn0DNR2zJelfRqCFpZOvGeN8U'
CHAT_ID = '1103230055'

# كلمات البحث
keywords = ["الأهلي", "Al Ahly", "Ahly", "AL-AHLY", "Al Ahly FC"]

# إعداد Selenium
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# رابط موقع تذكرتي
url = 'https://www.tazkarti.com/#/matches'

# متغير لمنع تكرار الإرسال
ticket_sent = False

def send_telegram_message(message):
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message}
    try:
        requests.post(telegram_url, data=payload)
    except Exception as e:
        print("❌ فشل إرسال رسالة تليجرام:", e)

def check_tickets():
    global ticket_sent
    print("⏳ جاري التحقق من تذاكر الأهلي...")

    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        tickets_available = (
            any(word.lower() in soup.text.lower() for word in keywords)
            and "تم غلق الحجز" not in soup.text
        )

        if tickets_available:
            if not ticket_sent:
                print("✅ التذاكر متاحة! إرسال إشعار...")
                send_telegram_message(
                    "🎟️ فيه تذاكر متاحة لـ Al Ahly FC!\nاحجز من هنا: https://www.tazkarti.com/#/matches"
                )
                ticket_sent = True
            else:
                print("✅ التذاكر متاحة لكن تم الإرسال قبل كده.")
        else:
            print("❌ مفيش تذاكر مفتوحة للأهلي دلوقتي.")

    except Exception as e:
        print("⚠️ حصل خطأ:", e)

# تشغيل كل 10 ثواني بالظبط
interval = 10

while True:
    start_time = time.time()

    check_tickets()

    elapsed = time.time() - start_time
    sleep_time = interval - elapsed

    if sleep_time > 0:
        time.sleep(sleep_time)
