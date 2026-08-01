# Khảo sát — BOM GIẢI PHÁP (BOM List)

> Xác minh: `BomBuilderAddProductModal.vue` **là code chết** (không file nào import). Popup chọn hàng hoá **thật** là `pages/assign/quotations/components/QuotationProductSearchModal.vue`, import tại `BomBuilderEditor.vue:267`.

## A. Màn danh sách
**URL:** `/assign/bom-list`. Tiêu đề bảng: **Danh sách BOM List**. API `GET assign/bom-lists`.

### A1. Bộ lọc — panel "Bộ lọc danh sách BOM List" (phụ đề "Bạn có thể chọn tìm kiếm nâng cao để lọc nhiều thông tin hơn")
| Tiêu chí | Control | Ghi chú |
|---|---|---|
| Ô tìm nhanh | input | placeholder `Tìm theo Mã BOM, Tên BOM` — **không auto-search**, phải bấm Tìm kiếm |
| Công ty / Phòng ban / Bộ phận | `V2BaseCompanyDepartmentFilter` | phân quyền theo cấp |
| **Dự án TKT** | V2BaseSelect allowClear | `assign/prospective-projects/getAll` |
| **Giải pháp** | input **disabled** | placeholder `Chọn dự án TKT để hiện giải pháp` — tự suy từ dự án |
| **Hạng mục** | V2BaseSelect | `:disabled="!filters.solution_id"` |
| **Khách hàng** | V2BaseSelect | `human/customers?per_page=10000` |
| **Người tạo** | V2BaseSelect | `allEmployeesOptions` |
| **Trạng thái** | V2BaseSelect | 6 giá trị (mục H) |
| **Loại BOM** | V2BaseSelect | `Thành phần` (1) / `Tổng hợp` (2) |
| **Thời gian tạo từ** / **Đến** | V2BaseDatePicker ×2 | |

Cascading: chọn Dự án TKT → tự chọn Giải pháp, nạp Hạng mục, tự điền Khách hàng; bỏ chọn → xoá cả 3. Mọi filter khác keyword đều **auto-search**. Filter lưu localStorage `assign_bom_list`, 10 phút.

### A2. Cột bảng
STT · **Mã • Tên BOM** (sticky, dòng phụ `Người tạo` / `Phòng`, cụm nút thao tác) · Dự án TKT · Giải pháp · Hạng mục · **Version GP** · **Version HM** · Khách hàng · Loại BOM · Trạng thái (badge màu) · Người tạo · Ngày tạo (sort) · Cập nhật (sort, kèm "bởi {người}").

### A3. Nút thanh công cụ
| Nhãn | Điều kiện | Hành động |
|---|---|---|
| **Tạo mới** | `hasAPermission('Tạo BOM List')` | → `/assign/bom-list/add` |
| **Xuất Excel** | luôn (đổi nhãn `Đang xuất...`) | `GET assign/bom-lists/export-list` — xuất **danh sách theo bộ lọc**, file `Danh_sach_BOM_{yyyy-mm-dd}.xlsx` |
| icon **Cấu hình cột hiển thị** | luôn | `ColumnCustomizationModal` |

### A4. Thao tác từng dòng
| Nút | Điều kiện |
|---|---|
| **Xem chi tiết** | luôn — nuxt-link `/assign/bom-list/{id}` |
| **Sửa** | `status ∈ {1 Đang tạo, 2 Hoàn thành, 6 Không duyệt}` **VÀ** là người tạo |
| **Sao chép** | có quyền `Tạo BOM List` → `/assign/bom-list/add?copy_from={id}` |
| **Xem lịch sử** | luôn — `BomListLogModal` |
| **Xóa** | `status == 1` **VÀ** là người tạo **VÀ** có quyền `Tạo BOM List` |

Xoá → modal **Xác nhận xóa**, `Bạn có chắc muốn xóa BOM List '{code} - {name}'?`, nút `Hủy` / `Xóa`.

## B. BOM THÀNH PHẦN vs BOM TỔNG HỢP
Cột `bom_lists.bom_list_type` — `TYPE_COMPONENT = 1`, `TYPE_AGGREGATE = 2`; nhãn `Thành phần` / `Tổng hợp`. FE dùng `'component'` / `'aggregate'`, nhãn select là **BOM LIST thành phần** / **BOM LIST tổng hợp**.

