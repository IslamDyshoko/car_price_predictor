import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

info_book = {'name': [], 'price': [], 'rating': []}
for page in range(1, 7):  # Измените диапазон на нужное количество страниц
    url = f"https://books.toscrape.com/catalogue/page-{page}.html"
    sleep(3)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    book_card = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
    #print(book_card)

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

        #print(f"Рейтинг: {rating}, Название: {name}, Цена: {price}")
        info_book['name'].append(name)
        info_book['price'].append(price)
        info_book['rating'].append(rating)

df = pd.DataFrame(info_book)
df.to_csv('books.csv', index=False)
print(f"{len(df)} строк успешно сохранены в файл books.csv")