from flask import Flask, render_template
from models.db import db
from routes.document_management import document_management_bp
from routes.llm import llm_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)

app.register_blueprint(document_management_bp)
app.register_blueprint(llm_bp)

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

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

if __name__ == "__main__":
    app.run(port=5000, debug=True)