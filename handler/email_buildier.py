
from jinja2 import Environment, FileSystemLoader
def email_buildier(response:list[dict]):
    env = Environment(loader=FileSystemLoader('template'))
    template = env.get_template('final_template.jinja')
    html_content = template.render(response=response)  # response_json is your parsed JSON
    return html_content