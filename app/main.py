# Flask Tutorial

import os
# from requests import request
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# X = os.getcwd()
# app = Flask(__name__, template_folder="template")
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

X = os.getcwd()

# Set the database URI with an absolute path (works cross-platform)
# app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{X}/test.db"

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(X, 'test.db')}"

# app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'test.db')}"


db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    
    def __repr__(self):
        # return '<Task %r>' % self.id 
        return f'<Task {self.id}>'



def create_db():
    if not os.path.exists("test.db"): 
        with app.app_context():
            db.create_all()
        print("Database created !")

create_db()

@app.route('/', methods=['POST','GET'])
def index():
    # return "Hey there"
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "there was an issue adding your task"        
    else:
        # tasks = Todo.query.order_by(Todo.date).first()
        tasks = Todo.query.order_by(Todo.date).all()
        return render_template('index.html', tasks=tasks)
    
@app.route('/delete/<int:id>')
def Delete_Task(id):
    task = Todo.query.get_or_404(id) #task to delete
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
        return "there was an issue deleting your task"
    

@app.route('/update/<int:id>', methods=['POST','GET'])
def Update_Task(id):
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "there was an error updating your task"
    else:
        # tasks = Todo.query.order_by(Todo.date).all()
        return render_template('update.html', task=task)    

if __name__ == "__main__":
    app.run(debug=True)