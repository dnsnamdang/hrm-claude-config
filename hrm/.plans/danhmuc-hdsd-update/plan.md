# Cập nhật HDSD phần Danh mục cho khớp code hiện tại

**Người phụ trách:** @namdangit
**Mục tiêu:** Cập nhật lại 15 file HDSD trong `HRM/DanhMuc/` cho đúng logic code đang chạy (docs tạo 19–22/06/2026, code đã đổi nhiều).

## Quyết định đã chốt
- **Ảnh:** CHỤP LẠI THẬT bằng Playwright MCP (không giữ ảnh cũ).
- **Thứ tự:** làm theo mức thay đổi nhiều → ít, mỗi file xong báo cáo rồi làm tiếp.
- **Playwright MCP:** đã bật `--isolated` trong `~/.claude.json` (block project HRM, dòng ~743) để chạy browser riêng, không đụng phiên test local. → **CẦN RESTART Claude Code**. Vì isolated không giữ login nên **mỗi phiên phải tự login dev → cần tài khoản dev (email+mật khẩu) có quyền danh mục + có dữ liệu mẫu ở đủ trạng thái.**
- Site chụp: `https://dev-hrm.eteksofts.com`.

## Map tài liệu → code (sắp theo số commit đổi từ 18/6, nhiều → ít)
| # | Tài liệu (DanhMuc/) | Màn code (pages/assign/) | Commit | Trạng thái |
|---|---|---|---|---|
| 1 | HDSD_PhieuThuThapThongTin.docx | form-templates | 57 | ✅ XONG (dựng lại + verify) |
| 2 | HDSD_UngDung.docx | application | 47 | ✅ XONG (dựng lại + verify) |
| 3 | HDSD_LinhVucKhachHang.docx | customer-scopes | 39 | ✅ XONG (dựng lại + verify) |
| 4 | HDSD_NganHangCauHoiKhaoSat.docx | questions | 38 | ✅ XONG (dựng lại + verify) |
| 5 | HDSD_NhomNganh.docx | industry-groups | 37 | ✅ XONG (dựng lại + verify) |
| 6 | HDSD_HangMucDuAn.docx | project_items | 36 | ✅ XONG (dựng lại + verify) |
| 7 | HDSD_VaiTroDuAn.docx | project_role | 35 | ✅ XONG (dựng lại + verify) |
| 8 | HDSD_NhomGiaiPhap.docx | solution-groups | 34 | ✅ XONG (dựng lại + verify) |
| 9 | HDSD_GiaiDoanDuAn.docx | project_phase | 33 | ✅ XONG (dựng lại + verify) |
| 10 | HDSD_LoaiMeeting.docx | meeting_type | 30 | ✅ XONG (dựng lại + verify) |
| 11 | HDSD_LyDoThatBai.docx | reason_project_failure | 22 | ✅ XONG (dựng lại + verify) |
| 12 | HDSD_LoaiTaiLieu.docx | attachment-type | 14 | ✅ XONG (dựng lại + verify) |
| 13 | HDSD_KhachHang.docx | customers | 11 | ✅ XONG (dựng lại + verify) |
| 14 | HDSD_NhomLinhVucKhachHang.docx | customer-scope-groups | 9 | ✅ XONG (dựng lại + verify) |
| 15 | HDSD_LoaiChietKhau.docx | discount-types | 4 | ✅ XONG (dựng lại + verify) |

## Quy trình mỗi file (theo skill hdsd-documenter)
- [ ] Dump text+bảng doc cũ (python-docx) để đối chiếu
- [ ] Agent Opus đọc code FE+BE hiện tại → bảng lệch (doc cũ vs code)
- [ ] Chụp lại ảnh thật (Playwright isolated, login dev)
- [ ] Dựng lại docx (copy khung, strip body, rebuild, purge media mồ côi, updateFields)
- [ ] Verify: inline_shapes/tables/captions/Heading đúng, broken image = 0
- [ ] Báo cáo, chuyển file tiếp

## Tiến độ

