import json
from openai import OpenAI
import pandas as pd

def load_comics(file_path):
    with open(file_path, 'r') as file:
        comics = json.load(file)
    return comics

def load_keywords(file_path):
    with open(file_path, 'r') as file:
        keywords = file.read().strip().split(', ')
        keywords = [keyword.strip('"') for keyword in keywords]
    return keywords

def get_related_keywords(description, keywords):
    client = OpenAI()
    prompt = f"\nKeywords: {', '.join(keywords)}\nDescription: {description}"
    # print(prompt)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a comic description summarizer. Given a list of keyword and a description of the comic, which keywords from the list are strongly related to the description? Provide a list of matching keywords similar to this format: apple,banana,orange"},
            {"role": "user", "content": prompt}
        ]
    )

    summary = response.choices[0].message.content
    # print(summary)
    related_keywords_list = summary.split(', ')
    return related_keywords_list
    
def create_binary_matrix(comics, keywords):
    matrix = []
    cnt = 0
    for comic in comics:
        if cnt == 100:
            break
        cnt += 1
        description = comic['description']
        related_keywords = get_related_keywords(description, keywords)

        # Initialize the row with zeros
        row = [0] * len(keywords)

        # Fill the row with 1s for related keywords
        for i, keyword in enumerate(keywords):
            if keyword in related_keywords:
                row[i] = 1

        # print(row)
        # Append the row to the matrix
        matrix.append(row)

        print(f"comic {cnt} is summarized.")
    
    return matrix

def save_matrix_to_csv(matrix, keywords, file_path):
    df = pd.DataFrame(matrix, columns=keywords)
    df.to_csv(file_path, index_label='comic_id')

def main():
    comics = load_comics('./data/comic_data.json')
    keywords = load_keywords('./data/keyword.txt')
    
    binary_matrix = create_binary_matrix(comics, keywords)
    
    save_matrix_to_csv(binary_matrix, keywords, './data/comic_keywords_matrix.csv')

if __name__ == "__main__":
    main()