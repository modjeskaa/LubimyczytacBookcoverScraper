import os
import requests
from lxml import etree

def get_book_site(title: str, author: str):
    url = f"https://lubimyczytac.pl/szukaj/ksiazki?phrase={title}+{author}"
    return url

def extract_img_src(html_content):
    parser = etree.HTMLParser()
    tree = etree.fromstring(html_content, parser)

    # XPAth to extract image URL from the HTML
    img_tag = tree.xpath('/html/body/div[5]/main/div/div/div[3]/div[1]/div/span/span/div/div[2]/div[1]/form/img/@src')

    if img_tag:
        return img_tag[0]
    else:
        return None

if __name__ == "__main__":
    def download_image(url, save_directory):
        response = requests.get(url)
        response.raise_for_status()

        filename = os.path.join(save_directory, os.path.basename(url))

        with open(filename, 'wb') as f:
            f.write(response.content)

        print(f"Image downloaded successfuly")

    # Insert your search data
    book_title = input("Tytuł: ")
    book_author = input("Autor: ")

    book_url = get_book_site(book_title, book_author)
    response = requests.get(book_url)
    html_content = response.content

    # Save on desktop (in folder "book-covers")
    save_directory = os.path.join(os.path.expanduser("~"), "Desktop", "book-covers")

    # Checks if there's a folder "book-covers" on desktop and make one if there isn't one
    os.makedirs(save_directory, exist_ok=True)

    # Extract the image URL and download the image
    img_src = extract_img_src(html_content)
    if img_src:
        download_image(img_src, save_directory)
    else:
        print("Image not found")