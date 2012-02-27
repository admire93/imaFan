from flask import Flask, url_for
from jinja2 import Environment, PackageLoader

app = Flask(__name__)
env = Environment(loader=PackageLoader('app', 'templates'))

config = {
  'index': 'http://admire.kr:1200',
}

@app.route('/')
def index():
    template = env.get_template('index.html')
    return template.render(config=config, url_for=url_for)

@app.route('/me')
def me():
    template = env.get_template('me.html') 
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
