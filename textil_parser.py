from parsing_base import Parser
from bs4 import BeautifulSoup


class TextilParser(Parser):
    MAIN_PAGE = 'https://teks-o-park.com'

    def __init__(self):
        super().__init__()

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
        print(len(resps_collections))
        # for resp_collection in resps_collections:
        #     soup = BeautifulSoup(resp_collection, 'lxml')
        #     materials_blocks = soup.select('.woocommerce-LoopProduct-link')
        #     materials_urls = []
        #     for material_block in materials_blocks:
        #         materials_urls.append(material_block['href'])
        #     print(materials_urls)





if __name__ == '__main__':
    parser = TextilParser()
    parser.update_data()