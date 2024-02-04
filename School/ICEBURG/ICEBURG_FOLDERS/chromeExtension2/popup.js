document.getElementById('extractText').addEventListener('click', () => {
    // Query the current active tab
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        // Send a message to the content script of the active tab
        chrome.tabs.sendMessage(tabs[0].id, {action: "extractText"});
    });
    window.open('http://127.0.0.1:5000/', '_blank');
});

document.getElementById('snippetMode').addEventListener('click', () => {
    // Query the current active tab
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        // Send a message to the content script of the active tab
        chrome.tabs.sendMessage(tabs[0].id, {action: "extractText"}); //change extract screen after evan is done
    });
    window.open('http://127.0.0.1:5000/snippetMode', '_blank');
});






document.getElementById('youtubeWizard').addEventListener('click', () => {
    var inputText = document.getElementById('youtubeURL').value; // Assuming 'youtubeURL' is the ID of your input field in popup.html
    console.log(inputText); // Log or handle the URL as needed

    // Send the URL to the Flask app
    fetch('http://127.0.0.1:5000/receive_text_url', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({text: inputText}),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });

    window.open('http://127.0.0.1:5000/youtubeWizard', '_blank');
});



const ws = new WebSocket("ws://localhost:3000")
ws.addEventListener("open", () =>{
  console.log("connected");
});