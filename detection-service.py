from flask import render_template
from configuration import Options
from api import app
from api.pages import admin_page, contact_page, favicon_page, player_page, upload_page, errors_page


app.register_blueprint(admin_page)
app.register_blueprint(contact_page)
app.register_blueprint(favicon_page)
app.register_blueprint(player_page)
app.register_blueprint(upload_page)
app.register_blueprint(errors_page)


@app.route('/', methods=['GET'])
def index():
    yt_file = open("youtube_url.txt", "r")
    return render_template('index.html', youtube_embed_url=yt_file.readline())


if __name__ == '__main__':

    # Start serving
    app.run(host='0.0.0.0', port=Options.detection_service_port, threaded=True, debug=False)
