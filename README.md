# BUDGETracker
My Django App

## Prerequisites

Install Python version 3.8.0 (https://www.python.org/)

Create a virtual environment in your working directory and install Django version 2.2 in it

On macOS: 

```
pip3 install pipenv                                                        
$ pipenv install django==2.2                                                       
$ pipenv shell                                                                              
```
## Install dependencies stored in the Pipfile

```
(virt_env) $ pipenv sync
```
## Perform database migration:

```
(virt_env) $ python manage.py migrate   
```

## Run Development Server

```
(virt_env) $ python manage.py runserver
```

## Access the webpage

```
http://127.0.0.1:8000/
```
