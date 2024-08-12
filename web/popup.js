document.addEventListener('DOMContentLoaded', function() {
  const resultElement = document.getElementById('result');
  const checkButton = document.getElementById('check-button');
  const inputElement = document.getElementById('features-input');

  checkButton.addEventListener('click', async () => {
    const features = inputElement.value;
    
    try {
      const response = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ features: JSON.parse(features) }),
      });

      if (response.ok) {
        const result = await response.json();
        // Format the JSON result
        const formattedResult = Object.entries(result).map(([model, preds]) => {
          const predictions = preds.map(pred => `Prediction: ${pred}`).join('<br/>');
          return `<strong>${model}:</strong><br/>${predictions}`;
        }).join('<br/><br/>');
        
        resultElement.innerHTML = formattedResult;
      } else {
        resultElement.innerHTML = `Error: ${response.statusText}`;
      }
    } catch (error) {
      resultElement.innerHTML = `Error: ${error.message}`;
    }
  });
});
