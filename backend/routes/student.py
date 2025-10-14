@app.route("/student/login", methods=["POST"])
def student_login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM students WHERE email=%s AND password=%s", (email, password))
    student = cursor.fetchone()

    if student:
        return jsonify({"message": "Login successful", "student": email})
    else:
        return jsonify({"error": "Invalid credentials"}), 401
