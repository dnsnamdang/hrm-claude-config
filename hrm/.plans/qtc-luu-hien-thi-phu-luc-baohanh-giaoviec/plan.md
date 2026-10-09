# QTC: lưu + hiển thị người/phòng quyết toán công ở phụ lục bổ sung, phiếu bảo hành, yêu cầu giao việc khác

Nối tiếp feature "Quyết toán công theo HĐ" (Assign). Hiện `SettlementContractService::syncEmployeeQtcContractErp`
chỉ lưu `employee_qtc_id`/`department_qtc_id` về HĐ CHÍNH (TpWrContract/TpContract), CHƯA lưu về phụ lục bổ sung.

## Yêu cầu (user)
1. Lưu + hiển thị người/phòng QTC ở **phụ lục bổ sung** — cả HĐDV (wr) và HĐ hãng (firm)
2. Hiển thị người/phòng QTC trên **phiếu bảo hành**
3. Hiển thị người/phòng QTC trên **yêu cầu giao việc khác**
4. Kiểm tra: **yêu cầu giao việc khác KHÔNG gắn hợp đồng** có lập QTC được không

## Quyết định (user chốt)
1. Lan QTC xuống **phụ lục bổ sung + phiếu bảo hành** (cả wr + firm)
2. Giao việc khác KHÔNG gắn HĐ → **KHÔNG** cho lập QTC (giữ nguyên)
3. Hiển thị QTC ở phụ lục/bảo hành → **CHỈ ở ERP blade** (không làm transformer HRM)

## Phát hiện
- Cột `employee_qtc_id` + `department_qtc_id` ĐÃ CÓ sẵn trên `wr_service_contracts` + `firm_contracts` (phụ lục/bảo hành là hàng cùng bảng) → không cần migration.
- Firm blade (`sale/firm/contracts/form` + `sale/firm/addition_annexes/form`) ĐÃ hiển thị QTC (người+phòng) → chỉ thiếu DATA.
- wr (HĐDV): quản lý ở Customercare, chưa rõ blade nào hiển thị QTC.

## Tasks
- [x] Khảo sát luồng QTC (agent)
- [x] Fix A (HRM): `SettlementContractService::syncEmployeeQtcContractErp` lan QTC xuống hàng con — wr (parent_id, type∈{2,3}) + firm (parent_contract_id, type=2). php -l PASS.
- [x] Fix B (ERP blade): thêm hiển thị người/phòng QTC ở blade phụ lục HĐDV (wr) + phiếu bảo hành + giao việc khác (firm đã có sẵn)
- [x] Fix C (giao việc khác): QTC lấy từ firm_contract liên kết (option A)
- [ ] Verify runtime (browser)

## Ghi chú
- employee_qtc_id = người QTC, department_qtc_id = phòng QTC (trên HĐ)
- employee_info_qtc_ids (JSON) trên wr_assign_tasks = NV QTC theo từng PCT
