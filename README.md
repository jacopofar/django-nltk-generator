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

If you use the provided grammar, which describes arithmetical expressions, and use "hello world" as seed, you get *sin(4.25 + 3.2 + 4 * sqrt(9.8 + 3.8) * sin(9.8 * 1 * sin(sqrt(8.5)) + 8 + sin(sin(2.9) + 9.8 + 7 * 7 * 98 + 8 + 78 + 9.0 + 8.2 * sqrt(9467.4) * sin(6)) + 0 + 3.7) + 4.5)*

That's it!

__License__: Apache 2.0