# Plan — Batch 10 task Redmine (nhánh tpe-develop-assign_fix)

Nguồn: quanly.dnsmedia.vn issues 9752, 10741, 10804, 10810, 10818, 10840, 10885, 10897, 10948, 10986
Phụ trách: @cuong61n

## Trạng thái khảo sát ban đầu
- [x] #10804 Bảng giá ERP cho Báo giá — ĐÃ CÓ SẴN (migration add_price_type_id_to_quotations, QuotationService applyErpUnitPrice)
- [x] #10840 Tự sinh mã hàng tạm — ĐÃ CÓ SẴN (QuotationService sinh HHBG, BomListService tương ứng)

## Phase 1 — #10741 + #10810: Mô tả giải pháp (2 task trùng nhau)
- [x] BE: migration thêm cột `description` (text nullable) vào `solutions`
- [x] BE: nhận + validate optional ở Request, trả về ở Resource
- [x] FE: textarea "Mô tả" ở form tạo/sửa giải pháp
- [x] FE: hiển thị "Mô tả" ở màn chi tiết (read-only)

## Phase 2 — #10897: Icon "Tạo yêu cầu làm giải pháp" ở danh sách dự án TKT
- [x] FE: thêm row-action, chỉ hiện với luồng "Nội bộ phòng ban" / "Liên phòng ban"
- [x] FE: điều hướng sang form tạo yêu cầu làm giải pháp + prefill dự án tiền khả thi

## Phase 3 — #10818: Báo cáo Dự án TKT theo PB - NV KD
- [x] BE: bỏ filter nhóm ngành / nhóm giải pháp, thêm filter loại hình hoạt động + lĩnh vực KD khách hàng (multi)
- [x] BE: đổi cột dữ liệu trả về
- [x] FE: đổi bộ lọc, tiêu đề phân nhóm, cột bảng

## Phase 4 — #10885: Sticky toolbar / Quick Add Bar / Thu gọn - Mở rộng (BOM + Báo giá)
- [x] FE (BOM): sticky toolbar + nút Thêm nhóm
- [x] FE (BOM): Quick Add Bar cuối mỗi nhóm
- [x] FE (BOM): Thu gọn/Mở rộng tất cả (toolbar + header bảng)
- [x] FE (BOM): icon mũi tên đã có sẵn + bổ sung click tiêu đề nhóm để đóng/mở
- [x] FE (Báo giá): sticky toolbar + Thêm nhóm, Thu gọn/Mở rộng tất cả, Quick Add Bar, icon mũi tên + click tiêu đề (edit.vue + _id/index.vue)

## Phase 5 — #10948: Báo giá tổng hợp trúng thầu → báo giá nguồn trúng thầu
- [x] BE: khi đánh dấu báo giá tổng hợp trúng thầu, cascade trạng thái các báo giá nguồn

## Phase 6 — #9752: Duyệt chuyển hàng tạm thành hàng dùng chung — ❌ USER CHỐT BỎ, KHÔNG LÀM
Quyết định 2026-08-18: user chốt bỏ task này. Lý do đưa ra quyết định (đã khảo sát xong):
- Luồng duyệt hàng tạm → hàng dùng chung ĐÃ CÓ cho Báo giá (`TmpProductSyncService`: sendApproval →
  ERP tạo hàng thật → pullStatus ghi `erp_product_id`), thủ công, mở khi báo giá Trúng thầu.
- Phía BOM chưa có: `bom_list_products` không có cột `erp_tmp_product_id` → phải dựng mới toàn bộ.
- KHÔNG có callback ERP báo "hợp đồng duyệt hiệu lực"; chỉ có `POST /v1/assign/quotations/erp-contract/{id}/mark`
  ERP gọi lúc LẬP hợp đồng. Muốn tự động theo hiệu lực thì phải bắt team ERP tích hợp thêm.
- Mô tả task trên Redmine chỉ có 1 dòng tiêu đề, không có AC.

