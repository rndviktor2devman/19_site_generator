from markdown import markdown
import json
import os
import argparse
from jinja2 import Environment, FileSystemLoader
from collections import defaultdict

SOURCE_INDEX_PATH = 'templates/index.html'
TARGET_INDEX_PATH = 'site/index.html'
SOURCE_ARTICLES_PATH = 'site/articles'
SOURCE_TEMPLATES_PATH = 'templates/page.html'


def load_json(file):
    with open(file, 'r') as data:
        return json.load(data)


def render_base(page_structure):
    environment = Environment(loader=FileSystemLoader('./'))
    template = environment.get_template(SOURCE_TEMPLATES_PATH)
    return template.render(page_structure)


def build_site_structure(config):
    for item in config['articles']:
        output, filename = os.path.split(item['source'])
        output_dir = os.path.join(SOURCE_ARTICLES_PATH, output)
        filename = filename.replace('md', 'html')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        html = md_conversion(os.path.join('articles', item['source']))
        page_structure = {'html': html,
                'title': item['title'],
                'topic': item['topic']}
        with open(os.path.join(output_dir, filename), 'w') as f:
            f.write(render_base(page_structure))


def md_conversion(file):
    with open(file, 'r') as md_file:
        return markdown(md_file.read(),
                        extensions=['codehilite', 'fenced_code'])


def create_index(config):
    page_structure = defaultdict(list)
    for item in config['articles']:
        path = item['source'].replace('md', 'html')
        page_structure[item['topic']].append([os.path.join('articles', path), item['title']])
    env = Environment(loader=FileSystemLoader('./'))
    template = env.get_template(SOURCE_INDEX_PATH)
    with open(TARGET_INDEX_PATH, 'w') as f:
        f.write(template.render(struct=page_structure))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Static site based on markdown files')
    parser.add_argument('path', help='json file path')
    args = parser.parse_args()
    json_configuration = load_json(args.path)
    build_site_structure(json_configuration)
    create_index(json_configuration)