**Quan hệ:** BOM tổng hợp **gom từ các BOM thành phần**, lưu ở `bom_list_relations` (`parent_bom_list_id` → `child_bom_list_id`).

**Hệ quả trạng thái:** BOM tổng hợp chọn 1 BOM thành phần làm con → BOM con đổi sang **Đã được tổng hợp** (5); bỏ chọn hoặc xoá BOM tổng hợp → con trở lại **Hoàn thành** (2).

**Điều kiện tạo BOM tổng hợp:**
1. Giải pháp **có hạng mục con** mà BOM gắn cấp Giải pháp (không chọn Hạng mục) → **bắt buộc** loại Tổng hợp. Lỗi: `Giải pháp có hạng mục con — BOM cấp giải pháp chỉ được tạo loại Tổng hợp.` FE khoá ô Loại BOM.
2. **Duy nhất 1 BOM tổng hợp / (Giải pháp [+ Hạng mục]) / version.** Lỗi: `Giải pháp[ / Hạng mục] đã có BOM tổng hợp trên version này: {tên} ({mã}) (version …)`
3. Danh sách BL con được chọn (luôn cùng Dự án + cùng Giải pháp):

| BOM đang tạo | Loại con nhận | Trạng thái con yêu cầu |
|---|---|---|
| Cấp Giải pháp, GP **có** hạng mục | `aggregate` cấp hạng mục | **status = 4 (Đã duyệt)** |
| Cấp Giải pháp, GP **không** chia hạng mục | `component` | `status ≠ 1` |
| Cấp Hạng mục | `component` cùng hạng mục | `status ≠ 1` |

## C. TẠO MỚI BOM THÀNH PHẦN
**Mở từ:** nút **Tạo mới** → **`/assign/bom-list/add`**. Vào thẳng trang mà không có quyền `Tạo BOM List` → toast `Bạn không có quyền tạo BOM List` + đẩy về danh sách.

### C1. Thông tin chung
| Nhãn | Control | Bắt buộc / message | Mặc định | Ẩn / readonly | Cascading | Options |
|---|---|---|---|---|---|---|
| **Mã BOM** | V2BaseInput readonly | – | BE sinh khi Lưu: `BOM-{năm}-{5 số}` | **Ẩn hẳn** khi chưa có mã | – | – |
| **Tên BOM LIST** | V2BaseInput | ✔ `Vui lòng nhập tên BOM.`; quá dài: `Tên BOM không được vượt quá 255 ký tự.` | trống, `VD: BOM điều khiển dây chuyền line 01` | – | – | – |
| **Dự án** | SearchPicker | ✔ `Vui lòng chọn Dự án.` (nới lỏng khi Lưu nháp) | trống, `Tìm dự án theo mã / tên...` | – | chọn → fill Khách hàng, tự chọn Giải pháp, **xoá sạch BL con** | `assign/prospective-projects/getAll?per_page=10000&my_projects=1` |
| **Giải pháp** | V2BaseInput **readonly** | ✔ `Vui lòng chọn Giải pháp.` | suy từ Dự án | luôn readonly | đổi → nạp lại Hạng mục, xoá BL con | `assign/solutions/getAll` |
| **Hạng mục** | SearchPicker | không | trống, `Tìm hạng mục theo mã / tên...` | **khoá khi chưa có Giải pháp** | bỏ trống (khi GP có hạng mục) → ép Loại BOM = Tổng hợp | `modules[]` trong `solutions/getAll` |
| **Khách hàng** | V2BaseInput **readonly** | ✔ `Vui lòng chọn Khách hàng.` | tự điền từ Dự án; `Chọn dự án để tự động hiện khách hàng` | luôn readonly | – | từ chi tiết BOM (ERP TpCustomer) |
| **Ghi chú** | V2BaseInput | – | trống, `BOM dùng cho giải pháp triển khai demo.` | – | – | – |
| **Loại BOM LIST** | V2BaseSelect | `Vui lòng chọn Loại BOM.` | **BOM LIST thành phần** | khoá khi `isSolutionLevelBom` | đổi khi đã có dữ liệu → confirm `Hệ thống sẽ xoá bỏ toàn bộ danh sách hàng hoá đang có. Bạn xác nhận sẽ thay đổi?` rồi **xoá sạch** lưới | 2 giá trị hard-code |
| **Chọn BL con** (nút) | button | – | – | chỉ bấm được khi Loại = Tổng hợp | – | – |