## Phase 7 — #10986: Chuẩn hoá màn danh sách — ❌ USER CHỐT BỎ, KHÔNG LÀM
Quyết định 2026-08-18: user chốt bỏ. Hiện trạng đã rà xong (giữ lại để lần sau khỏi rà lại):
- **BR-02 cấu hình cột theo user: ĐÃ CÓ ĐỦ HẠ TẦNG.** Bảng `column_customizations` lưu theo
  `created_by` (user) + 1 cột JSON cho mỗi màn; đã phủ 27 màn. BE: `Modules/Human` —
  `ColumnCustomizationController` / `ColumnCustomizationService` / Entity `ColumnCustomization`.
  ⚠️ Thêm 1 màn = thêm 1 CỘT vào bảng (phải viết migration), không phải thêm 1 dòng.
- **BR-03 popup chọn trường khi xuất Excel: component ĐÃ CÓ** — `components/modal/export-modal.vue`
  (Select2 multiple + checkbox Chọn tất cả), NHƯNG mới chỉ dùng ở module Đào tạo, chưa dùng ở assign.
- **BR-01 gộp cột Mã - Tên: đã làm rải rác** bằng `V2BaseTitleSubInfo` + `separatorTitle="-"`
  (solution-groups, customers, bom-list, customer-scopes, tasks, request-solution, handover…), chưa phủ hết.
- Quy mô nếu làm: `pages/assign` có 27 màn danh sách (11 màn đã có cấu hình cột); toàn hệ thống 69 màn.


### Checkpoint — 2026-08-18
Vừa hoàn thành: #10741+#10810 (Mô tả GP), #10897 (icon tạo YC làm GP), #10818 (báo cáo đổi 2 chiều cơ cấu), #10948 (cascade trúng thầu). #10804 + #10840 xác nhận đã có sẵn.
Đang làm dở: chưa bắt đầu #10885, #9752, #10986
Bước tiếp theo: #10885 (sticky toolbar / quick add / thu gọn - mở rộng BOM + Báo giá)
Blocked: #10986 phạm vi toàn hệ thống — cần chốt phạm vi với user


### Checkpoint — 2026-08-18 (lần 2)
Vừa hoàn thành: #10885 phần BOM (BomBuilderTableCard.vue) — sticky toolbar + Thêm nhóm, Thu gọn/Mở rộng tất cả, Quick Add Bar cuối nhóm, click tiêu đề nhóm để đóng/mở.
Đang làm dở: #10885 phần Báo giá — `pages/assign/quotations/_id/edit.vue` (~5400 dòng) và `_id/index.vue` chưa đụng. Màn này CHƯA có state đóng/mở nhóm nên phải thêm mới hoàn toàn (expandedGroups + icon mũi tên + 3 mục còn lại), khuôn copy từ BomBuilderTableCard.vue.
Bước tiếp theo: làm #10885 cho Báo giá, rồi #9752, cuối cùng #10986.
Blocked: #10986 phạm vi toàn hệ thống — cần chốt phạm vi với user trước khi code.

### Khảo sát sẵn cho #10885 phần Báo giá (chưa sửa file nào)
- File chính: `hrm-client/pages/assign/quotations/_id/edit.vue`; màn xem: `_id/index.vue`
- Nhóm render qua computed `groupedRows()` (dòng ~1663): trả mảng phẳng đã sắp xếp Cấp 1 → Cấp 2,
  mỗi phần tử `{ id, temp_id, name, parents, level, romanLabel, groupRef }` — tương đương `renderGroups()` của BOM.
- Khoá nhóm để lưu trạng thái đóng/mở: `group.id || group.temp_id` (đã dùng làm `:key` ở template).
- Markup nhóm: dòng `<tr class="group-row">` ~dòng 428; header section A + nút "Thêm nhóm"/"Thêm mới" ~dòng 396-405.
- Màn này CHƯA có state đóng/mở nhóm → phải thêm mới `expandedGroups` + `isGroupExpanded/toggleGroupExpand/toggleAllGroups`
  (copy nguyên khuôn từ `BomBuilderTableCard.vue` vừa làm), rồi thêm `v-show` cho các tbody sản phẩm của nhóm.
