# Review T2 — FE hrm-client Phase 2c (4 danh mục xe công ty + menu nhóm Xe) — 14/10/2026

Reviewer CHỈ ĐỌC (không sửa code, không chạy e2e, không ghi DB).
Phạm vi: `git diff feat/chuyen-doi-hang-hoa...feat/cdhh-2c-xe` (commit `7d2daca61`, 10 file) ở
`wt-chuyen-doi-hang-hoa/hrm-client` + spec `e2e/tests/master-data/vehicles-ui.spec.ts` và chỗ sửa ở
`product-catalog-ui.spec.ts` / `product-catalog-common.api.spec.ts`. Đối chiếu: `2c-t2-brief.md`,
`2c-t1-report.md`, `2c-fix1-brief.md` + diff BE chưa commit đang làm song song trong `hrm-api`.

Đường dẫn file FE dưới đây tính từ gốc `hrm-client`, số dòng theo nhánh `feat/cdhh-2c-xe`.

## Kết luận nhanh

- Không có lỗi Critical.
- Đạt so với brief: entity-type đúng tên bảng ở cả 4 màn (`license_plates`, `drives`, `fuels`,
  `vehicles`, cả `catalogHistoryTable` lẫn `SystemInfoSection`). Cột Hành động dùng chung
  `vehicleCatalogScreenMixin`: `switch` theo key chuỗi, khoá/mở khoá so `status === 1`, mở khoá gọi
  `/unlock`, nút Sửa/Xoá/Khoá/Tạo mới ẩn khi không có quyền Quản lý. Menu khai `subItems`, chuỗi quyền
  khớp T1. Ô lái xe ngoài chọn nhiều trả mảng số (khai `extraSettings.multiple` + `toIds`). Payload chỉ
  mang các ô của loại chủ xe / loại tài xế đang chọn. Không dùng prop `trim`, khoảng trắng cắt lúc
  lưu. Bố cục popup đủ 12 cột mỗi hàng. Giá hiển thị dạng `en-US` (đúng HRM/CLAUDE.md, không theo chữ
  "định dạng VN" trong brief).
- Dây chuyền Hãng → Loại → Model: chỉ xoá con trong `@change`. `v-select2-component` chỉ phát `change`
  khi có `select2:select/unselect` (người dùng thao tác). Gán bằng code thì chạy `setValue`, không
  phát gì ⇒ **khi mở form Sửa, nạp dữ liệu không làm xoá nhầm giá trị con**. Cha đã khoá được chèn
  lại bằng `withLockedParent`. Khi `mounted` về muộn, `mergeOptions` vẫn giữ các option có
  `is_locked` ⇒ form Sửa vẫn hiện tên của giá trị đã khoá.
- Còn 3 điểm Important: có giá trị ẩn bị gửi đi, phụ thuộc vào BE fix1, và e2e còn thiếu ca.

---

## Critical

Không có.

## Important

### I1. Đổi qua đổi lại radio thì ô tìm trên máy chủ HIỆN TRỐNG nhưng vẫn GỬI giá trị cũ
- `pages/master-data/vehicles/AddVehicleModal.vue:143/168` (`v-if`/`v-else` theo Chủ xe), `:172-180` (`V2BaseSelectRemote` NCC), `:199/212` (`v-if`/`v-else` theo loại tài xế), `:215-223` (`VehicleRemoteMultiSelect`).
- `pages/master-data/vehicles/components/VehicleRemoteMultiSelect.vue:47` (lúc `mounted` chỉ gieo `initialOptions`), `:131-137` (`applyValue`: `$select.val(ids)` với id không có `<option>` thì select2 bỏ qua, không báo gì).
- Kịch bản 1 (Tạo mới):
  1. Chọn "Tài xế công ty", gõ tìm rồi chọn NV A.
  2. Đổi sang "Lái xe ngoài" ⇒ `v-if` huỷ ô NV.
  3. Đổi lại "Tài xế công ty" ⇒ ô dựng lại chỉ có `initialOptions` (`[]` khi Tạo mới) ⇒ **ô trống**,
     trong khi `data.company_drivers` vẫn là `[A]`.
  4. Bấm Lưu ⇒ gửi `company_drivers: [A]`. Lưu thành công một tài xế mà người dùng không nhìn thấy
     trên form.
