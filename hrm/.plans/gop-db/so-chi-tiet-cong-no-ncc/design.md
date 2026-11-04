# Sổ chi tiết công nợ phải trả NCC — tóm tắt thiết kế

Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-11-04-so-chi-tiet-cong-no-ncc-design.md` (user duyệt 04/11/2026).

- Port ERP `account-detail.index` (bản NCC, không tham số) → `/finance/supplier-debt-details`, Tài chính › Kế toán công nợ › Nhà cung cấp.
- 4 ô bắt buộc: Tài khoản, Nhà cung cấp, Từ ngày, Đến ngày. NCC = `supplier_id OR customer_id`. Nhân viên = `contract_created_by`.
- Quyền 2 cấp tên y ERP (325/326): tổng công ty / công ty (`ad.company_id` = công ty mình OR `contract_created_by` = mình). 403 mọi endpoint.
- Đầu kỳ dùng ĐÚNG bộ lọc danh sách (user chốt). Ngoại tệ: đầu kỳ / PS / cuối kỳ theo từng loại tiền. Thêm In, Ghi chú = ghi chú chứng từ.
- Dùng chung khung sổ chi tiết với màn NV: `Services/AccountDebt/AccountLedgerService` + trait `AccountDebtCommon` + `ValidatesAccountDebtFilters`.
