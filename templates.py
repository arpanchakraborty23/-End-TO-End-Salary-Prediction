import os
from pathlib import Path
import logging

list_to_files=[
    ".github/.gitkeep",
    'config/config.yaml',
    'templates/index.html',
    'NoteBooks/Eda.ipynb',
    'src/__init__.py',
    'src/pipline/__init__.py',
    'src/components/__init__.py',
    'src/constant/__init__.py',
    'src/configure/__init__.py',
    'src/entity/__init__.py',
    'src/logging/__init__.py',
    'src/logging/logger.py',
    'src/exception/__init__.py',
    'src/exception/exception.py',
    'src/utils/__init__.py',
    'src/utils/utils.py',
    'params.yaml',
    '.gitignore',
    'main.py',
    'app.py',
    'requirements.txt',
    'setup.py'
]

for filepath in list_to_files:
    filepath=Path(filepath)
    fildir,filename=os.path.split(filepath)
    if fildir !='':
        os.makedirs(fildir,exist_ok=True)

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
            with open(filepath, "w") as f:
                pass    