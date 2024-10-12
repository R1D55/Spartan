from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai

app = Flask(__name__)

# Configure Google Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Create the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Home Route - Displays the chat interface
@app.route('/')
def home():
    return render_template('index.html')

# API route to handle chatbot queries
@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.form['message']
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(user_message)
    
    return jsonify({'response': response.text})

if __name__ == '__main__':
    app.run(debug=True)
