import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


def render(template, template_values):
    template = JINJA_ENVIRONMENT.get_template(template)
    return template.render(template_values)
