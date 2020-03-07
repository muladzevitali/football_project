import os
from multiprocessing import Pool, Value
from urllib.request import urlretrieve

import requests
import scrapy

ID = Value('i', 0)

PAGES = [i + 1 for i in range(20)]
START_URLS = [
    'https://www.gettyimages.com/photos/manchester-united-fc?family=editorial&page={}&phrase=manchester%20united%20fc#license',
    'https://www.gettyimages.com/photos/ac-milan?family=editorial&page={}&phrase=ac%20milan#license',
    'https://www.gettyimages.com/photos/liverpool-fc?family=editorial&page={}&phrase=liverpool%20fc#license',
    'https://www.gettyimages.com/photos/barcelona-fc?family=editorial&page={}&phrase=barcelona%20fc#license',
    'https://www.gettyimages.com/photos/atletico-madrid-fc?family=editorial&page={}&phrase=atletico%20madrid%20fc#license',
    'https://www.gettyimages.com/photos/porto-fc?family=editorial&page={}&phrase=porto%20fc#license',
    'https://www.gettyimages.com/photos/ajax-fc?family=editorial&page={}&phrase=ajax%20fc#license',
    'https://www.gettyimages.com/photos/real-madrid?family=editorial&page={}&phrase=real%20madrid#license',
    'https://www.gettyimages.com/photos/olympique-lyonnais?family=editorial&page={}&phrase=olympique%20lyonnais#license',
    'https://www.gettyimages.com/photos/nottingham-forest-fc?family=editorial&page={}&phrase=nottingham%20forest%20fc#license',
    'https://www.gettyimages.com/photos/manchester-city-matches?family=editorial&page={}&phrase=manchester%20city%20matches#license',
    'https://www.gettyimages.com/photos/juventus-matches?family=editorial&page={}&phrase=juventus%20matches#license',
    'https://www.gettyimages.com/photos/olympique-de-marseille?family=editorial&page={}&phrase=olympique%20de%20marseille#license',
    'https://www.gettyimages.com/photos/fulham-matches?family=editorial&page={}&phrase=fulham%20matches#license',
    'https://www.gettyimages.com/photos/everton?family=editorial&page={}&phrase=everton#license',
    'https://www.gettyimages.com/photos/benfica?family=editorial&page={}&phrase=benfica#license',
    'https://www.gettyimages.com/photos/roma-fc?family=editorial&page={}&phrase=roma%20fc#license',
    'https://www.gettyimages.com/photos/leicester-city?family=editorial&page={}&phrase=leicester%20city#license',
    'https://www.gettyimages.com/photos/celtic-fc?family=editorial&page={}&phrase=celtic%20fc#license',
    'https://www.gettyimages.com/photos/arsenal-fc?family=editorial&page={}&phrase=arsenal%20fc#license',
    'https://www.gettyimages.com/photos/chelsea-fc?family=editorial&page={}&phrase=chelsea%20fc#license',
    'https://www.gettyimages.com/photos/monako-fc?family=editorial&page={}&phrase=monako%20fc#license',
    'https://www.gettyimages.com/photos/santos-fc?family=editorial&page={}&phrase=santos%20fc#license',
    'https://www.gettyimages.com/photos/sevilla-fc?family=editorial&page={}&phrase=sevilla%20fc#license',
    'https://www.gettyimages.com/photos/napoli-fc?family=editorial&page={}&phrase=napoli%20fc#license']


def get_image(title, image_url, image_type):
    image_local_path = '/home/vitali/files/football_project/unlabeled/' + title + '.' + image_type
    urlretrieve(image_url, image_local_path)


def parse(start_url):
    name = start_url.split('?')[0].split('/')[-1]
    print(name)
    page = requests.get(start_url)
    sel = scrapy.Selector(page)
    url = sel.xpath('//*[@id="assets"]/article//a[@class="search-result-asset-link"]/img/@src').extract()
    for item in url:
        image_url = item

        image_title = f'{name}_{ID.value}'
        image_type = 'jpg'
        if not os.path.isfile('/home/vitali/files/football_project/unlabeled/' + image_title + '.' + image_type):
            get_image(image_title, image_url, image_type)
            with ID.get_lock():
                ID.value += 1
        else:
            print('Already exists :)', ID.value)
            with ID.get_lock():
                ID.value += 1
            continue


if __name__ == '__main__':
    pages = []
    for url in START_URLS:
        for page in PAGES:
            pages.append(url.format(page))
    print(len(pages))
    pool = Pool()
    pool.map(parse, pages)
