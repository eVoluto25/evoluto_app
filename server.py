from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route("/trigger", methods=["POST"])
def trigger_main():
    try:
        # Avvia main.py come sottoprocesso
        subprocess.run(["python", "main.py"], check=True)
        return "✅ Script eseguito correttamente", 200
    except subprocess.CalledProcessError as e:
        return f"❌ Errore esecuzione: {str(e)}", 500

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
