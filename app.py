import flask
import random
from urllib.parse import urlparse
import string
import sqlite3 as sql

app = flask.Flask(__name__)
app.config['DATABASE'] = 'database.db'


def get_db():
    db = getattr(flask.g, '_database', None)
    if db is None:
        db = sql.connect(app.config['DATABASE'], check_same_thread=False)
        db.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            short_url TEXT, 
            long_url TEXT
            )""")
        flask.g._database = db
    return db
    

def close_db(exception=None):
    db = getattr(flask.g, '_database', None)
    if db is not None:
        db.close()


def uri_validator(url):
    """Method to check if given url is valid or not"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def get_random_string():
    """Generate random string of English lower and upper letters of given length"""
    characters = string.ascii_letters + string.digits
    random_str = "".join(random.choice(characters) for i in range(8))
    return random_str


@app.route("/", methods=['GET', 'POST'])
def main():
    if flask.request.method == 'POST':
        long_url = flask.request.form['long_url']
        if uri_validator(long_url):
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT short_url FROM urls WHERE long_url = ?", (long_url,))
            result = cursor.fetchone()
            if result:
                short_url = result[0]
            else:
                short_url = get_random_string()
                cursor.execute("INSERT INTO urls (short_url, long_url) VALUES (?, ?)", (short_url, long_url))
                db.commit()
            cursor.close()
            return flask.render_template("form.html", short_url=short_url)
        else:
            return flask.render_template("form.html", msg="Please provide a valid URL")
    return flask.render_template("form.html")


@app.route("/<short_url>")
def short_url_page(short_url):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT long_url FROM urls WHERE short_url = ?", (short_url,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        long_url = result[0]
        return flask.redirect(long_url)
    return "Invalid URL"


if __name__ == "__main__":
    app.teardown_appcontext(close_db)
    app.run(debug=True)
