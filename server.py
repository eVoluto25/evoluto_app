import subprocess
import threading

@app.route("/trigger", methods=["POST"])
def trigger_main():
    def run_script():
        subprocess.run(["python", "main.py"])
    
    threading.Thread(target=run_script).start()
    return "✅ Script avviato in background", 200
