from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from doctest import OutputChecker
import textwrap
from youtube_transcript_api import YouTubeTranscriptApi
import requests
import time



textFromApp = ""



api_key = "AIzaSyAZCYEesMFWF7qwbXZz_AI22zKoxMYzx_E" 

API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/158e2c5ca1cb98881c848241a12f8801/ai/run/"
headers = {"Authorization": "Bearer RWG-19eYHl7tWsHDSPCk7P1j65zHHH5c8yMXKDXm"}

persona = "You are a Learning assistant and educator designed to facilitate a comprehensive and interactive learning experience. you serve as a digital tutor, provide educational support and resources to users across a wide range of subjects. when given a prompt you should summeraize the data in into a collection of main points."

app = Flask(__name__)
CORS(app)

# Global variable to store the text
global_text = ""
getTextFromPageSummary = None

@app.route('/receive_text', methods=['POST'])
def receive_text():
    global global_text  # Declare to modify the global variable
    if request.is_json:
        data = request.get_json()
        global_text = data.get('text', '')  # Update global variable with received text
        return jsonify({"message": "Text received successfully!","text":global_text}), 200
    else:
        return jsonify({"error": "Request must be JSON"}), 400

@app.route('/')
def home():
    return render_template('index.html', text=global_text)

@app.route('/get_text')
def get_text():
    global global_text
    renderedText = getPageSummary(global_text)
    time.sleep(2)
    return jsonify({"text": renderedText})

if __name__ == '__main__':
    app.run(debug=True)


def getPageSummary(global_text):
    #This function reads a message from stdin and decodes it.


    outputs = []

    #make a method that recieves a google chrome native message and assigns the message to transcript
    transcript = global_text
    transcript_parts = textwrap.wrap(transcript, 4096)

    for part in transcript_parts:
        # Use the transcript as the user's message in the inputs for the run function
        inputs = [
            { "role": "system", "content":  persona},
            { "role": "user", "content": part}
        ]

    def run(model, inputs):
        input = { "messages": inputs }
        response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input)
        return response.json()
    
    output = run("@cf/meta/llama-2-7b-chat-int8", inputs)
    outputs.append(output['result']['response'])  # append the response to the outputs list

    outputs_str = ' '.join(outputs)

    inputs = [
        { "role": "system", "content": "You are a Learning assistant and educator. When given a list of points, you should identify and return the 10 most important points. Make sure you cover a wide array of points and not to focus only on one aspect." },
        { "role": "user", "content": outputs_str}
    ]

    final_output = run("@cf/meta/llama-2-7b-chat-int8", inputs)
    return final_output


