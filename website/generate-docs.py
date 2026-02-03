import json
import os
import shutil
import sys
import yaml

templates_dir = '../catalog'
definition_filename = 'definition.yaml'
usage_filename = 'README.md'
converted_notebook_filename = 'notebook.html'
generated_json = 'data.json'

gn_dir = 'generated'
gn_docs_dir = f'{gn_dir}/docs'
resources_dir = 'resources'

repo_catalog = 'https://github.com/scc-digitalhub/hub/tree/main/catalog'
repo_definition_base = 'https://raw.githubusercontent.com/scc-digitalhub/hub/refs/heads/main/catalog'

# Remove pre-existing generated website and initialize the new one
def initialize_website():
    if os.path.isdir(gn_dir):
        shutil.rmtree(gn_dir)

    os.mkdir(gn_dir)
    os.mkdir(gn_docs_dir)

    # Copy javascripts and stylesheets
    shutil.copytree(f'{resources_dir}/extra-javascripts', f'{gn_docs_dir}/javascripts')
    shutil.copyfile(f'{resources_dir}/search-library/searchLibrary.js', f'{gn_docs_dir}/javascripts/searchLibrary.js')
    shutil.copytree(f'{resources_dir}/stylesheets', f'{gn_docs_dir}/stylesheets')

    # Copy MkDocs yaml file and home page file
    shutil.copyfile(f'{resources_dir}/base-mkdocs.yml', f'{gn_dir}/mkdocs.yml')
    shutil.copyfile(f'{resources_dir}/homepage.md', f'{gn_docs_dir}/index.md')

# Create metadata div for template page
def template_page_metadata(metadata, category, template):
    contents = '<div id="template-metadata">'

    # Interactive element in top right
    contents += '<div id=template-metadata-right>'

    contents += f'<a class="md-cell-right" id=md-repo-directory target="_blank" href="{repo_catalog}/{category}/{template}">Repository</a>'
    contents += f'<a class="md-cell-right" id=md-repo-definition target="_blank" href="{repo_definition_base}/{category}/{template}/{definition_filename}">Definition</a>'

    # Button to copy hub reference
    contents += '<div id="hub-ref" class="md-cell-right">'
    contents += '<button id="hub-ref-text" class="hub-ref-button" onclick="toggleRef()">Reference <span id="hub-ref-icon">&#x25BC;</span></button>'

    hub_ref = f'hub://{category}/{template}'
    if 'version' in metadata:
        hub_ref += f':{metadata["version"]}'
    copy_button_contents = '<span id=hub-ref-copy-clipboard>&#10064;</span><span id=hub-ref-copy-copied>&#10003;</span><span id=hub-ref-copy-space>&#10064;</span>'
    contents += f'<div id="hub-ref-link"><span id=hub-ref-link-text>{hub_ref}</span><button id=hub-ref-link-button onclick="copyRef()">{copy_button_contents}</button></div>'
    
    
    contents += '</div>'

    contents += '</div>'
    
    # Main metadata
    contents += '<div id=template-metadata-left>'
    if 'name' in metadata:
        contents += '<div class=md-cell>'
        contents += '<div class=md-cell-title>Name</div>'
        contents += f'<div class=md-cell-content id=md-name>{metadata["name"]}</div>'
        contents += '</div>'
    if 'description' in metadata:
        contents += '<div class=md-cell>'
        contents += '<div class=md-cell-title>Description</div>'
        contents += f'<div class=md-cell-content id=md-description>{metadata["description"]}</div>'
        contents += '</div>'
    if 'version' in metadata:
        contents += '<div class=md-cell>'
        contents += '<div class=md-cell-title>Version</div>'
        contents += f'<div class=md-cell-content id=md-version>{metadata["version"]}</div>'
        contents += '</div>'
    if 'labels' in metadata:
        contents += '<div class=md-cell>'
        contents += '<div class=md-cell-title>Labels</div>'
        contents += '<div class=md-cell-content id=md-labels>'
        for label in metadata['labels']:
            contents += f'<span class="md-label">{label}</span>'
        contents += '</div>'
        contents += '</div>'
    contents += '</div>'

    contents += '</div>'
    return contents

