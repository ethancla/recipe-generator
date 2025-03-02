import json
import openai
import os
from flask import Flask, request, jsonify
import googleapiclient.discovery

app = Flask(__name__)

# Prompt used to ensure GPT returns JSON with specified quiz questions and answers
prompt = ("You are RecipeGPT. You are tasked with generating multiple foods that can be created with a given ingredients list. The user will input multiple ingredients and you must return multiple food items that can be created with ONLY the items listed. If there are no foods that can be created because the user inputted too little ingredients, inform them that they have inputted too little ingredients. If another error occurs, provide a simple error message indicating what the user did wrong. You MUST ONLY RESPOND IN JSON FORM, do not include any unnecessary comments. THE USER CAN INPUT IN ANY FORMAT. This means they can seperate ingredients with whitespace or with english words like AND So be ready for inputs like: apples and bannanas and cabbage OR waffle mapel syrup eggs")
valid_examples = ("EXAMPLES: { \"response\": [ \"Garden Salad\", \"Lettuce Wraps with Ranch and Tomatoes\", \"Tomato and Lettuce Salad with Ranch Dressing\" ]}, { \"response\": \"No ingredients provided.\" }, { \"response\": \"You put too little ingredients!\" }")

def generate_recipes():
    '''Function that calls GPT with the provided prompt in combination with user input to generate food items'''

    user_input = input("Ingredients:\n")

    ### REPLACE THE API KEY BEFORE WE BLOW UP! ###
    client = openai.OpenAI(api_key="")

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt + valid_examples},
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    print(completion.choices[0].message.content) # Just for debugging / verification
    return json.dumps(completion.choices[0].message.content) # Return for later use

### EXAMPLE RESPONSE: ###

# { "response": [ "Apple Sauce", "Baked Apples", "Caramel Apples", "Apple Crisp", "Apple Juice", "Dried Apples" ] }
# { "error": "No ingredients provided." }


def youtube_test(subject):

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = '' # REPLACE DA KEY!!!
 
    return_list = []

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)
    request = youtube.search().list(
        part='snippet',
        q=subject,
        maxResults=5,
        order="relevance",
        type="video"
    )
    return_value = request.execute()
    
    for items in return_value['items']:
        x = items['id']['videoId']
        link = f"https://www.youtube.com/watch?v={x}"


        return_list.append([items['snippet']['title'], items['id']['videoId'], link, items['snippet']['thumbnails']['high']['url']])

    return return_list
### EXAMPLE RESPONSE:
# [['NEW ELIZABETH CRAZY DIAMOND BEAT DOWN!', 'noFwVqZ0jRs', 'https://www.youtube.com/watch?v=noFwVqZ0jRs', 'https://i.ytimg.com/vi/noFwVqZ0jRs/hqdefault.jpg'], ['BaneBeetle vs Fidget spinner!', '9PnJ2zZjEHE', 'https://www.youtube.com/watch?v=9PnJ2zZjEHE', 'https://i.ytimg.com/vi/9PnJ2zZjEHE/hqdefault.jpg'], ['Extolyt and BaneBeetle...', 'RTI7Yj2Wem4', 'https://www.youtube.com/watch?v=RTI7Yj2Wem4', 'https://i.ytimg.com/vi/RTI7Yj2Wem4/hqdefault.jpg'], ['I GOT JACKO SP BASE FROM THIS TRADE! | Yba Trading', 'evnRKQNSsnA', 'https://www.youtube.com/watch?v=evnRKQNSsnA', 'https://i.ytimg.com/vi/evnRKQNSsnA/hqdefault.jpg'], ['POV: Ur running for a sticker but you give them heart shaped donuts (trust me they are heart shaped)', '24eoTsMK4xE', 'https://www.youtube.com/watch?v=24eoTsMK4xE', 'https://i.ytimg.com/vi/24eoTsMK4xE/hqdefault.jpg']]

# Flask endpoints

@app.route('/recipes', methods=['POST'])
def recipes_endpoint():
    data = request.get_json()
    ingredients = data.get("ingredients")
    if not ingredients:
        return jsonify({"error": "Please provide ingredients"}), 400

    # Patch input() for generate_recipes() to use provided ingredients.
    import builtins
    original_input = builtins.input
    builtins.input = lambda prompt="": ingredients

    try:
        response = generate_recipes()
        parsed_response = json.loads(response)
        return jsonify(parsed_response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        builtins.input = original_input

@app.route('/youtube', methods=['GET'])
def youtube_endpoint():
    subject = request.args.get("subject")
    if not subject:
        return jsonify({"error": "Please provide a subject query parameter"}), 400
    try:
        results = youtube_test(subject)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    generate_recipes()


### EXAMPLE RESPONSE: ###

# { "response": [ "Apple Sauce", "Baked Apples", "Caramel Apples", "Apple Crisp", "Apple Juice", "Dried Apples" ] }
# { "error": "No ingredients provided." }



'''In another world where stars align
I feel I'm falling through the sky
To a place where youre all mine
A dream of love
Til the break of night
I just wanna close my eyes
Then I'll have you by my side
In a realm where we entwine
Through the night
I find my way right to your arms
I know its right where I belong
I can embrace all of your love
And in my dreams I'm all that you want
I can stay right here forever
In this eternal bliss
Realize all my love is true
Whenever I dream of you
As the stars adorn the midnight sky
Our love goes on til the end of time
A dream of us that mends my heart
Where you and I won't ever part
I just wanna close my eyes
Then I'll have you by my side
In a realm where we entwine
Through the night
I find my way right to your arms
I know its right where I belong
I can embrace all of your love
And in my dreams I'm all that you want
I can stay right here forever
In this eternal bliss
Realize all my love is true
Whenever I dream of you
There's a place
Inside my mind
Where you and I are so divine
So divine
You stay with me through the night
I know its a dream but it feels so right
I'll have you by my side
When I sleep
Through the night
I find my way right to your arms
I know its right where I belong
I can embrace all of your love
And in my dreams I'm all that you want
I can stay right here forever
In this eternal bliss
Realize all my love is true
Whenever I dream of you'''

