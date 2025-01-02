# SparkFlow

Meet **SparkFlow**, the friendly task manager designed to help you get things done without feeling overwhelmed. If you have ADHD or just struggle with managing your energy and tasks, SparkFlow is here to make life easier. It focuses on small, doable tasks to help you build momentum and keep going, even when things feel tough.
## How It Helps:

1. **Matches Your Energy**: Helps you pick tasks that fit your current energy level, so you don’t burn out.
2. **Start with Rewards**: It prioritizes tasks that are quick and rewarding to complete given the user's energy. These small wins give you a boost of confidence and motivation.
3. **Builds Momentum**: Turns small successes into stepping stones for bigger achievements, creates a psychological safety net to reduce the fear of failure and helps you handle tougher tasks later.
4. **Grows With You**: Gradually helps you take on more challenging tasks as you build confidence, gently nudges you toward slightly more challenging tasks, helping you grow without feeling pressured.
5. **ADHD-Friendly**: Designed with techniques that work well for people who struggle with focus and energy management.

Inspired by *Martin Seligman’s theory on Learned Helplessness*, SparkFlow helps you break the cycle of feeling stuck. It encourages effort and smart task selection to build resilience and keep you moving forward

## Why SparkFlow?
Traditional task managers can feel overwhelming, especially if you have ADHD. SparkFlow is different. It breaks things down into tiny, manageable steps so you can start without stress. By focusing on small wins, it helps you build momentum and keeps you moving forward, even on tough days.
## How It Works:
SparkFlow makes task management simple and stress-free. Here’s how it helps you stay on track:

1. **Match Your Energy**: SparkFlow suggests tasks that align with your current energy level—whether you’re feeling low, medium, or peak energy. It’s all about efficiency, not just starting easy.
2. **Feel the Win**: Complete it and feel that sense of accomplishment.
3. **Build Momentum**: Use that good feeling to tackle the next thing.
4. **Grow Gradually**: As you gain confidence, take on slightly bigger tasks.
5. **Keep Flowing**: Keep the progress going, one small step at a time.

## Mathematical Model (Mathematical Simulation of the Proof-of-Concept)

## Product Management
### Problem Statement:
Lack of an efficienct energy distribution structure is a problem that haunts labor given scarcity of energy. People left on their own lack a good model of their energy allocation practices as well as task requirements, and often find themselves in burn-out, fluctuating from one task to another to offset (avoidable) dissipation of energy.
![Problem Visual](diagrams/Problem%20Visualization.jpeg)
### Stakeholders/End Users
The primary users are anyone engaged in a multiplicity of tasks whom he lacks a good model of in terms of: his own estimated energy, task requirements, efficient energy allocation strategies, without impacting his subjective priority.
### Product Roadmap
#### Product Vision 
Build a smart task manager that maximizes productivity (minimizes burn-out)
#### Product Strategy (Project Scope)
The smart task manager automates energy allocation strategies by aligning estimated energy, user priority and task requirements
## Functional Analysis (System Requirements)

- **Energy-Task Alignment**: Prioritize tasks based on available energy and optimal difficulty.
- **Failure Tolerance**: Build resilience by starting with easier tasks and progressively handling more complex ones.
- **Avoid Learned Helplessness**: Leverage initial successes to avoid frustration and increase motivation.
- **Sunk Gain Exploitation**: Use small, early wins to create momentum and buffer against failures.
- **Risk-Neutral Decision Making**: Focus on guaranteed gains to exploit risk-aversion toward losses.

## Logical Architecture
![Logical Architecture](diagrams/Logical%20Architecture.jpeg)
### Components Analysis:
- **User**: anyone engaged in a multitude of tasks but lacks a good model of: his own energy level, energy allocation strategies, task requirements.
   - *Goals (Priority)*
   - *Current skills*
   - *Work Experience* e.g. CV
   - *Energy levels*

- **Subjective Factors**: these are factors that inevitably emanates from the user.
   - *Biased Estimation*: the user subjectively lacks a representative model of his own energy level due to inevitable imperfect information and partial observability, thereby potentially disrupting the system's performance. 
   - *Priority (Sorting Order)*: the user has a subjective priority order that the system shouldn't alter but merely align with his (estimated) energy level.
