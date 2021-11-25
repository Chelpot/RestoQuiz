release: python menuQuiz/manage.py migrate
web: gunicorn --chdir menuQuiz menuQuiz.wsgi --log-file -