# Plan — Xóa dữ liệu giảm giá hàng loạt ở Báo giá (Redmine #10900)

> @junfoke — Nhánh `task_10900` (tách từ `tpe`), chỉ repo `hrm-client`.
> Design: `.plans/quotation-clear-discount/design.md`

## Phase 1 — FE (pages/assign/quotations/_id/edit.vue)

- [x] 1.1 Computed `hasDiscountDataToClear` — GG mặt hàng: có dòng nào `discount_percent`/
      `discount_amount` > 0; GG tổng: `totalAllocatedDiscount` > 0
- [x] 1.2 Computed `clearDiscountLabel` — "Xóa giảm giá" (GG mặt hàng) / "Xóa phân bổ" (GG tổng)
- [x] 1.3 Method `clearItemDiscounts()` — GG(%) + GG(đ) mọi dòng hàng hóa và dịch vụ về 0
- [x] 1.4 Method `clearAllocatedDiscounts()` — cột Phân bổ GG mọi dòng + dòng Chi phí vận chuyển về 0
- [x] 1.5 Method `handleClearDiscount()` — popup xác nhận theo đúng câu chữ spec, rẽ nhánh theo
      `discountMethod`, toast báo kết quả
- [x] 1.6 Nút trên toolbar cạnh nút "Áp dụng" (làm tròn): `primary status="danger"`, icon
      `ri-eraser-line`, disable khi không có dữ liệu GG, ẩn khi không có quyền GG
- [x] 1.7 Vá lỗi có sẵn: `clearAllDiscountData()` reset thêm `shippingAllocatedDiscount`
- [x] 1.8 Kiểm line ending — file đang CRLF, `git diff --stat` phải ra số dòng đúng bằng phần sửa

## Phase 2 — Verify

- [x] 2.1 GG mặt hàng: nhập GG vài dòng → bấm Xóa giảm giá → GG về 0, Đơn giá sau GG / Thành tiền /
      VAT / Tổng báo giá / Tỷ suất lợi nhuận tính lại đúng
- [x] 2.2 GG tổng: thêm khoản GG + phân bổ tự động → bấm Xóa phân bổ → cột Phân bổ GG (gồm dòng vận
      chuyển) về 0, bảng khoản GG còn nguyên, nút "Phân bổ tự động" hiện lại
- [x] 2.3 Nút ẩn khi tài khoản không có quyền "Cho phép thêm giảm giá trong báo giá" — PASS trên
      dev server riêng (port 3005, bản hrm-cursor). Ca "disable khi GG = 0" mới kiểm được ở mức
      computed, chưa bấm được trên UI vì tài khoản dev không có quyền GG (ô chọn GG bị khoá)
- [x] 2.4 Kiểm theo PAYLOAD mà nút Lưu gửi lên BE (xem mục dưới) — không tạo được báo giá thật vì tài khoản dev không phải Sale phụ trách dự án nào
- [x] 2.5 Màn Tạo mới (create.vue) hoạt động y hệt màn Sửa

### Checkpoint — 2026-09-11
Vừa hoàn thành: tách nhánh `task_10900` từ `tpe`, chốt 3 điểm spec với user, viết design + plan
Đang làm dở: chưa sửa code
Bước tiếp theo: task 1.1 → 1.7 trong `pages/assign/quotations/_id/edit.vue`
Blocked:

### Kiểm bằng hàm thật trong bundle đã build (2026-09-11, port 3005)

Tài khoản dev `namdangit@gmail.com` KHÔNG có quyền "Cho phép thêm giảm giá trong báo giá" nên ô chọn
GG bị khoá — không bấm được nút trên UI thật. Đã gọi thẳng computed/method từ `vm.$options` của
bundle đang chạy với dữ liệu giả lập, kết quả:

| Ca | Kết quả |
| --- | --- |
| GG mặt hàng — nhãn nút | `Xóa giảm giá` ✔ |
| GG mặt hàng — sau khi xóa | GG(%) + GG(đ) mọi dòng hàng hóa & dịch vụ = 0, `discount_input_mode` = null, `hasDiscountDataToClear` true → false ✔ |
| GG tổng — nhãn nút | `Xóa phân bổ` ✔ |
| GG tổng — sau khi xóa | Phân bổ dòng = 0, phân bổ vận chuyển 50.000 → 0, tổng đã phân bổ 550.000 → 0, `allocationStale` = false ✔ |
| GG tổng — bảng khoản GG | GIỮ NGUYÊN (`quotationDiscounts` còn đủ) ✔ |
| Không GG | `hasDiscountDataToClear` = false → nút ẩn ✔ |
| Vá lỗi cũ `clearAllDiscountData()` | phân bổ vận chuyển 75.000 → 0 ✔ |
| Không có quyền GG | nút KHÔNG render ✔ |

CÒN LẠI (cần tài khoản có quyền GG): bấm nút thật → popup xác nhận → số liệu Đơn giá sau GG /
Thành tiền / VAT / Tổng báo giá / Tỷ suất lợi nhuận tính lại; lưu rồi mở lại.