- **System Inputs**:
   - *Estimated Energy*: the energy esimated by the user. Given that this esimation is subject to bias and lack of good representation, Sensitivity Analysis is needed to ensure that the system is well-conditioned (low condition number) i.e. robust, or that the energy estimation process is enhanced with categorical nudges and choices (user skills can also be used instead of user energy but that changes the logic of the app).
   - *Estimation Error Correction*: 
      - Magic Insight (Penultimate Step): one parameter to rule them all e.g. energy/impact ratio.
      - Orthogonalization Method: Divide-and-Conquer the energy-specific question into subquestions each of which concerning a domain and/or axis of energy measurement which is orthogonal to every other subquestion (zero covariance or overlap implies maximum user information feedback) e.g. Intellectual Energy (e.g. Cognitive Energy: Clarity of Thought, Focus/Attention, Mental Fatigue. Task Readiness, Cognitive Load), Psychological Energy (e,g. Mental Energy: Motivation, Stress Level, Emotional State), Physical Energy, Temporal Energy (Circadian Rhythm (Peak Times/Cortisol Level), Energy Trends), Environmental Energy (External Stimulation), Social Energy (Interaction Energy), Behavioral Energy. 
      The limits of orthogonalization is recursion dilemma and saturation effects (diminishing returns if too many variables used).
      - Pilot Test: a quick, gamified test to measure energy. The problem with this method is that the measures do not prefigure the task unless the test is the task itself (performance actualism) which defeats the logic due to the task-specific nature of the test for its effectiveness. However, user-specific (task-free) tests can be conducted with the purpose of measuring user energy.
   - *Task List*: list of tasks sorted accordingly to priority, or unsorted if the user doesn't have an initial priority.
- **Smart Task Manager System**: the STM system processes input information to generate appropriate model to be utilized by the user
   - *Sensitivity Analysis*: the input error corresponds to an output error regardless of the system's efficiency, implying the need for estimation error correction, otherwise the system will function at an effectiveness value bounded by the input error.
   - *Metacognitive Knowledge*: this is the second-order metacognitive knowledge that the user needs and lacks. This knowledge extends to the user's energy level, energy allocation strategies and task requirements.
   - *Task Requirements*: the energetic demands of each tasks which depend on a lot of factors and the prevailing user context, making them hard to measure accurately.
   - *Requirement Error Correction*: User-Contextualization and Metamodeling
      - User Feedback: Finished Tasks (Kanban Board)
      - LLM: Divide-and-Conquer Prompting (works especially if the tasks are generic and easily comparable e.g. writing vs coding), Fine-Tuning or RAG
      - External Database
   - *Task Metamodel*: the metamodel variables can either be solely task-specific, or user-task-specific and they should also pertain to abstract the energy required by task (they should measure, in collectivity, the energy demands of a task)
      1- Priority: How closely the task aligns with the user immediate or future goals e.g. urgency, passion, interest, motivation.
      2- Skill Overlap/Transferability (Transfer Theory): The extent to which existing skills can be reused in the task (a good [MVP](https://github.com/ErgodicEntropy/Skill-Matcher)).
      3- Learning Curve: How steep the initial difficulty is and how quickly proficiency can be achieved.
      4- Community and Ecosystem: The size, quality, and activity of the community and available resources for the task.
      5- Depth vs. Breadth: Whether the task requires exploring a few concepts deeply or many concepts broadly.
      6- Relevance to Current Trends: How "cutting-edge" or in-demand the skill is in the market.
      7- Task Novelty: The level of unfamiliarity or learning involved in the task
      8- Cognitive Load/Complexity: The mental effort required to complete the task e.g. high-demand (strategic, creative) to low-demand (repetitive, mechanical)
      9- Temporal Focus Intensity: The required focus duration for successful task completion. Examples: High (programming for hours), Moderate (cleaning a room), Low (sending a quick email).
      10- Physical Exertion: The physical effort required for the task. Examples: High (moving furniture), Moderate (cooking), Low (writing an email).
      11- Risk-to-Reward Balance: The potential risks involved in the task compared to its anticipated benefits. e.g.  Launching a startup (high risk, high reward) vs. updating a resume (low risk, moderate reward).
      12- Collaboration Intensity: The degree to which the task depends on coordination with others (energy demand diffused through economies of scale) e.g. Group project (high intensity) vs. individual coding session (low intensity).
      13- Task Duration: The typical time required to complete the task.
      14- Task Precision: The level of accuracy or exactness required for successful task execution.
      15- Recommended Start Time: Early Morning, Morning, Afternoon, Evening, Night, Midnight
   - *Task Model (System Identification)*: 
      1- System Identifier: User (user-task-specific metamodel) or AI Agent (task-specific metamodel)
      2- Modeling Typicality
      3- Modeling Difficulty      
- **System Output**: 
   - Energy-Priority Aligned Tasks i.e. tasks sorted accoridngly to the user's priority and his energy level.
   - Recommendation: LLM-generated piece of advice concerning energy allocation strategies based on the provided optimal tasks list.
## Physical Architecture
![Physical Architecture](diagrams/Physical%20Architecture.jpeg)
### Components Analysis: 
- **User**: anyone engaged in a multitude of tasks but lacks a good model of: his own energy level, energy allocation strategies, task requirements.
- **Data Interface**: The user submits his data composed of his estimated energy and a task list ordered by priority: Options (Discrete Data), Slider (Continuous Data).
- **Scale**: The scale used to compute the weighted average score of energy level and task requirements: Likert Scale (Numeric Discrete), Percentage (Numeric Continuous), Categorical (Nominal Discrete)
- **Energy Orthogonalization Function**: this function maximizes user information feedback based on the orthogonal superposition principle.
- **Energy Scoring Function**: this function compounds the results of the energy orthogonalization function into a weighted average or sum.
- **Energy Threshold Function**: this function classifies the result of the energy scoring function into an energy category from low to high -> this function may end up undoing the value of the orthogonalization method because it abstracts all modularity into one category causing thereby information loss.
- **Task Orthogonalization Function**: this function maximizes task requirement information based on the orthogonal superposition principle.
- **Requirement Scoring Function**: this function compounds the results of the task orthogonalization function into a weighted average or sum 
- **Requirement Threshold Function**: this function classifies the result of the task scoring function into an task required energy category from low to high -> this function may end up undoing the value of the orthogonalization method because it abstracts all modularity into one category causing thereby information loss.
- **Energy-Requirement Alignment Scoring Function (Optional)** :  this function compounds the results of the task orthogonalization function and energy orthogonalization function into a weighted average or sum to avoid orthogonalization information loss, but it requires that the orthgonalization process is user-task bijective (one-to-one metamodel equivalence)
- **Energy-Requirement Alignment Threshold Function (Optional)**: this function classifies the result of the alignment scoring function into an alignment category (unaligned, moderately aligned, completely aligned)
- **Task Requirements**: the energetic demands of each tasks which depend on a lot of factors and the prevailing context, making them hard to measure accurately. Technically, the task requirements is stored in a dynamic database that changes with human-feedback.
- **AI Agent**: the role of the AI Agent is to contextualize the task requirement database to fit the user-context (user input data). To do so, it checks whether there is a pre-existing human feedback on the database (Fine-tuning or RAG), otherwise it generates task requirement itself (specific prompting). This process goes from initial prompting to eventual Fine-tuning or RAG.
- **Optimal Task Button**: the user clicks on this button to redirect towards an interface that displays the optimally aligned task list with his energy level as well as priority.
- **Kanban Board**: the optimal task list is organized according to a gamified Kanban board.
- **Human-in-the-Loop and Network Effects**: this subarchitecture exploits the positive network effects of other users feedback to allow for scalability and impact.
- **User Feedback On Finished Tasks**: the user provides feedback on the task difficulty (or required energy) after finishing it.
   - *Task difficulty*
   - *Time taken* (user-given or system-given)
   - *Satisfaction with the learning outcome*
- **Context-Friendly Human Feedback**: task labeling based on context-friendly human feedback represented by the task required energy on the user initial energy ratio -> a supervised learning model is utilized to match each task-user energy ratio to a task label (user-free task required energy) or a symbolic model using a JSON dict (this process is called task decontextualization, and its purpose is scalability to facilitate network effects)
- **Recommendation Button**: the user clicks on this button to get recommendations on energy allocation strategies for the optimal task list provided.
- **QA Conversational Interface**: the LLM enters into a chat conversation with the user about each task in the optimal tasks list (ideally, fine-tuning or RAG should be used in this step) ->  With enough human-in-the-loop (enough network effects), the task requirements database gets increasingly filled to eventually allow for the transition from specific prompting to fine-tuning and/or RAG.
   1. Task Segmentation Strategy:  How the user decides to break down the task into smaller segments or phases, affecting their work rhythm (e.g., segmented vs. continuous work).
   2. Energy Conservation Strategy: The approach the user takes to conserve their energy for later stages of the task or other future tasks.
   3. Break/Rest Strategy: How the user decides to take breaks or rest during task execution, and how these breaks are structured.
   4. Energy Recovery Strategy: How the user plans for recovery during or after the task to prevent burnout and recharge for future tasks.
   5. Task Switching Strategy: The approach the user takes to switch between tasks, balancing cognitive load and energy conservation.
   6. Energy Effort Adjustment: Measures how the user adjusts the intensity of their effort in response to task demands and their current energy reserves.
## Installation

To get started with the project, follow these steps:


1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/risk-neutral-task-manager.git

2. **Login to Heroku**  
   Open your terminal (in VSCode or any terminal) and log in to your Heroku account by running:
   - `heroku login`  
     This will open a browser window for authentication.

3. **Add Changes to Git**  
   Stage your changes for commit by running:
   - `git add .`  
     This will add all modified files to the staging area.

4. **Commit Your Changes**  
   Commit your changes with a descriptive message:
   - `git commit -m "Your commit message"`

5. **Create a New Heroku App**  
   Create a new app on Heroku by running:
   - `heroku create {name-of-your-app}`  
     Replace `{name-of-your-app}` with your desired app name. It must be unique.

6. **Verify Heroku Remote URL**  
   Confirm that the Heroku remote repository is correctly set up:
   - `git remote -v`  
     This will display the remote URL for Heroku.

7. **Push to Heroku**  
   Push your code to Heroku to deploy your app:
   - If you’re using the `main` branch:
     - `git push heroku main`
   - If you’re using the `master` branch:
     - `git push heroku master`  
     Heroku will build and deploy your app.

8. **Open Your App**  
   After the deployment process is complete, you can access your app in the browser:
   - `heroku open`  
     This will automatically open your deployed app in your default browser.

