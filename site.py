import sys

from flask import Flask, render_template
from flask_flatpages import FlatPages, flatpages
from flask_frozen import Freezer

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FREEZER_DESTINATION = 'dist'

app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)


@app.route('/')
@app.route('/bio/')
def index():
    return render_template('bio.html', pages=pages)


@app.route('/portfolio/')
def portfolio():
    projects = (p for p in pages if 'date' in p.meta)
    projects = sorted(projects, reverse=True, key=lambda p: p.meta['date'])
    return render_template('portfolio.html', pages=projects)


@app.route('/portfolio/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    return render_template('project.html', page=page)


@app.route('/contatti/')
def contatti():
    page = pages.get_or_404("contatti")
    return render_template('page.html', page=page)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(port=8080)