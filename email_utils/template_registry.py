from jinja2 import Environment, FileSystemLoader
import os

env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))

TEMPLATES = {
    "magic_link": "magic_link.html",
    "verification": "verification.html"
}

def get_email_body(identifier: str, **kwargs) -> str:
    template_name = TEMPLATES.get(identifier)
    if not template_name:
        raise ValueError("Unknown email template identifier")

    template = env.get_template(template_name)
    return template.render(**kwargs)
