import time

import cv2

from api.commons import label_detector, LABELS, height, flags
from api.utils import handle_results, send_request
from configuration import Options
from utils.detection.yolo.utils.detector import detection
from utils.detection.yolo.yolo.preprocess import prep_image


class Video(object):

    def __init__(self, filename, user):
        self.video_source = filename
        self.user = user
        self.video = None
        self.is_active = True
        self.frame = None
        self.is_paused = False
        self. duration = 0

    def jump_to_frame(self, frame_num):
        """
        Jump to specific frame in the video.
        See also https://docs.opencv.org/3.4.2/d4/d15/group__videoio__flags__base.html
        #gaeb8dd9c89c10a5c63c139bf7c4f5704d
        :param frame_num: int -- number of destination frame 
        """
        # Pause the video and wait a bit, to prevent async_lock crashes
        self.is_paused = True
        time.sleep(0.04)

        self.video.set(1, frame_num)  # Id of CAP_PROP_POS_FRAMES is 1
        self.is_paused = False  # Un pause again

    def jump_to_time(self, target_time):
        """
        Jump to specific millisecond position in the video.
        See also https://docs.opencv.org/3.4.2/d4/d15/group__videoio__flags__base.html
        #gaeb8dd9c89c10a5c63c139bf7c4f5704d
        :param target_time: float -- destination milliseconds
        """
        # Pause the video and wait a bit, to prevent async_lock crashes
        self.is_paused = True
        time.sleep(0.04)

        self.video.set(0, target_time)  # Id of CAP_PROP_POS_MSEC is 0
        self.is_paused = False

    def play_pause(self):
        """
        Play or pause the video.
        """
        self.is_paused = not self.is_paused

    def set_video_source(self, source):
        self.video_source = source

    def start_streaming(self, options):
        self.video = cv2.VideoCapture(self.video_source)
        if not self.video.isOpened():
            raise RuntimeError('Could not start video.')

        # Calculate duration by dividing frame count by frame rate.
        # See VideoCaptureProperties enumerator for all IDs.
        self.duration = self.video.get(7) / self.video.get(5)

        # Read and return the first frame so that the variables are not empty
        res, frame = self.video.read()
        time.sleep(0.04)
        frame = cv2.imencode('.jpg', frame)[1].tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        _frame_number = 0
        while True:
            _frame_number += 1
            # Break if video is not active
            if not self.is_active:
                break
            if not self.is_paused:
                # Read next frame only if not paused
                res, frame = self.video.read()
                if not res:
                    data = {'info': "video end", 'time': str(time.time()),
                            'source': 'Meta', 'user': self.user, 'vidname': self.video_source}
                    send_request('http://127.0.0.1:{}/player/'.format(Options.detection_service_port), headers=data)
                    break
                image_loader = prep_image(frame, height, path=False)

                results = detection(image_loader, label_detector, flags, draw=False)
                if results != 0 and _frame_number % 10:
                    r_time = self.video.get(0)
                    det_text = options["detecttext"]
                    det_logos = options["detectlogos"]
                    frame = handle_results(frame, results, LABELS, self.user, self.video_source, r_time, det_text,
                                           det_logos)

                frame = cv2.imencode('.jpg', frame)[1].tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            j = 0
            while self.is_paused:
                if j % 10 == 0:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                j = j + 1
                time.sleep(.100)

            time.sleep(0.04)

