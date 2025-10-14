from flask import Flask
from models import app
from flask_cors import CORS

# Enable frontend access
CORS(app)

# Import API routes
from routes.auth import auth_bp
from routes.jobs import jobs_bp
from routes.resumes import resume_bp
from routes.applications import applications_bp
from routes.interviews import interviews_bp
from routes.analytics import analytics_bp
from routes.ats import ats_bp

# Register routes
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(jobs_bp, url_prefix='/api')
app.register_blueprint(resume_bp, url_prefix='/api')
app.register_blueprint(applications_bp, url_prefix='/api')
app.register_blueprint(interviews_bp, url_prefix='/api')
app.register_blueprint(analytics_bp, url_prefix='/api')
app.register_blueprint(ats_bp, url_prefix='/api')

@app.route('/')
def home():
    return "Placement Management System Backend is Running"

if __name__ == "__main__":
    app.run(debug=True)
