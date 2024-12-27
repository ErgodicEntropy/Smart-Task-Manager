# Smart Task Manager

A task management framework designed to optimize productivity by aligning tasks with energy levels, avoiding **Learned Helplessness**, and building **Failure Tolerance**. This system starts by focusing on small wins, easy-to-complete tasks to accumulate early successes in order to gain momentum (a positive feedback loop), gradually increasing the complexity of tasks while leveraging the psychological principle of **Sunk Gain** to improve resilience, robustness and task performance. Given an energy level E, starting with a task with complexity C (or difficulty D) that requires an energy level E(C) > E, is likely to disrupt the **Power Proces** defined as: having a goal, exerting serious efforts towards that goal and attaining the goal.

The framework takes in consideration that the (negative) impact of a loss, as in failing to complete task due to complexity-energy mismatch, is much greater, everything else held equal (ceteris paribus), than the (positive) impact of a gain, as in completing the task (attaining the goal). The power process is therefore not risk-neutral, but risk averse. The framework also takes in consideration the timing or chronological order of both types of these impact e.g. having accumulated initially losses is worse (more negatively impactful) than doing so after accumulating initial gains-- this is very well documented by the Sunk Cost fallacy. The framework also takes in consideration the continuity of either losses or gains (and the feedback loops that arise from them) in that the Power Process dynamics represents a pitchfork bifurcation between either a positive feedback loop of learned helplessness, or a positive feedback loop of learned robustness. 

The frameworks also takes in consideration other effects such as: Planning fallacy, Optimism Bias and Parkinson Law. To deal with them, the system needs to emulate the Pomodoro and Task Unpacking techniques.

