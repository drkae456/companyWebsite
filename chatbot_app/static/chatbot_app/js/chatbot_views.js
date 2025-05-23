// Tab functionality
function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    
    // Hide all tab content
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
        tabcontent[i].classList.remove("active");
    }
    
    // Remove active class from all tab buttons
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].classList.remove("active");
    }
    
    // Show the current tab and add active class to the button
    document.getElementById(tabName).style.display = "block";
    document.getElementById(tabName).classList.add("active");
    evt.currentTarget.classList.add("active");
}

// Enable buttons in the formatted response
document.addEventListener('DOMContentLoaded', function() {
    const formattedResponse = document.querySelector('.formatted-response');
    if (formattedResponse) {
        const buttons = formattedResponse.querySelectorAll('.suggestion-btn');
        buttons.forEach(button => {
            button.addEventListener('click', function() {
                const message = this.getAttribute('onclick').replace('sendMessage(\'', '').replace('\')', '');
                window.location.href = '?q=' + encodeURIComponent(message);
            });
        });
    }
    
    // Initialize chat functionality if we're on the chat page
    if (document.querySelector('.chat-container')) {
        initChat();
    }
});

// Chat functionality
function initChat() {
    // Session management
    let sessionId = localStorage.getItem('chatSessionId') || null;
    
    // DOM elements
    const chatBox = document.getElementById('chat-box');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const connectionStatus = document.getElementById('connection-status');
    
    // Initialize chat
    function initializeChat() {
        // Show connection status
        connectionStatus.innerText = 'Connected to HardHat Assistant';
        connectionStatus.classList.remove('connecting');
        connectionStatus.classList.add('connected');
        
        // Add welcome message
        addBotMessage("Hello! Welcome to Hardhat Enterprises. My name is HardHat Assistant. I am here to help you explore the world of Hardhat Enterprises.");
        
        // Add suggested questions
        addSuggestedQuestions();
    }
    
    // Function to add a message to the chat box
    function addMessage(messageObject, isLoadingHistory = false) {
        if (!chatBox) {
            chatBox = document.getElementById("chat-box");
        }
        if (!chatBox) {
            console.error("Chat box not found, cannot add message.");
            return;
        }
        const messageDiv = document.createElement('div');
        const isUser = messageObject.sender === 'user';
        const isBot = messageObject.sender === 'bot';
        const isIndicator = messageObject.sender === 'indicator';

        messageDiv.className = `message ${isUser ? 'user-message' : isBot ? 'bot-message' : 'typing-indicator'}`;

        if (isUser) {
            const prefix = `${currentUser.isLoggedIn ? currentUser.name : 'Guest'}: `;
            messageDiv.textContent = prefix + messageObject.text;
        } else if (isBot) {
            let formattedMessage = messageObject.text || "";
            
            // Check if the message contains a formatted response
            if (formattedMessage.includes('formatted-response')) {
                messageDiv.innerHTML = formattedMessage;
            } else {
                // Add bot prefix and format message
                const prefix = '<span class="bot-prefix">Hardhat Assistant:</span> ';
                formattedMessage = formattedMessage.replace(/\\n/g, '<br>');
                formattedMessage = formattedMessage.replace(/⸻/g, '<hr>');
                
                // Format emojis and special characters
                formattedMessage = formattedMessage.replace(/🟩|🟨|🟥/g, match => `<span class="difficulty-emoji">${match}</span>`);
                formattedMessage = formattedMessage.replace(/📘/g, '<span class="challenge-title">📘</span>');
                formattedMessage = formattedMessage.replace(/🔥/g, '<span class="points-emoji">🔥</span>');
                formattedMessage = formattedMessage.replace(/🔗/g, '<span class="link-emoji">🔗</span>');
                
                // Format links
                const pathRegex = /\/challenges\/detail\/(\d+)/g;
                formattedMessage = formattedMessage.replace(pathRegex, (match, id) => 
                    `<a href="${match}" class="challenge-link" target="_blank">Take Challenge</a>`
                );
                
                messageDiv.innerHTML = prefix + formattedMessage;
            }
            
            // Add click handlers for "Show more" buttons
            if (formattedMessage.includes('Show me more')) {
                const showMoreButtons = messageDiv.querySelectorAll('.action');
                showMoreButtons.forEach(button => {
                    button.addEventListener('click', () => {
                        const query = button.textContent.trim();
                        sendMessage(query);
                    });
                });
            }
        } else if (isIndicator) {
            messageDiv.id = 'typing-indicator';
            messageDiv.innerHTML = '<span class="typing-text">Hardhat Assistant typing</span><div class="typing-bubbles"><span></span><span></span><span></span></div>';
        }

        chatBox.appendChild(messageDiv);

        if ((isUser || isBot) && !isLoadingHistory) {
            messageObject.timestamp = messageObject.timestamp || Date.now();
            chatHistory.push(messageObject);
            saveChatHistory();
        }

        // Adjust scroll behavior based on the message type
        if (isBot) {
            // For bot messages, scroll to show the start of the message
            scrollToMessageStart(messageDiv);
        } else {
            // For user messages and typing indicators, scroll to bottom
            scrollChatToBottom();
        }
    }
    
    // Initialize interactive elements in formatted responses
    function initializeFormattedResponse(messageElement) {
        // Handle tables
        const tables = messageElement.querySelectorAll('.search-results-table');
        tables.forEach(table => {
            // Add hover effect to table rows
            const rows = table.querySelectorAll('tbody tr');
            rows.forEach(row => {
                row.addEventListener('mouseover', () => {
                    row.style.backgroundColor = '#f8f9fa';
                });
                row.addEventListener('mouseout', () => {
                    row.style.backgroundColor = '';
                });
            });
        });
        
        // Handle result titles
        const titles = messageElement.querySelectorAll('.result-title');
        titles.forEach(title => {
            title.addEventListener('click', (e) => {
                e.preventDefault();
                const text = title.textContent;
                messageInput.value = `Tell me more about ${text}`;
                messageInput.focus();
            });
        });
    }
    
    // Enhanced bot message handling
    function addBotMessage(message) {
        // Remove any existing typing indicator
        hideTypingIndicator();
        
        // Check if the message is a JSON string containing formatted content
        try {
            const messageData = JSON.parse(message);
            if (messageData.formatted_response) {
                addMessage(messageData, true);
                return;
            }
        } catch (e) {
            // Not JSON, continue with normal message
        }
        
        // Regular message handling
        addMessage(message, true);
    }
    
    // Add a user message
    function addUserMessage(message) {
        addMessage(message, false);
    }
    
    // Show typing indicator
    function showTypingIndicator() {
        console.log("Showing typing indicator in chatbot_views.js");
        if (!chatBox) {
            chatBox = document.getElementById("chat-box");
            console.log("Getting chat box element in views.js:", chatBox);
        }
        
        const typingIndicator = document.createElement('div');
        // Add both classes for better targeting
        typingIndicator.classList.add('message', 'typing-message');
        typingIndicator.id = 'typing-indicator';
        
        // Create a more direct structure for the typing indicator
        typingIndicator.innerHTML = `
            <div class="chat-bubble">
                <div class="typing">
                    <div class="dot"></div>
                    <div class="dot"></div>
                    <div class="dot"></div>
                </div>
            </div>
        `;
        
        chatBox.appendChild(typingIndicator);
        console.log("Typing indicator added to DOM in views.js:", typingIndicator);
        
        chatBox.scrollTop = chatBox.scrollHeight;
        
        // Debug check if indicator is visible after short delay
        setTimeout(() => {
            const indicator = document.getElementById('typing-indicator');
            console.log("Typing indicator after delay in views.js:", indicator);
            if (indicator) {
                console.log("Indicator styles in views.js:", window.getComputedStyle(indicator));
                const bubbleEl = indicator.querySelector('.chat-bubble');
                if (bubbleEl) {
                    console.log("Chat bubble styles in views.js:", window.getComputedStyle(bubbleEl));
                }
            }
        }, 100);
    }
    
    // Hide typing indicator
    function hideTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    // Add suggested questions
    function addSuggestedQuestions() {
        // Clear previous suggestions
        document.querySelectorAll('.suggested-questions').forEach(el => el.remove());
        const suggestionsDiv = document.createElement('div');
        suggestionsDiv.classList.add('suggested-questions');
        suggestionsDiv.innerHTML = `
            <p>Here are some things you can ask:</p>
            <button class="suggestion-btn" onclick="sendMessage('Tell me about AppAttack')">Tell me about AppAttack</button>
            <button class="suggestion-btn" onclick="sendMessage('What challenges are available?')">What challenges are available?</button>
            <button class="suggestion-btn" onclick="sendMessage('What is DeakinThreatmirror?')">What is Deakin Threatmirror?</button>
            <button class="suggestion-btn" onclick="sendMessage('Tell me about malware viz')">Tell me about malware visualization</button>
            <button class="suggestion-btn" onclick="sendMessage('What is PTGUI viz')">What is PTGUI?</button>
            <button class="suggestion-btn" onclick="sendMessage('What is smishing detection?')">What is smishing detection?</button>
            <button class="suggestion-btn" onclick="sendMessage('How can I upskill?')">How can I upskill?</button>
            <button class="suggestion-btn" onclick="sendMessage('Tell me about VR ')">Tell me about Deakin Cybersafe VR</button>
            <button class="suggestion-btn" onclick="sendMessage('Tell me about announcments ')">Tell me about the latest announcements</button>
        `;
        chatBox.appendChild(suggestionsDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
    
    // Enhanced send message function
    async function sendMessage(message = null) {
        const messageText = message || messageInput.value.trim();
        
        if (!messageText) return;
        
        // Add user message to chat
        addUserMessage(messageText);
        
        // Clear input if using the input field
        if (!message) {
            messageInput.value = '';
        }
        
        // Show typing indicator and record start time
        showTypingIndicator();
        const typingStartTime = Date.now();
        
        try {
            const response = await fetch(`/chatbot/api/session/${sessionId}/message/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    message: messageText,
                    user_info: {
                        is_authenticated: false,
                        username: 'Guest'
                    }
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.status === 'error') {
                throw new Error(data.message || 'Unknown error occurred');
            }
            
            // Calculate time elapsed since showing typing indicator
            const elapsedTime = Date.now() - typingStartTime;
            const minTypingTime = 1800; // 1.8 seconds in milliseconds
            
            // If response came back too quickly, wait until 1.8 seconds have passed
            const remainingTime = Math.max(0, minTypingTime - elapsedTime);
            
            // Add bot response after ensuring typing indicator has shown for at least 1.8 seconds
            setTimeout(() => {
                // Hide typing indicator after delay
                hideTypingIndicator();
                if (data.formatted_response) {
                    // Handle formatted response
                    addBotMessage(JSON.stringify({
                        formatted_response: data.formatted_response
                    }));
                } else {
                    // Handle regular response
                    addBotMessage(data.response);
                }
                // Show suggestion bubbles after each bot response
                addSuggestedQuestions();
            }, remainingTime);
            
        } catch (error) {
            console.error('Error:', error);
            
            // Calculate time elapsed since showing typing indicator
            const elapsedTime = Date.now() - typingStartTime;
            const minTypingTime = 1800; // 1.8 seconds in milliseconds
            
            // If error occurred too quickly, still wait until 1.8 seconds total
            if (elapsedTime < minTypingTime) {
                setTimeout(() => {
                    handleError(error);
                }, minTypingTime - elapsedTime);
            } else {
                handleError(error);
            }
        }
    }
    
    // Error handling function
    function handleError(error) {
        // Ensure typing indicator is hidden
        hideTypingIndicator();
        
        const errorMessage = error.message === 'Failed to fetch'
            ? `<div class="error-message">I'm having trouble connecting to the server. Please check your internet connection and try again.</div>`
            : `<div class="error-message">I encountered an error processing your message. Please try again.</div>`;
        
        addBotMessage(errorMessage);
        // Show suggestion bubbles after error response
        addSuggestedQuestions();
        
        // Update connection status
        updateConnectionStatus('error');
    }
    
    // Update connection status
    function updateConnectionStatus(status) {
        const statusElement = document.getElementById('connection-status');
        if (!statusElement) return;
        
        statusElement.classList.remove('connecting', 'connected', 'error');
        
        switch (status) {
            case 'connecting':
                statusElement.innerText = 'Connecting to HardHat Assistant...';
                statusElement.classList.add('connecting');
                break;
            case 'connected':
                statusElement.innerText = 'Connected to HardHat Assistant';
                statusElement.classList.add('connected');
                break;
            case 'error':
                statusElement.innerText = 'Connection error. Please try again.';
                statusElement.classList.add('error');
                // Attempt to reconnect after 30 seconds
                setTimeout(() => {
                    if (statusElement.classList.contains('error')) {
                        updateConnectionStatus('connected');
                    }
                }, 30000);
                break;
        }
    }
    
    // Event listeners
    sendButton.addEventListener('click', () => sendMessage());
    
    messageInput.addEventListener('keypress', event => {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Make sendMessage available globally
    window.sendMessage = sendMessage;
    
    // Initialize the chat
    initializeChat();
}

// Add styles for the new formatting
const styles = `
.challenge-title {
    font-size: 1.2em;
    margin-right: 5px;
}

.difficulty-emoji {
    font-size: 1.1em;
    margin-right: 3px;
}

.points-emoji {
    color: #ff6b6b;
    margin-right: 3px;
}

.link-emoji {
    color: #0366d6;
    margin-right: 3px;
}

.challenge-link {
    color: #0366d6;
    text-decoration: none;
    font-weight: 500;
}

.challenge-link:hover {
    text-decoration: underline;
}

hr {
    border: none;
    border-top: 1px solid #e0e0e0;
    margin: 10px 0;
}

.bot-message .action {
    color: #0366d6;
    cursor: pointer;
    margin-top: 5px;
}

.bot-message .action:hover {
    text-decoration: underline;
}
`;

// Add the styles to the document
const styleSheet = document.createElement("style");
styleSheet.textContent = styles;
document.head.appendChild(styleSheet); 