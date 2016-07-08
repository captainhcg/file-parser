
## Tech Stack
This project is implemented by python 2.7, running on [Flask](http://flask.pocoo.org/) and [Sqlite](https://www.sqlite.org/). Dependencies are listed in `requirements.txt`
```
Flask             # web framework
flask-sqlalchemy  # orm
flask-script      # command line tools
coverage          # test coverage
mock              # test tools
``` 
***
## Setup
It is recommended to setup this project in virtual environment. Then locate to project folder and install dependencies.
```
> pip install -r requirements.txt
```
Init static database (there is only one static database in this project, which is `Specification`)
```
> python manage.py init_database
```
It is required to manually import Specification field into system. Command line is `python manage.py select_all -f [spec_name]`. Notice that alphanumeric characters are allowed in spec_name. By default specification files are located in `./specs`.
```
> python manage.py import_specification -f testspec
```
To import data files, simply run `./manage.py import_files`. All valid files located at `./data` will be imported.
```
> python manage.py import_files
```
To review the records imported, simply run `python manage.py select_all -f [spec_name]`. Notice that unicode characters are supported.
```
> python manage.py select_all -f testspec

name      |valid|count
----------|-----|-----
Foony     |True |    1
Barzane   |False|  -12
Quuxitude |True |  103
一二三四五六七八九十|True |  103
```
***
## Test

Every module except `manage.py` has a mirror test script located ar `./tests`. Test coverage is 83% at the moment.
```
> coverage run --source . -m --omit="tests/*" tests.test
> coverage report

Name               Stmts   Miss  Cover
--------------------------------------
__init__.py            0      0   100%
app.py                 7      0   100%
column.py             40      1    98%
importer.py           41      2    95%
manage.py             27     27     0%
models.py              8      2    75%
settings.py           18      0   100%
specification.py     105      9    91%
--------------------------------------
TOTAL                246     41    83%
```