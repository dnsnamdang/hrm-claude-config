# Fix: Phiếu admin huỷ suất ăn báo "Có lỗi xảy ra" — @namdangit

- [x] Popup chọn NV huỷ cơm chỉ hiện người còn suất để huỷ (theo ngày + loại cơm thường/khách); FormRequest chặn 422 kèm tên NV không có suất; snapshot NOT NULL có giá trị mặc định (gốc lỗi: `receiving_meal cannot be null` khi NV chưa cài nơi ăn, prod 03/10/2026)
