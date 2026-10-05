# Brief cho agent soạn config tài liệu danh mục (25/09/2026)

Mục tiêu: với mỗi `slug` được giao, viết **`.plans/gop-db/catalog-docs-v2/configs/<slug>.py`** (biến `CFG`) — từ đó bộ công cụ tự dựng HDSD + SRS (Word) và script sửa tab testcase online. Agent KHÔNG chụp ảnh, KHÔNG đụng Google Sheet/Drive, KHÔNG sửa code dự án, KHÔNG commit.

## Đọc trước (bắt buộc)
1. `configs/areas.py` — **MẪU CHUẨN**, đã được duyệt. Bám đúng tên key, cấu trúc, giọng văn, độ chi tiết.
2. `_catalog_docs_lib/catalog_v2.py` — chuỗi `SCHEMA` + hàm `build_hdsd`/`build_srs` để biết key nào bắt buộc/tuỳ chọn (vd `phan_rieng`, `menu_them`, `bang_them`, `ghi_chu_layout`).
3. `tc_gen.py`, `tc_ops.py` — cách sinh nhóm testcase Xuất Excel / Import và cấu trúc `CFG['tc']`.
4. `<slug>/ref/` — bản dump HDSD cũ, SRS cũ và **tab testcase hiện tại** (`testcase_tab.txt`, mỗi dòng `R<số hàng thật trên sheet>: A=… ;; B=…`).
5. Code nhánh gop_db (nguồn sự thật): FE `/Users/manhcuong/Desktop/dns/HRM/worktrees/gop_db-client` (pages/, components/), BE `/Users/manhcuong/Desktop/dns/HRM/worktrees/gop_db-api` (Modules/, app/). Không đọc vendor/node_modules.

## Quy tắc nội dung
- **Không ghi URL** ở bất kỳ đâu. Chỉ ghi đường bấm menu (`CFG['menu']` = 3 cấp: phân hệ, nhóm, mục — đúng chữ trên menu thật).
- Chữ UI, tên nút, thông báo, message validate: **lấy nguyên văn từ code** (FE + BE + lang file `hrm-api/resources/lang/vi/validation.php`, `hrm-client/locales/vi.json`).
- Mô tả **đúng hành vi hiện tại của code**. Nếu thấy lỗi (vd cột xuất rỗng, bộ lọc không áp vào file xuất) → tài liệu tả đúng thiết kế dự kiến nhưng ghi lỗi vào `CFG['loi_code']` (list chuỗi) để báo user; KHÔNG sửa code.
- Giữ lại nội dung nghiệp vụ đúng của tài liệu cũ (mục đích, thuật ngữ, quy tắc) — chỉ cập nhật phần đã đổi: **quy tắc tạo mã, Import, Xuất Excel, giao diện mới** (bộ lọc nhãn nổi, nút ba chấm, cấu hình cột, cửa sổ Chọn trường xuất file, cửa sổ Import có Validate/Bỏ dòng lỗi…).
- Số dạng quốc tế `1,234,567.89`; ngày `dd/mm/yyyy`.
- Màn không có chức năng nào (vd không có Import, không có Khoá) → bỏ key tương ứng, đừng bịa.
- Màn dạng TRANG RIÊNG (không phải popup) → ghi `CFG['form_type'] = 'page'` và mô tả đúng.

## Key `CFG['capture']` (tham số chụp ảnh — mình chạy)
```
{'route': '/human/areas', 'menu': {'phanhe': 'DANH MỤC', 'nhom': 'Địa lý', 'muc': 'Khu vực'},
 'search': '<tiền tố placeholder ô tìm nhanh>', 'searchText': '<chữ có kết quả>', 'detailCol': <chỉ số td chứa link xem chi tiết, 0-based>,
 'lockName': '<tên 1 bản ghi mẫu để khoá>' (bỏ nếu không có khoá), 'codeInput': '<placeholder ô mã>' (nếu có ô mã nhập tay),
 'create': True/False, 'lock': True/False}
```
`phanhe` = chữ in hoa ở đầu sidebar (vd `DANH MỤC`, `CSKH SAU BÁN`, `TÀI CHÍNH`) — tra `components/subsystems.js` / file menu FE.
`shots` dùng đúng tên file mà capture sinh ra: list `01_list.png` · rowmenu `03_rowmenu.png` · filter `filter.png` · filter_result `04_filter_result.png` · create `10_create.png` · create_error `11_create_error.png` · code_error `11b_code_error.png` · edit `12_edit.png` · delete `13_delete.png` · lock `14_lock.png` · unlock `15_unlock.png` · history `16_history.png` · detail `17_detail.png` · export `20_export.png` · import_open `21_import_open.png` · import_loaded `22_import_loaded.png` · import_validated `23_import_validated.png` · colcfg `25_colcfg.png`. Chỉ khai ảnh của chức năng có thật.

