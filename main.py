import numpy as np
import os
import secrets
import agents
from query import Query
import json
from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


def extract_json(data_str:str): #stripped LLM Response
    try:
        n = data_str.index('[')
        m = data_str.index(']')
        return json.loads(data_str[n:m+1].strip())
    except (ValueError, json.JSONDecodeError) as e:
        print(f"Error extracting JSON: {e}")
        return {}

def extract_JSON(data_str:str): #stripped LLM Response
    if data_str.startswith("```json"):
        data_str = data_str[7:]
    if data_str.endswith("```"):
        data_str = data_str[:-3]
    if data_str.startswith("```"):
        data_str = data_str[3:]

    data_str = data_str.strip()
    try:
        return json.loads(data_str)
    except (ValueError, json.JSONDecodeError) as e:
        print(f"Error extracting JSON: {e}")
        return {}

    
    
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
    if peak_daytime in daydict and current_daytime in daydict:
        daydist = {}    
        for dt in daydict:
            daydist[dt] = 6 - abs(daydict[peak_daytime] - daydict[dt])
            
        return daydist[current_daytime]
    else:
        return 0
        
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
    rank = db.Column(db.Integer, nullable=True)    
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


@app.route('/finalize_tasks', methods=['POST'])
def finalize_tasks():
    return redirect('/data')

# # User Data
# @app.route('/datatest', methods=['POST', 'GET'])
# def submit_form():
#     if request.method == "POST":
#         # energy_dist = {"extremely high": 90, "high": 70, "moderate": 50, "low": 30, "extremely low": 10}
#         # # form_data = request.form.to_dict()
#         # # data_list = [float(form_data['clarity'])]
#         # data_list = [request.form['clarity']]
#         energy_level = request.form['clarity']                    
#         new_energy = Energy(level=energy_level)
#         try:
#             db.session.add(new_energy)
#             db.session.commit()
#             session['energy_level'] = energy_level
#             flash(f'Energy level set to {energy_level}', 'success')
#         except:
#             flash('There was an issue saving the energy level', 'error')
#             return redirect('/datatest')

#     return render_template('datatest.html')


