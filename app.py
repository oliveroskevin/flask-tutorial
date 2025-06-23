from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created= db.Column(db.DateTime, default= datetime.now(timezone.utc))

    def __repr__(self):
        return '<Task %r>' % self.id

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    date_uploaded = db.Column(db.DateTime, default= datetime.now(timezone.utc))
    date_modified = db.Column(db.DateTime, default= datetime.now(timezone.utc))

    def __repr__(self):
        return '<Document %r>' % self.id
    

# PAGES    
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/prototypes')
def prototypes():
    return render_template('prototypes.html')

@app.route('/login-page')
def login_page():
    return render_template('login-page.html')

@app.route('/documents', methods=['POST', 'GET'])
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
            return redirect('/documents')
        except Exception as e:
            return f'There was an issue adding your document: {e}', 500
    else:
        documents = Document.query.order_by(Document.date_uploaded.desc()).all()
        return render_template('documents.html', documents=documents)

@app.route('/documents/edit/<int:id>', methods=['POST'])
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

@app.route('/documents/delete/<int:id>', methods=['DELETE'])
def delete_document(id):
    doc_to_delete = Document.query.get_or_404(id)
    try:
        db.session.delete(doc_to_delete)
        db.session.commit()
        return 'Document deleted successfully', 200
    except Exception as e:
        db.session.rollback()
        return f'There was a problem deleting that document: {e}', 500

if __name__ == "__main__":
    app.run(debug=True)