### File 1 — Phiếu thu thập thông tin (form-templates)
- [x] Dump doc cũ → `scratchpad_doc_phieu.txt` (HRM root) — 32 heading, 7 bảng, 11 ảnh
- [x] Đọc code FE+BE → bảng lệch đầy đủ: `form-templates-reconciliation.md` (cùng folder)
- [x] Chụp ảnh thật (dev, tài khoản namdangit) → `hdsd_phieu_shots/` 13 ảnh:
  01 danh-sách, 02 bộ-lọc, 03 builder-trống, 04 builder+thư-viện+section, 05 popup-tạo-nhanh,
  06 câu-hỏi-trong-section, 07 câu-hỏi-logic, 08 xem-trước, 09 xem-chi-tiết, 10 sửa,
  11 popup-khóa, 12 popup-xóa, 13 xem-trước-bản-in. (Không chụp màn quyền → giữ bảng quyền dạng text.)
- [x] Dựng lại docx (copy khung, strip body, rebuild, chèn 13 ảnh, purge media, updateFields) — generator: `scratchpad/gen_phieu.py`
- [x] Verify: 14 inline_shapes (13 hình + logo), 8 bảng, 13 caption, broken=0, không trùng ảnh, sectPr cuối, file 1.8M. Backup gốc: `scratchpad/HDSD_PhieuThuThapThongTin_BACKUP.docx`
- [x] 2 bẫy đã fix khi dựng: (1) caption proto kèm 1 drawing ẩn → clone 13 lần thành 13 ảnh thừa (fix: xóa drawing trong clone); (2) add_paragraph chèn TRƯỚC sectPr nhưng body.append chèn SAU → caption dồn cuối (fix: dùng sectPr.addprevious cho caption)

### File 2 — Ứng dụng (application)
- [x] Dump doc cũ → `scratchpad_doc_ungdung.txt`; reconciliation → `ungdung-reconciliation.md`
- [x] Chụp 8 ảnh dev → `hdsd_ungdung_shots/` (01 danh-sách, 02 bộ-lọc, 03 thêm-mới, 04 sửa, 05 xem-chi-tiết, 06 popup-xóa, 07 popup-khóa, 08 import)
- [x] Dựng lại docx → generator `scratchpad/gen_ungdung.py`. Verify: 9 inline_shapes (8 hình+logo), 7 bảng, 8 caption xen kẽ, broken=0, size 1.4M. Backup: `scratchpad/HDSD_UngDung_BACKUP.docx`
- [x] Bẫy khác template File 1: doc Ứng dụng KHÔNG có style Caption/TOF/List Bullet/Light Grid Accent 1 → CAP dùng đoạn Normal đánh số thủ công, BUL dùng "•" thủ công, TABLE tự vẽ viền + shade header. (Có TOC mục lục → updateFields vẫn cập nhật.)

**Thay đổi lớn File 2:** Nhóm ngành giờ chọn trực tiếp theo cặp với Nhóm giải pháp; thêm cặp bắt buộc "Loại hình:Lĩnh vực KH"; 2 cột danh sách mới; Tên cấm dấu `,` `:`; chặn khóa khi có dữ liệu liên kết; import thêm cột Lĩnh vực + Trạng thái bắt buộc.

### File 3 — Lĩnh vực khách hàng → "Lĩnh vực kinh doanh khách hàng" (customer-scopes)
- [x] Dump `scratchpad_doc_lvkh.txt`; reconciliation `lvkh-reconciliation.md`; 8 ảnh `hdsd_lvkh_shots/`
- [x] Dựng docx (template CÓ Caption → generator `scratchpad/gen_lvkh.py`). Verify: 9 inline_shapes, 7 bảng, 8 caption, broken=0, size 1.6M. Backup `scratchpad/HDSD_LinhVucKhachHang_BACKUP.docx`
- Thay đổi lớn: đổi tên "Lĩnh vực kinh doanh khách hàng"; mã LVKDKH.; cha đổi tên "Loại hình hoạt động khách hàng"; Xóa/Khóa luôn bật (BE hardcode); Tên cấm `,` `:`; import cha tùy chọn.

### File 4 — Ngân hàng câu hỏi khảo sát (questions)
- [x] Dump `scratchpad_doc_cauhoi.txt`; reconciliation `cauhoi-reconciliation.md`; 10 ảnh `hdsd_cauhoi_shots/`
- [x] Dựng docx (generator `scratchpad/gen_cauhoi.py`). Verify: 11 inline_shapes, 9 bảng, 10 caption, broken=0, size 1.3M. Backup `scratchpad/HDSD_NganHangCauHoiKhaoSat_BACKUP.docx`
- Thay đổi lớn: Nhóm ngành/Nhóm giải pháp → Ứng dụng (cột "Phạm vi câu hỏi" + "Ứng dụng"); bộ lọc 4 tiêu chí; BE ép Active khi tạo; chống trùng 4 yếu tố; điều kiện xóa khác doc cũ.

### File 5 — Nhóm ngành (industry-groups=scopes)
- [x] reconciliation `nhomnganh-reconciliation.md`; 8 ảnh `hdsd_nhomnganh_shots/`; generator `scratchpad/gen_nhomnganh.py` (template KHÔNG Caption). Verify: 9 inline_shapes, 7 bảng, 8 caption, broken=0, size 1.5M. Backup `scratchpad/HDSD_NhomNganh_BACKUP.docx`
- Chủ yếu KHỚP; sửa: toast "Thêm mới/Cập nhật thành công", Tên cấm `,` `:`, Mô tả form không giới hạn 1000, mã Sửa chặn ở lưu, import Status bắt buộc, Xem chi tiết hiện Số NGP/Số UD.

### File 6 — Hạng mục dự án (project_items)
- [x] generator `scratchpad/gen_hangmuc.py` (template KHÔNG Caption). Verify: 9 inline_shapes, 6 bảng, broken=0, size 1.7M. 8 ảnh `hdsd_hangmuc_shots/`. Chủ yếu KHỚP (catalog đơn giản: Tên + Trạng thái + Mô tả; xóa mọi trạng thái; không mã).

### File 7 — Vai trò dự án (project_role)
- [x] generator `scratchpad/gen_vaitro.py` (KHÔNG Caption). Verify: 9 inline_shapes, 6 bảng, broken=0, size 1.9M. 8 ảnh `hdsd_vaitro_shots/`. Chủ yếu KHỚP (cha-con; cột "Dùng ở dự án" BE chưa trả nên hiện trống).

### File 15 — Loại chiết khấu → "Loại giảm giá" (discount-types)
- [x] 7 ảnh `hdsd_chietkhau_shots/`; generator `scratchpad/gen_chietkhau.py`. Verify: 8 inline_shapes, 6 bảng, 7 caption, broken=0, size 1.6M.
- Thay đổi lớn: đổi tên "Loại chiết khấu" → "Loại giảm giá", mã CK- → GG-, quyền "Quản lý danh mục loại giảm giá", filter Trạng thái còn 2 lựa chọn.

## ✅ HOÀN THÀNH TOÀN BỘ 15/15 — 2026-07-16
Tất cả 15 file HDSD danh mục trong `DanhMuc/` đã dựng lại theo code hiện tại + verify (broken image=0, không trùng ảnh, sectPr cuối). Backup gốc từng file trong `scratchpad/HDSD_*_BACKUP.docx`. Generator từng file trong `scratchpad/gen_*.py`. Ảnh nguồn trong `hdsd_*_shots/`. Reconciliation chi tiết một số file trong `.plans/danhmuc-hdsd-update/*-reconciliation.md`.
LƯU Ý người dùng: mở file bằng Word, chọn cập nhật trường (hoặc Ctrl+A → F9) để Mục lục + Danh mục hình ảnh đánh lại số. Máy không có LibreOffice nên chưa render kiểm layout — cần mở xem bằng Word.

