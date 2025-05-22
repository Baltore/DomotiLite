import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import threading
from utils.sockets import start_server
from utils.devices import get_devices, add_device, delete_device, update_device_state


PRIMARY_COLOR = "#4A90E2"
BG_COLOR = "#F7F9FB"
TEXT_COLOR = "#2C3E50"
FONT = ("Segoe UI", 10)

latest_temp = "21°C"
latest_light_state = "ON"

def turn_on_light():
    print("Lumière allumée")


def open_device_manager():
    window = tk.Toplevel(bg=BG_COLOR)
    window.title("Gestion des appareils")
    window.geometry("550x300")

    def refresh():
        for widget in device_frame.winfo_children():
            widget.destroy()
        for i, (id_, name, type_, state) in enumerate(get_devices()):
            tk.Label(device_frame, text=f"{name} ({type_})", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT).grid(row=i, column=0, sticky="w")
            tk.Label(device_frame, text=f"État: {state}", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT).grid(row=i, column=1)
            ttk.Button(device_frame, text="ON", command=lambda id_=id_: update_device_state(id_, "ON") or refresh()).grid(row=i, column=2)
            ttk.Button(device_frame, text="OFF", command=lambda id_=id_: update_device_state(id_, "OFF") or refresh()).grid(row=i, column=3)
            ttk.Button(device_frame, text="Supprimer", command=lambda id_=id_: delete_device(id_) or refresh()).grid(row=i, column=4)

    def ajouter_appareil():
        name = entry_name.get()
        type_ = entry_type.get()
        if name and type_:
            add_device(name, type_)
            refresh()

    form_frame = tk.Frame(window, bg=BG_COLOR)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Nom", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT).grid(row=0, column=0)
    entry_name = tk.Entry(form_frame, font=FONT)
    entry_name.grid(row=0, column=1, padx=5)

    tk.Label(form_frame, text="Type", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT).grid(row=0, column=2)
    entry_type = tk.Entry(form_frame, font=FONT)
    entry_type.grid(row=0, column=3, padx=5)

    ttk.Button(form_frame, text="Ajouter", command=ajouter_appareil).grid(row=0, column=4, padx=5)

    device_frame = tk.Frame(window, bg=BG_COLOR)
    device_frame.pack(fill="both", expand=True, padx=10)
    refresh()


def update_time_label():
    now = datetime.now()
    hour = now.strftime("%H:%M")
    is_night = now.hour < 6 or now.hour >= 20
    emoji = "🌙 Nuit" if is_night else "☀️ Jour"
    time_label.config(text=f"{emoji} - {hour}")
    root.after(60000, update_time_label)


def update_dynamic_labels():
    global latest_temp, latest_light_state

    # Mise à jour température affichée
    temp_label.config(text=latest_temp)

    # Mise à jour état lumière
    light_status_label.config(text=latest_light_state)

    root.after(5000, update_dynamic_labels)


root = tk.Tk()
root.title("DomotiLite")
root.configure(bg=BG_COLOR)
root.geometry("420x450")

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=FONT, foreground=TEXT_COLOR, background=PRIMARY_COLOR)
style.map("TButton", background=[("active", "#357ABD")])

frame = tk.Frame(root, bg=BG_COLOR)
frame.pack(padx=20, pady=20, fill="both", expand=True)

# Entête
header = tk.Label(frame, text="DomotiLite", font=("Segoe UI", 16, "bold"), bg=PRIMARY_COLOR, fg="white", padx=10, pady=5)
header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))

# Bloc capteur température
temp_frame = tk.Frame(frame, bg="white", bd=1, relief="groove")
temp_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
tk.Label(temp_frame, text="Temperature", font=FONT, bg="white", fg=TEXT_COLOR).pack(pady=5)
temp_label = tk.Label(temp_frame, text="21°C", font=("Segoe UI", 12, "bold"), bg="white", fg=TEXT_COLOR)
temp_label.pack()

# Bloc lumière
light_frame = tk.Frame(frame, bg="white", bd=1, relief="groove")
light_frame.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")
tk.Label(light_frame, text="Lighting", font=FONT, bg="white", fg=TEXT_COLOR).pack(pady=5)
light_status_label = tk.Label(light_frame, text="ON", font=("Segoe UI", 12, "bold"), bg="white", fg=TEXT_COLOR)
light_status_label.pack()

# Boutons
tk.Button(frame, text="Turn Off Light", font=FONT, bg=PRIMARY_COLOR, fg="white", command=lambda: print("Lumière éteinte"))\
    .grid(row=2, column=0, pady=5, sticky="ew")
tk.Button(frame, text="Manage Devices", font=FONT, bg="white", fg=TEXT_COLOR, command=open_device_manager)\
    .grid(row=2, column=1, pady=5, sticky="ew")

# Zone de logs capteurs
log_frame = tk.LabelFrame(frame, text="Sensor Info", bg=BG_COLOR, font=FONT, fg=TEXT_COLOR)
log_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="nsew")

output_text = tk.Text(log_frame, height=6, width=50, state="disabled", bg="white", fg=TEXT_COLOR, font=("Consolas", 9))
output_text.pack(fill="both", expand=True, padx=5, pady=5)


def append_output(msg):
    global latest_temp, latest_light_state

    output_text.configure(state="normal")
    if msg == "__CLEAR__":
        output_text.delete(1.0, tk.END)
    else:
        output_text.insert(tk.END, msg + "\n")
        output_text.see(tk.END)

        if "[Capteurs]" in msg:
            try:
                import json
                data_str = msg.split("[Capteurs]")[1].strip()
                data = json.loads(data_str.replace("'", "\""))
                if "temperature" in data:
                    latest_temp = f"{round(data['temperature'], 1)}°C"
            except:
                pass

        if "[Action auto]" in msg and "lumière" in msg.lower():
            if "ON" in msg:
                latest_light_state = "ON"
            elif "OFF" in msg:
                latest_light_state = "OFF"

    output_text.configure(state="disabled")


# État heure/jour/nuit
time_label = tk.Label(frame, text="", font=("Segoe UI", 10), bg=BG_COLOR, fg=TEXT_COLOR)
time_label.grid(column=0, row=4, columnspan=2, pady=(5, 0))
update_time_label()

# Serveur socket
server_thread = threading.Thread(target=lambda: start_server(ui_callback=append_output), daemon=True)
server_thread.start()

# Lancer le rafraîchissement des labels dynamiques
update_dynamic_labels()

root.mainloop()