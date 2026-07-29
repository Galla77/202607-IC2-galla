import time
import random
import paho.mqtt.client as mqtt

BROKER = "localhost" # Modificar si el broker está en otra IP
PORT = 1883

client = mqtt.Client("Simulador_Software")
client.connect(BROKER, PORT)

while True:
    temp = round(random.uniform(15.0, 30.0), 2)
    hum = round(random.uniform(40.0, 70.0), 2)
    
    # Publicación de datos en texto simple, exactamente igual que el main.py
    client.publish("esp32/dht11/temperature", str(temp))
    client.publish("esp32/dht11/humidity", str(hum))
    
    # Publicación del estado
    client.publish("esp32/status", "ONLINE")
    
    print(f"Publicado -> Temp: {temp}°C | Hum: {hum}%")
    
    # Intervalo de 3 segundos para coincidir con la variable 'intervalo = 3000' de tu ESP32
    time.sleep(3)