import sys, json, pika

name, pattern = sys.argv[1], sys.argv[2]
conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
ch = conn.channel()
ch.exchange_declare(exchange='rapido-dispatch', exchange_type='topic')
q_name = ch.queue_declare(queue='', exclusive=True).method.queue
ch.queue_bind(exchange='rapido-dispatch', queue=q_name, routing_key=pattern)

def callback(ch, method, properties, body):
    msg = json.loads(body.decode())
    if 'zone' not in msg or not msg['zone']:
        print(f"[{name}] NACK (discarded bad msg): {msg}", flush=True)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    else:
        print(f"[{name} | {pattern}] ACK ({method.routing_key}): {msg}", flush=True)
        ch.basic_ack(delivery_tag=method.delivery_tag)

ch.basic_consume(queue=q_name, on_message_callback=callback)
ch.start_consuming()