**LƯU Ý template khi dựng file mới:** kiểm tra doc có style Caption / List Bullet / Light Grid Accent 1 không. Có → generator kiểu gen_phieu.py/gen_lvkh.py; Không → kiểu gen_ungdung.py (CAP/BUL/TABLE thủ công). 2 bẫy luôn phải fix: caption proto kèm drawing ẩn (xóa drawing trong clone); caption phải chèn bằng sectPr.addprevious (không dùng body.append).

**LƯU Ý template khi dựng file mới:** kiểm tra doc có style Caption / List Bullet / Light Grid Accent 1 không trước khi chọn generator. Có → kiểu gen_phieu.py; Không → kiểu gen_ungdung.py (CAP/BUL/TABLE thủ công).

**Thay đổi lớn nhất:** bỏ hoàn toàn "Nhóm ngành + Nhóm giải pháp" → thay bằng MỘT trường "Ứng dụng" (application_id). Kéo theo: cột danh sách còn 6, bộ lọc, builder chỉ còn 2 trường thông tin chung, ràng buộc "1 Ứng dụng = 1 mẫu Hoạt động", luồng sao chép đổi, popup Tạo nhanh thêm trường Trạng thái. Chi tiết xem file reconciliation.

## Checkpoint — 2026-07-16 (trước khi restart lấy --isolated)
Vừa hoàn thành: đọc code form-templates + bảng lệch; bật --isolated cho Playwright MCP; lưu plan.
Đang làm dở: chờ RESTART Claude Code để --isolated có hiệu lực.
Bước tiếp theo: sau restart → xin tài khoản dev → login dev → chụp ảnh màn form-templates (danh sách, bộ lọc nâng cao, builder tạo mới, popup Tạo nhanh, xem trước, xem chi tiết, popup khóa/xóa) → dựng lại HDSD_PhieuThuThapThongTin.docx.
Blocked: cần tài khoản dev (isolated không giữ login).

## Checkpoint — 2026-07-17 (cài LibreOffice + sửa layout Mục lục / Danh mục hình ảnh)
Vừa hoàn thành:
- Cài LibreOffice 26.2.4 (brew cask) + PyMuPDF → render 15 file ra PDF/ảnh soát layout thật.
- Phát hiện 6 file (dựng tay) bị Mục lục CHỈ 2 dòng + THIẾU hẳn mục "DANH MỤC HÌNH ẢNH" thật (chỉ có caption trong thân bài): KhachHang, LoaiChietKhau, NhomLinhVucKhachHang, PhieuThuThapThongTin, LinhVucKhachHang, NganHangCauHoiKhaoSat. Nguyên nhân: field TOC gốc malformed (thiếu fldChar end) + cache chỉ 2 entry; LibreOffice/Word chỉ đọc cache nên render thiếu. 4/6 file còn kèm lỗi "MỤC LỤC" tràn xuống đáy trang bìa (thiếu pageBreakBefore).
- Viết `scratchpad/rebuild_toc.py`: pageBreakBefore cho MỤC LỤC; thay field TOC cũ bằng cache đủ mọi Heading1/Heading2 (dot leader + số trang); chèn heading "DANH MỤC HÌNH ẢNH" (clone MỤC LỤC giữ định dạng) + field ToF liệt kê mọi caption Hình (đánh số lại 1..N). Số trang lấy bằng 2-pass render (dò heading theo màu/cỡ chữ, dò caption theo thứ tự dòng "Hình N:").
- Áp dụng 6 file, verify render: cả 15 file KHÔNG bleed bìa, Mục lục đầy đủ, Danh mục hình ảnh đủ số hình + số trang khớp, ảnh nguyên vẹn. Backup trước sửa: `scratchpad/bak_toc/HDSD_*.bak.docx`.
Đang làm dở: (không)
Bước tiếp theo: (chờ user) — cân nhắc sửa phụ đề bìa HDSD_LoaiChietKhau "(Danh mục Loại chiết khấu)" → "Loại giảm giá" nếu menu UI đã đổi tên (cần xác nhận).
Blocked: (không)
