# Plan — Demo "Tạo đơn giao hàng từ Hợp đồng mua"

> Người phụ trách: @khoipv · Bắt đầu: 06/10/2026
> Spec: `docs/superpowers/specs/2026-10-06-demo-don-giao-hang-design.md`

## Task

- [x] 1. Đọc luồng Cung ứng + logic HĐ mua (purposes[], điều khoản TT, Bên A/Bên B) + chuẩn UI V2Base
- [x] 2. Thiết kế nghiệp vụ: giao cho công ty khác Bên A, điều khoản TT (trả trước → ĐNTT / công nợ: hạn nợ + gối đầu), 3 phương thức giao (NCC giao kho · NCC giao thẳng KH · Cty tự lấy → về kho / giao KH) + chi phí vận chuyển
- [x] 3. Code `demos/demo-tao-don-giao-hang.html` (style V2Base)
- [x] 4. Cập nhật `demos/README.md`
- [x] 5. Verify Playwright (MCP browser)
- [x] 6. Fill spec + design.md
- [ ] 7. User xem demo + phản hồi
- [x] 8. Bỏ ô "VAT phí VC (%)" — phí VC NCC thu nhập 1 số tiền, cộng thẳng vào tổng thanh toán NCC
- [x] 9. Bỏ phân bổ chi phí VC vào giá vốn (ô chọn + ghi chú ở tab Giao nhận, 2 cột ở bảng hàng, dòng ở khối tổng)
- [x] 10. Bỏ cột "SL giao*" ở bảng hàng — SL nhập ở từng phiếu; dòng ngoài phiếu / HĐ NT có ô Giao trong cột Phiếu; dòng tổng bỏ ô tổng SL
- [x] 11. Công ty tự lấy hàng → ẩn khối Chi phí vận chuyển, bỏ bảng khoản tự chi + dòng chi phí tự VC ở khối tổng / popup lưu
- [x] 12. Bỏ cách tính hạn nợ "Kết hợp (cái nào đến trước)" — chỉ còn Theo thời hạn / Gối đầu; HĐ có cả TIME + ROLLING mặc định Gối đầu
- [x] 13. Bỏ khung "Luồng xử lý đơn giao" (stepper) + nút Giả lập bước tiếp / Làm lại; Lưu và gửi duyệt → nhãn trạng thái "Chờ duyệt"
- [x] 14. Dữ liệu mẫu công ty lấy theo bảng `companies` trên PM (8 công ty con của MOTA GROUP: TA, AV, TB, MN, VL, ĐG, OPCN, VX — tên, MST, địa chỉ thật); đổi tên kho mẫu theo
- [x] 15. Bỏ khối "Lộ trình" ở tab Giao nhận & vận chuyển (HTML + renderRoute + CSS)
- [x] 16. Tạm bỏ ghi chú "Luồng: Đơn giao được duyệt → …" + nút "Xem trước đề nghị thanh toán" ở khối Thanh toán trước (giữ code popup ĐNTT để bật lại)
- [x] 17. Giao thẳng KH (NCC giao thẳng / tự lấy giao KH) → CHẶN hàng cung ứng nội bộ + mua ngoài phiếu đề xuất: khóa dòng ở popup ("Hàng nội bộ — phải về kho"), báo đỏ ở bảng hàng, chặn lưu
- [x] 18. Giao thẳng KH cho **nhiều khách / nhiều địa chỉ** trong 1 đơn: bỏ ô chọn 1 KH + chặn "Khác KH nhận"; tự nhóm hàng theo KH thành Điểm giao (địa chỉ, người nhận, SĐT riêng); phí VC NCC thu nhập theo từng điểm; nhãn Điểm N ở bảng hàng; Nơi nhận = danh sách điểm
- [x] 19. Nút xóa từng phiếu (1 mã × 1 KH/phiếu ĐX) trong cột Phiếu của bảng hàng — dòng có ≥ 2 phiếu; xóa xong phiếu được chọn lại ở popup, hết phiếu thì xóa cả dòng
- [x] 20. Bỏ dòng xem trước đơn đang lập (DGH-2026-0011 "Đang lập") khỏi bảng "Các đơn giao của HĐ này" — bảng chỉ liệt kê đơn đã lưu
- [x] 21. Bỏ chú thích "Chỉ HĐ mua Đã duyệt, còn hàng chưa giao (HĐ Nguyên tắc: không giới hạn SL)" dưới ô chọn HĐ mua
- [x] 22. Ngày giao dự kiến thêm giờ: ô ngày + ô giờ (`state.deliverTime`, mặc định 08:00) cùng 1 field; logic hạn chi / đến hạn vẫn theo ngày
- [x] 23. Kho nhận: chuyển chú thích "Lọc theo Công ty nhận hàng" vào tooltip (icon ⓘ cạnh nhãn)
- [x] 24. Nhận tại kho công ty: thêm "Ngày giờ nhận*" (ô ngày + ô giờ, mặc định theo Ngày giao dự kiến của header cho tới khi sửa tay — `state.recvDate`/`recvTime`)
- [x] 25. Chi phí VC công ty chịu → **bảng các khoản chi** tự liệt kê (Khoản chi — gợi ý sẵn, Điểm giao khi giao thẳng KH, Số tiền, Ghi chú, xóa dòng, + Thêm khoản chi, tổng); thay ô phí đơn + phí theo từng điểm; validate tên + số tiền > 0
- [x] 26. Đổi nhãn bảng "Các khoản chi phí NCC thu" → "Các khoản chi" (có thể thuê xe ngoài, công ty trả trực tiếp)
- [x] 27. Tab Giao nhận: chuyển chú thích thành icon ⓘ tooltip — giao thẳng KH (tự nhóm điểm giao, kho nhập-xuất thẳng), nhận tại kho (tạo phiếu nhập kho), ghi chú dưới bảng Các khoản chi
- [x] 28. Bỏ ô "Giao nhận theo HĐ" ở khối Thông tin hợp đồng mua
- [x] 29. Bỏ cảnh báo vàng "Phương thức khác điều khoản giao nhận của HĐ… ghi rõ lý do ở Diễn giải" ở tab Giao nhận
- [x] 30. Bảng Các khoản chi: bỏ cột "Điểm giao" (khoản chi tính chung cả đơn)
- [x] 31. Công ty tự lấy hàng tại NCC → hiện lại khối Chi phí vận chuyển với bảng Các khoản chi riêng (`state.selfCosts`, gợi ý: cước thuê xe ngoài, xăng xe, cầu đường, bốc xếp, công tác phí; không bắt buộc) — công ty trả trực tiếp, KHÔNG cộng vào tiền thanh toán NCC; hiện dòng riêng ở khối tổng + popup lưu
- [x] 32. Khối Lấy hàng tại NCC: bỏ Phương tiện (Xe công ty / Thuê ngoài), Xe / biển số, Đơn vị vận chuyển + validate + `onVehicle` (thuê xe ngoài ghi ở bảng Các khoản chi)
- [x] 33. Tách tiền hàng khỏi chi phí VC: bảng Các khoản chi (NCC chở + công ty chịu) thêm cột **Trả cho** (Đơn vị vận chuyển — công ty trả trực tiếp / NCC — cùng hóa đơn) + ô Đơn vị vận chuyển nhận tiền*; Tiền thanh toán NCC = tiền hàng + khoản trả NCC (không gồm khoản trả đơn vị VC); tab Thanh toán tách Tiền hàng / Phí VC NCC thu / Số tiền thanh toán NCC + khối riêng Chi phí VC trả đơn vị vận chuyển; sửa khối tổng, popup ĐNTT, popup lưu
- [x] 34. Fix ô select / input trong bảng Các khoản chi bị cắt chữ (ép cao 28px nhưng giữ padding 7px) → thêm `.v2-input.sm` (28px, padding 3px 8px); kèm sửa viền đỏ lỗi không hiện do trùng thuộc tính style

### Checkpoint — 06/10/2026
Vừa hoàn thành: Demo `demos/demo-tao-don-giao-hang.html` (4 tab + stepper luồng), README, spec + design. Verify MCP browser: 3 HĐ mẫu × các phương thức giao/thanh toán, không lỗi JS; đã sửa lộ trình không cập nhật khi đổi phương tiện + 2 lỗi CSS nhỏ.
Đang làm dở: —
Bước tiếp theo: User xem demo, chốt 5 câu hỏi mở trong spec mục 9.
Blocked: Chờ phản hồi user
