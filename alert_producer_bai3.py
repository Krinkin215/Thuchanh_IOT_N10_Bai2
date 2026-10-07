import pika
import time

BROKER_HOST = "localhost"
EXCHANGE_NAME = "iot_alert_exchange"

ALERTS = [
    ("info",     "Hệ thống khởi động thành công mức info"),
    ("warning",  "Nhiệt độ phòng máy vượt ngưỡng warning"),
    ("critical", "Cảm biến kho lạnh mất kết nối critical"),
    ("warning",  "Áp suất đường ống bất thường mức warning"),
    ("critical", "Nguồn điện chính bị ngắt mức critical"),
]

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

    for routing_key, message in ALERTS:
        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=routing_key,
            body=message.encode("utf-8"),
            properties=pika.BasicProperties(delivery_mode=2),
        )
        print(f"[x] Gửi [{routing_key}]: {message}")
        time.sleep(0.5)

    connection.close()
    print("Alert producer đã kết thúc.")

if __name__ == "__main__":
    main()
