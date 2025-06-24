from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime, timezone
from models.db import db
from models.document import Document

document_management_bp = Blueprint('document_management_bp', __name__, template_folder='../templates', static_folder='../static')

@document_management_bp.route('/documents', methods=['POST', 'GET'])
def documents():
    if request.method == 'POST':
        file_name = request.form.get('name')
        file_size = request.form.get('size')
        file_type = request.form.get('type')

        if not all([file_name, file_size, file_type]):
            return 'Missing data', 400

        new_document = Document(
            name=file_name,
            size=int(file_size),
            type=file_type
        )

        try:
            db.session.add(new_document)
            db.session.commit()
            return redirect(url_for('document_management_bp.documents'))
        except Exception as e:
            return f'There was an issue adding your document: {e}', 500
    else:
        documents = Document.query.order_by(Document.date_uploaded.desc()).all()
        return render_template('documents.html', documents=documents)

@document_management_bp.route('/documents/edit/<int:id>', methods=['POST'])
def edit_document(id):
    doc_to_edit = Document.query.get_or_404(id)
    data = request.get_json()
    new_name = data.get('name')

    if not new_name:
        return 'New name is required', 400

    doc_to_edit.name = new_name
    doc_to_edit.date_modified = datetime.now(timezone.utc)
    try:
        db.session.commit()
        return 'Document updated successfully', 200
    except Exception as e:
        db.session.rollback()
        return f'There was an issue updating the document: {e}', 500

@document_management_bp.route('/documents/delete/<int:id>', methods=['DELETE'])
def delete_document(id):
    doc_to_delete = Document.query.get_or_404(id)
    try:
        db.session.delete(doc_to_delete)
        db.session.commit()
        return 'Document deleted successfully', 200
    except Exception as e:
        db.session.rollback()
        return f'There was a problem deleting that document: {e}', 500
