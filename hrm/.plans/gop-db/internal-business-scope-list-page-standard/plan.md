# Plan — Chuẩn hoá màn Lĩnh vực Công ty kinh doanh theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db`

## Phase 1 — Backend (`hrm-api`)

- [x] 1.1 **Sửa bug 500**: `InternalBusinessScope::isCanLockUpdate()` viết cứng `scopes.status` → lấy tên bảng từ model (`hrm_scopes`)
- [x] 1.2 `getStatusTextAttribute()` đổi `Khoá` → `Khóa` theo bảng text chuẩn
- [x] 1.3 `ExportColumnRegistry::COLUMNS['internal_business_scopes']` (8 cột) + `export()` dùng `DynamicExport`, đuôi `.xlsx`
- [x] (Service đã chuẩn sẵn từ đợt trước: whitelist sort, tìm theo người tạo, xếp theo độ khớp, ngày `d/m/Y H:i`)

## Phase 2 — Frontend

- [x] 2.1 `V2BaseSmartFilterPanel` + schema `filterFields` 7 ô, placeholder chuẩn
- [x] 2.2 `ignoredFields` computed dùng `textFilterKeys()` — ô Mã / Tên chờ Enter
- [x] 2.3 Cột Hành động chuyển từ renderer `type: 'actions'` sang `V2BaseRowActions`
- [x] 2.4 Thêm cột **Số nhóm ngành** (BE đã trả `scopes_count`, bảng chưa hiện) — căn phải
- [x] 2.5 `columnCustomizationMixin` + `ColumnCustomizationModal` (màn chưa từng có)
- [x] 2.6 `exportFieldsMixin` + `ExportFieldsModal`; **giữ cách tải TRỰC TIẾP** (comment cũ: blob + `download` hỏng trên Safari/webview)
- [x] 2.7 `filterStateMixin` + `mergeKnownFilters`
- [x] 2.8 Mục 15b: `fixed-layout` + `width`/`minWidth` đủ 10 cột (1578px) + `clamp-2` + `:title`
- [x] 2.9 Button-convention: Import cam + `ri-upload-line`, Xuất xanh lá, `:interactable`, icon Xóa `ri-delete-bin-line`
- [x] 2.10 Lệnh GHI (Xóa, Khóa/Mở khóa) bọc `$safeLoading` trong `finally`
- [x] 2.11 Bỏ hết `—`; chữ về `Khóa` / `Xóa`

## Phase 3 — Kiểm chứng

- [x] 3.1 Compile FE + dò identifier template bằng AST
- [x] 3.2 Smoke test: gọi thẳng service + Resource + dựng file Excel (route trả 403 vì tài khoản test thiếu quyền "Xem danh mục lĩnh vực Công ty kinh doanh")
- [x] 3.3 Đối chiếu cột bảng ↔ cột file ↔ registry BE (8 = 8, 10 cột đủ width+minWidth)
- [ ] 3.4 User mở trình duyệt kiểm tra

⚠️ DB local chỉ có **1 bản ghi** (`LVKDNB.KHAC`) nên phần hiển thị nhiều dòng chưa kiểm chứng được.

### Checkpoint — 2026-09-05
Vừa hoàn thành: toàn bộ Phase 1-2, kiểm chứng 3.1-3.3.
Bước tiếp theo: user kiểm tra trên trình duyệt.
Blocked: không có.
