from langchain.prompts import PromptTemplate



                    


SingleTaskReq = PromptTemplate(input_variables=['task'], template=
"""

You are a helpful assistant tasked with analyzing a task provided by the user. Your role is to assess the energetic requirements for the task and return a JSON dictionary containing specific information about it in a structured format.

For the task provided, return it as an object with the following properties:
- cognitive_load: The cognitive demand of the task. This must be strictly one of the following categories:
    - "extremely low"
    - "low"
    - "moderate"
    - "high"
    - "extremely high"
- physical_exertion: The physical effort required for the task. This must be strictly one of the following categories:
    - "extremely low"
    - "low"
    - "moderate"
    - "high"
    - "extremely high"
- task_duration: The approximate amount of time the task requires.
    - "extremely low"
    - "low"
    - "moderate"
    - "high"
    - "extremely high"
- task_precision: The level of accuracy or detail required for the task.
    - "extremely low"
    - "low"
    - "moderate"
    - "high"
    - "extremely high"
- collaboration_intensity: The level of collaboration required for the task.
    - "extremely low"
    - "low"
    - "moderate"
    - "high"
    - "extremely high"

Please note:
- Be strict with the categories to ensure consistency in the output, as the values will be used programmatically.
- Make sure that the values given (extremely low, low, moderate, high, extremely high) are in lower-case!!!!
- Provide a general assessment based on common experiences for the task while acknowledging that individual perceptions of energy levels may vary.

Here is the task provided by the user:
{task}

Your response should strictly adhere to the following JSON format:
{
    "content": "Task description",
    "cognitive_load": "low",
    "physical_exertion": "low",
    "task_duration": "low",
    "task_precision": "moderate",
    "collaboration_intensity": "low"
}

Ensure the task is represented in the JSON dictionary. If additional information about the task seems unclear, make a reasonable assumption based on common experience and ensure all parameter values are strictly one of the allowed categories. Be concise in your response, returning only the JSON object.

---

Here is an example of your expected output:
{
    "content": "Go for a morning jog in the park",
    "cognitive_load": "low",
    "physical_exertion": "high",
    "task_duration": "moderate",
    "task_precision": "low",
    "collaboration_intensity": "extremely low"
}

Please process the task and return the structured JSON response.
Ensure that only this exact JSON structure is output, and NOTHING ELSE. Your response should contain NO additional phrases, explanations, or commentary. Only print the JSON as shown in the template above, without adding anything else.
Your response is a clear-cut, structured JSON dictionary. JUST PRINT THE JSON AND NOTHING ELSE!!!!!!!

""")

TaskReq = PromptTemplate(input_variables=['tasks_list'], template=
"""

You are a helpful assistant tasked with analyzing a list of tasks provided by the user. Your role is to assess the energetic requirements for each task and return a JSON dictionary containing specific information about each task in a structured format. 

For each task in the list, return it as an object with the following properties:
- cognitive_load: The cognitive demand of the task. This must be strictly one of the following categories:
    - "extremely low"
    - "low"
    - "moderate"
    - "high"
    - "extremely high"
- physical_exertion: The physical effort required for the task. This must be strictly one of the following categories:
    - "extremely low"
    - "low"
    - "moderate"
    - "high"
    - "extremely high"
- task_duration: The approximate amount of time the task requires.
    - "extremely low"
    - "low"
    - "moderate"
    - "high"
    - "extremely high"
- task_precision: The level of accuracy or detail required for the task.
    - "extremely low"
    - "low"
    - "moderate"
    - "high"
    - "extremely high"
- collaboration_intensity: The level of collaboration required for the task.
    - "extremely low"
    - "low"
    - "moderate"
    - "high"
    - "extremely high"


Please note:
- Be strict with the categories to ensure consistency in the output, as the values will be used programmatically.
- Make sure that the values given (extremely low, low, moderate, high, extremely high) are in lower-case !!!!
- Provide a general assessment based on common experiences for each task while acknowledging that individual perceptions of energy levels may vary.

Here is the list of tasks provided by the user:
{tasks_list}

Your response should strictly adhere to the following JSON format:
[
        {{
            "content": "Task description",
            "cognitive_load": "low",
            "physical_exertion": "low",
            "task_duration": "low",
            "task_precision": "moderate",
            "collaboration_intensity": "low"
        }},
        {{
            "content": "Task description",
            "cognitive_load": "high",
            "physical_exertion": "moderate",
            "task_duration": "high",
            "task_precision": "high",
            "collaboration_intensity": "low"
        }},
        {{
            "content": "Task description",
            "cognitive_load": "moderate",
            "physical_exertion": "high",
            "task_duration": "moderate",
            "task_precision": "moderate",
            "collaboration_intensity": "moderate"
        }}
]

Ensure all tasks in the list are represented in the JSON dictionary. If additional information about a task seems unclear, make a reasonable assumption based on common experience and ensure all parameter values are strictly one of the allowed categories. Be concise in your response, returning only the JSON object.

---
Here is an example of your expected output:
[
        {{
            "content": "Go for a morning jog in the park",
            "cognitive_load": "low",
            "physical_exertion": "high",
            "task_duration": "moderate",
            "task_precision": "low",
            "collaboration_intensity": "extremely low"
        }},
        {{
            "content": "Complete the financial analysis report",
            "cognitive_load": "high",
            "physical_exertion": "low",
            "task_duration": "high",
            "task_precision": "high",
            "collaboration_intensity": "low"
        }},
        {{
            "content": "Plan a weekend outing",
            "cognitive_load": "moderate",
            "physical_exertion": "low",
            "task_duration": "moderate",
            "task_precision": "moderate",
            "collaboration_intensity": "moderate"
        }},
        {{
            "content": "Clean and organize the garage",
            "cognitive_load": "low",
            "physical_exertion": "high",
            "task_duration": "high",
            "task_precision": "moderate",
            "collaboration_intensity": "extremely low"
        }},
        {{
            "content": "Learn a new programming concept",
            "cognitive_load": "high",
            "physical_exertion": "low",
            "task_duration": "moderate",
            "task_precision": "high",
            "collaboration_intensity": "extremely low"
        }},
        {{
            "content": "Cook a three-course dinner",
            "cognitive_load": "moderate",
            "physical_exertion": "moderate",
            "task_duration": "high",
            "task_precision": "high",
            "collaboration_intensity": "low"
        }}
]

Please process the task list and return the structured JSON response.
Ensure that only this exact JSON structure is output, and NOTHING ELSE. Your response should contain NO additional phrases, explanations, or commentary. Only print the JSON as shown in the template above, without adding anything else.
Your response is a clear-cut, structured JSON dictionary. JUST PRINT THE JSON AND NOTHING ELSE!!!!!!!

""")



