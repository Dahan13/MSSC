# MSSC

## Requirements

- python 3.7 or higher
- A working installation of pip

## How to launch the application

Download the project archive and dezip it.

Open a console command in the project main directory

First install the requirements :

```bash
$ pip install -r requirements.txt
```

Then launch the application. Either execute the .bat file if you are on windows, or type :
```bash
$ python -m shiny run --port 5000 --host localhost --reload app.py
```

You can now find the application at the URL : http://localhost:5000