import requests
from bs4 import BeautifulSoup
import json

comic_num = 2941  # Number of comics to scrape

def scrape(index):
    r = requests.get('https://www.explainxkcd.com/wiki/index.php/' + str(index))
    soup = BeautifulSoup(r.text, 'html.parser')

    title = soup.find('b').text
    image = 'https://www.explainxkcd.com/' + (soup.find('img'))['src']
    h2_tag = soup.find('h2')
    span_tag = soup.find('span', id='Discussion')

    explanation = ''
    current_tag = h2_tag.next_sibling
    while current_tag and current_tag != span_tag:
        explanation += ('\n' + current_tag.get_text())
        current_tag = current_tag.next_sibling
    
    explanation = '\n'.join([line for line in explanation.split('\n') if line.strip() != ''])

    return {
        'title': title,
        'image_url': image,
        'description': explanation
    }

def main():
    comic_data = []
    success = 0
    failure = 0

    for index in range(1, comic_num + 1):
        print("-----------------------------------")
        try:
            comic_data.append(scrape(index))
            success += 1
            print(f"Index {index} succeeded")
        except:
            failure += 1
            print(f"Index {index} failed")
        print(f"Total Attempts: {index}")
        print(f"Total Successes: {success}")
        print(f"Total Failures: {failure}")
        print("-----------------------------------")

    # Save the list of dictionaries to a JSON file
    with open('comic_data.json', 'w') as json_file:
        json.dump(comic_data, json_file, indent=4)

    # # Load and print the JSON data to verify
    # with open('comic_data.json', 'r') as json_file:
    #     loaded_comic_data = json.load(json_file)
    #     for comic in loaded_comic_data:
    #         print(f"Title: {comic['title']}")
    #         print(f"Image URL: {comic['image_url']}")
    #         print(f"Description: {comic['description']}\n")

main()
