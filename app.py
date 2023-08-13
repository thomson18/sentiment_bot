from flask import Flask, request, jsonify, render_template
import joblib

app = Flask(__name__)

model_path = 'models/lr_sentiment_model.pkl'
vectorizer_path = 'models/tfidf_vectorizer.pkl'

def predict_sentiment(user_input, model, tfidf):
    v = tfidf.transform([user_input])
    prediction = model.predict(v)[0]
    sentiment = 'Positive' if prediction > 0.5 else 'Negative'
    return sentiment

# @app.route('/')
# def hello_world():
#     return jsonify(message='Hello, World!')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict_sentiment', methods=['POST', 'GET'])
def predict_sentiment_api():
    try:
        data = request.get_json()
        user_input = data['user_input']

        model = joblib.load(model_path)
        tfidf = joblib.load(vectorizer_path)

        sentiment = predict_sentiment(user_input, model, tfidf)

        # Add chatbot response to conversation history
        if sentiment == 'Positive':
            chatbot_response = "I'm glad you're feeling positive!"
        else:
            chatbot_response = "I'm sorry to hear you're feeling negative."


        response = {
            'input': user_input,
            'predicted_sentiment': sentiment,
            'chatbot_response': chatbot_response
        }
        return jsonify(response), 200
    except Exception as e:
        error_msg = {'error': str(e)}
        return jsonify(error_msg), 500

if __name__ == '__main__':
    app.run(debug=True)
