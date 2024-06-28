import json
from openai import OpenAI
import time

def load_keywords(file_path):
    with open(file_path, 'r') as file:
        keywords = json.load(file)
    return keywords

def are_keywords_related(keyword1, keyword2):
    client = OpenAI()
    prompt = f"Are the words '{keyword1}' and '{keyword2}' highly related? Answer YES or NO."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a keyword relationship analyzer."},
            {"role": "user", "content": prompt}
        ]
    )
    answer = response.choices[0].message.content
    return 'YES' in answer

def build_adjacency_list(keywords):
    adjacency_list = {keyword: [] for _, keyword in keywords}
    keyword_list = [keyword for _, keyword in keywords]

    for i in range(len(keyword_list)):
        for j in range(i + 1, len(keyword_list)):
            keyword1 = keyword_list[i]
            keyword2 = keyword_list[j]
            if are_keywords_related(keyword1, keyword2):
                adjacency_list[keyword1].append(keyword2)
                adjacency_list[keyword2].append(keyword1)
            time.sleep(0.5)
        print(f"id={i} completed")
    
    return adjacency_list

def save_adjacency_list_to_json(adjacency_list, keywords, output_file):
    adjacency_list_with_ids = {keywords[key]: [keywords[neighbor] for neighbor in neighbors] for key, neighbors in adjacency_list.items()}
    
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(adjacency_list_with_ids, file, ensure_ascii=False, indent=4)

def save_adjacency_list_to_json(adjacency_list, keywords, output_file):
    keyword_to_id = {keyword: idx for idx, keyword in keywords}
    adjacency_list_with_ids = {keyword_to_id[key]: [keyword_to_id[neighbor] for neighbor in neighbors] for key, neighbors in adjacency_list.items()}
    
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(adjacency_list_with_ids, file, ensure_ascii=False, indent=4)

# Main program
keywords_file_path = 'comic_keywords.json'
keywords = load_keywords(keywords_file_path)

# Build adjacency list
adjacency_list = build_adjacency_list(keywords)

# Save adjacency list to a JSON file
output_file = 'keyword_adjacency_list.json'
save_adjacency_list_to_json(adjacency_list, keywords, output_file)
print(f"Adjacency list saved to {output_file}")