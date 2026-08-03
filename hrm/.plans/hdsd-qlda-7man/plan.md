# Plan — HDSD 7 màn QLDA (theo HDSD.docx)

Nguồn yêu cầu: `HDSD.docx` (bảng 8 dòng). Output: **7 file Word tách theo màn** (user chốt).
Ảnh chụp thật trên https://dev-hrm.eteksofts.com/ — user cho phép **tạo bộ dữ liệu mẫu đẹp**.
Giao hàng: **làm hết rồi giao 1 lần** (user chốt).

## Phase 1 — Khảo sát code ✅ XONG
Kết quả lưu tại `.plans/hdsd-qlda-7man/khaosat/` — đây là **nguồn nội dung chính** để viết tài liệu.
- [x] `01-du-an-tao-sua.md` — Tạo/Sửa dự án TKT (từng trường, thêm nhanh KH, KH thương mại dịch vụ, cách triển khai)
- [x] `02-thu-thap-thong-tin.md` — Tab Thu thập thông tin trong chi tiết dự án
- [x] `03-meeting.md` — Meeting
- [x] `04-yeu-cau-lam-giai-phap.md` — YCGP + giải pháp + hồ sơ trình duyệt + lập HĐ ERP
- [x] `05-yeu-cau-bao-gia.md` — Báo giá + lấy từ BOM + gửi duyệt giá
- [x] `06-bom-giai-phap.md` — BOM thành phần/tổng hợp + hàng tạm + đồng bộ
- [x] `07-giao-viec-task-issue.md` — Task & Issue
- [x] `08-bang-quyen-tong-hop.md` — Bảng quyền 7 màn

## Phase 2 — Dữ liệu mẫu & ảnh (Playwright MCP)
Ảnh lưu tại `hdsd_7man_shots/`.
- [x] Login dev, khảo sát dữ liệu sẵn có
- [x] Dự án: 01 danh sách · 02 lọc nâng cao · 03 form tạo mới (full-page) · 04 popup Thêm nhanh KH · 05 tick "KH thương mại dịch vụ" (hiện khối KH thụ hưởng cuối) · 06 popup Chọn khách hàng · 07 chi tiết 10 tab · 08 tab Thu thập thông tin
- [x] Meeting: 10 danh sách · 11 lọc nâng cao · 12 form tạo mới · 13 tick "Meeting theo dự án" (hiện tab thứ 4 + khối Khách hàng) · 14 tab Biên bản
- [x] Task: 20 danh sách · 21 modal tạo chế độ Đơn giản · 22 chế độ Nâng cao
- [x] Issue: 25 danh sách · 26 modal tạo mới
- [x] BOM: 30 danh sách · 31 form tạo mới
- [x] Báo giá: 40 danh sách · 41 form tạo mới
- [x] YCGP: 50 form tạo mới
- [x] Mẫu phiếu: dùng **template 13 "Khảo sát Ứng dụng Gara tổng hợp"** (dữ liệu nghiệp vụ thật, 3 câu:
      1 checkbox 6 lựa chọn bắt buộc + 2 text dài) thay vì dựng mẫu tổng hợp — chất lượng minh hoạ tốt hơn.
      Ảnh: `09_danhmuc_maupheu.png`, `09b_maupheu_chitiet.png`
- [x] **Đã tạo dự án mẫu**: `HN_NSHC.UD.0101.2026.DA022 — Nâng cấp hệ thống quản lý gara VESTA` (id 277)
      · KH: TRUNG TÂM BẢO HÀNH Ô TÔ VESTA (29TPHPBA-180) · Loại hình: Ô tô và xe có động cơ khác
      · Lĩnh vực: Dịch vụ và bảo hành sửa chữa · Ứng dụng: Gara tổng hợp · Tự triển khai · Quy mô Vừa
      · Ngân sách 8.000.000.000 · trạng thái *Thu thập thông tin dự án*
      Ảnh: `03b/03c/03d_duan_taomoi_*.png` (form đã điền đầy đủ)
- [x] Phiếu thu thập của dự án mẫu: đã nhập đáp án + lưu; chụp `08b` (phiếu trống), `08c` (đã nhập),
      `08d` (lịch sử thay đổi có diff), `08e` (mẫu in)
- [ ] Đi tiếp luồng trên dự án 277: tạo Giải pháp → BOM → Báo giá → Task/Issue → Meeting gắn dự án
- [ ] Chụp bổ sung các popup: chọn nhân viên (meeting), điểm danh, modal Tiếp nhận YCGP, hồ sơ trình duyệt,
      popup chọn hàng hoá (dùng chung BOM + báo giá), thêm hàng tạm, chọn BL con, modal Gửi duyệt báo giá,
      màn Báo giá chờ duyệt, modal Nhập kết quả task, daily-report, các modal lịch sử

## Phase 3 — Dựng 7 file Word (HDSDClean, template `.claude/skills/hdsd-documenter/assets/HDSD_MAU.docx`)
Mỗi file theo cấu trúc skill: Bìa → Mục lục → Danh mục hình → Tổng quan → Truy cập & bố cục → từng PHẦN.
**Bắt buộc có mục "Phân quyền & hướng dẫn theo quyền"** — lưu ý phần lớn thao tác ghi KHÔNG gắn quyền,
phải mô tả theo **vai trò dữ liệu + trạng thái** (xem `08-bang-quyen-tong-hop.md` mục 8).
- [x] 1. HDSD_TaoSuaDuAn.docx — 32 trang, 9 ảnh
- [x] 2. HDSD_ThuThapThongTinDuAn.docx — 21 trang, 8 ảnh
- [x] 3. HDSD_Meeting.docx — 26 trang, 6 ảnh
- [x] 4. HDSD_YeuCauLamGiaiPhap.docx — 28 trang, 2 ảnh
- [x] 5. HDSD_YeuCauBaoGia.docx — 25 trang, 3 ảnh
- [x] 6. HDSD_BomGiaiPhap.docx — 23 trang, 3 ảnh
- [x] 7. HDSD_GiaoViec_TaskIssue.docx — 28 trang, 6 ảnh
- [x] Verify style: cả 7 file đều heading-override = 2 (đúng bằng baseline template),
      run định dạng trong ô bảng = 0, ảnh hỏng = 0, mọi ảnh nội dung 6.0" canh giữa.
      Đã render PDF kiểm mắt: heading xanh, bảng Light Grid Accent 1, body justify — khớp file mẫu.

