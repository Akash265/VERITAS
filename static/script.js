function analyzeComment() {
  var comment = document.getElementById('commentInput').value;
  alert('Funtion is called');
  // Send the comment to the server for analysis
  fetch('/analyze', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ comment: comment })
  })
  .then(response => response.json())
  .then(data => {
    // Display the analysis result in a pop-up
    alert('Analysis Result:\n' + data.analysis);
  })
  .catch(error => {
    console.error('Error:', error);
    alert('An error occurred during analysis.');
  });
}
