# Plan — Chuẩn hoá màn Danh sách ứng dụng theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db`

## Phase 1 — Backend (`hrm-api`)

- [x] 1.1 `ApplicationService::SORTABLE_COLUMNS` — mở whitelist cho Mã / Tên / Ngày tạo / Ngày cập nhật (trước chỉ có `updatedAt`), chốt `id desc` cuối
- [x] 1.2 Subquery `creator_name` / `updater_name` (chỉ TÊN, không kèm mã NV, không leftJoin)
- [x] 1.3 Ô tìm nhanh tìm thêm theo **người tạo** bằng `EXISTS`
- [x] 1.4 `ApplicationsResource` — thêm `status_text`, `creator_name`, `updater_name`; ngày đổi sang `d/m/Y H:i`
- [x] 1.5 `ExportColumnRegistry::COLUMNS['applications']` (12 cột) + `ApplicationsController::export()` dùng `DynamicExport`

## Phase 2 — Frontend

- [x] 2.1 `V2BaseSmartFilterPanel` + schema `filterFields` 9 ô, bỏ `title`/`subtitle`, placeholder chuẩn
- [x] 2.2 `ignoredFields` computed dùng `textFilterKeys()`
- [x] 2.3 Tách cột `appCode` (button `.v2-cell-link` mở modal Xem, sticky+locked) / `appName`
- [x] 2.4 Cột `actions` cuối bảng + `V2BaseRowActions`; bỏ "Xem"; ẩn nút thay vì disable
- [x] 2.5 Nút Khóa/Mở khóa rời khỏi ô Trạng thái vào menu `⋮`; lý do bị chặn đưa vào `title` badge
- [x] 2.6 Trạng thái dùng `V2BaseBadge` (bỏ `v-html` + `status-pill` + `renderStatus`)
- [x] 2.7 Cột Người tạo / Ngày tạo / Người cập nhật / Ngày cập nhật riêng; mặc định hiện 7 cột + ô chọn
- [x] 2.8 `columnCustomizationMixin` + `ColumnCustomizationModal` (màn chưa từng có)
- [x] 2.9 `exportFieldsMixin` + `ExportFieldsModal` + `$safeLoading` (cả trong luồng import)
- [x] 2.10 `filterStateMixin` + `mergeKnownFilters`; giữ link `?scope_id=` / `?industry_id=`, áp SAU bộ lọc đã lưu
- [x] 2.11 `loadData()` chạy đầu tiên, 4 request danh mục hoãn tới khi mở panel lọc
- [x] 2.12 Bỏ `—`, căn lề + width theo bảng quy tắc; ô chọn sticky cùng nhóm STT / Mã
- [x] 2.13 Button theo `button-convention`: Import cam + `ri-upload-line`, Xuất xanh lá, `:interactable` thay `:disabled`, "Xóa nhiều" đổi `danger` → `primary status="danger"`, chữ `Khóa`/`Mở khóa`/`Xóa`
- [x] 2.14 Lệnh GHI (Xóa, Xóa nhiều, Khóa/Mở khóa) bọc `$safeLoadingStart()` + `$safeLoadingFinish()` trong `finally`

## Phase 3 — Kiểm chứng

- [x] 3.1 Compile FE + dò identifier template bằng AST (bộ dò cũ dùng regex `_vm.` là VÔ HIỆU với output của `vue-template-compiler` — đã viết lại, kiểm chứng bắt được lỗi thật)
- [x] 3.2 Smoke test API: index / sort theo `appCode` / keyword theo người tạo / export
- [x] 3.3 Đối chiếu khoá cột bảng ↔ cột file ↔ registry BE (12 = 12)
- [ ] 3.4 User mở trình duyệt kiểm tra

### Checkpoint — 2026-09-05
Vừa hoàn thành: toàn bộ Phase 1-2, kiểm chứng 3.1-3.3.
Bước tiếp theo: user kiểm tra trên trình duyệt.
Blocked: không có.

## Lỗi tự phát hiện trong lúc làm

`eventHandler()` / `handleCloseModal()` (2 hàm của modal Thêm/Sửa) suýt bị mất khi tách khối import —
bộ dò identifier cũ KHÔNG bắt được vì `vue-template-compiler.compile()` trả render dùng `with(this)`,
identifier để trần chứ không có tiền tố `_vm.` như regex đang tìm. Đã viết lại bộ dò bằng AST
(bỏ key của object + `.prop`, cộng whitelist tên do mixin cung cấp) và thử nghiệm xác nhận bắt được lỗi.

## Cập nhật 2026-09-05 — MẶC ĐỊNH HIỆN HẾT CỘT (user chốt)

- [x] Bỏ toàn bộ `isVisible: false` trong `allColumns` — vào màn là thấy đủ cột, ai thấy rộng quá
      thì tự tắt bớt ở popup "Cấu hình cột hiển thị" (cấu hình lưu riêng theo từng người).

⚠️ Đây là **ngoại lệ có chủ ý** so với `list-page` mục 6 (mặc định 7 cột). Lệnh user thắng skill;
skill vẫn ghi luật cũ nên muốn đổi thì phải qua PR (CLAUDE.md: skill là tài sản chung).

- [x] Nới bề rộng 4 cột nội dung dài: Nhóm ngành 200→220px · **Nhóm giải pháp 240→340px** ·
      **Loại hình hoạt động KH 220→280px** · **Lĩnh vực kinh doanh KH 240→340px** — 3 cột sau chứa
      nhãn GHÉP CẶP ("Nhóm ngành : Nhóm giải pháp", "Loại hình : Lĩnh vực") nên dài hơn hẳn cột thường,
      lại càng dễ bị bóp khi bảng hiện hết cột.

## Cập nhật 2026-09-05 (2) — Áp mục 15b của skill `list-page` (bề rộng cột)

Skill vừa được bổ sung **mục 15b "Bề rộng cột — màn nhiều cột, có cả chữ dài lẫn chữ ngắn"** (chốt
cùng ngày) sau khi tôi đọc skill lần đầu → lần chỉnh bề rộng trước đó (đoán tay từng cột) là SAI cách.

- [x] Bật prop `fixed-layout` trên `V2BaseDataTable`
- [x] Khai `width` + `minWidth` cho **đủ mọi cột** theo 4 bậc S (130-150) · M (170-190) · L (220-260) · XL (300)
- [x] Cột chữ dài dùng `cellClass: 'text-wrap clamp-2'` + `:title` trên thẻ trong slot (kẹp 2 dòng, hover xem đủ)
