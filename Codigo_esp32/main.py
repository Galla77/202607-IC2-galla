import network
import time
import machine
import dht
from umqtt.simple import MQTTClient
from machine import Pin
     
# =========================
# WIFI
# =========================
WIFI_SSID = "UNRaf_Libre"     # <--- Poné el nombre de tu Wi-Fi del celular
WIFI_PASS = "unraf2021"

# =========================
# MQTT (Tópicos como strings para consistencia)
# =========================
MQTT_BROKER = "10.103.26.134"
CLIENT_ID = "ESP32Client"

TOPIC_TEMP = "esp32/dht11/temperature"
TOPIC_HUM = "esp32/dht11/humidity"
TOPIC_LED_CONTROL = "esp32/led/control"
TOPIC_LED_STATUS = "esp32/led/status"
TOPIC_STATUS = "esp32/status"

# =========================
# HARDWARE
# =========================
LED_PIN = 2
DHT_PIN = 4

led = machine.Pin(LED_PIN, machine.Pin.OUT)
sensor = dht.DHT11(machine.Pin(DHT_PIN))

# =========================
# VARIABLES
# =========================
intervalo = 3000
last_read = 0
client = None  # Definición inicial del objeto cliente

# =========================
# WIFI
# =========================
def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Buscando red Wi-Fi...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        # Esperar hasta 10 segundos a que conecte
        intentos = 0
        while not wlan.isconnected() and intentos < 10:
            print("Conectando al Wi-Fi... Segundo", intentos)
            time.sleep(1)
            intentos += 1
            
    if wlan.isconnected():
        print("\n[Wi-Fi OK] Conectado con éxito a la red.")
        print("Datos de red (IP, Máscara, Gateway, DNS):", wlan.ifconfig())
    else:
        print("\n[Wi-Fi FALLÓ] No se pudo conectar. Revisá los datos.")
        raise Exception("Error de conexión Wi-Fi")

# =========================
# CALLBACK MQTT
# =========================
def callback(topic, msg):
    global client  # Indicar que usamos el cliente global
    
    topic = topic.decode()
    msg = msg.decode()
    
    print("Mensaje recibido:", topic, msg)
        
    
    if topic == TOPIC_LED_CONTROL:
        if msg == "ON":
            led.value(1)
            client.publish(TOPIC_LED_STATUS, "ON")
            print("LED ON")
        elif msg == "OFF":
            led.value(0)
            client.publish(TOPIC_LED_STATUS, "OFF")
            print("LED OFF")

# =========================
# MQTT
# =========================
def conectar_mqtt():
    global client
    try:
        print("Conectando al bróker MQTT...")
        client = MQTTClient(CLIENT_ID, MQTT_BROKER)
        client.set_callback(callback)
        client.connect()
        client.subscribe(TOPIC_LED_CONTROL)
        
        # Avisar que el ESP32 está online
        client.publish(TOPIC_STATUS, "ONLINE")
        print("MQTT conectado")
        return True
    except Exception as e:
        print("Error conectando a MQTT:", e)
        return False

# =========================
# INITIALIZATION
# =========================
conectar_wifi()
conectar_mqtt()

# =========================
# MAIN
# =========================
while True:
    try:
        # Verificar estado de conexión antes de operar
        wifi = network.WLAN(network.STA_IF)
        if not wifi.isconnected():
            print("[ALERTA] WiFi caído. Reconectando...")
            if conectar_wifi():
                conectar_mqtt()
            time.sleep(2)
            continue

        if client is None:
            conectar_mqtt()
            time.sleep(2)
            continue

        # Procesar mensajes entrantes del Broker
        client.check_msg()
        
        # Manejo de tiempo no bloqueante para el DHT11
        now = time.ticks_ms()
        if time.ticks_diff(now, last_read) > intervalo:
            try:
                sensor.measure()
                temp = sensor.temperature()
                hum = sensor.humidity()
                
                print("Temp:", temp, "°C | Hum:", hum, "%")
                
                # Publicar lecturas
                client.publish(TOPIC_TEMP, str(temp))
                client.publish(TOPIC_HUM, str(hum))
                client.publish(TOPIC_STATUS, "ONLINE")
                
            except OSError as dht_error:
                print("Error al leer el sensor DHT11:", dht_error)
                
            last_read = now

    except Exception as e:
        print("Error en el lazo principal:", e)
        # Si el error es por desconexión de MQTT, forzamos reinicio de cliente
        client = None 
        time.sleep(2)
        
    time.sleep_ms(100)