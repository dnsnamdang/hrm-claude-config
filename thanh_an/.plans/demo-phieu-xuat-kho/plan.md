# Plan — Demo Phiếu xuất kho

> @khoipv · Bắt đầu 23/11/2026 · Tiếp luồng từ `demos/demo-phieu-de-nghi-xuat-kho.html`
> Demo: `demos/demo-phieu-xuat-kho.html` · Spec: [2026-11-23-demo-phieu-xuat-kho-design.md](../../docs/superpowers/specs/2026-11-23-demo-phieu-xuat-kho-design.md)

## Phase 1 — Tìm hiểu & chốt hướng
- [x] 1. Đọc PXK bên hrm (`pages/finance/warehouse-exports`, `WarehouseExportService`): tạo từ ĐNXK, thủ kho kho đó lập, lô/vị trí, không giá
- [x] 2. Đọc logic kho Thành An: `stock_balances` / `stock_serials` / `stock_ledgers`, pattern Phiếu nhập kho (nháp → đã duyệt, thủ kho của kho, cảnh báo HSD)
- [x] 3. Chốt hướng: PXK lập từ ĐNXK (Chờ xuất kho / Đang xuất kho), 1 ĐNXK nhiều PXK (xuất từng phần), 2 trạng thái Nháp → Đã xuất kho

## Phase 2 — FE demo (`demos/demo-phieu-xuat-kho.html`)
- [x] 4. Dữ liệu mẫu: ĐNXK đang chờ (KHO01 / KHO02), PXK đã xuất + 1 PXK nháp, lô có giữ cho HĐ / tồn chung / KH gửi / cận date / hết hạn / serial
- [x] 5. Màn danh sách V2: tab Phiếu xuất kho + tab Đề nghị chờ xuất kho, bộ lọc đủ cột, cấu hình cột, xuất Excel, Sửa / Xóa / ⋮
- [x] 6. Popup Tạo mới: chọn ĐNXK chờ xuất của kho mình (chặn ĐNXK đang có PXK nháp)
- [x] 7. Form Tạo / Sửa: thông tin chung khóa theo ĐNXK, Ngày xuất, bảng hàng theo dòng ĐNXK → lô; Gợi ý lô (FEFO, ưu tiên lô giữ cho HĐ); lỗi realtime
- [x] 8. Duyệt xuất kho: popup xác nhận kèm cảnh báo mềm (xuất thiếu, cận date) → trừ tồn lô, seri, ghi thẻ kho, cập nhật Đã xuất / trạng thái ĐNXK
- [x] 9. Màn chi tiết: banner, thông tin chung, tab Hàng hóa / Thẻ kho / Lịch sử, footer In · Sửa · Xóa · Duyệt xuất kho · Gửi bộ phận giao hàng · Quay lại
- [x] 10. Bản in mẫu 02-VT (xem trước)
- [x] 11. `node --check` + test logic Node (FEFO, chặn vượt tồn, trừ tồn khi duyệt, ĐNXK chuyển 4/5)

## Phase 3 — Tài liệu
- [x] 12. Spec chi tiết `docs/superpowers/specs/2026-11-23-demo-phieu-xuat-kho-design.md`
- [x] 13. Tóm tắt `.plans/demo-phieu-xuat-kho/design.md` + câu hỏi mở
- [x] 14. Cập nhật `demos/README.md` + `STATUS.md`

## Phase 4 — Chỉnh theo phản hồi user (23/11/2026)
- [x] 15. Danh sách cuộn bị giật: ẩn `#footer` khi rỗng (fixed + backdrop-filter repaint mỗi khung hình), đồng bộ thanh cuộn trên/dưới có khóa chiều (tránh ping-pong), giữ vị trí cuộn khi vẽ lại bảng (bấm ⋮ / đổi trang)
- [x] 16. Chọn Phiếu đề nghị xuất kho ngay trong form Tạo mới (bỏ popup chọn trước): select bắt buộc + xóa chọn, chỉ ĐNXK chờ xuất của kho mình chưa có nháp; đổi / bỏ chọn khi đã nhập SL → xác nhận; chọn xong tự điền thông tin + gợi ý lô; Sửa nháp thì khóa 🔒
- [x] 17. Build lại + `node --check` + chạy lại test logic (40/40 + 16/16 luồng chọn ĐNXK trong form)

