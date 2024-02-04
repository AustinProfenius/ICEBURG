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
    // Query the current active tab
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        // Send a message to the content script of the active tab
        chrome.tabs.sendMessage(tabs[0].id, {action: "extractText"}); //change extract screen 
    });
    window.open('http://127.0.0.1:5000/youtubeWizard', '_blank');
});

const ws = new WebSocket("ws://localhost:3000")
ws.addEventListener("open", () =>{
  console.log("connected");
});