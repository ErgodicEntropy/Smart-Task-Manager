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

## Logical Architecture
![Logical Architecture](diagrams/Logical%20Architecture%20(Level%201).jpeg)
### Components Analysis:
- **User**: anyone engaged in a multitude of tasks but lacks a good model of: his own energy level, energy allocation strategies, task requirements.
- **Subjective Factors**: these are factors that inevitably emanates from the user.
   - *Biased Estimation*: the user subjectively lacks a representative model of his own energy level due to inevitable imperfect information and partial observability, thereby potentially disrupting the system's performance. 
   - *Priority (Sorting Order)*: the user has a subjective priority order that the system shouldn't alter but merely align with his (estimated) energy level.
- **System Inputs**:
   - *Estimated Energy*: the energy esimated by the user. Given that this esimation is subject to bias and lack of good representation, Sensitivity Analysis is needed to ensure that the system is well-conditioned (low condition number) i.e. robust, or that the energy estimation process is enhanced with categorical nudges and choices.
   - *Task List*: list of tasks sorted accordingly to priority, or unsorted if the user doesn't have an initial priority.
- **Smart Task Manager System**: the STM system processes input information to generate appropriate model to be utilized by the user
   - *Metacognitive Knowledge*: this is the second-order metacognitive knowledge that the user needs and lacks. This knowledge extends to the user's energy level, energy allocation strategies and task requirements.
   - *User-System Conversational Interaction*: a conversational interaction between the user and the system about his energy level, energy allocation strategies and task requirements.
      - ***Energy Model***: energy level conversational review to correct, if need be, user prior estimation.
      - ***Energy Allocation Model***: proposed energy allocation strategies.
      - ***Task Requirements Model***: discussion about the energetic requirements of each task.
   - *Structured Response (Conversation -> JSON Data)*: the user-system conversational interaction is converted to structured response in the form of JSON.
      - ***Person***: Data containing the Energy Model and Task Priority
      - ***Strategy***: Data containing Energy Allocation Model
      - ***Task***: Data containing Task Requirements Model and Task Priority
- **System Output**: Energy-Priority Aligned Tasks i.e. tasks sorted accoridngly to the user's priority and his energy level.
## Physical Architecture


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

