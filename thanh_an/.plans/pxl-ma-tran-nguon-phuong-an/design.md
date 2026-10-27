# PXL — bảng Xử lý cung ứng hàng theo ma trận Nguồn × Phương án

@khoipv · Bắt đầu 23/10/2026

Spec chi tiết: [docs/superpowers/specs/2026-10-23-pxl-ma-tran-nguon-phuong-an-design.md](../../docs/superpowers/specs/2026-10-23-pxl-ma-tran-nguon-phuong-an-design.md)
Demo: `demos/demo-pxl-tach-nguon-hang.html` (bản user gửi 23/10/2026)

## Mục tiêu
Bảng hàng phiếu xử lý: mỗi hàng = khối dòng nguồn (Hàng tồn kho · Khách đang vay · Chốt mua thêm) × cột phương án
(Xuất bán · Xuất khách gửi · Xuất trả gửi cho KH · Xuất cho KH vay · Trừ hàng KH vay). SL đã xử lý xanh/đỏ (thiếu/thừa).

## Quyết định lớn
- Áp dụng mọi loại phiếu (user chốt). Loại 3/4/5/6: tồn + mua × Xuất bán. Loại 2: tồn + mua × Xuất kho nội bộ.
- Lưu 11 cột ô `alloc_<nguồn>_<pa>`; `alloc_*` cũ giữ, BE suy ra (`alloc_mua` = Σ dòng mua) → báo cáo nhu cầu mua,
  giới hạn đề xuất không phải sửa. Migration backfill phiếu cũ. (dev tự quyết)
- Giới hạn nguồn (tồn xuất được, KH vay, KH gửi) chặn lưu ở FE; hàng trùng mã chia nguồn từ trên xuống. (dev tự quyết)
- Bỏ cột Xuất đổi; đổi hàng vẫn bằng dòng THAY CHO.
- Tab tổng hợp đổi tên theo demo; đề nghị xuất kho tách "Xuất ngay từ tồn kho" / "Chờ hàng mua về".
