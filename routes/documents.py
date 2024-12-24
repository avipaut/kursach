from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory
import os

documents_bp = Blueprint('documents', __name__)
UPLOAD_FOLDER = "uploaded_documents"

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Allowed file extension check
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['pdf', 'docx', 'txt', 'jpg', 'png']

@documents_bp.route('/')
def documents():
    # List the documents in the upload folder
    documents = os.listdir(UPLOAD_FOLDER)
    
    # Print documents to debug what's being fetched
    print(f"Documents found: {documents}")  # Debugging line to check what's found

    # If there are no documents, show a message
    if not documents:
        documents = ["No documents available. Upload a new file!"]

    return render_template('documents.html', documents=documents)

@documents_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        print(f"File uploaded: {filename}")  # Debugging line to check if the file is being uploaded
        return redirect(url_for('documents.documents'))  # Refresh the page to reload the documents
    
    return redirect(url_for('documents.documents'))

@documents_bp.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    try:
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        os.remove(filepath)
        print(f"File deleted: {filename}")  # Debugging line to check if file is being deleted
        return redirect(url_for('documents.documents'))
    except FileNotFoundError:
        return "File not found", 404

@documents_bp.route('/view/<filename>')
def view_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@documents_bp.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
