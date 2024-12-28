import numpy as np
import os
import secrets
import agents
from query import Query
import json
from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

def daycategory(hour):
    if 5 <= hour < 9:
        return "Early Morning"
    elif 9 <= hour < 12:
        return "Late Morning"
    elif 12 <= hour < 17:
        return "Afternoon"
    elif 17 <= hour < 20:
        return "Evening"
    elif 20 <= hour < 24:
        return "Night"
    else:
        return "Midnight"

def daymetric(peak_daytime,current_daytime):
    daydict = {
        "Early Morning": 1,
        "Late Morning": 2,
        "Afternoon": 3,
        "Evening": 4,
        "Night": 5,
        "Midnight": 6
    }
    
    daydist= {peak_daytime : 6} # as maximum value 
    L = daydict.copy()
    L.pop(peak_daytime)
    for dt in L:
        daydist[dt] = 6 - abs(daydict[peak_daytime] - daydict[dt])
        
    return daydist[current_daytime]
    
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Required for using sessions

basedir = os.path.abspath(os.path.dirname(__file__))
X = os.getcwd()

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(X, 'test.db')}"
db = SQLAlchemy(app)

# Task Object
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f'<Task {self.id}>'

# Energy Object
class Energy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(200), nullable=False)


class UpdatedToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    energy_required = db.Column(db.String(200), nullable=False)
    preparation = db.Column(db.String(200), nullable=False)
    task_type = db.Column(db.String(200), nullable=False)
    recommended_start_time = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f'<Task {self.id}>'

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

    tasks = Todo.query.order_by(Todo.date).all() # this is a Todo object (db.Model) (tasks[0] is the earliest and the most prioritized)
    tasks_list = [task.content for task in tasks] #this is a list of strings (tasks[0] is the earliest and the most prioritized)
    stringifiedtasklist = ', '.join(tasks_list) #this is a string containing a list of strings
    # to converse back to task list: tasks_list = stringifiedtasklist.split(', ')
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

# User Data
@app.route('/data', methods=['POST', 'GET'])
def submit_form():
    energy_dist = {"extremely high": 90, "high": 70, "moderate": 50, "low": 30, "extremely low": 10}
    currenthour = datetime.today().hour
    day_category = daycategory(currenthour)
    if request.method == 'POST':
        data_list = [
            request.form.get('clarity'),
            request.form.get('focus'),
            request.form.get('fatigue'),
            request.form.get('readiness'),
            request.form.get('load'),
            request.form.get('motivation'),
            request.form.get('stress'),
            request.form.get('physical_fatigue'),
            daymetric(request.form.get('circadian_rhythm'), day_category),
            request.form.get('trend'),
            request.form.get('external_stimulation'),
            request.form.get('interaction_energy'),
            request.form.get('task_initiation')
        ]
        # Energy Scoring Function (Weighted Average)
        N = len(data_list)
        weights = np.random.pareto(2.0,N)
        weights = weights/weights.sum() # Normalize to sum to 1
        
        weighted_sum = 0
        for k in range(N):
            weighted_sum += weights[k]*data_list[k]
        
        average_energy = weighted_sum/N

        #Energy Threshold Function
        # Determine energy level category
        if average_energy >= energy_dist["extremely high"]:
            energy_level = "extremely high"
        elif average_energy >= energy_dist["high"]:
            energy_level = "high"
        elif average_energy >= energy_dist["moderate"]:
            energy_level = "moderate"
        elif average_energy >= energy_dist["low"]:
            energy_level = "low"
        else:
            energy_level = "extremely low"
                    
        new_energy = Energy(level=energy_level)
        try:
            db.session.add(new_energy)
            db.session.commit()
            session['energy_level'] = energy_level
            flash(f'Energy level set to {energy_level}', 'success')
        except:
            flash('There was an issue saving the energy level', 'error')
            return redirect('/data')

    return render_template('data.html')

