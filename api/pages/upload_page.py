from flask import Blueprint, Response
import os
from api.commons import CUR_VIDEO, TERM_TEXT, OPTIONS
from api.resources.basevideo import Video

upload_page = Blueprint('upload_page', __name__,
                        template_folder='../../front/templates',
                        static_folder='../../front/static')

_UNLABELED_LOGOS = 'data/logo/unlabeled/'

@upload_page.route('/upload/<filename>/<user_id>')
def uploaded_file(filename, user_id):
    TERM_TEXT.set_user(user_id)

    if not OPTIONS.get(user_id):
        # Create default options for user
        OPTIONS[user_id] = {"detecttext": "true", "detectlogos": "true"}
    print(f'File {filename} uploaded, starting editing', user_id)
    # For easy reference to api/basevideo object
    if CUR_VIDEO.get(user_id):
        CUR_VIDEO[user_id].is_active = False
        CUR_VIDEO[user_id] = None

    CUR_VIDEO[user_id] = Video(f'upload/{filename}', user_id)
    # Make a folder for a unlabeled objects
    unlabeled_data_path = os.path.join(_UNLABELED_LOGOS, filename.split('.')[0].upper())
    os.makedirs(unlabeled_data_path, exist_ok=True)
    os.makedirs(f"data/ocr/unlabeled/{filename.split('.')[0].upper()}", exist_ok=True)

    print('Start streaming')
    return Response(CUR_VIDEO[user_id].start_streaming(OPTIONS[user_id]),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
