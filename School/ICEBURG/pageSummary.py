from doctest import OutputChecker
import textwrap

from youtube_transcript_api import YouTubeTranscriptApi
import requests
import transcript_Test
import app

textFromApp = ""



api_key = "AIzaSyAZCYEesMFWF7qwbXZz_AI22zKoxMYzx_E" 

API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/158e2c5ca1cb98881c848241a12f8801/ai/run/"
headers = {"Authorization": "Bearer RWG-19eYHl7tWsHDSPCk7P1j65zHHH5c8yMXKDXm"}

persona = "You are a Learning assistant and educator designed to facilitate a comprehensive and interactive learning experience. you serve as a digital tutor, provide educational support and resources to users across a wide range of subjects. when given a prompt you should summeraize the data in into a collection of main points."
#This function reads a message from stdin and decodes it.
def run(model, inputs):
    input = { "messages": inputs }
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input)
    return response.json()


outputs = []

#make a method that recieves a google chrome native message and assigns the message to transcript
transcript = transcript_Test.get_transcript()
transcript_parts = textwrap.wrap(transcript, 4096)

for part in transcript_parts:
    # Use the transcript as the user's message in the inputs for the run function
    inputs = [
        { "role": "system", "content":  persona},
        { "role": "user", "content": part}
    ]


output = run("@cf/meta/llama-2-7b-chat-int8", inputs)
outputs.append(output['result']['response'])  # append the response to the outputs list

outputs_str = ' '.join(outputs)

inputs = [
    { "role": "system", "content": "You are a Learning assistant and educator. When given a list of points, you should identify and return the 10 most important points. Make sure you cover a wide array of points and not to focus only on one aspect." },
    { "role": "user", "content": outputs_str}
]

final_output = run("@cf/meta/llama-2-7b-chat-int8", inputs)
print(final_output)