- [x] 18. (23/11) User hỏi chỉ cho chọn ĐNXK Chờ xuất kho → đã nêu vướng: xuất thiếu làm ĐNXK sang Đang xuất kho thì không xuất tiếp được → user chốt **giữ như hiện tại** (chọn được Chờ xuất kho + Đang xuất kho), không sửa code
- [x] 19. (23/11) Bảng hàng form PXK bỏ 2 cột Đã xuất / Còn phải xuất; cột SL đề nghị hiện phần ĐNXK còn phải xuất; lỗi đổi thành "Tổng SL xuất vượt SL đề nghị (x)"; build + test 40/40 + 16/16
- [x] 20. (23/11) Form PXK cho sửa thông tin vận chuyển (Vận chuyển / Người nhận / SĐT / Địa chỉ) — mặc định theo ĐNXK, validate bắt buộc + SĐT, KH tự lấy bỏ địa chỉ, "Lấy lại" theo ĐNXK, lưu trên PXK (không ghi ngược ĐNXK), chi tiết / danh sách / lọc / PGH / in 02-VT dùng thông tin PXK; build + test 40/40 + 16/16 + 21/21
- [x] 21. (23/11) Tạm bỏ hàng KH gửi khỏi demo PXK (bỏ lô CRP-3, dòng A7 của PDNXK2611-0008, nhãn/chip, logic `kgui`/`tgui`) — chờ user chốt logic rồi làm lại
- [x] 22. (23/11) Bổ sung hàng hóa mẫu cho PDNXK2611-0008 đủ trường hợp: A3 (hết hạn / cận date / nháp khác giữ), A6 (cho KH vay), A9 găng tay (thiếu tồn), A10 giá đỡ (không HSD), A11 dung dịch rửa máy (chỉ có ở kho khác); build + test 48/48 + 16/16 + 21/21
- [x] 24. (23/11) Bỏ dòng chú thích "Phiếu nháp khác giữ: x" dưới Tồn khả dụng ở form (vẫn trừ SL nháp khác giữ vào tồn khả dụng); test 48/48 + 16/16 + 21/21
- [x] 25. (23/11) Bỏ tab "Đề nghị chờ xuất kho" ở danh sách (chỉ còn list PXK; ĐNXK chờ xuất chọn trong form Tạo mới), bỏ CSS tab/tiến độ; test 48/48 + 16/16 + 21/21
- [x] 26. (23/11) Cột Tồn khả dụng: dòng nhóm từng hàng hiện tổng tồn khả dụng các lô xuất được (bỏ lô hết hạn), đỏ khi không đủ SL đề nghị; test 49/49 + 16/16 + 21/21
- [x] 27. (23/11) Chế độ thu gọn form PXK theo khuôn PNK + Báo cáo tồn kho: Thông tin chung Thu gọn / Mở rộng (thu gọn còn dòng tóm tắt + chip lỗi); từng hàng chip trạng thái + nút Chọn lô / Thu gọn, nút Mở tất cả / Thu gọn tất cả; > 5 hàng mặc định thu gọn; lưu lỗi tự mở phần lỗi; test 56/56 + 16/16 + 21/21
- [x] 28. (23/11) Góp ý: form quá đơn giản → đưa trường hợp khó lên đầu, làm kỹ luồng **chọn lô → chọn seri**: (a) dữ liệu mẫu Lô→Seri (máy đo đường huyết, cần 10 / 3 lô) + Lô+HSD+Seri (catheter, cần 10 / 4 lô: hết hạn, cận date, giữ HĐ, tồn chung), xếp đầu PDNXK2611-0008; (b) lô có seri: gõ SL ở lô → tự lấy seri, chip seri đã chọn bỏ được; (c) ô Quét / gõ seri ở từng hàng → tự nhận lô, báo seri lỗi (không có trong kho, khác hàng, khác kho, lô hết hạn, lô giữ HĐ khác, phiếu nháp khác giữ, đã chọn, vượt SL đề nghị); (d) popup Chọn seri theo lô: tìm kiếm, Chọn tự động, Bỏ chọn hết; (e) build + test — xong: hàng có seri mặc định mở khi thu gọn, chi tiết hiện seri dạng chip; test 81/81 + 16/16 + 21/21
- [x] 29. (23/11) Bỏ chú thích "· n seri đang ở phiếu nháp khác" ở cột Serial của lô (giống tồn khả dụng không hiện chú thích riêng)
- [x] 30. (23/11) Screenshot_60: (a) ô chọn Phiếu đề nghị xuất kho xếp phiếu mới nhất lên đầu → PDNXK2611-0008 (BV ĐK tỉnh Hà Nam) đứng đầu; (b) nút Mở tất cả / Thu gọn tất cả: còn dòng hàng nào đang mở thì hiện "Thu gọn tất cả" (trước chỉ khi mở hết mới đổi → chọn phiếu có dòng seri mở sẵn vẫn hiện "Mở tất cả chi tiết")
- [x] 31. (23/11) Hàng chỉ có seri, không lô (PNK cho bỏ trống lot_no): thêm A14 Máy đo SpO2 vào PDNXK2611-0008 (dòng tồn không lô giữ HĐ 2 + tồn chung 6, KHO02 2); ô Lô hiện "Không lô", thông báo quét / popup / toast / bản in gọi theo loại tồn, chip không đếm lô
- [x] 32. (23/11) Bỏ hết chỗ hiện "Nháp PXK-…": popup Chọn seri không liệt kê seri phiếu nháp khác đang giữ (thay vì khóa + nhãn Nháp <mã>); quét seri đó báo chung "Seri không còn khả dụng"
- [x] 33. (23/11) Bỏ toast "Đã gợi ý lô: ưu tiên lô giữ cho HĐ, sau đó HSD gần nhất — kiểm tra lại trước khi lưu." khi bấm Gợi ý lô (chỉ điền lại SL, không thông báo)
- [ ] 23. Làm lại hàng KH gửi trên PXK khi user chốt logic