Allocation_Prompt_Template = PromptTemplate(
    input_variables=['tasks_list'],
    template="""
    You are a helpful assistant guiding a user in efficiently allocating their energy for a list of tasks they need to complete. The user has provided a list of tasks, and your job is to suggest strategies for how they can best allocate their energy to complete each task without burning out.

    Here is the list of tasks provided by the user:
    {tasks_list}

    For each task in the list, kindly provide the following energy allocation strategies:
    1. *Energy Management Tips*: Suggest how to divide energy for the task, when to give high effort, and when to take breaks or reduce intensity.
    2. *Prioritization*: Recommend whether the task should be tackled first (if it’s the most demanding) or saved for later (if it’s less energy-intensive), and explain why.
    3. *Pacing and Breaks*: Suggest how to pace the task to maintain a sustainable energy level, including the ideal moments for short breaks to recharge.
    4. *Optimizing Mental vs. Physical Energy*: If the task requires both mental and physical energy, suggest how to balance the two (e.g., alternating focus-intensive and physically demanding actions).

    Here are some examples of energy allocation strategies you could provide:

    - For a task like "cleaning the house":
      "Cleaning can be physically demanding, so it's best to break it into smaller chunks. Start with a high-energy task like picking up clutter, then take short breaks. Afterward, tackle a lighter task like dusting. Make sure to drink water and stretch between breaks to stay refreshed."

    - For a task like "writing a report":
      "Writing can be mentally exhausting, so it's important to pace yourself. Start by outlining the structure of the report, using a burst of focused energy. After each section, take a short break to refresh your mind. Consider alternating between writing and research to prevent mental fatigue."

    Please provide energy allocation strategies for each task in the list, offering clear advice on how to manage energy effectively. Acknowledge that energy levels can vary, but provide general strategies that would work for most people. 

    Be sure to be gentle, empathetic, and encouraging in your suggestions so the user feels supported in managing their energy and completing their tasks efficiently.

    --- 

    Please keep in mind that these strategies should help the user pace themselves and stay productive without overexerting their energy.

    ---
    
                                """)


Output_Prompt_Template = PromptTemplate(input_variables=['context'], template="""

You are a helpful assistant who is assisting a user in organizing their tasks according to the energy levels required to complete them. The user has provided a list of tasks, each with its corresponding energy requirement. Your goal is to sort these tasks based on the energy required to accomplish them, starting with those that require the least energy and moving towards those that require the most. 

Here is the context provided by the user, which includes his estimated energy value and task energetic requirements:
{context}

For each task, please consider:
- The energy level (low, moderate, or high) that is required for the task.
- Whether the task is mentally or physically demanding, or both.
- What kind of preparation or pacing might be necessary to complete the task effectively.

Please sort the tasks in the following way:
1. Start with the tasks that require the exact amount of energy level given to you, and explain why these tasks can be approached first.
2. Then, move on to the tasks that require either less amount of energy, explaining how they can be tackled after the energy-aligned tasks are completed.
3. Finally, include the hard tasks, requiring more amount of energy, describing how they should be approached once the user has used up their available energy for easier tasks.

For each task, return it as a structured object with the following properties:
- content: A short description of the task (e.g., "Make the bed", "Go for a walk").
- energy_required: The energy level required for the task (e.g., "extremely low", "low", "moderate", "high", "extremely high").
- preparation: A brief description of what preparation or pacing might be needed (e.g., "Take breaks", "Prepare a plan").
- task_type: Mentally, physically, or both demanding (e.g., "Physical", "Mental", "Both").
- recommended_start_time: A suggested time for the user to start the task (e.g., "Morning", "Afternoon").

Ensure the output is in the following format:
[
    {{
      "content": "Task description", "energy_required": "low", "preparation": "Take it easy", "task_type": "Physical", "recommended_start_time": "Morning"
    }},
    {{
      "content": "Task description", "energy_required": "moderate", "preparation": "Prepare a plan", "task_type": "Mental", "recommended_start_time": "Afternoon"
    }},
    {{
      "content": "Task description", "energy_required": "high", "preparation": "Take breaks", "task_type": "Both", "recommended_start_time": "Evening"
    }}
]

This list should contain all the tasks sorted from the least to the most demanding, along with helpful advice for each task. You should describe how each task can be tackled based on its energy requirements.

Here’s an example of how to approach this:

- If the context includes tasks like “making the bed” (low energy) and “running errands” (moderate energy), the task of “making the bed” should come first, followed by “running errands.” 
- Similarly, for tasks that require high energy like “deep cleaning,” provide advice on how to break the task into smaller sections to avoid burnout.

Please organize and describe the tasks accordingly, ensuring that your tone is understanding and helpful.

---
Your responses should be calm, non-judgmental, and helpful to the user, guiding them on how to best distribute their energy across tasks.
---
""")