## Key `CFG['import_test']` (nếu màn có Import)
`{'rows': [[giá trị theo đúng thứ tự cột của file mẫu], ...]}` — 6–8 dòng: vài dòng hợp lệ (tên có tiền tố `DOC-` để dễ nhận) + mỗi loại lỗi chính 1 dòng (bỏ trống bắt buộc, trùng trong file, trùng hệ thống, tham chiếu không tồn tại, mã sai định dạng…). Ghi cả `'cols': [tên cột]` lấy từ code sinh file mẫu (FE `buildImportTemplate` / BE template).

## Key `CFG['tc']` — sửa tab testcase (QUAN TRỌNG, đọc kỹ)
Quy tắc user chốt:
- **Sửa THẲNG vào case đã có** liên quan tới **mã (quy tắc tạo mã), Import, Xuất Excel**: sửa ô Chức năng (D) / Tiền điều kiện (F) / Bước (G) / Test data (H) / Expected (I). Ghi vào `edits` = `[('I52', 'nội dung MỚI đầy đủ của ô'), ...]` theo **số hàng thật** (số sau chữ R). Xuống dòng trong ô dùng `\n`. Giữ văn phong cũ, chỉ đổi phần sai.
- **Mọi hàng đã sửa** → thêm số hàng vào `clear_k` (xoá "DNS check lần 1" để tester test lại).
- Chức năng **chưa có case nào** (thường là Import; Xuất Excel nếu tab chưa có) → thêm NHÓM MỚI ngay sau case cuối của nhóm cuối cùng (trước các dòng ghi chú review màu vàng ở cuối tab): `{'after': <hàng case cuối>, 'groups': [('VIII', 'XUẤT EXCEL (bổ sung 25/09/2026)', 8, 'export'), ('IX', 'IMPORT TỪ FILE EXCEL (bổ sung 25/09/2026)', 9, 'import')]}` — số La Mã / chỉ số TC nối tiếp nhóm cuối. `'export'`/`'import'` tự sinh case từ `CFG['xuat']`/`CFG['import']` (+ `import_rows_dung`, `import_loi_data`, `export_theo_loc`, `export_extra`, `import_extra` — xem `tc_gen.py`).
- Tab **đã có** nhóm Import → KHÔNG thêm nhóm Import; chỉ sửa case cũ nếu sai so với code. Đã có Xuất Excel → sửa các case đó theo giao diện mới (cửa sổ “Chọn trường xuất file”, tên file, cột), KHÔNG thêm nhóm mới.
- Case MỚI thuộc nhóm đã có (vd quy tắc mã mới: định dạng mã, tự in hoa, mã tự sinh, trùng mã) → chèn vào **cuối đúng nhóm đó**: `{'after': <hàng case cuối nhóm>, 'merge_from': <hàng case đầu nhóm>, 'cases': [('TC_03.010', Chức năng, 'P0', Tiền điều kiện, Bước, Test data, Expected), ...]}` — TC ID nối tiếp.
- `hdr_row` = số hàng của 1 dòng tiêu đề nhóm có sẵn (dòng chỉ có cột C kiểu "VII. …").
- Ngoài phạm vi (mã/import/export) thì KHÔNG sửa, kể cả thấy sai — ghi vào `CFG['tc_ngoai_pham_vi']` (list chuỗi) để báo user.
- Không ghi URL trong case.

## Tự kiểm trước khi trả
```
cd /Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/catalog-docs-v2
python3 -c "import sys; sys.path.insert(0,'../_catalog_docs_lib'); from catalog_v2 import load_cfg; c=load_cfg('<slug>'); print(sorted(c))"
python3 tc_ops.py <slug>      # phải in được các khối chèn, không lỗi
```
Trả về: danh sách file đã viết, tóm tắt thay đổi testcase (số edits, số case/nhóm thêm), `loi_code`, `tc_ngoai_pham_vi`, và mọi điểm KHÔNG chắc cần mình kiểm trên màn hình.
