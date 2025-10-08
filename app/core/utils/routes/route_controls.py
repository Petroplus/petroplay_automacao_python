from flask_cors import CORS
from app.feature.get_plate.routes.times_routes import GetPlateRoutes
from routes import Routes
from flask import Flask 


class RouteControls:
    @staticmethod
    def initialize():
        app = Flask(__name__)
        CORS(app)
        Routes(app)
        GetPlateRoutes(app)
        return app
