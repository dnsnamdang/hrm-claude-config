# Plan — Mockup màn Theo dõi thực hiện hợp đồng

> Nhánh `gop_db`. Design: `design.md`. File mockup: `mockup.html`.

## Phase 1 — Dựng mockup (XONG 02/09/2026)

- [x] T1. Đọc `THEO DÕI THỰC HIỆN HỢP ĐỒNG.docx`, tách yêu cầu thành 3 nhóm A (trường + trạng thái HĐ) /
      B (màn theo dõi) / C (3 báo cáo)
- [x] T2. Khảo sát hiện trạng: `pages/assign/contracts/` + `Modules/Assign/Entities/Contract/Contract.php`
      → xác định phần đã có vs phần còn thiếu
- [x] T3. Chốt phạm vi với user: bỏ màn danh sách, làm 1 màn chi tiết 7 tab, để lại nhóm A & C
- [x] T4. Trích shell (topbar + sidebar navy + SVG ribbon) từ `mockup-chi-tiet-bao-gia`, đổi tiêu đề
- [x] T5. Viết CSS: stepper 7 trạng thái, tab bar, KPI, stat strip, timeline, chip, callout, bảng, cột ghim
- [x] T6. Tab 1 — Thông tin chung (KPI, cảnh báo, 21 trường, phụ lục, timeline 8 mốc)
- [x] T7. Tab 2 — Hàng hoá ký (9 mã + 4 dịch vụ, nhóm A/B, chip PL01, dòng tổng khớp 5.038.000.000 ₫)
- [x] T8. Tab 3 — Cung ứng hàng (bảng phương án + mở rộng nguồn cung ứng, 3 mã thiếu)
- [x] T9. Tab 4 — Tài chính (dự toán vs thực tế, công nợ thu 5 đợt, phải trả NCC, hoá đơn–quyết toán)
- [x] T10. Tab 5 — Thiết kế & giám sát (6 hạng mục + nhật ký giám sát)
- [x] T11. Tab 6 — Giao hàng – Nghiệm thu (5 đợt giao + khối lượng theo mã)
- [x] T12. Tab 7 — Bảo hành (quỹ dự phòng, chi phí đã dùng, BH theo thiết bị ↔ NCC)
- [x] T13. JS chuyển tab + mở rộng dòng cung ứng
- [x] T14. Verify Playwright 1440×900, đo bằng số từ DOM

### Lỗi tự phát hiện khi verify (đã sửa)

- [x] F1. `thead` sticky không dính (`theadTop: -124`) — `.tblwrap` cuộn ngang nhưng không cuộn dọc.
      Sửa: `overflow:auto` + `max-height:calc(100vh - 250px)`.
      ⚠️ Lỗi có sẵn trong `mockup-chi-tiet-bao-gia` — cần sửa kèm khi port sang code thật.
- [x] F2. Tab 7 tràn ngoài màn ở 1440 (1208 > 1160) — rút nhãn tab 2 & 6, giảm padding tab.
- [x] F3. Cột *Hành động* (Giữ hàng / Đặt hàng) rơi ngoài vùng cuộn ngang → ghim `.stick-r`;
      cột ghim che đuôi *Đã về kho* → thu gọn cột, `min-width` 1320→1160, `td.name` 200→170px.

### Kết quả đo cuối

| Hạng mục | Kết quả |
| --- | --- |
| Pane hiển thị đồng thời | 1/1 ở cả 7 tab |
| Phần tử bị thanh hành động đè | **0** ở cả 7 tab (hở 42–43px) |
| `thead` dính mép khung | Đúng ở mọi bảng có cuộn dọc |
| Trang cuộn ngang | Không (1440 = 1440) |
| Cột ghim phải hiển thị | Đúng ở `scrollLeft` 0 và max; nút bấm được (`elementFromPoint` khớp) |
| Mở rộng dòng cung ứng | 9/9 |
| Lỗi console | 0 |

## Phase 2 — Chỉnh theo góp ý user (vòng 1 XONG 02/09/2026)

- [x] T15. **Sidebar thu gọn** — rail icon 62px mặc định, burger topbar bật/tắt về 236px, mỗi mục có tooltip,
      thanh hành động bám theo (`left` 62 ↔ 236)
