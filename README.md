# Sistema de Monitoreo Ambiental basado en IoT

**Alumno:** Marcos Galla
**Materia:** Ingeniería en Computación II

## Estructura del Directorio
* `Codigo_esp32/`: Contiene el código fuente en MicroPython para el nodo ESP32, encargado de la lectura del sensor DHT11 y el control del actuador (LED).
* `mosquitto/`: Contiene el archivo de configuración del broker MQTT (`mosquitto.conf`), el cual establece las políticas de conexión y persistencia.
* `node_red/`: Contiene el archivo `flows.json` con la exportación del flujo de Node-RED, donde se define la lógica de enrutamiento y la interfaz gráfica del dashboard.
* `simulador.py`: Script en Python desarrollado para emitir telemetría simulada (temperatura y humedad) con el objetivo de probar el sistema sin necesidad del hardware físico.
* `informe_ICII_Marcos_Galla.pdf`: Documento formal del proyecto que incluye requerimientos, decisiones de arquitectura, diagramas de flujo y resultados de pruebas.

## Tópicos MQTT y Especificación
* **Autenticación:** El broker se ejecuta en modo anónimo (sin usuario/contraseña), permitiendo conexiones locales sin requerir credenciales.

### Tópicos Utilizados
* `esp32/dht11/temperature`
  * **Publica:** Nodo ESP32 (o script simulador)
  * **Suscribe:** Node-RED
  * **Formato de datos:** Cadena de texto (String) representando el valor numérico en °C (Ej: "24.5").

* `esp32/dht11/humidity`
  * **Publica:** Nodo ESP32 (o script simulador)
  * **Suscribe:** Node-RED
  * **Formato de datos:** Cadena de texto (String) representando el porcentaje de humedad (Ej: "55.0").

* `esp32/led/status`
  * **Publica:** Nodo ESP32 (confirmando el cambio físico)
  * **Suscribe:** Node-RED (para actualizar el estado en el dashboard)
  * **Formato de datos:** String ("ON" / "OFF").

* `esp32/led/control`
  * **Publica:** Node-RED (al accionar el switch en el dashboard)
  * **Suscribe:** Nodo ESP32 (para ejecutar la acción)
  * **Formato de datos:** String ("ON" / "OFF").
 
🚀 Guía de Despliegue y Verificación
Requisitos Previos
Tener instalado Docker y Docker Compose.
Tener instalado Python 3 con la librería paho-mqtt:
pip install paho-mqtt

⚡ Ejecución Rápida (TL;DR)
Si querés probar el proyecto inmediatamente en un clon limpio, ejecutá en tu terminal:

# 1. Clonar e ingresar al proyecto
git clone https://github.com/Galla77/202607-IC2-galla
cd 202607-IC2-galla

# 2. Levantar la infraestructura (Broker MQTT + Node-RED)
docker compose up -d

# 3. Ejecutar el simulador del ESP32
python simulador.py ( En consola apareceran los datos enviados y datos recibidos )

Ctrl+C para detener scrip

#4. El Dashboard y Node-Red
Dashboard "Localhost:1880/ui"
Node-Red "Localhost:1880"

#5. detener y limpiar entorno
Broker-Node-red docker compose down
