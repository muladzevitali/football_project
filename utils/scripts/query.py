import os

PATH = '/home/vitali/Downloads/bbox/Labels/001'

for file in os.listdir(PATH):
    file_path = os.path.join(PATH, file)
    with open(file_path, 'r') as input_file:
        if len(input_file.readlines()) > 10:
            os.remove(file_path)