# User Data
@app.route('/data', methods=['POST', 'GET'])
def submit_form():
    if request.method == "POST":
        threshold ={
            'extremely low': 0,
            'low': 1.1879440506810733,
            'moderate': 2.7561698026964763,
            'high': 5.017618750479866,
            'extremely high': 6.343199292229015
        }
        currenthour = datetime.today().hour
        day_category = daycategory(currenthour)
        data_list = [
            float(request.form['clarity']),
            float(request.form['focus']),
            float(request.form['fatigue']),
            float(request.form['readiness']),
            float(request.form['load']),
            float(request.form['motivation']),
            float(request.form['stress']),
            float(request.form['physical_fatigue']),
            daymetric(request.form['circadian_rhythm'], day_category),
            float(request.form['trend']),
            float(request.form['external_stimulation']),
            float(request.form['interaction_energy']),
            float(request.form['task_initiation'])
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
        if average_energy >= threshold["extremely high"]:
            energy_level = "extremely high"
        elif average_energy >= threshold["high"]:
            energy_level = "high"
        elif average_energy >= threshold["moderate"]:
            energy_level = "moderate"
        elif average_energy >= threshold["low"]:
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
        energy_dist = { 
            'extremely low': 1,
            'low': 2,
            'moderate': 3,
            'high': 4,
            'extremely high': 5
        }
        threshold_dist ={
            'extremely low': 0,
            'low': 0.1879440506810733,
            'moderate': 0.22373788162148546,
            'high': 0.4232223375873885,
            'extremely high': 0.643199292229015
        }

        UEmetric = energy_dist[UE]

        distancedict = {UE: 0}
        re_energy_dist = energy_dist.copy()
        re_energy_dist.pop(UE)
        for level in re_energy_dist:
            distancedict[level] = UEmetric - re_energy_dist[level]

        tasks_list_str = session.get('tasks_list')
        # For divide-and-conquer prompting (LLM Error Correction with Input Size Minimization) -> Almost-Accuracy-free Format Problem: For this to work, the json response should be more creative than categorical energy e.g. low, moderate..etc
        # tasklist = tasks_list_str.split(',')
        # taskenergyjson = []
        # for task in tasklist:                
        #     single_task_energy_dict = agents.run_single_task_query(task).strip()
        #     n = single_task_energy_dict.index('[')
        #     m = single_task_energy_dict.index(']')
        #     single_task_energy_dict = single_task_energy_dict[n:m+1]
        #     singletaskenergyjson = json.loads(single_task_energy_dict)
        #     taskenergyjson.append(singletaskenergyjson)
        # taskenergyjson = taskenergyjson.to_dict() #convert the list to a json dict

        #Requirement Orthogonalization function
        task_energy_dict = agents.run_task_query(tasks_list_str).strip()
        # n = task_energy_dict.index('[')
        # m = task_energy_dict.index(']')
        # task_energy_dict = task_energy_dict[n:m+1]
        # taskenergyjson = json.loads(task_energy_dict)
        taskenergyjson = extract_json(task_energy_dict)

        #Requirement Scoring Function
        energytest = []
        tasksdata = [] #list of content-energy dictionaries
        weights = np.random.pareto(2.0,5)
        weights /= weights.sum()
        for task in taskenergyjson:
            energyvals = [task["cognitive_load"], task["physical_exertion"], task["task_duration"], task["task_precision"], task["collaboration_intensity"]]
            K = len(energyvals) # K = L - 1 (L is the task metamodel complexity) 5
            weighted_sum = 0 
            for k in range(K):
                weighted_sum += weights[k]*energy_dist[energyvals[k]]
            energy_value = weighted_sum/K
            energytest.append(energy_value)
            #Requirement Threshold Function
            if energy_value >= threshold_dist["extremely high"]:
                EL = "extremely high"
            elif energy_value >= threshold_dist["high"]:
                EL = "high"
            elif energy_value >= threshold_dist["moderate"]:
                EL = "moderate"
            elif energy_value >= threshold_dist["low"]:
                EL = "low"
            else:
                EL = "extremely low"
            
            tasksdata.append({'content':task["content"], 'energy_required':EL})

        task_list = [task['content'] for task in tasksdata] #task_content (task:dict)
        N = len(task_list)
        priority = [N-task_list.index(task) for task in task_list] # task:str
        PriorityValue = {task_list[k]: priority[k] for k in range(len(priority))}

        UpdatedTasks = []
        compatible_tasks = list(filter(lambda task: task['energy_required'] == UE, tasksdata))
        for task in compatible_tasks:
            UpdatedTasks.append(task)

        incompatible_tasks = list(filter(lambda task: task['energy_required'] != UE, tasksdata))
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
                rank = k+1,
                date = datetime.now()) #date and index correlate -> make sure that the date is very specific to allow for ordering
            try:
                db.session.add(new_task)
                db.session.commit()
                print(f"Task added: {new_task}")
            except Exception as e:
                flash(f"llm output problem {e}", 'error')
                print(f"Error adding task: {e}")

    optimal_task_list = UpdatedToDo.query.order_by(UpdatedToDo.date).all() #early comes first
    return render_template('output.html', optimal_task_list=optimal_task_list)

#Route for Energy Allocation Recommendation
@app.route('/recommendation/<int:id>', methods=['POST','GET'])
def recommend(id):
    task = UpdatedToDo.query.get_or_404(id)
    resp = agents.run_allocation_query(task.content) 
    if request.method == "POST":
        message = request.form['userMessage']
        resp = agents.run_allocation_query(message)         # conversationchain is needed
    return render_template('recommendation.html', task=task, resp=resp)


#Route for Rank Explanation
@app.route('/explanation/<int:id>', methods=['POST','GET'])
def explain(id):
    task = UpdatedToDo.query.get_or_404(id)
    taskname  = task.content
    taskrank = str(task.rank)
    taskenergyreq = task.energy_required
    userenergy = session.get('energy_level')
    resp = agents.run_explanation_query(taskname,taskrank,taskenergyreq,userenergy) 
    if request.method == "POST":
        message = request.form['userMessage']
        resp = agents.continue_conversation(message)         # conversationchain is needed
    return render_template('explanation.html', task=task, resp=resp)


# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)



