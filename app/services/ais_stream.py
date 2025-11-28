import os
import asyncio
import websockets
import json
from websockets.exceptions import ConnectionClosedError
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

API_KEY = os.getenv("AISSTREAM_API_KEY")
URL = "wss://stream.aisstream.io/v0/stream"

"""
https://aisstream.io/documentation#AISMessage
https://aisstream.io/coverage
"""

async def connect_ais_stream():
    subscribe_message = {
        "APIKey": API_KEY,
        "BoundingBoxes": [[[-10, -80], [-45, 20]]],
        "FilterMessageTypes": ["PositionReport"],
    }

    while True:
        try:
            async with websockets.connect(URL) as websocket:
                subscribe_message_json = json.dumps(subscribe_message)
                await websocket.send(subscribe_message_json)

                async for message_json in websocket:
                    message = json.loads(message_json)
                    message_type = message.get("MessageType")

                    if message_type == "PositionReport":
                        print(
                            f"Nome: {(message['MetaData']['ShipName']).strip()}, "
                            f"MMSI: {message['MetaData']['MMSI']}, "
                            f"Latitude: {message['MetaData']['latitude']}, "
                            f"Longitude: {message['MetaData']['longitude']}, "
                            f"Timestamp (UTC): {message['MetaData']['time_utc']}"
                        )
                        # await asyncio.sleep(0.5)

        except ConnectionClosedError as e:
            print(f"[WARN] Conexão fechada: {e}. Tentando reconectar em 5s...")
            await asyncio.sleep(5)
        except ConnectionAbortedError as e:
            print(f"[WARN] Conexão abortada pelo host: {e}. Tentando reconectar em 5s...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"[ERROR] Erro inesperado: {e}. Tentando reconectar em 10s...")
            await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(connect_ais_stream())