Trường **tiền tệ** có trong payload (`currency_id`) nhưng **không render** trên UI; mặc định VND qua `GET assign/bom-lists/currencies`.
Lưu nháp (`status=1`) thì Dự án/Giải pháp/Khách hàng thành `nullable`.

### C2. Bảng chi tiết hàng hoá — tiêu đề **Chi tiết BOM LIST**
Toolbar: **Import Excel** (khoá khi chưa lưu nháp, tooltip `Vui lòng lưu nháp BOM trước khi import`) · **Xuất Excel** · **Ẩn cấp con / Hiện cấp con**. Dòng thống kê: `Tổng nhóm cha: N` · `Tổng hàng con: N` · `Kéo icon ⠿ để đổi thứ tự`.
Bảng chia 2 khối: **A — Hàng hoá** và **B — Dịch vụ & Chi phí khác**.

**Cột:**
| Cột | Nhập tay | Công thức / ghi chú |
|---|---|---|
| Thao tác | – | ẩn ở chế độ Xem |
| STT | – | cha `1,2,3…`, con `1.1`; có nhóm thì nhóm đánh số La Mã `I.`, nhóm con `I.1` |
| Mã hàng | – | hàng tạm để trống → BE sinh `HHB` + id pad 6 |
| Tên hàng | – | sửa qua popup; bên dưới là cụm nút thao tác dòng |
| Model / Thương hiệu / Xuất xứ | – | bật mặc định |
| ĐVT | **select** chỉ khi dòng cha là hàng ERP, không có con | `POST assign/quotations/erp-product-units` |
| Thông số kỹ thuật | – | rich-text, sửa qua popup |
| **Ghi chú** | **CÓ** — gõ trực tiếp | |
| **Số lượng** | **CÓ** — cha luôn nhập; **con bị khoá nếu cha là hàng ERP** (tooltip `SL theo công thức ghép bộ, tự nhân theo SL cha`) | đổi SL cha ERP → `con.qty = làm tròn(recipeUnitQty × SL cha, 2)` |
| Giá nhập / Thành tiền nhập / Giá bán / Thành tiền bán / Tỷ suất LN (%) | **mặc định TẮT** — ghi chú code: *"BOM không còn quản lý giá — toàn bộ giá nhập ở Báo giá"* | Thành tiền = giá × SL; roll-up cha = `Σ(giá con × SL con) / SL cha`; Tỷ suất LN = `(bán − nhập)/nhập × 100` |

> Modal **Tuỳ chỉnh cột hiển thị** tồn tại nhưng **không có nút nào mở được** → thực tế chỉ thấy 7 cột mặc định.

**Thêm dòng:**
| Nút | Vị trí | Mở gì |
|---|---|---|
| **Thêm nhóm** | dòng `A — Hàng hoá` | modal **Tạo nhóm hàng** |
| **Thêm mới** | dòng `A — Hàng hoá` / header từng nhóm | **`QuotationProductSearchModal`** tab Hàng hoá → dòng CHA |
| **Thêm nhóm con** | header nhóm Cấp 1 | modal **Tạo nhóm hàng** (Cấp 2) |
| **Thêm con** | dưới tên dòng cha | cùng popup; chỉ khi cha **không phải dịch vụ** và **không phải hàng ERP** |
| **Thêm mới** | dòng `B — Dịch vụ & Chi phí khác` | cùng popup, tab **Dịch vụ & Chi phí** |

Popup chọn hàng hoá: tiêu đề động **Thêm hàng hoá** / **Thêm dịch vụ / chi phí**; ô **Nhóm hàng** (bắt buộc, lỗi `Vui lòng chọn nhóm hàng`); panel **Bộ lọc hàng hoá** + 18 filter nâng cao; bảng 16 cột (Ảnh, Loại hàng hóa, Tên hàng hoá, Model, Mã hàng, Giá niêm yết, Bảo hành, VAT(%), Định mức đàm phán giá (%), SL tồn có thể bán, SL KM có thể xuất, SL có thể LR, Ghi chú, Tính chất hàng hóa, Nguồn); chọn nhiều bằng checkbox; footer **Thêm {n} hàng hoá** / **Đóng**. Thêm trùng → overlay **Hàng hoá đã tồn tại** với **Cộng dồn số lượng** / **Tạo dòng mới** / **Huỷ**.

