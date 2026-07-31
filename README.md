# Sistema de Monitoreo Ambiental basado en IoT (ESP32 + MQTT + Node-RED)

**Alumno:** Marcos Galla  
**Materia:** Ingeniería en Computación II  
**Comisión / Curso:** [Agrega aquí tu comisión si aplica, ej: Comisión 1]  

---

## 1. Estructura del Directorio
* `Codigo_esp32/`: Contiene el código fuente para el microcontrolador ESP32, encargado de la lectura de telemetría (DHT11) y control del actuador físico (LED).
* `mosquitto/`: Configuración del broker MQTT (`mosquitto.conf`) con políticas de conexión locales y persistencia.
* `node_red/`: Persistencia del contenedor de Node-RED. Incluye `flows.json` (lógica y diseño gráfica) y `package.json` (declaración de dependencias para la auto-instalación del módulo `node-red-dashboard`).
* `docker-compose.yml`: Orquestación de servicios en contenedores (Mosquitto v2.0.18 + Node-RED v5.0.4) con redes e instalaciones automatizadas.
* `requirements.txt`: Declaración de dependencias de Python fijando la versión de `paho-mqtt==1.6.1` para compatibilidad con la API v1.
* `simulator.py`: Script de prueba en Python para emitir telemetría simulada (temperatura/humedad) y responder a comandos de control del LED sin hardware físico.
* `informe_ICII_Marcos_Galla.pdf`: Documento técnico formal (requerimientos, decisiones de arquitectura, diagramas de red y evidencia de pruebas).

---

## 2. Protocolo de Comunicación y Tópicos MQTT

* **Autenticación:** El broker Mosquitto corre por defecto en **modo anónimo (sin usuario/contraseña)** dentro de la red local sobre el puerto estándar **`1883`**.


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

| Tópico MQTT | Publicador | Suscriptor | Formato / Payload | Ejemplo de Dato | Descripción |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `esp32/dht11/temperature` | ESP32 / Simulador | Node-RED | **JSON (Float)** | `{"temperature": 24.5}` | Valor en °C publicado periódicamente. |
| `esp32/dht11/humidity` | ESP32 / Simulador | Node-RED | **JSON (Float)** | `{"humidity": 55.0}` | Porcentaje de humedad publicado periódicamente. |
| `esp32/led/control` | Node-RED (Dashboard)| ESP32 / Simulador | **String** | `"ON"` / `"OFF"` | Orden de encendido o apagado enviada por el usuario. |
| `esp32/led/status` | ESP32 / Simulador | Node-RED | **String** | `"ON"` / `"OFF"` | Confirmación real del estado del actuador. |

---

## 3. Guía de Despliegue y Puesta en Marcha (Ejecución Limpia)

### Prerrequisitos
* **Docker y Docker Compose** instalados.
* **Python 3.8+** (para ejecutar el script simulador de hardware).

### Paso 1: Clonar el repositorio
```bash
git clone [https://github.com/Galla77/202607-IC2-galla.git](https://github.com/Galla77/202607-IC2-galla.git)
cd 202607-IC2-galla

