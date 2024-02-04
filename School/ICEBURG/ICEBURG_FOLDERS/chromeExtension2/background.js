// This function listens for a click on your extension's icon.
chrome.action.onClicked.addListener((tab) => {
    console.log("icon Clicked");
    // Send a message to the content script in the active tab
    chrome.tabs.sendMessage(tab.id, {action: "extractText"}, function(response) {
      if (chrome.runtime.lastError) {
          // Handle any errors that might occur
          console.log(chrome.runtime.lastError.message);
      } else if (response) {
          const allText = response.text;
          // Now you can use the extracted text. For example, log it:
            
          console.log(allText);
          console.log("text printing from background.js")

  
          // If you want to open a new tab and do something with the text:
          // You might need to pass it to the new tab via storage or directly if you control the new page
          // Example: Opening a new tab with a URL that includes part of the text (be mindful of URL length limits)
          // chrome.tabs.create({url: 'https://yourprocessingpage.com/?data=' + encodeURIComponent(allText)});
      }
    });
  });

  // background.js
/*chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    console.log("background on message BEFORE request action");
    if (request.action === "sendNativeMessage") {
        console.log("background on message after request action");

        chrome.runtime.sendNativeMessage('com.duntz_corp.extract_text', {text: request.data.text},
            function(response) {
                //console.log("Received response: ", request.data.text); 
                console.log("response received from pyton: ", response);
                // Optional: Send a response back to the content script
                //sendResponse({response: "Message sent to Python script"});
            });

            chrome.runtime.sendNativeMessage('com.duntz_corp.extract_text', {text: "Test message"}, function(response) {
                if (chrome.runtime.lastError) {
                    console.error("Error sending message:", chrome.runtime.lastError.message);
                    return;
                }
                console.log("Received response from Python:", response);
            });
        // Return true to indicate that you will send a response asynchronously
        return true;
    }
});*/



 