import os
from multiprocessing import Pool, Value
from urllib.request import urlretrieve

import requests
import scrapy


pages = [i + 1 for i in range(42)]


def get_image(title, image_url, image_type):
    image_local_path = '/home/vitali/files/football_project/unlabeled/' + title + '.' + image_type
    urlretrieve(image_url, image_local_path)


def parse(page_num):
    print(page_num)
    start_url = f'https://www.sportphotogallery.com/football/#page={page_num}'
    page = requests.get(start_url)
    sel = scrapy.Selector(page)
    url = sel.xpath('//*[@id="magic-warpper"]/div//img[@class="magic-item landscape"]/@src').extract()
    for item in url:
        image_url = 'https://www.sportphotogallery.com' + item
        image_title = str(page_num) + '_' + image_url.split('/')[-2]
        image_type = 'jpg'
        if not os.path.isfile('/home/vitali/files/football_project/unlabeled/' + image_title + '.' + image_type):
            # print(image_title + '.' + image_type, sep='\t')
            get_image(image_title, image_url, image_type)
        else:
            print('Already exists :)')
            continue


if __name__ == '__main__':
    pool = Pool()
    pool.map(parse, pages)
