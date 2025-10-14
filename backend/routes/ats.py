from flask import Blueprint, request, jsonify
import re
import os
from models import mysql
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
import docx

ats_bp = Blueprint('ats', __name__)

# Lightweight stopwords; avoids heavy NLP deps
STOPWORDS = set(
    """
    a an the and or but if then else when while for to of in on at from by with without as is are was were be been being
    this that those these over under into within out up down it its it's you your he she they we i our us them their his her
    """.strip().split()
)

# Basic hard-skill dictionary to improve signal (extend as needed)
HARD_SKILLS = [
    'python','java','javascript','react','node','flask','django','mysql','postgresql','mongodb','sql','nosql','html','css','git','docker','kubernetes',
    'aws','azure','gcp','linux','bash','rest','graphql','fastapi','spring','hibernate','typescript',
    'data structures','algorithms','oop','ml','machine learning','deep learning','nlp','pandas','numpy','scikit','sklearn','tensorflow','pytorch',
    'power bi','tableau','excel','spark','hadoop','airflow','etl'
]

def tokenize(text: str):
    return [t for t in re.sub(r"[^a-z0-9\s]", " ", (text or "").lower()).split() if t and t not in STOPWORDS and len(t) > 1]

def analyze(resume_text: str, jd_text: str):
    # Tokens and sets
    r_tokens = tokenize(resume_text)
    j_tokens = tokenize(jd_text)
    r_set = set(r_tokens)

    # Heuristic weighting: boost tokens that appear in bullet-like lines or after headings in JD
    weights = {}
    for tok in j_tokens:
        weights[tok] = weights.get(tok, 0) + 1
    # Headings boost
    for line in (jd_text or '').splitlines():
        l = line.strip().lower()
        if any(h in l for h in ['requirements', 'responsibilities', 'must have', 'qualifications', 'skills']):
            for t in tokenize(l):
                weights[t] = weights.get(t, 0) + 2
        if l.startswith('-') or l.startswith('*') or l.startswith('•'):
            for t in tokenize(l):
                weights[t] = weights.get(t, 0) + 1

    # Unique keywords sorted by importance
    keywords = sorted(list(set(j_tokens)), key=lambda t: weights.get(t, 0), reverse=True)
    matched_kw = [k for k in keywords if k in r_set]
    missing_kw = [k for k in keywords if k not in r_set]

    # Skill matching using dictionary (phrase and unigram)
    r_text_low = (resume_text or '').lower()
    skills_matched, skills_missing = [], []
    for s in HARD_SKILLS:
        if s in r_text_low:
            skills_matched.append(s)
        else:
            if any(w in j_tokens for w in s.split()):
                skills_missing.append(s)

    # Subscores
    kw_score = (len(matched_kw) / max(1, len(matched_kw) + len(missing_kw))) * 100
    skill_score = (len(skills_matched) / max(1, len(skills_matched) + len(skills_missing))) * 100

    # Formatting checks
    has_email = re.search(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", resume_text or "", re.I) is not None
    has_phone = re.search(r"(\+\d{1,3}[\s-]?)?\d{10}", resume_text or "") is not None
    words = (resume_text or '').split()
    length_ok = len(words) <= 900
    no_images = True  # on text input, assume OK
    clear_headings = any(h in (resume_text or '').lower() for h in ['experience', 'education', 'projects', 'skills', 'summary'])

    fmt_score_parts = [
        20 if has_email else 0,
        20 if has_phone else 0,
        20 if length_ok else 0,
        20 if no_images else 0,
        20 if clear_headings else 0
    ]
    fmt_score = sum(fmt_score_parts)

    # Final weighted score
    final_score = round(0.5 * kw_score + 0.35 * skill_score + 0.15 * fmt_score)

    # Suggestions
    suggestions = []
    if not has_email: suggestions.append('Add a professional email address in header/contact section.')
    if not has_phone: suggestions.append('Include a reachable phone number with country code.')
    if not length_ok: suggestions.append('Reduce resume length to 1–2 pages (~900 words).')
    if not clear_headings: suggestions.append('Use clear section headings like Summary, Skills, Experience, Education, Projects.')
    if skills_missing[:10]: suggestions.append('Add or emphasize relevant skills: ' + ', '.join(skills_missing[:10]))
    if missing_kw[:10]: suggestions.append('Incorporate role-specific keywords naturally: ' + ', '.join(missing_kw[:10]))

    return {
        'score': final_score,
        'subscores': {
            'keywords': round(kw_score, 1),
            'skills': round(skill_score, 1),
            'formatting': fmt_score
        },
        'matched': matched_kw[:200],
        'missing': missing_kw[:200],
        'skillsMatched': skills_matched[:200],
        'skillsMissing': skills_missing[:200],
        'checks': {
            'hasEmail': has_email,
            'hasPhone': has_phone,
            'lengthOk': length_ok,
            'clearHeadings': clear_headings
        },
        'suggestions': suggestions[:10]
    }

@ats_bp.route('/ats/analyze', methods=['POST'])
def ats_analyze():
    try:
        data = request.get_json(force=True)
        resume_text = data.get('resume_text', '')
        jd_text = data.get('jd_text', '')
        if not jd_text:
            return jsonify({'message': 'jd_text is required'}), 400
        result = analyze(resume_text, jd_text)
        return jsonify(result)
    except Exception as e:
        return jsonify({'message': f'Analysis failed: {str(e)}'}), 500

def extract_text_from_file(path: str) -> str:
    try:
        ext = os.path.splitext(path)[1].lower()
        if ext == '.pdf':
            text = []
            with open(path, 'rb') as f:
                reader = PdfReader(f)
                for page in reader.pages:
                    text.append(page.extract_text() or '')
            return '\n'.join(text)
        if ext in ('.docx',):
            d = docx.Document(path)
            return '\n'.join(p.text for p in d.paragraphs)
        if ext in ('.doc',):
            # .doc not directly supported; return empty, or integrate textract in future
            return ''
        # Fallback: treat as text
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        return ''

@ats_bp.route('/ats/analyze-file', methods=['POST'])
def ats_analyze_file():
    try:
        jd_text = request.form.get('jd_text', '')
        if not jd_text:
            return jsonify({'message': 'jd_text is required'}), 400

        resume_text = ''
        # Option A: analyze uploaded file directly
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename:
                filename = secure_filename(file.filename)
                tmp_path = os.path.join('uploads', f'_tmp_{filename}')
                if not os.path.exists('uploads'):
                    os.makedirs('uploads')
                file.save(tmp_path)
                resume_text = extract_text_from_file(tmp_path)
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass
        # Option B: analyze existing uploaded resume by id
        elif request.form.get('resume_id'):
            resume_id = request.form.get('resume_id')
            cur = mysql.connection.cursor()
            cur.execute("SELECT filepath FROM resumes WHERE id=%s", (resume_id,))
            row = cur.fetchone()
            if row and row.get('filepath') and os.path.exists(row['filepath']):
                resume_text = extract_text_from_file(row['filepath'])

        result = analyze(resume_text, jd_text)
        return jsonify(result)
    except Exception as e:
        return jsonify({'message': f'Analysis failed: {str(e)}'}), 500
