from flask import Blueprint, request, jsonify
from models import mysql

jobs_bp = Blueprint('jobs', __name__)

# Add a job
@jobs_bp.route('/add', methods=['POST'])
def add_job():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    recruiter_id = data.get('recruiter_id')

    if not title or not description or not recruiter_id:
        return jsonify({"message":"Missing fields"}), 400

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO jobs (title, description, recruiter_id) VALUES (%s, %s, %s)", (title, description, recruiter_id))
    mysql.connection.commit()
    return jsonify({"message":"Job added successfully"})

# List all jobs
@jobs_bp.route('/list', methods=['GET'])
def list_jobs():
    cur = mysql.connection.cursor()
    cur.execute("SELECT jobs.*, recruiters.name AS recruiter_name FROM jobs JOIN recruiters ON jobs.recruiter_id = recruiters.id")
    jobs = cur.fetchall()
    return jsonify(jobs)
