import requests
import pandas as pd
from bs4 import BeautifulSoup as soup


url = "https://books.toscrape.com/catalogue/page-1.html"

rows = []

stars_dict = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

while url != None:
    
    print("\n\nPAGE:", url)
    response = requests.get(url)
    content = soup(response.content, "lxml")

    books = content.findAll("article")

    for book in books:

        book_url = book.find("h3").find("a")["href"]
        book_url = "https://books.toscrape.com/catalogue/" + book_url

        # Access the individual page of each book
        print("Acessing", book_url)
        response = requests.get(book_url)
        book_content = soup(response.content, "lxml")

        image_url = book_content.find("div", id="product_gallery").find("img")["src"]
        image_url = "https://books.toscrape.com" + image_url[5:]

        title = book_content.find("h1").text.strip()
        price = book_content.find("p", class_="price_color").text.strip()
        availability = book_content.find("p", class_="availability").text.strip()
        rating_str = book_content.find("p", class_="star-rating")["class"][-1].strip()
        rating = stars_dict[rating_str]

        breadcrumb = book_content.find("ul", class_="breadcrumb").find_all("li")
        category = breadcrumb[-2].text.strip()

        row = (
            book_url, image_url, title, price, availability, rating, category
        )
        rows.append(row)
    
    # Check if have the button "next"
    next = content.find("ul", class_="pager").find("li", class_="next")
    if next:
        url = "https://books.toscrape.com/catalogue/" + next.find("a")["href"]
    else:
        url = None

columns = (
    "book_url", "image_url", "title", "price", "availability", "rating", "category"
)
df = pd.DataFrame(rows, columns=columns)
print(df)
df.to_excel("books.xlsx", index=False)