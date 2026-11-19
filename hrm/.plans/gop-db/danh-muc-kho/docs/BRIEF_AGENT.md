# Brief — Xuất SRS + HDSD + Testcase cho 7 danh mục kho (phân hệ Kho → Danh mục)

Làm bằng tiếng Việt. Repo `d:\CompanyProject\hrm`. KHÔNG commit git, KHÔNG upload Drive, KHÔNG sửa code app
(`hrm-api`, `hrm-client`). Thấy code lệch nghiệp vụ / lỗi thì GHI VÀO BÁO CÁO, không tự sửa.

Tài liệu viết cho **HRM** theo **code hiện tại** (nhánh `develop` — repo chính đang ở `feat/chuyen-xe-cho-hang` đã chứa
code kho). KHÔNG tham chiếu ERP, KHÔNG mô tả hành vi ERP. Testcase cũ được viết lúc còn đối chiếu ERP → phải rà lại.

## 7 màn

| slug (thư mục) | Màn | Route FE | Dòng sheet Checklist |
|---|---|---|---|
| warehouses | Danh mục kho vật lý | `/warehouse/warehouses` | 259 |
| accounting-warehouses | Danh mục kho kế toán | `/warehouse/accounting-warehouses` | 260 |
| houses | Danh mục nhà kho | `/warehouse/houses` | 261 |
| rows | Danh mục dãy | `/warehouse/rows` | 262 |
| spaces | Danh mục khoang | `/warehouse/spaces` | 263 |
| positions | Danh mục vị trí | `/warehouse/positions` | 264 |
| packages | Danh mục kiện | `/warehouse/packages` | 265 |

