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
[
    {{
        "content": "Task description",
        "cognitive_load": "low",
        "physical_exertion": "low",
        "task_duration": "low",
        "task_precision": "moderate",
        "collaboration_intensity": "low"
    }}
]

Ensure the task is represented in the JSON dictionary. If additional information about the task seems unclear, make a reasonable assumption based on common experience and ensure all parameter values are strictly one of the allowed categories. Be concise in your response, returning only the JSON object.

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
    }}
]

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



AllocationStrategies = PromptTemplate(
    input_variables=['task'],
    template="""
    You are a helpful and empathetic assistant guiding a user in efficiently allocating their energy for a task they need to complete. Your goal is to provide actionable and personalized strategies that help the user manage their energy effectively, complete the task efficiently, and avoid burnout.

    Here is the task provided by the user:
    {task}

    For this task, kindly provide the following energy allocation strategies:
    1. **Task Segmentation Strategy**: Suggest how the user could break down the task into smaller, manageable segments or phases, and the ideal balance between segmented vs. continuous work based on the task's demands.
    2. **Energy Conservation Strategy**: Recommend how the user can conserve their energy for later stages of the task or for future tasks, especially when the task is prolonged or requires intense effort.
    3. **Break/Rest Strategy**: Provide guidance on how to structure breaks or rest periods during the task. Suggest the optimal timing and length of breaks to recharge without disrupting task flow.
    4. **Energy Recovery Strategy**: Explain how the user can plan for recovery during or after the task to prevent burnout, maintain energy levels, and ensure they are ready for subsequent tasks.
    5. **Task Switching Strategy**: Offer advice on when and how the user can switch between tasks to balance cognitive load, maintain energy, and avoid feeling overwhelmed.
    6. **Energy Effort Adjustment**: Advise on how the user should adjust their effort levels in response to the task's demands and their current energy levels, ensuring they avoid overexertion or under-engagement.

    Example Output:
    - For a task like *writing a report*:
      - **Task Segmentation Strategy**: Break the report into distinct sections (introduction, body, conclusion) and work on each one in separate focused sessions, with breaks in between.
      - **Energy Conservation Strategy**: Start with the most mentally demanding section of the report when energy is high, and save editing or proofreading for later when energy is lower.
      - **Break/Rest Strategy**: Work in 30-minute intervals with 5-minute breaks. After completing a major section, take a longer 15-minute break to recharge.
      - **Energy Recovery Strategy**: During breaks, engage in activities like stretching or deep breathing to relax both body and mind. After completing the task, take a longer rest to recover.
      - **Task Switching Strategy**: Avoid switching tasks too frequently to maintain deep focus on the report, but feel free to switch to a lighter task like checking emails during an energy dip.
      - **Energy Effort Adjustment**: Focus on high-effort tasks during your peak energy times (usually early in the day). As energy levels dip, shift to less demanding tasks like editing or formatting.

    Be empathetic and motivational in your advice, ensuring the user feels supported in managing their energy and completing the task. Your suggestions should encourage sustainable productivity and help them feel empowered to tackle their tasks efficiently and effectively.

    ---
    Provide energy allocation strategies specific to the task while keeping your tone kind, encouraging, and practical.
    ---
    """
)
