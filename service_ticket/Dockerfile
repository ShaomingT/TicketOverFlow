FROM python:3.10
WORKDIR /app
COPY . .

RUN pip3 install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

CMD ["gunicorn", "app:wsgi_app", "-b", "0.0.0.0:9999", "--workers", "5", "--threads", "2",  "--log-level", "info"]

