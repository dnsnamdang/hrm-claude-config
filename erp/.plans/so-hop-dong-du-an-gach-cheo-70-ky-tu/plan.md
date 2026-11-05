# Hợp đồng dự án: số hợp đồng nhận dấu "/" và tối đa 70 ký tự

Không Redmine (user nhờ, ảnh số `0726/TPE-EG/PO3200374723`) · @junfoke · ERP `TanPhatDev` nhánh `gop_db`

## Ngày 04/11/2026 (@junfoke)
- [x] 04/11/2026 — Số HĐ màn Hợp đồng dự án nhận thêm `/` (`FirmContractStoreRequest`, `FirmContractUpdateRequest`); câu báo lỗi bổ sung "dấu chấm và dấu gạch chéo" (câu cũ thiếu dấu chấm dù quy tắc cho phép). Xuất Excel báo cáo vận chuyển của HĐ (`FirmContractController.php:1953`): đổi `/` → `-` riêng trong tên file. Commit `49571151fc` (đã lên origin gop_db + develop_02). HĐ nguyên tắc / ĐH nguyên tắc / bản ZTEC chưa mở `/`.

## Ngày 05/11/2026 (@junfoke)
- [x] 05/11/2026 — Ô Số hợp đồng cố định tối đa **70 ký tự** (trước = 50 trừ tiền tố "HĐ_công ty_phòng_năm_số" nên mỗi phòng một mức, phòng trong ảnh chỉ 23); báo lỗi "Số hợp đồng không được quá 70 ký tự."; cột mã HĐ DB 255 nên mã đầy đủ ~95 ký tự vẫn lưu được. Commit `51ce2e883a` (gop_db, đã push).
- [ ] Hỏi user: nâng HĐ nguyên tắc / ĐH nguyên tắc (`PrincipleContract*Request`, `PrincipleOrderStoreRequest`, vẫn 50) cho đồng bộ?
