from flask import Flask, render_template, jsonify, request # เพื่อทำ api
from flask_cors import CORS # เพื่อทำ api
import subprocess
import time
import threading

app = Flask(__name__)
last_state = None 


def is_charging(): # เช็ค สถานะการชาร์ตของ มือถือ โดยใช้ adb
    result = subprocess.run(["adb", "shell", "dumpsys", "battery"], capture_output=True, text=True)
    output = result.stdout
    return "AC powered: true" in output or "USB powered: true" in output



def changestatus(): 
    print("พาโวเสเตตัดเชน!!!!!")


def mong(): # เช็ค last_state ของ adb (สถานะการชาร์ตของ มือถือ)
    global last_state
    while True:
        charging = is_charging()
        if last_state is None:
            last_state = charging
        elif last_state and not charging:
            changestatus()
        last_state = charging
        time.sleep(1)



@app.route("/") # ระบบ website(localhost)
def home(): 

    status_text = "good" if last_state else "⚠️ เหี้ย"
    return f"<h1>Power Status: {status_text}</h1>"

@app.route('/api/data', methods=['GET']) # ระบบ api
def get_data():
    status_text = "charging" if last_state else "disconnected"
    data = { "status": status_text }
    return jsonify(data)

#@app.route("/มายมึงแต้")     
#def check():
    #status_text = "good" if last_state else "⚠️ เหี้ย"
    #return render_template("check.html", INPUT_NAME_1 = status_text)

    #  อันนี้ลองทำให้มัน edit html โดยตรงแต่ลืมว่าเรามี api อยู่แล้ว (แฮะๆ)

if __name__ == "__main__":
    threading.Thread(target=mong, daemon=True).start()
    CORS(app)

    app.run(host="0.0.0.0", port=5000)
