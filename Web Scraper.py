import csv
import requests
from bs4 import BeautifulSoup

base_url = "https://books.toscrape.com/"


def get_items_list(url):
    response = requests.get(url)
    html_code = response.text

    soup = BeautifulSoup(html_code, features='html.parser')
    items_list = soup.find_all('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'})

    return items_list


def write_items_to_csv(items_list, csv_file):
    with open(csv_file, 'a', newline='', encoding='utf-8') as csv_file_obj:
        fieldnames = ['title', 'price', 'availability']
        csv_writer = csv.DictWriter(csv_file_obj, fieldnames=fieldnames)

        # Only write the header if the file is empty
        if csv_file_obj.tell() == 0:
            csv_writer.writeheader()

        for item in items_list:
            title = item.h3.a.get('title')
            price = item.find('p', 'price_color').text.replace('Â', '').strip()
            availability = item.find('p', class_='instock availability').text.strip()

            csv_writer.writerow({'title': title, 'price': price, 'availability': availability})


def main():
    csv_file = "items.csv"

    for i in range(1, 50):
        url = base_url + 'catalogue/page-' + str(i) + '.html'
        items_list = get_items_list(url)
        write_items_to_csv(items_list, csv_file)


if __name__ == "__main__":
    main()

