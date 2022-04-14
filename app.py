import flask
import requests
import random
from urllib.parse import urlparse
import string


app = flask.Flask(__name__)


def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False


def get_random_string(length):
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    return result_str


@app.route('/')
def hello_world():
    # return "Hello world"
    # google = requests.request("GET", "http://www.google.com")
    return flask.redirect("http://127.0.0.1:5000/shortening", code=302)


@app.route("/shortening")
def url_short():
    return flask.render_template('form.html')


@app.route('/shortening', methods=['POST'])
def my_form_post():
    web_address = flask.request.form['http_adress']
    if uri_validator(web_address):
        return "http://127.0.0.1:5000/" + get_random_string(5)
    else:
        return "Please provide valid url"


@app.route('/<id>')  # /landingpageA
def landing_page(id):
    return id


if __name__ == '__main__':
    app.debug = True
    app.run()

