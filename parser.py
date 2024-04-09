from bs4 import BeautifulSoup
import requests
import time
def parse(page_num):
    url = f'https://www.pepper.ru/?page={page_num}'
    myHeaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    page = requests.get(url, headers=myHeaders)

    print(f"Данные со страницы №{page_num}")

    soup = BeautifulSoup(page.text, 'html.parser')
    deals = soup.find_all('article', class_='thread')

    deal_num = 0

    for deal in deals:
        names_with_links = deal.find('a', class_='cept-tt')
        names_without_links = deal.find('span', class_='thread-link') #Требуется авторизация для доступа к ссылкам
        degrees = deal.find('span', class_=['cept-vote-temp', 'space--h-2'])
        ads = deal.find('span', class_='space--r-1')
        ads_link = deal.find('a', class_='button')

        if names_with_links:
            links = names_with_links['href']
        elif names_without_links:
            links = 'Необходима авторизация на сайте'
        elif ads_link:
            links = 'Ссылка на акцию отсутствует, рекламная ссылка: ' + ads_link['href']

        if ads:
            name_text = '\033[1m(Рекламное сообщение)\033[0m ' + ads.string
        elif names_with_links:
            name_text = names_with_links.string
        else:
            name_text = names_without_links.string

        if not degrees:
            degrees_text = 'отсуствуют'
            name_text = '\033[1m(Опрос)\033[0m ' + name_text
        else:
            degrees_text = degrees.string.strip()
            if "space--h-2" in degrees.get('class', []):
                name_text = "\033[1m(Акция закончилась)\033[0m " + name_text

        deal_num += 1

        print(f"{deal_num}.Название: {name_text}"
              f"\n  Градусы: {degrees_text}"
              f"\n  Ссылка: {links}\n")

    time.sleep(1)