import os
import agents
from query import Query
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

# Task Object
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.id}>'

# Energy Object
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

# Main routes for managing tasks

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
    tasks_list = [task.content for task in tasks] #this is a list of strings
    stringifiedtasklist = ', '.join(tasks_list) #this is a string containing a list of strings
    session['tasks_list'] = stringifiedtasklist
    return render_template('index.html', tasks=tasks)

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


# Transitional Route (Task-to-Energy)

@app.route('/finalize_tasks', methods=['POST'])
def finalize_tasks():
    return redirect('/energy')

# Main routes for managing energy

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
            # return redirect('/energyconversation')
        except:
            flash('There was an issue saving the energy level', 'error')
            return redirect('/energy')

    return render_template('energy.html')

# Main routes for managing user-system interaction

@app.route('/energyconversation', methods=['POST'])
# Function to retrieve numeric energy value from the database
def energyfunc():
    # Retrieve the most recent energy record for the current session's energy level
    energy = session.get('energy_level')
    if not energy:
        flash("energy level is missing",'error')
    # Run the energy agent query
    energy_resp = agents.run_energy_query(energy)
    
    usermessage = request.form['userMessage']
    if usermessage:
        conversational_resp = agents.continue_conversation(usermessage)
        
    session['updated_energy_level'] = usermessage
    
    return render_template('energy_conversation.html', energy=energy, energy_resp=energy_resp, conversational_resp=conversational_resp)



@app.route('/taskconversation', methods=['POST'])
# Function to retrieve task list from the session and input it to the LLM
def taskfunc():
    tasks_list = session.get('tasks_list')
    if not tasks_list:
        flash("task list is missing.", 'error')
    task_resp = agents.run_task_query(tasks_list)
    usermessage = request.form['userMessage']
    if usermessage:
        conversational_resp = agents.continue_conversation(usermessage)

    return render_template('taskreq_conversation.html', task_resp=task_resp, conversational_resp=conversational_resp)

@app.route('/allocationconversation', methods=['POST'])
# Function to retrieve task list from the session and input it to the LLM
def allocfunc():
    tasks_list = session.get('tasks_list')
    if not tasks_list:
        flash("task list is missing.", 'error')
    allocation_resp = agents.run_allocation_query(tasks_list)
    usermessage = request.form['userMessage']
    if usermessage:
        conversational_resp = agents.continue_conversation(usermessage)

    return render_template('allocation_conversation.html', allocation_resp=allocation_resp, conversational_resp=conversational_resp)


# Main route for managing the output

@app.route('/output', methods=['GET'])
def task_output():
    # Fetch data from session
    energy_level = session.get('updated_energy_level', "No energy level provided.") #string
    tasks_list_str = session.get('tasks_list', "No tasks provided.") # string containing a list of strings
    
    # Initialize the Query instance
    query_instance = Query(name="Task-Energy Output Management")

    # Concatenate inputs into a single context string
    context = query_instance.concatenate_inputs(energy_level, tasks_list_str)

    # Pass context to the query runner or agent
    optimal_task_list = agents.run_output_query(context)
    
    return render_template('output.html', optimal_task_list=optimal_task_list)



# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)



