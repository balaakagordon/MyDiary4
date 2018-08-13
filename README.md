# MyDiary_GB

MyDiary is an online application where users can note down their thoughts and feelings. Set up your account and begin documenting your emotions.

[![Build Status](https://travis-ci.org/balaakagordon/challenge3.svg?branch=finish_feedback)](https://travis-ci.org/balaakagordon/challenge3)
[![Coverage Status](https://coveralls.io/repos/github/balaakagordon/challenge3/badge.svg)](https://coveralls.io/github/balaakagordon/challenge3)


## Getting Started
These instructions will help you get the application running on your local machine for development and testing.

### Prerequisites
* [Python](https://www.python.org/getit/)
* [Pip](https://pip.pypa.io/en/stable/installing/)

### Setup
* Clone the remote repository on [GitHub](https://github.com/new)
```
    $ git clone https://github.com/balaakagordon/test.git
    $ cd MyDiary_GB
```

* Create a virtual environment for your application and install all relevant requirements
```
    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
```

### Database
* Set up a database to hold your data
```
CREATE DATABASE mydiary_db
```

* Run the application on a local server
```
    $ python mydiaryapp/app.py
```
Check that the application is now be running on the localhost server(http://127.0.0.1:5000)

### Testing
* Run tests on api endpoints to ensure methods work
```
    $ curl -i http://localhost:5000/api/v1/entries/1
    $ curl -i http://localhost:5000/api/v1/entries
    $ curl -i -H "Content-Type: application/json" -X POST -d '{"entrytitle":"Plan for today", "entrydata":"Read a book"}' http://localhost:5000/api/v1/entries
    $ curl -i -H "Content-Type: application/json" -X PUT -d '{"entrytitle":"Today Was Fun", "entrydata":"Went shopping and bought lots of stuff!"}' http://localhost:5000/api/v1/entries/1
```

| Method       | Endpoint           | Description  |
| ------------- |:-------------:| -----|
| GET      | home/api/v1/entries | Get all entries
| GET      | home/api/v1/entries/<entry_id>      | Get specific entry using an id |
| POST | home/api/v1/entries      | Create a new entry |
| PUT      | home/api/v1/entries/<entry_id>      | Edit an entry using an id |

* Run tests on the application and check the test coverage
```
    $ nosetests -v --with-coverage --cover-package=mydiaryapp/tests
```

This application can also be found on [Heroku](https://mydiary3-gbalaaka.herokuapp.com/api/v1/entries)
The app's templates can be seen on [GitHub pages](https://balaakagordon.github.io/MyDiary_GB/)
This application can also be found on [Heroku](https://mydiary3-gbalaaka.herokuapp.com/api/v1/entries)
The api documentation may be found on [Apiary](https://mydiary17.docs.apiary.io/#)