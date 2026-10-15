# QTC: popup tạo quyết toán không hiện phiếu bảo hành

## Bug
Popup tạo QTC (`getDataContractWaitSettlement`) không hiện phiếu bảo hành để chọn.

## Nguyên nhân
Nhánh wr lọc `status IN [3,4,5,6]` (đúng cho HĐ: CO_HIEU_LUC=3, DANG_QUYET_TOAN=4, DA_QUYET_TOAN=5, DA_HOAN_THANH=6). Nhưng bảo hành (type=BAO_HANH=2) dùng bộ status RIÊNG: BH_DA_DUYET=2, BH_DANG_THUC_HIEN=3, BH_HOAN_THANH=4. Data: 13 phiếu bảo hành có QTC đều ở status 2 → bị [3,4,5,6] loại.

## Quyết định (user chốt: A)
- HĐ + phụ lục (type != 2): giữ status [3,4,5,6]
- Bảo hành (type = 2): status [2,3,4]

## Tasks
- [x] BE: `SettlementContractController::getDataContractWaitSettlement` — lọc status theo loại (type-aware) trong nhánh wr
- [x] php -l sạch
- [ ] User verify: phiếu bảo hành (đã duyệt/đang thực hiện/hoàn thành) có gán QTC + chưa QTC → hiện trong popup

## Ghi chú
BE-only, hrm-api, branch `tpe`. Không thể chỉ thêm 2 vào [3,4,5,6] chung (sẽ kéo HĐ chờ duyệt vào).
