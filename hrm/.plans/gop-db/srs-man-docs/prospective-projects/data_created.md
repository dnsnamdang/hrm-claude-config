# Dữ liệu tạo cho SRS - Dự án (05/10/2026, DB local_hrm_erp, tạo qua API :8003 bằng tài khoản namdangit = employee 13)

| Bảng | id | Mã | Nội dung |
|---|---|---|---|
| prospective_projects | 157 | CTV_NV.2026.DAC001 | Dự án CHA "Đầu tư trang thiết bị chuỗi xưởng dịch vụ Ô tô Việt Phúc 2026-2027" — KH 180 (29TPHXHO-1), Lưu chính thức |
| prospective_projects | 158 | CTV_NV.UD.0101.2026.DA004 | Dự án CON của 157 — "Xưởng dịch vụ Việt Phúc Long Biên – cầu nâng và thiết bị chẩn đoán" |
| prospective_projects | 159 | CTV_NV.UD.0101.2026.DA005 | Dự án CON của 157 — "Xưởng dịch vụ Việt Phúc Hưng Yên – thiết bị khoang sơn" |
| prospective_projects | 160 | (chưa có mã) | Dự án NHÁP (Đang tạo) "Nâng cấp thiết bị khoang bảo dưỡng nhanh – Ô tô Việt Hải" — KH 148 |

Dữ liệu demo có sẵn chỉ đọc: dự án 145–154 (không sửa).
| prospective_project_extension_requests | 1 | GHDA.00001 | Đề xuất gia hạn 45 ngày cho dự án 158 (Chờ TP duyệt) |

Ghi chú: 4 dự án 157–160 tạo qua API nên thiếu các cột "ảnh chụp" tên/mã KH, người liên hệ (FE thường tự gửi) → đã bổ sung bằng SQL `UPDATE prospective_projects ... WHERE id IN (157,158,159,160)` từ bảng customers / customer_contacts.
Dự án 158: đã sửa qua API `PUT` bật "Có cần làm GP? = Có" (để có nút Tạo giải pháp).
