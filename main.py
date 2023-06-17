import detoxify
import requests
from bs4 import BeautifulSoup

from flask import Flask, render_template, request, jsonify


app = Flask(__name__)

# Load the pre-trained model
model = detoxify.Detoxify("original")


# Function to detect hateful speech in Instagram chat and comments
def analyze_comment(text):
    # Use the model to classify the text
    predictions = model.predict(text)
    
    # Get the probability of toxic content
    score = max(predictions)

    # Return True if the text is classified as hateful, False otherwise
    if predictions[score] > 0.5:
        return f"{score} detected"
    else:
        return f"No problem detected"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    comment = request.json['comment']
    print(comment)
    analysis_result = analyze_comment(comment)
    return jsonify({'analysis': analysis_result})

if __name__ == '__main__':
    app.run(debug=True)


