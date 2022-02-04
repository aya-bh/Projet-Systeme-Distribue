#!/usr/bin/env python
import json
import pika
import os
import mysql.connector

url = os.environ.get('CLOUDAMQP_URL', 'amqps://unpdhmjh:9O6phmtSscvSCVvrg88qq8461qz8y8t5@jellyfish.rmq.cloudamqp.com/unpdhmjh')
params = pika.URLParameters(url)
params.socket_timeout = 5
connection = pika.BlockingConnection(params) # Connect to CloudAMQP
channel = connection.channel()
channel.queue_declare(queue='Interieur')

def on_request(ch, method, props, body):
    n =body
    print("1")
    print(n)
    connection = mysql.connector.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='testpolice',
                                 )
    print("connection succes")
    try:

            mycursor = connection.cursor()
            sql = "SELECT * FROM Personne WHERE cin = %s"
            cin=(n,)
            mycursor.execute(sql, cin)
            myresult = mycursor.fetchall()

            json_output = json.dumps(myresult,default=str)
            print(json_output)
            print(" [.] response(%s)" % n)
            ch.basic_publish(exchange='',
                             routing_key='Interieur',
                             properties=pika.BasicProperties(correlation_id= \
                                                                 props.correlation_id),
                             body=str(json_output))
            ch.basic_ack(delivery_tag=method.delivery_tag)
    finally:
     #Closez la connexion (Close connection).
            connection.close()
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='Interieur', on_message_callback=on_request)
print(" [x] Awaiting RPC requests")
channel.start_consuming()








