# utils/devices.py

import sqlite3

DB_PATH = "db/domotilite.db"

def get_devices():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, name, type, state FROM devices")
    devices = cur.fetchall()
    conn.close()
    return devices

def add_device(name, type_, state="OFF"):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO devices (name, type, state) VALUES (?, ?, ?)", (name, type_, state))
    conn.commit()
    conn.close()

def delete_device(device_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM devices WHERE id = ?", (device_id,))
    conn.commit()
    conn.close()

def update_device_state(device_id, new_state):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE devices SET state = ? WHERE id = ?", (new_state, device_id))
    conn.commit()
    conn.close()
