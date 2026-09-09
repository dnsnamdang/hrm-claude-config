# Đưa `gop_db` lên PROD — tóm tắt

> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-09-04-prod-cutover-design.md`
> Trạng thái: **spec xong, chưa code**. Ngày 2026-09-04. @namdangit

## Mục tiêu

ERP chạy code `master`, HRM chạy code `gop_db`, **cả hai dùng chung một DB gộp**.
PROD và dev dùng **chung một nhánh** `gop_db`: PROD chỉ mở phân hệ HRM đã nghiệm thu, dev thấy đủ để làm tiếp.

## Kết luận khảo sát (số đo 2026-09-04, DB local)

Bản gộp `local_hrm_erp` **đang có lỗi dữ liệu thật, âm thầm**:

| # | Vấn đề | Số đo |
| --- | --- | --- |
| 🔴 A.1 | Mất ràng buộc FOREIGN KEY của ERP | 2.313 FK / 556 bảng → còn **10 FK / 7 bảng** |
| 🔴 A.2 | Dòng ERP trỏ **nhầm** sang vai trò HRM sau khi dời id `roles +100000` | **736 trỏ nhầm + 1.820 mồ côi** trên 2.556 dòng — gồm `companies.deputy_role` **8/8 công ty** |
| 🔴 A.3 | 14 bảng ERP bị `DROP` rồi thay bằng bản HRM | `majors` mất 156 dòng (còn **0**), `areas` còn **1/20** — ERP `master` vẫn dùng cả hai |
| 🟠 A.4 | `notifications` bị TRUNCATE | 154.176 + 687.693 → **299** |
| 🟠 A.5 | Ghi đè chéo theo `id` ở nhóm `SHARE` | `customers` **77** dòng lệch, `districts` 15 |
| 🟡 A.6 | Bản gộp local là snapshot cũ, không bê lên PROD được | `settlement_contract_employees` −4.554, `customers` −118 |
| 🟢 A.7 | 42 migration mới, 12 cái ALTER bảng ERP | 2 cái đáng ngờ nhất đã đọc: **an toàn**, có ghi lý do |

Nguồn lỗi A.2/A.3/A.4 nằm trong `Modules/Timesheet/Database/Seeders/GopDb/` — chạy pipeline đó lên PROD
sẽ tái hiện y hệt.

## Quyết định đã chốt

| Điểm | Chốt |
| --- | --- |
| Nguồn cấu hình bật/tắt phân hệ | **Bảng cấu hình trong DB (runtime)** — không phải `.env` |
| Đơn vị bật/tắt | **Theo phân hệ** + danh sách chặn link lẻ |
| Nhánh PROD hiện tại của HRM | `tpe` |
| Ranh giới | 17 thư mục `pages/` mới + 3 màn lẻ (`/assign/contracts`, `/human/districts`, `/human/hamlets`) |
| Mức chặn ở BE | **HOÃN** — user chốt "backend kệ đi", ưu tiên rủi ro DB trước |

## Việc phải làm theo thứ tự

1. Xác minh cách bản gộp local được tạo ra (giải thích vì sao mất 99,6% FK)
2. Vá pipeline gộp: remap FK toàn bộ, không DROP bảng ERP, tách `hrm_*` thay vì chọn một bên, archive notifications, khôi phục FK
3. ✅ **XONG** — Command `gopdb:health-check` (`app/Console/Commands/GopDb/HealthCheckCommand.php`), chỉ SELECT:
   `--mode=pre` cảnh báo cái gì sắp mất, `--mode=post` đo cái gì đã hỏng, exit code 0/1/2.
   Còn lại: chạy trên clone của PROD để đối chiếu số.
4. Phần B (ẩn menu PROD) — độc lập, làm được ngay
5. Kỷ luật migration cho giai đoạn PROD/dev chung nhánh
