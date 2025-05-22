# utils/sockets.py

import socket
import threading
import json
import sqlite3

from utils.automation import evaluate_rules
from utils.devices import update_device_state, get_devices


DB_PATH = "db/domotilite.db"

def handle_client_connection(conn, addr, ui_callback=None):
    print(f"[APP] Connexion entrante de {addr}")
    if ui_callback:
        ui_callback(f"[Connexion capteur] {addr}")

    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            try:
                sensor_data = json.loads(data.decode('utf-8'))
                print(f"[APP] Données reçues : {sensor_data}")

                if ui_callback:
                    ui_callback("__CLEAR__")
                    ui_callback(f"[Capteurs] {sensor_data}")

                save_sensor_data(sensor_data)

                # Appliquer les règles automatiques
                actions = evaluate_rules(sensor_data)
                devices = get_devices()

                for target_type, new_state in actions:
                    for device in devices:
                        id_, name, type_, state = device
                        if target_type.lower() in name.lower() or target_type.lower() in type_.lower():
                            update_device_state(id_, new_state)
                            if ui_callback:
                                ui_callback(f"[Action auto] {name} → {new_state}")


            except Exception as e:
                print(f"[ERREUR] {e}")
                if ui_callback:
                    ui_callback(f"[ERREUR] {e}")


def save_sensor_data(data):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for sensor_type, value in data.items():
        cur.execute(
            "INSERT INTO sensor_data (type, value) VALUES (?, ?)",
            (sensor_type, value)
        )
    conn.commit()
    conn.close()

def start_server(ui_callback=None):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 65432))
    server.listen()
    print("[APP] Serveur socket en écoute sur le port 65432")

    while True:
        conn, addr = server.accept()
        client_thread = threading.Thread(
            target=handle_client_connection,
            args=(conn, addr, ui_callback)
        )
        client_thread.start()

