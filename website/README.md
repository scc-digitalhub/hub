# Hub website

This directory is dedicated to generating the website for the hub.

## Generate website files

The **generate-docs.py** file is a Python script that will create a directory called `generated`, containing a *MkDocs* website for the hub.

You will need *MkDocs* and the *mkdocs-material* theme to run the website locally. Install them as follows:

``` 
pip install mkdocs
pip install mkdocs-material
```

After running the script, `cd` to that directory and execute `mkdocs serve`, you will find the website at `http://localhost:8000`.

## Files involved in the website generation

If you wish to change something about the generated website, this brief summary of the files and directories involved may help you.

`catalog`: This folder, located at the root of this repository, contains all templates, divided by categories. Add a new folder to add a new category, or add a template to its corresponding category, and the script will pick it up when run again.

`website/resources`: This folder contains various resources used in generating the website. Most notably, the `stylesheets` subfolder contains CSS files.
