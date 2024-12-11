from newspaper import Article

def extract_main_text(url):
    try:
        # Download and parse the article
        article = Article(url)
        article.download()
        article.parse()

        # Extract the main content
        return article.text

    except Exception as e:
        return f"An error occurred: {e}"

# Example usage
url = "https://en.wikipedia.org/wiki/Artos_(drink)"
main_text = extract_main_text(url)
print("Extracted Text:")
print(main_text)
