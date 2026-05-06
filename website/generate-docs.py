import json
import os
import shutil
import sys
import yaml

templates_dir = '../catalog'
definition_filename = 'definition.yaml'
usage_filename = 'README.md'
converted_notebook_filename = 'notebook.html'

gn_dir = 'generated'
gn_docs_dir = f'{gn_dir}/docs'
resources_dir = 'resources'
base_json = f'{resources_dir}/base-data.json'
generated_json = 'data.json'
previous_dir = 'previous'

repo_definition_base = 'https://raw.githubusercontent.com/scc-digitalhub/hub/refs/heads/main/catalog'

with open(base_json, 'r', encoding='utf-8') as f:
    structure = json.load(f)

"""Remove any pre-existing generated website and initialize the new one.
"""
def initialize_website():
    # Remove
    if os.path.isdir(gn_dir):
        shutil.rmtree(gn_dir)

    # Initialize directories
    os.mkdir(gn_dir)
    os.mkdir(gn_docs_dir)

    # Copy javascripts and stylesheets
    shutil.copytree(f'{resources_dir}/extra-javascripts', f'{gn_docs_dir}/javascripts')
    shutil.copyfile(f'{resources_dir}/search-library/searchLibrary.js', f'{gn_docs_dir}/javascripts/searchLibrary.js')
    shutil.copytree(f'{resources_dir}/stylesheets', f'{gn_docs_dir}/stylesheets')

    # Copy MkDocs yaml file and home page file
    shutil.copyfile(f'{resources_dir}/mkdocs.yml', f'{gn_dir}/mkdocs.yml')
    shutil.copyfile(f'{resources_dir}/homepage.md', f'{gn_docs_dir}/index.md')

"""Form the string that references the template on the hub

    Parameters
    ----------
    category : str
        The category the template belongs to
    template : str
        Name of the template
    metadata : str
        Metadata object of the template

    Returns
    -------
    str
        Reference to the template on the hub
"""
def hub_ref(category, template, metadata):
    hr = f'hub://{category}/{template}'
    if 'version' in metadata:
        hr += f':{metadata["version"]}'
    return hr

"""Create metadata div for the template's page

    Parameters
    ----------
    category : str
        The category the template belongs to
    template : str
        Name of the template
    metadata : str
        Metadata object of the template

    Returns
    -------
    str
        Metadata div
"""
def template_page_metadata(category, template, version, metadata, version_menu):
    contents = '<div id="template-metadata">'

    # Interactive element in top right
    contents += '<div id=template-metadata-right>'

    contents += version_menu

    catalog_url = structure['catalog_url']
    version_dir = f'/{previous_dir}/{version}' if version != 'latest' else ''
    contents += f'<a class="md-cell-right" id=md-repo-directory target="_blank" href="{catalog_url}/{category}/{template}{version_dir}">Repository</a>'
    contents += f'<a class="md-cell-right" id=md-repo-definition target="_blank" href="{repo_definition_base}/{category}/{template}{version_dir}/{definition_filename}">Definition</a>'

    # Button to copy hub reference
    contents += '<div id="hub-ref" class="md-cell-right">'
    contents += '<button id="hub-ref-text" class="hub-ref-button" onclick="toggleRef()">Reference <span id="hub-ref-icon">&#x25BC;</span></button>'

    hr = hub_ref(category, template, metadata)
    copy_button_contents = '<span id=hub-ref-copy-clipboard>&#10064;</span><span id=hub-ref-copy-copied>&#10003;</span><span id=hub-ref-copy-space>&#10064;</span>'
    contents += f'<div id="hub-ref-link"><span id=hub-ref-link-text>{hr}</span><button id=hub-ref-link-button onclick="copyRef()">{copy_button_contents}</button></div>'
    
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

"""Create usage div for the template's page

    Parameters
    ----------
    usag_path : str
        Path to the file describing template usage

    Returns
    -------
    str
        Usage div
"""
def template_usage(usage_path):
    content = '<div class="template-info-tab" id="template-usage" markdown="1">'
    if os.path.isfile(usage_path):
        with open(usage_path, 'r', encoding='utf-8') as usage_file:
            usage = usage_file.read()
        content += usage
    else:
        content += f'This template is missing information on usage. {usage_path}'
    return content + '</div>'

"""Create notebook div for the template's page

    Parameters
    ----------
    notebook_path : str
        Path to the notebook file

    Returns
    -------
    str
        Notebook div
"""
def template_notebook(notebook_path):
    content = '<div class="template-info-tab" id="template-notebook">'
    with open(notebook_path, 'r', encoding='utf-8') as notebook_file:
        notebook_lines = notebook_file.readlines()
        # Some lines need to be removed, or they will disrupt MkDocs' structure
        notebook_content = ''.join(notebook_lines[6:-1])
        notebook_content = notebook_content.replace('<main>', '')
        notebook_content = notebook_content.replace('</main>', '')
        content += notebook_content
    return content + '</div>'

def template_versions(c, t):
    # Check if folder for previous versions exists
    previous_path = f'{templates_dir}/{c}/{t}/{previous_dir}'
    if not os.path.isdir(previous_path):
        return []

    # Each previous version should have its own subfolder
    dir_contents = os.listdir(previous_path)
    versions = []
    for c in dir_contents:
        if os.path.isdir(f'{previous_path}/{c}'):
            versions.append(c)

    if not versions:
        return []

    versions.sort()
    return ['latest'] + versions


