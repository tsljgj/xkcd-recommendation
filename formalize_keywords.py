import json

# Load the summarized comics data
file_path = 'comics_summary.json'
with open(file_path, 'r') as file:
    comics = json.load(file)

# Extract keywords and store them in a structured format
keywords = []
for idx, comic in enumerate(comics):
    comic_id = idx + 1  # Assuming comic IDs start from 1
    summary_keywords = comic['summary'].split()
    for keyword in summary_keywords:
        keywords.append((comic_id, keyword))

# Save the keywords to a file
keywords_file_path = 'comic_keywords.json'
with open(keywords_file_path, 'w', encoding='utf-8') as file:
    json.dump(keywords, file, ensure_ascii=False, indent=4)