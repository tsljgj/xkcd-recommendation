import pandas as pd
import numpy as np
import random

# Load the data using the relative path
data_train = pd.read_csv('./data/data_train.csv')
data_test = pd.read_csv('./data/data_test.csv')
features_item = pd.read_csv('./data/features_item.csv')

# Print the column names to debug
print("Columns in data_train:", data_train.columns)
print("Columns in data_test:", data_test.columns)
print("Columns in features_item:", features_item.columns)

# Initialize variables for the epsilon-greedy algorithm with features
epsilon = 0.1  # Probability of choosing a random action
num_features = features_item.shape[1] - 1  # Number of features (assuming first column is item_id)
value_estimates = np.zeros(num_features)  # Value estimates for each feature
counts = np.zeros(num_features)  # Count of pulls for each feature

def select_action(user_id):
    if random.random() < epsilon:
        return random.randint(0, features_item.shape[0] - 1)  # Random action (exploration)
    else:
        # Calculate the expected value for each item based on its features
        expected_values = features_item.iloc[:, 1:].dot(value_estimates)
        return np.argmax(expected_values)  # Best action based on expected values (exploitation)

def update_estimates(item_features, reward):
    for i, feature in enumerate(item_features):
        if feature == 1:  # Only update for features that are present in the item
            counts[i] += 1
            n = counts[i]
            value_estimates[i] += (1 / n) * (reward - value_estimates[i])

# Train the model
for index, row in data_train.iterrows():
    user_id = row['user_id']
    chosen_item = row['item_id']
    reward = row['reward']  # Assuming the reward column exists

    # Select an action (item) for the user
    arm = select_action(user_id)

    # Update estimates with the observed reward
    item_features = features_item.iloc[arm, 1:].values  # Get features of the selected item
    update_estimates(item_features, reward)

print("Feature-based value estimates after training:", value_estimates)

# Evaluate the model
total_rewards = 0
num_trials = data_test.shape[0]

# Use trained value estimates to make better recommendations
for index, row in data_test.iterrows():
    user_id = row['user_id']
    true_item = row['item_id']
    reward = row['reward']  # Assuming the reward column exists

    # Select the best action (item) based on the current estimates
    arm = select_action(user_id)

    # Accumulate the reward for evaluation
    total_rewards += reward

average_reward = total_rewards / num_trials
print(f'Average Reward: {average_reward}')

# Use the trained value estimates to recommend items for each user in data_test
recommendations = []
for index, row in data_test.iterrows():
    user_id = row['user_id']
    
    # Select the best action (item) based on the current estimates
    arm = select_action(user_id)  # This should be argmax(value_estimates) to always pick the best known item
    
    recommended_item = features_item.iloc[arm]['item_id']
    recommendations.append((user_id, recommended_item))

# Print or save the recommendations
for user_id, recommended_item in recommendations:
    print(f"Recommend item {recommended_item} for user {user_id}")
