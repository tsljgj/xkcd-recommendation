import random

def load_keywords(file_path):
    with open(file_path, 'r') as file:
        keywords = file.read().strip().split(', ')
    return keywords

def save_keywords(file_path, keywords):
    with open(file_path, 'w') as file:
        file.write(', '.join(keywords))

def delete_random_keywords(keywords, num_to_delete):
    if num_to_delete > len(keywords):
        raise ValueError("Number of keywords to delete exceeds the total number of keywords.")
    return random.sample(keywords, len(keywords) - num_to_delete)

def main():
    keyword_file_path = './data/keyword.txt'
    num_keywords_to_delete = 300  # Specify the number of keywords to delete

    # Load keywords
    keywords = load_keywords(keyword_file_path)
    print(f"Original Keywords: {keywords}")

    # Delete random keywords
    modified_keywords = delete_random_keywords(keywords, num_keywords_to_delete)
    print(f"Modified Keywords: {modified_keywords}")

    # Save modified keywords back to the file
    save_keywords(keyword_file_path, modified_keywords)

if __name__ == "__main__":
    main()