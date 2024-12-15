from langchain.prompts import PromptTemplate
from pydantic import BaseModel
import datetime  # For timestamping saved files
import json
import os
import tempfile


class Query(BaseModel):
    name: str  # Descriptive name of the query object

    # Save data as a JSON file locally
    def save_json_file(self, data: dict, filename_prefix: str) -> str:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return filename
        except Exception as e:
            raise RuntimeError(f"Failed to save your data: {e}")

    # Save data as a plain text file
    def save_text_file(self, data: str, filename_prefix: str) -> str:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.txt"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(data)
            return filename
        except Exception as e:
            raise RuntimeError(f"Failed to save your text data: {e}")

    # Decode JSON from a result string into a python dictionary
    @staticmethod
    def json_decode(result_str: str) -> dict:
        if not result_str:
            raise ValueError("No response from the language model.")
        
        # Remove code block markers if present
        if result_str.startswith("```json") and result_str.endswith("```"):
            result_str = result_str[7:-3].strip()
        elif result_str.startswith("```") and result_str.endswith("```"):
            result_str = result_str[3:-3].strip()
        
        # Attempt JSON decoding
        try:
            return json.loads(result_str.strip()) #this is a python dictionary
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to decode JSON: {e}")

    # Save query, result, and prompt as JSON and text files
    def save_query_and_result(self, query: dict, prompt: str, result_str: str) -> dict:
        # Save input query and prompt
        input_json = json.dumps(query, ensure_ascii=False, indent=4) #Converts the query dictionary into JSON format
        jsonified_prompt = prompt.replace("{tasks_list}", input_json) #Embeds the jsonified query into the prompt.
        
        saved_files = {}
        try:
            # Save input query as JSON
            saved_files['query_file'] = self.save_json_file(query, "query_input")
            # Save reformulated prompt as text
            saved_files['prompt_file'] = self.save_text_file(jsonified_prompt, "query_prompt")

            # Decode and save the result as JSON if applicable
            if result_str:
                result_data = self.json_decode(result_str)
                saved_files['result_file'] = self.save_json_file(result_data, "query_result")
            else:
                raise ValueError("Empty result string provided.")
        except Exception as e:
            raise RuntimeError(f"An error occurred while saving files: {e}")
        return saved_files
    
    # Save Query and Result using a PromptTemplate
    def save_query_and_result(
        self, query: dict, prompt: PromptTemplate, result_str: str
    ) -> dict:
        """
        Save the query, prompt (as a PromptTemplate), and result string to files.

        Parameters:
        - query: The input dictionary to the prompt.
        - prompt: A LangChain PromptTemplate object.
        - result_str: The LLM's response string.

        Returns:
        A dictionary containing the file paths of the saved query, prompt, and result.
        """
        # Render the prompt template with the query data
        rendered_prompt = prompt.format(**query)

        # Save the query as a JSON file
        query_file = self.save_json_file(query, "query_input")

        # Save the rendered prompt as a text file
        prompt_file = self.save_text_file(rendered_prompt, "query_prompt")

        # Decode and save the result as a JSON file (if valid JSON)
        try:
            result_data = self.json_decode(result_str)
            result_file = self.save_json_file(result_data, "query_result")
        except json.JSONDecodeError:
            # If not valid JSON, save as plain text
            result_file = self.save_text_file(result_str, "query_result")

        return {
            "query_file": query_file,
            "prompt_file": prompt_file,
            "result_file": result_file,
        }

    def concatenate_inputs(self, input_1: str, input_2: str | list[str], delimiter: str = "\n\n") -> str:
        """
        Concatenates two inputs into one string, handling lists gracefully.

        Args:
            input_1 (str): The first input string.
            input_2 (str | list[str]): The second input, which can be a string or a list of strings.
            delimiter (str): The delimiter to use between the two inputs. Defaults to two newlines.

        Returns:
            str: A single concatenated string.
        """
        if not isinstance(input_1, str):
            raise TypeError("input_1 must be a string.")

        if isinstance(input_2, list):
            # Convert the list to a single string
            input_2 = delimiter.join(input_2)
        elif not isinstance(input_2, str):
            raise TypeError("input_2 must be a string or a list of strings.")
        
        return f"{input_1.strip()}{delimiter}{input_2.strip()}"

    @staticmethod
    def transform_response_to_string(agent_response) -> str:
        """
        Purpose: Safely convert the agent's response into a string.
        Logic: 
            Converts the agent's response into a string.
            If the response is already a string, it returns it as-is.
            If not, it tries to cast the response to a string.
            If the input is a string, it trims and returns it.
            If it's a dictionary, it serializes it into a JSON string.  
            For other types (e.g., list, number), it converts them into a string using str().
        """
        if isinstance(agent_response, str):
            return agent_response.strip()
        elif isinstance(agent_response, dict):
            # Convert dictionary to a JSON-like string
            return json.dumps(agent_response, ensure_ascii=False, indent=4)
        else:
            # Fallback: Convert other types to string
            return str(agent_response).strip()

    @staticmethod
    def transform_response_to_json(agent_response) -> dict:
        """
        Purpose: Convert the agent's response into a JSON dictionary.   
        Logic:
            If the response is already a dictionary, it returns it directly.
            If it's a string, it tries to parse it as JSON.
            If parsing fails, it raises a ValueError.
            For unsupported types, it raises a TypeError.
            Converts the agent's response into a JSON object (dictionary).
            Assumes the response is either a JSON string or a dictionary."""
        
        if isinstance(agent_response, dict):
            # Already a dictionary, return as-is
            return agent_response
        elif isinstance(agent_response, str):
            # Try parsing the string as JSON
            try:
                return json.loads(agent_response.strip())
            except json.JSONDecodeError:
                raise ValueError("The response string is not valid JSON.")
        else:
            # If the response is not a string or dict, raise an error
            raise TypeError("Agent response must be a JSON string or dictionary.")
    
    # Save and clean up temporary files
    @staticmethod
    def save_temp_files(data_list: list, suffix=".json") -> list:
        temp_files = []
        try:
            for data in data_list:
                with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8', suffix=suffix) as tmp_file:
                    tmp_file.write(data)
                    temp_files.append(tmp_file.name)
            return temp_files
        except Exception as e:
            raise RuntimeError(f"Failed to save temporary files: {e}")
        finally:
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
