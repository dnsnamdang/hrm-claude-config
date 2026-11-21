# Plan — Demo "Phiếu đề nghị xuất kho" (tham khảo màn Yêu cầu xuất hàng bên hrm, có đổi hàng)

> Người phụ trách: @khoipv · Bắt đầu: 21/11/2026
> Design: `.plans/demo-phieu-yeu-cau-xuat-hang/design.md`
> Spec: `docs/superpowers/specs/2026-11-21-demo-phieu-yeu-cau-xuat-hang-design.md`

## Phase 1 — Khảo sát & thiết kế
- [x] 1. Đọc màn Phiếu yêu cầu xuất hàng bên hrm (`hrm-client/pages/finance/product-export-requests` + BE)
- [x] 2. Đọc luồng Thành An: PXL (ma trận nguồn × phương án, tab Đề nghị xuất kho), đổi hàng (khối cặp THAY CHO), kho / sổ tồn / PNK, phiếu giao hàng, HĐ bán
- [x] 3. Chốt thiết kế demo + viết spec + design tóm tắt

## Phase 2 — Demo HTML
- [x] 4. Code `demos/demo-phieu-de-nghi-xuat-kho.html` (đổi tên file từ demo-phieu-yeu-cau-xuat-hang.html) (style V2Base, vanilla JS, mở trực tiếp)
- [x] 4b. User đề nghị "làm demo đúng chuẩn base, skill như phần mềm hiện có" → dựng lại theo V2Base + skill list-page / button-convention / modal-popup / form-validate / select-and-input-state (bộ lọc thông minh floating field, bảng MISA, V2Button, V2BaseModal, V2Footer, validate realtime 3 mức); spec bổ sung mục 4.0 + 4.4, sửa Người tạo / Ngày tạo, màu trạng thái, bảng validate
- [x] 4c. `node --check` script + chạy thử logic lõi bằng Node (Còn lại / Tồn xuất được / đổi hàng / công nợ / parseQty) — khớp số kỳ vọng
- [x] 5. Cập nhật `demos/README.md`
- [x] 7. Đổi tên phiếu "Phiếu yêu cầu xuất hàng" → **"Phiếu đề nghị xuất kho"** (viết tắt ĐNXK, mã `PDNXK2611-0001` khớp tiền tố tab PXL): demo (tiêu đề, breadcrumb, popup, cột "Đã đề nghị" / "SL đề nghị", thông báo), spec, design, README, STATUS. Giữ nguyên tên file / folder để không gãy link
- [x] 8. Bỏ thông tin PXL trên phiếu (user: "chỉ cần biết tồn còn xuất được bao nhiêu"; chốt: chỉ giữ Tồn xuất được, giữ cột Nguồn tách dòng, chỉ lấy hàng đã có ở kho):
  - [x] Bảng hàng form: bỏ cột Phiếu xử lý / SL theo PXL / Đã đề nghị / Còn lại; ẩn dòng mua chưa về + đã đề nghị đủ; bỏ chip "Chưa về kho"; lỗi đổi thành "Vượt SL còn được đề nghị (x)"; dòng THAY CHO đổi "Tỷ lệ theo PXL" → "Tỷ lệ đổi"
  - [x] Ghi chú dưới bảng: bỏ dòng "Đã đề nghị" + dòng NCC giao thẳng; tooltip tồn bỏ chữ YC
  - [x] Chi tiết: bỏ cột Phiếu xử lý · Danh sách: bỏ lọc / cột / tìm nhanh theo PXL · Popup chọn HĐ: bỏ cột Phiếu xử lý
  - [x] node --check + chạy thử logic (ẩn A5s2 chưa về, A3 vượt tồn 28 cảnh báo cam, nhập 60 → "Vượt SL còn được đề nghị (30)")
  - [x] Cập nhật spec (D4, D5, D5b, 4.1, 4.2, validate, edge case), design (mục 10), README
- [x] 9. Bỏ cột Nguồn (user: "bỏ cái nguồn đi"):
  - [x] Bỏ cột Nguồn ở bảng hàng form + chi tiết; bỏ chữ "nguồn: …" ở tiêu đề bảng
  - [x] Gộp dòng thường cùng mã hàng + đơn giá thành 1 dòng (`buildRows` thêm `cap`/`parts`, `capOf`), hàng ĐỔI vẫn tách — tránh 2 dòng Glucose giống nhau
  - [x] node --check + chạy thử: GLU HĐ-0642 gộp còn 26 (20 + 6 đã về), nhập 27 → "Vượt SL còn được đề nghị (26)"
  - [x] Cập nhật spec (D5b, 4.2), design (mục 10), README
- [x] 10. User: "vẫn phải cho họ biết SL theo HĐ, đã xuất, còn lại":
  - [x] Bảng hàng thêm SL theo HĐ (nội bộ: SL theo phiếu) · Đã xuất (thực xuất PXK) · Chờ xuất (đã đề nghị phiếu khác chưa xuất, tooltip) · Còn lại = HĐ − Đã xuất − Chờ xuất; `reqd` trả thêm `e`
  - [x] Hiện lại dòng Còn lại = 0 (mờ, "Đã đề nghị đủ", khóa tick); bỏ chặn theo phần mua đã về (`capOf` = SL theo HĐ) → QTC chưa về hiện với tồn 0
  - [x] Lỗi về lại "Vượt SL còn lại (x)"; ghi chú dưới bảng giải thích Đã xuất / Chờ xuất
  - [x] node --check + chạy thử: HĐ-0655 GLU 15 / xuất 5 / chờ 7 / còn 3; EDTA 20 / 8 / 4 / 8; HĐ-0642 GLU nhập 29 → cảnh báo tồn 28, 31 → vượt còn lại 30
  - [x] Cập nhật spec (D4, D5b, 4.2, validate, edge case), design (mục 10), README
- [x] 11. User: "không cần đã xuất, chờ xuất, chỉ cần SL theo HĐ và SL còn lại" → bỏ 2 cột Đã xuất / Chờ xuất, tooltip cách tính đặt ở tiêu đề cột Còn lại, bỏ dòng mô tả công thức ở tiêu đề bảng, sửa ghi chú dưới bảng; node --check + chạy thử (HĐ-0655 GLU 15 / còn 3, EDTA 20 / còn 8; số cột khớp colspan); cập nhật spec / design / README
- [x] 12. User: "màn này chỉ demo loại xuất bán, chọn loại khác báo chưa phát triển":
  - [x] Select Loại xuất: option khác Xuất bán thêm hậu tố "(chưa phát triển)"; chọn → toast cảnh báo, giữ nguyên Xuất bán (không bỏ chọn hàng)
  - [x] Đổi 2 phiếu mẫu khác loại sang Xuất bán: PDNXK2611-0004 (nội bộ → HĐ-0655 EDTA 2, Kho Hà Nam, Nháp), PDNXK2611-0006 (cho vay → HĐ-0642 Glucose 10, Bị trả lại, sửa lý do)
  - [x] node --check + chạy thử: seed chỉ còn loại ban; HĐ-0655 GLU 15 / còn 3, EDTA 20 / còn 6; HĐ-0642 GLU 30 / còn 20
  - [x] Cập nhật spec (D3, dữ liệu mẫu, edge case), design (mục 11), README
- [x] 13. User: "tạm bỏ box công nợ (Trong hạn mức — Công nợ hiện tại / Giá trị phiếu / Công nợ sau phiếu / Hạn mức)":
  - [x] Thêm cờ `DEBT_ON = false`: ẩn box công nợ dưới bảng hàng, ẩn ô "Công nợ KH" trên thanh DEMO, Gửi kho bỏ kiểm công nợ → Chờ xuất kho (giữ code để bật lại)
  - [x] node --check + chạy thử: form không còn box, thanh DEMO không còn ô công nợ
  - [x] Cập nhật spec (D10), design (mục 12), README
- [x] 14. User hỏi "SL theo HĐ là SL ký hay SL còn lại" → giải thích (là tổng SL phải xuất từ kho theo PXL, cố định; hàng đổi là SL hàng thay), user chốt đổi tên cột → **SL cần xuất**: thêm tooltip ở tiêu đề + dòng ghi chú dưới bảng, tooltip Còn lại đổi theo; bỏ nhãn "SL theo phiếu" (chỉ còn Xuất bán); node --check; cập nhật spec (D4, D5b, 4.2, validate), design, README
- [x] 15. User hỏi bỏ cột Còn lại → chốt **giữ nguyên 2 cột** SL cần xuất · Còn lại (không sửa code). Giải thích: Còn lại = SL cần xuất − SL đã đề nghị phiếu khác (trừ cả phiếu nháp / chờ xuất, không chỉ phần đã thực xuất)
- [x] 16. User: "bỏ cột Còn lại, để SL cần xuất = SL HĐ − SL đã thực hiện":
  - [x] Gộp 2 cột thành 1 cột **SL cần xuất** (giá trị = còn lại; tooltip ô "Theo HĐ x − đã thực hiện y", tooltip tiêu đề giải thích công thức); "đã thực hiện" = đã đề nghị trên phiếu khác (kể cả nháp / chờ xuất) để tránh đề nghị trùng
  - [x] ncol 9 → 8, colspan tổng cộng 5 → 4; lỗi "Vượt SL cần xuất (x)"; ghi chú dưới bảng gộp 2 dòng; popup chọn HĐ cột "SL cần xuất"; log Đóng phần còn lại
  - [x] node --check + chạy thử: HĐ-0642 GLU 20 (30 − 10), EDTA 30 (50 − 20), QTB 2 (4 − 2); nhập 21 → "Vượt SL cần xuất (20)"; th = td = 12 (có đổi) / 11 (không đổi)
  - [x] Cập nhật spec (D5b, 4.2, validate), design, README
- [x] 17. Đổi tên cột "SL cần xuất" → **"SL còn lại HĐ"** (tiêu đề, tooltip, lỗi "Vượt SL còn lại HĐ (x)", ghi chú, popup chọn HĐ, log Đóng phần còn lại); node --check; cập nhật spec / design / README
- [x] 18. User: "SL đã thực hiện phải tính là đã đưa cho khách" → đã làm (delivered theo PXK KH tự lấy / PGH giao xong + dòng "còn đề nghị được") rồi user bảo **back lại như cũ** → đã hoàn nguyên demo + spec / design / README về bản task 17 (SL còn lại HĐ = theo HĐ − đã đề nghị trên phiếu khác); node --check + chạy thử lại: HĐ-0642 GLU 20 (30 − 10), nhập 21 → "Vượt SL còn lại HĐ (20)"
- [x] 19. Ghi chú dưới bảng: rút gọn dòng SL còn lại HĐ chỉ còn "SL còn lại HĐ = SL theo HĐ − SL đã thực hiện." (bỏ phần giải thích trong ngoặc + SL theo HĐ + phiếu hủy); tooltip tiêu đề cột giữ nguyên
- [x] 20. User: "cột Tồn xuất được thể hiện rõ tồn giữ cho HĐ này bao nhiêu, tồn chung bao nhiêu":
  - [x] Lô giữ chuyển từ theo KH sang **theo HĐ** (`lots.held` = id HĐ; `pendingMap` gom theo HĐ; `stockInfo` nhận F.src; popup Xuất kho lọc lô theo HĐ, chip "Giữ cho HĐ-xxxx")
  - [x] Ô Tồn xuất được: số chính đậm + dòng nhỏ "Giữ cho HĐ: x" · "Tồn chung: y" · "Đã đề nghị chờ xuất: −z" (chỉ khi có trừ); tooltip đổi theo
  - [x] node --check + chạy thử: GLU HĐ-0642 Kho tổng 18 = 6 + 22 − 10; GLU HĐ-0655 Kho tổng 19 = 5 + 22 − 4 − 4 (HĐ khác vượt giữ); QTB 8 = 0 + 8
  - [x] Cập nhật spec (D7), design (mục 5), README; sửa link tên file demo mới ở spec / design / plan / README / STATUS
- [x] 21. User: "chỉ cần biết giữ cho HĐ này, tồn chung bao nhiêu thôi" + "bỏ Đã đề nghị chờ xuất":
  - [x] Ô Tồn xuất được chỉ còn 2 dòng Giữ cho HĐ / Tồn chung (bỏ số tổng đậm + dòng chờ xuất); thêm `stockSplit()` tách phần còn xuất được (chờ xuất trừ tồn giữ trước)
  - [x] node --check + chạy thử: tổng 2 số = Tồn xuất được ở mọi dòng (HĐ-0642/0655, Kho tổng/Kho 2); không còn chữ "Đã đề nghị chờ xuất"
  - [x] Cập nhật spec D7, design mục 5, README
- [x] 22. User: "vẫn để tổng tồn xuất được" → thêm lại số tổng đậm trên 2 dòng nhỏ Giữ cho HĐ / Tồn chung (không có dòng chờ xuất); cập nhật spec D7 + design mục 5
- [ ] 6. User xem demo + phản hồi (chốt Q1–Q6 trong spec)

### Checkpoint — 21/11/2026
Vừa hoàn thành: Ô Tồn xuất được = số tổng đậm + Giữ cho HĐ · Tồn chung
Đang làm dở: —
Bước tiếp theo: User mở demo test tay, phản hồi + chốt câu hỏi mở Q1–Q6 → chỉnh demo
Blocked: 