- `edit.vue` là LF (không phải CRLF) → sửa bằng script ghi \n bình thường.
- Thanh toolbar hiện có kết thúc ~dòng 342; bảng bắt đầu `<div class="products-scroll">` dòng 346,
  `<thead class="bg-light sticky-head">` dòng 348, `<th>Thao tác</th>` dòng 350 → chèn nút
  Thu gọn/Mở rộng tất cả vào đúng th này (khuôn giống BOM).


### Checkpoint — 2026-08-18 (kết thúc batch)
Vừa hoàn thành: #10885 phần Báo giá (edit.vue + _id/index.vue) — thêm mới hoàn toàn state đóng/mở nhóm.
Đã verify: 12 file .vue thay đổi đều compile sạch qua vue-template-compiler.
Đã đổi trạng thái Redmine sang "Đang tiến hành" cho 8 task: 10741, 10804, 10810, 10818, 10840, 10885, 10897, 10948 (kèm ghi chú mô tả việc đã làm).
KHÔNG đụng #9752 (giữ Mới) và #10986 (giữ Pending) — user chốt bỏ 2 task này.
Bước tiếp theo: test trên môi trường dev rồi commit. CHƯA commit, CHƯA test Playwright.
Blocked: không có.


### Checkpoint — 2026-08-18 (đã test Playwright xong)
Đã test UI thật trên localhost:3000 / :8000, tài khoản namdangit@gmail.com. Kết quả: 8/8 task PASS.

**2 bug phát hiện khi test và ĐÃ SỬA:**
1. #10897 — icon "Tạo yêu cầu làm giải pháp" ban đầu chỉ gate theo `implementation_type` (2/3),
   trong khi dropdown "Dự án tiền khả thi" ở form tạo YC lọc theo `forRequestSolution` gồm 4 vế:
   type != 1, CHƯA có yêu cầu làm GP, `created_by` = user hiện tại, không phải dự án cha.
   → icon hiện cho dự án không có trong dropdown, bấm vào prefill rỗng.
   Sửa: BE `ProspectiveProjectResource` trả cờ `is_can_create_request_solution` dùng ĐÚNG 4 vế đó,
   FE chỉ đọc cờ (1 nguồn sự thật, theo CLAUDE.md). Sau sửa: chỉ còn 2 dự án hiện icon, prefill chạy đúng.
2. #10885 — Quick Add Bar ban đầu bị chèn nhầm vào nhánh `<template v-else>` (nhánh BOM KHÔNG có nhóm)
   thay vì trong `<template v-for="block in renderGroups">`. Hậu quả: `block` undefined → vỡ nguyên
   màn Sửa BOM thành trang 404. ⚠️ BẪY: `BomBuilderTableCard.vue` có 2 nhánh render (có nhóm: dòng
   190-488, không nhóm: 492-759) với đoạn đóng `</tbody></template></template>` GIỐNG HỆT nhau —
   bám anchor theo chuỗi text sẽ khớp nhầm nhánh. Phải kiểm depth `<template>` trước khi chèn.

**Đã test và PASS:**
- #10741/#10810: textarea Mô tả không có dấu *, nhập + Lưu nháp → DB lưu đúng, màn chi tiết hiện read-only.
- #10897: icon chỉ hiện đúng dự án đủ điều kiện; bấm → form tạo YC prefill đúng dự án.
- #10818: hết Nhóm ngành/Nhóm giải pháp; tiêu đề nhóm đúng nguyên văn; CascadePairSelect nạp 226 option;
  lọc "Khai thác khoáng sản" → gửi `customer_scope_group_id=1`, bảng ra 1 loại hình / 2 lĩnh vực.
