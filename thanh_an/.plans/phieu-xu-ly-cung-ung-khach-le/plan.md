# Bảng xử lý cung ứng — loại Cung ứng khách lẻ (type 3)

Phụ trách: @khoipv
Bắt đầu: 23/09/2026
Nguồn yêu cầu: sheet Google "CUNG ỨNG KHÁCH HÀNG LẺ" (gid=40971644)

## Mục tiêu
Màn `Lập phiếu xử lý cung ứng` hiện chỉ biết 2 loại (KH hợp đồng / Nội bộ). Phiếu lập từ
đề xuất khách lẻ (type 3) đang rơi vào nhánh "KH hợp đồng" → thừa cột theo HĐ, thiếu cột giá.
Làm lại bộ cột đúng mẫu sheet cho riêng loại 3.

## Quyết định đã chốt với user
- "Đã xử lý" VẪN cộng cột "Mua hàng" (giữ hàm dùng chung `rowDaXuLy`, không tách riêng
  cho khách lẻ). Số mẫu trong sheet (5/5) coi như gõ nhầm.
- Thành tiền = Đơn giá x SL "Xuất bán", CHƯA cộng VAT.
- VAT lấy tự động từ danh mục hàng hóa (`products.tax`), chỉ đọc, snapshot vào phiếu khi lưu.
- Thành tiền KHÔNG lưu DB, luôn tính lại.

## Phase 1 — Backend
- [x] Migration thêm `supply_handling_products.don_gia` + `vat_percent`
- [x] `SupplyHandling`: TYPE_KHACH_LE = 3, thêm vào TYPES + COLS_BY_TYPE[3] = ['mua','ban']
- [x] `SupplyHandlingService::productInfoMap()` trả thêm `tax`
- [x] `SupplyHandlingController::productInfo` nhận `type`, merge `retailPriceMap` cho khách lẻ
- [x] `StoreSupplyHandlingRequest` thêm `products.*.don_gia`
- [x] `SupplyHandlingService::syncProducts()` lưu `don_gia` + snapshot `vat_percent`
- [x] `DetailSupplyHandlingResource` trả `don_gia`, `vat_percent`
- [x] Chạy migrate

## Phase 2 — Frontend
- [x] `constants.js`: TYPE.KHACH_LE, TYPE_OPTIONS, COLS_BY_TYPE[3], buildHandlingSrcCols(3), helper isRetailType/hasPriceCols
- [x] `HandlingGoodsTable.vue`: cột nguồn đọc từ productInfo, 3 cột Đơn giá / VAT / Thành tiền, dòng Tổng, nhãn "SL đặt đơn"
- [x] `add.vue`: loadProductInfo gửi unit_id + type; payload lưu don_gia; export Excel thêm cột
- [x] Build lại client (restart dev server — webpack giữ cache cũ của constants.js)

## Phase 3 — Kiểm thử
- [x] Playwright: lập phiếu xử lý từ đề xuất khách lẻ, kiểm tra cột + tính tiền + lưu/mở lại
- [x] Rà soát cấu trúc bảng đối chiếu sheet mẫu (19 cột, colspan/rowspan, dòng Tổng, file Excel xuất ra)

## Phase 4 — Chỉnh theo mẫu
- [x] Gộp nhóm "Tiền hàng" vào nhóm "Kết quả" trên bảng (HandlingGoodsTable.vue)
- [x] Gộp nhóm tương ứng khi xuất Excel (add.vue: group 'Tiền hàng' -> 'Kết quả')

## Phase 5 — Loại 6: Cung ứng khách hàng hợp đồng nguyên tắc (@khoipv)
Bảng = layout khách lẻ BỎ 2 cột giá dealer + BỎ 3 cột tiền → 14 cột.
- [x] FE constants.js: thêm TYPE.HD_NGUYEN_TAC = 6 + TYPE_OPTIONS
- [x] FE constants.js: COLS_BY_TYPE[6] = ['mua', 'ban']
- [x] FE constants.js: buildHandlingSrcCols nhánh loại 6 (SL tồn kho / SL đang mua)
- [x] BE SupplyHandling.php: TYPE_HD_NGUYEN_TAC = 6, TYPES, COLS_BY_TYPE[6]
- [x] Rà tab "Tham chiếu hợp đồng bán" cho loại 6 (HandlingSummaryTabs.vue) — đã kiểm thử hiện đúng
- [x] Kiểm thử: tạo đề xuất loại 6 trên staging rồi lập phiếu xử lý
- [x] Sửa loadGoodsPool: mọi loại bám HĐ (1/4/5/6) phải gửi customer_id (trước đó chỉ loại 1)

## Phase 6 — Tinh chỉnh tab tham chiếu HĐ (@khoipv)
- [x] Đổi tên cột "Số hợp đồng" -> "Mã hợp đồng" (HandlingSummaryTabs.vue)
- [x] Gắn link mã HĐ sang /contract/contract/:id, target _blank (theo ContractRefTab.vue của màn đề xuất)

## Checkpoint

### Checkpoint — 23/09/2026
Vừa hoàn thành: Phase 1 (BE) + Phase 2 (FE) + Phase 3 (kiểm thử Playwright) cho loại 3 — khách lẻ.
- Kiểm thử trên đề xuất DXCU-2026-0024 (id 35, type 3). Bộ cột đúng mẫu sheet:
  STT | Định danh | Hàng hóa | Số liệu nguồn (SL tồn kho / SL đang mua / Dealer không service / Dealer có service)
  | SL đặt đơn | Xử lý cung ứng (Mua hàng, Bán hàng) | Kết quả (Đã xử lý, Còn lại) | Tiền hàng (Đơn giá, VAT (%), Thành tiền) | Xóa
- Giá dealer / giá vốn quy đổi theo ĐVT dòng hàng: 2.000.000 / 4.000.000 và 1.890.000 / 2.079.000
- VAT = 5 lấy từ danh mục hàng hóa, chỉ đọc
- Tính tiền: dòng 1 bán 5 × 20.000 = 100.000; dòng 2 bán 2 × 15.000 = 30.000; Tổng 130.000
- Lưu nháp → DB lưu đúng don_gia + vat_percent (snapshot phía BE); mở lại phiếu khôi phục đầy đủ
- Đã xóa phiếu test (supply_handlings id 18) để trả DB staging về nguyên trạng

Đang làm dở: không có
Bước tiếp theo: viết design.md (tóm tắt) + docs/superpowers/specs/2026-09-23-phieu-xu-ly-cung-ung-khach-le-design.md (chi tiết),
sau đó làm tiếp loại 4/5/6 khi user yêu cầu.
Blocked:

### Checkpoint — 23/09/2026 (bổ sung)
Vừa hoàn thành: gộp nhóm cột "Tiền hàng" vào "Kết quả" theo file mẫu.
- HandlingGoodsTable.vue: bỏ <th> nhóm "Tiền hàng", resColspan = (hasPrice ? 5 : 2) + (editable ? 1 : 0); bỏ CSS .grp-money
- add.vue: 3 cột Đơn giá / VAT (%) / Thành tiền đổi group 'Tiền hàng' -> 'Kết quả'
- Kiểm tra live: nhóm "Kết quả" colspan 6 (Đã xử lý, Còn lại, Đơn giá, VAT, Thành tiền, Xóa), tổng span mọi dòng vẫn 19
- Excel xuất ra: merge nhóm đổi từ N6:O6 + P6:R6 thành N6:R6 (một nhóm "Kết quả" duy nhất)

Đang làm dở: không có
Bước tiếp theo: viết design.md (tóm tắt) + docs/superpowers/specs/2026-09-23-phieu-xu-ly-cung-ung-khach-le-design.md (chi tiết),
sau đó làm tiếp loại 4/5/6 khi user yêu cầu.
Blocked:

### Checkpoint — 23/09/2026 (loại 6 — HĐ nguyên tắc)
Vừa hoàn thành: bảng xử lý cung ứng cho loại 6 (Cung ứng khách hàng hợp đồng nguyên tắc).
- Bảng 14 cột = layout khách lẻ BỎ 2 cột giá dealer + BỎ 3 cột tiền:
  STT | Định danh (4) | Hàng hóa | Số liệu nguồn (SL tồn kho, SL đang mua) | SL đặt đơn
  | Xử lý cung ứng (Mua hàng, Bán hàng) | Kết quả (Đã xử lý, Còn lại, Xóa)
- FE constants.js: TYPE 4/5/6 + TYPE_OPTIONS, isNguyenTacType(), CONTRACT_TYPES/isContractType(),
  COLS_BY_TYPE[6] = ['mua','ban'], nhánh buildHandlingSrcCols cho loại 6
- FE add.vue: loadGoodsPool gửi customer_id cho MỌI loại bám HĐ (BE goods-pool trả rỗng nếu thiếu)
- FE HandlingSummaryTabs.vue: showContractTab dùng isContractType (vẫn chặn bằng contractRows)
- BE SupplyHandling.php: TYPE_HD_DAT_MUON/TRAO_TANG/NGUYEN_TAC, TYPES, COLS_BY_TYPE[6], isNguyenTacType()
- Kiểm thử live (đề xuất test DXCU-TEST-NT6 nhân bản từ DXCU-2026-0024): thead 14 span, tbody 14,
  tfoot 14; nhập Mua hàng 6 → Đã xử lý 6, Còn lại 4, dòng Tổng 20/6/0/6/14
- Excel xuất ra 13 cột A..M (không có cột Xóa), merges: A1:M1, B6:E6, G6:H6, J6:K6, L6:M6, A6:A7, F6:F7, I6:I7
- Tab "Tham chiếu hợp đồng bán": kiểm thử với đề xuất test gắn HĐ nguyên tắc HD-188/2026 (contracts.id 209,
  contracts.type = 5 Nguyên tắc) — tab hiện đủ Số HĐ / Thời gian ký / Thời gian KT / Cty thực hiện / SL HĐ-PL-TH-Còn lại.
  Tab chỉ hiện khi dòng hàng có in_contract = 1 và contract_id != null (đúng thiết kế).
- Đã xóa dữ liệu test (supply_proposals id 37, 38 + dòng hàng) — DB staging về nguyên trạng

Đang làm dở: không có
Bước tiếp theo: loại 4 (HĐ đặt/mượn) + loại 5 (HĐ trao tặng) khi user yêu cầu;
viết design.md (tóm tắt) + docs/superpowers/specs/2026-09-23-phieu-xu-ly-cung-ung-khach-le-design.md
Blocked:

### Checkpoint — 23/09/2026 (tab tham chiếu HĐ)
Vừa hoàn thành: tab "Tham chiếu hợp đồng bán" của màn lập phiếu xử lý.
- Cột "Số hợp đồng" -> "Mã hợp đồng"
- Mã HĐ thành nuxt-link `/contract/contract/${r.contract_id}` target _blank, class .lnk-contract
  (copy style từ pages/supply/supply_proposals/components/ContractRefTab.vue để 2 màn giống nhau)
- Không có contract_code thì hiện "—" như cũ
- Kiểm thử live với đề xuất test gắn HD-188/2026: header đúng, 2 dòng đều ra link
  href=/contract/contract/209, target=_blank, title="Xem chi tiết hợp đồng HD-188/2026"
- Đã xóa dữ liệu test (supply_proposals id 39) — DB staging về nguyên trạng

Đang làm dở: không có
Bước tiếp theo: loại 4 (HĐ đặt/mượn) + loại 5 (HĐ trao tặng) khi user yêu cầu
Blocked:

## Phase 7 — Test E2E loại 6 từ luồng phiếu đề xuất (23/09/2026)

- [x] Dựng HĐ nguyên tắc test còn hiệu lực (contracts id 223 `HD-TEST-NT/2026`, type = 5, status = 3,
      customer 3216, KT 31/12/2027) + 5 dòng contract_products
- [x] Màn đề xuất: chọn loại 6 + khách hàng -> popup chọn hàng chỉ ra hàng của HĐ nguyên tắc đúng khách
- [x] Chọn 3 mặt hàng trong HĐ, nhập SL 100 / 20 / 30 -> Tổng SL đề xuất 150
- [x] Tab "Tham chiếu hợp đồng bán" màn đề xuất: cột "Mã hợp đồng" ra link /contract/contract/223
- [x] Gửi đề xuất -> DXCU-2026-0026 (type 6, status 2) -> BGĐ duyệt -> status 3 (Chờ xử lý)
- [x] Từ inbox bấm lập phiếu xử lý -> /supply/supply_handlings/add?proposal_id=40, bảng ra đúng 14 cột
- [x] Nhập phân bổ: dòng 1 Mua 60 + Bán 40 (còn 0), dòng 2 Mua 20 (còn 0), dòng 3 Bán 10 (còn 20)
      -> footer Tổng 150 / Đã xử lý 130 / Còn lại 20, chú thích "Mua hàng: 80 · Bán hàng: 50"
- [x] Lưu phiếu -> PXL-2026-0013 (type 6), 3 dòng lưu đúng alloc_mua/alloc_ban, in_contract = 1,
      contract_id = 223, don_gia/vat_percent = 0 (loại 6 không có cột tiền)
- [x] Đề xuất gốc chuyển status 9 (Đã xử lý)
- [x] Mở lại phiếu (mode = show): bảng 13 cột (ẩn cột Xóa), số liệu giữ nguyên,
      tab "Tham chiếu hợp đồng bán" nạp lại từ HĐ gốc, mã HĐ vẫn là link
- [x] Export Excel: 13 cột A..M, merges A1:M1, B6:E6, G6:H6, J6:K6, L6:M6, A6:A7, F6:F7, I6:I7
- [x] Xóa toàn bộ dữ liệu test (contract 223 + contract_products, đề xuất 40, phiếu xử lý 19)

### Checkpoint — 23/09/2026 (E2E loại 6 từ luồng đề xuất)
Vừa hoàn thành: chạy hết luồng loại 6 từ lập đề xuất -> duyệt -> lập phiếu xử lý -> lưu -> mở lại -> export.
Không phát hiện lỗi thuộc phạm vi loại 6.

Ghi nhận 1 điểm KHÔNG phải bug (đã kiểm chứng):
- Tab tham chiếu HĐ GỘP các dòng cùng hàng hóa trong 1 HĐ và quy đổi về ĐVT chính
  (SupplyProposalService::contractRefMap + aggregateContractLines). Dữ liệu test ban đầu có 3 dòng
  cùng mã hàng HC-SH-3307 với 2 ĐVT khác nhau nên SL hợp đồng ra 150 thay vì 200; xóa 2 dòng thừa
  thì về đúng 200. Đây là logic sẵn có, không liên quan loại 6.

Ghi nhận vấn đề CHUNG (mọi loại phiếu, không riêng loại 6) — chưa sửa, chờ ý kiến:
- DetailSupplyHandlingResource trả ton_kho / dang_mua / sl_vay / sl_gui / sl_doi = 0 khi mở lại phiếu
  (đã có comment "Task sau wire; tạm 0") -> cột "Số liệu nguồn" của phiếu đã lưu luôn hiển thị 0/0 và 0.

Đang làm dở: không có
Bước tiếp theo: loại 4 (HĐ đặt/mượn) + loại 5 (HĐ trao tặng) khi user yêu cầu;
viết design.md (tóm tắt) + docs/superpowers/specs/2026-09-23-phieu-xu-ly-cung-ung-khach-le-design.md
Blocked:

## Phase 8 — Loại 5 (Cung ứng khách hàng hợp đồng trao tặng) — 23/09/2026

Chốt từ mockup user gửi: bảng loại 5 GIỐNG HỆT loại 6 (HĐ nguyên tắc) — 14 cột,
không có 2 cột giá dealer, không có 3 cột tiền; cột xử lý chỉ "Mua hàng" + "Xuất bán".

- [x] FE constants.js: gộp loại 5 + 6 vào cùng 1 nhánh cột (đổi tên isNguyenTacType)
- [x] FE constants.js: COLS_BY_TYPE[5] = ['mua', 'ban']
- [x] BE SupplyHandling.php: COLS_BY_TYPE[TYPE_HD_TRAO_TANG] + đổi tên isNguyenTacType
- [x] Kiểm thử live: bảng 14 cột, toán phân bổ, tab tham chiếu HĐ, export Excel
- [x] Xóa dữ liệu test

### Checkpoint — 23/09/2026
Vừa hoàn thành: Phase 8 — loại 5 (HĐ trao tặng) dùng chung bộ cột với loại 6.
- FE `supply_handlings/constants.js`: đổi `isNguyenTacType` → `isNoPriceContractType`
  (gồm loại 5 + 6), `COLS_BY_TYPE[5] = ['mua','ban']`, nhánh `buildHandlingSrcCols`
  trả 2 cột nguồn (SL tồn kho / SL đang mua), không có cột giá dealer & 3 cột tiền.
- BE `SupplyHandling.php`: thêm `COLS_BY_TYPE[TYPE_HD_TRAO_TANG]`, hằng
  `NO_PRICE_CONTRACT_TYPES` + `isNoPriceContractType()`.
- Kiểm thử live E2E (HĐ test id 224 `HD-TEST-TT/2026` type 3 CHO_TANG → đề xuất 41
  DXCU-2026-0026 type 5 → phiếu xử lý 20 PXL-2026-0013 type 5):
  bảng 14 cột đúng mockup; phân bổ 100→60+40, 20→20, 30→10 cho Đã xử lý 100/20/10,
  Còn lại 0/0/20, footer 150 / 130 / 20, "Mua hàng: 80 · Bán hàng: 50";
  tab "Tham chiếu hợp đồng bán" hiện 3 dòng HĐ, mã HĐ link `/contract/contract/224`;
  DB lưu `don_gia = vat_percent = 0`, `in_contract=1`, `contract_id=224`;
  đề xuất chuyển status 9; mở lại `mode=show` còn 13 cột (bỏ cột Xóa);
  Excel 13 cột A..M, merges `A1:M1, B6:E6, G6:H6, J6:K6, L6:M6, A6:A7, F6:F7, I6:I7`.
- Đã xóa sạch dữ liệu test (HĐ 224 + contract_products 6226-6228, đề xuất 41, phiếu 20).

Đang làm dở: không
Bước tiếp theo: loại 4 (HĐ đặt/mượn) khi user yêu cầu
Blocked:

## Phase 9 — Loại 4 (Cung ứng khách hàng hợp đồng đặt/mượn) — 23/09/2026

User chốt: bảng loại 4 GIỐNG loại 5 (trao tặng) — 14 cột, không cột giá dealer,
không 3 cột tiền; cột xử lý chỉ "Mua hàng" + "Xuất bán".

- [x] FE constants.js: thêm loại 4 vào NO_PRICE_CONTRACT_TYPES + COLS_BY_TYPE[4]
- [x] BE SupplyHandling.php: thêm TYPE_HD_DAT_MUON vào NO_PRICE_CONTRACT_TYPES + COLS_BY_TYPE
- [x] Kiem thu live: bang 14 cot, toan phan bo, tab tham chieu HD, export Excel
- [x] Xoa du lieu test

### Checkpoint — 23/09/2026
Vừa hoàn thành: Phase 9 — loại 4 (HĐ đặt/mượn) dùng chung bộ cột với loại 5 + 6.
- FE `supply_handlings/constants.js`: `NO_PRICE_CONTRACT_TYPES` = [4, 5, 6],
  `COLS_BY_TYPE[4] = ['mua','ban']`.
- BE `SupplyHandling.php`: `COLS_BY_TYPE[TYPE_HD_DAT_MUON]` + thêm TYPE_HD_DAT_MUON vào
  `NO_PRICE_CONTRACT_TYPES`.
- Kiểm thử live E2E (HĐ test id 225 `HD-TEST-DM/2026` type 4 DAT_MUON → đề xuất 42
  DXCU-2026-0026 type 4, duyệt BGĐ qua UI → status 3 → phiếu xử lý 21 type 4):
  goods-pool lọc đúng 3 dòng của HĐ 225; bảng 14 cột; phân bổ 100→60+40, 20→20, 30→10
  cho Đã xử lý 100/20/10, Còn lại 0/0/20, footer 150 / 130 / 20, "Mua hàng: 80 · Bán hàng: 50";
  tab tham chiếu HĐ link `/contract/contract/225`; DB `don_gia = vat_percent = 0`,
  `in_contract=1`, `contract_id=225`; đề xuất chuyển status 9;
  `mode=show` còn 13 cột; Excel 13 cột A..M, merges giống loại 5/6.
- Đã xóa sạch dữ liệu test (HĐ 225 + contract_products, đề xuất 42, phiếu 21).

Đang làm dở: không
Bước tiếp theo: còn thiếu file design.md (tóm tắt) + docs/superpowers/specs/... (chi tiết) cho feature này
Blocked:


---

## Phase 10 — Kiểm thử edge case loại 4 (23/09/2026)

- [x] Test vượt SL đặt đơn (Mua 80 + Bán 50 / SL đặt đơn 100)
- [x] Test lưu nháp → đề xuất KHÔNG chuyển sang "Đã xử lý"
- [x] Test sửa phiếu nháp (`?id=N&mode=edit`) — giữ 14 cột + prefill
- [x] Test popup chọn hàng ở chế độ sửa (nhãn "Trong HĐ ·" / "Ngoài HĐ") + xóa dòng
- [x] Test xóa phiếu → đề xuất revert về "Chờ xử lý" (status 3)
- [x] Test luồng duyệt phiếu xử lý
- [x] Xóa dữ liệu test (HĐ 226, đề xuất 43, phiếu 22 + 23 và toàn bộ dòng hàng)

### Checkpoint — 23/09/2026
Vừa hoàn thành: Phase 10 — chạy edge case trên loại 4, phát hiện 3 vấn đề (đang chờ ý kiến
vì đều nằm ở code dùng chung).

**Chạy đúng như mong đợi:**
- Lưu nháp (status 1) → đề xuất vẫn ở status 3, không nhảy "Đã xử lý".
- Xóa phiếu → `syncHandledStatus()` revert đề xuất 43 về status 3.
- `mode=edit` giữ nguyên 14 cột, prefill đúng số đã lưu.
- Popup chọn hàng ở chế độ sửa: dòng trong HĐ gắn nhãn `Trong HĐ · HD-TEST-DM2/2026`,
  hàng ngoài HĐ thêm được (VT-XN-001), xóa dòng OK.
- Gửi chính thức: phiếu 23 → status 3, đề xuất 43 → status 9.

**Vấn đề 1 — phiếu loại 3/4/5/6 gửi đi rồi KHÔNG AI DUYỆT ĐƯỢC (nặng nhất):**
`SupplyHandlingService::submitStatus()` đưa mọi loại ≠ TYPE_KHACH về `STATUS_CHO_DUYET`,
nhưng `guardApprove()` (`SupplyHandlingService.php:341`) và `can_approve` ở cả 2 resource
(`SupplyHandlingResource.php:34`, `DetailSupplyHandlingResource.php:35`) đều hard-code
`type == TYPE_NOI_BO`. → Phiếu loại 3, 4, 5, 6 kẹt ở "Chờ duyệt" vĩnh viễn, màn danh sách
không hiện nút Duyệt, màn chi tiết cũng không.

**Vấn đề 2 — xử lý vượt SL đặt đơn chỉ cảnh báo, vẫn lưu được:**
`dat_don=100`, nhập Mua 80 + Bán 50 → UI hiện "Còn lại -30" + banner
"Có 1 mặt hàng xử lý vượt SL đặt đơn." nhưng bấm Lưu vẫn lưu thành công (phiếu 22 lưu
`alloc_mua=80, alloc_ban=50`). `StoreSupplyHandlingRequest` cũng không có rule chặn
tổng phân bổ ≤ `dat_don`. Lỗi có sẵn, ảnh hưởng mọi loại phiếu.

**Vấn đề 3 — hằng số BE chưa được dùng:**
`SupplyHandling::COLS_BY_TYPE` và `isNoPriceContractType()` không được gọi ở đâu trong
runtime (chỉ `isRetailType()` dùng tại `SupplyHandlingController.php:43`). Việc chặn cột
hiện hoàn toàn nằm ở FE → API vẫn nhận `alloc_xvay`, `alloc_xgui`... cho phiếu loại 4/5/6.

Đang làm dở: không
Bước tiếp theo: chờ xác nhận có sửa 3 vấn đề trên không (đều là code dùng chung);
sau đó viết design.md + docs/superpowers/specs/...
Blocked: không
