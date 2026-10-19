# HĐ đã kết xuất — cảnh báo HĐ phát sinh phụ lục sau khi kết xuất

@khoipv — Bắt đầu 15/10/2026

Spec: [docs/superpowers/specs/2026-10-15-hd-ket-xuat-canh-bao-phu-luc-design.md](../../docs/superpowers/specs/2026-10-15-hd-ket-xuat-canh-bao-phu-luc-design.md)

## Phase 0 — Brainstorming
- [x] Tìm hiểu hiện trạng 7 loại phụ lục + màn HĐ đã kết xuất
- [x] Chốt yêu cầu với user
- [x] Viết spec + design tóm tắt

## Phase 1 — BE
- [x] `RenderedContractService`: hằng 7 loại + `annexAfterRenderSubquery()` + addSelect `annexes_after_render`
- [x] `RenderedContractService`: bộ lọc `has_annex` (1 Có / 2 Không)
- [x] `RenderedContractResource`: trường `annexes_after_render` (type_label rút gọn)
- [x] php -l + test tinker (rollback)

## Phase 2 — FE
- [x] `constants.js`: `HAS_ANNEX_OPTIONS`
- [x] ~~Cột "Phụ lục phát sinh" (badge + tooltip escape)~~ — user bỏ cột (15/10/2026)
- [x] Icon cạnh Mã HĐ thay cho cột riêng
- [x] Bỏ tooltip → bấm icon mở popup `AnnexAfterRenderModal.vue` (V2BaseModal, link sang chi tiết PL)
- [x] Bộ lọc "Phụ lục phát sinh"
- [x] Excel cột "Phụ lục phát sinh"

## Phase 3 — Verify
- [x] Playwright `e2e/tests/supply/hd-ket-xuat-canh-bao-phu-luc.spec.js` (seed + dọn sạch) — 4/4 pass, kèm spec ngày KT 3/3

## Phase 4 — HĐ đã đề xuất đủ, phát sinh PL thay đổi số lượng → mở lại lập đề xuất
- [x] Rà luồng: tiến độ "Hoàn thành" (`fullyProposedContractIds`), chặn lập phiếu (`assertContractHasRemaining`),
      `prefill`, popup chọn hàng đều tính LIVE từ `contract_products.qty` hiện tại; duyệt PL SL
      (`ContractAnnexQuantityController::approve`) cộng thẳng vào `contract_products.qty` / tạo dòng hàng mới
- [x] Kiểm chứng bằng script (transaction + rollback) trên HD-194/2026 (đang Hoàn thành):
      tăng SL dòng cũ +5 → mở lại, prefill SL 5; thêm dòng hàng mới SL 7 → mở lại, prefill SL 7; rollback → Hoàn thành lại
- [x] Kết luận: KHÔNG cần sửa code — hệ thống tự mở lại khi PL tăng SL được duyệt
- [x] Playwright `e2e/tests/supply/hd-ket-xuat-mo-lai-de-xuat-khi-pl-tang-sl.spec.js` — luồng THẬT (chèn PL chờ duyệt
      + gọi API duyệt), kiểm trước/sau trên danh sách, prefill = SL tăng thêm, form lập phiếu + popup chọn hàng — pass,
      afterAll trả DB nguyên trạng (qty, versions, changes, current_version, ngày KT, thông báo, PL)
- Ghi nhận (chưa sửa, chờ user): popup chọn hàng chỉ lấy HĐ còn hiệu lực → HĐ quá ngày KT mở lại nhưng không chọn
  được hàng trong HĐ; cột "SL còn lại theo HĐ" ở form = HĐ + PL − đã xuất, không trừ phần đã đề xuất;
  `ContractAnnexQuantityController::approve()` không return response (body rỗng)

## Phase 5 — HĐ có PL phát sinh đẩy lên đầu danh sách (16/10/2026)
Luật: thứ tự mặc định = MỚI NHẤT của (ngày kết xuất, ngày duyệt PL phát sinh gần nhất) giảm dần — PL duyệt thì HĐ
nổi lên như vừa cập nhật, HĐ khác kết xuất sau đó thì nằm trên. Bấm sort theo cột thì giữ nguyên luật cột.
- [x] `RenderedContractService::getList()`: nhánh sort mặc định → `COALESCE(MAX(approved_time PL phát sinh), supply_rendered_at) DESC`
- [x] php -l + script kiểm thứ tự (rollback): PL duyệt → lên đầu; PL chờ duyệt → không đổi; HĐ kết xuất sau → nằm trên; sort cột ngày kết xuất giữ luật cũ
- [x] Playwright: thêm case thứ tự vào `hd-ket-xuat-canh-bao-phu-luc.spec.js` (5/5 pass); sửa `hd-ket-xuat-ngay-kt-phu-luc.spec.js`
      chọn HĐ chưa có PL gia hạn thật (HĐ có PL giờ nổi lên đầu) — 2/2 pass; DB sạch

## Phase 6 — Chốt các điểm còn mở (16/10/2026)
- [x] Chỉ lập đề xuất khi HĐ CÒN HIỆU LỰC (contract_end_time đã gồm gia hạn PL đã duyệt; trống = còn):
      `SupplyProposalService::isContractEffective()` + `assertContractEffective()`; áp vào cờ
      `can_create_supply_proposal` (Resource + receiveInfo), `prefill`, `store`. `update` (sửa phiếu nháp/bị trả lại) CHƯA chặn
- [x] Bỏ trường Excel "Phụ lục phát sinh" (FE `exportFields` + `exportCellValue`)
- [x] `ContractAnnexTimeService::approve()`: `$contract->end_time` (không có cột) → `contract_end_time` (Y-m-d).
      Ảnh hưởng: chỉ `contract_changes.old_value` bị NULL (bảng chỉ ghi, chưa màn nào đọc); ngày KT HĐ vẫn cập nhật đúng.
      Dữ liệu cũ: 1 dòng (PL-020/2026, HD-150/2026) old_value NULL — chưa vá
- [x] Kiểm chứng: php -l; t6.php/t7.php (rollback) — hết hạn + PL tăng SL → chặn; gia hạn đến hôm nay → mở;
      ngày KT trống → mở; store HĐ hết hạn → chặn; duyệt PL gia hạn thật → old_value đúng, mở lại.
      Playwright 3 spec HĐ kết xuất 8/8 pass (spec mở lại đề xuất đi thêm bước PL gia hạn thật); DB sạch
- [x] Chặn nhập SL đề xuất vượt SL CÒN ĐƯỢC ĐỀ XUẤT của HĐ (user duyệt 16/10/2026, chặn cả lưu nháp):
  - [x] BE `SupplyProposalService::assertNotOverContract($items, $ignoreProposalId)` — mốc = HĐ + PL − đã xuất
        − SL phiếu sống khác (quy đổi ĐVT); gọi ở `store`, `update`, `send`
  - [x] BE `goodsPool` / `contractGoodsPool` nhận `ignore_proposal_id` → dòng pool có `sl_con_de_xuat` (+ `_main`)
  - [x] BE `contractRefMap($products, $proposalId)` → `sl_con_de_xuat` cho màn sửa/xem phiếu (Detail resource)
  - [x] FE `swapBlocks.js` helper `contractRemain` / `isOverContractAt` / `overContractRows`; GoodsPickerModal +
        `buildProductRow` mang `sl_con_de_xuat`; `loadGoodsPool` gửi `ignore_proposal_id` khi sửa; GoodsTable cột
        "SL còn lại theo HĐ" hiện mốc này, bôi đỏ "Vượt SL còn được đề xuất (x)", note chặn; `validate()` chặn
        Lưu nháp / Gửi; Excel cột cùng số
  - [x] Kiểm chứng: php -l; script t8.php (rollback) 11 ca đúng; node test helper 9/9; compile-check 3 file .vue.
        Playwright CHƯA chạy (chỉ chạy khi user bảo)
