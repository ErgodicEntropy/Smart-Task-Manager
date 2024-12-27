# import llm
from langchain.llms import Cohere
# from langchain_cohere import ChatCohere
import prompts
from langchain.chains import ConversationChain, LLMChain
from langchain.memory import ConversationBufferMemory
import os
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory


# Default configurations
MAX_TOKENS = 400
MODEL_NAME = "declare-lab/flan-alpaca-large" # "gpt-3.5-turbo"  # or "gpt-4", etc. "google/flan-t5-xxl"
TEMPERATURE = 0.2
HUGGINGFACE_API_TOKEN = ''
COHERE_API_TOKEN = 'IdU5efIJTsWndc1HkSqoqdCK45tViujej4p8NopX'

os.environ['COHERE_API_KEY'] = COHERE_API_TOKEN


llm = Cohere()

memory = ConversationBufferMemory(memory_key='history', return_messages=True)

# memory = InMemoryChatMessageHistory()




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

# Run LLM Query for Energy Agent
def run_energy_query(query: str): #query type: string (energy)
    Energy_Agent = LLMChain(llm=llm,prompt=EP, verbose=True)
    response = Energy_Agent.run({"energy_level": query})
    # Energy_Agent = EP | llm | StrOutputParser()
    # response = Energy_Agent.invoke({"energy_level":query})
    # Log the response into memory
    memory.chat_memory.add_user_message(f"Energy Level Query: {query}")
    memory.chat_memory.add_ai_message(response)
    return response

# Run LLM Query for Summarizing/Infering user energy level    
def retain_energy(message: str): #query type: string (user message)
    Retain_Agent = LLMChain(llm=llm, prompt= RP, verbose=True)
    response = Retain_Agent.run({"user_message": message})
    # Retain_Agent = RP | llm | StrOutputParser()
    # response = Retain_Agent.invoke({"input":message})
    memory.chat_memory.add_ai_message(response)
    return response

# Run LLM Query for Task Requirement Agent
def run_task_query(query: str): #query type: list of strings or stringified list of strings (tasks list)
    Task_Agent = LLMChain(llm=llm,prompt=TP, verbose=True)
    response = Task_Agent.run({"tasks_list": query})
    # Task_Agent = TP | llm | StrOutputParser()
    # response = Task_Agent.invoke({"tasks_list":query})
    # Log the response into memory
    memory.chat_memory.add_user_message(f"Task List Query: {query}")
    memory.chat_memory.add_ai_message(response)
    return response

# Run LLM Query for Task Requirement Agent
def run_taskreq_query(query: str): #query type: list of strings or stringified list of strings (tasks list)
    Task_Agent = LLMChain(llm=llm,prompt=TRP, verbose=True)
    response = Task_Agent.run({"tasks_list": query})
    # Task_Agent = TRP | llm | StrOutputParser()
    # response = Task_Agent.invoke({"tasks_list":query})
    # Log the response into memory
    memory.chat_memory.add_user_message(f"Task List Query: {query}")
    memory.chat_memory.add_ai_message(response)
    return response


# Run LLM Query for Energy Allocation Agent
def run_allocation_query(query: str): #query type: list of strings or stringified list of strings (tasks list)
    Allocation_Agent = LLMChain(llm=llm,prompt=AP, verbose=True)
    response = Allocation_Agent.run({"tasks_list": query})
    # Allocation_Agent = AP | llm | StrOutputParser()
    # response = Allocation_Agent.invoke({"tasks_list":query})
    # Log the response into memory
    memory.chat_memory.add_user_message(f"Task List Query: {query}")
    memory.chat_memory.add_ai_message(response)
    return response

# Run LLM Query for Output Agent (Optimal Task List)
def run_output_query(query: str): #query type: string + list of strings or stringified list of strings (tasks list + energy)
    Output_Agent = LLMChain(llm=llm,prompt=OP, verbose=True)
    response = Output_Agent.run({"context": query})
    # Output_Agent = OP | llm | StrOutputParser()
    # response = Output_Agent.invoke({"context":query})
    return response





