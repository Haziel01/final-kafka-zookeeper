# final-kafka-zookeeper
Desarrollar un sistema Pipeline mediante Apache Kafka

# 1.34 Proyecto Final

**Objetivo**
Desarrollar un sistema Pipeline mediante Apache Kafka

**Actividad**
Construir un Data Pipeline con las siguientes características:

- Utilizar al menos dos API’s (Airlabs, Nasa, Openweather, etc.)
- Crear en Python un productor de mensajes de las API’s
- Mediante Apache Kafka administrar los mensajes (crear un topic por cada API-al menos dos-)
- Crear en Python un consumidor que tome los datos del topic de Apache Kafka
- Almacenar los datos en MongoDB
- Tomar los datos de MongoDB y graficar los resultados
- De los datos que ofrecen los APIs seleccione la información a procesar y gráficar

*Diagrama de implementación*
![[Diagrama de implementación]](https://github.com/Haziel01/final-kafka-zookeeper/blob/main/kafka.png?raw=true)

# Instrucciones para Iniciar Kafka y Zookeeper

## Paso 1: Iniciar la imagen y contenedores de Kafka y Zookeeper

Para iniciar los contenedores de Kafka y Zookeeper, ejecuta el siguiente comando:
<pre lang="bash">
docker-compose <nombre_archivo_yml> up
</pre>

<pre lang="bash">
kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic openweather && \
kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic exchangerate
</pre>

<pre lang="bash">
kafka-topics --list --bootstrap-server localhost:9092
</pre>






