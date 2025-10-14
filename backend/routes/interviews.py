from flask import Blueprint, request, jsonify
from models import mysql

interviews_bp = Blueprint('interviews', __name__)

@interviews_bp.route('/interviews/schedule', methods=['POST'])
def schedule_interview():
    try:
        data = request.json
        application_id = data.get('application_id')
        scheduled_at = data.get('scheduled_at')  # ISO datetime string
        mode = data.get('mode', 'online')
        notes = data.get('notes', '')
        if not application_id or not scheduled_at:
            return jsonify({"message": "Missing fields"}), 400
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO interviews (application_id, scheduled_at, mode, notes) VALUES (%s,%s,%s,%s)",
            (application_id, scheduled_at, mode, notes)
        )
        mysql.connection.commit()
        return jsonify({"message": "Interview scheduled"})
    except Exception as e:
        return jsonify({"message": f"Schedule failed: {str(e)}"}), 500

@interviews_bp.route('/interviews/by-application/<int:application_id>', methods=['GET'])
def list_interviews_for_application(application_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM interviews WHERE application_id=%s ORDER BY scheduled_at DESC", (application_id,))
        rows = cur.fetchall()
        return jsonify(rows)
    except Exception as e:
        return jsonify({"message": f"Fetch failed: {str(e)}"}), 500