Menu: **Phân hệ Kho => Danh mục => <tên màn>** (`hrm-client/components/subsystem-menu/warehouse.js`). Quyền duy nhất:
**"Quản lý kho"** (xem + ghi cả 7 màn). Code: FE `hrm-client/pages/warehouse/<slug>/` (index + Add*Modal),
mixin `vehicleCatalogScreenMixin`/`vehicleCatalogModalMixin`; BE `hrm-api/Modules/MasterData/*/Warehouse/`,
`WarehouseCatalogScope`, `WarehouseTreeCatalogController`. Nghiệp vụ + quyết định đã chốt: `../design.md`, `../plan.md`
(đọc hết, kể cả mục 28/10 về #11810 "Số nhà kho").

## Đầu ra — `danh-muc-kho/docs/<slug>/`
- `SRS - <Tên màn>.docx` (vd `SRS - Danh mục kho vật lý.docx`)
- `HDSD_<Tên màn>.docx` (vd `HDSD_Danh mục kho vật lý.docx`)
- `testcase - <Tên màn>.xlsx` (form 17 cột)
- `out/*.pdf` bản xem nhanh của SRS + HDSD
- script sinh (`gen_srs.py`, `gen_hdsd.py`, `gen_testcase.py`, `capture.js`) — ảnh để trong `shots/`, `uml/`, `icons/`
  (chỉ local, đã bị gitignore theo mẫu `*_shots`… → đặt tên thư mục ảnh là `hdsd_shots/` cho chắc)

## Khuôn — form "Danh mục quốc gia" (TPE đã duyệt)
- ĐỌC KỸ trước: `../../phieu-theo-form-quoc-gia/CHECKLIST.md` (góp ý TPE — áp hết phần SRS + HDSD),
  `hrm-claude-config/hrm/.claude/skills/srs-documenter/SKILL.md`, `hdsd-documenter/SKILL.md` (bản GỌN),
  `testcase-documenter/SKILL.md`, `../../catalog-docs-v2/SRS_UI_EVENTS_BRIEF.md` (mọi chức năng phải đủ 2 bảng
  "Mô tả chi tiết giao diện" + "Danh sách event").
- File khuôn: `../../geo-catalogs-docs/SRS - Danh mục quốc gia.docx`, `../../geo-catalogs-docs/HDSD_Danh mục quốc gia.docx`;
  HDSD gọn: `hrm-claude-config/hrm/.claude/skills/hdsd-documenter/assets/HDSD_MAU_GON.docx`.
- Thư viện dựng sẵn (team viết trên macOS, tái dùng được): `../../_catalog_docs_lib/catalog_v2.py` + `qg_writer.py` (SRS từ
  config, mẫu config `../../catalog-docs-v2/configs/districts.py` / `provinces.py` — danh mục có cha + Khoá/Mở khoá + Lịch sử
  + Xuất Excel), `../../_catalog_docs_lib/hdsd_gon.py` (HDSD gọn, mẫu `../../catalog-docs-v2/provinces/gen_hdsd_gon.py`).
  Lưu ý chạy trên Windows: `catalog_v2` đặt ROOT/TPL/ICONS cố định vào `catalog-docs-v2/` (thư mục `templates/`, `icons/`
  KHÔNG có trên máy này) và `finalize()` gọi Word **macOS**. KHÔNG sửa 2 file lib dùng chung — viết wrapper riêng trong
  `docs/` (vd `docs/_lib_win.py`: trỏ lại ROOT/TPL/ICONS, thay `finalize` bằng `word_finalize.ps1`) hoặc gọi `QgWriter`
  trực tiếp. Bị kẹt thì có thể dựng theo khuôn `../../phieu-theo-form-quoc-gia/formqg_lib.py` + `hdsd_phieu_lib.py`.
- Cập nhật mục lục / số trang / bỏ font nhúng / xuất PDF: `powershell -File ../../phieu-theo-form-quoc-gia/word_finalize.ps1
  -Docx <abs.docx> -Pdf <abs.pdf>`. Word mở riêng, chỉ đóng đúng PID của mình; KHÔNG kill Word theo tên.
- Use Case: vẽ PNG bằng `hrm-claude-config/hrm/.claude/skills/srs-documenter/assets/srs_uml_render.py` (≥1700px). Tổng quan có
  «extend» cho Tìm kiếm-lọc / Tùy chỉnh cột vào Xem danh sách; sơ đồ riêng CHỈ cho chức năng thao tác + Xem chi tiết
  (tác nhân → 1 use case). Tên use case là cụm động từ. Tên sơ đồ `Use Case Diagram – Quản lý danh mục <X>`.
- Định dạng: Times New Roman, H1 18pt căn giữa sang trang mới, mọi chữ khác 13pt KỂ CẢ trong bảng.
- KHÔNG ghi URL. Đường dẫn: "Menu: Phân hệ Kho => Danh mục => <màn>". Nhãn nút, tên cột, message lỗi, toast: NGUYÊN VĂN theo
  code. Tài liệu không dùng thuật ngữ code (không tên bảng, API, status = 1…).
- SRS có Phần 5 "Bảng màn hình tham chiếu dữ liệu" (STT | Nhóm | Màn hình | Đường dẫn): màn HRM THẬT SỰ đọc dữ liệu danh
  mục này (grep code FE/BE: vd ô chọn kho ở Phiếu nhập kho, Kế hoạch kiểm kê…). Không bịa.
- HDSD gọn: Bìa · MỤC LỤC · TỔNG QUAN (Thuật ngữ · Cập nhật tài liệu: 1.0 | 02/11/2026 | Đội phát triển phần mềm | Phát hành
  lần đầu · Quyền sử dụng · Sơ đồ chức năng tổng quan) · PHẦN 1 TRUY CẬP VÀ TÌM KIẾM · mỗi chức năng 1 PHẦN. Chỉ "Bước n" +
  icon nút inline + 1 ảnh/chức năng; Thêm mới nêu trường bắt buộc / tùy chọn + định dạng.

## Testcase
- Có sẵn bản cũ: `../testcase/gen_testcase_<tên>.py` + `.xlsx` (engine `hrm-claude-config/hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`,
  form 17 cột). Chép generator sang `docs/<slug>/gen_testcase.py` rồi RÀ LẠI từng case theo code hiện tại: menu/route mới
  (phân hệ Kho), nhãn/thông báo nguyên văn, bỏ mọi case/câu chữ về ERP hoặc gọi thẳng API, thêm case cho chức năng code có mà
  TC thiếu, bỏ case chức năng không còn. Giọng tester, không emoji, không thuật ngữ code. Cột kết quả/check để trống.
- Ghi trong báo cáo: số case giữ / sửa / thêm / bỏ.

## Chụp ảnh — dev-hrm, headless riêng (KHÔNG dùng Playwright MCP, KHÔNG dùng local)
- `const { openDev, DEV } = require('D:/CompanyProject/hrm/hrm-claude-config/hrm/.plans/gop-db/phieu-theo-form-quoc-gia/pw_dev.js');`
  `const { browser, page } = await openDev('<abs docs/<slug>>');` — chạy bằng `C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe`.
- Trước hết kiểm dev đã có màn (menu Kho => Danh mục) và tài khoản có quyền đủ nút (Tạo mới, Sửa, Khoá, Xoá, Lịch sử, Xuất
  Excel). Thiếu màn / thiếu quyền → DỪNG, báo lại, đừng chụp ảnh thiếu nút.
- AN TOÀN: dev là dữ liệu dùng chung — TUYỆT ĐỐI không bấm xác nhận Lưu / Xoá / Khoá / Mở khoá / Import. Mở popup → chụp →
  Đóng/Huỷ. Hộp xác nhận: chụp có nội dung rồi bấm Huỷ. Lịch sử: chọn bản ghi CÓ lịch sử.
- Chờ dữ liệu nạp (networkidle + có dòng), chuột ra (5,5), rồi chụp. Icon nút cắt từ UI vào `icons/` +
  `hrm-claude-config/hrm/.claude/skills/hdsd-documenter/assets/trim_icon.py` (`--dry` phải ra Cần cắt 0/N).
- XEM LẠI mọi ảnh bằng tool Read.

## Python / Node
- Python có python-docx, openpyxl, Pillow: `/c/Users/Legion/AppData/Local/Microsoft/WindowsApps/python3` (đặt
  `PYTHONIOENCODING=utf-8`). Tên file có `/` thì thay bằng `-`.

## Tự kiểm trước khi báo xong
- Render PDF, XEM bằng Read ít nhất: bìa, mục lục, 1 chức năng Thêm mới, 1 hộp xác nhận, Phần 4, Phần 5 (SRS); bìa, tổng quan,
  Phần 1, Thêm mới (HDSD).
- Mục lục đã cập nhật (không còn chữ "quốc gia" của khuôn: assert trong generator), font chỉ Times New Roman, cỡ chữ mọi run
  trong bảng = 13.
- Báo cáo cuối: đường dẫn 3 file + số trang, số TC (giữ/sửa/thêm/bỏ), danh sách điểm code lệch nghiệp vụ / nghi lỗi, chỗ
  nào chưa chắc.

## Bổ sung sau màn mẫu (user duyệt 02/11/2026)
- MÀN MẪU ĐÃ DUYỆT: `docs/warehouses/` — CHÉP KHUÔN Y HỆT (5 script: `capture.js`, `make_import_test.py`, `gen_srs.py`,
  `gen_hdsd.py`, `gen_testcase.py`) + thư viện chung `docs/_lib_win.py`, `docs/_capture_login.js`. Chỉ đổi khối dữ liệu
  và phần riêng của màn. KHÔNG sửa `_lib_win.py` / `_capture_login.js` / file trong `warehouses/` (agent khác dùng song song);
  cần thêm thì viết trong thư mục màn của mình.
- Dev không có bản ghi có lịch sử → được dùng ảnh Lịch sử giả lập trên trình duyệt như màn mẫu (`mockHistory`), user đã chấp nhận.
- Phần 5 SRS: giữ HẾT các màn có đọc/dùng dữ liệu danh mục (kể cả màn chỉ chọn để xem), theo form mẫu.
