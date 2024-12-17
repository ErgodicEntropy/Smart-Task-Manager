import numpy as np
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
        session['userEnergyMessage'] = usermessage
        conversational_resp = agents.continue_conversation(usermessage)
        
    accurate_enegy_level = agents.retain_energy(usermessage)
    session['updated_energy_level'] = accurate_enegy_level
    
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
        session['userTaskMessage'] = usermessage
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
        session['userAllocationMessage'] = usermessage
        conversational_resp = agents.continue_conversation(usermessage)

    return render_template('allocation_conversation.html', allocation_resp=allocation_resp, conversational_resp=conversational_resp)


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
    #Energy Metric system
    if request.method == "POST":
        #Get User Energy
        UE = session.get('updated_energy_level')

        energy_dist = {"extremely high":5, "high":4, "moderate":3, "low":2, "extremely low":1}
        UEmetric = energy_dist[UE] #1 to 5


        distancedict = {}
        distancedict[UE] = 0
        re_energy_dist = energy_dist.copy()
        re_energy_dist.pop(UE)
        for level in re_energy_dist:
            distancedict[level] = UEmetric - re_energy_dist[level] #negative for higher values than UE, positive for lower values than UE
            re_energy_dist.pop(level)
            
            
        
        #Get Task Energy
        tasks_list_str = session.get('tasks_list', "No tasks provided.") # string containing a list of strings
        task_info_dict = agents.run_taskreq_query(tasks_list_str) #string python/json dict
        jsontaskdict = json.load(task_info_dict) # for a list: tasks_info_dict.split(',')        

        ## Retrieve Tasks info from the LLM output
        task_content = [ task['content'] for task in jsontaskdict]
        # energy_req = [ task['energy_required'] for task in jsontaskdict]
        # preparation = [ task['preparation'] for task in jsontaskdict]
        # task_type = [ task['task_type'] for task in jsontaskdict]
        # rst = [ task['recommended_start_time'] for task in jsontaskdict]

        #Get User Priority
        # task_list = tasks_list_str.split(',') #convert the string into a list of strings containing task content (Todo attribute)
        task_list = task_content
        N = len(task_list)
        priority = [N-task_list.index(task) for task in task_list] #priority value is as unique as the task id/index
        PriorityValue = {} #content-priority pair
        for k in range(len(priority)): 
            PriorityValue[task_list[k]] = priority[k] 
        #Greedy Algorithm
        UpdatedTasks = [] #composing both (prioritized) compatible tasks and incompatible tasks -> for compatible tasks, they are sorted by priority (energy fixed to user energy), for incompatible tasks, they are sorted by both priority and energy required (user energy proximity)
        ## For compatible tasks:
        compatible_tasks = list(filter(lambda task: task['energy_required']==UE,jsontaskdict)) #start with the safety choice heuristic
        ### sorted by priority: already sorted 
        # compatiblepriority = []
        # for task in compatible_tasks:
        #     X = taskvalue[task['content']]
        #     compatiblepriority.append(X) #list sorted by design because jsontaskdict is sorted according to user priority input
        
        # sortedcp = sorted(compatiblepriority, reverse=True)
        
        # t = 0
        # for task in compatible_tasks:
        #     if taskvalue[task['content']] == sortedcp[t]:
        #         UpdatedTasks.append(task)
        #         t += 1
        #     else:
        #         pass            

        for task in compatible_tasks:
            UpdatedTasks.append(task)
                    
        ## For incompatible tasks:
        incompatible_tasks = list(filter(lambda task: task['energy_required']!=UE,jsontaskdict)) #start with the safety choice heuristic
        
        ##Sorting: we accumulate both priority and proximity as one value to sort the incompatible tasks
        
        ### sorted by user energy proximity
        ProximityValue = {} #EL is already sorted by priority as given by its index -> resolve value (user energy proximity) index (priority) conflict
        for task in incompatible_tasks:
            X =  distancedict[task['content']] 
            ProximityValue[task['content']] = X
                    
        Proximity_Priority_Value = {}
        for task in incompatible_tasks:
            PPV = PriorityValue[task['content']] + ProximityValue[task['content']]
            Proximity_Priority_Value[task['content']] = PPV
        
        sortedppv = sorted(Proximity_Priority_Value, reverse=True)
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
        

        ### sorted by priority: already sorted
        # incompatiblepriority = []
        # for task in incompatible_tasks:
        #     X = taskvalue[task['content']]
        #     incompatiblepriority.append(X) #list sorted by design because jsontaskdict is sorted according to user priority input
        
        # sortedicp = sorted(incompatiblepriority, reverse=True)
        
        # j = 0
        # for task in incompatible_tasks:
        #     if taskvalue[task['content']] == sortedcp[j]:
        #         UpdatedTasks.append(task)
        #         j += 1
        #     else:
        #         pass
        
    
    
        #save in the db model
        for k in range(len(UpdatedTasks)): #k index correlates with datetime.now()
            new_task = UpdatedToDo(content = UpdatedTasks[k]['content'], energy_required = UpdatedTasks[k]['energy_required'], preparation = UpdatedTasks[k]['preparation'], task_type = UpdatedTasks[k]['task_type'], recommended_start_time =UpdatedTasks[k]['recommended_start_time'], date=datetime.now() )
            try:
                db.session.add(new_task) #date sorted 
                db.session.commit()
            except:
                flash("llm output problem", 'error')
    else:    
        optimal_task_list = UpdatedToDo.query.order_by(UpdatedToDo.date).all()
        return render_template(' output.html',optimal_task_list=optimal_task_list)

