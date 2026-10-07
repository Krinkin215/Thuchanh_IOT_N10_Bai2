# Báo cáo Thực Hành: Lập Trình Python Với Giao Thức AMQP

## 1. Thông Tin Chung

| Họ và tên | Mã sinh viên |
|---|---|
| Phạm Văn Kiên | B23DCCN466 |
| Lưu Đức Thành Đạt | B23DCCN130 |

| Môn học | Broker sử dụng |
|---|---|
| Internet of Things (IoT) | RabbitMQ (localhost:5672) |

---

## 2. Yêu Cầu Môi Trường

- Python 3.x
- Thư viện pika
- RabbitMQ đã cài đặt và đang chạy trên máy

### Cài đặt thư viện

`ash
pip install pika
`

### Khởi động RabbitMQ (nếu chưa chạy)

`ash
# Windows (chạy với quyền Administrator)
rabbitmq-service start

# Hoặc vào Services và khởi động RabbitMQ
`

---

## 3. Bài 1 – Gửi và Nhận Message Cơ Bản

### Mô tả

- **Queue sử dụng:** iot_lab_queue
- **Producer** gửi 3 message chứa họ tên và mã sinh viên.
- **Consumer** lắng nghe queue và in message kèm thời gian nhận.

### Cách chạy

**Bước 1:** Mở terminal, chạy consumer trước (chạy liên tục):

`ash
python consumer_bai1.py
`

**Bước 2:** Mở terminal khác, chạy producer để gửi message:

`ash
python producer_bai1.py
`

### Kết quả mong đợi

**Producer:**
```
[x] Đã gửi: Xin chào từ ứng dụng Python AMQP - B23DCCN466 - B23DCCN130 - Phạm Văn Kiên - Lưu Đức Thành Đạt
[x] Đã gửi: Message thứ 2 - B23DCCN466 - B23DCCN130 - Phạm Văn Kiên - Lưu Đức Thành Đạt
[x] Đã gửi: Message thứ 3 - B23DCCN466 - B23DCCN130 - Phạm Văn Kiên - Lưu Đức Thành Đạt
Kết nối đã đóng. Producer kết thúc.
```

**Consumer:**
```
[*] Đang chờ message. Nhấn Ctrl+C để dừng.
Đã nhận message: Xin chào từ ứng dụng Python AMQP - B23DCCN466 - B23DCCN130 - Phạm Văn Kiên - Lưu Đức Thành Đạt
Thời gian nhận: 14:05:21
--------------------------------------------------
Đã nhận message: Message thứ 2 - B23DCCN466 - B23DCCN130 - Phạm Văn Kiên - Lưu Đức Thành Đạt
Thời gian nhận: 14:05:21
--------------------------------------------------
```

---

## 4. Bài 2 – Mô Phỏng Cảm Biến IoT Gửi Dữ Liệu Môi Trường

### Mô tả

- **Queue sử dụng:** sensor_data_queue
- **Sensor Producer** mô phỏng cảm biến sensor01, gửi dữ liệu nhiệt độ/độ ẩm ngẫu nhiên mỗi 3 giây dưới định dạng JSON.
- **Monitoring Consumer** nhận dữ liệu, phân tích và cảnh báo khi:
  - Nhiệt độ > 35°C → `CẢNH BÁO: Nhiệt độ cao`
  - Độ ẩm < 40% → `CẢNH BÁO: Độ ẩm thấp`

### Cách chạy

**Bước 1:** Chạy monitoring consumer:

`ash
python monitor_consumer_bai2.py
`

**Bước 2:** Mở terminal khác, chạy sensor producer:

`ash
python sensor_producer_bai2.py
`

### Kết quả mong đợi

**Sensor Producer:**
```
[*] Bắt đầu gửi dữ liệu từ sensor01. Nhấn Ctrl+C để dừng.
[x] Đã gửi: {"device_id": "sensor01", "temperature": 36.4, "humidity": 38.9, "timestamp": "2026-10-07 14:10:00"}
[x] Đã gửi: {"device_id": "sensor01", "temperature": 28.1, "humidity": 65.3, "timestamp": "2026-10-07 14:10:03"}
```

