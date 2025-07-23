import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://books.toscrape.com/catalogue/page-1.html"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
book_card = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
print(book_card)
info_book = {'name': [], 'price': [], 'rating': []}
for book in book_card:

    name = book.find("h3").find("a")["title"]
    price = book.find("p", class_="price_color").text[2:]
    rating_p = book.find('p', class_='star-rating')
    rating = None
    if rating_p.has_attr('class'):
        classes = rating_p['class'] # Получаем список всех классов: ['star-rating', 'Three']
        if 'One' in classes:
            rating = 1
        elif 'Two' in classes:
            rating = 2
        elif 'Three' in classes:
            rating = 3
        elif 'Four' in classes:
            rating = 4
        elif 'Five' in classes:
            rating = 5

    print(f"Рейтинг: {rating}, Название: {name}, Цена: {price}")
    info_book['name'].append(name)
    info_book['price'].append(price)
    info_book['rating'].append(rating)

df = pd.DataFrame(info_book)
df.to_csv('books.csv', index=False)
print("Данные успешно сохранены в файл books.csv")