- Kịch bản 2: tương tự với NCC — chọn NCC qua tìm kiếm → bấm "Xe Tân Phát" → bấm lại "Xe nhà cung
  cấp" ⇒ ô NCC trống, `data.owner` vẫn giữ id ⇒ BE nhận `owner` hợp lệ, không báo "bắt buộc".
- Kịch bản 3 (Sửa): đổi NCC từ X sang Y rồi bật/tắt radio ⇒ ô được gieo lại X (`supplierInitial`),
  nhưng value là Y nên không khớp option ⇒ ô trống mà vẫn lưu Y.
- Cách sửa gợi ý (chọn 1):
  - (a) Khi ô bị huỷ, xoá luôn giá trị của loại vừa bỏ (`data.owner = null` / `company_drivers = []`).
    Đúng nghĩa "bỏ chọn loại này".
  - (b) Giữ lại option đã chọn (cache `{id,name}` ở cha, truyền xuống làm `initialOption(s)`).
  - (c) Dùng `v-show` thay `v-if`.
- E2E nên có ca bật/tắt radio rồi đo: chip trên ô khớp đúng mảng trong payload.

### I2. Phụ thuộc BE fix1 đang làm song song: ô Lái xe ngoài
- `AddVehicleModal.vue:451-468` (`loadExternalDrivers` gọi `master-data/external-drivers/getAll`).
- Diff BE chưa commit (`ExternalDriverService::getAll`): `getAll` chỉ còn `id, name, status` + `is_locked`.
  SĐT chuyển sang endpoint mới có gate `GET master-data/vehicles/options/external-drivers`
  (`optionsForVehicleForm`, nhận `include_ids`).
- Hệ quả khi BE fix1 lên:
  - Không lỗi JS: `row.phone` rỗng thì nhãn rơi về chỉ còn tên. Nhưng mất "Tên - SĐT", mà report T2
    §2 ghi lý do cần SĐT là có lái xe trùng tên ⇒ dễ chọn nhầm người.
  - Câu ghi trong report T2 ("hiển thị Tên - SĐT") sẽ thành sai.
- Rủi ro tiềm ẩn ở `:463`: `is_locked: !!row.is_locked || Number(row.status) !== 1`. Nếu sau này BE bỏ
  nốt `status` (fix1 ghi "+ status nếu khuôn cần") thì `Number(undefined) !== 1` cho ra **mọi option
  đều bị coi là khoá**. Khi đó `filterUnusedLockedOptions` ẩn hết option chưa chọn ⇒ dropdown rỗng,
  không tạo được xe có lái xe ngoài. Nên dựa vào `is_locked` của BE là đủ.
- Cần làm: FE chuyển sang `master-data/vehicles/options/external-drivers?include_ids[]=` và bỏ
  `|| Number(row.status) !== 1`. Đổi xong, chạy lại ca e2e "khoá ⇒ 🔒" (hiện ca này chỉ so `DRIVER`
  nên vẫn xanh dù mất SĐT).
- `options/employees` bỏ `telephone`: **FE không dùng** (`fetchEmployees` `:476-482` dùng `name` do BE
  ghép sẵn; nhãn ban đầu `:594-598` dùng `code` + `name` lấy từ show xe). Không ảnh hưởng.
- BE fix1 đổi "mở khoá xe bị chặn" từ 400 sang 422: `toggleLock` của mixin hiện `payload.message` cho
  mọi mã ≠ 403 ⇒ vẫn hiện đúng câu báo. Không ảnh hưởng.

