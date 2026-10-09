# Fix DHNT lập được với mặt hàng từ phụ lục CHƯA DUYỆT

## Bug
Đơn hàng nguyên tắc (DHNT, type 8) lập + duyệt được với mặt hàng chỉ có trong
phụ lục bổ sung CHƯA DUYỆT (status=1). Vì `FirmContract::final_products()` gom
tab-product theo `root_firm_contract_id` mà KHÔNG lọc status của phụ lục sở hữu.
Case thật: đơn DHNT_TPV_MT_KD_26_1368_MAF.2707.26 (fc 25041) có MARA-P0704 —
mã này chỉ nằm trong PLBS2 (fc 25040, status=1, chưa duyệt).

## Điều kiện hợp lệ (chốt)
Mặt hàng phải thuộc contract sở hữu có `status = DA_DUYET (3)` → bao gồm HĐ gốc
+ phụ lục bổ sung ĐÃ DUYỆT; tự loại phụ lục chưa duyệt. (Kiểm chứng: parent
22027 → 160 SP hợp lệ, loại đúng MARA-P0704.)

## Tasks
- [x] Fix 1: `FirmContractService::getDataForPrincipleOrder` — eager-load
      `final_products` kèm closure lọc `firm_contract_id IN (firm_contracts status=3)`
      → verify: parent 22027 còn 160 SP, loại đúng MARA-P0704.
- [x] Fix 2 (phòng thủ): `PrincipleOrderService::validateProductsInApprovedScope`
      + gọi trong `PrincipleOrderController@store` → chặn payload FE chứa SP
      ngoài tập hợp lệ.
- [x] php -l 3 file PASS
- [ ] (User) test lại màn tạo DHNT: SP phụ lục chưa duyệt không hiện + submit payload lạ bị chặn
- [ ] (Hỏi) Xử lý dữ liệu đơn 25041 đã lỡ tạo với MARA-P0704 (fix code không dọn data cũ)
