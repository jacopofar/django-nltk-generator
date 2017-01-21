This Django applications shows how it is possible to generate a text from a NLTK grammar.

How to run
=========

You need Python 3, then configure the environment:
```
git clone https://github.com/jacopofar/django-nltk-generator.git
cd django-nltk-generator
python3 -m venv venv 
source venv/bin/activate
```

to install the dependencies:
```
pip3 install -r requirements.txt
```
Now run the application:
```
cd nltkgen && python3 manage.py runserver
```

Visit `http://localhost:8000/generator/` and you will see the interface:

![alt text](https://github.com/jacopofar/django-nltk-generator/raw/master/screen.png "What you should see in your browser")