"""Generates dropdown menu for previous versions, if necessary

    Parameters
    ----------
    c : str
        Name of the template's category
    t : str
        Template name

    Returns
    -------
    str
        Dropdown menu for previous versions
"""
def previous_menu(c, t, versions, vs):
    if not versions:
        return ''

    # Build menu
    menu = '<div id="previous-menu">'

    # Plain text for the version being viewed
    menu += f'<div class="version-entry" id="version-this">{vs}</div>'

    for v in versions:
        if v != vs:
            if vs == 'latest':
                v_path = f'./{v}'
            else:
                if v == 'latest':
                    v_path = '..'
                else:
                    v_path = f'../{v}'
            menu += f'<a class="version-entry version-other" href="{v_path}">{v}</a>'

            # Build pages for other versions
            if vs == 'latest':
                previous_path = f'{templates_dir}/{c}/{t}/{previous_dir}'
                definition_path = f'{previous_path}/{v}/{definition_filename}'
                if os.path.isfile(definition_path):
                    with open(definition_path, 'r', encoding='utf-8') as definition_file:
                        definition = next(yaml.load_all(definition_file, Loader=yaml.SafeLoader))

                    # Create template's own page
                    template_folder = f'./{gn_docs_dir}/{c}/{t}/{v}'
                    os.mkdir(template_folder)
                    template_path = f'{template_folder}/index.md'

                    contents = page_contents(c, t, versions, v, definition)
                    with open(template_path, 'w', encoding='utf-8') as template_file:
                        template_file.write(contents)
    menu += '</div>'

    return menu

"""Generates main contents for the template's page

    Parameters
    ----------
    c : str
        Name of the template's category
    t : str
        Template name
    definition : dict
        Definition of the template

    Returns
    -------
    str
        Main contents of the template's page
"""
def page_contents(c, t, versions, v, definition):
    contents = ''

    # Header section
    contents += '<div id="template-content" markdown="1">'
    browse_path = './../../'
    if v:
        browse_path += '..'
    contents += f'<a id="browse" href="{browse_path}">< Browse</a>'
    template_title = t
    if 'metadata' in definition and 'name' in definition['metadata']:
        template_title = definition['metadata']['name']
    contents += f'<div id="template-title">{template_title}</div>'

    version_menu = previous_menu(c, t, versions, v)

    # Metadata section
    if 'metadata' in definition:
        contents += template_page_metadata(c, t, v, definition['metadata'], version_menu)

    # Toolbar for tabs
    tab_toolbar = '<div id="template-tab-buttons">'
    tab_toolbar += '<button class="tab-button tab-button-selected" id="tab-button-usage" onclick="openTab(\'usage\')">Usage</button>'
    template_dir = f'{templates_dir}/{c}/{t}'
    if v != 'latest':
        template_dir += f'/{previous_dir}/{v}'

    notebook_path = f'{template_dir}/{converted_notebook_filename}'
    if os.path.isfile(notebook_path):
        tab_toolbar += '<button class="tab-button tab-button-not-selected" id="tab-button-notebook" onclick="openTab(\'notebook\')">Notebook</button>'
    tab_toolbar += '</div>'
    contents += tab_toolbar

    # Main contents of the page, containing usage and notebook
    contents += '<div id="template-info" markdown="1">'

    # Usage
    usage_path = f'{template_dir}/{usage_filename}'
    contents += template_usage(usage_path)

    # Notebook
    if os.path.isfile(notebook_path):
        contents += template_notebook(notebook_path)
    
    contents += '</div></div>'

    return contents

def main():
    initialize_website()

    structure_catalog = structure['catalog']

    # Generate pages based on catalog directory
    categories = os.listdir(templates_dir)
    categories.sort()

    for c in categories:
        if os.path.isdir(f'{templates_dir}/{c}'):
            structure_catalog[c] = []

            # Create folder for category
            category_dir = f'{gn_docs_dir}/{c}'
            os.mkdir(category_dir)

            # Create pages for all templates in category
            category_templates = os.listdir(f'{templates_dir}/{c}')
            category_templates.sort()
            for t in category_templates:
                # Ensure template has a definition file before proceeding
                definition_path = f'{templates_dir}/{c}/{t}/{definition_filename}'
                if os.path.isfile(definition_path):
                    with open(definition_path, 'r', encoding='utf-8') as definition_file:
                        definition = next(yaml.load_all(definition_file, Loader=yaml.SafeLoader))

                    # Entry for JSON structure file
                    structure_entry = definition
                    if 'metadata' in structure_entry:
                        structure_entry['metadata']['path'] = f'{c}/{t}'
                        catalog_url = structure['catalog_url']
                        structure_entry['metadata']['repository'] = f'{catalog_url}/{c}/{t}'
                        structure_entry['metadata']['relationships'] = [{'type': 'part_of', 'dest': hub_ref(c, t, structure_entry['metadata'])}]
                    structure_catalog[c].append(structure_entry)

                    # Create template's own page
                    template_folder = f'./{gn_docs_dir}/{c}/{t}'
                    os.mkdir(template_folder)
                    template_path = f'{template_folder}/index.md'

                    versions = template_versions(c, t)
                    contents = page_contents(c, t, versions, 'latest', definition)
                    with open(template_path, 'w', encoding='utf-8') as template_file:
                        template_file.write(contents)

    # Write JSON structure to file
    with open(f'{gn_docs_dir}/{generated_json}', 'w', encoding='utf-8') as json_file:
        json.dump(structure, json_file, indent=4, default=str)

if __name__ == "__main__":
    main()