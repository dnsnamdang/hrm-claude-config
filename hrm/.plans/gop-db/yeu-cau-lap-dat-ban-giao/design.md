# Phiếu yêu cầu lắp đặt, bàn giao (ERP → HRM) — @khoipv

Spec chi tiết: `docs/superpowers/specs/gop-db/2026-11-16-yeu-cau-lap-dat-ban-giao-design.md`

**Mục tiêu:** port ERP `assemblyRequest.*` (Lắp đặt - BH - SC › Phiếu yêu cầu lắp đặt, bàn giao) sang
`/customer-care/assembly-requests` — danh sách (`?type=all` + lối `?type=wait-approve`), thêm/sửa, chi tiết + Duyệt / Từ chối /
Chuyển phòng tiếp nhận / Tạo phiếu giao việc, In, Xuất Excel, Lịch sử. Khuôn: màn Giao việc khác (`assign-other-requests`).

**Quyết định (user chốt 16/11/2026):**
1. Nguồn HĐ **2 nguồn** (ERP `firm_contracts` + HRM `hrm_contracts`) như Giao việc khác → thêm `assembly_requests.hrm_contract_id`,
   `firm_contract_id` nullable. HĐ HRM chưa có SL đã xuất → tạm thời chưa ra hàng lắp được.
2. Phân quyền theo cấp **y ERP** — dùng lại mã `customer_care.phieu_yeu_cau_lap_dat_ban_giao.view` (scopes) +
   `..._truong_phong.approve`, thêm platform `hrm`.
3. Sửa / Xoá: người tạo && (Đang tạo | Từ chối), xoá cứng — y ERP.
4. Subagent: Opus 5.5.
5. Popup HĐ dùng lại `AssignOtherContractSourceService::contracts()` (thêm tham số bỏ lọc "đã có phiếu"); HĐ HRM chỉ lấy `need_install = 1`.

**Lệch ERP có chủ ý:** màu trạng thái theo SRS; lọc ngày theo `date_expected` (ERP lọc cột không tồn tại); nhãn "Người tạo / Ngày tạo".
**Không port:** `?type=assign-task` (đã có màn Phiếu chờ giao việc), `exportables` (ERP đã bỏ).
