import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google.cloud import dialogflow


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\amans\Downloads\ember-y9cd-71ede1fef42c.json"

app = Flask(__name__)
CORS(app)


def detect_intent_text(project_id, session_id, text, language_code):
    try:
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(project_id, session_id)
        text_input = dialogflow.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)
        response = session_client.detect_intent(request={"session": session, "query_input": query_input})
        return response.query_result.fulfillment_text
    except Exception as e:
        return str(e)


@app.route("/chat", methods=["POST"])
def chat():
    try:
        
        data = request.get_json()
        user_text = data.get("text", "")  
        session_id = data.get("session_id", "123456")

       
        project_id = "ember-y9cd"

       
        bot_response = detect_intent_text(project_id, session_id, user_text, "en")

        
        return jsonify({"response": bot_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
