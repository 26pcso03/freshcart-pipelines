import time, json, random, pika
from datetime import datetime

conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
ch = conn.channel()
ch.exchange_declare(exchange='rapido-dispatch', exchange_type='topic')

cities = {'bangalore': ['koramangala', 'indiranagar', 'whitefield'],
          'chennai': ['tnagar', 'whitefield']}
types = ['ride', 'food']

i = 0
while True:
    i += 1
    c = random.choice(list(cities.keys()))
    z = random.choice(cities[c])
    t = random.choice(types)
    rk = f"{c}.{z}.{t}"
    msg = {"id": f"ORD-{i}", "city": c, "zone": z, "type": t, "ts": datetime.now().isoformat()}
    if i % 10 == 0:
        del msg["zone"]
    ch.basic_publish(exchange='rapido-dispatch', routing_key=rk, body=json.dumps(msg))
    print(f"[DISPATCHER] Sent {rk}: {msg}", flush=True)
    time.sleep(2)
