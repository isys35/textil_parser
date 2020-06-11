import requests
from bs4 import BeautifulSoup
import os
import xlwt
import sys
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'
}

MAIN_PAGE = 'https://textiledata.ru'
IMG_FOLDER = 'img'


def update_data(url):
    try:
        os.listdir(IMG_FOLDER)
    except FileNotFoundError:
        os.mkdir(IMG_FOLDER)
    for the_file in os.listdir(IMG_FOLDER):
        file_path = os.path.join(IMG_FOLDER, the_file)
        os.unlink(file_path)
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'lxml')
    description = soup.select_one('.right-block.fl-r').text.replace('\t', '')
    add_description_block = soup.select_one('.left-block.fl-l')
    add_descriptions = []
    for add_description in add_description_block.select('.r'):
        add_descriptions.append(
            'static;' + add_description.text.replace('\t', '').replace('\n', '').replace(' ' * 8, '') + '|')
    add_description_text = '\n'.join(add_descriptions)
    wb = xlwt.Workbook()
    ws = wb.add_sheet('sheet')
    ws.write(0, 0, description)
    ws.write(0, 1, add_description_text)
    wb.save('data.xls')
    download_image(resp)
    images_block = soup.findAll('li', itemprop="isRelatedTo")
    for images_block in images_block:
        url = MAIN_PAGE + images_block.select_one('a')['href']
        resp = requests.get(url, headers=headers)
        download_image(resp)


def download_image(resp):
    soup = BeautifulSoup(resp.text, 'lxml')
    image_block = soup.select_one('.images-block')
    url = MAIN_PAGE + image_block.select('img')[-2]['src']
    image_resp = requests.get(url, headers=headers)
    with open(f"{IMG_FOLDER}/{url.split('/')[-1]}", 'wb') as out:
        out.write(image_resp.content)


def main():
    url = input('Введите ссылку:')
    update_data(url)
    print('[INFO] Завершено')


if __name__ == '__main__':
    while True:
        main()