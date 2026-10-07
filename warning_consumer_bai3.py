import pika

BROKER_HOST = "localhost"
EXCHANGE_NAME = "iot_alert_exchange"
QUEUE_NAME = "warning_queue"
ROUTING_KEY = "warning"

def callback(ch, method, properties, body):
    message = body.decode("utf-8")
    print(f"[warning_queue] Đã nhận: {message}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=BROKER_HOST)
    )
    channel = connection.channel()

    channel.exchange_declare(
        exchange=EXCHANGE_NAME,
        exchange_type="direct",
        durable=True,
    )
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.queue_bind(
        queue=QUEUE_NAME,
        exchange=EXCHANGE_NAME,
        routing_key=ROUTING_KEY,
    )

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

    print(f"[*] Warning consumer đang lắng nghe trên '{QUEUE_NAME}'. Nhấn Ctrl+C để dừng.")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
        print("Warning consumer đã dừng.")
    finally:
        connection.close()

if __name__ == "__main__":
    main()
