import jinja2
import os

from template_engine import jinja2_filters

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
JINJA_ENVIRONMENT.filters['date'] = jinja2_filters.date
JINJA_ENVIRONMENT.filters['digits'] = jinja2_filters.digits
JINJA_ENVIRONMENT.filters['escapeurl'] = jinja2_filters.escapeurl
JINJA_ENVIRONMENT.filters['floatformat'] = jinja2_filters.floatformat
JINJA_ENVIRONMENT.filters['rfc2822'] = jinja2_filters.rfc2822
JINJA_ENVIRONMENT.filters['slugify'] = jinja2_filters.slugify
JINJA_ENVIRONMENT.filters['strip_frc'] = jinja2_filters.strip_frc


def render(template, template_values):
    template = JINJA_ENVIRONMENT.get_template(template)
    return template.render(template_values)
