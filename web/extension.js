// content_script.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "extractData") {
      // Replace the following lines with actual data extraction logic
      const data = {
        sourceIP: document.querySelector("#source-ip")?.innerText || "N/A",
        sourcePort: document.querySelector("#source-port")?.innerText || "N/A",
        // Add other fields similarly
      };
  
      sendResponse(data);
    }
  });
  