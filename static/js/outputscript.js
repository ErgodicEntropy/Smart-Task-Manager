let timers = {};

function startTimer(taskId) {
    const startTime = Date.now();
    timers[taskId] = startTime;

    const timerDisplay = document.createElement('span');
    timerDisplay.id = 'timer-' + taskId;
    timerDisplay.style.marginLeft = '10px';
    document.getElementById('task-' + taskId).appendChild(timerDisplay);

    updateTimer(taskId);
}

function updateTimer(taskId) {
    const timerDisplay = document.getElementById('timer-' + taskId);
    if (!timerDisplay) return;

    const elapsedTime = Date.now() - timers[taskId];
    const seconds = Math.floor((elapsedTime / 1000) % 60);
    const minutes = Math.floor((elapsedTime / (1000 * 60)) % 60);
    const hours = Math.floor((elapsedTime / (1000 * 60 * 60)) % 24);

    timerDisplay.innerHTML = `${hours}h ${minutes}m ${seconds}s`;

    setTimeout(() => updateTimer(taskId), 1000);
}

function stopTimer(taskId) {
    delete timers[taskId];
    const timerDisplay = document.getElementById('timer-' + taskId);
    if (timerDisplay) {
        timerDisplay.remove();
    }
}

function markAsDoing(taskId) {
    const taskRow = document.getElementById('task-' + taskId);
    const taskContent = taskRow.querySelector('td');

    taskRow.classList.add('doing');
    taskContent.classList.add('almost_completed');

    const doingButton = taskRow.querySelector('.doing-button');
    doingButton.innerHTML = 'Doing';
    doingButton.style.backgroundColor = '#808080';
    doingButton.style.cursor = 'not-allowed';

    startTimer(taskId);
}
function openFeedbackModal(taskId){
    const overlay = document.getElementById("overlay");
    const modal = document.getElementById("feedbackModal");
    overlay.style.display = "block";        
    modal.style.display = "block";
    

    // Save taskId in a hidden field or as a global variable
    modal.dataset.taskId = taskId;

}

function submitFeedback() {
    const modal = document.getElementById("feedbackModal");

    const taskId = modal.dataset.taskId;
    const feedback = document.querySelector('input[name="feedback"]:checked');
    
    if (feedback) {
        saveFeedback(taskId, feedback.value);
        closeModal();
    } else {
        alert("Please select a feedback option.");
    }
}

function saveFeedback(taskId, feedback) {
    console.log(`Task ID: ${taskId}, Feedback: ${feedback}`);

    fetch('/save_feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ taskId: taskId, feedback: feedback }),
    })
    .then(response => {
        if (response.ok) {
            return response.blob(); // Receive the file as a blob
        }
        throw new Error('Failed to save feedback');
    })
    .then(blob => {
        // Create a link element and trigger the download
        const link = document.createElement('a');
        const url = window.URL.createObjectURL(blob);
        link.href = url;
        link.download = 'feedback.json'; // Default file name for the downloaded file
        link.click(); // Trigger the download
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function closeModal() {
    const modal = document.getElementById("feedbackModal");
    const overlay = document.getElementById("overlay");
    modal.style.display = "none";
    overlay.style.display = "none";
}
    
function markAsFinished(taskId) {
    const taskRow = document.getElementById('task-' + taskId);
    const taskContent = taskRow.querySelector('td');

    taskRow.classList.add('finished');
    taskContent.classList.add('completed');
    
    const finishButton = taskRow.querySelector('.finish-button');
    finishButton.innerHTML = 'Completed';
    finishButton.style.backgroundColor = '#808080';
    finishButton.style.cursor = 'not-allowed';

    stopTimer(taskId);
    openFeedbackModal(taskId);
}

// Function to show the loading overlay
function showLoading() {
    document.getElementById('loading-overlay').style.display = 'flex';
}

// Function to hide the loading overlay
function hideLoading() {
    document.getElementById('loading-overlay').style.display = 'none';
}

// Function to update the loading message
function updateLoadingMessage(message) {
    document.getElementById('loading-message').textContent = message;
}
            
function getRecommendation(taskId) {
    const overlay = document.getElementById("overlay");
    const chatmodal = document.getElementById("chatbot");
    const botMessageDiv = document.querySelector(".message.bot-message");

    // Show the overlay and chatbot modal
    overlay.style.display = "block";
    chatmodal.style.display = "block";

    // Show the loading overlay and update the message
    showLoading();
    updateLoadingMessage('Processing your request. Please wait...');

    // Fetch the recommendation
    fetch(`/get_recommendation/${taskId}`, {
        method: 'GET',
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Parse the JSON response
    })
    .then(data => {
        console.log('Task:', data.task);
        console.log('Response:', data.response);

        // Update the loading message
        updateLoadingMessage('Almost there!  Thanks for your patience.' );

        // Update the UI with the data
        if (botMessageDiv) {
            botMessageDiv.textContent = data.response; // Update the content
        } else {
            console.error("Bot message div not found!");
            throw new Error("Bot message div not found!");
        }
    })
    .catch(error => {
        console.error('Error:', error);
        updateLoadingMessage('Something went wrong. Please try again.');
    })
    .finally(() => {
        hideLoading(); // Hide the loading overlay regardless of success or error
    });
}

function postRecommendation() {
    const userMessage = document.getElementById("userMessage").value;
    const chatbox = document.querySelector(".chatbox");

    // Show the loading overlay and update the message
    showLoading();
    updateLoadingMessage('Processing your request. Please wait...');

    // Fetch the recommendation
    fetch(`/post_recommendation`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ userMessage: userMessage }), // Send the user message
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Parse the JSON response
    })
    .then(data => {
        console.log('Response:', data.response);

        // Update the loading message
        updateLoadingMessage('Almost there! Thanks for your patience.');

        // Append the user's message as a separate div
        const userMessageDiv = document.createElement("div");
        userMessageDiv.className = "message user-message";
        userMessageDiv.textContent = userMessage;

        // Append the bot's response as a separate div
        const botMessageDiv = document.createElement("div");
        botMessageDiv.className = "message bot-message";
        botMessageDiv.textContent = data.response;

        // Add messages to the chatbox
        chatbox.appendChild(userMessageDiv);
        chatbox.appendChild(botMessageDiv);

        // Clear the input field
        document.getElementById("userMessage").value = "";
    })
    .catch(error => {
        console.error('Error:', error);
        updateLoadingMessage('Something went wrong. Please try again.');
    })
    .finally(() => {
        hideLoading(); // Hide the loading overlay regardless of success or error
    });
}

        
function closeChat() {
    const overlay = document.getElementById("overlay");
    const chatmodal = document.getElementById("chatbot");
    chatmodal.style.display = "none";
    overlay.style.display = "none";

}

