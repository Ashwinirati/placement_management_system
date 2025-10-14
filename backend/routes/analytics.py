from flask import Blueprint, jsonify
from models import mysql

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics/summary', methods=['GET'])
def summary():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) AS c FROM students"); students = cur.fetchone()['c']
        cur.execute("SELECT COUNT(*) AS c FROM recruiters"); recruiters = cur.fetchone()['c']
        cur.execute("SELECT COUNT(*) AS c FROM jobs"); jobs = cur.fetchone()['c']
        cur.execute("SELECT COUNT(*) AS c FROM applications"); applications = cur.fetchone()['c']
        cur.execute("SELECT COUNT(*) AS c FROM applications WHERE status='hired'"); hired = cur.fetchone()['c']
        return jsonify({
            'students': students,
            'recruiters': recruiters,
            'jobs': jobs,
            'applications': applications,
            'hired': hired
        })
    except Exception as e:
        return jsonify({"message": f"Failed to fetch analytics: {str(e)}"}), 500
