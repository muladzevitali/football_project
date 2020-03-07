import requests
import os

PATH = '/home/vitali/Downloads/new_logo'
length = len(os.listdir(PATH))

for i, image in enumerate(os.listdir(PATH)):
    print(f'{i}/{length}')
    image_path = os.path.join(PATH, image)
    headers = {'path': image_path}
    response = requests.post('http://127.0.0.1:1719/insert', headers=headers)

    print(response.json())
print('Done...')
