
/*chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "extractText") {
      extractTextAsync().then(text => {
        sendResponse({text: text});
        console.log(text);
      }).catch(error => {
        console.error("Error extracting text:", error);
        sendResponse({error: error.toString()});
      })
      // Must return true to indicate you're sending a response asynchronously
      return true;
    }
  });*/


  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "extractText") {
        // Extract text here
        const extractedText = document.body.innerText; // Simple example of text extraction
        sendResponse({extractedText: extractedText});
        // Send the extracted text to your Flask app
        fetch('http://127.0.0.1:5000/receive_text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({text: extractedText}),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // Use sendResponse to send success back to the sender, if needed
            sendResponse({success: true, data: data});
        })
        .catch((error) => {
            console.error('Error:', error);
            sendResponse({success: false, error: error.toString()});
        });

        // Must return true to indicate you're sending a response asynchronously
        return true;
    }
    // Optionally, handle other actions here
});




// In content.js or other scripts intended to receive messages
/*chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {

    // Handle message
    console.log(message);
    return true; // Keep the message channel open for async response
});*/

  /*function extractTextAsync() {
    return new Promise((resolve, reject) => {
      try {
        // Synchronously getting all text from the webpage
        const allText = document.body.innerText;
        resolve(allText); // Resolving the promise with the text
      } catch (error) {
        reject(error); // Rejecting the promise if there's an error
      }
    });
  }
  */