Chọn hàng cha ERP → tự nạp hàng con theo công thức ghép bộ (`GET assign/bom-lists/erp-recipe-children`), con bị khoá giá + khoá SL.

**Sửa dòng:** nút **Sửa** → modal **Sửa nhanh hàng hoá** / **Sửa nhanh dịch vụ**. Trường: Tên hàng ✔, Mã (luôn disabled), Dự án/Giải pháp (disabled), Đơn vị tính ✔, Model ✔, Thương hiệu, Xuất xứ, Số lượng cần dùng, Ghi chú, Đặc điểm / Thông số kỹ thuật. Hàng ERP hiện banner `Hàng hoá lấy từ ERP — chỉ có thể sửa Số lượng...`. Lỗi FE: `Vui lòng nhập tên hàng hoá.` / `Vui lòng chọn model.` / `Vui lòng chọn đơn vị tính.` / `Mã hàng cha đang bị trùng trong BOM.` / `Mã hàng con đang bị trùng trong cùng một dòng cha.`

**Xoá dòng:** modal **Xác nhận xoá**: cha `Bạn có chắc muốn xoá dòng cha và toàn bộ hàng con của nó?`, con `Bạn có chắc muốn xoá dòng con này?`, nhóm `Xoá nhóm này sẽ xoá tất cả hàng hoá trong nhóm. Bạn có chắc?` (⚠️ thực tế code chỉ chuyển hàng sang nhóm còn lại — message sai so với hành vi). Dòng dịch vụ xoá **ngay, không confirm**.

**Gom nhóm:** cây **2 cấp** (`bom_list_groups`), Cấp 1 số La Mã, Cấp 2 thụt lề. Modal nhóm chỉ 1 trường **Tên nhóm** (bắt buộc), nút **Lưu** / **Huỷ**. Kéo thả sắp xếp bằng SortableJS.

**Lưu:** thanh cố định đáy — **Quay lại** · **Lưu nháp** (chỉ khi tạo mới hoặc BOM "Đang tạo") → `status=1` · **Lưu BOM** → `status=2`. Toast `Đã lưu BOM LIST thành công.`

## D. TẠO MỚI BOM TỔNG HỢP
Cùng URL `/assign/bom-list/add`, **khác 3 điểm**:
1. Đặt **Loại BOM LIST = BOM LIST tổng hợp** (hoặc bị ép khi BOM cấp Giải pháp mà GP có hạng mục).
2. Bấm nút **Chọn BL con** → modal **Chọn BOM con để gộp**: bảng 6 cột **Chọn / Mã BL / Tên BL / Dự án / Giải pháp / Hạng mục**, tick nhiều, nút **Gộp BOM con**. Chưa chọn Dự án/Giải pháp → toast `Vui lòng chọn Dự án và Giải pháp trước khi chọn BL con.`; chưa tick → `Chưa chọn BL con nào.`
3. Bấm **Gộp BOM con** → FE gọi `GET assign/bom-lists/{id}` từng BOM con, **xoá sạch lưới hiện tại** rồi nạp lại hàng hoá + nhóm (gộp nhóm trùng tên) + dịch vụ theo thứ tự BOM con tạo trước → sau; hàng tạm trùng mã bị xoá mã để BE cấp lại. Validate: `Loại tiền tệ không khớp: {…}. BOM tổng hợp và BOM thành phần phải cùng loại tiền tệ.` và `Các BOM con phải có cùng cấu trúc. BOM có nhóm: {…}. BOM không có nhóm: {…}.`

Sau khi lưu, các BOM thành phần được chọn tự chuyển **Đã được tổng hợp**.
Lưu ý: nút **Thêm mới / Thêm nhóm** trên lưới **vẫn bấm được** ở BOM tổng hợp — code cố ý giữ hành vi này.

