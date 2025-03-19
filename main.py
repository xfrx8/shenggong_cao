import threading, webview
from app import app

if __name__ == '__main__':
    threading.Thread(target=lambda: app.run(host="127.0.0.1", port=5000, debug=False), daemon=True).start()
    webview.create_window("Standard Curve Fitting", "http://127.0.0.1:5000", width=1800, height=1080)
    webview.start()
