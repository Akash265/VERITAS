import detoxify
import requests
from bs4 import BeautifulSoup

from flask import Flask, render_template, request, jsonify
import os, io
from google.cloud import vision
from distutils.log import debug
from fileinput import filename
from flask import *  


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

@app.route('/analyseImage', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        f.save(f.filename)  
        
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'client_file_vision_ai.json'
        client = vision.ImageAnnotatorClient()
    
        path = os.path.abspath(f'.\{f.filename}')
        with io.open(path, "rb") as image_file:
            content = image_file.read()


        image = vision.Image(content=content)
        nsfwResponse = client.safe_search_detection(image=image)
        safe = nsfwResponse.safe_search_annotation

        likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                    'LIKELY', 'VERY_LIKELY')
        
        adult = likelihood_name[safe.adult]
        spoof = likelihood_name[safe.spoof]
        violence = likelihood_name[safe.violence]
        racy = likelihood_name[safe.racy]
        negativeList = ['UNLIKELY', 'POSSIBLE',
                    'LIKELY', 'VERY_LIKELY']
        
        os.remove(f.filename)
        result = "This is cyberbullying material"
        
        for i in range(4):
            if adult == negativeList[i]:
                return jsonify({'analysis': result})
            if spoof == negativeList[i]:
                return jsonify({'analysis': result})
            if violence == negativeList[i]:
                return jsonify({'analysis': result})
            if racy == negativeList[i]:
                return jsonify({'analysis': result})
            
        return jsonify({'analysis': "This is not cyberbullying material"})

if __name__ == '__main__':
    app.run(debug=True)


