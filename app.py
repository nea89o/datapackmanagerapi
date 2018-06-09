from flask import Flask, abort

from api import bp as api_blueprint

app = Flask(__name__)


@app.route('/')
def index():
    abort(404)


app.register_blueprint(api_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run()
