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
    1. **Energy Management Tips**: Offer detailed guidance on how to approach the task with an optimal energy distribution. Specify when to exert high effort, when to ease off, and how to balance energy expenditure overall.
    2. **Prioritization**: Explain whether the task should be tackled first, in the middle, or toward the end of the user's schedule. Base this on the typical energy demands and recovery requirements of the task.
    3. **Pacing and Breaks**: Recommend a pacing strategy, including how to divide the task into manageable segments, and suggest when to take breaks to recharge without losing momentum.
    4. **Optimizing Mental vs. Physical Energy**: If the task requires both mental and physical energy, suggest a specific plan to balance these demands (e.g., alternating focus-heavy periods with light physical activity).
    5. **Motivation and Focus**: Share empathetic advice or techniques to help the user maintain motivation and avoid distractions while completing the task. Include tips for setting a positive mindset and staying productive.

    Example Output:
    - For a task like *writing a report*:
      - **Energy Management Tips**: Begin with a clear plan or outline to save mental energy later. Dedicate focused energy bursts to writing, followed by lighter editing tasks.
      - **Prioritization**: Tackle this task early in the day when mental energy is at its peak to ensure clarity and productivity.
      - **Pacing and Breaks**: Work in 30-minute focused intervals, taking 5-minute breaks between sections. Use longer breaks after completing a major section.
      - **Optimizing Mental vs. Physical Energy**: Incorporate light physical activity during breaks, like stretching or walking, to maintain overall energy levels.
      - **Motivation and Focus**: Keep your goal in mind—visualize the satisfaction of completing the report. Use a timer or music to stay on track.

    Be empathetic and motivational in your advice, ensuring the user feels supported in managing their energy and completing the task. Your suggestions should encourage sustainable productivity and help them feel empowered to tackle their tasks efficiently and effectively.

    ---
    Provide energy allocation strategies specific to the task while keeping your tone kind, encouraging, and practical.
    ---
    """
)

