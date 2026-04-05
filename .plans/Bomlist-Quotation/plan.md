# Plan: Bomlist - Quotation

## Trạng thái
- Bắt đầu: 2026-03-28
- Tiến độ: Phase 1-5 done, Phase 6 (Test) pending

## Danh sách task

### Phase 1: Màn danh sách BOM List + Status + Delete
[x] Task 1-10: Hoàn thành

### Phase 1.5: Bổ sung trường mới + Permission + Filter
[x] Task 11-20: Hoàn thành

### Phase 2: Refactor logic lưu sản phẩm BOM
[x] Hoàn thành

### Phase 3: Xuất Excel
[x] Hoàn thành

### Phase 4: Import Excel
[x] Hoàn thành

### Phase 5: Trang chi tiết (view-only)
[x] Trang detail _id/index.vue — reuse BomBuilderEditor viewOnly
[x] Ẩn tất cả buttons thêm/sửa/xoá/kéo thả
[x] Editable fields → text thuần
[x] Fix sticky columns khi ẩn cột Thao tác
[x] Header card: người tạo + thời gian
[x] Footer bar fixed: button Sửa + Xuất Excel
[x] STT cấp con: lùi đầu dòng, font-weight normal
[x] Button Import chỉ hiện loại BOM Thành phần

### Phase 6: Test toàn bộ BOM List

#### 6.1 Màn danh sách
[ ] Truy cập /assign/bom-list — hiện danh sách đúng
[ ] Quick search theo Mã BOM, Tên BOM
[ ] Filter cascading: chọn Dự án → tự select Giải pháp → enable Hạng mục
[ ] Filter: Công ty, Phòng ban, Bộ phận, Người tạo, Trạng thái, Loại BOM, Ngày tạo
[ ] Phân quyền: user chỉ thấy BOM theo quyền (tất cả / công ty / phòng ban / bộ phận)
[ ] BOM Đang tạo chỉ hiện cho người tạo
[ ] Column customization: tuỳ chỉnh cột hiển thị
[ ] Pagination + sorting (ngày tạo, ngày cập nhật)

#### 6.2 Tạo BOM List
[ ] Tạo BOM loại Thành phần — Lưu nháp (status=1)
[ ] Tạo BOM loại Thành phần — Lưu (status=2)
[ ] Tạo BOM loại Tổng hợp — chọn BL con
[ ] Chọn Dự án → tự fill Giải pháp + Khách hàng
[ ] Thêm nhanh hàng hoá cha → thêm lần 2 không trùng code
[ ] Thêm nhanh hàng hoá con cho cha vừa tạo local
[ ] Chọn hàng hoá từ danh mục (PickModal) → copy data sang bom_list_products
[ ] Sửa hàng hoá trong BOM → KHÔNG thay đổi product_projects
[ ] Xoá hàng hoá cha/con
[ ] Kéo thả đổi thứ tự cha/con

#### 6.3 Sửa BOM List
[ ] Mở edit BOM Đang tạo — hiện cả Lưu nháp + Lưu
[ ] Mở edit BOM Hoàn thành — chỉ hiện Lưu (ẩn Lưu nháp)
[ ] BOM Chờ duyệt/Đã duyệt — form disabled, không sửa được
[ ] Sửa thông tin header (tên, ghi chú, loại BOM)
[ ] Sửa sản phẩm → save → reload đúng data

#### 6.4 Xoá BOM List
[ ] Xoá BOM Đang tạo (status=1) + created_by = user → thành công
[ ] Xoá BOM Hoàn thành (status=2) → không cho xoá
[ ] Xoá BOM của người khác → không cho xoá
[ ] Confirm modal hiện đúng thông tin

#### 6.5 Xuất Excel
[ ] Click icon xuất Excel trên row → hiện popup chọn cột
[ ] Chọn/bỏ chọn cột → Select all/deselect all
[ ] Checkbox xuất cấp con: bật → có hàng con, tắt → chỉ hàng cha
[ ] File Excel: header thông tin BOM đúng (tên, dự án, giải pháp, hạng mục, KH)
[ ] File Excel: font Times New Roman, auto-fit, số tiền format #,##0
[ ] File Excel: hàng cha bold background xanh, hàng con indent
[ ] Xuất từ trang chi tiết (footer bar) → hoạt động đúng

#### 6.6 Import Excel
[ ] Download template mẫu → file mở được, có header + dòng mẫu cha/con
[ ] Import file mẫu → preview đúng 2 dòng (cha + con)
[ ] Validate: thiếu tên → lỗi, thiếu model/brand/origin/uom/qty → lỗi
[ ] Validate: hàng cha thành tiền ≠ tổng con → cảnh báo
[ ] Import thành công → sản phẩm thêm vào BOM, reload đúng
[ ] Model/Brand/Origin/Unit chưa có trong DB → tự tạo mới
[ ] Mã hàng hoá không nhập → tự sinh
[ ] Phân biệt cha/con qua STT (1=cha, 1.1=con) → parent_id đúng
[ ] Button Import chỉ hiện ở loại BOM Thành phần

#### 6.7 Trang chi tiết (view-only)
[ ] Truy cập /assign/bom-list/{id} → hiện readonly
[ ] Không có buttons: Chọn hàng hoá, Import, Thêm nhanh, Sửa, Xoá, kéo thả
[ ] Không có cột Thao tác, không lệch layout
[ ] Editable fields hiện text thuần (qty, price, specification)
[ ] STT cấp con lùi đầu dòng, font-weight normal
[ ] Header card: hiện người tạo + thời gian
[ ] Footer bar fixed: button Sửa → navigate edit, button Xuất Excel → show modal
[ ] Bộ lọc header disable toàn bộ input/select

## Checkpoint
- 2026-03-28: Phase 1 done
- 2026-03-29: Phase 1.5 + 2 done
- 2026-03-29: Phase 3 + 4 done
- 2026-03-30: Phase 5 done
- Phase 6: Test — pending
