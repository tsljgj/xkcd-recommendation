from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random

app = Flask(__name__)
CORS(app)

# Load comic data
with open('comic_data.json', 'r') as file:
    comics = json.load(file)

# Placeholder for user actions (you can load this from a file or database)
user_actions = {}
user_estimates = {}

# Multi-armed bandit functions (implement your logic here)
def select_action(user_id):
    # Placeholder: random selection
    if user_id not in user_estimates:
        user_estimates[user_id] = [0] * len(comics)
    
    # Example of epsilon-greedy selection
    epsilon = 0.1
    if random.random() > epsilon:
        return user_estimates[user_id].index(max(user_estimates[user_id]))
    else:
        return random.randint(0, len(comics) - 1)

def update_estimates(user_id, item_id, reward):
    # Placeholder: update estimates
    if user_id not in user_estimates:
        user_estimates[user_id] = [0] * len(comics)
    user_estimates[user_id][item_id] += reward

@app.route('/get_comic', methods=['GET'])
def get_comic():
    user_id = int(request.args.get('user_id'))
    comic_id = select_action(user_id)
    print(f"Selected comic ID: {comic_id} for user ID: {user_id}")
    return jsonify(comics[comic_id])

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    user_id = int(data['user_id'])
    comic_id = int(data['comic_id'])
    reward = int(data['reward'])

    if user_id not in user_actions:
        user_actions[user_id] = []

    user_actions[user_id].append({'comic_id': comic_id, 'reward': reward})
    update_estimates(user_id, comic_id, reward)

    print(f"Feedback received: User {user_id}, Comic {comic_id}, Reward {reward}")
    
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
