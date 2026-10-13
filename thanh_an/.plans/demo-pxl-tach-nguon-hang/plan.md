# Plan — Demo PXL: tách "Mua hàng" thành khối Nguồn hàng

> Người phụ trách: @khoipv · Bắt đầu: 08/10/2026
> Spec: `docs/superpowers/specs/2026-10-08-demo-pxl-tach-nguon-hang-design.md`
> Chỉ làm DEMO HTML — chưa sửa code thật (`HandlingGoodsTable.vue`, `constants.js`).

## Task

- [x] 1. Đọc cấu trúc bảng hàng hóa PXL hiện tại (`HandlingGoodsTable.vue`, `constants.js` — COLS_BY_TYPE, buildHandlingSrcCols)
- [x] 2. Code `demos/demo-pxl-tach-nguon-hang.html`: khối **Nguồn hàng** (Lấy tồn kho + Mua hàng = SL đặt đơn) tách khỏi khối **Xuất phục vụ HĐ** (Bán · Xuất gửi · Trả gửi · Xuất vay · Trả vay · Xuất đổi); toggle Hiện trạng / Đề xuất mới; 3 loại phiếu (KH · Khách lẻ/HĐ · Nội bộ); khối đổi hàng
- [x] 3. Cập nhật `demos/README.md`
- [x] 4. Verify bằng MCP browser (không lỗi JS)
- [x] 5. User phản hồi: demo phải giống hệt màn PM thật, chỉ khác cấu trúc bảng
- [x] 6. Làm lại demo: clone HTML/CSS + font icon từ dev (`supply/supply_handlings/add?proposal_id=53`), chỉ vẽ lại bảng hàng hóa (loại KH) — Nguồn hàng (Lấy tồn kho · Mua hàng) / Xử lý cung ứng (6 cột xuất) / Kết quả (Đã xử lý · Còn lại · Chưa xuất)
- [x] 7. Verify MCP browser: 0 lỗi console, so ảnh với dev, thử báo lỗi + chuyển tab
- [x] 8. Lúc mở demo bỏ khối đổi hàng (dòng 4 = RO-SHPT-2210 hàng thường, chưa nhập)
- [x] 9. Nút "Chọn hàng hóa" mở popup "Chọn hàng hóa từ danh mục" clone từ dev (tìm kiếm, chọn dòng / chọn tất cả / bỏ chọn, hàng đã có trong bảng → "Đã thêm", Thêm vào đề xuất → thêm dòng mới vào bảng)
- [x] 10. Thêm cột **Hợp đồng bán** ngay sau cột Hàng hóa (trước khối Số liệu nguồn): mã HĐ màu xanh, tooltip ngày ký / kết thúc, hàng ngoài HĐ hiện "Ngoài HĐ"; hàng thêm từ popup mang theo HĐ của nó (HD-091 / HD-166); tfoot + dòng breakdown +1 cột
- [x] 11. Sửa popup theo đúng quy tắc **1 phiếu chỉ bám 1 HĐ** (`GoodsPickerModal.isOtherContract` + `lockedContractId` của PXL): hàng HĐ khác mờ + 🔒 "HĐ khác" (tooltip), không tick được, Chọn tất cả bỏ qua; sửa luôn icon avatar navbar bị hỏng
- [x] 12. Thêm tab phiếu con như PM (`HandlingSummaryTabs`): Phiếu đề nghị xuất kho (Bán hàng · Trả gửi · Xuất vay · Xuất đổi, mỗi hàng × mục đích 1 dòng) · Phiếu đề nghị mua hàng (= cột Mua hàng của khối Nguồn hàng) · Phiếu xuất gửi · Phiếu trả vay; tab tự hiện/ẩn theo SL. MỚI ở PDNXK: 2 cột "Xuất ngay từ tồn kho" / "Chờ hàng mua về"
- [x] 13. Fix bug (ca thật: `supply_handlings/add?proposal_id=62`): chọn "Chất hiệu chuẩn … mức trung bình" → đóng popup → không chọn tiếp được "… mức cao" (cùng mã HC-HH-084, khác dòng HĐ). Demo: khóa theo dòng HĐ thay vì theo mã; dòng HĐ khác cùng mã + cùng HĐ → nhãn "Cộng dồn", tick được, cộng dồn vào dòng sẵn có (như màn Đề xuất)
- [x] 14. Chọn lại hàng đã có (theo HĐ) thành **dòng riêng ngoài HĐ** để mua thêm cho khách vay / mua về tồn kho: popup thêm các dòng danh mục "Ngoài HĐ" (như goodsPool = dòng HĐ + catalogItems), mã đã có dòng HĐ vẫn tick được dòng Ngoài HĐ (nhãn "Dòng riêng"); dòng mới chèn ngay dưới dòng HĐ, không validate SL còn lại, ẩn nút Đổi; dòng HĐ giữ validate SL còn lại. Lấy tồn kho validate theo TỔNG các dòng cùng mã
- [x] 15. Tạm thời để trống 4 cột Số liệu nguồn: SL đang mua · SL hàng vay · SL hàng gửi · SL hàng đổi (bảng chính, dòng hàng gốc khi đổi, các tab phiếu con)
- [x] 16. 2 dòng cùng mã (dòng HĐ + dòng riêng ngoài HĐ): SL tồn kho của dòng dưới = tồn − phần "Lấy tồn kho" các dòng TRÊN cùng mã đã lấy (cả a lẫn b, có ghi chú "−X dòng trên"); validate / tự chia Lấy tồn kho theo tồn còn lại đó → lỗi chỉ báo ở dòng vượt; tab phiếu con dùng cùng số tồn còn lại
- [x] 17. Bỏ dòng ghi chú "−X dòng trên" dưới SL tồn kho (giữ tooltip khi rê chuột)
- [x] 18. Bỏ tự chia Lấy tồn kho / Mua hàng khi nhập SL đặt đơn (kể cả dòng dưới cùng mã, bỏ đổi hàng) → user tự nhập; validate giữ nguyên
- [x] 19. Bỏ cột "Chưa xuất" ở khối Kết quả (header, ô, tfoot, colspan dòng đổi hàng / breakdown); lỗi "Xuất vượt nguồn hàng" chuyển xuống ô Xử lý cung ứng đầu tiên bị vượt
- [x] 20. Fix: nút "Đổi sang hàng khác" bấm không có tác dụng (demo chưa gắn hành động) → mở popup chế độ đổi hàng như PM (`openSwapPicker` / `onSwapConfirm`): tiêu đề "Chọn hàng thay thế từ danh mục", ghi chú vàng, chỉ hàng danh mục (ngoài HĐ), chọn 1 (radio), khóa chính hàng gốc; đã nhập phân bổ thì hỏi lại; dòng thành hàng thay thế + dòng phụ "THAY CHO" hàng gốc, SL hàng gốc = SL đặt đơn; đổi tiếp giữ SL hàng gốc; picker coi mã hàng gốc là đã thêm
- [x] 21. Bỏ dòng "Phân bổ theo phương án: …" dưới dòng Tổng cộng của bảng hàng hóa
- [x] 22. Fix: nhập số lượng bị nhảy scroll — render() thay innerHTML nên khung `.table-responsive` mới có scrollLeft = 0, focus() lại kéo trang → giữ scrollLeft bảng + scroll trang qua mỗi lần vẽ lại, focus({ preventScroll: true })
- [x] 23. Lúc mở demo chưa có hàng nào (bỏ 4 dòng mẫu) → hiện khối rỗng như HandlingGoodsTable ("Chưa có hàng hóa nào trong phiếu xử lý." + nút Chọn hàng hóa)
- [ ] 24. User xem demo bản mới + chốt câu hỏi mở
- [x] 26. Thiết kế lại bảng hàng hóa thành **ma trận Nguồn × Mục đích** (theo ảnh phác tay): mỗi hàng 1 khối nhiều dòng — cột chung rowspan (STT, Hàng hóa, HĐ bán, SL còn lại theo HĐ, SL đặt đơn, **Mua thêm** nhập tay — placeholder gợi ý = đặt đơn − Σ ô, Đã xử lý, Còn lại, Thao tác); mỗi nguồn 1 dòng con (Tồn kho tự do · SL đang đi mua · Khách vay · Tồn kho gửi, ẩn nguồn = 0) × 6 cột mục đích, ô cấm xám ✗ + tooltip lý do. Validate: Σ dòng nguồn ≤ SL nguồn; Σ ô + Mua thêm ≤ SL đặt đơn. Bỏ khối Nguồn hàng (Lấy tồn / Mua hàng) + cột số liệu nguồn cũ. Tab phiếu con: PDNMH = Mua thêm; PDNXK tách theo nguồn (tồn → Xuất ngay, đang mua → Chờ hàng về); Xuất gửi / Trả vay = tổng cột. Giữ đổi hàng, dòng riêng ngoài HĐ, popup
- [x] 27. Dữ liệu demo đủ 4 nguồn cho mọi hàng trong danh mục (Tồn kho tự do · SL đang đi mua · Khách vay · Tồn kho gửi) — trước đây đa số hàng = 0 nên bị ẩn nguồn / "Không có nguồn sẵn"
- [x] 28. Dữ liệu demo trộn: một số hàng đủ 4 nguồn, một số thiếu vài nguồn, một số không có nguồn nào (để thấy cả trạng thái ẩn nguồn / "Không có nguồn sẵn")
- [x] 29. Gộp "Mua thêm" vào ma trận thành dòng nguồn **Mua hàng** (luôn hiện, cuối khối, SL nguồn "—" không giới hạn) × mục đích được nhập: Bán hàng · Trả vay · Xuất gửi · Xuất đổi (Trả gửi / Xuất vay cấm ✕). Bỏ cột Mua thêm riêng; ô Bán hàng của dòng Mua hàng có số mờ gợi ý = SL đặt đơn − Σ các ô khác. Validate Σ mọi ô ≤ SL đặt đơn. Tab phiếu con: PDNMH = Σ dòng Mua hàng; PDNXK/Xuất gửi/Trả vay tính phần từ Mua hàng vào "Chờ hàng mua về"
- [x] 30. Hoàn tác task 29: quay lại cột **Mua thêm** riêng như trước (khôi phục template.bak21 — giữ dữ liệu nguồn trộn của task 28)
- [x] 31. Ô cấm (cell-deny): để trắng, không nhập — bỏ nền sọc xám và dấu ✕ (giữ tooltip lý do khi rê chuột)
- [x] 32. Thêm cuộn dọc cho bảng hàng hóa: khung bảng giới hạn chiều cao (cuộn cả dọc lẫn ngang), đầu bảng 2 tầng + dòng tổng (tfoot) dính cố định, cột Định danh vẫn cố định trái; vẽ lại giữ nguyên vị trí cuộn dọc
- [x] 33. Đưa **Mua thêm** vào khối Nguồn hàng: dòng nguồn cuối mỗi khối (luôn có), ô nhập SL ngay ở cột SL nguồn (số mờ gợi ý = SL đặt đơn − Σ ô nguồn, báo "Vượt SL đặt đơn" tại đây), các ô mục đích để trắng; bỏ cột Mua thêm riêng; tfoot cột SL nguồn = Σ Mua thêm
- [x] 34. Dòng **Mua thêm** nhập được vào Mục đích sử dụng (Bán hàng · Xuất gửi · Trả vay · Xuất đổi; Trả gửi / Xuất vay để trắng) — như 1 nguồn có SL do người dùng nhập: Σ ô dòng Mua thêm ≤ SL Mua thêm (lỗi "Vượt SL mua thêm"), còn thiếu thì nhắc "X chưa chọn mục đích"; ô Bán hàng có số mờ gợi ý phần chưa chia; Đã xử lý = Σ mọi ô mục đích; tfoot cột mục đích gồm cả Mua thêm; PDNXK phần từ Mua thêm vào "Chờ hàng mua về"
- [x] 35. Đổi thứ tự nguồn: **Tồn kho gửi** đứng ngay dưới Tồn kho tự do (Tồn kho tự do → Tồn kho gửi → SL đang đi mua → Khách vay → Mua thêm)
- [x] 36. Demo mới `demos/demo-bc-tong-hop-nhu-cau-mua.html` — Báo cáo tổng hợp nhu cầu mua theo logic PXL mới: vỏ giống màn `/supply/reports/purchase-demand` trên dev; chỉ hàng có SL **Mua thêm** > 0 ở phiếu xử lý; cột Nhu cầu = SL Mua thêm; bỏ cột mục đích + bối cảnh nguồn; chia 2 tab: **Cần đi mua** (còn cần mua > 0) / **Đã có HĐ mua** (dòng đã lập HĐ/đơn mua — mua 1 phần thì nằm cả 2 tab)
- [x] 37. Cập nhật `demos/README.md` cho demo báo cáo nhu cầu mua
- [x] 39. Demo báo cáo nhu cầu mua: tab 2 chỉ hiện hàng đã có **HĐ mua** (bỏ đơn mua) — Đã mua / Còn cần mua chỉ tính SL trên HĐ mua; đổi tên tab, KPI, tooltip, dữ liệu mẫu
- [x] 38. Demo báo cáo nhu cầu mua: đổi tên cột "Nhu cầu" → "Cần mua thêm" (tooltip, dòng gợi ý, README)
- [x] 40. Fix demo báo cáo nhu cầu mua: bộ lọc (ô chọn / ô ngày / ô nhập) không thao tác được — làm cho các ô lọc dùng được và lọc thật trên dữ liệu mẫu
- [x] 41. Demo báo cáo nhu cầu mua: tab **Đã có HĐ mua** bỏ 3 cột Cần mua thêm / Đã mua / Còn cần mua
- [x] 42. Demo báo cáo nhu cầu mua: tab **Đã có HĐ mua** lọc theo hợp đồng mua (ô chọn HĐ ngay trên thanh công cụ + bấm chip HĐ để lọc) → nút **Tạo đơn mua** từ HĐ vừa lọc (popup xem trước các dòng, HĐ chờ duyệt thì khóa)
- [x] 43. Demo báo cáo nhu cầu mua: tab Đã có HĐ mua — khi đã lọc 1 HĐ thì hiện cột tick chọn hàng hóa của HĐ đó; Tạo đơn mua chỉ lấy hàng đã tick
- [x] 25. Fix: popup chọn hàng — 2 ô lọc "Tất cả hợp đồng" / "Phân loại: tất cả" không lọc được (là HTML select2 chụp từ dev, demo không có select2 + `pkList()` chưa đọc). Gắn dropdown cho 2 ô (có nút × xóa như allowClear), lọc theo `GoodsPickerModal.filtered`: HĐ cụ thể / "Ngoài hợp đồng" (__none__); phân loại Nhập khẩu / Phân phối lại (pill theo `import_type_id`); chế độ đổi hàng bỏ qua 2 bộ lọc; mở popup thì reset

### Checkpoint — 09/10/2026 (task 34–37)
Vừa hoàn thành: Mua thêm chia mục đích (34), Tồn kho gửi dưới Tồn kho tự do (35), demo `demos/demo-bc-tong-hop-nhu-cau-mua.html` (36) + README (37) — đã kiểm tra trên Playwright MCP (2 tab, số đếm 30/12, dòng mua 1 phần nằm cả 2 tab, link qua lại giữa tab, tìm nhanh, 0 lỗi JS)
Đang làm dở: —
Bước tiếp theo: chờ user góp ý demo báo cáo; vẫn chờ chốt câu hỏi mở của task 24
Blocked: —

### Checkpoint — 09/10/2026 (task 26)
Vừa hoàn thành: Bảng hàng hóa demo chuyển sang ma trận Nguồn × Mục đích (khối nhiều dòng, ô cấm ✕, Mua thêm nhập tay + gợi ý, validate vượt nguồn / vượt SL đặt đơn, tfoot theo cột, tab phiếu con theo nguồn). Đã kiểm tra MCP: ví dụ 2202 (150 = 15 + 20 + 50 + 20 + mua thêm 45), lỗi, đổi / bỏ đổi hàng, dòng riêng ngoài HĐ dùng chung nguồn; 0 lỗi JS (ảnh `.playwright-mcp/demo-v13-ma-tran-nguon.png`).
Đang làm dở: —
Bước tiếp theo: User xem demo. Lưu ý khi làm code thật: Trả vay hiện là "xuất HĐơn · không xuất kho" nhưng ma trận cho Trả vay lấy từ Tồn kho tự do / Đang đi mua → cần chốt lại định nghĩa.
Blocked: Chờ phản hồi user

### Checkpoint — 09/10/2026 (task 17–23)
Vừa hoàn thành: Bỏ ghi chú −X, bỏ tự chia nguồn, bỏ cột Chưa xuất, nút Đổi mở popup hàng thay thế, bỏ dòng Phân bổ theo phương án, fix nhảy scroll khi nhập, lúc mở chưa có hàng (khối rỗng). Đã verify MCP browser, 0 lỗi console (ảnh `.playwright-mcp/demo-v11-mac-dinh-rong.png`).
Đang làm dở: —
Bước tiếp theo: User xem demo; chốt có làm nút (+) "Thêm hàng thay thế" ở dòng THAY CHO (1 hàng gốc → nhiều hàng thay thế) + các câu hỏi mở bên dưới.
Blocked: Chờ phản hồi user

### Checkpoint — 09/10/2026 (cũ)
Vừa hoàn thành: Viết lại `demos/demo-pxl-tach-nguon-hang.html` giống màn PXL trên dev (navbar, khối thông tin, 3 tab, footer, CSS scoped + font icon của dev). Bảng mới: SL đặt đơn → [Nguồn hàng] Lấy tồn kho + Mua hàng → [Xử lý cung ứng] 6 cột xuất → [Kết quả] Đã xử lý / Còn lại / Chưa xuất. Có khối đổi hàng, báo lỗi ô, tự chia tồn/mua khi sửa SL đặt đơn.
Đang làm dở: —
Bước tiếp theo: User xem demo, chốt: ý nghĩa cột Kết quả; có cần bản Khách lẻ / Nội bộ; tab phiếu tổng hợp (đề nghị mua / xuất kho) hiển thị thế nào → rồi mới fill spec + sửa code thật.
Blocked: Chờ phản hồi user
