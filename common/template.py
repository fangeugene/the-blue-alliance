import jinja2
import os

from common import jinja2_filters

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
JINJA_ENVIRONMENT.filters['date'] = jinja2_filters.date


def render(template, template_values):
    template = JINJA_ENVIRONMENT.get_template(template)
    return template.render(template_values)
