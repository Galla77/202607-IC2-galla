# Sistema de Monitoreo Ambiental - IC 2

Este proyecto implementa una arquitectura de Internet de las Cosas (IoT) con comunicación bidireccional en tiempo real. Permite la adquisición de datos ambientales (temperatura y humedad) mediante un nodo sensor y el control a distancia de un actuador (LED), centralizando el tráfico de datos a través de un Broker MQTT y una interfaz gráfica de usuario.

##  Arquitectura del Sistema

El ecosistema está compuesto por tres capas principales:

1. **Nodo de Borde (ESP32):** Recolecta datos del sensor DHT11 y controla el estado físico del LED. Está programado en MicroPython.
2. **Capa de Mensajería (Mosquitto MQTT):** Servidor Broker corriendo en un contenedor Docker dentro de una Raspberry Pi 4 model B, encargado de distribuir los mensajes de forma asríncronica mediante tópicos configurados.
3. **Capa de Aplicación y Visualización (Node-RED):** dirige la lógica de control, procesa los datos entrantes y expone un Dashboard web con gráficos en tiempo real de temperatura y humedad e interruptores de control para el estado del LED.


 [ ESP32 (DHT11/LED) ] <---(WiFi / MQTT)---> [ Broker Mosquitto (Docker) ] <---> [ Node-RED Dashboard ]