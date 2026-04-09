# Plan: Bomlist - Quotation

## Trạng thái
- Bắt đầu: 2026-03-28
- Tiến độ: Phase 1-6 done

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

### Phase 6: Test toàn bộ BOM List ✓

#### 6.1 Màn danh sách
[x] Truy cập /assign/bom-list — hiện danh sách đúng
[x] Quick search theo Mã BOM, Tên BOM
[x] Filter cascading: chọn Dự án → tự select Giải pháp → enable Hạng mục
[x] Filter: Công ty, Phòng ban, Bộ phận, Người tạo, Trạng thái, Loại BOM, Ngày tạo
[x] Phân quyền: user chỉ thấy BOM theo quyền (tất cả / công ty / phòng ban / bộ phận)
[x] BOM Đang tạo chỉ hiện cho người tạo
[x] Column customization: tuỳ chỉnh cột hiển thị
[x] Pagination + sorting (ngày tạo, ngày cập nhật)

#### 6.2 Tạo BOM List
[x] Tạo BOM loại Thành phần — Lưu nháp (status=1)
[x] Tạo BOM loại Thành phần — Lưu (status=2)
[x] Tạo BOM loại Tổng hợp — chọn BL con
[x] Chọn Dự án → tự fill Giải pháp + Khách hàng
[x] Thêm nhanh hàng hoá cha → thêm lần 2 không trùng code
[x] Thêm nhanh hàng hoá con cho cha vừa tạo local
[x] Chọn hàng hoá từ danh mục (PickModal) → copy data sang bom_list_products
[x] Sửa hàng hoá trong BOM → KHÔNG thay đổi product_projects
[x] Xoá hàng hoá cha/con
[x] Kéo thả đổi thứ tự cha/con

#### 6.3 Sửa BOM List
[x] Mở edit BOM Đang tạo — hiện cả Lưu nháp + Lưu
[x] Mở edit BOM Hoàn thành — chỉ hiện Lưu (ẩn Lưu nháp)
[x] BOM Chờ duyệt/Đã duyệt — form disabled, không sửa được
[x] Sửa thông tin header (tên, ghi chú, loại BOM)
[x] Sửa sản phẩm → save → reload đúng data

#### 6.4 Xoá BOM List
[x] Xoá BOM Đang tạo (status=1) + created_by = user → thành công
[x] Xoá BOM Hoàn thành (status=2) → không cho xoá
[x] Xoá BOM của người khác → không cho xoá
[x] Confirm modal hiện đúng thông tin

#### 6.5 Xuất Excel
[x] Click icon xuất Excel trên row → hiện popup chọn cột
[x] Chọn/bỏ chọn cột → Select all/deselect all
[x] Checkbox xuất cấp con: bật → có hàng con, tắt → chỉ hàng cha
[x] File Excel: header thông tin BOM đúng (tên, dự án, giải pháp, hạng mục, KH)
[x] File Excel: font Times New Roman, auto-fit, số tiền format #,##0
[x] File Excel: hàng cha bold background xanh, hàng con indent
[x] Xuất từ trang chi tiết (footer bar) → hoạt động đúng

#### 6.6 Import Excel
[x] Download template mẫu → file mở được, có header + dòng mẫu cha/con
[x] Import file mẫu → preview đúng 2 dòng (cha + con)
[x] Validate: thiếu tên → lỗi, thiếu model/brand/origin/uom/qty → lỗi
[x] Validate: hàng cha thành tiền ≠ tổng con → cảnh báo
[x] Import thành công → sản phẩm thêm vào BOM, reload đúng
[x] Model/Brand/Origin/Unit chưa có trong DB → tự tạo mới
[x] Mã hàng hoá không nhập → tự sinh
[x] Phân biệt cha/con qua STT (1=cha, 1.1=con) → parent_id đúng
[x] Button Import chỉ hiện ở loại BOM Thành phần

#### 6.7 Trang chi tiết (view-only)
[x] Truy cập /assign/bom-list/{id} → hiện readonly
[x] Không có buttons: Chọn hàng hoá, Import, Thêm nhanh, Sửa, Xoá, kéo thả
[x] Không có cột Thao tác, không lệch layout
[x] Editable fields hiện text thuần (qty, price, specification)
[x] STT cấp con lùi đầu dòng, font-weight normal
[x] Header card: hiện người tạo + thời gian
[x] Footer bar fixed: button Sửa → navigate edit, button Xuất Excel → show modal
[x] Bộ lọc header disable toàn bộ input/select