function getExplanation(taskId) {
    const overlay = document.getElementById("overlay");
    const chatmodal = document.getElementById("chatbot_explainer");
    const botMessageDiv = document.querySelector(".message.bot-message_explainer");

    // Show the overlay and chatbot modal
    overlay.style.display = "block";
    chatmodal.style.display = "block";

    // Show the loading overlay and update the message
    showLoading();
    updateLoadingMessage('Processing your request. Please wait...');

    // Fetch the explanation
    fetch(`/get_explanation/${taskId}`, {
        method: 'GET',
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Parse the JSON response
    })
    .then(data => {
        console.log('Task:', data.task);
        console.log('Response:', data.response);

        // Update the loading message
        updateLoadingMessage('Almost there!  Thanks for your patience.');

        // Update the UI with the data
        if (botMessageDiv) {
            botMessageDiv.textContent = data.response; // Update the content
        } else {
            console.error("Bot message div not found!");
            throw new Error("Bot message div not found!");
        }
    })
    .catch(error => {
        console.error('Error:', error);
        updateLoadingMessage('Something went wrong. Please try again.');
    })
    .finally(() => {
        hideLoading(); // Hide the loading overlay regardless of success or error
    });
}

function postExplanation() {
    const userMessage = document.getElementById("userMessage_explainer").value;
    const chatbox = document.querySelector(".chatbox_explainer");

    // Show the loading overlay and update the message
    showLoading();
    updateLoadingMessage('Processing your request. Please wait...');

    // Fetch the explanation
    fetch(`/post_explanation`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ userMessage: userMessage }), // Send the user message
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Parse the JSON response
    })
    .then(data => {
        console.log('Response:', data.response);

        // Update the loading message
        updateLoadingMessage('Almost there!  Thanks for your patience.');

        // Append the user's message as a separate div
        const userMessageDiv = document.createElement("div");
        userMessageDiv.className = "message user-message_explainer";
        userMessageDiv.textContent = userMessage;

        // Append the bot's response as a separate div
        const botMessageDiv = document.createElement("div");
        botMessageDiv.className = "message bot-message_explainer";
        botMessageDiv.textContent = data.response;

        // Add messages to the chatbox
        chatbox.appendChild(userMessageDiv);
        chatbox.appendChild(botMessageDiv);

        // Clear the input field
        document.getElementById("userMessage_explainer").value = "";
    })
    .catch(error => {
        console.error('Error:', error);
        updateLoadingMessage('Something went wrong. Please try again.');
    })
    .finally(() => {
        hideLoading(); // Hide the loading overlay regardless of success or error
    });
}
        
function closeExplanationChat() {
    const overlay = document.getElementById("overlay");
    const chatmodal = document.getElementById("chatbot_explainer");
    chatmodal.style.display = "none";
    overlay.style.display = "none";
}