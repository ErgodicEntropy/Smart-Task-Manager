import llm
import prompts
from langchain.chains import ConversationChain, LLMChain
from langchain.memory import ConversationBufferMemory
import config

# Default configurations
model_name = config.MODEL_NAME 
maxtokens = config.MAX_TOKENS
temperature =config.TEMPERATURE



# Import prompts from prompts.py
EP = prompts.Energy_Prompt_Template
TP = prompts.Task_Prompt_Template
AP = prompts.Allocation_Prompt_Template
OP = prompts.Output_Prompt_Template


memory = ConversationBufferMemory(llm=llm,
    memory_key='chat_history', return_messages=True)


def continue_conversation(user_message: str):
    """
    Handles follow-up queries during an ongoing conversation.
    """
    llmscaffold = llm.QueryRunner(modelname=model_name, maxtoken=maxtokens, temp=temperature)
    llm_instance = llmscaffold.llm_def()
    Agent = ConversationChain(llm=llm_instance, memory=memory, verbose=True)

    # Run the conversation chain with user message as input
    response = Agent.run({"input": user_message})
    return response

# Run LLM Query for Energy Agent
def run_energy_query(query: str): #query type: string
    llmscaffold = llm.QueryRunner(modelname=model_name, maxtoken=maxtokens, temp=temperature)
    llm = llmscaffold.llm_def()
    Energy_Agent = LLMChain(llm=llm,prompt=EP, verbose=True)
    response = Energy_Agent.run({"energy_level": query})
    # Log the response into memory
    memory.chat_memory.add_user_message(f"Energy Level Query: {query}")
    memory.chat_memory.add_ai_message(response)
    return response
    
# Run LLM Query for Task Requirement Agent
def run_task_query(query: str): #query type: list of strings or stringified list of strings
    llmscaffold = llm.QueryRunner(modelname=model_name, maxtoken=maxtokens, temp=temperature)
    llm = llmscaffold.llm_def()
    Task_Agent = LLMChain(llm=llm,prompt=TP, verbose=True)
    response = Task_Agent.run({"tasks_list": query})
    # Log the response into memory
    memory.chat_memory.add_user_message(f"Task List Query: {query}")
    memory.chat_memory.add_ai_message(response)
    return response


# Run LLM Query for Energy Allocation Agent
def run_allocation_query(query: str): #query type: list of strings or stringified list of strings
    llmscaffold = llm.QueryRunner(modelname=model_name, maxtoken=maxtokens, temp=temperature)
    llm = llmscaffold.llm_def()
    Allocation_Agent = LLMChain(llm=llm,prompt=AP, verbose=True)
    response = Allocation_Agent.run({"tasks_list": query})
    # Log the response into memory
    memory.chat_memory.add_user_message(f"Task List Query: {query}")
    memory.chat_memory.add_ai_message(response)
    return response

# Run LLM Query for Output Agent (Optimal Task List)
def run_output_query(query: str): #query type: string + list of strings or stringified list of strings
    llmscaffold = llm.QueryRunner(modelname=model_name, maxtoken=maxtokens, temp=temperature)
    llm = llmscaffold.llm_def()
    Output_Agent = LLMChain(llm=llm,prompt=AP, verbose=True)
    response = Output_Agent.run({"context": query})
    return response





