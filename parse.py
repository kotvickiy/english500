#region pip install requests beautifulsoup4 lxml
import requests
import urllib3
from bs4 import BeautifulSoup as bs
import csv
#endregion


def save(data):
    with open('eng_rus.csv', 'a', encoding='utf-8', newline='') as file:
        order = ['name', 'transcription', 'translate']
        writer = csv.DictWriter(file, fieldnames=order)
        writer.writerow(data)


def get_html(url):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = requests.get(url, verify=False)
    if response.ok:
        return response.text
    else:
        return response.status_code


def get_data(html):
    soup = bs(html, 'lxml')
    blocks = soup.find('div', class_='entry-content').find_all('p')
    list_words = blocks[3].text.split('\n')
    for line in list_words:
        lines = line.replace('\xad', '')
        name = lines.split('. ')[1].split('[')[0].strip().replace("\xa0", " ").replace(' ', '_')
        transcription = '[' + lines.split('[')[1].split(']')[0].strip().replace("\xa0", " ").replace(' ', '_') + ']'
        translate = lines.replace("\xa0", " ").replace('- ', ' — ').split(' — ')[1].replace(',', ';')
        data = {'name': name,
                'transcription': transcription,
                'translate': translate}
        save(data)
    


def main():
    url = r'https://englishfull.ru/topiki/500-anglijskih-slov.html'
    get_data(get_html(url))


if __name__ == "__main__":
    main()
