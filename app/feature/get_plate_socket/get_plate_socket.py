import base64
from fastapi import WebSocket
# import numpy as np
import json
import asyncio
from app.feature.get_plate_socket.datasource.validate_token import ValidateToken
from app.feature.get_plate_socket.llm import GetPlateLLm


class Websocket_plate_detector:
    async def init_socket(self, ws: WebSocket):
        await ws.accept()
        print("✅ Cliente conectado")
        cont = 0
        try:
            data_text = await ws.receive_text()

            try:
                data = json.loads(data_text)
            except json.JSONDecodeError:
                print("❌ Erro: JSON inválido na primeira mensagem")
                await ws.send_text(json.dumps({"error": "JSON inválido na primeira mensagem"}))
                await ws.close(code=4000)
                return
            
            token = data.get("token")
            if not token:
                print("❌ Token ausente — conexão encerrada")
                await ws.send_text(json.dumps({"token": False}))
                await ws.send_text(json.dumps({"error": "Sem permissão = 401"}))
                await ws.close(code=4001)
                return
            else:
                validateToken = ValidateToken()
                response = validateToken.token(token)
                await asyncio.sleep(1)
                if response != 200:
                    print("❌ Token ausente — conexão encerrada")
                    await ws.send_text(json.dumps({"error": "Erro ao validar o token"}))
                    await ws.close(code=4001)
                    return

            print(f"🔐 Token recebido: {token}")
            await ws.send_text(json.dumps({"token": True}))

            while True:
                await asyncio.sleep(1)
                data = await ws.receive_text()
                print("📩 Frame recebido")
                payload = json.loads(data)
                b64 = payload.get("frame")
                if not b64:
                    print("⚠️ Nenhum frame encontrado no payload")
                    await ws.send_text(json.dumps({"error":"no_frame"}))
                    continue

                header_removed = b64.split(",")[-1]
                img_bytes = base64.b64decode(header_removed)

                returnPlate = await GetPlateLLm.detect_plate_from_image(img_bytes)

                # returnPlate = {'plate': None}

                if returnPlate['plate'] is not None:
                    await ws.send_text(json.dumps({"plate": returnPlate['plate']}))
                    print(f"Placa detectada: {returnPlate['plate']}, encerrando loop")
                    break
                else:
                    await ws.send_text(json.dumps({"noDetected": 'none'}))




                await asyncio.sleep(1)

                cont = cont + 1

                if cont > 3:
                # if cont > 30:
                    await ws.send_text(json.dumps({"error": "Quantidade de tentativas excedida"}))
                    await ws.close()
                    break
                    
        except Exception as e:
            print(f"❌ Erro WebSocket: {e}")
            await ws.send_text(json.dumps({"error": "Erro desconhecido"}))
            await ws.close()
