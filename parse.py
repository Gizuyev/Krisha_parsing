import requests
import csv 
from bs4 import BeautifulSoup
import pprint
from config import DOMEN, URL, HEADERS

def get_html(url, headers = HEADERS, params=None):
    r = requests.get(url, headers=headers, params=params)
    if r.status_code == 200:
        return r.text



def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='a-card__inc')
    data = []
    for item in items:
        try:
            title = item.find('a',class_='a-card__title').get_text(strip=True)
            title_data = title.split(', ')
            rooms = title_data[0]
            # print(rooms)
            square = title_data[1]
            # print(square)
            floor_data = title_data[2]
            all_data = floor_data.split(' ')
            floor = ' '.join(all_data[:-1])
            # print(floor)
            payment = all_data[-1]
            # print(payment)
            address = item.find('div', class_='a-card__subtitle').get_text(strip=True)
            # print(address)
            city = item.find('div', class_='card-stats__item').get_text(strip=True)
            # print(city)
            price = item.find('div', class_='a-card__price').get_text(strip=True)
            # print(price)
            date = item.find('div', class_='card-stats__item').find_next_sibling().get_text(strip=True)
            # print(date)
            image = item.find('img').get('src')
            # print(image)
            link = DOMEN + item.find('div', class_='a-card__header-left').find('a').get('href')
            # print(link)

            data.append({
                'rooms': rooms,
                'square': square,
                'floor': floor,
                'payment': payment,
                'address': address,
                'city': city,
                'price': price,
                'date': date,
                'image': image,
                'link': link,

            })
        except Exception  as e:
            print(e)
    return data
def save_to_csv(data):
    with open('flat.csv', 'a') as f:
        filedsnames = data[0].keys()
        writer = csv.DictWriter(f,filedsnames)
        writer.writeheader()
        writer.writerows(data)

def parser(page=1):
    contents = []
    for p in range(2, page+1):
        html = get_html(URL, params={'page': p} if p !=1 else None)
        content = get_content(html)
        contents.extend(content)
        print(f"Страница {p} спарсена")
    return contents         

html = get_html(URL)
content = get_content(html)
save_to_csv(parser(5))