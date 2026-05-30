# Design — Phiếu xác định & quy tắc xử lý vi phạm công nợ

**Trạng thái:** Đã chốt design — chờ user review spec chi tiết
**Phụ trách:** @khoipv
**Ngày:** 2026-05-18
**Mock tham khảo:** `hrm-thanhan-client/pages/timesheet/setting/debt-limit/canh-bao-cong-no-v4.html` (mục 4)
**Spec chi tiết:** `docs/superpowers/specs/2026-05-18-debt-violation-rules-design.md`

---

## Mục tiêu

Lưu cấu hình toàn hệ thống cho 2 nhóm thiết lập (mục 4 của mock cảnh báo công nợ):
1. **Phiếu xác định tính nợ** — chọn loại phiếu nào khi tạo sẽ tính là công nợ.
2. **Quy tắc xử lý vi phạm** — hành động khi điều khoản HĐ bị vi phạm (`BGĐ phê duyệt` hoặc `Chặn không xuất hàng`).

Phase này **chỉ làm UI + lưu DB + lịch sử thay đổi**. Logic tích hợp vào flow tạo phiếu / workflow phê duyệt sẽ là task riêng.

## Scope

- BE: 2 migrations (`debt_violation_rules`, `debt_violation_rule_logs`), 2 models, 1 controller (GET / PUT / GET history), 1 request validator. Đặt trong `Modules/Timesheet`.
- FE: 1 page mới `pages/timesheet/setting/debt-limit/index.vue` + 1 modal lịch sử (bê pattern `category/product_unit_price/PriceHistoryModal`). Thêm menu entry.
- DB: 1 row config duy nhất, seed sẵn `["DELIVERY","VAT"]` + `APPROVE`.

## Các quyết định lớn

| | |
|---|---|
| Cấu hình toàn hệ thống | 1 row duy nhất |
| 4 loại phiếu hardcode (`DELIVERY`/`VAT`/`EXPORT`/`SALES`) | Không cần CRUD danh mục riêng |
| `doc_types` lưu JSON array | Code consumer chỉ cần `in_array()`; thêm loại sau không cần migrate |
| Phân quyền | Theo pattern `payment-working-fee` (không thêm permission code) |
| Lịch sử thay đổi | Pattern timeline như `category/product_unit_price` |
| Vị trí | `pages/timesheet/setting/debt-limit/` (đúng folder mock) |

## Out of scope

- Tích hợp check rule khi tạo phiếu thực tế.
- Workflow BGĐ phê duyệt.
- Các mục 1/2/3/5 của mock (hạn mức KH, thông tin HĐ, điều khoản thanh toán, mô phỏng).
