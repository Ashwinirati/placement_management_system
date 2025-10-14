from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from models import mysql

resume_bp = Blueprint('resume', __name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@resume_bp.route('/upload/<int:student_id>', methods=['POST'])
def upload_resume(student_id):
    if 'file' not in request.files:
        return jsonify({"message":"No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message":"No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        file.save(path)
        # Save metadata in database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO resumes (student_id, filename, filepath) VALUES (%s, %s, %s)", (student_id, filename, path))
        mysql.connection.commit()
        resume_id = cur.lastrowid
        return jsonify({"message":"Resume uploaded successfully", "resume_id": resume_id})
    return jsonify({"message":"File type not allowed"}), 400

@resume_bp.route('/resumes/student/<int:student_id>', methods=['GET'])
def list_resumes_for_student(student_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, filename, filepath, created_at FROM resumes WHERE student_id=%s ORDER BY created_at DESC", (student_id,))
        rows = cur.fetchall()
        return jsonify(rows)
    except Exception as e:
        return jsonify({"message": f"Failed to fetch resumes: {str(e)}"}), 500
