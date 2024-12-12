// Handle Context Setting: Capture context based on the input type (paragraph, URL, file, or audio).


document.getElementById("setContextButton").addEventListener("click", async () => {
    const paragraph = document.getElementById("paragraphContext").value.trim();
    const url = document.getElementById("urlContext").value.trim();
    const file = document.getElementById("fileUpload").files[0];
    const audio = document.getElementById("audioUpload").files[0];
    let context = "";

    // Handle Paragraph Input
    if (paragraph) {
        try {
            const response = await fetch("/chat/set_paragraph_context/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ paragraph }),
            });
            const data = await response.json();
            if (response.ok) {
                context = data.context;
                localStorage.setItem("context", context);
                console.log("Paragraph context stored:", context);
                alert("Paragraph context set successfully!");
            } else {
                alert("Error setting paragraph context: " + data.error);
            }
        } catch (error) {
            console.error("Error setting paragraph context:", error);
            alert("Failed to set paragraph context.");
        }
        return;
    }

    // Handle URL Input
    if (url) {
        try {
            const response = await fetch("/chat/extract_text_from_url/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ url }),
            });
            const data = await response.json();
            if (response.ok) {
                context = data.text;
                localStorage.setItem("context", context);
                console.log("URL context stored:", context);
                alert("URL context set successfully!");
            } else {
                alert("Error extracting text from URL: " + data.error);
            }
        } catch (error) {
            console.error("Error extracting text from URL:", error);
            alert("Failed to set URL context.");
        }
        return;
    }

    // Handle File Upload
    if (file) {
        try {
            const formData = new FormData();
            formData.append("file", file);

            const response = await fetch("/chat/extract_text_from_file/", {
                method: "POST",
                body: formData,
            });
            const data = await response.json();
            if (response.ok) {
                context = data.text;
                localStorage.setItem("context", context);
                console.log("File context stored:", context);
                alert("File context set successfully!");
            } else {
                alert("Error extracting text from file: " + data.error);
            }
        } catch (error) {
            console.error("Error extracting text from file:", error);
            alert("Failed to set file context.");
        }
        return;
    }

    // Handle Audio Upload
    if (audio) {
        try {
            const formData = new FormData();
            formData.append("audio", audio);

            const response = await fetch("/chat/transcribe_audio/", {
                method: "POST",
                body: formData,
            });
            const data = await response.json();
            if (response.ok) {
                context = data.text;
                localStorage.setItem("context", context);
                console.log("Audio context stored:", context);
                alert("Audio context set successfully!");
            } else {
                alert("Error transcribing audio: " + data.error);
            }
        } catch (error) {
            console.error("Error transcribing audio:", error);
            alert("Failed to set audio context.");
        }
        return;
    }

    // No Valid Input Provided
    alert("Please provide a valid context (paragraph, URL, file, or audio).");
    console.error("No valid context provided.");
});



// Handle Question Submission: Send the question and context to the backend and display the response dynamically.
document.getElementById("askQuestionButton").addEventListener("click", async () => {
    const question = document.getElementById("questionInput").value.trim();
    const context = localStorage.getItem("context");

    if (!context) {
        alert("Please set the context first.");
        console.error("No context found in localStorage.");
        return;
    }

    if (question === "") {
        alert("Please enter a question.");
        console.error("No question entered.");
        return;
    }

    try {
        console.log("Sending question and context:", { question, context });

        const response = await fetch("/chat/process_query/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question, context }),
        });

        const data = await response.json();
        console.log("Response from backend:", data);

        if (response.ok) {
            const chatArea = document.getElementById("chatArea");
            chatArea.innerHTML += `
                <div class="chat-message">
                    <div class="user-message"><strong>User:</strong> ${question}</div>
                    <div class="response"><strong>Bot:</strong> ${data.bot_response}</div>
                </div>
            `;
            document.getElementById("questionInput").value = ""; // Clear input
        } else {
            alert("Error: " + data.error);
        }
    } catch (error) {
        console.error("Error during fetch:", error);
        alert("An error occurred.");
    }
});



// Load Previous Chats: Fetch and display previous chats in the sidebar.

window.addEventListener("load", async () => {
    try {
        const response = await fetch("/chat/fetch_chat_history/");
        if (response.status === 403) {
            alert("Please log in to view your chat history.");
            window.location.href = "/login/";
            return;
        }

        const data = await response.json();
        const chatList = document.getElementById("previousChatsList");
        chatList.innerHTML = ""; // Clear existing chats

        data.chat_history.forEach(chat => {
            const chatItem = document.createElement("li");
            chatItem.className = "list-group-item";
            chatItem.innerHTML = `
                <a href="#" onclick="loadChat('${chat.id}')">
                    ${chat.user_input.slice(0, 20)}...
                </a>`;
            chatList.appendChild(chatItem);
        });
    } catch (error) {
        console.error("Error loading chat history:", error);
    }
});


async function loadChat(chatId) {
    try {
        const response = await fetch(`/chat/view/${chatId}/`);
        if (!response.ok) {
            throw new Error("Failed to fetch chat details");
        }
        const data = await response.json();

        const chatArea = document.getElementById("chatArea");
        chatArea.innerHTML = `
            <div class="chat-message">
                <div class="user-message"><strong>User:</strong> ${data.user_input}</div>
                <div class="response"><strong>Bot:</strong> ${data.bot_response}</div>
            </div>
        `;
    } catch (error) {
        console.error("Error loading chat:", error);
    }
}

