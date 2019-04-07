# hackthon-project
Slashed: A marketplace that provides clothing at a discounted rate for people in need. 

## Table of Contents
* [Tech Stack](#techstack) 
* [Setting Up/Installation](#installation)
* [Demo](#demo)


## TechStack
* Frontend: HTML5, JavaScript, Jinja, jQuery, Bootstrap 
* Backend: Python, Flask, SQLite3, SQLAlchemy 

## Installation 

Note: Also deployed via Digital Ocean. 
```
http://159.89.154.13:5000/
```

To run Slashed on local computer, follow the below steps:

Clone repository: 
```
$ https://github.com/olivia-ea/hackthon-project.git
```

Set up virtual environment: 

```
$ virtualenv env
```

Activate virtual envirnoment:
```
$ source venv/bin/activate
```

Install dependencies:
```
$ pip install -r requirements.txt
```

Create database 'users':
```
$ createdb users
```

Create your database tables:
```
$ python3 model.py
```

Run from the command line:
```
$ python3 server.py
```

Open localhost:5000 on browser.

## Demo

![](slashed-1.gif)

![](slashed-2.gif)

![](slashed-3.gif)