#### References
|Concept|Source|
|-----|-----|
|Power Process|[Power Process](https://en.wikipedia.org/wiki/Industrial_Society_and_Its_Future)|
|Prospect Theory|[Prospect Theory](https://en.wikipedia.org/wiki/Prospect_theory)|
|Sunk Cost Fallacy|[Sunk Cost Fallact](https://en.wikipedia.org/wiki/Sunk_cost)|
|Learned Helplessness|[Learned Helplessness](https://ppc.sas.upenn.edu/sites/default/files/learnedhelplessness.pdf)|
|Planning Fallacy|[Planning Fallacy](https://en.wikipedia.org/wiki/Planning_fallacy)|
|Optimism Bias|[Optimism Bias](https://en.wikipedia.org/wiki/Optimism_bias)|
|Parkinson Law|[Parkinson Law](https://en.wikipedia.org/wiki/Parkinson%27s_law)|
|Pomodoro Technique|[Pomodoro Technique](https://en.wikipedia.org/wiki/Pomodoro_Technique)|
|Unpacking Technique|[Unpacking Technique](https://transformyour.work/aad2d3d202af4fcebd0177d65242f775)|
## Mathematical Model (Mathematical Simulation of the Proof-of-Concept)

## How It Works

The system starts by estimating the energy required for a list of tasks and selects the optimal one based on your current energy level. By focusing on tasks that provide early rewards, it helps build a psychological buffer, reducing the impact of future failures and encouraging consistent progress. This approach applies **Martin Seligman’s theory on Learned Helplessness**, aiming to unlearn helplessness through effort and strategic task selection.

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

## Logical Architecture (Overall Product)
![Logical Architecture](diagrams/Logical%20Architecture.jpeg)
### Components Analysis:
- **User**: anyone engaged in a multitude of tasks but lacks a good model of: his own energy level, energy allocation strategies, task requirements.
- **Subjective Factors**: these are factors that inevitably emanates from the user.
   - *Biased Estimation*: the user subjectively lacks a representative model of his own energy level due to inevitable imperfect information and partial observability, thereby potentially disrupting the system's performance. 
   - *Priority (Sorting Order)*: the user has a subjective priority order that the system shouldn't alter but merely align with his (estimated) energy level.
- **System Inputs**:
   - *Estimated Energy*: the energy esimated by the user. Given that this esimation is subject to bias and lack of good representation, Sensitivity Analysis is needed to ensure that the system is well-conditioned (low condition number) i.e. robust, or that the energy estimation process is enhanced with categorical nudges and choices.
   - *Estimation Error Correction*: 
      - Orthogonalization Method: Divide-and-Conquer the energy-specific question into subquestions each of which concerning a domain and/or axis of energy measurement which is orthogonal to every other subquestion (zero covariance or overlap implies maximum user information feedback) e.g. Intellectual Energy (e.g. Cognitive Energy: Clarity of Thought, Focus/Attention, Mental Fatigue. Task Readiness, Cognitive Load), Psychological Energy (e,g. Mental Energy: Motivation, Stress Level, Emotional State), Physical Energy, Temporal Energy (Circadian Rhythm (Peak Times/Cortisol Level), Energy Trends), Environmental Energy (External Stimulation), Social Energy (Interaction Energy), Behavioral Energy. 
      - Pilot Test: a quick, gamified test to measure energy. The problem with this method is that the measures do not prefigure the task unless the test is the task itself (performance actualism) which defeats the logic.
   - *Task List*: list of tasks sorted accordingly to priority, or unsorted if the user doesn't have an initial priority.
- **Smart Task Manager System**: the STM system processes input information to generate appropriate model to be utilized by the user
   - *Sensitivity Analysis*: the input error corresponds to an output error regardless of the system's efficiency, implying the need for estimation error correction, otherwise the system will function at an effectiveness value bounded by the input error.
   - *Metacognitive Knowledge*: this is the second-order metacognitive knowledge that the user needs and lacks. This knowledge extends to the user's energy level, energy allocation strategies and task requirements.
   - *Task Requirements*: the energetic demands of each tasks which depend on a lot of factors and the prevailing user context, making them hard to measure accurately.
   - *Requirement Error Correction*: Contextualization
      - User Feedback: Pre-done tasks and Finished Tasks (Kanban Board)
      - LLM: Task Genericity and Task Comparability (LLM Eligibility) -> Specific Prompting, Fine-Tuning or RAG
      - External Database
- **System Output**: 
   - Energy-Priority Aligned Tasks i.e. tasks sorted accoridngly to the user's priority and his energy level.
   - Recommendation: LLM-generated piece of advice concerning energy allocation strategies based on the provided optimal tasks list.
## Physical Architecture
![Physical Architecture](diagrams/Physical%20Architecture.jpeg)
### Components Analysis: 
- **User**: anyone engaged in a multitude of tasks but lacks a good model of: his own energy level, energy allocation strategies, task requirements.
- **Interface**: The user submits his data composed of his estimated energy and a task list ordered by priority: Options (Discrete Data), Slider (Continuous Data).
- **Scale**: The scale used to compute the weighted average score of energy level and task requirements: Likert Scale (Numeric Discrete), Percentage (Numeric Continuous), Categorical (Nominal Discrete)
- **Energy Orthogonalization Function**: this function maximizes user information feedback based on the orthogonal superposition principle.
- **Energy Scoring Function**: this function compounds the results of the energy orthogonalization function into a weighted average or sum.
- **Task Orthogonalization Function**: this function maximizes task requirement information based on the orthogonal superposition principle.
- **Requirement Scoring Function**: this function compounds the results of the task orthogonalization function into a weighted average or sum
- **Task Requirements**: the energetic demands of each tasks which depend on a lot of factors and the prevailing context, making them hard to measure accurately. 
- **AI Agent**: the role of the AI Agent is to contextualize the task requirement database to fit the user-context (user input data).
- **Optimal Task Button**: the user clicks on this button to redirect towards an interface that displays the optimally aligned task list with his energy level as well as priority.
- **Recommendation Button**: the user clicks on this button to get recommendations on energy allocation strategies for the optimal task list provided.
- **User Feedback On Finished Tasks**: the user provides feedback on the task difficulty after finishing it.


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

