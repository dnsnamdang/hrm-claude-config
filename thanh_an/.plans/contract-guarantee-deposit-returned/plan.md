# Thêm cột "Hoàn ký quỹ" — Tab bảo lãnh HĐ + Báo cáo bảo lãnh

**Phụ trách:** @khoipv
**Ngày tạo:** 23/09/2026

## Mục tiêu
Thêm cột nhập liệu **Hoàn ký quỹ** (`deposit_returned`) vào tab "Bảo lãnh thực hiện hợp đồng"
(màn thêm/sửa hợp đồng), đặt ngay sau cột "Tiền ký quỹ", nhập bằng `currency-input` giống
"Tiền ký quỹ". Dữ liệu chảy xuống màn báo cáo `contract/reports/guarantee_contract`
(cột "Hoàn ký quỹ" + "Còn lại" đã có sẵn trên UI nhưng đang gán cứng `null`).

## Quyết định
- Chỉ áp dụng cho bảo lãnh **hợp đồng** (`contract_guarantees`). Không thêm cho
  `bid_package_guarantees` → dòng báo cáo nguồn gói thầu để trống cột này.
- Dòng "Tổng" (lưới + Excel) **có** cộng tổng cột Hoàn ký quỹ.
- Cột "Còn lại" = Tiền ký quỹ − Hoàn ký quỹ (logic `remainingDepositValue` đã có sẵn, không sửa).
- Migration chỉ thêm cột, không foreign key.

## Task

### Phase 1 — Backend (hrm-thanhan-api)
- [x] Migration `add_deposit_returned_to_contract_guarantees_table` — `decimal(16) default 0`, comment "Hoàn ký quỹ", đặt sau `deposit_fee`
- [x] `ContractGuarantee` — thêm `deposit_returned` vào `$fillable`
- [x] `ContractDetailResource` — trả `deposit_returned` trong mảng `guarantees`
- [x] `ReportGuaranteeResource` — trả `deposit_returned`
- [x] `ReportGuaranteeFlatResource` — trả `deposit_returned`
- [x] Chạy `php artisan migrate`

### Phase 2 — Frontend tab bảo lãnh (hrm-thanhan-client)
- [x] `pages/contract/contract/components/GeneralComponent.vue` — thêm `<b-th>Hoàn ký quỹ</b-th>` sau "Tiền ký quỹ"
- [x] Thêm ô `currency-input v-model="guarantee.deposit_returned"` tương ứng

### Phase 3 — Frontend báo cáo bảo lãnh
- [x] `pages/contract/reports/guarantee_contract/index.vue` — map `deposit_returned` thật ở 3 chỗ (`buildRows`, `buildFlatRows`, `flattenGuarantees`) thay vì `null`
- [x] Computed `totalDepositReturned` + hiển thị ở ô trống trên dòng Tổng của lưới
- [x] Excel: cộng `deposit_returned` vào object totals + dòng "Tổng"

### Phase 4 — Kiểm thử (chờ user test UI)
- [ ] Nhập Hoàn ký quỹ ở tab bảo lãnh → Lưu → mở lại HĐ thấy đúng giá trị
- [ ] Báo cáo bảo lãnh: cột Hoàn ký quỹ + Còn lại hiển thị đúng, dòng Tổng đúng
- [ ] Xuất Excel: 2 cột + dòng Tổng khớp lưới

### Checkpoint — 23/09/2026
Vừa hoàn thành: toàn bộ code BE + FE, đã chạy `php artisan migrate` thành công (cột `contract_guarantees.deposit_returned`)
Đang làm dở: không
Bước tiếp theo: build lại client + hard refresh, test UI tab bảo lãnh và màn báo cáo
Blocked:
