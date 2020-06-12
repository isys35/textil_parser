from parsing_base import Parser
from bs4 import BeautifulSoup
import os
import sys
import xlwt


class TextilParser(Parser):
    MAIN_PAGE = 'https://teks-o-park.com'

    def __init__(self):
        super().__init__()
        self.image_catalog = 'img'

    def update_data(self):
        resp = self.request.get('https://teks-o-park.com/shop/')
        soup = BeautifulSoup(resp.text, 'lxml')
        colllections_blocks = soup.select('li.product-category')
        urls_collections = []
        for collecion_block in colllections_blocks:
            urls_collections.append(collecion_block.select_one('a')['href'])
        splited_urls_collections = self.split_list(urls_collections, 5)
        resps_collections = []
        for url_list in splited_urls_collections:
            resps_collections.extend(self.requests.get(url_list))
        materials_urls = []
        for resp_collection in resps_collections:
            soup = BeautifulSoup(resp_collection, 'lxml')
            materials_blocks = soup.select('.woocommerce-LoopProduct-link')
            for material_block in materials_blocks:
                materials_urls.append(material_block['href'])
        materials_data = []
        self.init_image_catalog()
        for url in materials_urls:
            resp = self.request.get(url)
            soup = BeautifulSoup(resp.text, 'lxml')
            img_url = soup.find('meta', attrs={'property': 'og:image'})['content']
            print(img_url)
            image_name = img_url.split('/')[-1]
            self.save_image(img_url, f"{self.image_catalog}/{image_name}")
            description = self.get_description(soup)
            materials_data.append([image_name, description])
        self.save_xls(materials_data)

    def save_xls(self, materials_data):
        wb = xlwt.Workbook()
        ws = wb.add_sheet('sheet')
        for i in range(len(materials_data)):
            ws.write(i, 0, materials_data[i][0])
            ws.write(i, 1, materials_data[i][1])
        wb.save('data.xls')

    def get_description(self, soup):
        discription = soup.find('div', attrs={'itemprop': 'description'})
        if not discription:
            return str()
        table = discription.select('table')[-1]
        trs = table.select('tr')
        description_text = str()
        for tr in trs:
            tds = tr.select('td')
            if tds[0].text == 'Рекомендации по чистке и уходу:':
                break
            elif tds[0].text == 'Устойчивость к окрашиванию при трении (основной цвет):':
                description_text += 'static;' + trs[trs.index(tr) + 1].text + '\t' + trs[trs.index(tr) + 2].text + '|'
                break
            else:
                description_text += 'static;' + tds[0].text + ';\t' + tds[1].text + '|\n'
        print(description_text)
        return description_text

    def init_image_catalog(self):
        try:
            os.listdir(self.image_catalog)
        except FileNotFoundError:
            os.mkdir(self.image_catalog)
        for the_file in os.listdir(self.image_catalog):
            file_path = os.path.join(self.image_catalog, the_file)
            os.unlink(file_path)


if __name__ == '__main__':
    parser = TextilParser()
    parser.update_data()