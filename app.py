import flask
import requests
import random
from urllib.parse import urlparse
import string
import sqlite3 as sql


app = flask.Flask(__name__)


def uri_validator(url):
    """Method to check if given url is valid or not"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def get_random_string(length):
    """Generate random string of English lower and upper letters of given length"""
    result_str = "".join(random.choice(string.ascii_letters) for i in range(length))
    return result_str


@app.route("/")
def hello_world():
    return flask.redirect("http://127.0.0.1:5000/shortening", code=302)


@app.route("/shortening")
def url_short():
    """Render template form to submit url to shorten it"""
    return flask.render_template("form.html")


@app.route("/shortening", methods=["POST"])
def my_form_post():
    """Process given url address"""
    if flask.request.method == "POST":
        try:
            web_address = flask.request.form["http_address"]
            if uri_validator(web_address):
                shortened = get_random_string(5)
                with sql.connect("database.db") as con:
                    cur = con.cursor()
                    sqlite_insert_with_params = """INSERT INTO urls 
                    (original, shortened) VALUES(?, ?)"""

                    cur.execute(sqlite_insert_with_params, (web_address, shortened))
                    con.commit()
                    msg = "Record successfully added"
                    print(msg)
                return "http://127.0.0.1:5000/" + shortened
            else:
                # TODO Add new template to show this message and to resubmit another url
                return "Please provide valid url"
        except:
            con.rollback()
            return "Error in insert operation"
        finally:
            con.close()


@app.route("/<shortened_url>")
def landing_page(shortened_url):
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            query_to_search = """SELECT original FROM urls 
            WHERE shortened LIKE (?);"""
            cur.execute(query_to_search, [shortened_url])
            result = cur.fetchone()
            return flask.redirect(result[0], code=302)

    except:
        con.rollback()
        return "Error in insert operation"
    finally:
        con.close()


if __name__ == "__main__":
    app.debug = 1
    app.run()
