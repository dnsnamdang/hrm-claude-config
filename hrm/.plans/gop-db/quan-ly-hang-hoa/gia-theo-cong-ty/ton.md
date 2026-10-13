# Giá theo công ty — Tồn trước khi lập design/plan (09/10/2026)

> Bối cảnh: user 09/10 đảo QC-2 — bảng giá riêng theo công ty là nội dung chính, làm trước màn giá 2-D2 (`../2d-erp-khong-loi/d2-ton.md`).
> Gộp từ `khao-sat-erp.md` §6.1 (ERP-G1…G10) + `khao-sat-du-lieu-hrm.md` (HRM-G1…G10). Hệ quả chi tiết từng đáp án xem 2 file đó.
> Hỏi LẦN LƯỢT; chưa trả lời hết thì không viết design/plan, không code.

## Phát hiện chính

- 🔴 A4 "gán giá cũ về công ty tạo" ⇒ chi nhánh mất giá ngày bật: SG 5.012 · Vinh 2.283 · HP 826 · ETEK 566 · TPE 174 cặp hàng×công ty đang bán hàng của công ty khác (6 tháng + có hệ số; HRM đo 8.861 cặp / 56.576 dòng giá; ERP đo theo phạm vi khác 12.574 cặp / ~78.399 dòng). HP + ETEK bán 100% hàng công ty khác.
- 🔴 Bảng "chung" hôm nay do nhiều công ty cùng ghi: PTG Cty 4 định giá 984 mã chủ Cty 1, Vinh 118 mã (PTG ghi theo công ty tạo hàng `PriceCalculate.php:384`).
- 🔴 Rủi ro lớn nhất: chỗ đọc quên lọc công ty ⇒ nhân đôi dòng / `first()` lấy giá công ty bất kỳ, im lặng. ERP ~55–65 file (3 lõi phủ ~90% màn), HRM 20 file / 37 điểm. ⇒ lớp truy cập giá tập trung + test danh sách trắng file đọc bảng giá.
- `product_units`: 6 cột dùng chung, 13 cột theo công ty (giá vốn, giá mua ngoài, 2 định mức, `according_base_price`, 8 cột chờ duyệt).
- HRM dùng 3 nguồn "công ty tính giá" khác nhau (chứng từ / `info->company_id` / `current_company_role`).
- Kế toán: giá vốn kho 632/156 lấy sổ kho, không lấy `cost_price` ⇒ an toàn; rủi ro ở hạch toán hỗ trợ / hiệu quả HĐ / báo cáo lợi nhuận (đọc giá vốn sống rồi lưu số).
- `getPriceByUnitAndType` (26 chỗ lấy giá) + HRM `getUnitPrice` hôm nay KHÔNG nhân hệ số ⇒ sau khi nướng hệ số vào giá, các chỗ này đổi số với 846 mã có hệ số ≠ 1.
- Đề xuất mô hình B1: `product_company_units` (13 cột, UNIQUE unit×company) + `product_unit_prices.company_id` (2 bước nullable → NOT NULL + UNIQUE unit×company×loại giá); `product_expected_prices` thừa hưởng qua dòng cha. Bất biến: cặp hàng×công ty có trạng thái ⇒ có đủ bộ giá.
- Triển khai B0 thêm cột → B1 sửa đọc (cờ tắt) → B2 sửa ghi → B3 seed → B4 bật cờ từng công ty → B5 NOT NULL/UNIQUE, bỏ hệ số, bỏ cột cũ.

## Hỏi user

