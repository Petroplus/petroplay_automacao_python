from flask import jsonify

class Routes:
    def __init__(self, app):
        self.app = app
        self.register_routes()

    def register_routes(self):
        @self.app.route('/', methods=['GET'])
        def home():
            return jsonify({"message": "pong"})



