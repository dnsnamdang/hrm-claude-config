# Hợp đồng HRM (tạo từ Báo giá) — Tóm tắt

> @dnsnamdang · Module `Assign` · Spec đầy đủ: `docs/superpowers/specs/2026-08-10-hop-dong-design.md`

## Mục tiêu
Chuyển nghiệp vụ hợp đồng từ ERP sang HRM. Gộp 3 loại hợp đồng ERP (bán/nguyên tắc/dự án) thành **1 hợp đồng duy nhất** ở HRM, tạo **1-1 từ báo giá trúng thầu**. Cấu trúc dòng hàng giống báo giá, thêm khối trường riêng của hợp đồng.

## Quyết định chốt (brainstorming 2026-08-10)
- **1 báo giá → 1 hợp đồng** (`quotation_id` UNIQUE), không cột `type`.
- **Snapshot (Cách 1)**: copy dòng hàng từ báo giá sang bảng riêng; dòng hàng **đóng băng** (read-only), chỉ nhập trường riêng của HĐ.
- **DB gộp `erp_hrm_check`** → mọi bảng prefix **`hrm_`** (tránh va chạm `contracts`/`contract_*` ERP cũ).
- Khối v1: **A** định danh/hiệu lực, **B** bên ký, **C** tài khoản/pháp nhân, **E** điều khoản thanh toán nhiều đợt, **H** đính kèm scan. Gác: D (giao hàng), F (kế toán/quyết toán), mẫu in, **phụ lục**.
- **Có bước phê duyệt** hợp đồng; trạng thái giữ enum ERP, v1 kích hoạt 6 trạng thái đầu.
- **Phân quyền 4 cấp** giống báo giá.
- **Xóa** chỉ khi `DANG_TAO`. Bắt buộc nhập: Ngày ký + Ngày hiệu lực. Điều khoản thanh toán lệch tổng: **chỉ cảnh báo**. Auto-fill pháp nhân/TK công ty nếu có danh mục.

## Bảng chính
`hrm_contracts` + con: `hrm_contract_groups`, `hrm_contract_product_prices`, `hrm_contract_service_items`, `hrm_contract_discounts`, `hrm_contract_process_payments` (mới), `hrm_contract_histories`, + `files` (đính kèm).

## Khuôn tham chiếu
Clone từ module Báo giá HRM (`Modules/Assign`, `pages/assign/quotations`). Tham khảo `SettlementContract` cho pattern cha-con + duyệt.

## HTHT (Hỗ trợ hạch toán) — bổ sung 2026-08-13
Spec đầy đủ: `docs/superpowers/specs/2026-08-13-hop-dong-htht-design.md`.
- HTHT = bảng phân tích giá + phân bổ thưởng/hoa hồng phòng–NV. **Không** sinh `account_details` (bút toán GL là downstream, ngoài scope).
- Tái dùng **cụm bảng ERP** `firm_support_accounting (+ 3 con)` polymorphic (`contractable_type = ...Contract`), tái dùng cấu hình `regulations` + `CompanyRuleCommission` + `Config.tndn`.
- Có **màn HTHT** riêng: preview khi chưa duyệt (không action); Duyệt trên màn HTHT = HĐ Có hiệu lực (đã gộp 1 bước, bỏ "Xác nhận hiệu lực").
- Field thiếu (`sale_max_percent`/`standard_price`/`net_price`/`cost_price`): **thêm cột + snapshot lúc tạo HĐ** tra product master qua `erp_product_id`/`bom_list_product_id` (A1, giống ERP). `market_costs` nhập tay (0).
- Phase A (phòng thực hiện) ✅ xong. Còn B (bóc tách giá), C (phân bổ phòng/quy chế), D (màn + luồng duyệt), E (verify E2E).
