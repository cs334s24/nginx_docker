
from flask import Flask, jsonify

def create_app():
    app = Flask(__name__)

    @app.route('/data')
    def index():
        return jsonify({'data': 'Hello, World!'})
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)