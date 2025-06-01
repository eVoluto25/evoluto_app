from flask import Flask, request, jsonify
from email_receiver import connect_email, process_emails

app = Flask(__name__)

@app.route("/trigger", methods=["POST"])
def trigger():
    try:
        mail = connect_email()
        if mail:
            process_emails(mail)
            return jsonify({"status": "ok"}), 200
        else:
            return jsonify({"error": "Connessione email fallita"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
