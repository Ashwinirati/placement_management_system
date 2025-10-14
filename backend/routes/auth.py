from flask import Blueprint, request, jsonify
from models import mysql
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

# Student registration
@auth_bp.route('/register/student', methods=['POST'])
def register_student():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if not name or not email or not password:
            return jsonify({"message":"Missing fields"}), 400

        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM students WHERE email=%s", (email,))
        if cur.fetchone():
            return jsonify({"message":"Email already registered"}), 400

        hashed = generate_password_hash(password)
        cur.execute("INSERT INTO students (name,email,password) VALUES (%s,%s,%s)", (name,email,hashed))
        mysql.connection.commit()
        return jsonify({"message":"Student registered successfully"})
    except Exception as e:
        return jsonify({"message": f"Registration failed: {str(e)}"}), 500

# Student login
@auth_bp.route('/login/student', methods=['POST'])
def login_student():
    try:
        data = request.json
        email = data['email']
        password = data['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM students WHERE email=%s", (email,))
        user = cur.fetchone()
        if user and check_password_hash(user['password'], password):
            return jsonify({"message":"Login success", "user": {"id": user['id'], "name": user['name'], "email": user['email']}})
        return jsonify({"message":"Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"message": f"Login failed: {str(e)}"}), 500

# Recruiter registration
@auth_bp.route('/register/recruiter', methods=['POST'])
def register_recruiter():
    try:
        data = request.json
        name = data['name']
        email = data['email']
        password = data['password']

        if not name or not email or not password:
            return jsonify({"message":"Missing fields"}), 400

        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM recruiters WHERE email=%s", (email,))
        if cur.fetchone():
            return jsonify({"message":"Email already registered"}), 400

        hashed = generate_password_hash(password)
        cur.execute("INSERT INTO recruiters (name,email,password) VALUES (%s,%s,%s)", (name,email,hashed))
        mysql.connection.commit()
        return jsonify({"message":"Recruiter registered successfully"})
    except Exception as e:
        return jsonify({"message": f"Registration failed: {str(e)}"}), 500

# Recruiter login
@auth_bp.route('/login/recruiter', methods=['POST'])
def login_recruiter():
    try:
        data = request.json
        email = data['email']
        password = data['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM recruiters WHERE email=%s", (email,))
        user = cur.fetchone()
        if user and check_password_hash(user['password'], password):
            return jsonify({"message":"Login success", "user": {"id": user['id'], "name": user['name'], "email": user['email']}})
        return jsonify({"message":"Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"message": f"Login failed: {str(e)}"}), 500