# Main route for managing the output
@app.route('/output', methods=['GET', 'POST'])
def Sort():
    ###SORTING ALGORITHM (better don't trust the fucking LLM in this) -> trade-off: the llm output should be as the dict keys otherwise errors
    ##LLMs are bad at reasoning, especially multi-variable reasoning, therefore restricting it to purely formating task is more efficient use of LLMs
    """
    Args:
        tasks_list (_type_): _description_
        User Energy: prone to estimation error by the user and the llm
        Task Energy: prone to estimation error by the llm
    Purpose:
        Sort the task list according to how energetically proximal they are to the user energy as well as user priority
        Sorting Variables: User Energy and User Priority
        Sorting Information Input: Task Energetic Requirements and Task Priority (User Priority)
        Output: Energy-Priority Aligned task list to be saved in the db and displayed in the output.html
    Logic:
        1- Retain the User Energy
        2- Retain the task energetic requirements
        3- Retain User Priority
        4- Greedy Algorithm: start with tasks that are the most energetically proximal to user energy (safety choice heuristic) -> sort them by priority
    """
    if request.method == "POST":
        UE = session.get('energy_level')
        energy_dist = {"extremely high": 5, "high": 4, "moderate": 3, "low": 2, "extremely low": 1}
        UEmetric = energy_dist[UE]

        distancedict = {UE: 0}
        re_energy_dist = energy_dist.copy()
        re_energy_dist.pop(UE)
        for level in re_energy_dist:
            distancedict[level] = UEmetric - re_energy_dist[level]

        tasks_list_str = session.get('tasks_list')
        tasklist = tasks_list_str.split(',')
        #Task Requirement
        task_info_dict = agents.run_taskreq_query(tasks_list_str).strip()
        n = task_info_dict.index('[')
        m = task_info_dict.index(']')
        task_info_dict = task_info_dict[n:m+1]
        jsontaskdict = json.loads(task_info_dict)

        task_content = [task['content'] for task in jsontaskdict]
        task_list = task_content
        N = len(task_list)
        priority = [N-task_list.index(task) for task in task_list]
        PriorityValue = {task_list[k]: priority[k] for k in range(len(priority))}

        UpdatedTasks = []
        compatible_tasks = list(filter(lambda task: task['energy_required'] == UE, jsontaskdict))
        for task in compatible_tasks:
            UpdatedTasks.append(task)

        incompatible_tasks = list(filter(lambda task: task['energy_required'] != UE, jsontaskdict))
        ProximityValue = {task['content']: distancedict[task['energy_required']] for task in incompatible_tasks}
        Proximity_Priority_Value = {task['content']: PriorityValue[task['content']] + ProximityValue[task['content']] for task in incompatible_tasks}

        sortedppv = sorted(Proximity_Priority_Value, key=Proximity_Priority_Value.get, reverse=True)
        remains = []
        l = 0
        for task in incompatible_tasks:
            if Proximity_Priority_Value[task['content']] == sortedppv[l]:
                UpdatedTasks.append(task)
                l += 1
            else:
                remains.append(task)

        if len(remains) != 0:
            for j in range(len(remains)):
                UpdatedTasks.append(remains[j])

        for k in range(len(UpdatedTasks)):
            new_task = UpdatedToDo(
                content=UpdatedTasks[k]['content'],
                energy_required=UpdatedTasks[k]['energy_required'],
                preparation=UpdatedTasks[k]['preparation'],
                task_type=UpdatedTasks[k]['task_type'],
                recommended_start_time=UpdatedTasks[k]['recommended_start_time']
            )
            try:
                db.session.add(new_task)
                db.session.commit()
                print(f"Task added: {new_task}")
            except Exception as e:
                flash(f"llm output problem {e}", 'error')
                print(f"Error adding task: {e}")

    optimal_task_list = UpdatedToDo.query.order_by(UpdatedToDo.date).all()
    print("------------------")
    print("Optimal Task List:", optimal_task_list)
    print("------------------")
    session['optimal_task_list'] = ','.join([task.content for task in optimal_task_list])
    return render_template('output.html', optimal_task_list=optimal_task_list)


@app.route('/recommendation', methods=['POST','GET'])
def recommend():
    
    
    render_template('recommendation.html')
    


# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)



