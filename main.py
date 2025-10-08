import uvicorn
import os
from fastapi import FastAPI


from routes_socket import RoutesSocket


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000)) 
    app = FastAPI()
    routesSocket = RoutesSocket(app)
    routesSocket.register_routes()
    uvicorn.run(app, host="0.0.0.0", port=port)