# @app.route('/output', methods=['GET'])
# def task_output():
#     # Fetch data from session
#     energy_level = session.get('updated_energy_level', "No energy level provided.") #string
#     tasks_list_str = session.get('tasks_list', "No tasks provided.") # string containing a list of strings
    
#     # Initialize the Query instance
#     query_instance = Query(name="Task-Energy Output Management")

#     # Concatenate inputs into a single context string
#     context = query_instance.concatenate_inputs(energy_level, tasks_list_str)

#     # Pass context to the query runner or agent
#     info_task_list_str = agents.run_output_query(context)
#     ### CONVERSION: String to a python dict or list
#     info_task_list = query_instance.json_decode(info_task_list_str)        
#     # optimal_task_list = optimal_task_list_str.split(', ')  # Adjust based on the response format (e.g., comma-separated list)
#     # optimal_task_list = json.loads(optimal_task_list_str)
#     # optimal_task_list = query_instance.transform_response_to_json(optimal_task_list_str)
#     tasks = Todo.query.order_by(Todo.date).all() # this is a Todo object (db.Model) (tasks[0] is the earliest and the most prioritized)
#     tasks_list = [task.id for task in tasks] #this is a list of strings (tasks[0] is the earliest and the most prioritized)
        
#     optimal_task_list = 0
    
#     ### Stringify the optimal task list/dict back into a string
#     session['optimal_task_list'] = ', '.join(optimal_task_list) 
#     # Assuming optimal_task_list is a string, you can split it into a list
#     optimal_task_list = query_instance.json_decode(optimal_task_list_str)        
#     return render_template('output.html', optimal_task_list=optimal_task_list)

# Main route for file saving: JSON or string
@app.route('/downloadtext', methods=['GET'])
def download():
    query_instance = Query(name="data download")
    opt = session.get('optimal_task_list')
    optdict = json.loads(opt.strip()) #this is a python dictionary
    query_instance.save_text_file(optdict,"task.txt")
    
    
@app.route('/downloadjson', methods=['GET'])
def download():
    query_instance = Query(name="data download")
    opt = session.get('optimal_task_list')
    optdict = json.loads(opt.strip()) #this is a python dictionary
    query_instance.save_json_file(optdict,"task.json")
    


# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)