## Câu hỏi mở (chờ user chốt)
- [ ] Q1. Phân quyền theo cấp cho màn danh sách PXK? (demo: thủ kho thấy phiếu kho mình, Cung ứng / BGĐ xem tất cả)
- [ ] Q2. Điều kiện xóa (`is_can_delete`)? (demo: phiếu Nháp + thủ kho của kho đó)
- [ ] Q3. Có cho bỏ duyệt / hủy PXK đã xuất (nhập lại kho) không? (demo: khóa như PNK)
- [ ] Q4. PXK có hiện đơn giá / giá vốn không? (demo: không, như hrm — mẫu in 02-VT để trống)
- [ ] Q5. Phiếu giao hàng lập theo từng PXK hay theo ĐNXK? (demo: theo từng PXK)
- [ ] Q6. Popup "Xuất kho" trên màn ĐNXK thay bằng chuyển sang màn tạo PXK? (demo PXK giả định đã thay)
- [ ] Q7. Ngày xuất cho lùi ngày không? (demo: ≥ ngày tạo ĐNXK, ≤ hôm nay)
- [ ] Q8. Sửa vận chuyển trên PXK có cần đồng bộ ngược về ĐNXK / báo người đề nghị không? (demo: không)

### Checkpoint — 23/11/2026
Vừa hoàn thành: Chọn lô → chọn seri cho trường hợp khó (Lô → Seri, Lô + HSD + Seri) xếp đầu PDNXK2611-0008 — gõ SL tự lấy seri, ô quét seri tự nhận lô, popup Chọn seri; bỏ chú thích seri ở phiếu nháp khác; ô chọn ĐNXK mới nhất lên đầu + nút Thu gọn tất cả khi còn dòng mở; thêm trường hợp chỉ seri không lô; bỏ nhãn "Nháp PXK-…" ở popup / ô quét; bỏ toast Gợi ý lô (test 87/87 + 16/16 + 21/21)
Đang làm dở:
Bước tiếp theo: User xem demo, chốt logic hàng KH gửi (việc 23) + câu hỏi mở Q1–Q8 → đồng bộ lại demo ĐNXK (bỏ popup Xuất kho, mã PXK, PGH theo PXK)
Blocked:
