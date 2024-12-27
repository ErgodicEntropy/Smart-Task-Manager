from langchain.prompts import PromptTemplate



Energy_Prompt_Template = PromptTemplate(
    input_variables=['energy_level'],
    template="""
You are a helpful assistant tasked with evaluating a user’s energy level. The user has provided an initial estimate of their energy level: {energy_level}.

Please ask the user to send a paragraph that helps you accurately estimate their energy. Encourage them to describe their current state as clearly as possible by considering the following aspects:
- Their physical and mental condition right now
- Whether they’ve had any recent rest or breaks
- How prepared they feel to take on tasks that require concentration


Make sure to explain that the more specific and honest their description is, the better the estimate will be. Keep the tone friendly and concise, and remind them to focus on the most relevant details.
Make sure that your output to the user is extremely brief without redundancy, ideally a phrase or two.

"""
)


Retain_Prompt_Template = PromptTemplate(
    input_variables=['user_message'],
    template="""
You have been having a conversation with the user about their tasks, energy levels, and various other factors that influence their energy. 

Based on the conversation, as well as the user's final response to the question of how they rate their energy level, your task is to summarize their current energy state based on their answer: {user_message}

Please consider the following:
1. Throughout the conversation, the user mentioned tasks and activities that may have provided insight into their energy level (e.g., tasks they consider tiring, mentally exhausting, etc.).
2. Pay attention to the final message where the user explicitly rates their energy level, or if they don't provide a final rating, summarize their energy level based on the entire conversation. Consider factors like how demanding their tasks were, how they described their energy during the conversation, and any explicit ratings provided.
3. If the user did not explicitly state their energy level, infer it based on their statements about task difficulty, physical or mental exhaustion, and overall tone throughout the chat.

Your output should be a summary of their current energy level and how you arrived at that conclusion. The energy levels to consider are:
- Extremely Low
- Low
- Moderate
- High
- Extremely High

Your output should be a clear-cut category (basically one line): extremely low, low, moderate, high, extremely High

Make sure to write the output in that exact lower-case format!

Provide your response in a clear, concise manner that gives the user a sense of how they might be feeling based on the entire conversation.

Example: 
If the user mentions feeling drained after doing multiple tasks and says they have very little energy left, your response might conclude: "It seems like you're feeling low on energy after completing various tasks. You've described feeling physically and mentally exhausted, and your energy level seems to be quite low."

Please give a short, supportive, and empathetic summary, acknowledging the user's energy level.

---
Final energy rating (if provided by the user) or inferred energy level:

"""
)


Task_Prompt_Template = PromptTemplate(
    input_variables=['tasks_list'],
    template="""
You are a helpful assistant assisting a user in understanding the energetic requirements of a list of tasks they have. The user has provided a list of tasks they need to accomplish. Your goal is to explain the energy each task may require, based on common experiences, in a friendly, empathetic, and easily understandable way.

Here is the list of tasks provided by the user:
{tasks_list}

For each task in the list, kindly explain the following:
- The energy level that may typically be required for the task.
- Whether the task requires high, moderate, or low energy.
- If the task may be mentally demanding, physically tiring, or both.
- Offer tips on how to tackle the task based on its energy requirement (e.g., how to prepare, take breaks, or pace yourself).

Your tone should be supportive and understanding, helping the user feel confident about approaching these tasks. Be mindful that energy levels vary from person to person, so offer general advice but also acknowledge that each person’s experience might differ.

Please generate an HTML table as output, with the following columns:
- **content**: A short description of the task (e.g., "Make the bed", "Go for a walk").
- **energy_required**: The energy level required for the task (use one of the following categories: "extremely low", "low", "moderate", "high", "extremely high").
- **preparation**: A brief description of what preparation or pacing might be needed (e.g., "Take breaks", "Prepare a plan").
- **task_type**: Mentally, physically, or both demanding (e.g., "Physical", "Mental", "Both").
- **recommended_start_time**: A suggested time for the user to start the task (e.g., "Morning", "Afternoon").

Make sure the table looks neat and is easy to read in HTML format.

Here is an example of the table format:
<table>
  <thead>
    <tr>
      <th>Content</th>
      <th>Energy Required</th>
      <th>Preparation</th>
      <th>Task Type</th>
      <th>Recommended Start Time</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Make the bed</td>
      <td>Low</td>
      <td>Take breaks</td>
      <td>Physical</td>
      <td>Morning</td>
    </tr>
    <tr>
      <td>Go for a walk</td>
      <td>Moderate</td>
      <td>Wear comfortable shoes</td>
      <td>Physical</td>
      <td>After morning meal</td>
    </tr>
    <tr>
      <td>Write a report</td>
      <td>High</td>
      <td>Plan ahead</td>
      <td>Mental</td>
      <td>Afternoon</td>
    </tr>
  </tbody>
</table>

Please go through each task and explain what kind of energy it might need, how it could feel, and offer supportive suggestions on how to manage energy while doing them.
"""
)



                    

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

TaskRequer = PromptTemplate(input_variables=['tasks_list'], template=
"""

You are a helpful assistant tasked with analyzing a list of tasks provided by the user. Your role is to assess the energetic requirements for each task and return a JSON dictionary containing specific information about each task in a structured format. 

For each task in the list, return it as an object with the following properties:
- content: A short description of the task (e.g., "Make the bed", "Go for a walk").
- energy_required: The energy level required for the task. This must be strictly one of the following categories: 
  - "extremely low"
  - "low"
  - "moderate"
  - "high"
  - "extremely high"
- preparation: A brief description of what preparation or pacing might be needed (e.g., "Take breaks", "Prepare a plan").
- task_type: Mentally, physically, or both demanding (e.g., "Physical", "Mental", "Both").
- recommended_start_time: A suggested time for the user to start the task (e.g., "Morning", "Afternoon").

Please note:
- Be strict with the energy_required categories to ensure consistency in the output, as the values will be used programmatically.
- Provide a general assessment based on common experiences for each task while acknowledging that individual perceptions of energy levels may vary.

Here is the list of tasks provided by the user:
{tasks_list}

Your response should strictly adhere to the following JSON format:
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

Ensure all tasks in the list are represented in the JSON dictionary. If additional information about a task seems unclear, make a reasonable assumption based on common experience and ensure the energy_required value is strictly one of the allowed categories. Be concise in your response, returning only the JSON object.

---

Here’s an example of your expected output:
[
    {{
        "content": "Go for a morning jog in the park",
        "energy_required": "low",
        "preparation": "Wear comfortable shoes and stretch lightly",
        "task_type": "Physical",
        "recommended_start_time": "Morning"
    }},
    {{
        "content": "Complete the financial analysis report",
        "energy_required": "moderate",
        "preparation": "Gather all financial data and review last month’s report",
        "task_type": "Mental",
        "recommended_start_time": "Afternoon"
    }},
    {{
        "content": "Plan a weekend outing",
        "energy_required": "high",
        "preparation": "Research destinations and activities, and organize travel arrangements",
        "task_type": "Both",
        "recommended_start_time": "Evening"
    }},
    {{
        "content": "Clean and organize the garage",
        "energy_required": "high",
        "preparation": "Wear gloves and set aside containers for sorting items",
        "task_type": "Physical",
        "recommended_start_time": "Morning"
    }},
    {{
        "content": "Learn a new programming concept",
        "energy_required": "moderate",
        "preparation": "Find reliable learning resources and allocate focused time",
        "task_type": "Mental",
        "recommended_start_time": "Afternoon"
    }},
    {{
        "content": "Cook a three-course dinner",
        "energy_required": "high",
        "preparation": "Prepare ingredients and ensure kitchen tools are ready",
        "task_type": "Both",
        "recommended_start_time": "Evening"
    }}
]

Please process the task list and return the structured JSON response.
Ensure that only this exact JSON structure is output, and NOTHING ELSE. Your response should contain NO additional phrases, explanations, or commentary. Only print the JSON as shown in the template above, without adding anything else.
Your response is a clear-cut, structured JSON dictionary. JUST PRINT THE JSON AND NOTHING ELSE!!!!!!!
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
