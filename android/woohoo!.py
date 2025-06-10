from flask import Flask, render_template
import subprocess
import time
import threading

app = Flask(__name__)
last_state = None 


def is_charging():
    result = subprocess.run(["adb", "shell", "dumpsys", "battery"], capture_output=True, text=True)
    output = result.stdout
    return "AC powered: true" in output or "USB powered: true" in output


def changestatus():
    print("พาโวเสเตตัดเชน!!!!!")


def mong():
    global last_state
    while True:
        charging = is_charging()
        if last_state is None:
            last_state = charging
        elif last_state and not charging:
            changestatus()
        last_state = charging
        time.sleep(1)



@app.route("/")
def home():
    status_text = "good" if last_state else "⚠️ bad"
    return f"<h1>Power Status: {status_text}</h1>"


if __name__ == "__main__":
    threading.Thread(target=mong, daemon=True).start()

    app.run(host="0.0.0.0", port=5000)
