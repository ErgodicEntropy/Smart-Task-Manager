# Risk-Neutral Task Manager

A task management framework designed to optimize productivity by aligning tasks with energy levels, avoiding **Learned Helplessness**, and building **Failure Tolerance**. This system starts by focusing on small, easy-to-complete tasks to accumulate early successes, gradually increasing the complexity of tasks while leveraging the psychological principle of **Sunk Gain** to improve resilience and task performance.

## Product Management
### Problem Statement: Need + Obstacles
Lack of an efficienct energy distribution structure is a problem that haunts labor given scarcity of energy. People left on their own lack a good model of their energy allocation practices as well as task requirements, and often find themselves in burn-out, fluctuating from one task to another to offset (avoidable) dissipation of energy.
### Stakeholders/End Users
The primary users are anyone engaged in a multiplicity of tasks assumed to be initially unsorted (e.g. not sorted by priority)
### Product Roadmap
#### Product Vision 
Build a smart task manager that maximizes productivity (minimizes burn-out)
#### Product Strategy (Project Scope)
The smart task manager automates energy allocation strategies by aligning estimated energy and task requirements
## Systems Engineering
### Operational Analysis (User Requirements)
### Functional Analysis (System Requirements)
### Logical Architecture
#### High-level Architecture of the Overall Product
#### Low-level Architecture of the MVP
### Physical Architecture

## Features

- **Energy-Task Alignment**: Prioritize tasks based on available energy and optimal difficulty.
- **Failure Tolerance**: Build resilience by starting with easier tasks and progressively handling more complex ones.
- **Avoid Learned Helplessness**: Leverage initial successes to avoid frustration and increase motivation.
- **Sunk Gain Exploitation**: Use small, early wins to create momentum and buffer against failures.
- **Risk-Neutral Decision Making**: Focus on guaranteed gains to exploit risk-aversion toward losses.

## How It Works

The system starts by estimating the energy required for a list of tasks and selects the optimal one based on your current energy level. By focusing on tasks that provide early rewards, it helps build a psychological buffer, reducing the impact of future failures and encouraging consistent progress. This approach applies **Martin Seligman’s theory on Learned Helplessness**, aiming to unlearn helplessness through effort and strategic task selection.

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

