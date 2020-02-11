from jinja2 import Template, Environment

# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True


env = Environment(trim_blocks=True, lstrip_blocks=True)


def load_template(filename):
    with open(filename) as f:
        return env.from_string(f.read())
