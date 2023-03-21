import requests
from bs4 import BeautifulSoup
import json
import csv

url = 'https://massage.co.ua/uk/tablica-kalorijnosti-produktov-v-100-grammax/'

header = {
    "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryYpr6JiWg4noyYCEb",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/111.0.0.0 Safari/537.36 "
}

req = requests.get(url, headers=header)
src = req.text


# 1 - Download html page
#
# with open('index.html', 'w') as f:
#     f.write(src)
#
# with open("index.html") as file:
#     src = file.read()

soup = BeautifulSoup(src, "lxml")

# 2 - Get table column headings

table_head = soup.find('table').find('tr').find_all('th')

product = table_head[0].text
proteins = table_head[1].text
fats = table_head[2].text
carbohydrates = table_head[3].text
callories = table_head[4].text

# 3 - Add data to csv file

with open('data/indexes.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(
        (
            product,
            proteins,
            fats,
            carbohydrates,
            callories
        )
    )

# 4 - Get code product data and add it to csv and json files

all_products_data = soup.find(class_="blog-ul").find_all('tr')
for item in all_products_data:
    if len(item.find_all('td')) < 1:
        all_products_data.remove(item)

product_info = []
for item in all_products_data:
    products_pfc = item.find_all('td')

    title = products_pfc[0].text
    proteins = products_pfc[1].text
    fats = products_pfc[2].text
    carbohydrates = products_pfc[3].text
    callories = products_pfc[4].text

    product_info.append(
        {
            "Title": title,
            "Proteins": proteins,
            "Fats": fats,
            "Carbohydrates": carbohydrates,
            "Callories": callories

        }
    )

    with open('data/indexes.csv', 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                title,
                proteins,
                fats,
                carbohydrates,
                callories
            )
        )

with open('data/indexes.json', 'a', encoding='utf-8') as file:
    json.dump(product_info, file, indent=4, ensure_ascii=False)
