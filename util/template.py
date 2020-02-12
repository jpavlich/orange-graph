from jinja2 import Template, Environment


env = Environment(trim_blocks=True, lstrip_blocks=False)


def load_template(filename):
    with open(filename) as f:
        return env.from_string(f.read())
