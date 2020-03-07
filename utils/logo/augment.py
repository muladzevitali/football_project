import Augmentor
import os

os.chdir('/home/vitali/Documents/files/football_project/logos')
for folder in os.listdir():
    for image in os.listdir(folder):
        p = Augmentor.Pipeline(folder)
        p.skew_left_right(probability=1, magnitude=1)
        p.sample(2, multi_threaded=True)
        p.process()
