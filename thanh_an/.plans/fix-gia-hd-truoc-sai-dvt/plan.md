# Fix: "Giá bán HĐ trước" không quy đổi đơn vị tính — @khoipv

## Bối cảnh

Phát hiện ở **BG-739** (`https://demothanhan.dnsmedia.vn/plan/quotation/739`, KH *CÔNG TY CỔ PHẦN Y TẾ PHÚC THỊNH*, tạo từ dự án DT-088/2026):
cột **Giá bán HĐ trước** của mặt hàng `Viên nén khử khuẩn bề mặt` (product_id 1084) hiển thị **3.500** trong khi giá đúng là **350.000**.

Giá được tra từ **HD-471/2026** (Bệnh Viện Bệnh Nhiệt Đới, cùng tỉnh HCM — nhánh fallback `source = province`),
đơn giá 3.500/**Viên**; báo giá tính theo **Hộp** (1 Hộp = 100 Viên) → phải quy đổi ×100 nhưng code bỏ qua.

## Nguyên nhân gốc

Logic lấy giá bị **copy làm 6 bản** ở 3 module, và 3 bản trong `GeneralComponent` **thiếu đoạn quy đổi ĐVT**:

| File | Kích hoạt khi | Quy đổi ĐVT |
|---|---|---|
| `pages/plan/quotation/components/ProductComponent.vue:1560` | thêm hàng hóa | có |
| `pages/plan/quotation/components/GeneralComponent.vue:1825` | chọn dự án / đổi khách hàng | **KHÔNG** |
| `pages/contract/contract/components/ProductComponent.vue:1871` | thêm hàng hóa | có |
| `pages/contract/contract/components/GeneralComponent.vue:2536` | chọn HĐ liên quan / đổi khách hàng | **KHÔNG** |
| `pages/bid_package/bid_package/components/ProductComponent.vue:1823` | thêm hàng hóa | có |
| `pages/bid_package/bid_package/components/GeneralComponent.vue:1213` | chọn dự án / đổi khách hàng | **KHÔNG** |

Thêm 1 lỗi phụ: `bid_package/GeneralComponent.getProducts()` map mảng `units` **thiếu field `coefficient`** → dù có thêm quy đổi vẫn ra hệ số 1.

## Phạm vi ảnh hưởng (audit trên `thanhan_stag_22092026`, nhánh "cùng khách hàng")

| Nhóm | Số dòng | Sai |
|---|---|---|
| ĐVT báo giá trùng ĐVT HĐ | 1.685 (96%) | 0 |
| Khác ĐVT, hệ số bằng nhau | 8 | 0 |
| Khác ĐVT + khác hệ số | 56 | **4** (BG-658) |

→ Lỗi chỉ lộ khi hội đủ 3 điều kiện: khác ĐVT + khác hệ số + lần tính cuối chạy qua `GeneralComponent`.

## Task

### Phase 1 — FE: gộp logic + fix quy đổi
- [x] Tạo helper mới `hrm-thanhan-client/utils/previousContractPrice.js` (`convertPreviousContractPrice`) — helper MỚI, không sửa hàm dùng chung có sẵn
- [x] `pages/plan/quotation/components/ProductComponent.vue` — dùng helper
- [x] `pages/plan/quotation/components/GeneralComponent.vue` — dùng helper (fix chính của BG-739)
- [x] `pages/contract/contract/components/ProductComponent.vue` — dùng helper
- [x] `pages/contract/contract/components/GeneralComponent.vue` — dùng helper
- [x] `pages/bid_package/bid_package/components/ProductComponent.vue` — dùng helper
- [x] `pages/bid_package/bid_package/components/GeneralComponent.vue` — dùng helper
- [x] `pages/bid_package/bid_package/components/GeneralComponent.vue:getProducts()` — bổ sung `coefficient: val.conversion_factor || 1` vào mảng `units`

### Phase 2 — Verify
- [x] Kiểm tra cú pháp 6 file (parse SFC)
- [x] Đối chiếu lại bằng số liệu HD-471/2026 → 3.500 × 100 = 350.000

### Phase 3 — Dữ liệu cũ (CHỜ USER CHỐT)
- [ ] Viết script rà + sửa lại `price_pre_contract` đã lưu sai (BG-739, BG-658, và quét cả `contract_products` / `bid_package_products`)
- [ ] CHƯA chạy trên demo/production — chờ xác nhận

## Ngoài phạm vi (đã báo user, chưa làm)
- Không lọc `contracts.status` → HĐ nháp/chờ duyệt/không duyệt/hủy vẫn được lấy làm "HĐ trước"
- Sắp xếp theo `contracts.created_at` thay vì ngày ký/hiệu lực
- UI không cho biết giá đến từ HĐ của **khách hàng khác cùng tỉnh** (API có trả `contract_code` nhưng FE bỏ đi)

### Checkpoint — 2026-09-23
Vừa hoàn thành: Phase 1 + Phase 2 — tạo helper `utils/previousContractPrice.js`, thay 6 bản copy ở 3 module bằng helper, bổ sung `coefficient` cho `units` ở `bid_package/GeneralComponent.getProducts()`. Parse SFC 6/6 file sạch (vue-template-compiler + @babel/parser), unit test helper 7/7 PASS (case BG-739 thật: 3.500/Viên × hệ số 100 → 350.000/Hộp).
Đang làm dở: không có.
Bước tiếp theo: build lại client + hard refresh, mở lại BG-739 ở màn **Sửa** để hệ thống tính lại và lưu đè giá đúng; sau đó chốt Phase 3 (script sửa dữ liệu cũ đã lưu sai).
Blocked: Phase 3 chờ user duyệt mới chạy trên DB.
