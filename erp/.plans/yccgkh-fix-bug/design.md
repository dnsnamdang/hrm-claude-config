# Design (tóm tắt) — Fix 22 bug YCCGKH

**Owner:** @junfoke · **Ngày:** 2026-08-19 · **Spec chi tiết:** `docs/superpowers/specs/2026-08-19-yccgkh-fix-bug-design.md`

## Mục tiêu
Fix 22 bug module **Phiếu YC chuyển giao khách hàng (YCCGKH)** trên ERP, nguồn Redmine http://quanly.dnsmedia.vn (dự án "Fix Bug - HRM (Nội bộ)", issue 10831–10871).

## Scope & nguồn code
- Repo ERP: **`d:\CompanyProject\hrm-cursor\TanPhatDev`** (bản B), nhánh **`task_10696`**. KHÔNG phải bản A (`d:\CompanyProject\TanPhatDev`) — 2 bản là 2 dòng phát triển khác nhau, bản B là nguồn chính (module dựng lại Task 1→10).
- Repo HRM (cho #10871): `d:\CompanyProject\hrm-cursor\hrm-api` (Modules/Assign).
- File bàn giao tham khảo: `d:\CompanyProject\BANGIAO-YCCGKH.md` (mô tả theo bản A — verify code bản B trước khi tin).

## 4 nhóm bug
- **A — Danh sách/bộ lọc (9):** 10867 (sắp thứ tự trường 3 hàng), 10846 (Bộ phận DS chờ duyệt), 10853 (Bộ phận+Trạng thái + searchDataApprove), 10850 (ngày có giờ), 10849 (lọc Người lập ra 0), 10848 (combobox trùng), 10851 (Đang tạo thêm Xóa), 10852 (Không duyệt thêm Sửa+Xóa), 10869 (màu link menu).
- **B — Chi tiết (4):** 10868 (sắp cột lịch sử + viết hoa), 10854 (Gửi duyệt hiện lý do), 10855 (ẩn Hủy duyệt ở Đã duyệt), 10857 (notify khi duyệt).
- **C — Form (8):** 10831 (auto-fill ngày/nơi cấp), 10833 (KH trước đầy đủ), 10834 (disable khi chưa chọn KH), 10835 (TK ngân hàng + 4 label), 10836 (contact cá nhân), 10837 (file 60MB), 10832 (validate size client), 10838 (popup contact).
- **D — ERP↔HRM (1):** 10871 (duyệt YCCGKH cập nhật KH sang báo giá HRM).

## Quyết định lớn
- **Không sửa lib/route dùng chung:** bộ lọc Bộ phận qua cờ `search_by_parts` sẵn có của lib DATATABLE (chỉ bật cho big_boss/boss, tránh trùng manager); combobox Người lập/duyệt dùng **endpoint riêng** (searchCreators/searchApprovers) thay `employee.searchEmployeeByKeyword` (370 màn).
- **searchDataApprove (DS chờ duyệt):** mặc định lọc Chờ duyệt, cho lọc rộng khi user chọn Trạng thái khác (Option 1).
- **#10871:** Option A — thêm HTTP endpoint hrm-api `POST /api/v1/assign/quotations/erp-contract/{id}/sync-customer`; ERP gọi (Guzzle, try/catch không chặn luồng) trong approve()/cancelApprove() theo `contractable.hrm_quotation_id`. Chỉ cập nhật quotation (không đụng prospective_project).
- **10838:** popup contact = union CustomerContact của KH + contact trên báo giá (firm_quotations) của KH, dedup theo id/SĐT (diễn giải Claude chốt — chờ BA duyệt).

## Verify
Chạy thực tế server local bản B (`php artisan serve :8001`, DB erp_dev_30_01_26). Nhóm A/B/C verify end-to-end. #10871 ERP-side non-breaking (HRM end-to-end chờ dev-hrm vì DB local thiếu bảng quotations).

## Bonus phát hiện
`CustomerHandoverRequest` chưa cast `approved_at` → `$handover->approved_at->format()` crash màn Đã duyệt. Fix: thêm `'approved_at' => 'datetime'` vào $casts.