## Script dựng tài liệu (tái tạo được)
Lưu tại scratchpad phiên làm việc: `hdsd_common.py` (phần dùng chung: TỔNG QUAN, PHÂN QUYỀN, TRUY CẬP)
và `doc1_duan.py` … `doc7_giaoviec.py`. Chạy: `PYTHONPATH=<scratchpad>:hdsd_p5_work python3.14 docN_*.py`
từ thư mục gốc HRM/. Nội dung lấy từ `.plans/hdsd-qlda-7man/khaosat/`, ảnh từ `hdsd_7man_shots/`.

## Hạn chế đã biết của bộ tài liệu v1.0
- Số ảnh không đều: 4 màn đầu ảnh đầy đủ; YCGP / Báo giá / BOM mới có ảnh danh sách + form tạo mới,
  chưa có ảnh các popup (chọn hàng hoá, thêm hàng tạm, chọn BL con, gửi duyệt giá, hồ sơ trình duyệt,
  nhập kết quả task, daily-report). Nội dung chữ vẫn mô tả đầy đủ các popup này.
- Chưa kiểm chứng bằng tay: câu hỏi checkbox nhiều lựa chọn của phiếu thu thập (xem mục "Cần kiểm chứng lại").

## Ghi chú
- `HDSD_luongchinh/` đã có tài liệu chồng lấn (HDSD_DuAnTienKhaThi, QLDA_1_QuanLyMeeting,
  QLDA_12_LamBaoGia, QLDA_13_TongHopBomlist, QLDA_2_GiaoTask) — bộ mới viết theo checklist HDSD.docx,
  chi tiết hơn và có mục phân quyền.
- Dữ liệu dev tham chiếu: dự án `DA01.UD.0100.2026.DA067 — TKT 2407 BOM - 1` (id 272, có GP + BOM);
  ứng dụng có mẫu phiếu Published: `Gara tổng hợp (trung tâm chăm sóc xe)` (app 323, template 13)
  — yêu cầu Loại hình `Ô tô và xe có động cơ khác` + Lĩnh vực `Dịch vụ và bảo hành sửa chữa`.

## Ghi chú kỹ thuật khi thao tác Playwright trên form Nuxt 2 này
- **KHÔNG dùng `$(select).val(x).trigger('change')`** để set V2BaseSelect: select2 đổi hiển thị nhưng
  **model Vue không cập nhật**, và còn làm hỏng reactivity của các select khác trên form (phải F5 làm lại).
- Cách đúng: gán `id` tạm cho `.select2-selection` rồi **click thật** bằng Playwright, sau đó click
  `.select2-results__option:has-text("…")`.
- Input/textarea thì set qua native setter + `dispatchEvent(new Event('input',{bubbles:true}))` là được.

## Cần kiểm chứng lại (chưa kết luận)
- Câu hỏi loại **checkbox nhiều lựa chọn**: tôi tick 4 ô bằng script, nhưng diff lịch sử và mẫu in chỉ
  ghi nhận **1 giá trị ("Bảo dưỡng")**. Chưa rõ do cách click bằng script hay là lỗi lưu nhiều lựa chọn.
  → **Phải thử lại bằng thao tác tay** trước khi viết vào HDSD hoặc báo lỗi.

### Checkpoint — 2026-07-28 (bàn giao v1.0)
Vừa hoàn thành: **ĐỦ 7 FILE WORD** trong `HDSD_luongchinh/`, tổng 183 trang, style khớp file mẫu.
Đang làm dở: không.
Bước tiếp theo: user duyệt nội dung; nếu cần thì bổ sung ảnh popup cho 3 màn YCGP / Báo giá / BOM.
Blocked: không.

### Checkpoint trước đó — 2026-07-28
Vừa hoàn thành: Phase 1 trọn vẹn (8/8 khảo sát, đã lưu ra `khaosat/`);
Phase 2 chụp xong **17 ảnh khung chính** của cả 7 màn (danh sách + form tạo mới + các trạng thái điều kiện).
Mọi giá trị mặc định trong khảo sát đã được **đối chiếu khớp với ảnh thật** (Task: Nháp/hôm nay/17:00;
Issue: Lỗi phần mềm/Trung bình/Cá nhân/Tự phát hiện/1 ngày; Báo giá: Bảng giá "Bán lẻ", mã "(Chưa tạo)";
BOM: "BOM LIST thành phần"; Meeting: người tạo tự vào Thành phần phía Công ty).
Đang làm dở: Phase 2 — còn dựng dữ liệu mẫu + chụp các popup chi tiết.
Bước tiếp theo: (1) tạo mẫu phiếu thu thập đầy đủ loại câu hỏi + dự án mẫu đi hết luồng;
(2) chụp bổ sung popup; (3) Phase 3 dựng 7 file Word bằng `HDSDClean`.
Blocked: không
