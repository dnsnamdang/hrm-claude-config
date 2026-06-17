# Plan — Bỏ validate khi hợp đồng "Không thực hiện"

**Người phụ trách:** @khoipv
**Spec:** `docs/superpowers/specs/2026-06-10-contract-not-executed-skip-validate-design.md`
**Plan chi tiết:** `docs/superpowers/plans/2026-06-10-contract-not-executed-skip-validate.md`

> Phát hiện: cả `store` (POST) và `update` (PUT) dùng chung `StoreContractRequest`; FE (add + edit) KHÔNG validate client → chỉ 1 thay đổi BE là đủ cho cả 4 trường hợp.

## Phase 1 — Backend (cốt lõi)

- [x] BE: Sửa `StoreContractRequest::rules()` — nếu `result == 2` → chỉ `'reason' => 'required'`
- [x] BE: Giữ nguyên toàn bộ rule cũ cho nhánh `result != 2`
- [x] BE: Thêm `messages()` — `reason.required` = "Vui lòng nhập lý do không thực hiện"
- [x] BE: `php -l` pass

## Phase 1b — Migration (phát sinh khi kiểm thử)

- [x] DB: Migration cho `main_company_id` + `customer_id` nhận NULL (báo giá/gói thầu có thể trống) — `2026_06_10_160000_make_main_company_id_customer_id_nullable_on_contracts_table.php`, đã chạy

## Phase 2 — Frontend (tùy chọn, chỉ UX)

- [x] FE: Thêm dấu `*` ở label Lý do trong `GeneralComponent.vue` khi `formSubmit.result == 2` (dòng 567)
- [x] (Không cần sửa logic validate FE — FE lấy lỗi trực tiếp từ BE)

## Phase 3 — Kiểm thử thủ công

- [ ] Tạo mới, `result = 2`, bỏ trống mọi field, có `reason` → lưu thành công
- [ ] Tạo mới, `result = 2`, `reason` trống → chặn ở `reason` (FE + BE)
- [ ] Tạo mới, `result = 1` → validate đầy đủ như cũ
- [ ] Tạo mới, `result` trống → validate đầy đủ như cũ
- [ ] Cập nhật HĐ, đổi sang `result = 2` → chỉ cần `reason`
- [ ] HĐ `result = 2` vẫn gửi duyệt + cập nhật trạng thái gói thầu/báo giá bình thường

## Checkpoint

### Checkpoint — 2026-06-10
Vừa hoàn thành: brainstorming xong, viết spec + design + plan
Đang làm dở: chưa code
Bước tiếp theo: lập kế hoạch implement chi tiết (writing-plans) rồi code Phase 1 (BE)
Blocked:

### Checkpoint — 2026-06-10 (code xong)
Vừa hoàn thành: BE sửa `StoreContractRequest` (rẽ nhánh `rules()` theo `result` + `messages()`), `php -l` pass; FE thêm dấu `*` label Lý do (GeneralComponent.vue:567)
Đang làm dở: không
Bước tiếp theo: người dùng kiểm thử thủ công 6 case ở Phase 3 trên UI (tạo/sửa HĐ, result=2/1/trống, có/thiếu lý do, luồng gửi duyệt + downstream)
Blocked: không
