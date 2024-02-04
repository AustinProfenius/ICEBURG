from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import requests
import textwrap
import time

API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/158e2c5ca1cb98881c848241a12f8801/ai/run/"
headers = {"Authorization": "Bearer RWG-19eYHl7tWsHDSPCk7P1j65zHHH5c8yMXKDXm"}
persona = "You are a Learning assistant built to do precisely one thing. Your task is to take the incoming text and break it down in to key points. Your only response to my prompt should be an ordered list of the most relevent and most important topics. aside from this ordered list there should be no other text output"


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'  # It's important for SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

global_text = ""  # Global variable to store the text

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
    global global_text
    if request.is_json:
        data = request.get_json()
        global_text = data.get('text', '')
        processed_text = myAIdef(global_text)  # Process text with AI before broadcasting
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
    socketio.emit('text_update', {'text': ai_response}, broadcast=True)

    return ai_response
