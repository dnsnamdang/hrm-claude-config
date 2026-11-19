# Fix: rice:update-meal-checkin-regular sập khi máy chấm cơm mất kết nối

- [x] BE: timeout + thử lại 3 lần mỗi lượt gọi máy, bắt lỗi kết nối để không dừng cả lệnh, máy lỗi 5 lần liên tiếp thì bỏ qua, log tổng kết từng máy, exit 1 khi chưa đủ (19/10/2026 — sự cố 10:12 cùng ngày, 338 người không lên máy)
- [x] BE: tách phần đẩy lên máy ra trait `Rice/Concerns/PushesMealCheckinToMachines`, áp cho cả `rice:update-meal-checkin-party`; RiceKernel chạy lại 2 lệnh check-in sau +30/+60 phút (bỏ lần chạy lại qua nửa đêm)
