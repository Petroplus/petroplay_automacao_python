import uvicorn
from fastapi import FastAPI


from routes_socket import RoutesSocket


if __name__ == "__main__":
    app = FastAPI()
    routesSocket = RoutesSocket(app)
    routesSocket.register_routes()
    uvicorn.run(app, host="0.0.0.0", port=5000)