**Monitoring Consumer:**
```
Device: sensor01
Temperature: 36.4
Humidity: 38.9
Timestamp: 2026-10-07 14:10:00
CẢNH BÁO: Nhiệt độ cao
CẢNH BÁO: Độ ẩm thấp
--------------------------------------------------
Device: sensor01
Temperature: 28.1
Humidity: 65.3
Timestamp: 2026-10-07 14:10:03
--------------------------------------------------
```

---

## 5. Bài 3 – Hệ Thống Điều Phối Cảnh Báo IoT Với Exchange

### Mô tả

- **Exchange sử dụng:** iot_alert_exchange (kiểu direct)
- **Alert Producer** gửi cảnh báo với 3 mức routing key: info, warning, critical.
- **Warning Consumer** chỉ nhận message có routing key warning (queue: warning_queue).
- **Critical Consumer** chỉ nhận message có routing key critical (queue: critical_queue).
- Message với routing key info không được nhận bởi consumer nào.

### Cách chạy

**Bước 1:** Mở terminal 1, chạy warning consumer:

`ash
python warning_consumer_bai3.py
`

**Bước 2:** Mở terminal 2, chạy critical consumer:

`ash
python critical_consumer_bai3.py
`

**Bước 3:** Mở terminal 3, chạy alert producer:

`ash
python alert_producer_bai3.py
`

### Kết quả mong đợi

**Alert Producer:**
```
[x] Gửi [info]: Hệ thống khởi động thành công mức info
[x] Gửi [warning]: Nhiệt độ phòng máy vượt ngưỡng warning
[x] Gửi [critical]: Cảm biến kho lạnh mất kết nối critical
[x] Gửi [warning]: Áp suất đường ống bất thường mức warning
[x] Gửi [critical]: Nguồn điện chính bị ngắt mức critical
Alert producer đã kết thúc.
```

**Warning Consumer (terminal 1):**
```
[*] Warning consumer đang lắng nghe trên 'warning_queue'. Nhấn Ctrl+C để dừng.
[warning_queue] Đã nhận: Nhiệt độ phòng máy vượt ngưỡng warning
[warning_queue] Đã nhận: Áp suất đường ống bất thường mức warning
```

**Critical Consumer (terminal 2):**
```
[*] Critical consumer đang lắng nghe trên 'critical_queue'. Nhấn Ctrl+C để dừng.
[critical_queue] Đã nhận: Cảm biến kho lạnh mất kết nối critical
[critical_queue] Đã nhận: Nguồn điện chính bị ngắt mức critical
```

---

## 6. Cấu Trúc File

`
Bai2/
├── producer_bai1.py          # Bài 1 - Producer gửi message chào mừng
├── consumer_bai1.py          # Bài 1 - Consumer nhận và hiển thị message
├── sensor_producer_bai2.py   # Bài 2 - Cảm biến gửi dữ liệu JSON mỗi 3s
├── monitor_consumer_bai2.py  # Bài 2 - Giám sát và cảnh báo dữ liệu cảm biến
├── alert_producer_bai3.py    # Bài 3 - Gửi cảnh báo qua direct exchange
├── warning_consumer_bai3.py  # Bài 3 - Nhận cảnh báo mức warning
├── critical_consumer_bai3.py # Bài 3 - Nhận cảnh báo mức critical
└── README.md                 # Tài liệu hướng dẫn
`

---

## 7. Lưu Ý

- Đảm bảo RabbitMQ đang chạy trước khi thực thi bất kỳ chương trình nào.
- Luôn chạy **consumer trước**, sau đó mới chạy **producer**.
- Để dừng consumer, nhấn `Ctrl+C`.
- Nếu muốn thay đổi thông tin sinh viên trong Bài 1, chỉnh sửa biến `STUDENT_NAME` và `STUDENT_ID` trong file `producer_bai1.py`.
- Có thể truy cập giao diện quản lý RabbitMQ tại: http://localhost:15672 (tài khoản mặc định: `guest/guest`).
