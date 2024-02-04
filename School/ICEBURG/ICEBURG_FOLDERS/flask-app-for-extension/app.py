from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import requests
import textwrap
import time
import re
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import requests


API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/158e2c5ca1cb98881c848241a12f8801/ai/run/"
headers = {"Authorization": "Bearer RWG-19eYHl7tWsHDSPCk7P1j65zHHH5c8yMXKDXm"}
persona = "You are a Learning assistant built to do precisely one thing. Your task is to take the incoming text and break it down in to key points. do not refer to anything without using the objects specific title for example format responses like this 'How does the book, essential calculus by john taylor...'.  each point should have at least 6 words and be descriptive. avoid arbitrary words like 'it and 'the book' please refer to nouns and pronouns specifically with their appropriate name and title. these key points need to be specific and have context so we can later talk about them more and know what the point is reffering to. do not include arbitrary information such as mentioning an author or figure without mentioning their name or put anything like homme, index licensing, references, intended use, or anything that does not provide context. Your only response to my prompt should be an ordered list of the most relevent and most important topics. aside from this ordered list there should be no other text output"


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'  # It's important for SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

global_text_screen_cap = ""  # Global variable to store the text
global_text_url = "" 
global_text_snip = "" 

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/snippetMode')
def snippet():
    return render_template('snippetMode.html')

@app.route('/youtubeWizard')
def youtubeWizard():
    return render_template('youtubeWizard.html')

@app.route('/receive_text', methods=['POST'])
def receive_text():
    global global_text_screen_cap
    if request.is_json:
        data = request.get_json()
        global_text_screen_cap = data.get('text', '')
        processed_text = myAIdef2(global_text_screen_cap)  # Process text with AI before broadcasting
        #time.sleep(2)  # Consider async handling instead of sleep
        
        return jsonify({"message": "Text processed and broadcasted successfully!", "text": processed_text}), 200
    else:
        return jsonify({"error": "Request must be JSON"}), 400
    

@app.route('/receive_text_url', methods=['POST'])
def receive_text_url():
    global global_text_url
    if request.is_json:
        data = request.get_json()
        global_text_url = data.get('text', '')
        processed_text = processVideotranscript(global_text_url)  
        #time.sleep(2)  # Consider async handling instead of sleep
        
        return jsonify({"message": "Text processed and broadcasted successfully!", "text": processed_text}), 200
    else:
        return jsonify({"error": "Request must be JSON"}), 400
    
    
@app.route('/receive_text_snip_text', methods=['POST'])
def receive_text_snip_text():
    global global_text_snip
    if request.is_json:
        data = request.get_json()
        global_text_snip = data.get('text', '')
        processed_text = myAIdef(global_text_snip)  # change def to give more on text input
        #time.sleep(2)  # Consider async handling instead of sleep
        
        return jsonify({"message": "Text processed and broadcasted successfully!", "text": processed_text}), 200
    else:
        return jsonify({"error": "Request must be JSON"}), 400

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('card_clicked_index')
def handle_event(data):
    print('Received data:', data)
    generateAIresponseToClick(data['text'])
    # Process the data as needed

@socketio.on('card_clicked_youtube')
def handle_event(data):
    print('Received data:', data)
    # Process the data as needed

if __name__ == '__main__':
    socketio.run(app, debug=True)

# Define the run function outside myAIdef to make it reusable
def run(model, inputs, headers):
    input_data = {"messages": inputs}
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input_data)
    return response.json()


def myAIdef(text_to_process):
 
    # Process the text with AI
    inputs = [
        {"role": "system", "content": persona},
        {"role": "user", "content": text_to_process}
    ]

    # Call the AI model
    output = run("@cf/meta/llama-2-7b-chat-int8", inputs, headers)
    
    # Assuming the AI response structure is correctly accessed
    try:
        ai_response = output['result']['response']
    except KeyError:
        ai_response = "Failed to process text."

    print(text_to_process)

    print(ai_response)  # For debugging
    print(type(ai_response))
    socketio.emit('text_update_2', {'text': ai_response}, broadcast=True)

    return ai_response

