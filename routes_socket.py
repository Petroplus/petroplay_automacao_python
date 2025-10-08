from app.feature.get_plate_socket.get_plate_socket import Websocket_plate_detector

class RoutesSocket:
    def __init__(self, app):
        self.app = app
        self.register_routes()

    def register_routes(self):
        websocket_plate_detector = Websocket_plate_detector()
        self.app.websocket("/ws/plates")(websocket_plate_detector.init_socket)