# Usage tab in template page
def template_usage(title, usage_path):
    content = '<div class="template-info-tab" id="template-usage" markdown="1">'
    if os.path.isfile(usage_path):
        with open(usage_path, 'r') as usage_file:
            usage = usage_file.read()
        content += usage
    else:
        content += f'#{title}\n\n'
        content += 'This template is missing information on usage.'
    return content + '</div>'

# Notebook tab in template page
def template_notebook(notebook_path):
    content = '<div class="template-info-tab" id="template-notebook">'
    content += '<div>'
    with open(notebook_path, 'r') as notebook_file:
        notebook_lines = notebook_file.readlines()
        notebook_content = ''.join(notebook_lines[6:-1])
        notebook_content = notebook_content.replace('<main>', '')
        notebook_content = notebook_content.replace('</main>', '')
        content += notebook_content
    return content + '</div>'

def main():
    initialize_website()

    # Generate pages based on catalog directory
    structure = {}
    with open(f'{gn_dir}/mkdocs.yml', 'a') as mkdocs_file:
        mkdocs_file.write('  - Catalogs:\n')

        categories = os.listdir(templates_dir)
        categories.sort()
        for c in categories:
            if os.path.isdir(f'{templates_dir}/{c}'):
                structure[c] = []

                # Create folder for category and corresponding search page
                category_dir = f'{gn_docs_dir}/{c}'
                os.mkdir(category_dir)
                shutil.copyfile(f'{resources_dir}/search-library/search.html', f'{gn_docs_dir}/{c}.md')

                # Append entry in nav for category search page
                mkdocs_file.write(f'    - {c.title()}: "{c}.md"\n')

                # Create pages for all templates in category
                category_templates = os.listdir(f'{templates_dir}/{c}')
                category_templates.sort()
                for t in category_templates:
                    # Ensure template has a definition file before proceeding
                    definition_path = f'{templates_dir}/{c}/{t}/{definition_filename}'
                    if os.path.isfile(definition_path):
                        with open(definition_path, 'r') as definition_file:
                            definition = next(yaml.load_all(definition_file, Loader=yaml.SafeLoader))

                        # Entry for JSON structure file
                        structure_entry = definition
                        structure_entry['path'] = f'{t}'
                        structure[c].append(structure_entry)

                        # Create template's own page
                        template_path = f'./{gn_docs_dir}/{c}/{t}.md'

                        template_title = t
                        if 'metadata' in definition and 'name' in definition['metadata']:
                            template_title = definition['metadata']['name']

                        with open(template_path, 'w') as template_file:
                            template_file.write(f'<div id="template-title">{template_title}</div>')

                            template_file.write('<div id="template-content" markdown="1">')

                            # Metadata
                            if 'metadata' in definition:
                                template_file.write(template_page_metadata(definition['metadata'], c, t))

                            # Tabs for usage and notebook
                            tab_toolbar = '<div id="template-tab-buttons">'
                            tab_toolbar += '<button class="tab-button tab-button-selected" id="tab-button-usage" onclick="openTab(\'usage\')">Usage</button>'

                            # Usage
                            usage_path = f'{templates_dir}/{c}/{t}/{usage_filename}'
                            contents = template_usage(t, usage_path)

                            # Notebook
                            notebook_path = f'{templates_dir}/{c}/{t}/{converted_notebook_filename}'
                            if os.path.isfile(notebook_path):
                                tab_toolbar += '<button class="tab-button tab-button-not-selected" id="tab-button-notebook" onclick="openTab(\'notebook\')">Notebook</button>'
                                contents += template_notebook(notebook_path)

                            tab_toolbar += '</div>'

                            # Write tab toolbar and tabs
                            template_file.write(tab_toolbar)
                            template_file.write('<div id="template-info" markdown="1">')
                            template_file.write(contents)
                            
                            template_file.write('</div>')
                            template_file.write('</div>')

    # Write JSON structure to file
    with open(f'{gn_docs_dir}/{generated_json}', 'w') as json_file:
        json.dump(structure, json_file, indent=4, default=str)

if __name__ == "__main__":
    main()