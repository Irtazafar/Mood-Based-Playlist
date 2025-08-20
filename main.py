emotion_classifier = pipeline ( " text - classification ",
model="j- hartmann / emotion - english - distilroberta - base ", top_k =1
)
# Configure Google Gemini
genai. configure ( api_key =" YOUR_GEMINI_API_KEY ")
gemini_model = genai. Generative Model (" models / gemini -1.5 - flash - latest")

def  detect_emotion ( text:  str):
"""	Detect emotional tone from user input."""
result = emotion_classifier ( text)[0 ][0 ]
return result[" label"]. lower (), result[" score "]

def generate_gemini_response ( user_input: str , mood : str) -> str:
"""	Generate a warm , empathetic response using Gemini AI."""
prompt = f """
You are a warm , supportive chatbot.
The user just said: "{ user_input}" Their mood is: { mood. upper()}.

Respond like a human	empathetic , conversational , and supportive
.
If appropriate , suggest music that could help. """
response = gemini_model. generate_content ( prompt)
return getattr( response , " text", " I’m␣here ␣if␣you ␣want␣to␣talk ."). strip ()

@app . route ("/") def index ():
"""	Load the chat interface."""
return  render_template (" index . html")

@app . route ("/ chat", methods =[" POST "]) def chat ():
"""	Process  user  message	detect  mood	generate  reply
suggest playlists."""
data = request. get_json ()
user_message = data . get(" message ", "")
# Step 1: Detect emotion
mood , confidence = detect_emotion ( user_message ) if confidence < 0.5 or mood == " neutral":
mood  =  map_to_emotion_fallback ( user_message )
# Step 2: Generate empathetic AI reply
reply = generate_gemini_response(user_message, mood)

# Step 3: Fetch mood-based playlists
playlists = get_playlists_by_mood(mood)

# Return combined response
return jsonify({
    "response": reply,
    "playlists": playlists
})