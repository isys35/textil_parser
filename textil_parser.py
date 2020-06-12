from parsing_base import Parser
from bs4 import BeautifulSoup
import os

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
            image_name = img_url.split('/')[-1]
            self.save_image(img_url, f"{self.image_catalog}/{image_name}")

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