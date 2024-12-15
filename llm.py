import config
from langchain.llms import HuggingFaceHub
from langchain_huggingface import HuggingFaceEndpoint
from langchain_community.llms import CTransformers


# Default configurations
model_name = config.MODEL_NAME 
maxtokens = config.MAX_TOKENS
temperature =config.TEMPERATURE


class QueryRunner:
    def __init__(self, maxtoken=maxtokens, modelname=model_name, temp=temperature):
        self.maxtoken = maxtoken
        self.modelname = modelname
        self.temp = temp

    def llm_def(self):
        # Initialize LLM from Hugging Face model hub
        llm = HuggingFaceHub(
            repo_id=self.modelname, 
            model_kwargs={'temperature': self.temp, 'max_length': self.maxtoken}
        )
        # repo_id="mistralai/Mistral-7B-Instruct-v0.2"
        # llm=HuggingFaceEndpoint(repo_id=repo_id,max_length=128,temperature=0.7,token=config.HUGGINGFACE_API_TOKEN)
        # llm.invoke("What is machine learning")
        return llm
    
    def llm_transformer_def():
        # Load the locally downloaded model here
        llm = CTransformers(
            model = "TheBloke/Llama-2-7B-Chat-GGML",
            model_type="llama",
            max_new_tokens = 512,
            temperature = 0.5
        )
        return llm