- #10885 BOM: sticky ✅, Thêm nhóm ✅, Thu gọn/Mở rộng tất cả ✅, 2 Quick Add Bar đúng cấp
  ("Thêm nhóm con" chỉ ở Cấp 1) ✅, mũi tên + click tiêu đề ✅.
- #10885 Báo giá (edit + xem chi tiết): 4 nhóm/4 mũi tên/4 Quick Add ✅, thu gọn ẩn hết dòng ✅,
  nút Thêm nhóm mở đúng popup "Thêm nhóm sản phẩm" ✅.
- #10948: verify bằng tinker trong transaction rollback (markWon → 2 báo giá nguồn sang status 7).
  KHÔNG test được qua UI vì cần báo giá tổng ở trạng thái Đã duyệt.
- #10804 / #10840: rà code xác nhận đã có sẵn, không sửa gì.

**Lưu ý môi trường:** phải restart Nuxt dev bằng Node 14.21.3 (`~/.nvm/versions/node/v14.21.3/bin`),
shell mặc định là Node 12 sẽ lỗi. Đã xoá `node_modules/.cache` + `.nuxt/cache` khi nghi bundle cũ
(hoá ra không phải nguyên nhân — nguyên nhân thật là chèn nhầm nhánh v-else).
Dev server hiện đang chạy nền, log ở /tmp/nuxt-dev.log.

Bước tiếp theo: commit (chưa commit).
Blocked: không có.


### Checkpoint — 2026-08-18 (test bổ sung #10948 qua UI + quét regression)
Đã TỰ DỰNG DATA và test #10948 qua giao diện thật (trước đó mới verify ở tầng service):
- Data dùng: báo giá tổng `BGT-2026-00013` (id 227, dự án cha ND.2026.CHA id 99, main_sale=13 = user test),
  2 nguồn `BG-2026-00224` (dự án con 100) + `NOGG-BG-002` (dự án con 101). Đưa tổng về trạng thái
  Đã duyệt (4) để nút "Trúng thầu" hiện.
- **Luồng thuận**: bấm Trúng thầu → popup xác nhận → Đồng ý → tổng sang 7, CẢ 2 nguồn sang 7,
  lịch sử ghi `action=finalize 4→7` kèm `meta={summary_quotation_id:227, summary_quotation_code:...}`. ✅
- **Luồng chặn**: dựng xung đột (đặt `BG-2026-00239` cùng dự án 100 sang Trúng thầu) → bấm Trúng thầu
  → 422, toast báo đúng: "Dự án con của báo giá BG-2026-00224 đã có báo giá trúng thầu (BG-2026-00239),
  vui lòng hủy chốt trước." Transaction rollback SẠCH: tổng vẫn 4, 2 nguồn vẫn 4. ✅
- Báo giá KHÔNG thuộc bản gộp (BG-2026-00239) không bị đụng khi cascade. ✅
- Đã dọn data xung đột về trạng thái ban đầu.

**Quét regression 13 màn** (solutions list/detail/edit, prospective-projects, request-solution add,
report, bom-list list/edit/view, quotations list/edit/view, summary-quotation detail):
KHÔNG màn nào 404, KHÔNG lỗi JS runtime nào. Warning còn lại đều CÓ SẴN của project, không do batch này:
- `V2BaseBadge` variant / `V2BaseButton` type không qua validator (OrgChartTab, V2BaseDataTable)
- `receiveDeptOptions` / `employees` / `disabled` không khai (RequestTab, TktTab)
- `rows="3"` thiếu dấu `:` ở `RequestTab.vue:145,156,164` → V2BaseTextarea nhận String thay vì Number
  (textarea Mô tả tôi thêm dùng `:rows="4"` đúng kiểu)
- `computed "fields" đã định nghĩa trong data` ở ChooseErpCustomerModal (xem memory veevalidate-fields)

Trạng thái: 8/8 task đã test đầy đủ, không còn lỗi. Bước tiếp theo: commit.