def myAIdef2(text_to_process):
    transcript_parts = textwrap.wrap(text_to_process, 4000)


    #runs the split up text
    for part in transcript_parts:
        # Use the transcript as the user's message in the inputs for the run function
        inputs = [
            { "role": "system", "content":  persona},
            { "role": "user", "content": part}
        ]
    outputs = []
    output = run("@cf/meta/llama-2-7b-chat-int8", inputs, headers)
    outputs.append(output['result']['response'])  # append the response to the outputs list

    # Join the outputs into a single string for the final run
    outputs_str = ' '.join(outputs)


    #final run. might need to refine worker prompt
    inputs = [
        { "role": "system", "content": "You are being given a list of topics and key points, you should identify and return the 10 most important topics that the user may want to know more about. You must return a list and only a list, no other text aside from the list elements" },
        { "role": "user", "content": outputs_str}
    ]

    final_output = run("@cf/meta/llama-2-7b-chat-int8", inputs, headers)
    

    # Extract the response text
    text = final_output['result']['response']

    # Initialize an empty list to hold the cleaned points
    cleaned_points = []

    # Split the text into lines and process each line
    for line in text.split('\n'):
        # Check if the line starts with a number followed by a period (indicative of a point)
        if line.strip().startswith(tuple(f"{i}." for i in range(1, 11))):
            # Remove the numbering and any leading/trailing whitespace
            point = line.split('. ', 1)[-1].strip()
            cleaned_points.append(point)
    socketio.emit('text_update', {'text': cleaned_points}, broadcast=True)



    print(cleaned_points)



#imports


#obtain transcript
def get_transcript_from_url(video_url):
    # Extract video id from URL
    video_id = video_url.split('watch?v=')[-1]
    
    # Get the transcript
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    
    # Combine each line of the transcript into a single string
    transcript_text = ' '.join([line['text'] for line in transcript])
    
    return transcript_text

def processVideotranscript(url):
    #method to call transcript. make sure to change ur to the users input
    transcript = get_transcript_from_url(url) #TODO create web socket input for video url

    # Split the transcript into chunks of 4096 characters
    transcript_parts = textwrap.wrap(transcript, 4000)


    #runs the split up text
    for part in transcript_parts:
        # Use the transcript as the user's message in the inputs for the run function
        inputs = [
            { "role": "system", "content":  persona},
            { "role": "user", "content": part}
        ]
    outputs = []
    output = run("@cf/meta/llama-2-7b-chat-int8", inputs, headers)
    outputs.append(output['result']['response'])  # append the response to the outputs list

    # Join the outputs into a single string for the final run
    outputs_str = ' '.join(outputs)


    #final run. might need to refine worker prompt
    inputs = [
        { "role": "system", "content": "You are being given a list of topics, you should identify and return the 10 most important topics that the user may want to know more about. You must return a list and only a list, no other text aside from the list elements" },
        { "role": "user", "content": outputs_str}
    ]

    final_output = run("@cf/meta/llama-2-7b-chat-int8", inputs, headers)
    

    # Extract the response text
    text = final_output['result']['response']

    # Initialize an empty list to hold the cleaned points
    cleaned_points = []

    # Split the text into lines and process each line
    for line in text.split('\n'):
        # Check if the line starts with a number followed by a period (indicative of a point)
        if line.strip().startswith(tuple(f"{i}." for i in range(1, 11))):
            # Remove the numbering and any leading/trailing whitespace
            point = line.split('. ', 1)[-1].strip()
            cleaned_points.append(point)
    socketio.emit('text_update_youtube', {'text': cleaned_points}, broadcast=True)



    print(cleaned_points)

def generateAIresponseToClick(text):
        # Process the text with AI
    inputs = [
        {"role": "system", "content": "Give me more information on this topic."},
        {"role": "user", "content": text}
    ]

    # Call the AI model
    output = run("@cf/meta/llama-2-7b-chat-int8", inputs, headers)
    
    # Assuming the AI response structure is correctly accessed
    try:
        ai_response = output['result']['response']
    except KeyError:
        ai_response = "Failed to process text."

    print(text)

    print(ai_response)  # For debugging
    print(type(ai_response))
    socketio.emit('text_update_2', {'text': ai_response}, broadcast=True)

    return ai_response
