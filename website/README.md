# Hub website

This directory is dedicated to generating the website for the hub.

## Generate website files

First, convert *Jupyter* notebook files to HTML. Install *Jupyter*:

```
pip install jupyter
```

Then, run the following from the root of the repository:

```
jupyter nbconvert ./**/notebook.ipynb --to html
```

The **generate-docs.py** file is a Python script that will create a directory called `generated`, containing a *MkDocs* website for the hub.

```
cd website
python generate-docs.py
```

You will need *MkDocs* and the *mkdocs-material* theme to run the website locally. Install them as follows:

``` 
pip install mkdocs
pip install mkdocs-material
```

Now, start the website:

```
cd generated
mkdocs serve
```

You will find the website at `http://localhost:8000`.

## Files involved in the website generation

If you wish to change something about the generated website, this brief summary of the files and directories involved may help you.

`catalog`: This folder, located at the root of this repository, contains all templates, divided by categories. Add a new folder to add a new category, or add a template to its corresponding category, and the script will pick it up when run again.

`website/resources`: This folder contains various resources used in generating the website. Most notably, the `stylesheets` subfolder contains CSS files.