### Checkpoint — 2026-09-11 (lần 2)
Vừa hoàn thành: code xong Phase 1 (7 task), syntax check PASS, kiểm logic bằng hàm thật trong bundle
Đang làm dở: Phase 2 — 4/5 ca UI chưa bấm được vì tài khoản dev thiếu quyền GG
Bước tiếp theo: chờ user quyết cấp quyền "Cho phép thêm giảm giá trong báo giá" cho tài khoản dev (đụng DB) hay tự verify bằng tài khoản khác
Blocked: quyền GG của tài khoản dev

## Phase 3 — Vá quyền thiếu của #10789 (phát sinh, user duyệt cho làm kèm)

- [x] 3.1 `PermissionsTableSeeder.php`: thêm quyền `Cho phép thêm giảm giá trong báo giá` (id **1182**,
      group `Báo giá`, type 4) — đặt ở **CUỐI** danh sách `Permission::create` theo quy tắc user chốt
      2026-09-11, id độc nhất và tăng dần
- [x] 3.2 Chạy lại seeder trên DB `hrm_prod_30_3_26` (đúng luồng: seeder truncate rồi insert lại theo id cố định)
- [x] 3.3 Gán quyền cho role **Super admin** qua giao diện Thiết lập → Phân quyền (không ghi thẳng DB)
- [ ] 3.4 (còn lại) Báo lên Redmine #10789: FE gate bằng quyền này từ trước nhưng BE chưa bao giờ seed → trước
      khi vá thì KHÔNG tài khoản nào (kể cả Super admin) bật được giảm giá trên báo giá

### Verify trên UI thật — PASS (2026-09-11)

Môi trường: FE `:3005` (hrm-cursor, nhánh `task_10900`) → API `:8002` (hrm-cursor/hrm-api, nhánh
`task_10900`) → DB `hrm_prod_30_3_26`. KHÔNG đụng `gop_db`.

| Ca | Trước | Sau | Kết quả |
| --- | --- | --- | --- |
| Không GG | — | — | Nút ẩn ✔ |
| GG mặt hàng, chưa nhập GG | — | — | Nút hiện chữ "Xóa giảm giá", **disable** ✔ |
| GG mặt hàng, GG 10% ở 2 dòng | Tổng GG 14.920.000 · Tổng sau GG 770.480.005 | Tổng GG **0** · Tổng sau GG **785.400.005** (+14.920.000) | ✔ GG(%) + GG(đ) mọi dòng = 0, nút tự disable lại |
| Popup xác nhận (GG mặt hàng) | — | "Bạn có chắc chắn muốn xóa toàn bộ dữ liệu giảm giá?" | ✔ đúng câu spec |
| Đổi sang GG tổng | — | — | Nhãn nút đổi thành "Xóa phân bổ" ✔ |
| GG tổng, khoản GG 20.000.000 + phân bổ tự động + 500.000 cho dòng vận chuyển | Đã phân bổ 20.500.000 (6 dòng) · Tổng sau GG 765.400.005 | Đã phân bổ **0** · vận chuyển **0** · Tổng sau GG **785.400.005** | ✔ |
| Popup xác nhận (GG tổng) | — | "Bạn có chắc chắn muốn xóa toàn bộ giá trị phân bổ giảm giá? Tất cả giá trị tại cột Phân bổ GG sẽ được đặt về 0" | ✔ đúng câu spec |
| Bảng khoản GG sau khi xóa phân bổ | 1 khoản, Tổng GG 20.000.000 | **giữ nguyên** 1 khoản, Tổng GG 20.000.000 | ✔ đúng quyết định user |
| Nút "Phân bổ tự động" | ẩn (đã phân bổ) | hiện lại | ✔ |

Ảnh: `btn-xoa-giam-gia-disabled.png`, `popup-xac-nhan-xoa-giam-gia.png`, `sau-khi-xoa-phan-bo.png`
(thư mục `hrm-client/`).

**Cách dựng dữ liệu test:** màn Tạo mới báo giá + nạp 10 dòng hàng hoá thật từ API báo giá
BG-2026-00103, GG nhập qua đúng handler `onDiscountPercentInput` mà ô GG(%) dùng. Loại tiền tệ set
bằng `form.currency_id` (ô chọn dùng select2, thao tác qua Playwright không ăn) — không liên quan
chức năng đang test. Toàn bộ thao tác XÓA đều là **bấm nút thật + bấm xác nhận thật trên popup**.

**CHƯA chạy:** ca "Lưu rồi mở lại xem dữ liệu GG đã về 0" — phải tạo một báo giá rác trong DB
(cần dự án + khách hàng). Luồng lưu KHÔNG bị sửa trong đợt này (payload giữ nguyên), nên rủi ro thấp.

### Checkpoint — 2026-09-11 (lần 3)
Vừa hoàn thành: Phase 1 (code) + Phase 2 verify UI thật PASS + Phase 3 vá quyền thiếu của #10789
Đang làm dở: không
Bước tiếp theo: user xem lại diff 2 repo; cân nhắc chạy nốt ca "Lưu rồi mở lại"; báo Redmine #10789 + #10900
Blocked: không

### Ca "Lưu rồi mở lại" — kiểm bằng payload (2026-09-11)

**Không tạo được báo giá thật:** BE trả `422 "Bạn không phải Sale phụ trách dự án này"` khi tài khoản
dev (`namdangit@gmail.com`, employee 13) tạo báo giá; API `prospective-projects/getAll?main_sale_mine=1`
trả **0 dự án** — tài khoản này không phụ trách dự án nào nên không có đường tạo báo giá hợp lệ.

Thay vào đó kiểm **đúng payload mà nút Lưu gửi lên BE** (gọi `save(false, {dryRun: true})` — chính
nhánh dựng payload của luồng lưu), trước và sau khi bấm nút + xác nhận thật:

| Trường trong payload | GG mặt hàng trước | sau | GG tổng trước | sau |
| --- | --- | --- | --- | --- |
| số dòng còn GG | 2 | **0** | — | — |
| tổng `discount_amount` | 4.860.000 | **0** | — | — |
| tổng `allocated_discount_amount` | 0 | 0 | 20.000.000 | **0** |
| `shipping_allocated_discount` | 0 | 0 | 500.000 | **0** |
| số khoản GG tổng | 0 | 0 | 1 (20.000.000) | **1 (20.000.000) — giữ nguyên** |

⇒ Giá trị gửi xuống DB đúng bằng 0 sau khi xóa; bảng khoản GG tổng không bị đụng. Luồng lưu không
bị sửa trong đợt này nên phần ghi/đọc DB giữ nguyên hành vi cũ.

**DB sạch:** không có báo giá rác nào được tạo (vẫn 102 bản ghi, mới nhất vẫn là BG-2026-00107).

**Muốn chạy roundtrip thật** thì cần 1 trong 2: gán tài khoản dev làm Sale phụ trách một dự án test,
hoặc dùng tài khoản Sale có sẵn dự án.

### Checkpoint — 2026-09-11 (lần 4, kết)
Vừa hoàn thành: commit cả 2 repo trên nhánh `task_10900` — `hrm-client` f9d584dfc (+100 dòng
`pages/assign/quotations/_id/edit.vue`), `hrm-api` 705acbfc7 (+5 dòng `PermissionsTableSeeder.php`).
Đã trả `.env` của hrm-client về nguyên trạng (API 8000 / port 3000), xóa file `.env.bak-task10900`,
tắt dev server 3005 + API 8002.
Đang làm dở: không
Bước tiếp theo: chưa merge / chưa push. Khi deploy phải chạy lại PermissionsTableSeeder ở mọi môi
trường rồi gán quyền "Cho phép thêm giảm giá trong báo giá" cho role cần dùng. Còn task 3.4 — báo
Redmine #10789 + #10900.
Blocked: không

## ⚠️ Đính chính Phase 3 (2026-09-11) — quyền KHÔNG thiếu, chỉ thiếu ở nhánh `tpe`

Khi build nhánh `tpe-develop-assign`, seeder chết:
`Duplicate entry 'Cho phép thêm giảm giá trong báo giá-api'`.

Nguyên nhân: quyền này **đã tồn tại từ trước** trên `tpe-develop-assign` với **id 1173**
(commit `e04418092` "fix quyen"). Nhánh `tpe` — nơi tách ra `task_10900` — chưa có, nên lúc rà tôi
kết luận "BE chưa bao giờ seed quyền này" (kết luận đó chỉ đúng trong phạm vi nhánh `tpe`). Commit
`705acbfc7` thêm id 1182 cùng tên -> merge vào là 2 dòng trùng `name` + `guard_name`, vi phạm unique.

Đã xử lý:
- `tpe-develop-assign`: commit `8f174e748` — gỡ dòng id 1182, giữ 1173 (có trước, đã gán cho role).
- `task_10900`: commit `390dd3cf3` — gỡ luôn dòng đó để nhánh này không mang mầm lỗi sang nhánh khác.
- Chạy lại `PermissionsTableSeeder` trên DB local: **thành công**, quyền còn đúng 1 dòng id 1173.

**Bài học ghi lại:** trước khi thêm quyền mới phải `grep` tên quyền trên **các nhánh phát triển
khác** (`git show <branch>:...PermissionsTableSeeder.php | grep "<tên quyền>"`), không chỉ nhánh
đang đứng — seeder unique theo `name` + `guard_name` chứ không theo id.

## Phase 4 — Test case cho QA (2026-09-14)

- [x] 4.1 `gen_testcase.py` + `testcase.xlsx` — 55 TC / 9 section La Mã + 3 TC phân quyền, P0 58%.
      Dựng bằng `tc_engine.py` của skill `testcase-documenter`; bộ kiểm tra thuật ngữ in "OK - sach".
- [x] 4.2 Ghi rõ ở mục 9 phần mô tả 5 bẫy dễ sai: nút cố tình hiện-mờ khi giảm giá = 0, "Xóa phân bổ"
      KHÔNG xoá bảng khoản giảm giá tổng, luôn kiểm dòng Chi phí vận chuyển, chưa Lưu thì dữ liệu cũ
      còn nguyên, định dạng số chuẩn quốc tế.