- [x] `ContractAnnexQuantityController::approve()` (module Category, user đồng ý sửa 16/10/2026): thêm `return`
      kết quả transaction; 3 lỗi giữa chừng đổi `return responseJson` → `throw Exception` (rollback, trả 400).
      Kiểm chứng t9.php: adjust −100 → 400 + không ghi gì; +5 → 200 `success`; rollback sạch

## Phase 7 — Cột "Phiếu đề xuất" gọn lại (16/10/2026)
- [x] FE `contract_render/index.vue`: ô chỉ hiện tối đa 2 mã phiếu (`PROPOSAL_PREVIEW`), còn lại link "Xem thêm (+n)"
- [x] FE popup `components/ProposalListModal.vue` (V2BaseModal): STT, Mã phiếu (link xem chi tiết), Trạng thái
- [x] Compile-check 2 file .vue
- [x] Playwright `e2e/tests/supply/hd-ket-xuat-xem-them-phieu-de-xuat.spec.js` (user bảo test 16/10/2026) — DB stag không có
      HĐ đã kết xuất nào > 2 phiếu nên chặn response API trên trình duyệt (page.route), ghép 5 phiếu thật vào dòng 1,
      2 phiếu vào dòng 2, KHÔNG ghi DB. Kiểm: ô chỉ 2 mã + "Xem thêm (+3)", dòng đủ 2 phiếu không có link; popup đủ 5
      dòng + trạng thái; bấm mã phiếu → màn chi tiết nạp đúng phiếu — pass, ảnh ở `e2e/test-results/xem-them-*.png`
- [x] Popup thêm cột "Người tạo" (user yêu cầu 16/10/2026):
  - [x] BE `RenderedContractService::getList()` — `proposal_list` thêm trường thứ 4 `created_by` (chỉ id, không nối họ
        tên vì GROUP_CONCAT bị cắt ở 1024 byte); `RenderedContractResource::proposalItems()` trả `creator_name`
        ("Mã NV - Họ tên"), nạp theo lô qua `creatorNames()` (nhớ tạm trong request)
  - [x] FE `ProposalListModal.vue` cột "Người tạo" (giữa Mã phiếu và Trạng thái)
  - [x] Kiểm chứng: php -l; gọi API thật thấy `creator_name`; compile-check; Playwright spec trên thêm kiểm cột — pass

### Checkpoint — 2026-10-16 (chiều)
Vừa hoàn thành: Phase 6 — chặn SL đề xuất vượt SL còn được đề xuất của HĐ (BE + FE) + sửa approve() PL SL
Đang làm dở: —
Bước tiếp theo: user reload API + build client, test trên dev; chờ trả lời: chặn `update` khi HĐ hết hạn?
                vá old_value PL-020/2026?
Blocked:

### Checkpoint — 2026-10-16
Vừa hoàn thành: Phase 5 — HĐ có PL phát sinh đẩy lên đầu danh sách (chỉ sửa BE, FE không đổi)
Đang làm dở: —
Bước tiếp theo: user kiểm trên dev; chờ user trả lời 3 điểm ghi nhận ở Phase 4
Blocked:

### Checkpoint — 2026-10-15
Vừa hoàn thành: BE (subquery `annexes_after_render` + lọc `has_annex`), FE (icon cạnh Mã HĐ → popup danh sách PL, bộ lọc, trường Excel), test tinker 7/7 + Playwright 4/4 pass, DB sạch; Phase 4 kiểm chứng mở lại đề xuất khi có PL tăng SL — chạy đúng sẵn, không sửa code
Đang làm dở: —
Bước tiếp theo: user build client + hard refresh, test trên dev với PL thật
Blocked:
