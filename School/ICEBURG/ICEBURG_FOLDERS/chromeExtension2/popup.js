document.getElementById('extractText').addEventListener('click', () => {
    // Query the current active tab
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        // Send a message to the content script of the active tab
        chrome.tabs.sendMessage(tabs[0].id, {action: "extractText"});
    });
    window.open('http://127.0.0.1:5000/', '_blank');
});