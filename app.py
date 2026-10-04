from flask import Flask, render_template, request, jsonify
import os
import uuid
from werkzeug.utils import secure_filename
from ocr_engine import parse_id, parse_premium, parse_invoice, verify_claim

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.errorhandler(Exception)
def handle_exception(e):
    # Return JSON instead of HTML for HTTP errors
    return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if 'id_image' not in request.files or 'premium_image' not in request.files or 'invoice_image' not in request.files:
        return jsonify({'error': 'Missing one or more required images (ID, Premium, Invoice)'}), 400

    id_img = request.files['id_image']
    premium_img = request.files['premium_image']
    invoice_img = request.files['invoice_image']

    paths = {}
    for name, f in [('id', id_img), ('premium', premium_img), ('invoice', invoice_img)]:
        if f.filename == '':
            return jsonify({'error': f'Empty filename for {name}'}), 400
        
        # Prevent file overwrite/locking issues by generating unique filenames
        safe_name = secure_filename(f.filename)
        if not safe_name:
            safe_name = "image.png"
        unique_filename = f"{uuid.uuid4().hex}_{safe_name}"
        path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        f.save(path)
        paths[name] = path

    # Process using OCR
    id_data = parse_id(paths['id'])
    premium_data = parse_premium(paths['premium'])
    invoice_data = parse_invoice(paths['invoice'])

    # Verify claim logic
    result = verify_claim(id_data, premium_data, invoice_data)

    return jsonify({
        'id_data': id_data,
        'premium_data': premium_data,
        'invoice_data': invoice_data,
        'verification': result
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
