
def getPageSummary(global_text):
    #This function reads a message from stdin and decodes it.


    outputs = []

    #make a method that recieves a google chrome native message and assigns the message to transcript
    transcript = global_text
    transcript_parts = "heres some random words for ya bitch"
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

def transcript_Test(global_text):
        
    api_key = "AIzaSyAZCYEesMFWF7qwbXZz_AI22zKoxMYzx_E"  # replace it with your API key
    #youtube = build('youtube', 'v3', developerKey=api_key)

    # Cloudflare AI
    API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/158e2c5ca1cb98881c848241a12f8801/ai/run/"
    headers = {"Authorization": "Bearer RWG-19eYHl7tWsHDSPCk7P1j65zHHH5c8yMXKDXm"}

    persona = "You are a Learning assistant and educator designed to facilitate a comprehensive and interactive learning experience. you serve as a digital tutor, provide educational support and resources to users across a wide range of subjects. when given a prompt you should summeraize the data in into a collection of main points."

    def extract_numbered_lines(text):
        # Split the text into lines
        lines = text.split('\n')

        # Create a list of numbered lines
        numbered_lines = [line for line in lines if re.match(r'\d+\.', line)]

        return numbered_lines

    def replace_escaped_characters(text):
        replacements = {
            "\\'": "'",
            '\\"': '"',
            '\\n': '\n',
            '\\t': '\t',
            '\\b': '\b',
            '\\r': '\r',
            '\\f': '\f',
            '\\\\': '\\',
            "\\": ""
            
            
        }
        for escaped, unescaped in replacements.items():
            text = text.replace(escaped, unescaped)
        return text

    def run(model, inputs):
        input = { "messages": inputs }
        response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input)
        return response.json()

    #def get_transcript(video_url):
        # Extract video id from URL
        #video_id = video_url.split('watch?v=')[-1]
        
        # Get the transcript
        #transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Combine each line of the transcript into a single string
        #transcript_text = ' '.join([line['text'] for line in transcript])
        
        #return transcript_text



    outputs = []
    # Get the transcript from a YouTube video URL
    #transcript = get_transcript('https://www.youtube.com/watch?v=nOF4MMokuzM&ab_channel=SVGProductions')

    # Split the transcript into chunks of 4096 characters
    if global_text == None:
        transcript_parts = "a bunch of random text a bunch of random text a bunch of random text a bunch of random text a bunch of random text"
    else:
        transcript_parts = textwrap.wrap(global_text, 4096)


    #for part in transcript_parts:
        # Use the transcript as the user's message in the inputs for the run function
    inputs = [
        { "role": "system", "content":  persona},
        { "role": "user", "content": global_text}
    ]

    output = run("@cf/meta/llama-2-7b-chat-int8", inputs)
    outputs.append(output['result']['response'])  # append the response to the outputs list

    # Join the outputs into a single string
    outputs_str = ' '.join(outputs)

    #here
    #outputs_str = replace_escaped_characters(outputs_str)

    #numbered_lines = extract_numbered_lines(outputs_str)

    inputs = [
        { "role": "system", "content": "You are a Learning assistant and educator. When given a list of points, you should identify and return the 10 most important points. Make sure you cover a wide array of points and not to focus only on one aspect." },
        { "role": "user", "content": outputs_str}
    ]

    final_output = run("@cf/meta/llama-2-7b-chat-int8", inputs)
    #TODO send numbered_lines as output not print
    #print(final_output)
    return final_output
