# utils/sockets.py
import socket
import threading
import json
from datetime import datetime
import sqlite3

DB_PATH = "db/domotilite.db"

def handle_client_connection(conn, addr):
    print(f"[APP] Connexion entrante de {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            try:
                sensor_data = json.loads(data.decode('utf-8'))
                print(f"[APP] Données reçues : {sensor_data}")
                save_sensor_data(sensor_data)
            except Exception as e:
                print(f"[ERREUR] {e}")

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

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 65432))
    server.listen()
    print("[APP] Serveur socket en écoute sur le port 65432")

    while True:
        conn, addr = server.accept()
        client_thread = threading.Thread(target=handle_client_connection, args=(conn, addr))
        client_thread.start()
