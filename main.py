def get_user_choices():
    choices = input("Enter the numbers of comics you like, separated by commas: ")
    return [int(choice.strip()) for choice in choices.split(',')]

def pick_random_comics(comics, num=6):
    return random.sample(comics, num)

def display_comics(comics):
    for idx, comic in enumerate(comics):
        print(f"{idx + 1}. Title: {comic['title']}")
        print(f"   URL: {comic['image_url']}\n")

def generate_prompt(all_comics, displayed_comics, user_likes):
    prompt = "Please consider the following comics information:\n"
    for idx, comic in enumerate(all_comics):
        prompt += f"Comic {idx + 1}: Title: {comic['title']}, Description: {comic['description']}\n"
    
    prompt += "\nUser interactions with previously shown comics:\n"
    for idx, comic in enumerate(displayed_comics):
        liked = "liked" if idx + 1 in user_likes else "not liked"
        prompt += f"Comic {idx + 1} ({liked}): Title: {comic['title']}, Description: {comic['description']}\n"
    
    with open('prompt.txt', 'w', encoding='utf-8') as file:
        file.write(prompt)

    return prompt

def get_recommendations(prompt):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": "Based on this, recommend 6 other comics the user may like. Output only the comic numbers."}
        ]
    )
    recommendations = response.choices[0].text.strip().split()
    return [int(num) for num in recommendations]

# Keep track of all shown comics and user choices
displayed_comics_history = []
user_likes_history = []

# Initially, pick 3 random comics
# displayed_comics = pick_random_comics(comics)
# displayed_comics_history.extend(displayed_comics)
# print("Here are 3 random comics:")
# display_comics(displayed_comics)

# while True:
#     user_likes = get_user_choices()
#     user_likes_history.extend([displayed_comics[i - 1] for i in user_likes])

#     # Generate a prompt with all comics and user preferences
#     prompt = generate_prompt(comics, displayed_comics_history, user_likes_history)
#     recommendations = get_recommendations(prompt)

#     recommended_comics = [comics[i - 1] for i in recommendations]
#     displayed_comics_history.extend(recommended_comics)
#     print("Comics recommended for you:")
#     display_comics(recommended_comics)

#     if input("Continue? (yes/no): ").lower() != 'yes':
#         break

#     # Update displayed comics with recommendations for the next iteration
#     displayed_comics = recommended_comics