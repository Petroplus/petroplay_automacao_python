import json
import re
# import openai
from openai import OpenAI
import base64
import requests
import ast
import os
from dotenv import load_dotenv

load_dotenv()

class GetPlateLLm:
    @staticmethod
    async def detect_plate_from_image(image_bytes: bytes) -> dict:
        """
        Envia a imagem para GPT-4V e retorna JSON {"plate": "XXX0000"} ou {"plate": null}
        """
        try:
            api_key = os.getenv("API_KEY_OPENAI")
            
            client = OpenAI(api_key=api_key)

            base64_image = base64.b64encode(image_bytes).decode("utf-8")

            response = client.responses.create(
                model="gpt-4.1",
                # model = 'gpt-5-nano',
                input=[
                    {
                        "role": "user",
                        "content": [
                            { "type": "input_text", "text": "Detecte a placa nesta imagem e retorne no SEMPRE o formato JSON {'plate': 'XXX0000'} ou mercosul {'plate': 'XXX0X00'} ou {'plate': None}, jamais retornar texto." },
                            {
                                "type": "input_image",
                                "image_url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        ],
                    }
                ],
            )

            print(response.output_text)

            reais_por_500 = 0.0011
            dolar_por_500 = 0.00019

            # Tokens usados
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            total_tokens = response.usage.total_tokens

            # Cálculo dos custos
            custo_reais = (total_tokens / 500) * reais_por_500
            custo_dolar = (total_tokens / 500) * dolar_por_500

            log = f'''
            ✳️✳️✳️✳️✳️✳️✳️✳️✳️
            Resposta:
            {response.output_text}

            Registro de uso:
            Token input: {input_tokens}
            Token output: {output_tokens}
            Token total: {total_tokens}

            💵💵💵💵💵💵💵💵💵
            Gastos:
            R$ {custo_reais:.6f}
            $ {custo_dolar:.6f}
            '''

            print(log)

            GetPlateLLm.myLogger(log)

            match = re.search(r'\{.*\}', response.output_text, re.DOTALL)
            if match:
                raw_json = match.group(0).strip()

                try:
                    data = json.loads(raw_json)
                except json.JSONDecodeError:
                    data = ast.literal_eval(raw_json)

                return {"plate": data.get("plate")}

                return {"plate": data.get("plate")}
            return {"plate": None, "success": False, "error": "JSON não encontrado"}

        except Exception as e:
            return {"plate": None, "success": False, "error": str(e)}
        


    @staticmethod
    def myLogger(content):
        url = "https://discord.com/api/webhooks/1430173594679246848/2wlc0p5VN5NahxzRgAdPabTSFIKnozBTBWZBtIa8wR6YSGJg9XfAgV2SIWEoCNJc61UZ" 

        payload = {
            "content": content,
            "username": "API LLM",
            "avatar_url": "https://raw.githubusercontent.com/hallanabreu2020/hallanabreu2020/main/eu.png"
        }

        try:
            response = requests.post(url, data=json.dumps(payload), headers={"Content-Type": "application/json"})
            print("Status:", response.status_code)
            print("Resposta:", response.text)
        except Exception as e:
            print("Erro ao enviar:", e)



