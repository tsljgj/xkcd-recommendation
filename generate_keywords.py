import json
from openai import OpenAI

def load_comics(file_path):
    with open(file_path, 'r') as file:
        comics = json.load(file)
    return comics

def summarize_comic(description):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a comic description summarizer."},
            {"role": "user", "content": f"Please give 5 key words seperated by one space that best capture the theme of the comic. Don't put comma between key words. {description}"}
        ]
    )
    summary = response.choices[0].message.content
    return summary

def save_summaries_to_json(comics, summaries, output_file):
    comic_summaries = [
        {
            "title": comic['title'],
            "image_url": comic['image_url'],
            "summary": summary
        }
        for comic, summary in zip(comics, summaries)
    ]
    
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(comic_summaries, file, ensure_ascii=False, indent=4)

# Main program
file_path = 'comic_data.json'
comics = load_comics(file_path)

# Display comics and summarize their descriptions
summaries = []
cnt = 0
for comic in comics:
    cnt += 1
    summary = summarize_comic(comic['description'])
    summaries.append(summary)
    print(f"Comic #{cnt} summarized.")
    if cnt >= 10:  # Set to 10 for summarizing only the first 10 comics
        break

# Save summaries to a JSON file
output_file = 'comics_summary.json'
save_summaries_to_json(comics, summaries, output_file)