## E. CHỈNH SỬA BOM
- **URL:** `/assign/bom-list/{id}/edit`.
- **Điều kiện được sửa (BE):** `status ∈ {1, 2, 6}` **và** `created_by == người đăng nhập`. Lỗi: `Chỉ người tạo BOM mới được phép sửa.` / `BOM ở trạng thái này không được phép sửa. Chỉ BOM "Đang tạo", "Hoàn thành" hoặc "Không duyệt" mới được sửa.`
  ⚠️ **FE chặt hơn**: chỉ cho `status ∈ [1,2]`, status 6 bị đá về màn Xem với toast `BOM ở trạng thái này không được phép sửa.` — lệch so với BE.
- **Trường khoá:** Mã BOM, Giải pháp, Khách hàng (readonly); Loại BOM khoá khi là BOM cấp Giải pháp; Mã hàng luôn khoá; dòng hàng ERP chỉ sửa được Số lượng.
- **Auto reset:** BOM đang **Không duyệt** khi lưu lại tự chuyển về **Hoàn thành**.
- **Versioning:** KHÔNG có version của bản thân BOM. Chỉ ghi `solution_version_id`, `solution_module_version_id` (ghi đè bằng `current_version_id` mỗi lần lưu). Update thực chất là **xoá sạch rồi ghi lại** products/groups/relations; lịch sử lưu ở `bom_list_logs`.
- **Sao chép BOM** thay cho versioning: `/assign/bom-list/add?copy_from={id}` → `GET assign/bom-lists/{id}/copy-data` prefill, lưu kèm `copied_from_bom_list_id`.

## F. HÀNG TẠM & ĐỒNG BỘ
**Hàng tạm là gì:** dòng hàng hoá **chưa có trong danh mục ERP** — `bom_list_products.erp_product_id IS NULL`. Mã HRM tự sinh khi lưu: `HHB` + id pad 6 (VD `HHB000123`).

**Thêm hàng tạm — nút ở đâu:** trong popup chọn hàng hoá (`QuotationProductSearchModal`), nút **Thêm hàng tạm** cạnh nút "Tìm kiếm nâng cao". Mở overlay **Thêm hàng tạm**, có ô **Nhóm hàng** (bắt buộc) dùng chung, và **2 tab**:

**Tab 1 — "Chọn từ kho hàng tạm (Tái sử dụng)"**: ô tìm `Tìm nhanh theo mã / tên hàng tạm...`; bảng **Mã hàng / Tên hàng / Model / Thương hiệu / Xuất xứ / ĐVT / Nguồn** (badge `Dự án` = hàng tạm cùng dự án từ `assign/product-projects?only_temp=1`, `Trong phiếu` = hàng tạm đang có trên lưới); nút **Thêm {n} hàng hóa** / **Đóng**. Chọn 1 cha sẽ copy cả cha lẫn con.

**Tab 2 — "Thêm mới thủ công"**:
| Nhãn | Control | Bắt buộc + message | Options |
|---|---|---|---|
| **Tên hàng hoá** | V2BaseInput `Nhập tên hàng hoá` | ✔ `Tên là bắt buộc` | – |
| **Đơn vị tính** | V2BaseSelectInModal `Chọn ĐVT` | ✔ `Đơn vị tính là bắt buộc` | `assign/product-projects/get-unit` |
| **Model** (+ icon `+` thêm nhanh) | V2BaseSelectRemote | không | `.../get-model` |
| **Thương hiệu** (+ icon `+`) | V2BaseSelectRemote | ✔ `Thương hiệu là bắt buộc` | `.../get-brand` |
| **Xuất xứ** (+ icon `+`) | V2BaseSelectRemote | ✔ `Xuất xứ là bắt buộc` | `.../get-origin` |
| **Số lượng cần dùng** | number, min 0 | không (mặc định 1) | – |
| **Ghi chú** | V2BaseInput | không | – |
| **Đặc điểm / Thông số kỹ thuật** | CompactReviewEditor | không | – |
| (chung) **Nhóm hàng** | V2BaseSelectInModal | ✔ `Vui lòng chọn nhóm hàng` | nhóm của BOM |

Nút: **Lưu** / **Lưu và tiếp tục** / **Đóng**. Icon `+` mở overlay nhỏ nhập **Tên** (+ **Mã thương hiệu** riêng cho thương hiệu), lỗi `Vui lòng nhập tên.` / `Vui lòng nhập mã.`

