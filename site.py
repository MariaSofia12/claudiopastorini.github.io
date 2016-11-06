import sys
from datetime import date

import subprocess
from flask import Flask, render_template
from flask import make_response
from flask import redirect
from flask import url_for
from flask_flatpages import FlatPages
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
def index():
    return redirect("bio", code=302)


@app.route('/bio/')
def bio():
    return render_template('bio.html', pages=pages)


@app.route('/portfolio/')
def portfolio():
    projects = sorted((p for p in pages if 'date' in p.meta), reverse=True, key=lambda p: p.meta['date'])
    return render_template('portfolio.html', pages=projects)


@app.route('/portfolio/<path:path>/')
def project(path):
    page = pages.get_or_404(path)
    return render_template('project.html', page=page)


@app.route('/contatti/')
def contatti():
    page = pages.get_or_404("contatti")
    return render_template('page.html', page=page)


@app.route('/robots.txt')
def robots():
    robots_txt = 'User-agent: *\nDisallow: /static/\nSitemap: ' + url_for('sitemaps', _external=True)
    response = make_response(robots_txt)
    response.headers["Content-Type"] = "text/plain"
    return response


@app.route('/sitemaps.xml')
def sitemaps():
    proc = subprocess.Popen('./last_modified_pages_times.sh', stdout=subprocess.PIPE)
    times = (proc.stdout.read().decode()).splitlines()

    times_and_pages = [time[:-3].split(' pages/') for time in times]

    get_time = lambda x: [(times_and_pages.pop(times_and_pages.index(time))[0]) for time in times_and_pages if
                          time[1] == x]

    bio_time = get_time('bio')[0]
    # portfolio_time = get_time('portfolio')[0]
    contatti_time = get_time('contatti')[0]

    sitemap_xml = render_template('sitemap.xml', bio_time=bio_time, portfolio_time=None, contatti_time=contatti_time,
                                  times_and_pages=times_and_pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"

    return response


@app.template_test('list')
def is_list(value):
    return isinstance(value, list)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        app.config['PREFERRED_URL_SCHEME'] = 'https'
        app.config['SERVER_NAME'] = 'claudiopastorini.github.io'
        freezer.freeze()
    else:
        app.run(debug=True, port=8080)
