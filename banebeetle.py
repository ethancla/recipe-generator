from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import json
import googleapiclient.discovery

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key!")
if not YOUTUBE_API_KEY:
    raise ValueError("Missing YouTube API Key!")

client = openai.Client(api_key=OPENAI_API_KEY)

prompt = ("You are RecipeGPT. You are tasked with generating multiple foods that can be created with a given ingredients list. "
          "The user will input multiple ingredients and you must return multiple food items that can be created with ONLY the items listed. "
          "If there are no foods that can be created because the user inputted too little ingredients, inform them. "
          "Provide a simple error message indicating what the user did wrong. Respond ONLY in JSON format.")

@app.route('/recipes', methods=['POST'])
def get_recipes():
    data = request.get_json()
    ingredients = data.get("ingredients", "")

    if not ingredients:
        return jsonify({"error": "No ingredients provided."}), 400

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": ingredients}
            ]
        )

        response_text = completion.choices[0].message.content.strip()

        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "").replace("```", "").strip()

        return jsonify(json.loads(response_text))
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/youtube', methods=['GET'])
def get_youtube():
    try:
        subject = request.args.get("subject", "")

        if not subject:
            return jsonify({"error": "No search term provided."}), 400

        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

        yt_request = youtube.search().list(
            part='snippet',
            q=subject,
            maxResults=3,
            order="relevance",
            type="video"
        )

        response = yt_request.execute()
        videos = [
            {
                "title": item["snippet"]["title"],
                "videoId": item["id"]["videoId"],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]
            }
            for item in response.get("items", [])
        ]

        return jsonify(videos)

    except Exception as e:
        print("YouTube API Error:", str(e))  # Logs the error in Render logs
        return jsonify({"error": f"Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)


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