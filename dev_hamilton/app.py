from flask import Flask, request

app = Flask(__name__)


@app.route('/api/v1/hamilton/concerts/<string:concert_id>', methods=['POST'])
def concerts(concert_id):
    s = f'begin render seating {concert_id}'
    print(s)
    return f'begin render seating {concert_id}', 202


@app.route('/api/v1/hamilton/tickets/<string:ticket_id>', methods=['POST'])
def ticket(ticket_id):
    s = f'begin render tickets {ticket_id}'
    print(s)
    return f'begin render tickets {ticket_id}', 202


def wsgi_app(environ, start_response):
    return app(environ, start_response)


if __name__ == '__main__':
    app.run(port=6666)
