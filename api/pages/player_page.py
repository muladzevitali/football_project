import os
import time
from json import dumps

from flask import request, redirect, url_for, render_template, Blueprint
from werkzeug.utils import secure_filename

from api import app
from api.commons import CUR_VIDEO, TEAM_MAPPER, TERM_TEXT, OPTIONS, generate_user_id
from api.utils import list_files, allowed_file
from configuration import Options
from api.messages import ok_message

player_page = Blueprint('player_page', __name__,
                        template_folder='../../front/templates',
                        static_folder='../../front/static')


@player_page.route('/player/', methods=['GET', 'POST'])
def upload_file():
    user_id = generate_user_id()
    print(user_id)
    if request.method == 'POST':
        # Check if outer user inputs video file
        if 'file' not in request.files:
            print('no file', request.url)
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('no filename')
            return redirect(request.url)

        # If user inputs normal video file
        if file and allowed_file(file.filename, Options.allowed_extensions):
            filename = secure_filename(file.filename)
            file.save(os.path.join(Options.upload_folder, filename))
            print('Getting new video')

            return render_template("player.html", vidsrc=url_for('uploaded_file', filename=filename, user_id=user_id),
                                   filelist=list_files(Options.upload_folder), videoname=filename[:-4])
    return render_template('player.html', vidsrc=f"/{Options.default_video}/{user_id}", user_id=user_id,
                           filelist=list_files(Options.upload_folder), videoname="Bundesliga Goals")


@player_page.route('/player/objects', methods=['POST'])
def process_caught_objects():
    if 'info' in request.headers and 'time' in request.headers:
        info = request.headers['info']
        r_time = request.headers['time']
        source = request.headers['source']
        video_name = request.headers['vidname']
        user_id = request.headers['user']
        # Id for counter in html
        cnt_id = "cnt" + source + info
        # Convert ordinary text to link
        # print('%s Got from user %s' % (source, user_id), info)

        image_name = "defaultlogo.svg" if source == "Logo" else "defaulttext.svg"
        
        if os.path.isfile(f"front/static/images/logos/{info.lower()}.svg"):
            image_name = f"{info.lower()}.svg"
        elif os.path.isfile(f"front/static/images/logos/{info.lower()}.png"):
            image_name = f"{info.lower()}.png"
        if TEAM_MAPPER.get(info):
            # Get link from dictionary
            link = TEAM_MAPPER[info]
            # print('Logo got from user %s' % user_id, info)
            # HTML wrapping. Link opens in new tab
            info = f'<a target="_blank" href="{link}">{info}</a>'

        # if source == "Logo":
        #     info = f'{info} Logo'
            
        result = {"info": info, "image": image_name, "time": r_time, "source": source, "video": video_name, "counter": cnt_id}
        # Append info to terminal in JSON format
        user_text = dumps(result) + "\n=======\n"
        TERM_TEXT.insert_text(user_id, user_text)
        return ok_message


@player_page.route('/player/terminal/<user_id>')
def term(user_id):
    """
    Continuously stream new terminal messages.
    :param user_id: float -- the id of the user whose terminal we want
    """

    def pr_term(_user_id):
        print('Getting terminal text for user %s' % _user_id)
        while True:
            target = TERM_TEXT.get_text(user_id)
            yield target
            time.sleep(.100)

    return app.response_class(pr_term(user_id), mimetype='text/html')


@player_page.route('/player/playpause/<user_id>')
def play_pause(user_id):
    CUR_VIDEO[user_id].play_pause()
    return ok_message


@player_page.route('/player/seek/<user_id>/<millis>')
def seek(user_id, millis):
    # Technically it's a float but we are always passing ints in url anyway
    CUR_VIDEO[user_id].jump_to_time(int(millis))
    return ok_message


@player_page.route('/player/getpos/<user_id>')
def get_pos(user_id):
    def pos(_user_id):
        """
        Continuously stream current millisecond position of video.
        :param _user_id: float -- the id of the user whose video we want
        """

        # Wait until a video is ready
        while not CUR_VIDEO.get(_user_id):
            time.sleep(.300)
        # Continuously stream video position, delimited by exclamation points
        while True:
            # Id of CAP_PROP_POS_MSEC is 0
            yield "!!!" + str(CUR_VIDEO[_user_id].video.get(0))
            time.sleep(.500)

    return app.response_class(pos(user_id), mimetype='text/plain')


@player_page.route('/player/getduration/<user_id>')
def get_duration(user_id):
    """
    Get duration of video (in seconds).
    :param user_id: float -- the id of the user whose video we want
    :return Duration of video as string
    """
    # Wait until a video is ready
    while not CUR_VIDEO.get(user_id):
        time.sleep(.300)

    return str(CUR_VIDEO[user_id].duration)


@player_page.route('/player/choption/<user_id>/<option>/<value>')
def change_setting(user_id, option, value):
    """
    Change the detection options for the current user
    :param user_id: float -- the id of the user whose video we want
    :param option: string -- name of the option
    :param value: boolean -- value of the option
    """
    OPTIONS[user_id][option] = value
    return str(value)
