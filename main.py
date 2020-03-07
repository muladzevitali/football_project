from multiprocessing import Pool
import os
from utils.helper import main


if __name__ == "__main__":
    pool = Pool(3)
    jobs = ['nohup python detection-service.py &',
            'nohup python ocr-service.py &',
            'nohup python logo-service.py &']
    if os.path.isfile('nohup.out'):
        os.remove('nohup.out')
    pool.map(main, jobs)
