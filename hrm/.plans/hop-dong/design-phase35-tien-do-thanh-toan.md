# Phase 35 — Tiến độ thanh toán chi tiết + cảnh báo thu tiền (HĐ bán HRM)

Nguồn: **yêu cầu khách hàng** 10/11/2026 mục 9 (`yeu-cau-bo-sung-10-11-gap.md`). Đợt 3 phần (a), làm sau Phase 34 (mốc Giao hàng lấy từ kế hoạch giao hàng).
Nguyên văn: "Cần chọn chi tiết để đưa ra được cảnh báo liên quan đến tiến độ thu tiền và công nợ quá hạn đối với khách hàng. Nếu chỉ thanh toán 1 lần
thì được chọn 1 trong các option của tất cả các lần. Lần 1: bao nhiêu ngày kể từ Ngày ký. Lần trung gian 2/3/4: Phê duyệt Thiết kế / Giao hàng có chữ ký KH /
Lắp đặt có chữ ký KH / Chạy thử có chữ ký KH (phải nhập ngày và có biên bản đính kèm) >> có cảnh báo kỹ thuật cần cập nhật biên bản. Nếu phê duyệt thiết kế /
lắp đặt / chạy thử: HĐ phải chọn bao nhiêu ngày kể từ ngày hiệu lực. Nếu Giao hàng: theo kế hoạch giao hàng. Lần cuối: Bàn giao nghiệm thu."

## 1. Đã chốt (12/11)

| # | Câu | Chốt |
|---|---|---|
| T1 | Hạn thu | **Hạn = ngày mốc**: ngày THỰC TẾ nếu đã nhập (biên bản), chưa có thì ngày DỰ KIẾN (ký + N · hiệu lực + N · hạn đợt giao). Quá ngày dự kiến mà chưa có biên bản ⇒ cảnh báo cập nhật biên bản |
| T2 | Ai nhập ngày thực tế + biên bản | **Chỉ người lập HĐ** (user đổi từ đề xuất "người lập + NV thực hiện"); cảnh báo cập nhật biên bản gửi người lập |
| T3 | Mốc Giao hàng | **Chọn đợt giao cụ thể** (Đợt n / Toàn bộ kế hoạch). Ngày thực tế = ngày đợt giao đủ theo Biên bản giao nhận (Phase 34), không nhập tay |
| T4 | Cảnh báo thu | Tiền đã trả (phiếu thu / báo có gắn HĐ) đắp vào các lần theo thứ tự hạn. Lần chưa thu đủ: nhắc khi còn **N ngày** (N = `companies.warning_due_date` "Thời gian hiển thị cảnh báo thu nợ đến hạn", có sẵn) + **Quá hạn** hôm sau hạn. Gửi **người lập** |
| T5 | Thứ tự mốc | **Ép khi gửi duyệt**: ≥ 2 lần ⇒ lần 1 = Ngày ký hoặc Hiệu lực, lần cuối = Nghiệm thu, lần giữa ∈ {Duyệt TK, Giao hàng, Lắp đặt, Chạy thử}; 1 lần ⇒ mốc bất kỳ. Mọi lần bắt buộc mốc + số ngày (Giao hàng: chọn đợt); tổng = 100% giá trị HĐ. Lưu nháp không ép |

## 2. Hiện có (Phase 5e, 16/10)

`hrm_contract_process_payments`: payment_type (Tạm ứng/Đặt cọc/Thanh toán), milestone (chữ), amount / amount_percent, payment_condition_id, offset_days, deadline (nhập tay), note.
Danh mục `payment_conditions` 8 mốc: KY_NGAY_KY · HIEU_LUC · DUYET_THIET_KE · GIAO_HANG_1 · GIAO_HANG_2 · LAP_DAT · CHAY_THU · NGHIEM_THU. FE `components/ContractPaymentTermsTable.vue`.
ERP: chỉ 1 hạn thu / HĐ (`payment_overdue_date` = duyệt + Số ngày nợ) + báo cáo cảnh báo thu nợ đến hạn — không theo từng lần.

## 3. Thiết kế (đề xuất — mockup trước khi code)

- **Dữ liệu** (`hrm_contract_process_payments` thêm cột): `delivery_batch_no` (mốc Giao hàng: số thứ tự đợt, 0 = toàn bộ kế hoạch — KHÔNG lưu id đợt vì kế hoạch lưu kiểu xoá-tạo lại, id đổi mỗi lần lưu), `event_date` (ngày mốc thực tế),
  `event_file_name/path` (biên bản), `event_updated_at`. Danh mục: gộp GIAO_HANG_1/2 ⇒ 1 mốc "Giao hàng có chữ ký KH" (đổi tên GIAO_HANG_1, ngừng GIAO_HANG_2; dòng cũ đang dùng _2 chuyển sang _1).
- **Hạn thu từng lần** (tính, không lưu): Ký ⇒ sign_date + N · Hiệu lực ⇒ effective_date + N · TK/Lắp đặt/Chạy thử/Nghiệm thu ⇒ event_date ?? (effective_date + N) ·
  Giao hàng ⇒ ngày đợt giao đủ ?? hạn đợt. Chưa có ngày gốc (chưa ký / chưa hiệu lực) ⇒ "Chưa xác định".
- **Số phải thu** từng lần = amount ?? amount_percent × giá trị HĐ sau VAT. **Đã thu** = bút toán thu gắn HĐ (cùng nguồn Phase 24 "Đang thực hiện": phiếu thu / báo có / điều chỉnh công nợ),
  đắp vào các lần theo hạn (sớm trước). Trạng thái lần: Đã thu đủ · Quá hạn · Sắp đến hạn (≤ N) · Chưa đến hạn · Chưa xác định.
- **Nút "Cập nhật mốc"** (màn xem HĐ, từng lần mốc sự kiện; người lập; HĐ KH đã ký / Có hiệu lực / Đang thực hiện): popup ngày thực tế * + biên bản * (khuôn Phase 32), sửa lại được, lịch sử cũ → mới.
- **Lệnh nhắc** `assign:warn-payment-schedule` 08:10: thu sắp hạn (còn đúng N) / quá hạn (hôm sau hạn) · mốc sự kiện quá ngày dự kiến 1 ngày chưa có biên bản ⇒ "cần cập nhật biên bản". Gửi người lập.
- **Form Lập/Sửa**: bảng tiến độ thanh toán thêm cột Hạn dự kiến (tự tính, chỉ đọc) + ô chọn đợt khi mốc Giao hàng; bỏ nhập tay `deadline`.
- **Gửi duyệt**: kiểm T5 (cùng 1 lần 422 với Phase 31/34).

## 4. Câu kỹ thuật còn mở (tự chốt khi lập plan)

- Nguồn "đã thu": xác nhận lại `ContractService::IN_PROGRESS_LEDGER_TYPES` + chiều Nợ/Có TK 131 trên dữ liệu thật (HĐ HRM chưa có bút toán ở rehearsal ⇒ test bằng fixture).
- Mốc Ký dùng `sign_date` (ngày KH ký, Phase 24) — HĐ chưa ký thì chưa có hạn.
- Đổi danh mục `payment_conditions` (bảng HRM) qua migration dữ liệu — liệt kê trước khi chạy.

Mockup: `mockup-tien-do-thanh-toan.html` (12/11, tương tác): ① bảng tiến độ ở form (mốc, số ngày / chọn đợt giao, hạn dự kiến tự tính, lỗi thứ tự mốc + tổng 100%
cùng lúc khi gửi duyệt) · ② màn xem (hạn thực tế / dự kiến, phải thu – đã thu – còn lại, badge, cảnh báo, nút Cập nhật mốc) · popup cập nhật mốc · ③ thông báo.
