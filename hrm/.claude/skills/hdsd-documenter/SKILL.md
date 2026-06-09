---
name: hdsd-documenter
description: Generate tài liệu Hướng dẫn sử dụng (HDSD) Word cho màn hình/luồng nghiệp vụ — CỰC KỲ CHI TIẾT, click-by-click, đủ từng trường + giá trị mặc định, ảnh chụp thật
---

# HDSD Documenter — ERP TPE

## Mục đích
Tạo tài liệu **Hướng dẫn sử dụng (HDSD)** dạng **Word (.docx)** cho người dùng cuối, cho một màn hình hoặc một luồng nghiệp vụ. Output theo đúng format mẫu đã được duyệt (`HDSD_filemau.docx`), ảnh **chụp thật** từ hệ thống.

## Khi nào dùng
- User yêu cầu "viết tài liệu hướng dẫn", "viết HDSD", "hướng dẫn sử dụng màn …".
- Cần tài liệu bàn giao cho người dùng/đào tạo.

## ⚠️ NGUYÊN TẮC SỐ 1 — ĐẦY ĐỦ & CHI TIẾT TỐI ĐA
User đã chốt: HDSD phải **chi tiết tới từng hành động nhỏ nhất**. Liệt kê nút thôi là **CHƯA ĐỦ**. Với **mỗi nút điều hướng/mở popup** (Tạo mới, Sửa, Xem, Duyệt, Từ chối, Nhập kết quả, Xử lý, Xóa, In…) phải mô tả:
1. Bấm nút đó **mở ra màn/popup nào** (chụp ảnh thật màn đó).
2. **LIỆT KÊ TỪNG TRƯỜNG** nhập liệu: nhãn, loại control, **có bắt buộc không**, **giá trị điền sẵn/mặc định khi tạo mới**, điều kiện ẩn/hiện/khóa, dữ liệu cascading.
3. **Các nút lưu** và hành động (lưu gì, thông báo thành công, điều hướng đi đâu).
4. Trạng thái/kết quả sau thao tác.

→ Mỗi tab/màn có riêng các mục: **Tạo mới / Sửa / Xem / Duyệt / Nhập kết quả / Lịch sử / Xóa** (tuỳ màn có gì). Mục Tạo mới luôn có **bảng từng trường** + **box "Giá trị điền sẵn khi tạo mới"**.

Xem thêm memory: `feedback_hdsd_detail_level`, `reference_hdsd_format`, `reference_hdsd_luongchinh`, `reference_playwright_ui_test`.

## Quy trình (4 bước)

### Bước 1 — Khảo sát màn (đọc code)
- Đọc `index.vue` / page chính để biết các tab, các modal, các nút, API gọi.
- Dùng **agent Explore** quét toàn bộ component các tab/modal → liệt kê: hiển thị gì, cột bảng, nút (text+icon), nút mở modal/điều hướng gì, empty state, API endpoint.
- Hỏi user nếu cần: bỏ tab nào không, format (mặc định Word), ảnh chụp thật hay placeholder.

### Bước 2 — Chụp ảnh thật (Playwright MCP)
- Dùng **Playwright MCP (Node)** — KHÔNG dùng Playwright Python (đó là cho pytest harness). Tham khảo `reference_playwright_ui_test`.
- Login site (vd dev-hrm.eteksofts.com) bằng tài khoản user cung cấp → form `#emailaddress` (hoặc textbox "Địa chỉ email") + "Mật khẩu" + nút "Đăng nhập".
- **Ưu tiên tài khoản có dữ liệu thật ở mọi tab** để ảnh sát thực tế.
- Resize 1440x900. Mở từng tab, cuộn container nội dung lên đầu (`document.querySelector('.overflow-auto').scrollTop=0`) rồi chụp viewport; với form dài dùng `fullPage:true`.
- Chụp đủ: mỗi tab danh sách, bộ lọc nâng cao mở, các popup/modal (lọc, cấu hình cột, xác nhận xóa, xuất Excel chọn cột), **và đặc biệt các FORM Tạo mới/Sửa** mà nút mở ra.
- Mở form Tạo mới KHÔNG lưu là an toàn. Với Duyệt/Xóa: chụp hộp xác nhận rồi **bấm Hủy** (không thực thi trên dữ liệu thật).
- Lưu ảnh vào `hdsd_<feature>_shots/` (đặt tên có số thứ tự + mô tả). Đọc lại ảnh để kiểm tra chất lượng trước khi dùng.

### Bước 3 — Đi sâu form (đọc field + mặc định)
- Mỗi nút "Tạo mới" thường mở **màn/popup riêng của phân hệ** (vd `/assign/solutions/add`, `/assign/meeting/create`, `/assign/assign_business/add`) hoặc popup trong trang (Task, Issue dùng `CreateXxxModal.vue`).
- **Cử nhiều agent Opus đọc song song** (mỗi agent 1 form/nhóm form). Yêu cầu mỗi agent trả về cho từng mode (create/edit/view/approve/handle):
  - Tiêu đề; các tab/section.
  - **Từng trường**: nhãn (nguyên văn tiếng Việt), control, bắt buộc + message lỗi, **giá trị mặc định/điền sẵn** (lấy từ `data()` init, `created/mounted`, prefill query, vd `created_by`=người dùng, ngày=hôm nay, phòng=phòng user, trạng thái mặc định), điều kiện ẩn/hiện/readonly, cascading, nguồn options (API).
  - Nút + hành động (API, toast, điều hướng); khác biệt giữa các mode.
