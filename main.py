import os
import sys 
import json
from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = ''  # Required for using sessions

basedir = os.path.abspath(os.path.dirname(__file__))
X = os.getcwd()

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(X, 'test.db')}"
db = SQLAlchemy(app)

# Task Logic
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.id}>'

# Energy Estimation Logic
class Energy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(200), nullable=False)


# Create the database if it doesn't exist
def create_db():
    if not os.path.exists("test.db"):
        with app.app_context():
            db.create_all()
        print("Database created!")

create_db()

# Main route for managing tasks and energy level

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task"


    tasks = Todo.query.order_by(Todo.date).all()
    tasks_list = [task.content for task in tasks]
    # session['tasks_list'] = json.dumps(tasks_list)
    stringifiedtasklist = ', '.join(tasks_list)
    session['tasks_list'] = stringifiedtasklist
    return render_template('index.html', tasks=tasks)

@app.route('/finalize_tasks', methods=['POST'])
def finalize_tasks():
    return redirect('/energy')

@app.route('/energy', methods=['POST', 'GET'])
def energy():
    if request.method == 'POST':
        energy_level = request.form['energy']
        new_energy = Energy(level=energy_level)
        try:
            db.session.add(new_energy)
            db.session.commit()
            session['energy_level'] = energy_level
            flash(f'Energy level set to {energy_level}', 'success')
            # return redirect('/conversation')
        except:
            flash('There was an issue saving the energy level', 'error')
            return redirect('/energy')

    return render_template('energy.html')

@app.route('/conversation', methods=['GET'])
# Function to retrieve numeric energy value from the database
def get_numeric_energy_value():
    energy_messages = {
    "Extremely High": "Wow, you're full of energy! You're ready to take on anything that comes your way. Keep up the great work!",
    "High": "You're feeling energized and ready to tackle challenges! Let's keep the momentum going!",
    "Medium": "You're in a good place—enough energy to stay productive without feeling drained. Keep it balanced!",
    "Low": "It looks like you're running low on energy. Take a break and recharge, you'll be back at it in no time!",
    "Extremely Low": "You're feeling really low on energy. It's time to rest and take care of yourself. Don't worry, you'll feel better soon!"
                            }
    # Retrieve the most recent energy record for the current session's energy level
    energy = session.get('energy_level')
    # energy = Energy.query.filter_by(level=session.get('energy_level')).order_by(Energy.id.desc()).first()
    
    return render_template('conversation.html', energy=energy, energy_messages=energy_messages)


@app.route('/LLM', methods=['POST'])
def LLM():
    ## JSON
    TLJ = session.get('tasks_list','[]')
    TL = json.loads(TLJ)
    
    ## STRING
    tasks_list = session.get('tasks_list', '')
    
    return render_template('notyet.html', TL=TL) #tasks_list = tasks_list

# Delete task route
@app.route('/delete/<int:id>')
def delete_task(id):
    task = Todo.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an issue deleting your task"

# Update task route
@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update_task(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error updating your task"
    return render_template('update.html', task=task)



# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)



