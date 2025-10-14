from flask import Blueprint, request, jsonify
from models import mysql

applications_bp = Blueprint('applications', __name__)

@applications_bp.route('/apply', methods=['POST'])
def apply_job():
    try:
        data = request.json
        student_id = data.get('student_id')
        job_id = data.get('job_id')
        if not student_id or not job_id:
            return jsonify({"message": "Missing fields"}), 400
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO applications (student_id, job_id) VALUES (%s, %s)
        """, (student_id, job_id))
        mysql.connection.commit()
        return jsonify({"message": "Applied successfully"})
    except Exception as e:
        return jsonify({"message": f"Apply failed: {str(e)}"}), 500

@applications_bp.route('/applications/student/<int:student_id>', methods=['GET'])
def list_student_applications(student_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT a.id, a.status, a.created_at, j.id AS job_id, j.title, j.description,
                   r.name AS recruiter_name
            FROM applications a
            JOIN jobs j ON a.job_id = j.id
            JOIN recruiters r ON j.recruiter_id = r.id
            WHERE a.student_id=%s
            ORDER BY a.created_at DESC
        """, (student_id,))
        apps = cur.fetchall()
        return jsonify(apps)
    except Exception as e:
        return jsonify({"message": f"Fetch failed: {str(e)}"}), 500

@applications_bp.route('/applications/<int:application_id>/status', methods=['PATCH'])
def update_application_status(application_id):
    try:
        data = request.json
        status = data.get('status')
        if status not in ['applied','shortlisted','rejected','interview_scheduled','hired']:
            return jsonify({"message": "Invalid status"}), 400
        cur = mysql.connection.cursor()
        cur.execute("UPDATE applications SET status=%s WHERE id=%s", (status, application_id))
        mysql.connection.commit()
        return jsonify({"message": "Status updated"})
    except Exception as e:
        return jsonify({"message": f"Update failed: {str(e)}"}), 500
