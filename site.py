import sys

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
    # Gets bio page
    bio_page = pages.get('bio')
    return render_template('bio.html', bio=bio_page)


@app.route('/portfolio/')
def portfolio():
    # Gets portfolio page
    portfolio_page = pages.get('portfolio')
    # Gets all section pages
    sections = sorted((page for page in pages if "-portfolio" in page.path), key=lambda page: page.meta['title'])
    # Gets all projects pages
    projects = sorted((page for page in pages if 'date' in page.meta), reverse=True, key=lambda page: page.meta['date'])
    return render_template('portfolio.html', portfolio=portfolio_page, sections=sections, projects=projects)


@app.route('/portfolio/<path:project_type>')
def portfolio_section(project_type):
    # Gets all section pages
    sections = [page for page in pages if
                "-portfolio" in page.path and project_type.replace('/', '') in page.meta.values()]
    # Gets all projects pages
    projects = sorted(
        (page for page in pages if 'date' in page.meta and project_type.replace('/', '') in page.meta.values()),
        reverse=True, key=lambda page: page.meta['date'])
    return render_template('portfolio.html', portfolio=None, sections=sections, projects=projects)


@app.route('/portfolio/<string:project_type>/<path:project_name>/')
def project(project_type, project_name):
    # Gets project page
    project_page = pages.get_or_404(project_name)
    return render_template('project.html', project=project_page)


@app.route('/contatti/')
def contatti():
    # Gets contatti page
    contatti_page = pages.get("contatti")
    return render_template('contatti.html', contatti=contatti_page)


@app.route('/robots.txt')
def robots():
    robots_txt = 'User-agent: *\nDisallow: /signature/\nSitemap: ' + url_for('sitemaps', _external=True)
    response = make_response(robots_txt)
    response.headers["Content-Type"] = "text/plain"
    return response


@app.route('/sitemaps.xml')
def sitemaps():
    # Gets last modified time from git
    proc = subprocess.Popen('./last_modified_pages_times.sh', stdout=subprocess.PIPE)
    times = (proc.stdout.read().decode()).splitlines()

    times_and_names = [time[:-3].split(' pages/') for time in times]

    # Useful lambda for getting time for not project pages
    get_time = lambda x: [(times_and_names.pop(times_and_names.index(time))[0]) for time in times_and_names if
                          time[1] == x]

    # Gets time for bio, portfolio and contatti
    bio_time = get_time('bio')[0]
    portfolio_time = get_time('portfolio')[0]
    contatti_time = get_time('contatti')[0]

    times_and_pages = list(((time_and_name[0], pages.get(time_and_name[1])) for time_and_name in times_and_names if
                            '-portfolio' in time_and_name[1]))

    # Removes times for not projects
    times_and_projects = list(((time_and_name[0], pages.get(time_and_name[1])) for time_and_name in times_and_names if
                               '-portfolio' not in time_and_name[1]))

    sitemap_xml = render_template('sitemap.xml', bio_time=bio_time, portfolio_time=portfolio_time,
                                  contatti_time=contatti_time, times_and_pages=times_and_pages,
                                  times_and_projects=times_and_projects)
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
