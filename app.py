from flask import flash, session
import tempfile
import os
import json
import datetime  # For timestamping saved files
import llm
import prompts
from langchain.chains import LLMChain
import config

# Default configurations
model_name = config.MODEL_NAME 
maxtokens = config.MAX_TOKENS
temperature =config.TEMPERATURE



# Import prompts from prompts.py
EP = prompts.Energy_Agent
TP = prompts.Task_Agent
AP = prompts.Energy_Allocation_Agent



# Save JSON File Locally
def save_json_file(data, filename_prefix):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.json"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return filename
    except Exception:
        flash("Failed to save your data.", 'error')
        return None



# Run LLM Query for Energy Agent
def run_energy_query(query):
    llmscaffold = llm.QueryRunner(modelname=model_name, maxtoken=maxtokens, temp=temperature)
    llm = llmscaffold.llm_def()
    Energy_Agent = LLMChain(llm=llm,prompt=EP, verbose=True)
    response = Energy_Agent.run({"energy_level": query})['text']
    result_str = response.get('result', '').strip()   
    if result_str:
        # Remove code block markers if present
        if result_str.startswith("```json") and result_str.endswith("```"):
            result_str = result_str[7:-3].strip()
        elif result_str.startswith("```") and result_str.endswith("```"):
            result_str = result_str[3:-3].strip()

        # Try parsing the JSON
        try:
            json_response = json.loads(result_str)
            session['energy_json'] = json_response
            return True
        except json.JSONDecodeError:
            flash("An error occurred while processing your questions. Please try again.", 'error')
            return False
    else:
        flash("No response from the language model.", 'error')
        return False
    
    
# Run LLM Query for Task Requirement Agent
def run_task_query(query):
    llmscaffold = llm.QueryRunner(modelname=model_name, maxtoken=maxtokens, temp=temperature)
    llm = llmscaffold.llm_def()
    # save task list in session
    flaskedtasklist = session.get('tasks_list')
    task_list = ', '.join(flaskedtasklist)   
    # Convert restructured_data to JSON string
    input_json = json.dumps(task_list, ensure_ascii=False, indent=4)

    # Prepare the prompt with the input JSON
    TPJ = TP.replace("{input_json}", input_json)
    Task_Agent = LLMChain(llm=llm,prompt=TPJ, verbose=True)
    response = Task_Agent.run({"tasks_list": query})['text']
    # Write the input JSON to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8', suffix=".json") as tmp_file:
        tmp_file.write(input_json)
        temp_file_path = tmp_file.name
    try:
        result_str = response.get('result', '').strip()
        if result_str:
            # Remove code block markers if present
            if result_str.startswith("```json") and result_str.endswith("```"):
                result_str = result_str[7:-3].strip()
            elif result_str.startswith("```") and result_str.endswith("```"):
                result_str = result_str[3:-3].strip()

            # Try parsing the JSON
            try:
                task_requirements = json.loads(result_str)
                session['task_requirements'] = task_requirements  # Store in session state
                return True
            except json.JSONDecodeError:
                flash("An error occurred while evaluating your performance.", 'error')
                return False
        else:
            flash("No response from the language model.", 'error')
            return False

    except Exception:
        flash("An unexpected error occurred during evaluation.", 'error')
        return False

    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

# Run LLM Query for Energy Allocation Agent
def run_allocation_query(query):
    llmscaffold = llm.QueryRunner(modelname=model_name, maxtoken=maxtokens, temp=temperature)
    llm = llmscaffold.llm_def()

    # Retrieve the Task List from session state
    flaskedtl = session.get('tasks_list')
    task_list = ', '.join(flaskedtl)

    if not task_list:
        flash("task list is missing.", 'error')
        return False

    # Convert the taxonomy_evaluation to a JSON string
    input_json_str = json.dumps(task_list, ensure_ascii=False, indent=4)

    # Prepare the prompt with the input JSON
    APJ = AP.replace("{input_json}", input_json_str)
    Allocation_Agent = LLMChain(llm=llm,prompt=APJ, verbose=True)
    response = Allocation_Agent.run({"tasks_list": query})['text']

    # Write the prompt to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8', suffix=".txt") as tmp_file:
        tmp_file.write(APJ)
        temp_file_path = tmp_file.name

    try:
        # Initialize QueryRunner with document_path and model_name
        result_str = response.get('result', '').strip()
        if result_str:
            # Store the recommendations
            session['allocation_strategies'] = result_str
            return True
        else:
            flash("No response from the language model.", 'error')
            return False

    except Exception:
        flash("An unexpected error occurred while generating recommendations.", 'error')
        return False

    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)