### I3. E2E chưa chốt các chỗ hay sót ở 3 màn phẳng, chưa có ca quyền, dọn dữ liệu chưa trọn
- 3 màn `license-plates` / `external-drivers` / `fuels` trong `product-catalog-ui.spec.ts:315-321`
  chỉ được đo **bố cục 12 cột**. Chưa có ca nào chốt:
  - `entity-type` của khối Lịch sử (đặc biệt `drives` — tên bảng khác slug, chỗ brief cảnh báo "hay sót");
  - mở khoá gọi `/unlock` (memory "danh mục bảng ERP khoá bằng 0": phải chốt bằng ĐƯỜNG được gọi);
  - bộ cột danh sách;
  - định dạng Giá `26,150` ở màn Nhiên liệu (memory "e2e UI phải kiểm khuôn giao diện").

  Report §3 có đo các ý này bằng MCP, nhưng không có ca để giữ lại. Khuôn có sẵn ở `:165` (Lịch sử)
  và `:450` (Mở khoá) — chỉ cần lặp theo slug.
- Không có ca UI về **quyền** cho 4 màn: chỉ quyền Xem ⇒ 0 nút "Tạo mới", cột Hành động chỉ còn
  "Lịch sử"; không quyền ⇒ bị đẩy sang 404. Memory "Always test permission cases" yêu cầu cover cả 2
  chiều. Report §3 đo tay, cũng không có ca giữ lại. Ca API 403 của 3 màn phẳng đã có ở
  `common.api`; màn `vehicles` thì chưa có cả ở API e2e (PHPUnit T1 có cover).
- Dọn dữ liệu `vehicles-ui.spec.ts:63-74`: không xoá `catalog_histories` của biển số / lái xe / xe
  thử. Mỗi lần chạy để lại khoảng 6–10 dòng lịch sử mồ côi. Report §6 ghi 0 dòng là nhờ dọn tay,
  không phải nhờ spec. Nên thêm `DELETE FROM catalog_histories WHERE table_name IN (...) AND table_id IN (...)`
  (kiểm tên cột thật trước khi viết) — lấy id trước khi xoá bản ghi.

## Minor

- **M1** `VehicleRemoteMultiSelect.vue:61-72` (khuôn chép từ `V2BaseSelectRemote`, bệnh có sẵn):
  - `transport` không trả về đối tượng `$request`. Khi `fetchFn` lỗi, select2 4.0.13
    (`select2.full.js:3641`) chạy `'status' in $request` với `$request = undefined` ⇒ TypeError ⇒
    không hiện "Không tải được dữ liệu", dropdown đứng ở "Đang tìm...".
  - Không huỷ được request cũ ⇒ gõ nhanh "Ng" → "Nguyễn" có thể hiện kết quả của "Ng" nếu request đó
    về sau.
  - Không có rò rỉ: `beforeDestroy` huỷ select2 và hàm thử focus lại.
- **M2** Nhãn tài xế công ty không thống nhất:
  - Gieo lúc Sửa `AddVehicleModal.vue:594-598` = "mã NV - Tên" (`10610026 - Bùi Duy Trước`).
  - Kết quả tìm `:476-482` = `name` của BE = "MÃ PHÒNG - Tên".
  - ⇒ Cùng một người nhưng chip hiện 2 kiểu tuỳ lúc.
- **M3** `loadPlateOptions` / `loadExternalDrivers` (`:432-468`, gọi không await ở `:504-505`) không
  có `seq`. Mở Sửa xe A → đóng nhanh → bấm Tạo mới: nếu request của A về sau thì ô Biển số của form
  tạo mới liệt kê cả biển của xe A (vì gửi `vehicle_id=A`). BE chặn bằng 422, nên chỉ gây khó chịu.
- **M4** `:569-572` Công ty của xe nằm ngoài `$store.state.companies` (ngoài phạm vi của người dùng,
  không phải đã khoá) vẫn bị gắn 🔒 ⇒ nhãn gây hiểu nhầm. Gắn liền với lo ngại 2 của report T2.
- **M5** `:374-385` Dữ liệu ERP cũ có Loại không thuộc Hãng của xe: `brandOptionsFiltered` lọc mất
  option ⇒ ô Loại hiện trống nhưng vẫn giữ id ⇒ bấm Lưu nhận 422 ở một ô đang trông như trống. Nên đo
  số xe lệch cha–con trên DB trước khi quyết có cần xử lý không.
- **M6** `mounted` `:350-367` dùng `Promise.all` không có `catch`: chỉ 1 trong 6 `getAll` lỗi là cả 6
  ô chọn đều trống, không có toast.
- **M7** Không có validate phía FE: bấm Lưu khi form trống vẫn đi 1 request. Chấp nhận được vì theo
  khuôn 2b, BE trả mọi lỗi cùng lúc (đo được 9 lỗi), nhưng lệch skill `form-validate` (màn mới dùng
  vee-validate realtime). Đã ghi ở report §7.1, chờ chốt.
- **M8** `fetchEmployees` không truyền `company_id` dù BE có hỗ trợ ⇒ xe Tân Phát công ty X vẫn chọn
  được NV công ty khác (report §7.3). Là câu hỏi nghiệp vụ, không phải lỗi.
- **M9** `vehicles-ui.spec.ts:300-303` ghi chú là "13 giá trị đổ đủ", nhưng chỉ assert có 2 ô chứa
  Hino/HINO. Chưa chốt Model, Dòng, Tải trọng, Nhiên liệu, Công ty, Bộ phận, tài xế công ty có tên ⇒
  nếu form Sửa làm rơi Model thì ca vẫn xanh. Nên assert số ô `.select2-selection__rendered` không
  rỗng = số ô đang hiện.
- **M10** `vehicles-ui.spec.ts:226/229/234` cứng vào dữ liệu Hino/HINO/Isuzu của DB dev. DB khác sẽ
  đỏ vì dữ liệu chứ không vì app. Có thể chấp nhận, nhưng nên ghi rõ trong comment đầu spec.
- **M11** `AddFuelModal.vue:29` `:max="99999999999999.99"` vượt độ chính xác của số thực double ở phần
  xu (thực tế ≈ …99.984). Không ảnh hưởng thực tế.

## Đã kiểm, không thấy lỗi

| Hạng mục | Kết quả |
|---|---|
| entity-type / `catalogHistoryTable` = tên bảng (4 màn) | ✔ `license_plates`, `drives`, `fuels`, `vehicles` |
| `V2BaseRowActions` key chuỗi, mở khoá gọi `/unlock` | ✔ (mixin 2b: `isActiveRow` = `status === 1`) |
| Ẩn nút ghi khi không có quyền Quản lý | ✔ `canManage` (Tạo mới, Sửa, Xoá, Khoá/Mở khoá); Xuất Excel không gate (khuôn 2b) |
| Menu `subItems` + chuỗi quyền | ✔ khớp T1 (1699–1706) |
| Chọn nhiều trả mảng số | ✔ lái xe ngoài (`extraSettings.multiple` + `toIds`); tài xế công ty (`map(Number)`) |
| Mở form Sửa không xoá nhầm con | ✔ không dùng `watch`; `v-select2-component` không phát `change` khi gán bằng code |
| Giá trị đã khoá hiện tên khi Sửa | ✔ `withLockedParent` + `include_ids` + `initialOption(s)` (trừ I1 khi bật/tắt radio) |
| Payload theo is_tanphat / driver_type | ✔ (nhưng xem I1: giá trị ẩn) |
| Bỏ prop `trim`, cắt khi lưu | ✔ cả 3 popup phẳng |
| Bố cục 12 cột | ✔ 7+5/12 · 6+3+3/4+4+4 · 5+4+3 · xe 4+4+4/4+4+4/6+6/12/6+6 hoặc 12/12/12 |
| Định dạng giá | ✔ `toLocaleString('en-US')` + `V2BaseCurrencyInput` |
| Lọc dây chuyền ở danh sách | ✔ xoá con trong cùng nhịp `handleFilterChange` (1 request) |
| `columnScreenKey` / `table` / `localStorageKey` trùng màn khác | ✔ không trùng (git grep) |
