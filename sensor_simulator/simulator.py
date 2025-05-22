# sensor_simulator/simulator.py
import socket
import time
import random
import json

HOST = 'localhost'
PORT = 65432  # même port que côté client GUI

def generate_fake_data():
    return {
        "temperature": round(random.uniform(18.0, 30.0), 2),
        "luminosity": random.randint(0, 100)
    }

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"[SIMULATEUR] Connecté à {HOST}:{PORT}")
        
        while True:
            data = generate_fake_data()
            s.sendall(json.dumps(data).encode('utf-8'))
            print(f"[SIMULATEUR] Données envoyées : {data}")
            time.sleep(5)  # attend 5 secondes avant d’envoyer les prochaines

if __name__ == "__main__":
    main()
