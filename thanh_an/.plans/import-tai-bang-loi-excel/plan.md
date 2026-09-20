# Tải bảng thông báo lỗi import về Excel — @khoipv

## Bối cảnh
Modal import Excel hiện chỉ hiện bảng lỗi trên màn hình (STT / Dòng / Lỗi), không copy ra ngoài được.
Bổ sung nút "Tải bảng lỗi (Excel)".

## Quyết định chốt với user
- Phạm vi: sửa thẳng component **dùng chung** `components/modal/import-excel-modal.vue`
  → mọi màn dùng modal này đều có nút (Khách hàng, Hàng hóa, Nhân viên, Chấm công, Bảng giá, Thu nhập khác…)
- Nội dung file: **3 cột** đúng như bảng đang hiển thị (STT / Dòng / Lỗi), không kèm dữ liệu gốc
  (sheet Khách hàng 15 cột vs sheet Người phụ trách 4 cột → kèm vào sẽ lệch cột)
- Xuất **client-side** bằng ExcelJS (đã có sẵn trong `package.json`, pattern giống `AdditionalInfo.vue`)
  → không cần API mới, không đụng BE

## Phase 1 — FE
- [x] Thêm nút "Tải bảng lỗi" phía trên bảng lỗi, chỉ hiện khi có dòng lỗi
- [x] Đồng bộ style nút theo repo (`b-button variant="secondary"` + `fas fa-file-excel`, size mặc định như nút "Xuất excel" ở màn Khách hàng/Hàng hóa); hàng nút dùng `justify-content-between`: trái là nhãn đỏ "Có N dòng lỗi:", phải là nút; đang xuất thì icon đổi thành `b-spinner small type="grow"`
- [x] Method `exportErrorExcel()` — ExcelJS dynamic import, header xanh + border + freeze dòng 1, `wrapText` để lỗi nhiều dòng không bị mất
- [x] Method `errorFileName()` — `loi-import-<loai-du-lieu>_<ngay-gio>.xlsx`, map tên tiếng Việt theo `type`
- [x] Chống bấm liên tục bằng `isExportingError`, reset khi đóng modal

## Phase 2 — BE
Không có.

## Verify (chạy thật, 9/9 PASS)
- Template compile bằng `vue-template-compiler`: không lỗi
- Xuất file `.xlsx` thật (7144 bytes) rồi đọc lại bằng ExcelJS: đúng header, đúng 3 dòng lỗi, `wrapText = true`,
  lỗi nhiều dòng (`\n`) giữ nguyên, freeze header, tên file đúng định dạng, cờ `isExportingError` trả về false

### Checkpoint — 2026-09-16
Vừa hoàn thành: toàn bộ Phase 1, file `components/modal/import-excel-modal.vue` (+116 dòng, 0 dòng xóa, giữ CRLF).
Đang làm dở: không có.
Bước tiếp theo: build lại client + hard refresh → import file lỗi để test nút tải.
Blocked:
