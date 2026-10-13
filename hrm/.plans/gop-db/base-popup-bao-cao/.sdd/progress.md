# SDD ledger — plan: .plans/base-popup-bao-cao/plan.md

Workspace: `.plans/base-popup-bao-cao/.sdd/` (script `sdd-workspace` đòi git root, mà `HRM/` không
phải repo — hrm-api và hrm-client mới là 2 repo riêng).
Nhánh: `gop_db` trên `hrm-client`, làm thẳng, ĐƯỢC commit theo task, KHÔNG push (user chốt).

Ruling: workspace đặt tại `.plans/base-popup-bao-cao/.sdd/` — `sdd-workspace` không chạy được vì
plan nằm ngoài mọi git repo — cái giá nếu sai: artifact nằm cạnh plan thay vì thư mục git-ignored;
`HRM/` không phải repo nên không có nguy cơ lẫn vào commit.

## Rà xung đột trước khi chạy (pre-flight)

| Cặp / Task | Cái này sinh ra | Cái kia tiêu thụ | Kết quả |
|---|---|---|---|
| T1 → T5, T6 | `measure-popup.mjs`, `baseline.json` (11 khoá) | T5 chạy script, T6 so 11 khoá | ✅ khớp |
| T1 (tự nó) | script `.mjs` | — | ❌ **LỖI**: còn dòng `require('fs');` thừa trong file ESM → `ReferenceError` ngay khi chạy |
| T2 → T3 | slot `header`, prop `noEnforceFocus` | T3 dùng slot `header` | ❌ **LỖI**: T3 KHÔNG truyền `no-enforce-focus` xuống `V2BaseModal` → prop thêm ra mà không ai dùng, ca e2e 8 (select2 trong popup) vẫn hỏng |
| T3 → T5 | props/events của `V2BaseReportModal` | T5 bind 14 prop + 4 event | ✅ khớp từng tên |
| T4 → T5 | `sortedRows`/`pagedRows`/`safePage`/`pageOffset`/`toggleSort`/`onPageChange`/`onPageSizeChange`/`resetFilters` | T5 bind trong template | ⚠️ **XUNG ĐỘT**: `DemandListModal` đang có `resetFilters()` riêng → component đè mixin, hook `onFilterChange()` của mixin không bao giờ chạy |
| T4 (tự nó) | mixin đòi `rows`, `columns`, `emptyFilters()`, `onFilterChange()` | T5 có đủ 4 thứ | ✅ khớp |
| T3 → T6 | lớp CSS của VỎ đổi sang `report-drill-*`; lớp RIÊNG của màn giữ `care-drill-*` | T6 đổi **toàn bộ** 106 chỗ `care-drill` → `report-drill` | ❌ **LỖI**: selector của các lớp ở lại màn (`filters`, `sum`, `customer`, `meeting`, `back`, `sub`) sẽ trỏ vào lớp không tồn tại |
| T5 → T6 | popup đã chuyển | so baseline | ✅ |
| T6 → T7 | spec đã đổi selector | chạy 29 ca | ✅ |
| T2, T5, T6, T7 (tự nó) | — | — | ✅ nội dung tự nhất quán |

## Rulings trước khi chạy

- Ruling: bỏ dòng `require('fs');` trong `measure-popup.mjs` (T1), chỉ giữ `await import('fs')` —
  file `.mjs` không có `require` — cái giá nếu sai: script đổ ngay bước đầu, phát hiện tức thì.
- Ruling: T3 phải truyền `no-enforce-focus` xuống `V2BaseModal` — nếu không thì prop thêm ở T2
  thành vô dụng và dropdown select2 trong popup đóng ngay khi mở — cái giá nếu sai: ca e2e 8 đỏ,
  người dùng không lọc được trong popup.
- Ruling: T5 XOÁ `resetFilters()` riêng của `DemandListModal`, dùng bản của mixin (bản mixin gọi
  `onFilterChange()` nên giữ được nếp "xoá lọc là tải lại từ server") — cái giá nếu sai: bấm
  "Xoá lọc" xoá ô lọc trên màn mà không tải lại dữ liệu.
- Ruling: đổi **toàn bộ** tiền tố `care-drill-*` → `report-drill-*` ở CẢ vỏ lẫn phần ở lại màn,
  không chỉ riêng lớp của Base — có vậy phép đổi selector hàng loạt ở T6 mới đúng — cái giá nếu
  sai: 106 selector e2e trỏ vào lớp không tồn tại, cả bộ test đỏ.

## Nhật ký chạy

BASE (trước Task 1): `dc57d23b1` — hrm-client @ gop_db
Task 1: đã dispatch (sonnet) — chụp baseline hành vi popup.
Task 1: DONE_WITH_CONCERNS (commit 0391b97 ở repo `hrm-claude-config`, KHÔNG push).
Task 1: Ruling: GIỮ commit 0391b97 dù nó nằm ở repo `hrm-claude-config@main` (ngoài phạm vi
  "được commit" mà user chốt cho hrm-client) — `.plans` là symlink sang repo chuyên chứa tài liệu
  plan, commit chỉ thêm 2 file tài liệu và chưa push; viết lại lịch sử nhánh main dùng chung rủi ro
  hơn là để yên — cái giá nếu sai: user phải tự gỡ 1 commit tài liệu khỏi repo config.
Task 1: Ruling: từ Task 2 trở đi CHỈ commit trong `hrm-client`; artifact trong `.plans` để nguyên
  trong working tree, báo user cuối đợt — cái giá nếu sai: tài liệu không được version hoá ngay.
Task 1: fix round 1/5 — finding: `sortDateAsc` = null vì nhãn cột thật là "Meeting thu thập nhu
  cầu" (DemandListModal.vue:364), brief ghi sai "Ngày meeting" -> phép kiểm sort-ngày ở Task 6 vô
  nghĩa. Đã gửi implementer sửa nhãn + chụp lại baseline.
Task 1: deferred (minor): baseline đo trên dữ liệu DB sống — dữ liệu đổi giữa T1 và T6 có thể gây
  lệch giả. Giảm thiểu: T6 chạy ngay sau T5.
Task 1: deferred (minor): heightFull(900) chỉ hơn heightNormal(844) 56px do viewport 1440x900 —
  mọi lần đo lại phải giữ đúng viewport này.
Task 1: fix round 1/5 — ĐÃ XỬ LÝ (sortDateAsc có 20 giá trị, tăng dần theo ngày họp).
Task 1: fix round 2/5 — finding: `sortTextAsc` chụp THỨ TỰ MẶC ĐỊNH chứ không phải kết quả sắp
  xếp, vì cột "Khách hàng" (DemandListModal.vue:355) không khai `sortable: true`. Đổi sang cột
  "Thị trường / Phường xã" (có `sortFields` — nhánh ghép nhiều trường, dễ vỡ nhất khi chuyển sang
  mixin) + thêm chốt: `sortBy()` ném lỗi nếu ô tiêu đề không có phần tử bấm-sắp-xếp.
Task 1: fix round 2/5 — ĐÃ XỬ LÝ. `sortTextAsc` giờ đúng thứ tự tiếng Việt (Cầu Giấy < Đại Mỗ <
  Đông Ngạc < Giảng Võ < Hà Đông < Hoàng Liệt). 3 "cặp nghịch" lệnh kiểm in ra đều là giả do
  Python so codepoint (ạ/ô, đ/g, à/o), không phải luật localeCompare(…,'vi').
Task 1: Ruling: KHÔNG dispatch task reviewer riêng cho Task 1 — sản phẩm của nó là script đo +
  JSON trong `.plans/`, không phải mã chạy thật, và tôi đã tự rà trực tiếp (tìm ra 2 lỗi thật:
  nhãn cột ngày sai, cột chữ không sắp xếp được) — cái giá nếu sai: một script scratch không qua
  mắt thứ hai; Task 6 sẽ dùng chính nó nên lỗi còn sót sẽ lộ ngay ở đó.
Task 1: complete (baseline 13 cột / 20 dòng / "Hiển thị 1–20 / 126 nhu cầu", sort chữ + sort ngày
  đều có dữ liệu thật, bảng đáy 713 < đỉnh nút 803, cao 844 -> 900; commit 0391b97 ở
  hrm-claude-config + 2 file sửa vòng 1-2 còn trong working tree).
BASE cho Task 2: dc57d23b1 (hrm-client @ gop_db)
Task 2: đã dispatch (sonnet) — slot `header` + prop `noEnforceFocus` cho V2BaseModal.
Task 2: implementer DONE (commit 7faef7daf; +9/-0 dòng; popup cũ kiểm DOM ra
  {coIcon, coTieuDe, coNutDong} đều true, headerChildCount=2).
Task 2: đã dispatch task reviewer (sonnet) trên gói diff dc57d23b1..7faef7daf.
Task 2: review clean (Spec ✅, quality Approved).
Task 2: minor (deferred): comment prop `noEnforceFocus` dùng /* */ thay vì /** */ như các prop
  khác cùng khối — do brief gợi ý đúng dạng đó (plan-mandated), không chặn merge.
Task 2: complete (commits dc57d23b1..7faef7daf, review clean)
BASE cho Task 3: 7faef7daf
Task 3: đã dispatch (sonnet) — V2BaseReportModal (vỏ banner + bảng schema + phân trang).
Task 3: implementer DONE_WITH_CONCERNS (commit eb7b3a7b2, chỉ 1 file mới).
Task 3: Ruling: KHÔNG xoá trắng `.report-drill-wrap` như một đoạn CSS chết — nó mang viền
  1px #e3e8ef + bo góc 6px + thanh cuộn mảnh của khung bảng. Thay vào đó truyền
  `body-class="report-drill-wrap"` cho `V2BaseTableScroll` (component có sẵn prop `bodyClass`) để
  CSS áp đúng vùng cuộn thật; chỉ xoá `.report-drill-topscroll` (thanh cuộn trên do
  V2BaseTableScroll tự render với class riêng) — cái giá nếu sai: popup mất viền/bo góc mà phép
  đối chiếu baseline ở Task 6 (chỉ so toạ độ + số dòng) KHÔNG bắt được.
Task 3: fix round 1/5 — đã gửi implementer kèm phép đo bắt buộc (border-top-width=1px,
  border-radius=6px trên phần tử mang class `report-drill-wrap`).
Task 3: deferred (minor): implementer không xem được popup bằng mắt vì tôi quên đưa
  /tmp/care-state.json trong lệnh dispatch (nó thử đăng nhập và dính 422). Đã bổ sung ở vòng sửa.
Task 3: fix round 1/5 — ĐÃ XỬ LÝ (commit 127285043). Đo: border-top-width 0px -> 1px,
  border-radius 0px -> 6px. Implementer tìm ra nguyên nhân sâu hơn ruling của tôi: CSS `scoped`
  KHÔNG với tới phần tử nằm trong template của `V2BaseTableScroll`, nên phải dời khối
  `.report-drill-wrap` sang `<style>` không scoped, chứ chỉ truyền `body-class` là chưa đủ.
Task 3: đã dispatch task reviewer (sonnet) trên gói 7faef7daf..127285043 (2 commit).
Task 3: review vòng 1 -> Spec ❌ + Needs fixes. Critical: `.report-drill-content` chết 100% vì
  `V2BaseModal.vue:20` hard-code `content-class="shadow"` và không có prop thay thế -> mất chặn
  chiều cao 92vh + `.modal-header` giữ padding/viền mặc định Bootstrap bao quanh dải banner.
  Important: `.report-drill-scroll` chết tương tự (V2BaseTableScroll chỉ có prop `bodyClass`).
Task 3: Ruling: sửa trong phạm vi Task 3 bằng selector hậu duệ bám `.report-drill-dialog`
  (class này đã được áp qua prop `dialogClass` có sẵn), KHÔNG thêm prop `contentClass` vào
  `V2BaseModal` — tránh đụng lần nữa vào component của 30 màn cho một nhu cầu của riêng popup báo
  cáo — cái giá nếu sai: nếu sau này popup báo cáo cần style phần tử `.modal-content` mà không
  nằm dưới `.report-drill-dialog` thì phải quay lại thêm prop.
Task 3: fix round 2/5 — đã gửi implementer kèm 4 phép đo bắt buộc + yêu cầu lập bảng đối chiếu
  "class khai trong style" vs "class thật có trong template" để không còn sót CSS chết.
Task 3: fix round 2/5 — implementer xong (commit 4ccaf4c34). Đo: .modal-content height=828px
  (=92% của 900) overflow=hidden; .modal-header padding-top=0px border-bottom-width=0px;
  .report-drill-scroll tồn tại, display=flex; đáy bảng 564.79 <= đỉnh nút 650.79 (không chồng).
  Tự tìm thêm lớp chết thứ ba `.report-drill-footer` và bọc lại.
Task 3: đã dispatch scoped re-review (sonnet) trên diff 127285043..4ccaf4c34, soi thêm rủi ro
  footer bọc 2 lớp (padding/sticky chồng nhau) và rủi ro đổi giá trị CSS khi đổi selector.
Task 3: fix round 2/5 — re-review: 2 finding cũ đều ADDRESSED; PHÁT SINH MỚI (Important): bọc
  `div.report-drill-footer` làm nút không còn là con trực tiếp của `.modal-footer` -> mất
  `margin: .25rem` Bootstrap cấp, hàng nút dính sát nhau.
Task 3: Ruling: BỎ HẲN wrapper footer + xoá rule `.report-drill-footer`, thay vì đắp
  `display:flex; gap:8px` để bù — 2 popup báo cáo khác đã dựng trên V2BaseModal đều đặt nút thẳng
  vào slot `#footer`, và margin .25rem của Bootstrap cho ra đúng 8px, khớp `gap: 8px` bản gốc —
  cái giá nếu sai: khoảng cách nút lệch vài px so với bản gốc, Task 5/6 sẽ lộ.
Task 3: fix round 3/5 — đã gửi implementer kèm 3 phép đo (khoảng cách ngang thật giữa 2 nút,
  số con trực tiếp của .modal-footer, và lại wrapBottom <= footerTop).
Task 3: fix round 3/5 — implementer xong (commit b41b207cc). Đo: khoảng cách 2 nút = 8px (đúng
  bằng gap bản gốc), .modal-footer có đúng 2 con trực tiếp là 2 nút, wrapBottom 550.87 <=
  footerTop 636.87. Đã dispatch scoped re-review (haiku, diff nhỏ).
Task 3: fix round 3/5 — ADDRESSED (re-review sạch, 1 file, không phát sinh mới).
Task 3: complete (commits 7faef7daf..b41b207cc, 4 commit, 3 vòng sửa, review clean)
BASE cho Task 4: b41b207cc
Task 4: đã dispatch (haiku — brief có sẵn toàn bộ code, chủ yếu là chép + kiểm biên dịch).
Task 4: implementer DONE (commit 220e24444, 1 file mới, dev server 200, không Failed to compile).
Task 4: đã dispatch task reviewer (sonnet) trên gói b41b207cc..220e24444, soi 6 điểm: chép đúng
  brief, ô trống xuống cuối ở CẢ 2 chiều, dateSortKey đọc dd/mm/yyyy trước new Date, mixin không
  tự lọc, đủ hợp đồng tên cho Task 5, không thêm fallback che lỗi cho emptyFilters().
Task 4: review clean (Spec ✅, Approved; chép khớp từng ký tự, 6 điểm rủi ro đều đúng).
Task 4: minor (deferred): chưa có unit test cho sortedRows/dateSortKey — repo FE không có
  framework test đơn vị, brief cũng chỉ yêu cầu kiểm biên dịch. Không chặn merge.
Task 4: complete (commits b41b207cc..220e24444, review clean)
BASE cho Task 5: 220e24444
Task 5: Ruling: bước "kiểm index.vue không đổi" trong plan dùng `git diff --numstat` là SAI trong
  hoàn cảnh này — chính file đó đang có thay đổi chưa commit của việc khác (bộ lọc chuẩn mới), nên
  diff không bao giờ rỗng. Thay bằng so MD5 trước/sau: giá trị chốt = 3ee332b47108445a757211849a1388db
  — cái giá nếu sai: không phát hiện được nếu implementer lỡ sửa màn cha.
Task 5: đã dispatch (sonnet) — chuyển DemandListModal sang Base + mixin.
Task 5: implementer DONE (commit 74298de2e, DemandListModal 1307 -> 849 dòng). So baseline:
  9/11 khoá khớp tuyệt đối; lệch tableBottom -4px, footerTop -16px.
Task 5: implementer tự tìm và sửa 3 BUG THẬT ngoài file được giao, tôi đã kiểm và commit riêng
  (f73f569b8): (a) .v2-modal-body + .v2-table-scroll đều display:block -> đứt chuỗi flex, bảng
  không cuộn trong khung mà tràn (đáy y=1366 / popup cao 828px), cuộn thì bộ lọc trôi theo;
  (b) thiếu class modal-dialog-centered (V2BaseModal không có prop `centered`) -> lệch 16px;
  (c) dateSortKey() rớt giờ:phút -> cùng ngày khác giờ xếp lẫn lộn.
Task 5: Ruling: CHẤP NHẬN lệch tableBottom -4px / footerTop -16px — đó là hệ quả cố ý của việc
  bỏ khung footer riêng để dùng `.modal-footer` chuẩn của V2BaseModal (chính mục tiêu của đợt
  này); bất biến quan trọng vẫn giữ: đáy bảng < đỉnh hàng nút, không chồng lấn — cái giá nếu sai:
  hàng nút nằm cao hơn bản cũ 16px, khác biệt thị giác nhỏ, không ảnh hưởng thao tác.
Task 5: đã dispatch task reviewer trên gói 220e24444..f73f569b8 (2 commit).
Task 5: review vòng 1 -> Spec ❌ + Needs fixes.
  Critical: còn `id-prefix="care-drill"` (DemandListModal.vue:120) -> KpiBoxes sinh id DOM
    `care-drill-kpis-title-info`, Task 6 đổi selector theo tiền tố sẽ không trỏ tới.
  Important: MẤT hành vi "lật trang thì cuộn bảng về đầu" (bản gốc có
    `this.$refs.bodyScroll.scrollTop = 0` trong onPageChange) — rơi rụng lặng lẽ, không thuộc giỏ
    "đã chuyển đi" lẫn giỏ "cố ý bỏ".
  Minor: report ghi 2 file là "CHƯA COMMIT" trong khi tôi đã commit (f73f569b8) -> sửa report.
Task 5: Ruling: khôi phục cuộn-về-đầu ở VỎ (V2BaseReportModal, qua ref tới V2BaseTableScroll),
  KHÔNG ở mixin — vùng cuộn thuộc về vỏ, mixin không được biết DOM — cái giá nếu sai: popup nào
  dùng mixin mà không dùng vỏ sẽ phải tự lo, nhưng hiện chưa có popup nào như vậy.
Task 5: fix round 1/5 — đã gửi implementer kèm phép đo bắt buộc (scrollTop trước/sau khi lật trang).
Task 5: fix round 1/5 — implementer xong (commit 00877f63f). grep `care-drill` rỗng; scrollTop
  300 -> 0 khi lật trang (trang mới 21-40/126, STT đầu 21); so baseline vẫn 9/11 khớp, 2 khoá
  lệch y hệt (tableBottom 709 vs 713, footerTop 787 vs 803), không phát sinh lệch mới.
Task 5: parked — index.vue bắn 2 request `demand-list` TRÙNG mỗi lần mở popup (bug có sẵn, không
  do đợt này). Kết hợp watcher `rows() { page = 1 }` của mixin, nếu người dùng lật trang đúng lúc
  response thứ hai về thì trang bị âm thầm kéo về 1. Ruling: KHÔNG sửa trong đợt này — gốc nằm ở
  `index.vue`, file đang có thay đổi chưa commit của việc khác, sửa kèm là trộn hai việc; ghi lại
  để mở task riêng — cái giá nếu sai: người dùng thỉnh thoảng bị nhảy về trang 1 khi lật trang
  ngay lúc vừa mở popup.
Task 5: đã dispatch scoped re-review (haiku) trên diff f73f569b8..00877f63f.
Task 5: fix round 1/5 — ADDRESSED (re-review sạch: grep rỗng, cuộn-về-đầu đặt đúng ở vỏ cho cả
  page-change lẫn page-size-change, không đụng file cấm, hợp đồng props/events không đổi).
Task 5: complete (commits 220e24444..00877f63f, 3 commit, 1 vòng sửa, review clean;
  DemandListModal 1307 -> 849 dòng)
Ruling: CHUYỂN thư mục tài liệu `.plans/base-popup-bao-cao/` -> `.plans/gop-db/base-popup-bao-cao/`
  — CLAUDE.md của HRM quy định nhánh `gop_db` (đang đứng) thì tài liệu feature phải nằm dưới
  `.plans/gop-db/`; tôi đặt sai từ đầu vì chưa đọc rule đó — cái giá nếu sai: đường dẫn trong các
  brief/report đã phát đi trỏ sai chỗ, nên chuyển NGAY lúc không có subagent nào đang chạy.
BASE cho Task 6: 00877f63f
Task 6: implementer xong lượt 1 — so baseline: 9/11 khớp, đúng 2 khoá lệch đã chấp nhận
  (tableBottom 713->709, footerTop 803->787), KHÔNG có khoá thứ ba, bất biến 709<=787 giữ nguyên.
  Đổi 110 chỗ care-drill -> report-drill (brief ước 106); spec vẫn 29 ca.
  `HRM/e2e` KHÔNG phải git repo -> không commit được, file đã lưu trực tiếp.
Task 6: phép kiểm BỔ SUNG (không có trong plan) phát hiện 4 nhóm selector trỏ vào lớp đã bị gỡ:
  .report-drill-content (4 dòng), .report-drill-footer (2), .report-drill-topscroll (2),
  .report-drill-scroll-top (chưa từng tồn tại).
Task 6: Ruling: ánh xạ content->.modal-content, footer->.modal-footer,
  topscroll->.v2-table-scroll__top, bỏ hẳn vế .report-drill-scroll-top; và SỬA TRONG TASK 6, không
  đẩy sang Task 7 (Task 7 chỉ chạy test) — cái giá nếu sai: 8 dòng spec trỏ vào lớp không tồn tại,
  cả bộ 29 ca đỏ mà nguyên nhân bị che bởi vật cản môi trường.
Task 6: fix round 1/5 — đã gửi implementer kèm bảng ánh xạ + yêu cầu danh sách "không tìm thấy
  nơi định nghĩa" phải RỖNG.
Task 6: fix round 1/5 — ADDRESSED. Danh sách selector không tìm thấy nơi định nghĩa nay RỖNG;
  grep care-drill = 0; spec vẫn 29 ca. Implementer scope thêm `.report-drill-dialog` cho 2 lớp
  Bootstrap chung để tránh vỡ strict-mode khi popup xem-trước-in mở đè — tốt hơn ruling của tôi.
Task 6: tôi tự đối chiếu độc lập: 7 chỗ dùng selector mới trong spec; các lớp report-drill-dialog
  (11), -wrap (12), -table (11), -sort (2), -head (18) đều có thật trong mã nguồn.
Task 6: minor (deferred): 2 biến `barOnOpen`/`barAfter` (spec dòng 1049/1056) được tính nhưng
  không có expect() nào dùng — code chết có sẵn từ trước đợt này.
Task 6: complete (không commit được — `HRM/e2e` không phải git repo; file spec đã lưu trực tiếp)
Task 7: Ruling: KHÔNG sửa `e2e_provision.php`, KHÔNG tạo/sửa tài khoản trong DB dùng chung —
  người dùng đã được hỏi đúng chuyện này ở đợt trước và chọn không đụng; thay vào đó Task 7 chạy
  một lượt tự kiểm Playwright 8 luồng trên trình duyệt thật, đo bằng số — cái giá nếu sai: không
  có dòng "29 passed" làm bằng chứng, phải dựa vào 8 luồng đo tay.
Task 7: đã dispatch (sonnet).
Task 7: complete. Phần A: vật cản đúng như đã biết (hrm_employees không tồn tại), không sửa gì.
  Phần B: --list ra 29 ca; chạy thật đổ ở beforeAll vì thiếu tài khoản e2e (1 failed + 28 did not
  run) — KHÔNG phải hồi quy. Phần C: 8/8 luồng ĐẠT, đo bằng số DOM (popup khớp 126 dòng nền; sắp
  xếp 2 cột đổi thứ tự; lật trang STT 21 + scrollTop 0; 100 dòng/trang; lọc/xoá lọc bắn đúng
  request; phóng to 1400x844 -> 1440x900 rồi về đúng cũ; mở lượt mới không mang trạng thái cũ;
  wrap.bottom 709 <= footer.top 787, border-top 1px).
Tất cả 7 task hoàn thành. Chuyển sang rà soát toàn nhánh.

## Rà soát toàn nhánh (opus) — kết quả

Sạch ở 2 chỗ rủi ro nhất, ĐO BẰNG SỐ chứ không suy luận: (a) 30 popup dùng `V2BaseModal` không
đổi hành vi (không consumer nào truyền slot `header`; `noEnforceFocus` default trùng default của
BootstrapVue; đo popup khác trên cùng trang có nạp 33 rule report-drill-* vẫn nguyên header chuẩn);
(b) CSS không rò — mọi rule đụng lớp dùng chung đều neo dưới `.report-drill-dialog`/`.report-drill-scroll`.

Ruling: Finding 4 (thanh phân trang biến mất khi 0 dòng) KHÔNG phải hồi quy — `V2BasePagination`
tự ẩn bằng `v-if="totalRows > 0"` (dòng 2), nên bản gốc `v-if="!loading"` cho ra CÙNG kết quả.
Khép lại, không cần hỏi user — cái giá nếu sai: không có, đã đọc thẳng mã component.

Ruling: LẬT NGƯỢC nhãn "parked" của Task 5. Việc bắn 2 request `demand-list` KHÔNG phải bug có
sẵn ở `index.vue` mà là HỒI QUY do chính ruling Task 5 của tôi ("xoá resetFilters riêng, dùng bản
mixin") — bản gốc tách 2 vai: `resetFilters()` dọn state im lặng, `clearFilters()` mới emit; gộp
lại làm watcher `drillKey` bắn thêm 1 request. Reviewer đo được 2 request cùng mốc ms khi đổi drill
key, 1 request khi không đổi — cái giá nếu sai: gấp đôi tải cho query nặng nhất của màn, và lật
trang trong khoảng giữa 2 response bị kéo về trang 1 im lặng.

Vụ rơi rụng thứ BA và thứ TƯ (baseline 11 khoá không bắt được vì chỉ đo toạ độ/số dòng):
- cột tiền mất căn phải/in đậm/tabular-nums vì rule khai trong `<style scoped>` mà `<td>` do VỎ
  render (đo: textAlign left, fontWeight 400);
- `toggleSort()` thiếu `page = 1` (đo: đang trang 3, bấm sort vẫn 41-60).
=> Hợp đồng `cellClass` phải ghi rõ: style cho class truyền vào vỏ BẮT BUỘC khai KHÔNG scoped.
   Điều này ảnh hưởng thẳng Phase 2 (cả 2 popup đều dùng cellClass/align).

Đã dispatch MỘT lượt sửa gộp (6 mục) kèm 3 phép đo mới mà bộ đo cũ bỏ lọt.
Lượt sửa gộp sau rà cuối: xong (commit 26d17c2c2, 6 file). Đo: (1) mở popup đổi drill key =
  1 request demand-list (trước là 2), bấm "Xoá lọc" vẫn 1 request; (2) ô tiền textAlign right /
  fontWeight 700 / tabular-nums; (3) trang 3 -> bấm sort -> "Hiển thị 1-20 / 126"; kèm scrollTop
  200 -> 0. So baseline: vẫn 9/11, đúng 2 khoá lệch đã biết, không có khoá thứ ba.
Đã dispatch scoped re-review cho lượt sửa (00877f63f..26d17c2c2).
Rà lượt sửa gộp: 5/6 ADDRESSED; Finding 1 NOT ADDRESSED — nhánh `keepView` của watcher `drillKey`
  vẫn gọi bản có hook (đường bấm số trong hộp KPI + nút "Quay lại"). Ruling: SỬA NỐT (1 dòng) thay
  vì park — cùng một lỗi Critical, Phase 2 sẽ nhân ra 2 popup nữa dùng chung mixin này — cái giá
  nếu sai: bàn giao kèm lỗi gọi API 2 lần mà chính tôi gây ra.
Finding 1: ĐÃ XỬ LÝ HẲN (commit b85478388). Đếm request cả 4 đường đều = 1: KPI drill (keepView),
  "Quay lại" (keepView), đổi chỉ tiêu (không keepView), "Xoá lọc". Chỉ còn đúng nút "Xoá lọc" gọi
  bản có hook.

## Phase 2 — Task 8
Task 8: baseline TKT XONG (baseline-tkt.json: 11 cột / 20 dòng / "Hiển thị 1-20 / 50 dự án";
  cột sắp xếp: chữ = "Nhân viên phụ trách", ngày = "Ngày lập dự án").
Task 8: baseline CMD BỊ CHẶN — 3 quyền của báo cáo (id 1187-1189) gán cho 0 role, không tài khoản
  nào mở được popup. Subagent TỪ CHỐI bịa baseline rỗng (đúng: sortTextAsc rỗng chính là dấu hiệu
  "bấm nhầm cột không sortable").
Ruling (ĐÃ HỎI USER, user chọn): gán quyền 1187 cho role 100002 (Super Admin), company_id=1 trên
  DB local. Dòng đã chèn: role_has_permissions(permission_id=1187, role_id=100002, company_id=1).
  Gỡ lại bằng: DELETE FROM hrm_erp.role_has_permissions WHERE permission_id=1187 AND role_id=100002
  AND company_id=1; — cái giá nếu sai: 1 role trên DB local có thêm quyền xem 1 báo cáo.
SỬA RULING gán quyền: dòng đầu tôi chèn SAI role. Hàm `isCurrentEmployeeHasPermission()` đọc roles
  qua `Modules\Timesheet\Entities\Employee`, employee 13 thực tế mang role **18** (không phải
  100002 như bảng `employee_has_roles` gợi ý). Subagent phát hiện và DỪNG LẠI thay vì chạy tiếp.
  Đã gỡ dòng sai, chèn đúng theo khuôn dòng đang làm popup TKT chạy được:
    XOÁ: role_has_permissions(1187, 100002, 1)
    CHÈN: role_has_permissions(1187, 18, 1)   [đối chiếu: (1190, 18, 1) có sẵn -> TKT chạy được]
  Gỡ lại toàn bộ: DELETE FROM hrm_erp.role_has_permissions WHERE permission_id=1187 AND role_id=18
  AND company_id=1;
Task 8: complete. baseline-cmd.json (12 cột / 20 dòng / "Hiển thị 1-20 / 598 meeting"; sort chữ =
  "Phòng ban", sort ngày = "Ngày họp"); baseline-tkt.json (11 cột / 20 dòng / "Hiển thị 1-20 /
  50 dự án"; sort chữ = "Nhân viên phụ trách", sort ngày = "Ngày lập dự án"). Script đã tham số
  hoá + 3 phép đo mới, kiểm hồi quy lại popup cũ: khớp baseline.json từng khoá.
  Sau khi gán đúng role 18, permission_level nhảy sang "all_company" ngay trên token cũ.
BASE cho Task 9: b85478388
Task 9: đã dispatch (sonnet) — chuyển DevelopmentDrillModal.
Task 9: implementer xong (1204 -> 1053 dòng), tôi tự commit vì subagent bám rule "không commit khi
  chưa được yêu cầu" của CLAUDE.md (tôi quên nhắc lại quyền commit user đã cấp) -> commit 81bdddd18.
Task 9: tôi tự đối chiếu 7 khoá lệch: heightFull (không có -> 900, popup NAY CÓ nút phóng to),
  heightNormal 752->844 (bằng popup thứ nhất), modalContentOverflow visible->hidden (có chặn chiều
  cao), viền khung bảng 0px->1px/6px, tableBottom 633->645, footerTop 719->787. Bất biến giữ:
  645 <= 787. Tất cả đúng hướng "đổi mặt" mà user đã chốt trước khi làm.
Task 9: đã dispatch task reviewer trên gói b85478388..81bdddd18.
Task 9: review clean (Spec ✅, Approved, không Critical/Important). Reviewer xác nhận cả 4 lớp lỗi
  của popup thứ nhất đều KHÔNG tái diễn; người làm phân biệt đúng class-do-vỏ-sở-hữu (scoped ở vỏ
  là đúng) với class-do-popup-sở-hữu (phải không-scoped). Tiện tay sửa 1 bug có sẵn: exportExcel()
  nay dựng từ sortedRows thay vì filteredRows -> file xuất khớp thứ tự đang xem.
Task 9: minor (deferred, chuyển sang Task 11): (a) `modal-id="cmd-drill-modal"` vẫn mang tiền tố cũ
  (là id phần tử, không phải selector CSS; DemandListModal cũng giữ `care-demand-list-modal`);
  (b) 2 literal 'cmd-center'/'cmd-money' còn trong `columns()` — CỐ Ý, vì đó là nguồn dùng chung
  cho bản in + Excel, đã map qua CELL_CLASS_MAP. Task 11 grep 'cmd-' sẽ thấy 2 chỗ này, ĐỪNG tưởng
  là đổi sót.
Task 9: complete (commit b85478388..81bdddd18, review clean)
BASE cho Task 10: 81bdddd18
Task 10: đã dispatch (sonnet) — chuyển ProjectListModal (server-side, CHỈ vỏ, không mixin).
Task 10: implementer DONE (commit 01a6fbb28, 888 -> 848 dòng). So baseline-tkt: cols /
  firstPageRowCount / STT / pageTotal / footerButtonGaps / sortTextAsc / sortDateAsc KHỚP; các
  khoá "đổi mặt" lệch đúng hướng; bất biến 642 <= 787 giữ. Đo thêm: 1 request khi mở, 1 khi lật
  trang, 1 khi sắp xếp; sắp xếp ở trang 2 -> về trang 1; căn lề ô đúng.
Task 10: implementer tự bắt 1 lỗi cùng họ với ca e2e 17 của popup 1: `fetchList()` không xoá
  `rows` trước khi tải lại -> popup giữ dữ liệu CŨ trong lúc chờ, "Đang tải…" không bao giờ hiện.
  Đã sửa và đo lại.
Task 10: đã dispatch task reviewer; Task 11 (e2e) chạy song song vì đụng thư mục khác (HRM/e2e).
Task 10: review clean (Spec ✅, Approved, không Critical/Important). Xác nhận: không gắn mixin,
  cellClass khai đúng chỗ (phân biệt ai render phần tử), mỗi thao tác đúng 1 lần fetchList(),
  bản sửa `rows = []` không có tác dụng phụ (total/columns/filters không bị xoá kèm).
Task 10: minor (deferred): 3 popup đều MẤT icon tròn header + nhãn tiền tố "Thuộc:" khi chuyển
  sang vỏ banner (nội dung vẫn còn trong dòng meta). Là hệ quả kế thừa của vỏ dùng chung, nằm
  trong phần "đổi mặt" user đã đồng ý, nhưng chưa từng được gọi tên cụ thể -> đã báo user.
Task 10: complete (commit 81bdddd18..01a6fbb28, review clean)
Task 11: complete. customer-market-development.spec.ts: 19 chỗ `cmd-drill` + PHÁT HIỆN THÊM 9 chỗ
  không chứa chuỗi `cmd-drill` nhưng vẫn trỏ lớp đã đổi tên (.cmd-kpi*, .cmd-sum__*, .cmd-sumhead,
  .cmd-sumwrap, .cmd-sumbox__title) -> tổng 28. Plan ước 19 là ĐẾM HỤT; đổi đúng 19 thì bộ vẫn đỏ.
  tkt-result-report.spec.ts: đúng 15/15. Danh sách selector "không tìm thấy nơi định nghĩa": RỖNG.
  --list: 18 và 10 ca, đúng kỳ vọng. e2e không phải git repo -> không commit.
Task 12: đã dispatch (sonnet) — nghiệm thu 8 luồng x 2 popup + kiểm hồi quy popup 1 + thử bộ e2e.
Task 12: complete — ĐẠT toàn bộ, không hồi quy, không phải sửa gì.
  Phần A: 8/8 luồng ĐẠT cho CẢ 2 popup mới. Đáng chú ý: popup CMD lọc client -> 0 request API khi
    lọc/xoá lọc; popup TKT lọc BE -> đúng 1 request mỗi thao tác. Cả 2 popup có heightNormal=844,
    heightFull=900, border-top 1px, radius 6px — KHỚP CHÍNH XÁC baseline popup gốc => đúng 1 vỏ.
  Phần B (hồi quy popup 1): 9 khớp + đúng 2 khoá lệch đã biết, KHÔNG có khoá thứ ba. 3 phép đo
    từng lọt lưới đều đạt: ô tiền vẫn right/700, mở popup 1 request, trang 3 bấm sort về trang 1.
  Phần C: api-setup đổ đúng vật cản môi trường đã biết (không sửa); 3 spec biên dịch OK: 29/18/10.
Đã dispatch rà soát cuối Phase 2, trọng tâm: 3 popup có dùng vỏ NHẤT QUÁN không.

## Rà nhất quán 3 popup (vòng cuối Phase 2)
Đạt ở tầng khung nhìn (vỏ không rò nghiệp vụ; override sortedRows của popup2 an toàn). CHƯA đạt ở
tầng mảnh nghiệp vụ: 5 điểm lệch + 3 lỗ hổng tài liệu.
USER CHỐT: (1) dọn 5 điểm rẻ + viết tài liệu vào code; (2) popup 3 thiếu nút "Xoá lọc" và chip
không bấm được là BỎ SÓT -> bổ sung cho giống 2 popup kia.
BASE cho lượt dọn: 01a6fbb28

## Chạy e2e thật (sau khi gỡ vật cản e2e_provision.php)
Sửa 5 tên bảng hrm_* -> tên thật trong `hrm-api/database/e2e_provision.php` (CHƯA COMMIT).
Kết quả (đều chạy --workers=1, máy rảnh):
- tkt-result-report: **22/22 passed** (lượt đầu 19 passed/1 failed/1 flaky là NHIỄU do chạy chồng).
- customer-market-development: 7 passed / 2 failed (đều đỏ sẵn) / 26 did not run.
- potential-customer-care (UI): lượt đầy đủ 16 passed / 1 failed (ca 16, đỏ sẵn) / 13 did not run;
  khi loại ca đỏ sẵn thì 25+ ca xanh. Ca 27, 28, 29 (của phiên này) chạy riêng: ĐỀU XANH.

5 ca đỏ SẴN (không phải hồi quy, có bằng chứng): API tổng tỷ trọng (làm tròn 138 dòng);
API tổ hợp lọc AND (timeout); UI 16 "Tạo mới" (select ở màn tạo dự án TKT, popup đã làm đúng phần
của nó); UI 19 phân trang popup (test giả định chỉ 2 trang, DB nay 126 dòng); UI 26 lịch sử
(fixture cần >=2 meeting hoàn thành, DB có 1).

8 LỖI TRONG CHÍNH CÁC BÀI TEST TÔI VIẾT/SỬA, đã vá:
1. ca 9: `button:has-text("Tìm kiếm")` khớp nhầm nút toggle "Tìm kiếm nâng cao".
2. ca 27: phân nhánh theo "trang 2 có tiêu đề phần không" thay vì theo DANH TÍNH phần -> chỉ đúng
   một nửa trường hợp; dữ liệu khác đi là xanh giả.
3. ca 28: hàng nút đổi chỗ khi panel sang "bộ lọc gọn".
4. ca 28: bài test ghi cấu hình xuống DB, đỏ giữa chừng là để rác, đầu độc mọi lần chạy sau.
5. ca 28: helper neo /^Tìm kiếm$/ — RegExp so nguyên văn textContent (có xuống dòng) nên không khớp.
6. ca 28: sau khôi phục cấu hình, panel về chế độ nâng cao và khối ô lọc ĐÓNG -> phải mở lại (2 chỗ).
7. ca 29: quét 8 dòng đầu là quá hẹp.
8. ca 29: đếm nút "Xem biên bản" NGAY khi panel vừa hiện, trước khi panel nạp xong dữ liệu ->
   mọi dòng đều ra 0 và bài test chẩn đoán SAI thành "fixture không có biên bản".
Ruling: các bản sửa trên đều là sửa PHÉP ĐO cho đúng ý định ban đầu, KHÔNG nới lỏng assertion nào.

Dọn DB: xoá cấu hình rác `filter_customizations` của tài khoản e2e (1180) do ca 28 để lại.
