// Handle Context Setting: Capture context based on the input type (paragraph, URL, file, or audio).


document.getElementById("setContextButton").addEventListener("click", async () => {
    const paragraph = document.getElementById("paragraphContext").value;
    const url = document.getElementById("urlContext").value;
    const file = document.getElementById("fileUpload").files[0];
    const audio = document.getElementById("audioUpload").files[0];

    let context = "";

    if (paragraph) {
        context = paragraph;
    } else if (url) {
        // Send URL to the backend for text extraction
        const response = await fetch("/chat/extract_text_from_url/", {
            method: "POST",
            body: JSON.stringify({ url }),
            headers: { "Content-Type": "application/json" },
        });
        const data = await response.json();
        context = data.text;
    } else if (file) {
        // Upload file to backend for processing
        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch("/chat/extract_text_from_file/", {
            method: "POST",
            body: formData,
        });
        const data = await response.json();
        context = data.text;
    } else if (audio) {
        // Upload audio to backend for transcription
        const formData = new FormData();
        formData.append("audio", audio);

        const response = await fetch("/chat/transcribe_audio/", {
            method: "POST",
            body: formData,
        });
        const data = await response.json();
        context = data.text;
    }

    alert("Context set successfully!");
    // Optionally, store the context for subsequent questions
});


// Handle Question Submission: Send the question and context to the backend and display the response dynamically.

document.getElementById("askQuestionButton").addEventListener("click", async () => {
    const question = document.getElementById("questionInput").value;
    const context = ""; // Retrieve the context from where it was stored

    const response = await fetch("/chat/process_query/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ question, context }),
    });

    const data = await response.json();
    const chatArea = document.getElementById("chatArea");

    chatArea.innerHTML += `
        <div class="chat-message">
            <div class="user-message">User: ${question}</div>
            <div class="response">Bot: ${data.bot_response}</div>
        </div>
    `;

    document.getElementById("questionInput").value = "";
});

// Load Previous Chats: Fetch and display previous chats in the sidebar.

window.addEventListener("load", async () => {
    const response = await fetch("/chat/fetch_chat_history/");
    const data = await response.json();

    const chatList = document.getElementById("previousChatsList");
    data.chat_history.forEach(chat => {
        const chatItem = document.createElement("li");
        chatItem.className = "list-group-item";
        chatItem.innerHTML = `<a href="#" onclick="loadChat('${chat.id}')">${chat.user_input.slice(0, 20)}...</a>`;
        chatList.appendChild(chatItem);
    });
});

async function loadChat(chatId) {
    const response = await fetch(`/chat/view/${chatId}/`);
    const data = await response.json();

    const chatArea = document.getElementById("chatArea");
    chatArea.innerHTML = `
        <div class="chat-message">
            <div class="user-message">User: ${data.user_input}</div>
            <div class="response">Bot: ${data.bot_response}</div>
        </div>
    `;
}
