from langchain.llms import Cohere
import prompts
from langchain.chains import ConversationChain, LLMChain
from langchain.memory import ConversationBufferMemory
import os


# Default configurations
COHERE_API_TOKEN = ''

os.environ['COHERE_API_KEY'] = COHERE_API_TOKEN


llm = Cohere()

memory = ConversationBufferMemory(memory_key='history', return_messages=True)


# Import prompts from prompts.py
EP = prompts.Energy_Prompt_Template
TP = prompts.Task_Prompt_Template
AP = prompts.Allocation_Prompt_Template
OP = prompts.Output_Prompt_Template
RP = prompts.Retain_Prompt_Template
TRP = prompts.TaskRequer



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
    Task_Agent = LLMChain(llm=llm,prompt=TP, verbose=True)
    response = Task_Agent.run({"tasks_list": query})
    # Log the response into memory
    memory.chat_memory.add_user_message(f"Task List Query: {query}")
    memory.chat_memory.add_ai_message(response)
    return response

# Run LLM Query for Task Requirement Agent
def run_taskreq_query(query: str): #query type: list of strings or stringified list of strings (tasks list)
    Task_Agent = LLMChain(llm=llm,prompt=TRP, verbose=True)
    response = Task_Agent.run({"tasks_list": query})
    # Log the response into memory
    memory.chat_memory.add_user_message(f"Task List Query: {query}")
    memory.chat_memory.add_ai_message(response)
    return response


# Run LLM Query for Energy Allocation Agent
def run_allocation_query(query: str): #query type: list of strings or stringified list of strings (tasks list)
    Allocation_Agent = LLMChain(llm=llm,prompt=AP, verbose=True)
    response = Allocation_Agent.run({"tasks_list": query})
    # Log the response into memory
    memory.chat_memory.add_user_message(f"Task List Query: {query}")
    memory.chat_memory.add_ai_message(response)
    return response

# Run LLM Query for Output Agent (Optimal Task List)
def run_output_query(query: str): #query type: string + list of strings or stringified list of strings (tasks list + energy)
    Output_Agent = LLMChain(llm=llm,prompt=OP, verbose=True)
    response = Output_Agent.run({"context": query})
    return response