- Dùng Opus cho subagent (memory `feedback_subagent_model_opus`).

### Bước 4 — Dựng file Word (python-docx)
Theo `reference_hdsd_format` + `reference_hdsd_luongchinh`. Generator (python `/opt/homebrew/opt/python@3.14/bin/python3.14`, lib `python-docx` + `Pillow`):
1. **Copy 1 file catalog làm khung** (vd `HDSD_DanhMuc/HDSD_KhachHang.docx`): giữ Bìa + MỤC LỤC (TOC field) + DANH MỤC HÌNH ẢNH (TOF field) + styles + `updateFields=true`.
2. Sửa bìa `(Danh mục X)` → `(Màn hình: …)` / `(Luồng nghiệp vụ: …)`.
3. Lưu **proto Caption** (clone, có SEQ field auto-số): run0 "Hình " + SEQ + run2 ": <text>".
4. **Strip body** từ heading "TỔNG QUAN PHẦN MỀM" tới hết, GIỮ `sectPr` (luôn là child cuối của body).
5. Rebuild bằng helper H1/H2/H3 (style "Heading 1/2/3"), P (Normal justify), List Bullet, bảng style **Light Grid Accent 1**, ảnh căn giữa width ~6.0" (form dài để nguyên), caption qua `sectPr.addprevious(clone)`.
6. **Purge media mồ côi** sau khi strip (python-docx không xoá media khi xoá paragraph → file phình): quét `r:embed`/`r:link` trong document/header/footer → map qua `.rels` → bỏ media + Relationship không tham chiếu. (Bìa các file mẫu là text, purge an toàn.)
7. Bật `updateFields=true` để Word tự cập nhật mục lục/danh mục hình khi mở.
8. **Verify**: mở lại bằng python-docx, kiểm `inline_shapes`/`tables`/`captions`/`Heading 1` đúng số; quét mọi `r:embed` resolve được (broken=0).

## Cấu trúc tài liệu (bắt buộc)
Bìa → MỤC LỤC → DANH MỤC HÌNH ẢNH → **TỔNG QUAN PHẦN MỀM** (1. Thuật ngữ, 2. Cập nhật tài liệu, 3. Giới thiệu chung + đường dẫn, 4. Quyền & phạm vi) → **PHẦN 1: Truy cập & bố cục** → **mỗi tab/màn = 1 PHẦN**, trong đó:
- Ảnh tổng quan tab.
- Tìm kiếm & lọc (ô nhanh + bộ lọc nâng cao liệt kê từng tiêu chí).
- Các cột danh sách.
- Nút thanh công cụ (Tạo mới / Xuất Excel / Cấu hình cột…).
- Thao tác từng dòng (theo quyền & trạng thái).
- **Tạo mới** (ảnh form + bảng từng trường + box mặc định + nút lưu).
- **Sửa / Duyệt / Nhập kết quả / Xử lý / Lịch sử / Xóa** (mô tả khác biệt, ảnh nếu cần).

## Checklist độ đầy đủ (tự kiểm trước khi giao)
- [ ] Mỗi nút "Tạo mới" có ảnh form thật + bảng từng trường + cột "Bắt buộc" + cột "Giá trị mặc định".
- [ ] Đã ghi rõ giá trị điền sẵn (người tạo/người duyệt/người theo dõi/ngày/giờ/trạng thái/phòng ban…).
- [ ] Mỗi thao tác thay đổi dữ liệu (Sửa/Duyệt/Từ chối/Nhập kết quả/Xóa) đều được mô tả: mở ra gì, nhập gì, lưu thế nào, kết quả.
- [ ] Bộ lọc nâng cao liệt kê đủ từng tiêu chí.
- [ ] Ảnh chụp thật, rõ, đúng nội dung; caption đánh số tự động.
- [ ] File mở được, mục lục/danh mục hình tự cập nhật, không lỗi ảnh (broken=0).

## Output & lưu trữ
- File Word: `HDSD_luongchinh/HDSD_<TênMàn>.docx` (luồng/màn lớn) — hoặc theo vị trí user chỉ định.
- Ảnh nguồn: `hdsd_<feature>_shots/`.
- Generator: lưu trong scratchpad (ephemeral) — ghi lại cách chạy vào `.plans/[feature]/design.md` để tái dựng.
- Cập nhật `.plans/[feature]/plan.md` + `STATUS.md` theo convention.

## Lưu ý
- Tài liệu + ngôn ngữ: **tiếng Việt**, văn phong cho người dùng cuối.
- KHÔNG thực thi thao tác phá huỷ trên dữ liệu thật khi chụp (Duyệt/Xóa → bấm Hủy).
- Nếu màn tái sử dụng form của phân hệ khác (vd "Tạo mới" mở màn module khác) → vẫn mô tả đầy đủ trong HDSD này (đừng chỉ trỏ "xem màn khác").
