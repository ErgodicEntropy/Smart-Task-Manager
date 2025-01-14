from langchain.llms import Cohere
import prompts
from langchain.chains import ConversationChain, LLMChain
from langchain.memory import ConversationBufferMemory
import os

# Safely retrieve the Cohere API key from environment variables
COHERE_API_TOKEN = os.environ.get('COHERE_API_KEY')

if not COHERE_API_TOKEN:
    raise ValueError("Cohere API key is missing. Set the 'COHERE_API_KEY' environment variable.")

# Initialize the Cohere LLM with the API token
llm = Cohere(cohere_api_key=COHERE_API_TOKEN)

memory = ConversationBufferMemory(memory_key='history', return_messages=True)


# Import prompts from prompts.py
TR = prompts.TaskReq
STR = prompts.SingleTaskReq
AS = prompts.AllocationStrategies
TRE = prompts.TaskRankExplanation

def continue_conversation(user_message: str): #query type: string (user message)
    """
    Handles follow-up queries during an ongoing conversation.
    """
    Agent = ConversationChain(llm=llm, memory=memory, verbose=True)

    # Run the conversation chain with user message as input
    response = Agent.run({"input": user_message, "history": memory.memory_key})
    return response


# Run LLM Query for Task Requirement Agent
def run_task_query(query: str): #query type: list of strings or stringified list of strings (tasks list)
    Task_Agent = LLMChain(llm=llm,prompt=TR, verbose=True)
    response = Task_Agent.run({"tasks_list": query})
    # Log the response into memory
    memory.chat_memory.add_user_message(f"Task List Query: {query}")
    memory.chat_memory.add_ai_message(response)
    return response

# Run LLM Query for Task Requirement Agent
def run_single_task_query(query: str): #query type: list of strings or stringified list of strings (tasks list)
    Task_Agent = LLMChain(llm=llm,prompt=STR, verbose=True)
    response = Task_Agent.run({"task": query})
    # Log the response into memory
    memory.chat_memory.add_user_message(f"Task Query: {query}")
    memory.chat_memory.add_ai_message(response)
    return response


# Run LLM Query for Energy Allocation Agent
def run_allocation_query(query: str): #query type: list of strings or stringified list of strings (tasks list)
    Allocation_Agent = LLMChain(llm=llm,prompt=AS, verbose=True)
    response = Allocation_Agent.run({"task": query})
    # Log the response into memory
    memory.chat_memory.add_user_message(f"Task List Query: {query}")
    memory.chat_memory.add_ai_message(response)
    return response

# Run LLM Query for Rank Explanation Agent
def run_explanation_query(task: str, rank: str, energy_required:str, user_energy:str): #query type: list of strings or stringified list of strings (tasks list)
    Allocation_Agent = LLMChain(llm=llm,prompt=TRE, verbose=True)
    inputs = {
    "task": task,
    "rank": rank,
    "energy_required": energy_required,
    "user_energy": user_energy     
    }   
    response = Allocation_Agent.run(inputs)
    # Log the response into memory
    memory.chat_memory.add_user_message(f"Inputs Query: {inputs}")
    memory.chat_memory.add_ai_message(response)
    return response





