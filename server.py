import subprocess

@app.route("/trigger", methods=["POST"])
def trigger_main():
    try:
        result = subprocess.run(["python", "main.py"], check=True, capture_output=True, text=True)
        return f"✅ Script eseguito:\n{result.stdout}", 200
    except subprocess.CalledProcessError as e:
        return f"❌ Errore:\nSTDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}", 500
