import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from detector import analyze_document

app = Flask(__name__)

# Configure upload directory and file restrictions
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 30 * 1024 * 1024  # 30 MB limit

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    # 1. Validation checks
    if 'document' not in request.files:
        return jsonify({"error": "No document file uploaded."}), 400

    file = request.files['document']
    query = request.form.get('query', '').strip()

    if file.filename == '':
        return jsonify({"error": "No file selected."}), 400

    if not query:
        return jsonify({"error": "Please enter a topic or question to search."}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid format. Only PDF and DOCX files are allowed."}), 400

    # 2. Save file temporarily
    filename = secure_filename(file.filename)
    saved_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(saved_path)

    # 3. Process via ML Engine
    try:
        results = analyze_document(query, saved_path, filename)
    except Exception as e:
        results = {"error": f"Internal analysis failed: {str(e)}"}
    finally:
        # Clean up uploaded file from disk after analysis
        if os.path.exists(saved_path):
            os.remove(saved_path)

    if "error" in results:
        return jsonify(results), 400

    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)