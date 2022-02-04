#!/usr/bin/env python
import pika
import uuid
import os
class FibonacciRpcClient(object):

    def __init__(self):
        url = os.environ.get('CLOUDAMQP_URL',
                             'amqps://unpdhmjh:9O6phmtSscvSCVvrg88qq8461qz8y8t5@jellyfish.rmq.cloudamqp.com/unpdhmjh')
        params = pika.URLParameters(url)
        params.socket_timeout = 5

        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='Interieur',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=n)
        while self.response is None:
            self.connection.process_data_events()
        return self.response


fibonacci_rpc = FibonacciRpcClient()

print(" [x] Requesting fib(30)")
response = fibonacci_rpc.call("11111111")
print(" [.] Got %r" % response)