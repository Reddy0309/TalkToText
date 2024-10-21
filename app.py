from flask import Flask, request, jsonify
import speech_recognition as sr
from gtts import gTTS
from deep_translator import GoogleTranslator
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize the recognizer
listener = sr.Recognizer()

# Define language options
languages = {
    "1": {"name": "Hindi", "code": "hi"},
    "2": {"name": "Telugu", "code": "te"},
    "3": {"name": "Kannada", "code": "kn"},
    "4": {"name": "English", "code": "en"}
}


@app.route('/')
def home():
    return "Welcome to my Flask application!"
    
@app.route('/Speechtotext', methods=['POST'])
def Speechtotext():
    data = request.get_json()
    language_choice = data.get('language_choice', '4')  # Default to English if not provided
    
    if language_choice not in languages:
        return jsonify({"error": "Invalid language choice"}), 400
    
    selected_language = languages[language_choice]
    
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source)
            print("Listening...")
            voice = listener.listen(source)
            
            command = listener.recognize_google(voice, language=selected_language['code'])
            print(f"You said: {command}")

            if selected_language['code'] != "en":
                translation = GoogleTranslator(source=selected_language['code'], target='en').translate(command)
            else:
                translation = command
                
                
            print(f"Translation: {translation}")

            converted = gTTS(translation, lang='en')
            converted.save("translation.mp3")
            response = jsonify({"command": command, "translation": translation})
            response.headers.add('Access-Control-Allow-Origin', '*')  # Adjust as needed
            return response

    except sr.UnknownValueError:
        return jsonify({"error": "Google Speech Recognition could not understand audio"}), 400
    except sr.RequestError as e:
        return jsonify({"error": f"Could not request results from Google Speech Recognition service; {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
