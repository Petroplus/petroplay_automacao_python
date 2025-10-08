import base64
from fastapi import WebSocket
import numpy as np
import cv2
import json
from app.feature.get_plate_socket.connection_state import ConnectionState
from app.feature.get_plate_socket.datasource.validate_token import ValidateToken
from app.feature.get_plate_socket.find_plate_in_image_bgr import Find_plate_in_image_bgr


class Websocket_plate_detector:
    async def init_socket(self, ws: WebSocket):
        await ws.accept()
        print("✅ Cliente conectado")
        find_plate_in_image_bgr = Find_plate_in_image_bgr()
        state = ConnectionState(consensus_frames=4)
        try:
            data_text = await ws.receive_text()

            try:
                data = json.loads(data_text)
            except json.JSONDecodeError:
                print("❌ Erro: JSON inválido na primeira mensagem")
                await ws.close(code=4000)
                return
            
            token = data.get("token")
            if not token:
                print("❌ Token ausente — conexão encerrada")
                await ws.close(code=4001)
                return
            else:
                validateToken = ValidateToken()
                response = validateToken.token(token)
                if response != 200:
                    print("❌ Token ausente — conexão encerrada")
                    await ws.close(code=4001)
                    return

            print(f"🔐 Token recebido: {token}")
            await ws.send_text('true')

            while True:
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
                arr = np.frombuffer(img_bytes, np.uint8)
                img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
                if img is None:
                    print("⚠️ Imagem inválida")
                    await ws.send_text(json.dumps({"error":"invalid_image"}))
                    continue
                found = find_plate_in_image_bgr.initialize(img)
                plate = found[0] if found else None
                print(f"🔍 Detecção OCR: {plate}")

                state.push(plate)
                confirmed = state.consensus_plate()
                if confirmed:
                    print(f"✅ Placa confirmada: {confirmed}")
                    await ws.send_text(json.dumps({"plate": confirmed}))
                    state.last_detections.clear()
                else:
                    await ws.send_text(json.dumps({"detected": plate}))
        except Exception as e:
            print(f"❌ Erro WebSocket: {e}")
            await ws.close()