### Phase 7: Cập nhật theo yêu cầu khách hàng

#### 7.1 Popup "Thêm hàng hoá" gộp (thay PickModal + QuickCreateModal)
[x] Tạo BomBuilderAddProductModal.vue — 2 tab (Tìm có sẵn + Tạo mới)
[x] Tab 1: Search hàng ERP (erp2326.products) + hàng BOM hiện tại
[x] Tab 1: Filter theo Model, Thương hiệu, Xuất xứ
[x] Tab 1: Multi-select checkbox + nhập số lượng + badge nguồn (ERP/BOM)
[x] Tab 2: Form tạo mới dùng V2Base components (giữ style cũ)
[x] Tab 2: Validate từng field (Tên, Model, ĐVT, Thương hiệu, Xuất xứ) — hiện lỗi tại element
[x] Tab 2: Chọn nhóm hàng khi có groups
[x] API endpoint GET /erp-products — search products từ ERP
[x] API endpoint GET /{bomList}/bom-products — search products trong BOM
[x] Model TpProduct + TpProductUnit (mysql2 connection)
[x] Xoá BomBuilderPickModal.vue + BomBuilderQuickCreateModal.vue
[x] Load model options từ API (get-model)

#### 7.2 Cấp nhóm hàng (Grouping)
[x] Tạo bảng bom_list_groups (migration)
[x] Thêm bom_list_group_id vào bom_list_products (migration)
[x] Entity BomListGroup + relationships
[x] Button "Tạo nhóm" ở header → mở b-modal (không dùng prompt trình duyệt)
[x] Sửa nhóm → b-modal centered
[x] Xoá nhóm → BaseConfirmModal xác nhận
[x] Row nhóm hiển thị STT La Mã (I, II, III)
[x] STT hàng cha reset mỗi nhóm
[x] Button "Thêm hàng hoá" nằm trực tiếp trên row nhóm
[x] Mỗi nhóm expand/collapse (mũi tên + v-show)
[x] Hiển thị số lượng hàng mỗi nhóm
[x] Service syncGroups() + loadDetail() eager load groups
[x] Save payload: bom_groups[] + group_id per product

#### 7.3 Validate BOM tổng hợp
[x] Unique: 1 solution + module chỉ 1 BOM tổng hợp
[x] validateUniqueAggregate() trong BomListService
[x] Controller trả lỗi 422 nếu trùng
[x] SubBomModal: filter theo solution/module, exclude status nháp

#### 7.4 Đồng bộ hàng ERP
[x] Thêm erp_product_id vào bom_list_products (migration)
[x] syncErpFields() — re-fetch ERP data khi lưu BOM
[x] Mapping: name, code, model_id, brand_id, origin_id, product_attributes, unit_id

#### 7.5 Sửa lỗi / cải thiện
[x] Fix cột column_customizations thiếu bom_lists (migration)
[x] Fix API route 404 — đổi $axios sang $store.dispatch('apiGetMethod')
[x] Fix checkbox chọn hàng không reactive (bỏ computed copy, dùng mảng gốc)
[x] Đổi tên cột "Đặc điểm" → "Thông số kỹ thuật"
[x] Fix group modal lệch layout → dùng b-modal centered

#### 7.6 Test
[ ] Test tạo BOM với groups + hàng ERP + hàng tạo mới
[ ] Test edit BOM — groups + products load đúng
[ ] Test validate BOM tổng hợp unique
[ ] Test SubBom modal filter
[ ] Test expand/collapse nhóm
[ ] Test trang chi tiết view-only

## Checkpoint
- 2026-03-28: Phase 1 done
- 2026-03-29: Phase 1.5 + 2 done
- 2026-03-29: Phase 3 + 4 done
- 2026-03-30: Phase 5 done
- 2026-04-08: Phase 6 done — test passed

### Checkpoint — 2026-04-09
Vừa hoàn thành: Phase 7.1–7.5 code done, đã fix 5 vòng bug từ test user
Đang làm dở: Phase 7.6 — test thủ công (chưa hoàn thành, user wrap up)
Bước tiếp theo: Tiếp tục test Phase 7.6 → fix bug nếu có → đánh [x] test cases
Blocked:
