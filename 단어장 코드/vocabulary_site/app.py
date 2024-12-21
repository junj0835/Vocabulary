from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vocabulary.db'
db = SQLAlchemy(app)

# Database Model
class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False)
    definition = db.Column(db.String(500), nullable=False)
    example = db.Column(db.String(500))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def home():
    words = Word.query.order_by(Word.date_added.desc()).all()
    return render_template('home.html', words=words)

@app.route('/add', methods=['GET', 'POST'])
def add_word():
    if request.method == 'POST':
        word = Word(
            word=request.form['word'],
            definition=request.form['definition'],
            example=request.form['example']
        )
        db.session.add(word)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_word.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)