# Brief chung — sửa SRS + HDSD màn phiếu theo form "Danh mục quốc gia"

Làm bằng tiếng Việt. Repo `d:\CompanyProject\hrm`. KHÔNG commit git, KHÔNG upload Drive, KHÔNG sửa code app.
Màn mẫu đã được user duyệt: **STT 27 Phiếu chuyển hàng nhập thẳng** — thư mục
`hrm-claude-config/hrm/.plans/gop-db/finance-product-import-direct-transfer/form_qg/`
(`patch_srs.py`, `gen_hdsd.py`, `out/*.docx|pdf`). CHÉP KHUÔN TỪ ĐÂY, chỉ đổi khối dữ liệu + phần riêng của màn.

## Đầu vào mỗi màn
- `<feature>/form_qg_<STT>/drive_0710/SRS_Drive.docx` và `HDSD_Drive.docx` = bản Drive MỚI NHẤT (đã tải 28/10). Làm trên
  bản này, KHÔNG dựng SRS lại từ generator cũ (Drive có chỗ người khác sửa tay).
- Thư viện chung trong `.plans/gop-db/phieu-theo-form-quoc-gia/`: `CHECKLIST.md` (ĐỌC KỸ — góp ý TPE), `formqg_lib.py`
  (vá SRS, vẽ Use Case khổ quốc gia), `word_finalize.ps1` (mục lục/số trang/bỏ font nhúng/xuất PDF qua Word),
  `hdsd_phieu_lib.py` (HDSD gọn), `pw_dev.js` (trình duyệt headless riêng, đăng nhập sẵn dev-hrm), `mau/` (2 file mẫu quốc gia).
- Skill: `hrm-claude-config/hrm/.claude/skills/hdsd-documenter/SKILL.md` (bản GỌN) và `srs-documenter/SKILL.md`.
- Code: FE `hrm-client/pages/<route>/` + components; BE `hrm-api`; menu `hrm-client/components/subsystem-menu/*.js`.
- Python có python-docx/Pillow/pymupdf: `/c/Users/Legion/AppData/Local/Microsoft/WindowsApps/python.exe`.
- Node: `C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe`.

## SRS — vá bản Drive (script `form_qg_<STT>/patch_srs.py` → `form_qg_<STT>/out/<tên file Drive gốc>.docx`)
Áp HẾT checklist + các điểm đã làm ở màn 27:
- Đường dẫn "Đường dẫn màn hình: / Menu: Phân hệ ... => ..." đúng menu thật (đối chiếu file menu), không URL; câu
  "Modal ... được mở ngay trên màn hình <đúng màn mở popup> theo đường dẫn ở trên." cho mọi popup.
- Use Case: bỏ sơ đồ riêng ở Cài đặt bộ lọc / Tùy chỉnh cột / Tìm-lọc / Lịch sử / Xem DS; CÓ sơ đồ cho Xem chi tiết và
  mọi chức năng thao tác. Vẽ lại kiểu quốc gia (tác nhân → 1 use case, không include/extend) đồng loạt như màn 27.
  Số Hình + số mục con liên tục.
- Mọi dòng "Quy tắc chung: ..." có vế "Chỉ bổ sung quy tắc riêng của <màn>." (giữ hyperlink).
- Tác nhân ghi tên quyền; Điều kiện ban đầu dạng 1. Đăng nhập 2. Có quyền 3. Trạng thái phiếu; bước ghi lịch sử ở
  tạo/sửa/duyệt/từ chối/hủy; sự kiện phụ rời màn chưa lưu theo ĐÚNG hành vi code; câu "Nếu có lỗi kiểm tra → gửi thông
  báo lỗi theo quy tắc thông báo chung [link], không thực hiện bước After" ở event Lưu/Duyệt/Từ chối/Xóa/Hủy.
- Cột Loại / loại event chuẩn hóa như checklist (bỏ Keypress, Blur, Loading, Number, Modal, Text).
- Phần 4: câu dẫn mẫu quốc gia, BR liên tục, bỏ ý trùng quy tắc chung. Giữ quy tắc "thao tác xong quay về danh sách".
- THÊM Phần 5 (bảng STT | Nhóm | Màn hình | Đường dẫn): màn THẬT SỰ đọc/dùng dữ liệu phiếu (grep code). Không có thì ghi
  rõ trong báo cáo, không bịa. Thêm vào mục lục.
- **Sửa nội dung lệch với CODE HIỆN TẠI** (nhánh đang chạy dev / repo chính; KHÔNG theo nhánh `feat/phieu-theo-chuan-quoc-gia`):
  nút, nhãn, trường, bộ lọc, popup, có ghi lịch sử không... Ảnh cũ sai rõ ràng so với giao diện hiện tại thì thay bằng ảnh
  chụp mới (dùng chung bộ ảnh HDSD).
- Cập nhật mục lục bằng `word_finalize.ps1`; xuất PDF; render các trang đã sửa và XEM bằng tool Read.

## HDSD — dựng lại dạng GỌN (script `form_qg_<STT>/gen_hdsd.py` → `form_qg_<STT>/out/<tên file Drive gốc>.docx`)
- Khuôn y hệt HDSD màn 27: Bìa · MỤC LỤC · TỔNG QUAN (Thuật ngữ · Cập nhật tài liệu: giữ dòng cũ của bản Drive + thêm
  dòng 28/10/2026 "Chuyển sang form chuẩn", Người cập nhật = "Đội phát triển phần mềm" · Quyền sử dụng · Sơ đồ chức năng
  tổng quan) · PHẦN 1 TRUY CẬP VÀ TÌM KIẾM · mỗi chức năng 1 PHẦN. Chỉ "Bước n" + icon nút inline + 1 ảnh/chức năng;
  Thêm mới nêu rõ trường bắt buộc / tùy chọn. Không URL, không văn xuôi, không bảng trường, không phần vai trò/lỗi/lưu ý.
- Giữ ý nghiệp vụ quan trọng của bản cũ dưới dạng bước (vd "Không duyệt" chỉ lưu nháp...) nếu code vẫn vậy.

## Chụp ảnh — DEV, KHÔNG dùng local, KHÔNG dùng Playwright MCP
- `https://dev-hrm.eteksofts.com`, tài khoản `namdangit@gmail.com` / `2025Dns@2`. Dùng `pw_dev.js`:
  `const { openDev, DEV } = require('<abs>/phieu-theo-form-quoc-gia/pw_dev.js'); const { browser, page } = await openDev('<abs>/form_qg_<STT>');`
  Mỗi agent trình duyệt headless riêng → song song thoải mái. Viết script chụp `form_qg_<STT>/capture.js`.
- AN TOÀN: dev là dữ liệu dùng chung — TUYỆT ĐỐI không bấm xác nhận Lưu/Duyệt/Từ chối/Xóa/Hủy phiếu/Tạo phiếu.
  Mở form/hộp thoại → chụp → Đóng/Hủy. Cần nút Sửa/Xóa mà tài khoản không có phiếu đủ điều kiện thì tìm phiếu khác;
  không có thì chỉ bật tạm hiển thị trên trình duyệt (không ghi dữ liệu) như màn 27.
- Chờ dữ liệu nạp (đợi text mã phiếu / networkidle), chuột ra (5,5), rồi chụp. Ảnh `form_qg_<STT>/hdsd_shots/`,
  icon `hdsd_shots/icons/` + chạy `trim_icon.py` (`--dry` phải ra Cần cắt 0/N). Icon dùng lại được từ màn 27:
  `finance-product-import-direct-transfer/form_qg/hdsd_shots/icons/` (chỉ khi nhãn giống hệt).
- XEM LẠI ảnh bằng Read (ghép tấm). Lịch sử: chọn phiếu CÓ lịch sử.

## Word COM
Nhiều agent chạy song song → `word_finalize.ps1` mở Word riêng, chỉ đóng đúng PID của mình; lỗi RPC lúc Close thì thử lại
1 lần. KHÔNG kill Word theo tên.

## Kiểm + báo cáo cuối (ngắn, tiếng Việt)
- Render PDF mọi trang HDSD + các trang SRS đã sửa, xem bằng Read: không trang trắng, chú thích không tách ảnh, số
  Bước/Hình liên tục, mục lục không còn dòng mẫu.
- Báo cáo: file đầu ra + số trang; thay đổi chính; chỗ đã sửa theo code; lỗi app nghi ngờ (chỉ báo); câu hỏi cần chốt.
