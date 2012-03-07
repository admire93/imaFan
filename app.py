import urllib2
import simplejson

import facebook

from flask import Flask, url_for, request
from jinja2 import Environment, PackageLoader

import lib.facebook as nfacebook

app = Flask(__name__)
env = Environment(loader=PackageLoader('app', 'templates'))

config = {
  'index': 'http://admire.kr:1200',
  'appid': '339932072707609',
  'secret': 'd154e4b288a4fe1020f54c2f0eb46921',
}


@app.route('/')
def index():
    template = env.get_template('index.html')
    return template.render(config=config, url_for=url_for)

@app.route('/me')
def me():
    user = nfacebook.parse_signed_request(
        request.cookies, 
        config['appid'],
        config['secret']
    )
    template = env.get_template('me.html') 

    if user:
        graph = facebook.GraphAPI(user['access_token'])
        profile = graph.get_object("me")
        return template.render(config=config, url_for=url_for, profile=profile);
    else:
        return template.render(config=config, url_for=url_for);

@app.route('/<int:uid>')
def person(uid):
    template = env.get_template('person.html')
    return template.render(url_for=url_for, config=config, uid=(str)(uid))

@app.route('/search')
def search():
    template = env.get_template('search.html')
    return template.render(url_for=url_for, config=config)

if __name__ == '__main__':
  app.run(host='admire.kr', port=1200, debug=True);