Nút **Nhân bản** trên dòng cha hàng tạm (tooltip `Tạo thêm 1 dòng cùng hàng tạm này (dùng chung mã)`) tạo dòng clone **dùng chung 1 mã HHB**.

**Xử lý trùng mã khi lưu:** mã hàng tạm chỉ **giữ nguyên** nếu đã tồn tại trong **cùng dự án** (quét `bom_list_products` của BOM tổng hợp và `quotation_product_prices` của báo giá tự lập, mọi trạng thái). Mã "lạ" (import/copy từ dự án khác) bị **vứt → sinh HHB mới**.

**"Đồng bộ" là gì:** đẩy hàng tạm sang ERP để ERP duyệt và cấp `product_id` chính thức.
> ⚠️ **Chức năng này KHÔNG nằm trên màn BOM.** `TmpProductSyncService` chỉ nhận `Quotation`, không nhận `BomList`.
- `sendApproval(Quotation)` — `POST {ERP}/api/v1/tmp-product-requests/sync-from-hrm`, ERP trả `map {hrm_line_id → tmp_product_id}`; HRM ghi `erp_tmp_product_id` từng dòng và đặt `quotation.tmp_sync_status = 'syncing'`. Map rỗng → lỗi `ERP không trả về kết quả tạo hàng tạm. Vui lòng thử lại.`
- `pullStatus(Quotation)` — `POST {ERP}/api/v1/tmp-product-requests/approved-status`; dòng ERP duyệt (`status=1`) thì ghi `erp_product_id`; hết dòng chưa có `erp_product_id` → `tmp_sync_status = 'synced'`. Trả `{synced, rejected, pending}`.

**Ai bấm, ở đâu:** tab Báo giá của Dự án tiềm năng, banner `Báo giá trúng thầu {code} — Đồng bộ hàng tạm sang ERP`, badge **Chưa đồng bộ / Đang đồng bộ sang ERP / Đã đồng bộ**, tiến độ `{n}/{m} hàng tạm đã duyệt`, 2 nút **Gửi duyệt hàng tạm** (chỉ NV KD phụ trách dự án) và **Cập nhật kết quả duyệt**; confirm `Gửi duyệt hàng tạm của báo giá trúng thầu sang ERP?`; API `POST assign/prospective-projects/{id}/send-tmp-approval`.

**Trên BOM chỉ có 2 dấu vết đồng bộ:**
- Cột `bom_list_products.erp_sync_status` — accessor trả `Đã đồng bộ` / `Chưa đồng bộ`. Hiển thị ở màn Hàng hoá dự án.
- Trong **Import Excel BOM**, dòng trùng mã hiện 2 nút: **Tạo mã mới** hoặc **Giữ nguyên mã và đồng bộ**.

## G. Duyệt BOM
**Không có nút Duyệt/Từ chối/Gửi duyệt trên màn BOM.** Trạng thái BOM tổng hợp được **hồ sơ trình duyệt Giải pháp / Hạng mục** điều khiển:
| Review status hồ sơ | BOM tổng hợp chuyển sang | Log |
|---|---|---|
| `pending` | **3 — Chờ duyệt** | `Gửi duyệt BOM List` |
| `approved` | **4 — Đã duyệt** | `BOM List đã được duyệt` |
| `rejected` | **6 — Không duyệt** | `BOM List không được duyệt` |
Chỉ áp cho `bom_list_type = 2`. Khi duyệt xong gửi notify 4 đối tượng: người gửi hồ sơ, PM phụ trách giải pháp, người lập BOM, NV KD phụ trách dự án.

**Duyệt giá** là luồng khác (dành cho Báo giá): bảng `bom_price_approval_configs` cấu hình ngưỡng 3 cấp (**Cấp 1 Tự duyệt / Cấp 2 Trưởng phòng / Cấp 3 Ban giám đốc**); quyền `Trưởng phòng duyệt giá Bom giải pháp` / `Ban giám đốc duyệt giá Bom giải pháp` gắn ở route **quotations**, không gắn ở route bom-lists.

## H. Trạng thái BOM
| Mã | Nhãn | Màu | Đặt bởi |
|---|---|---|---|
| 1 | **Đang tạo** | #FF9800 | **mặc định** khi tạo; nút **Lưu nháp** |
| 2 | **Hoàn thành** | #4CAF50 | nút **Lưu BOM**; auto khi sửa BOM "Không duyệt"; auto khi bị gỡ khỏi BOM tổng hợp |
| 3 | **Chờ duyệt** | #2196F3 | hồ sơ trình duyệt GP/hạng mục `pending` |
| 4 | **Đã duyệt** | #9C27B0 | hồ sơ `approved` |
| 5 | **Đã được tổng hợp** | #9E9E9E | BOM thành phần bị BOM tổng hợp chọn làm con |
| 6 | **Không duyệt** | #F44336 | hồ sơ `rejected` |

Badge trạng thái chỉ hiện ở **màn Chi tiết**, góc trên trái card thông tin.

## I. Downstream — BOM đã duyệt dùng ở đâu
**1. Báo giá lấy từ BOM.** Trường **BOM tổng hợp** nạp bằng `GET assign/bom-lists/getAll?prospective_project_id={id}&bom_list_type=2&status=4&only_aggregate_solution_level=1&per_page=50` — **chỉ BOM Tổng hợp, Đã duyệt, cấp Giải pháp**. 1 BOM → tự chọn + nạp hàng (`type=1`); nhiều → bắt chọn; không có → `Không có BOM tổng hợp đã duyệt`, báo giá thành `type=2` (tự lập). Đổi BOM khi đã có dữ liệu → confirm `Việc chọn lại BOM sẽ xoá toàn bộ thông tin hàng hoá/dịch vụ trên báo giá!`

**2. Hàng hoá dự án** (`/assign/product-project`, tiêu đề **Danh sách hàng hoá làm dự án**) — **không có bảng `product_projects`**. Là **view union 2 nguồn**, dedup theo (mã + dự án):
| Nguồn | Điều kiện lọc | dedup_rank |
|---|---|---|
| `bom_list_products` | join `bom_lists` với **`bom_list_type = 2`** **và `status = 4`**; lấy cả cha lẫn con | 2 |
| `quotation_product_prices` | join `quotations` với **`type = TYPE_SELF_BUILT`**, **`bom_list_id IS NULL`**, **`status ∈ {4, 7}`** | Trúng thầu = 3, Đã duyệt = 2 |
Dedup: cùng mã + cùng dự án → giữ rank cao nhất → `created_at` mới nhất → `row_id` lớn nhất. Dòng không có mã giữ hết.

Cột màn Hàng hoá dự án: STT · Mã hàng · Tên hàng · **Mã BOM** (link `/assign/bom-list/{id}`, hàng từ báo giá độc lập để `—`) · Model · Dự án · Giải pháp · Thương hiệu · Xuất xứ · Người tạo · ĐVT · Đặc điểm / TSKT · Hàng hoá cha · Ghi chú · **Mã đồng bộ ERP** · **Trạng thái ĐB**. Bộ lọc: `Tìm theo mã, tên hàng hoá...` + Dự án · Giải pháp · Người tạo · Model · Thương hiệu · Xuất xứ · Trạng thái đồng bộ. Toolbar: **Xuất Excel** · **Cấu hình cột**. **Không có thao tác từng dòng, read-only.**

**3. Picker "Dùng lại hàng tạm dự án"** trong popup thêm hàng tạm cũng ăn từ view này (`only_temp=1`, chỉ hàng cha, chỉ hàng chưa đồng bộ).

## J. Quyền
| id | Tên quyền |
|---|---|
| 1035 | `Xem danh sách BOM List theo tổng công ty` |
| 1031 | `Xem danh sách BOM List theo công ty` |
| 1032 | `Xem danh sách BOM List theo phòng ban` |
| 1033 | `Xem danh sách BOM List theo bộ phận` |
| 1034 | `Tạo BOM List` |
| 1092 | `Xem giá vốn hàng hoá` |

**⚠️ Cảnh báo: "Tạo BOM List" chỉ được kiểm ở FE.** Group route `/assign/bom-lists` **không có `checkPermission` nào**, và grep `'Tạo BOM List'` trong `hrm-api/Modules` trả **0 kết quả**. `POST/PUT/DELETE /assign/bom-lists` gọi trực tiếp API **không cần quyền**. Trong HDSD nên mô tả quyền này là "quyền hiển thị nút", không phải rào chặn.

Gating trong controller/service:
- `isCurrentEmployeeHasPermission('Xem giá vốn hàng hoá')` → cờ `can_view_cost_price`; chặn cứng khi thêm hàng ERP làm con: `Bạn không có quyền "Xem giá vốn hàng hoá" nên không thể chọn hàng ERP làm hàng con.`
- Sửa/xoá: gate bằng `created_by` + trạng thái.

**hasAPermission ở FE:** nút Tạo mới / Sao chép / Xoá → `Tạo BOM List`; filter theo cấp → 4 quyền `Xem danh sách BOM List theo …`; chặn vào trang add/edit → `Tạo BOM List`; chọn hàng ERP làm con → `Xem giá vốn hàng hoá`.

**Phân quyền theo cấp:** `checkPermissionListWithColumn(..., 'bom_lists', 'created_by')` chuẩn. Không có mở rộng theo thành viên.

## K. Import/Export/Lịch sử
- **Import Excel**: tiêu đề **Import hàng hoá BOM List**, phụ đề `Validate rồi áp dữ liệu vào lưới BOM — chọn phương thức (từng phần / thay thế), kiểm tra rồi bấm "Lưu BOM"`. Nút: **Chọn file Excel** · **Tải file mẫu** · **Load lên bảng** · **Validate** · **Chỉ dòng lỗi / Hiện tất cả** · **Đang bỏ qua dòng lỗi / Bỏ qua dòng lỗi** · **Xoá trạng thái validate** · **Import** · **Làm mới** · **Đóng**. Cột file mẫu: `Loại*`, `Nhóm hàng cha (Cấp 1)`, `Nhóm hàng con (Cấp 2)`, `STT*`, `Mã hàng cha`, `Mã hàng*`, `Tên hàng*`, `Model`, `Thương hiệu*`, `Xuất xứ*`, `ĐVT*`, `Số lượng*`, `Thông số kỹ thuật`, `Ghi chú`. Bấm Import → popup **Chọn phương thức áp dữ liệu**: **Import từng phần** / **Thay thế hoàn toàn**; file thuộc BOM khác → **Phát hiện dữ liệu thuộc BOM khác** + **Sao chép vào lưới**. Dòng trùng mã → **Tạo mã mới** / **Giữ nguyên mã và đồng bộ**. API: `POST assign/bom-lists/{id}/import/validate` rồi `POST .../import`.
- **Xuất Excel 1 BOM**: tiêu đề **Xuất Excel BOM List**, checkbox **Xuất hàng hoá cấp con**, nút **Xuất Excel** / **Huỷ**; `GET assign/bom-lists/{id}/export?include_children=1|0`, tên file = mã BOM. Chỉ mở được từ màn **Chi tiết** và **Cập nhật**.
- **Lịch sử**: tiêu đề **Lịch sử BOM List**, timeline theo hành động (`created / updated / deleted / status_completed / submitted / approved / rejected / imported`), hiển thị người thực hiện, nội dung, danh sách thay đổi (`{nhãn}: {cũ} → {mới}`), danh sách hàng hoá **Thêm / Xoá / Sửa**, thống kê `Thành công: n, Thất bại: m`, thời gian `DD/MM/YYYY HH:mm`.

## L. Bất thường phát hiện (lưu ý khi viết HDSD)
1. `BomBuilderAddProductModal.vue` — code chết, đừng mô tả.
2. Modal **Tuỳ chỉnh cột hiển thị** trên màn tạo/sửa BOM **không có nút mở** → không đưa vào HDSD.
3. Màn **Chi tiết BOM** render **2 thanh footer chồng nhau**.
4. Message confirm xoá nhóm nói "sẽ xoá tất cả hàng hoá trong nhóm" nhưng code chỉ chuyển hàng sang nhóm khác.
5. FE chặn sửa BOM ở trạng thái **Không duyệt (6)** trong khi BE cho phép — mô tả theo FE (thực tế người dùng thấy).
6. Khối `pricingMode` (Gửi duyệt giá, badge Cấp 1/2/3) tồn tại trong `BomBuilderEditor` nhưng **không trang nào bật** → không thuộc luồng hiện hành.
