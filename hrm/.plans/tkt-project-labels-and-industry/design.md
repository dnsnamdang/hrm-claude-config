# Design — Dự án TKT: đổi nhãn + trường Nhóm ngành (Redmine #11142)

> @junfoke — Nhánh `task_11142` (tách từ `tpe`), cả 2 repo `hrm-client` + `hrm-api`.

## Phạm vi issue #11142 (4 mục)

| # | Nội dung | Trạng thái |
| --- | --- | --- |
| 1 | Đổi nhãn: Ngày bắt đầu → **Ngày bắt đầu dự án TKT**, Ngày kết thúc → **Ngày kết thúc dự án TKT**, Giai đoạn dự án → **Giai đoạn dự án KH** | Phase 1 — làm ngay |
| 2 | Bổ sung trường **Nhóm ngành** (dự án con/độc lập: bắt buộc, chọn 1; dự án cha: chọn nhiều) | Phase 2 |
| 2b | Ràng buộc: 1 khách hàng + 1 nhóm ngành chỉ có 1 dự án TKT đang mở | Phase 3 — cần chốt spec |
| 3 | Chọn nhu cầu từ meeting + cảnh báo mềm khi bỏ trống | ✅ **ĐÃ CÓ SẴN** trên `tpe` |
| 4 | Kéo meeting của khách cá nhân về dự án doanh nghiệp khi chuyển loại KH | Phase 4 — cần chốt spec |

Mục 3 đã xong từ trước: ô "Nhu cầu khách hàng" ở `components/CustomerBlock.vue` + popup cảnh báo
`confirmMissingCustomerDemand()` ở `add.vue` (cảnh báo nhưng vẫn cho lưu) — không phải làm lại.

## Phase 1 — Đổi nhãn (đang làm)

Nhãn đổi ở **mọi nơi hiển thị trường của dự án TKT**: form Tạo/Sửa, màn chi tiết, cột danh sách,
bộ lọc, và message validate của BE (để lỗi trả về khớp nhãn mới).

Điểm phải hỏi user trước khi lan rộng: trường `project_phase_id` còn được dùng ở **Báo giá**,
**Yêu cầu làm giải pháp**, **Công việc của tôi**, **Meeting** (#11016/#11058 cho chọn ngay trên các
màn đó rồi đồng bộ ngược về dự án gốc). Đổi nhãn ở những màn đó nữa hay giữ nguyên, và **tên danh
mục** "Giai đoạn dự án" (menu Danh mục) có đổi theo không — xem plan.md.

## Phase 2-4 (chưa làm)

Xem phần "Điểm cần chốt" trong plan.md — mục 2b và 4 spec còn hở, phải hỏi khách trước khi code.