- [x] T16. **Bỏ thanh trạng thái (stepper)** — màn chỉ áp dụng cho HĐ *Có hiệu lực*; trạng thái còn 1 chip cạnh mã HĐ
- [x] T17. **Rút gọn nhãn tab** — bỏ số thứ tự, giữ nguyên nghĩa; 7 tab vừa khít khung (dư 0px, không tràn)
- [x] T18. **Thiết kế lại khối tổng hợp 7 tab** theo mockup *Báo cáo kết quả CSKH tiềm năng*:
      card `.rsum` có nút Thu gọn + box `.rsum-blk` tint + hàng `.rsum-kpi` border-left, số lớn, track 5px, công thức.
      Bỏ hẳn `.kpis/.kpi` và `.stats/.st` cũ
- [x] T19. Verify lại toàn bộ — xem bảng đo ở `design.md` mục *Vòng 2*
- [x] T20. **Sửa lỗi số liệu**: tổng *Đang đi mua* 218 → **217**, *Đã phân bổ* 1.676 → **1.675**
      (cân đúng 1.458+217=1.675 và 1.675+92=1.767=tổng SL ký)

## Phase 2b — Dọn tab Thông tin chung (vòng 3 XONG 02/09/2026)

- [x] T21. **Bỏ summary tài chính khỏi tab Thông tin chung** (Giá trị & thu tiền, Chi phí & hiệu quả)
      → chỉ theo dõi ở tab Tài chính. Khối còn lại đổi tên *Tiến độ thực hiện*, 3 KPI tiến độ
- [x] T22. **Gỡ trùng lặp trong tab**: bỏ ô Số hợp đồng / Khách hàng / Trạng thái (đã có ở thanh tiêu đề);
      bỏ chip *còn 45 ngày*; bỏ dòng phụ đặt cọc; timeline bỏ chip cảnh báo + các dòng *mở khoá thanh toán đợt N*
- [x] T23. **Chia thông tin HĐ thành 4 nhóm chủ đề** (6 · 6 · 3 · 3 ô — không nhóm nào lẻ ô):
      Hồ sơ & các bên · Hiệu lực & thời hạn · Điều khoản hợp đồng · Cấu hình cảnh báo
- [x] T24. Verify lại — xem `design.md` mục *Vòng 3*

## Phase 2c — Gom nhóm thông tin & bỏ note điều hướng (vòng 4 XONG 02/09/2026)

- [x] T25. Card *Thông tin chung hợp đồng* → **Thông tin chung**, chia lại thành 4 nhóm theo yêu cầu:
      **Thông tin hợp đồng** (9 ô) · **Thông tin khách hàng** (6 ô) · **Hiệu lực & thời hạn** (9 ô) ·
      **File đính kèm** (bảng 4 file: tên · loại · ngày tải · người tải · dung lượng · nút tải về)
- [x] T26. Tách file bản ký khỏi ô *Ngày ký* để dồn hết về nhóm *File đính kèm*
- [x] T27. Card *Mốc thực hiện hợp đồng* → **Tiến độ thực hiện theo các mốc thời gian**
- [x] T28. **Bỏ các note điều hướng sang tab khác** — gỡ `.rsum-sub` tab 1, cắt vế trỏ tab ở hint
      tab *Hàng hoá ký* và *Thiết kế & giám sát*; đo còn 0 lần trên toàn trang
- [x] T29. Verify lại — xem `design.md` mục *Vòng 4*

## Phase 2d — Trường định danh & màu tab (vòng 5 XONG 02/09/2026)

- [x] T30. Nhóm *Thông tin hợp đồng*: đưa **Số hợp đồng lên đầu tiên**, thêm Trạng thái + Loại tiền tệ → **12 ô**
- [x] T31. Nhóm *Thông tin khách hàng*: đưa **Mã khách hàng · Tên khách hàng · Mã số thuế lên trước**,
      tách SĐT / Email thành 2 ô → **9 ô**
- [x] T32. **Nới nguyên tắc gỡ trùng lặp** — trường định danh vẫn nằm trong nhóm của nó kể cả khi thanh tiêu đề
      đã hiện; chỉ gỡ lặp lại không mang thêm thông tin
