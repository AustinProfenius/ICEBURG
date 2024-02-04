from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pageSummary

app = Flask(__name__)
CORS(app)

# Global variable to store the text
global_text = ""

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
    sendTextToApp(global_text)
    getTextFromPageSummary()
    return jsonify({"text": global_text})

if __name__ == '__main__':
    app.run(debug=True)

def sendTextToApp(global_text):
    pageSummary.textFromApp = global_text

def getTextFromPageSummary():
    global global_text
    global_text = pageSummary.final_output

    
