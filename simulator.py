import time
import random
import json
import paho.mqtt.client as mqtt

# Configuración del broker (apunta a localhost para correr en la PC del profesor)
BROKER_HOST = "localhost"
BROKER_PORT = 1883

# Tópicos MQTT del contrato
TOPIC_TEMP = "esp32/dht11/temperature"
TOPIC_HUM = "esp32/dht11/humidity"
TOPIC_LED_CONTROL = "esp32/led/control"
TOPIC_LED_STATUS = "esp32/led/status"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[OK] Conectado al broker Mosquitto.")
        client.subscribe(TOPIC_LED_CONTROL)
        print(f"[OK] Suscrito a '{TOPIC_LED_CONTROL}' para escuchar comandos del Dashboard.")
    else:
        print(f"[ERROR] Falló la conexión al broker. Código rc: {rc}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8')
    print(f"\n[COMANDO LED RECIBIDO] Tópico: {msg.topic} | Dato: {payload}")
    
    # Simular que el hardware ejecuta el cambio y confirma su estado real
    print(f"[SIMULADOR] Confirmando estado del LED en '{TOPIC_LED_STATUS}'...")
    client.publish(TOPIC_LED_STATUS, payload)

def main():
    client = mqtt.Client("Simulador_Software")
    client.on_connect = on_connect
    client.on_message = on_message

    print(f"Conectando al broker en {BROKER_HOST}:{BROKER_PORT}...")
    client.connect(BROKER_HOST, BROKER_PORT, 60)
    
    # Iniciar hilo de escucha para mensajes entrantes del LED
    client.loop_start()

    print("Iniciando publicación de datos DHT11 simulados (Ctrl+C para detener)...")
    try:
        while True:
            temp = round(random.uniform(20.0, 30.0), 1)
            hum = round(random.uniform(40.0, 65.0), 1)

            client.publish(TOPIC_TEMP, json.dumps({"temperature": temp}))
            client.publish(TOPIC_HUM, json.dumps({"humidity": hum}))

            print(f"[PUBLICADO] Temp: {temp}°C | Hum: {hum}%")
            time.sleep(3)
            
    except KeyboardInterrupt:
        print("\nSimulador detenido.")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()