- [x] T33. **Tô màu 7 tab** — mỗi tab 1 cặp biến `--tc` / `--tcl`; icon luôn tô màu tab, hover đổi nền tint,
      tab đang chọn = nền tint + chữ + viền trên cùng màu. Chiều cao 7 tab vẫn bằng nhau (35px), không tràn khung
- [x] T34. Verify lại — xem `design.md` mục *Vòng 5*

## Phase 2e — Rút gọn trường & KD phụ trách (vòng 6 XONG 03/09/2026)

- [x] T35. **Bỏ dòng meta *Người lập · Tạo lúc*** ở card Thông tin chung
- [x] T36. **Thanh tiêu đề bổ sung *KD phụ trách: Nguyễn Thu Hà*** (đoạn `.cust` thứ 2, ngăn bằng vạch dọc)
- [x] T37. **Bỏ 4 trường** khỏi Thông tin chung: *Mẫu in · Người nhận cảnh báo · Cảnh báo giao hàng ·
      Cảnh báo hết hiệu lực* → nhóm HĐ còn 10 ô, nhóm Hiệu lực còn 7
- [x] T38. Chống ô lẻ dòng: ô *Thời gian bảo hành* cho tràn hết hàng (`.irow.full`);
      gộp *Ngày bàn giao mặt bằng* vào ô *Mốc tính thời hạn* để nhóm Hiệu lực về đúng 6 ô (3×2)
- [x] T39. Verify lại — xem `design.md` mục *Vòng 6*

## Phase 2f — Mở ô nhập cho trường nhập tay (vòng 7 XONG 03/09/2026)

- [x] T40. Rà lại tài liệu gốc, lọc ra đúng các trường ghi *bắt buộc nhập / chọn ngày / nhập số ngày /
      phải nhập ngày + biên bản đính kèm / bắt buộc lý do*
- [x] T41. Tab *Thông tin chung*: 6 ô nhập (Ngày ký · Điều kiện hiệu lực · Ngày có hiệu lực ·
      Mốc tính thời hạn · Ngày đạt mốc · Thời hạn thực hiện) + dấu `*` bắt buộc;
      **Ngày hết hiệu lực khoá lại (`TỰ TÍNH`)** kèm công thức
- [x] T42. Tab *Tài chính*: ô nhập lý do vượt dự toán (dòng chưa nhập để viền đỏ + placeholder bắt buộc);
      ngày đạt mốc + nút Đính kèm biên bản cho đợt thanh toán chưa tới
- [x] T43. Tab *Thiết kế*: ngày duyệt + nút Tải hồ sơ cho 2 hạng mục chưa duyệt
- [x] T44. Tab *Giao hàng*: ngày dự kiến / thực tế + nút Đính kèm cho 3 đợt chưa giao
- [x] T45. **Không** mở nhập tay ở tab *Cung ứng* — SL Giữ hàng / Đang đi mua sinh từ phiếu giữ & đơn mua
- [x] T46. Verify lại — xem `design.md` mục *Vòng 7*

## Phase 2g — Gộp dịch vụ vào Cung ứng (vòng 8 XONG 03/09/2026)

- [x] T47. **Bỏ tab *Hàng hoá ký*** (gỡ cả nút tab lẫn `pane#p2`) → còn 6 tab
- [x] T48. Tab *Cung ứng* đổi tên **Cung ứng & dịch vụ**, thêm card **Dịch vụ đã ký** (4 gói:
      đơn vị thực hiện · hạn hoàn thành · % tiến độ · trạng thái hạch toán · nút Cập nhật tiến độ)
- [x] T49. Khối tổng hợp tab này đổi thành 2 block: *Hàng hoá cần cung ứng* (9 mã) / *Dịch vụ đã ký* (4 gói)
- [x] T50. Timeline: **bỏ chip *Đúng hạn* ở mốc Ký hợp đồng** — chỉ kiểm soát đúng hạn từ các mốc sau khi ký
- [x] T51. **Fix lỗi tự phát hiện**: card *Dịch vụ đã ký* chèn rơi ra ngoài `pane#p3` (hiện ở mọi tab)
      → chuyển vào trong pane; kiểm bằng cách liệt kê con trực tiếp của `.mainpad`
- [x] T52. Verify lại — xem `design.md` mục *Vòng 8*

- [x] T53. **User chốt: bỏ hẳn** đơn giá / thành tiền / VAT từng đầu mục — không đưa lại vào Cung ứng hay Tài chính.
      Kiểm bằng grep: 0 cột giá, 8/8 đơn giá từng mã = 0 lần; số tổng vẫn nguyên. Không phải sửa mockup.

## Phase 2h — Chỉnh bảng cung ứng (vòng 9 XONG 03/09/2026)

- [x] T54. **Header bảng có viền đầy đủ**, đồng nhất với thân bảng (`thead th` viền teal `#bfe3e8`)
- [x] T55. Dòng *Đang đi mua* hiện thêm **số Yêu cầu đặt hàng (YCĐH)**; số Đơn mua (PO) xuống dòng phụ
- [x] T56. Dòng *Giữ hàng* bổ sung **Hạn giữ**; hàng còn trong kho sắp hết hạn giữ có chip cảnh báo
- [x] T57. Cột **Đã về kho → Tồn kho khả dụng** (đổi cả nội dung: bỏ thanh tiến độ, thay bằng số tồn còn dùng được)
- [x] T58. **Dòng đã phân bổ đủ để ô Hành động trống** — bỏ 6 nút *Sửa phương án*
- [x] T59. Bảng chi tiết nguồn cung ứng thêm **hàng tiêu đề 8 cột** (trước đó cột ngày không có nhãn)
- [x] T60. **Fix bất nhất dữ liệu tự phát hiện**: cùng số PO ghi 2 nhà cung cấp khác nhau giữa tab Cung ứng
      và tab Tài chính → gán lại theo bảng công nợ NCC; sửa kèm câu nhắc PO ở tab Giao hàng
- [x] T61. Verify lại — xem `design.md` mục *Vòng 9*

## Phase 2i — Logic Hiệu lực & thời hạn (vòng 10 XONG 03/09/2026)

- [x] T62. *Kể từ ngày ký* → **Ngày có hiệu lực = Ngày ký**, đổi ngày ký thì chạy theo
- [x] T63. *Theo bảo lãnh được duyệt* → **hiện thêm Số bảo lãnh + Ngày bảo lãnh duyệt**;
      ngày hiệu lực lấy theo ngày bảo lãnh, dòng nguồn ghi kèm số bảo lãnh
- [x] T64. *Theo đặt cọc lần đầu* → lấy **ngày phiếu thu đặt cọc đầu tiên**; ghi rõ nguồn ở tab Tài chính (nối sau)
- [x] T65. **Ngày có hiệu lực chuyển thành ô `TỰ TÍNH`** (bỏ nhập tay) + dòng nguồn động
- [x] T66. **Ngày hết hiệu lực tính lại trực tiếp** = Ngày đạt mốc + Thời hạn thực hiện; thiếu dữ liệu hiện `—` + nhắc
- [x] T67. Fix lưới: bỏ `full` ở *Ngày có hiệu lực* để không còn ô trống lẻ ở cả 3 nhánh;
      thêm `.irow[hidden]{display:none}` (vì `.irow` là `display:flex` nên `hidden` mặc định không ăn)
- [x] T68. Chạy thử 8 kịch bản bằng Playwright — xem `design.md` mục *Vòng 10*

## Phase 2j — Tình hình đặt mua & tính theo SL còn lại (vòng 11 XONG 03/09/2026)

- [x] T69. Khối tổng hợp: giữ nguyên 2 block *Hàng hoá cần cung ứng* / *Dịch vụ đã ký*;
      **bỏ toàn bộ hàng KPI “Tình hình cung ứng”**, thay bằng **“Tình hình đặt mua”**:
      Tổng đặt mua (4 đơn mua) · Số lượng đã về kho (121) · Số lượng đang mua (96)
- [x] T70. **Popup chi tiết** cho 2 KPI sau — modal dùng chung, đóng bằng ×/nền/Esc;
      liệt kê theo mã: YCĐH · đơn mua · NCC · SL đặt · đã về / chưa về · ngày (dự kiến) về · tình trạng
- [x] T71. **Thêm 2 cột *SL đã xuất* + *SL còn lại*** sau *SL ký*; dựng lại toàn bộ bảng để
      **mọi cột sau tính theo SL còn lại** (phân bổ chỉ đếm nguồn chưa xuất giao)
- [x] T72. Mã đã giao đủ → `còn lại = 0`, trạng thái mới **Đã xuất đủ**
- [x] T73. Bỏ tổng cột *SL đặt* trong popup (mã ống thép nằm ở cả 2 popup nên cộng sẽ trùng)
- [x] T74. Nới popup 1.020 → 1.200px cho khỏi cắt cột *Tình trạng*
- [x] T75. Verify — xem `design.md` mục *Vòng 11*

## Phase 2k — Drawer CSKH & dọn ghi chú (vòng 12 XONG 03/09/2026)

- [x] T76. Dòng *Giữ hàng*: tình trạng **chỉ còn `Còn hạn` / `Quá hạn`**, suy từ Hạn giữ so với hôm nay
- [x] T77. **Bỏ toàn bộ dòng quy tắc / ghi chú** — 7 dòng `.hint` + dòng *Quy tắc* ở khối tổng hợp tab Cung ứng
- [x] T78. **Dựng lại popup theo khung `.ticket-drawer` của mockup Báo cáo CSKH tiềm năng**:
      drawer trượt từ phải, backdrop transition, header gradient + icon tròn + chip trắng mờ,
      thân nền xám chứa khối card có tiêu đề; màu nhấn theo ngữ cảnh (xanh lá / hổ phách)
- [x] T79. Khối *Hàng hoá cần cung ứng*: **Đã phân bổ → Số lượng đã giao** = 1.458 (82,5%)
      — đồng thời sửa số cũ đã lỗi thời (1.675)
- [x] T80. Fix cắt cột trong drawer: nới 940 → 1.080px + cho cột *Nhà cung cấp* xuống dòng → 0 ô bị cắt
- [x] T81. Verify — xem `design.md` mục *Vòng 12*

## Phase 2l — Popup căn giữa & sticky header (vòng 13 XONG 03/09/2026)

- [x] T82. **Đổi drawer trượt phải → popup căn giữa** theo khung `.minutes-modal` của mockup mẫu
      (1.240px / 94vw · max 86vh · `scale(.96)→scale(1)` + fade · backdrop `rgba(0,0,0,.4)`)
- [x] T83. **Bảng trong popup cuộn được + tiêu đề cột dính** — `.mm-wrap{max-height:56vh;overflow:auto}`
      + `thead th{position:sticky;top:0}` (đúng `.drill-wrap` của mẫu)
- [x] T84. **Tồn kho khả dụng ≤ 0 → bỏ nút *Giữ hàng***, chỉ còn *Đặt hàng*
- [x] T85. Verify — xem `design.md` mục *Vòng 13*

## Phase 2m — Tab Tài chính chia 4 tab con (vòng 14 XONG 03/09/2026)

- [x] T86. Dựng **component tab con** (pill xanh lá theo màu tab Tài chính) + JS chuyển pane con
- [x] T87. **Tab con 1 — Giá trị & thanh toán**: bảng giá trị HĐ & thuế (gốc / PL01 / tổng) ·
      điều khoản thanh toán 2 bên (tỷ lệ · thời hạn · chứng từ bắt buộc) · điều khoản khác
- [x] T88. **Tab con 2 — Công nợ NCC**: thống kê + cảnh báo quá hạn + công nợ theo NCC + **bảng phiếu chi** (7 dòng)
- [x] T89. **Tab con 3 — Công nợ KH**: thống kê + cảnh báo quá hạn + công nợ theo đợt +
      **bảng phiếu thu** (6 dòng) + hoá đơn–nghiệm thu–quyết toán
- [x] T90. **Tab con 4 — Dự toán**: thống kê + cảnh báo khoản vượt chưa có lý do + bảng dự toán vs thực tế
- [x] T91. Tách bảng *Công nợ phải thu* cũ: điều khoản → tab con 1, tình hình thu → tab con 3
- [x] T92. Verify — xem `design.md` mục *Vòng 14*

## Phase 2n — Tab Giao hàng & nghiệm thu (vòng 15 XONG 03/09/2026)

- [x] T93. **Đưa tab *Giao hàng & nghiệm thu* lên vị trí thứ 3** (di chuyển cả nút tab lẫn pane)
- [x] T94. Cột **Nội dung giao** → `N mã · M đơn vị`, **bấm ra popup** chi tiết mã + SL giao trong đợt
      (5 popup cho 5 đợt; tổng 9 mã · 1.767 đơn vị = đúng tổng SL ký)
- [x] T95. **Demo 1 đợt có nhiều PXK**: đợt 2 giao 2 chuyến — PXK-2026-1326 + PXK-2026-1331;
      popup chỉ rõ mã nào theo phiếu nào
- [x] T96. Bảng khối lượng: **bấm số cột *Đã giao* → popup serial** (5 popup);
      mặt hàng không quản lý serial thì popup nói rõ
- [x] T97. Tổng quát hoá popup: 1 module dùng chung, uỷ quyền click qua `[data-mm]`, cấu hình cột theo từng bộ dữ liệu
- [x] T98. **Fix lỗi tự phát hiện**: link serial gắn nhầm cột *SL ký* ở 3 dòng → đổi sang đếm chỉ số ô
- [x] T99. **Fix lệch số liệu**: đợt 3 còn 5 ngày (không phải 6) — đồng bộ 4 chỗ
- [x] T100. Verify — xem `design.md` mục *Vòng 15*

## Phase 2o — Đồng nhất màu header popup (vòng 16 XONG 03/09/2026)

- [x] T101. Header popup **dùng chung 1 gradient xanh** `#0a1c3d → #0e7490` như mockup Báo cáo CSKH;
      gỡ hết màu theo ngữ cảnh (xanh lá / hổ phách / hồng / teal) và biến inline `--mm-a`/`--mm-b`
- [x] T102. Verify 12/12 popup chỉ còn 1 gradient — xem `design.md` mục *Vòng 16*

## Phase 2p — Đổi nhãn tab (vòng 17 XONG 03/09/2026)

- [x] T103. Đổi nhãn tab **“Cung ứng & dịch vụ” → “Cung ứng”** (nội dung tab giữ nguyên 2 card)
- [x] T104. Verify nhãn + tab bar không tràn + bấm mở đúng pane

## Phase 2q — Góp ý tiếp theo (CHỜ)

- [ ] T105. User xem lại mockup vòng 17, ghi chú yêu cầu chỉnh → mỗi yêu cầu 1 task ở đây

## Phase 3 — Sau khi chốt UI (CHƯA BẮT ĐẦU)

- [ ] T16. Mockup nhóm A — bổ sung trường + luồng 7 trạng thái vào form hợp đồng
- [ ] T17. Mockup nhóm C — 3 báo cáo
- [ ] T18. Design chi tiết DB/BE/FE cho màn thật → `docs/superpowers/specs/gop-db/`

### Checkpoint — 03/09/2026 (vòng 17)
Vừa hoàn thành: đổi nhãn tab "Cung ứng & dịch vụ" → "Cung ứng".
Đang làm dở: không.
Bước tiếp theo: user duyệt vòng 17.
Blocked:

### Checkpoint — 03/09/2026 (vòng 16)
Vừa hoàn thành: header popup dùng chung 1 gradient xanh navy→teal như mockup CSKH, bỏ màu theo ngữ cảnh.
Đo 12/12 popup chỉ còn 1 gradient.
Đang làm dở: không.
Bước tiếp theo: user duyệt vòng 16.
Blocked:

### Checkpoint — 03/09/2026 (vòng 15)
Vừa hoàn thành: đưa tab Giao hàng lên vị trí 3; cột Nội dung giao thành "N mã · M đơn vị" bấm ra popup;
demo đợt 2 có 2 PXK; cột Đã giao bấm ra popup serial. Tự bắt & sửa 2 lỗi (link gắn nhầm cột, lệch số ngày).
Đang làm dở: không.
Bước tiếp theo: user duyệt vòng 15.
Blocked:

### Checkpoint — 03/09/2026 (vòng 14)
Vừa hoàn thành: chia tab Tài chính thành 4 tab con (Giá trị & thanh toán · Công nợ NCC · Công nợ KH · Dự toán),
mỗi tab con có thống kê + cảnh báo riêng; bổ sung bảng phiếu chi NCC và phiếu thu KH.
Kiểm cân bằng số học 3 nhóm bảng mới, khớp 100%.
Đang làm dở: không.
Bước tiếp theo: user duyệt vòng 14.
Blocked:

### Checkpoint — 03/09/2026 (vòng 13)
Vừa hoàn thành: đổi drawer sang popup căn giữa theo khung .minutes-modal của mockup mẫu;
bảng trong popup cuộn được + sticky header; bỏ nút Giữ hàng khi tồn kho khả dụng ≤ 0.
Đang làm dở: không.
Bước tiếp theo: user duyệt vòng 13.
Blocked:

### Checkpoint — 03/09/2026 (vòng 12)
Vừa hoàn thành: tình trạng giữ hàng chỉ còn Còn hạn/Quá hạn; bỏ hết dòng quy tắc; popup dựng lại theo
khung drawer của mockup CSKH; khối Hàng hoá cần cung ứng đổi sang Số lượng đã giao 1.458.
Đang làm dở: không.
Bước tiếp theo: user duyệt vòng 12.
Blocked:

### Checkpoint — 03/09/2026 (vòng 11)
Vừa hoàn thành: đổi hàng KPI sang "Tình hình đặt mua" + 2 popup chi tiết; thêm 2 cột SL đã xuất /
SL còn lại và dựng lại bảng cung ứng để mọi cột sau tính theo SL còn lại. Kiểm cân bằng số học 9/9 dòng, 0 lỗi.
Đang làm dở: không.
Bước tiếp theo: user duyệt vòng 11.
Blocked:

### Checkpoint — 03/09/2026 (vòng 10)
Vừa hoàn thành: logic Hiệu lực & thời hạn chạy thật — 3 nhánh điều kiện hiệu lực, ẩn/hiện 2 ô bảo lãnh,
ngày hiệu lực & ngày hết hiệu lực đều tự tính; chạy thử 8 kịch bản bằng Playwright.
Đang làm dở: không.
Bước tiếp theo: user duyệt vòng 10. **Còn treo:** nhánh *đặt cọc* đang hard-code ngày 12/05/2026 —
chờ dựng phiếu thu đặt cọc ở tab Tài chính rồi nối vào.
Blocked:

### Checkpoint — 03/09/2026 (vòng 9)
Vừa hoàn thành: header bảng có viền, thêm YCĐH + Hạn giữ vào dòng chi tiết, đổi cột Đã về kho →
Tồn kho khả dụng, bỏ nút Sửa phương án ở dòng đủ, thêm tiêu đề cho bảng chi tiết.
Tự bắt & sửa bất nhất PO → nhà cung cấp giữa tab Cung ứng và tab Tài chính.
Đang làm dở: không.
Bước tiếp theo: user duyệt vòng 9.
Blocked:

### Checkpoint — 03/09/2026 (vòng 8)
Vừa hoàn thành: bỏ tab Hàng hoá ký, gộp dịch vụ vào tab Cung ứng & dịch vụ (2 bảng),
bỏ chip Đúng hạn ở mốc Ký hợp đồng. Tự bắt & sửa lỗi card dịch vụ rơi ngoài pane.
Đang làm dở: không.
Bước tiếp theo: user duyệt vòng 8. **Đã chốt 03/09/2026:** bỏ hẳn đơn giá / thành tiền từng đầu mục —
màn theo dõi chỉ giữ số lượng ở cấp đầu mục, tiền chỉ ở cấp tổng.
Blocked:

### Checkpoint — 03/09/2026 (vòng 7)
Vừa hoàn thành: mở ô nhập tay cho đúng các trường tài liệu ghi bắt buộc (19 ô ở 4 tab),
khoá ô Ngày hết hiệu lực dạng TỰ TÍNH kèm công thức.
Đang làm dở: không.
Bước tiếp theo: user duyệt vòng 7.
Blocked:

### Checkpoint — 03/09/2026 (vòng 6)
Vừa hoàn thành: bỏ meta Người lập/Tạo lúc, thêm KD phụ trách lên thanh tiêu đề, bỏ 4 trường
(Mẫu in, Người nhận cảnh báo, 2 cảnh báo), sắp lại lưới để không có ô lẻ dòng.
Đang làm dở: không.
Bước tiếp theo: user duyệt vòng 6. **Chờ user chốt:** có bỏ luôn ô *NV kinh doanh* trong nhóm
Thông tin hợp đồng không (đã hiện ở thanh tiêu đề) — nếu bỏ thì nhóm về đúng 9 ô (3×3).
Blocked:

### Checkpoint — 02/09/2026 (vòng 5)
Vừa hoàn thành: bổ sung trường định danh (Số HĐ / Mã–Tên KH–MST) lên đầu nhóm, nới nguyên tắc gỡ trùng lặp,
tô màu nhận diện cho 7 tab.
Đang làm dở: không.
Bước tiếp theo: user duyệt vòng 5.
Blocked:

### Checkpoint — 02/09/2026 (vòng 4)
Vừa hoàn thành: gom lưới thông tin thành 4 nhóm theo yêu cầu (thêm nhóm Thông tin khách hàng + File đính kèm),
đổi tên 2 card, bỏ hết note điều hướng sang tab khác.
Đang làm dở: không.
Bước tiếp theo: user duyệt vòng 4.
Blocked:

### Checkpoint — 02/09/2026 (vòng 3)
Vừa hoàn thành: dọn tab Thông tin chung — bỏ summary tài chính, gỡ trùng lặp với thanh tiêu đề,
chia lưới thông tin thành 4 nhóm chủ đề.
Đang làm dở: không.
Bước tiếp theo: user duyệt vòng 3.
Blocked:

### Checkpoint — 02/09/2026 (vòng 2)
Vừa hoàn thành: Phase 2 vòng 1 — sidebar thu gọn, bỏ stepper, rút nhãn tab, thiết kế lại khối tổng hợp
7 tab theo mockup Báo cáo CSKH tiềm năng; sửa lỗi cộng tổng cột Đang đi mua (218→217).
Đang làm dở: không.
Bước tiếp theo: user mở lại `mockup.html` duyệt vòng 2.
Blocked:


---

### Checkpoint — 06/09/2026 (wrap up)

Mockup dừng ở **vòng 17**, chốt hình: 6 tab (Thông tin chung · Cung ứng · Giao hàng & nghiệm thu ·
Tài chính *(4 tab con)* · Thiết kế & giám sát · Bảo hành), 12 popup dạng `.minutes-modal` căn giữa,
19 ô nhập tay đúng chỗ tài liệu ghi bắt buộc.

**Cách mở (link không chết):** file tự chứa hoàn toàn — 0 tham chiếu ngoài (không CDN / `fetch` /
`XMLHttpRequest`) nên **mở thẳng bằng `file://` là bền nhất**:
`.plans/gop-db/theo-doi-thuc-hien-hop-dong/mockup.html`.
Bản HTTP dùng **cổng cố định 8700** (`python3 -m http.server 8700` trong thư mục feature) —
trước đây mỗi vòng verify lại đổi cổng rồi `pkill` server nên mọi link cũ user giữ đều chết.

*(Trong thư mục có thêm `QLHD_mockup.html` — bản sao user tự đặt tên, nội dung y hệt `mockup.html`.)*

**Còn treo:** nhóm **A** (bổ sung trường + luồng 7 trạng thái vào form HĐ) và nhóm **C** (3 báo cáo:
công nợ quá hạn · theo dõi đặt hàng theo HĐ có hiệu lực · theo dõi tiến độ giao hàng) — user chốt làm sau.
Màn **danh sách HĐ đang thực hiện** cũng để sau. Nhánh *đặt cọc* trong logic hiệu lực đang hard-code
ngày 12/05/2026, chờ dựng phiếu thu bên tab Tài chính rồi nối.

Blocked:
