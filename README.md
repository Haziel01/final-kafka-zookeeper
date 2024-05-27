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

## Iniciar la imagen y contenedores de Kafka y Zookeeper
Para iniciar los contenedores de Kafka y Zookeeper, ejecuta el siguiente comando en la ruta de nuestro proyecto para ejecutar el archivo [docker-compose.yml](https://github.com/Haziel01/final-kafka-zookeeper/blob/eb19fc2cbf05261dd2509d75400fde95a81a0774/docker-compose.yml):
<pre lang="bash">
docker-compose <nombre_archivo_yml> up -d
</pre>

## Creamo los topicos que necesitarmenmos para llevar a cabo nuestro proyecto
<pre lang="cmd">
kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic openweather && \
kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic exchangerate
</pre>

## Verificamos que nuestros topicos se generaran sin problema y se agregaron a kafka-topics
<pre lang="cmd">
kafka-topics --list --bootstrap-server localhost:9092
</pre>

Una vez hecho esto, procedemos a establecer la conexion con nuestra base de datos y podemos ejecutar nuestor codigo de `producer.py` y de manera casi inmediata podemos proceder a ejecurtar nuestro codigo `consumer.py`








