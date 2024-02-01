
from flask import Flask, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix

"""
  
"""
def create_app():
    app = Flask(__name__)
    # According tothe Flask documents, this tells the app to trust the 
    # headers from the proxy server
    # See https://flask.palletsprojects.com/en/2.3.x/deploying/proxy_fix/
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )

    @app.route('/data')
    def index():
        return jsonify({'data': 'Hello, World!'})
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)