| # | Gốc | Câu | ⭐ | Trả lời |
|---|---|---|---|---|
| P1 | HRM-G1, ERP-G2 | Ngày bật, công ty khác chủ (đang bán hàng công ty khác) lấy giá ở đâu | Nhân bản chọn lọc: chép **đúng con số ERP đang hiện** (giá chủ × hệ số, làm tròn như `getData`) |✅ theo ⭐ (09/10) — chép đúng số ERP đang hiện (giá chủ × hệ số, làm tròn như getData) |
| P2 | HRM-G2 | Mốc "đang bán" để chọn cặp cần chép | chứng từ 6 tháng + mọi cặp đang có dòng hệ số/trạng thái |🔄 (09/10) user: "hàng do Cty 1 (Tân Phát) quản lý thì LUÔN sao chép giá cho Vinh (3), Hải Phòng (2), Sài Gòn (4) theo hệ số giá (không có hệ số ⇒ hệ số 1) và ngược lại ⇒ các công ty khác mặc định chưa dùng hàng của nhau". Không theo mốc chứng từ. **P2b** "ngược lại" = cụm 1-2-3-4 chép lẫn nhau: hàng của công ty nào trong cụm cũng chép cho 3 công ty còn lại, áp hệ số của công ty NHẬN (không có ⇒ 1); ~775k dòng giá mới từ hàng Cty 1. **P2c** ngoài cụm: chỉ quan tâm **Cty 7 ETEK Green**; Cty 5, 6, 8 **sẽ loại bỏ** ⇒ không chép, không xử lý giá riêng (ETEK 8 mất 566 cặp — chấp nhận). Cty 7 hiện không quản lý mã nào và không nằm trong số cặp đang bán hàng công ty khác ⇒ khởi đầu trống, lấy hàng về (2-C2) + tự nhập giá. **P2d** chép giá thì sinh kèm dòng trạng thái "Đang kinh doanh" ở công ty nhận (bất biến 2 chiều trạng thái ⇔ bộ giá) |
| P3 | HRM-G3 | Dòng giá cũ (264.646) gán cho ai | công ty tạo (giữ A4); công ty khác có bản sao qua P1 |🔄 (09/10) gán cho `products.company_id` (công ty quản lý hàng hoá) — = công ty tạo hiện tại: Cty1 258.270 · Cty4 6.215 · Cty3 138 · Cty2 18 · NULL 5 (hàng 9964 đã xoá) |
| P4 | ERP-G1 | Lúc chạy: công ty chưa có giá cho mã (hàng lấy về mới…) | chặn chọn hàng/chặn lưu chứng từ, báo "chưa có giá tại công ty" |🔄 (09/10) "chưa có giá tức là hàng đó chưa tới được status Đang kinh doanh ⇒ chưa vào popup được" — bất biến: Đang kinh doanh ở công ty ⇒ có bộ giá của công ty đó; popup chỉ lấy hàng Đang kinh doanh (như N53). Khớp H1'/H1'' (2-C): hàng tạo mới/lấy về treo ở "Đang nhập thông tin" tới luồng Tính giá (Phase 7) ⇒ trước Phase 7 công ty chỉ bán được hàng đã có trạng thái + giá từ backfill (cụm 1-2-3-4); Cty 7 chưa bán được mã mới cho tới Phase 7 (hiện cũng không bán mã nào) |
| P5 | HRM-G4 | Ai sửa giá mã nào | mỗi công ty sửa bộ giá của mình (bỏ luật QC-4) |✅ theo ⭐ (09/10) — bỏ QC-4 |
| P6 | HRM-G8, ERP-G6 | Chứng từ đọc giá của công ty nào | công ty ghi trên chứng từ (sửa/duyệt chứng từ cũ cũng vậy) |✅ theo ⭐ (09/10) |
| P7 | HRM-G5, ERP-G4 | Giá vốn theo công ty: cột nào, khởi tạo thế nào | 13 cột theo công ty (gồm ĐMGG thanh lý); backfill chép giá vốn chủ; hàng lấy về mới ⇒ 0 |✅ theo ⭐ (09/10) |
| P8 | ERP-G5 | Hạch toán hỗ trợ / hiệu quả HĐ khi công ty chưa có giá vốn | lấy giá vốn công ty chứng từ, thiếu thì chặn duyệt |✅ theo ⭐ (09/10) |
| P9 | HRM-G7, ERP-G3 | PTG + hàng tạm ERP (còn ở ERP tới Phase 7/6) ghi giá vào đâu | PTG ⇒ công ty lập phiếu; hàng tạm ⇒ công ty của hàng tạm |⏸ (09/10) "tới phase update phiếu tính giá hỏi lại" — cách ghi CẠM THỜI từ lúc bật giá công ty tới Phase 7 ⇒ P9b → (09/10) **không có giai đoạn tạm**: user chỉ đưa lên production khi XONG HẾT các phase ⇒ PTG/hàng tạm chốt ở Phase 7/6 |
| P10 | HRM-G6, ERP-G9 | Bỏ hệ số giá khi nào | cùng lúc bật giá theo công ty; chấp nhận 26 chỗ (khuyến mại, đơn mua, chuyển kho…) đổi sang giá có hệ số |✅ theo ⭐ (09/10) |
| P11 | ERP-G7, HRM-G10 | Cron 14:30 reset giá về 0 khi hết tồn (N5) | chỉ reset dòng giá của chính công ty có cấu hình |✅ theo ⭐ (09/10) |
| P12 | ERP-G10 | Bật thế nào | cờ bật lần lượt từng công ty, có lệnh so khớp trước khi bật |✅ theo ⭐ (09/10) — bật một lần cả cụm 1-2-3-4, lệnh so khớp trước khi bật, có cờ để lui |
| P13 | HRM-G9 | Duyệt/Không duyệt đổi `products.status` (soát lại D1) | chỉ duyệt của công ty chủ mới đổi status (2→1/5) |✅ theo ⭐ (09/10) — công ty khác chỉ đổi trạng thái theo công ty mình |
| P14 | ERP-G8 | Thứ tự với màn giá HRM 2-D2 | giá theo công ty lên trước hoặc cùng lúc màn Cập nhật giá + Duyệt giá HRM |✅ (09/10) lên cùng lúc — thực tế cả feature lên production một lần (xem dưới) |


## Ghi chú chốt 09/10/2026

- 🔴 **Triển khai production MỘT LẦN** khi đã xong hết các phase của feature Chuyển đổi hàng hoá (user 09/10) ⇒ không thiết kế giai đoạn
  chuyển tiếp/tạm giữa các phase (vd PTG ERP ghi giá theo công ty nào trong lúc chờ Phase 7). Câu hỏi kiểu "trong lúc chờ phase sau" ⇒ không hỏi.
- Cụm chép giá: **1 Tân Phát · 2 CN Hải Phòng · 3 CN Vinh · 4 TP Sài Gòn** (chép lẫn nhau, hệ số công ty nhận, mặc định 1, kèm trạng thái
  Đang kinh doanh). **Cty 7 ETEK Green** giữ, khởi đầu trống. **Cty 5, 6, 8 sẽ loại bỏ** — không xử lý giá riêng.
- Còn lại D2b/D5–D12 của `../2d-erp-khong-loi/d2-ton.md` phải soát lại theo mô hình mới (D2b tự hết: P5 mỗi công ty sửa giá của mình).
