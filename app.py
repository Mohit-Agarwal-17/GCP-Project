from flask import Flask, request, jsonify
from PyPDF2 import PdfMerger
import io
import os
from dotenv import load_dotenv
from flask_cors import CORS
import base64

app = Flask(__name__)

CORS(app)  # Enable CORS for all routes and origins

# Configure FLASK_DEBUG from environment variable
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG')

@app.route('/merge_pdfs', methods=['POST'])
def merge_pdfs():
    # Check if two files are provided
    if 'file1' not in request.files or 'file2' not in request.files:
        return jsonify({'error': 'Two PDF files are required.'}), 400
    
    file1 = request.files['file1']
    file2 = request.files['file2']
    
    # Check if files are PDFs
    if file1.filename.endswith('.pdf') and file2.filename.endswith('.pdf'):
        # Create a PdfMerger object
        merger = PdfMerger()
        
        # Merge the PDFs
        merger.append(file1)
        merger.append(file2)
        
        # Save the merged PDF to a BytesIO object
        merged_pdf_stream = io.BytesIO()
        merger.write(merged_pdf_stream)
        merged_pdf_stream.seek(0)
        
        # Close the merger object
        merger.close()
        
        # Encode the merged PDF bytes to base64
        merged_pdf_base64 = base64.b64encode(merged_pdf_stream.getvalue()).decode('utf-8')
        
        return jsonify({'merged_pdf': merged_pdf_base64}), 200
    
    else:
        return jsonify({'error': 'Both files should be in PDF format.'}), 400


if __name__ == '__main__':
    app.run()
