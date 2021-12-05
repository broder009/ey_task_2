import glob
import os
import flask
from pathlib import Path
from werkzeug.utils import secure_filename

from convert_to_db import Database

upload_dir = Path(Path.cwd(), "upload")

app = flask.Flask(__name__, template_folder='template', static_folder='static')
app.config['upload_dir'] = upload_dir
app.add_url_rule("/uploads/<name>", endpoint="download_file", build_only=True)


@app.route("/", methods=['GET', 'POST'])
def upload():  # uploading files on web
    if flask.request.method == 'POST':
        file = flask.request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['upload_dir'], filename))
        return flask.redirect("/upload")
    return flask.render_template("home.html")


@app.route("/upload", methods=['GET', 'POST'])
def uploaded_files():  # displaying list of files on web
    direct = os.listdir(str(upload_dir))
    return flask.render_template("uploaded.html", direct=direct)


@app.route("/display", methods=['GET', 'POST'])
def display():  # displaying of database on web
    db = Database("database.db")
    db.create_table()
    db.insert_data()
    data = db.display_table()
    return flask.render_template("display.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)  # start of app
