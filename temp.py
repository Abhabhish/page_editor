from bs4 import BeautifulSoup
from googletrans import Translator

def translate_html_content(html_content, target_language='hi'):
    soup = BeautifulSoup(html_content, 'html.parser')
    translator = Translator()

    # Loop through all text nodes
    for text_node in soup.find_all(string=True):
        if text_node.strip():  # Only translate non-empty text
            translated_text = translator.translate(text_node, dest=target_language).text
            text_node.replace_with(translated_text)

    # Return the translated HTML content
    return str(soup)


