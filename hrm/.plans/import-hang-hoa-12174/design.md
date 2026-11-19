# Import hàng hoá — file mẫu 10 sheet (Redmine #12174)

Vị trí: Danh mục › Hàng hóa › Dữ liệu hàng hoá công ty (`/master-data/products/company`), nút **Import** hiện có.
Ticket: http://quanly.dnsmedia.vn/issues/12174
File mẫu nghiệp vụ: https://docs.google.com/spreadsheets/d/1Zj48ybb5OGOWh3T9NNzCEn371vrIHgXu/edit?gid=406052145

**Bản này nâng cấp chức năng đã chạy trên develop**, thiết kế gốc ở `HRM/.plans/import-hang-hoa-cong-ty/design.md`
(gọi tắt "thiết kế cũ"). Mọi quyết định của thiết kế cũ **giữ nguyên** trừ khi mục dưới đây ghi khác.
Code hiện có: FE `hrm-client/components/product/ProductImportModal.vue`, mẫu `hrm-client/static/Mau_import_hang_hoa.xlsx`;
BE `hrm-api/Modules/MasterData/Services/Product/Import/*` (Service, Validator, UpdateChecks, Writer, Catalog, Cells, Row),
controller `V1\Product\ProductImportController`, route `POST /products/import/validate` và `POST /products/import`.

## 1. Mục đích

Mẫu cũ là 1 sheet 79 cột, lưới 1-N (thuộc tính, ĐVT, công thức, phụ kiện, vật tư, nhóm máy, catalog) nhồi vào ô bằng `;`
và ghép theo vị trí, rất dễ lệch. Nghiệp vụ đổi sang mẫu **10 sheet**: Sheet 1 thông tin chung, mỗi lưới 1-N một sheet,
mỗi dòng một bản ghi, nối về Sheet 1 qua cột Mã hàng hoá. Thêm lưới mới **Phân loại xe** (Sheet 8) và cho **nhiều ĐVT
có giá riêng** trên một hàng (Sheet 2).

## 2. Mục tiêu / ngoài phạm vi / không được xảy ra

Mục tiêu:
- Đọc, validate, sửa trên popup và ghi được file 10 sheet cho cả THÊM MỚI và CẬP NHẬT.
- Báo đủ lỗi, sửa trên popup rồi validate lại; tải về file lỗi `.xlsx` cùng cấu trúc để sửa và import lại.

Ngoài phạm vi:
- Không còn hỗ trợ mẫu 79 cột (mẫu 10 sheet **thay hẳn**; file cũ upload lên thì báo sai mẫu).
- Không import ảnh, video, tài liệu kỹ thuật (như cũ).
- Không đổi form nhập tay (form vẫn kiểm trùng 4 trường).

Không được xảy ra (giữ của thiết kế cũ + thêm):
- Ô trống làm mất dữ liệu cũ; đổi mã hàng đã có; xoá dòng ĐVT cũ; ghi đè giá hàng Đang kinh doanh.
- Ghi **một phần** một hàng: lỗi ở bất kỳ sheet nào của hàng ⇒ không ghi gì của hàng đó.
- Dòng ở sheet con "mồ côi" bị âm thầm bỏ qua mà người dùng không biết.

## 3. Quyết định

### User quyết định (17/11/2026)

| # | Vấn đề | Quyết định |
|---|---|---|
| V1 | Lỗi ở dòng sheet con | **Từ chối cả hàng** (dòng Sheet 1 + mọi dòng con). Không có chế độ "ghi hàng, bỏ dòng con lỗi" |
| V2 | Kiểm trùng | **5 trường** Tên + Model + Hãng SX + Code đặt hàng + Thương hiệu, cho cả THÊM MỚI và CẬP NHẬT, trong file và trong DB. Thay U7 của thiết kế cũ (4 trường). Form nhập tay vẫn 4 trường — chấp nhận có hàng import qua nhưng mở form sửa bị báo trùng |
| V3 | Popup | Theo đề xuất ở mục 4 (tab theo sheet, lọc theo mã, thêm/xoá dòng con, bảng lỗi có cột Sheet) |
| V4 | Sheet 2 khi CẬP NHẬT | ĐVT có rồi ⇒ cập nhật giá, **hệ số khác DB ⇒ lỗi** (chốt lại 17/11, như form); chưa có ⇒ thêm; có trong DB mà thiếu trong file ⇒ giữ, không xoá; không đổi ĐVT cơ bản |
| V5 | Sheet 8 | Theo mục 6.8 |
| V7 | Công ty quản lý (17/11) | Chốt D10: chỉ công ty đang đăng nhập |
| V8 | File mẫu (17/11) | Dùng file 10 sheet của nghiệp vụ làm file tĩnh, thay `Mau_import_hang_hoa.xlsx`; ngoại lệ có chủ đích với quy ước `buildImportTemplate` (đổi tên sheet `DM_` + chèn dòng ví dụ sẽ lệch mẫu nghiệp vụ) |
| V6 | Các đề xuất còn lại (mục "Claude quyết định") | Đồng ý theo đề xuất |

### Claude quyết định (user đã cho "theo ý bạn", vẫn nên xem lại)

| # | Vấn đề | Quyết định | Lý do |
|---|---|---|---|
| D1 | Mẫu cũ | Thay hẳn bằng mẫu 10 sheet, cùng tên file tĩnh `Mau_import_hang_hoa.xlsx` | Duy trì 2 mẫu song song gấp đôi code validate |
| D2 | Đọc file | Mỗi sheet: dòng 1 header, dòng 2 hướng dẫn, dữ liệu từ dòng 3. Nhận diện sheet theo **thứ tự 1..10 và tên sheet** (bỏ khoảng trắng, không phân biệt hoa thường); header phải khớp bộ cột của sheet đó, sai ⇒ báo sai mẫu, không load. Dòng mà mọi ô trừ STT đều trống ⇒ bỏ qua | Mẫu nghiệp vụ như vậy; Sheet 3 dòng 2 có chữ "STT" thừa ở cột A — dòng 2 luôn bỏ |
| D3 | Khoá nối | Cột Mã hàng hoá (Sheet 1) là khoá; sheet con nối theo giá trị đã trim, phân biệt hoa thường như mã hệ thống. THÊM MỚI là mã tạm, CẬP NHẬT là mã thật. Mã ở Sheet 1 bắt buộc và không được trùng giữa các dòng Sheet 1 (cả THÊM MỚI) | Không có khoá thì không nối được sheet con |
| D4 | Dòng con mồ côi | Mã ở sheet con không có trên Sheet 1 ⇒ lỗi dòng `Không tìm thấy mã ở Sheet 1`. Dòng mồ côi không thuộc hàng nào nên không làm hỏng hàng khác, nhưng **chặn nút Import** cho tới khi xoá/sửa (kể cả bật "Bỏ qua dòng lỗi" thì dòng mồ côi cũng chỉ bị bỏ, được đếm vào số lỗi) | Không được âm thầm bỏ |
| D5 | Đơn vị tính lỗi | Một "hàng" = 1 dòng Sheet 1 + mọi dòng con cùng mã. Pill Tổng/Hợp lệ/Lỗi đếm theo **hàng**, cộng số dòng mồ côi vào Lỗi. Giới hạn 500 **hàng**/file; tổng dòng tất cả sheet ≤ 20.000 | V1 |
| D6 | Cột Tên ở lưới con (Sheet 4,5,6,7,9) | Chỉ tham khảo: hệ thống luôn lấy tên chuẩn theo Mã (DB, hoặc Sheet 1 nếu mã đang tạo cùng đợt). Tên khác ⇒ **không lỗi**, ô tô vàng + tooltip tên chuẩn | Ghi chú file mẫu. Thay C16 của thiết kế cũ (lệch Tên là lỗi) |
| D7 | Cột ĐVT ở lưới con (Sheet 4,5,6) | Phải là ĐVT có trong danh mục (không có ⇒ lỗi). Khác ĐVT của hàng con trong DB ⇒ **cảnh báo** vàng, không chặn; ghi theo ĐVT của hàng con (như form) | Ghi chú file mẫu "cần cảnh báo trên giao diện" |
| D8 | Lưới con trỏ tới hàng mới cùng đợt | Mã ở Sheet 4/5/6/7/9 được là mã tạm của dòng THÊM MỚI trên Sheet 1 cùng file. BE ghi hàng được trỏ tới **trước**; trỏ vòng (A cần B, B cần A, hoặc tự trỏ) ⇒ lỗi cả các hàng trong vòng. Hàng được trỏ tới bị lỗi ⇒ hàng trỏ tới nó cũng lỗi `Hàng <mã tạm> ở Sheet 1 bị lỗi`. Chia lô 50 phải giữ hàng được trỏ tới trong cùng lô hoặc lô trước; FE gửi kèm bảng `mã tạm ⇒ product_id` đã ghi ở lô trước | Ghi chú file mẫu "hoặc từ Sheet 1 (nếu là mã đang tạo mới cùng đợt)" |
| D9 | Một file một loại Hành động | Giữ (luật #12012). Vì vậy D8 chỉ xảy ra trong file THÊM MỚI | Đã chốt trước |
| D10 | Công ty quản lý (Sheet 1, cột mới) | THÊM MỚI: trống hoặc đúng tên công ty đang đăng nhập; công ty khác ⇒ lỗi `Chỉ tạo được hàng cho công ty đang đăng nhập`. CẬP NHẬT: bỏ qua, tô xám | `ProductWriteService::store` luôn gán `company_id` = công ty đăng nhập; tạo hộ công ty khác là luồng chưa có. User chốt V7 |
| D11 | Tính chất hàng hoá (Sheet 1) | Tính chất thật luôn suy từ Loại sản phẩm (cây product_natures). Ô có giá trị mà khác tính chất của Loại SP ⇒ lỗi `Tính chất không khớp Loại sản phẩm (<tính chất đúng>)`. Trống ⇒ bỏ qua. Phân loại xe kích hoạt theo `is_auto_parts` của tính chất suy ra | HRM không lưu tính chất riêng |
| D12 | Sheet 1 các cột đơn | Map 1:1 sang các key form như thiết kế cũ; cột đổi tên: "Chuyển kinh doanh không tính giá" = cờ "Kinh doanh ngay" cũ; "Barcode" = Mã vạch; "Đặc tính sản phẩm" = Tính chất (characteristic); "Đặc điểm" = Thuộc tính sản phẩm; "Đơn vị bảo hành" = Loại bảo hành. Nhà cung cấp nhiều giá trị cách `;` (U9 cũ) | Giữ logic cũ, chỉ đổi nguồn ô |
| D13 | Sheet 2 khi THÊM MỚI | ≥ 1 dòng bắt buộc. Đúng 1 dòng `Đơn vị cơ bản = Có`, hệ số của nó = 1 (trống coi như 1). Dòng `Không` bắt buộc hệ số > 0. Không trùng Đơn vị trong cùng hàng. Thứ tự dòng = thứ tự ĐVT | Ghi chú mẫu "chỉ có 1 ĐVT thì phải là cơ bản" |
| D14 | Sheet 2 khi CẬP NHẬT | Theo V4. Dòng `Có` phải trùng ĐVT cơ bản hiện tại, khác ⇒ lỗi `Không đổi được ĐVT cơ bản`. ĐVT đã có: hệ số trong file khác hệ số DB ⇒ lỗi (không sửa hệ số ĐVT cũ, C10 cũ). ĐVT mới: hệ số > 0 bắt buộc | Dòng ĐVT cũ không sửa/xoá được |
| D15 | Giá ở Sheet 2 | Mỗi dòng ĐVT mang giá của ĐVT đó (bỏ C19 cũ "1 ĐVT có giá mỗi lần"). Quy tắc ghi giá giữ mục 8 thiết kế cũ: quyền 1657 (U6), hàng Đang kinh doanh bỏ cột giá (U3, tô xám), hàng kế thừa giá điền giá ⇒ lỗi, sàn `OwnerPriceFloor` | Mẫu mới cho giá theo từng ĐVT |
| D16 | Lưới 1-N khi CẬP NHẬT | Sheet 3,4,5,6,7,8,9,10: có ≥ 1 dòng của mã ⇒ **thay toàn bộ** lưới đó; không có dòng nào ⇒ giữ nguyên. Không có cách "xoá sạch lưới" qua import | Ticket |
| D17 | Sheet 3 Thuộc tính | Mỗi dòng 1 thuộc tính: Thuộc tính (danh mục, bắt buộc nếu dòng có dữ liệu), Giá trị, Đơn vị (danh mục, không bắt buộc), In tem Có/Không (trống = Không; nhận `có`/`không` không phân biệt hoa thường). Trùng thuộc tính trong 1 hàng ⇒ lỗi | Mẫu có ví dụ "có" viết thường |
| D18 | Sheet 4–7 | Mỗi dòng 1 hàng con: Mã bắt buộc + tồn tại (hoặc mã tạm cùng đợt, D8); Số lượng nguyên dương bắt buộc ở Sheet 4/5/6 (Sheet 7 không có SL); Thành phần chính Có/Không (Sheet 4). Trùng mã con trong 1 lưới của 1 hàng ⇒ lỗi; hàng con = chính nó ⇒ lỗi. Giữ các ràng buộc khác của `ProductRequest` | Như form |
| D19 | Sheet 9 Nhóm máy | Mỗi dòng: Nhóm máy (Loại SP) và/hoặc Mã máy. Có Mã máy mà Nhóm máy trống ⇒ lấy nhóm của máy. Có cả hai mà máy không thuộc nhóm ⇒ lỗi. Tên máy/Nhóm máy tương ứng: tham khảo như D6. Nhóm máy gom unique | Giống `ProductMachineRows` |
| D20 | Sheet 10 Catalog | Mỗi dòng 1 nhánh 4 cấp; Tiểu mục bắt buộc, 3 cấp trên nếu điền phải đúng nhánh (C18/`CatalogBranchGuard` cũ) | Ghi chú mẫu |
| D21 | File lỗi | `.xlsx` sinh ở client (dùng `exceljs`/`xlsx` đã có trong client — người làm chọn), đủ 10 sheet, dòng 1–2 copy header + hướng dẫn của mẫu, giữ độ rộng cột. Gồm mọi hàng bị từ chối (dòng Sheet 1 + **mọi** dòng con, cả dòng con không lỗi) và dòng mồ côi. Cột cuối mỗi sheet "Chi tiết lỗi hệ thống" ghi lỗi của chính dòng đó (nhiều lỗi nối bằng `; `); Sheet 1 thêm tóm tắt `Sheet N dòng M: ...`. Giá trị lấy theo dữ liệu đang trên popup (gồm ô đã sửa). Cảnh báo vàng không đưa vào | Ticket + V1 |
| D22 | Câu lỗi theo ticket | `Mã hàng hóa không tồn tại`; `Từ chối: Hàng hóa đang bị khóa bởi phiếu YCHG <mã> (Trạng thái: <tên>)`; trùng file `Trùng Tên + Model + Hãng SX + Code đặt hàng + Thương hiệu với dòng N`; trùng DB `Đã có hàng hoá cùng Tên, Model, Hãng SX, Code đặt hàng và Thương hiệu: <mã>`; 2 dòng CẬP NHẬT cùng mã ⇒ lỗi ở cả hai. Trạng thái YCHG mở giữ `PriceAskingRequest::OPEN_STATUSES` (đã khớp ticket) | Ticket |
| D23 | Lỗi ở dòng con hiển thị trên Sheet 1 | Dòng Sheet 1 có thêm lỗi tổng `Có lỗi ở Sheet N` (cột Mã) để tab 1 thấy hàng bị chặn | V1 |
| D24 | Hàng công ty khác tạo (U2 cũ) với sheet con | Sheet 2: chỉ ghi cột giá của **ĐVT đã có** (theo U2); dòng ĐVT mới ⇒ lỗi `Hàng công ty khác tạo, không thêm được ĐVT`; hệ số bỏ qua tô xám. Sheet 3–10: bỏ qua, tô xám (như các cột ngoài tab Quản trị ở U2), không lỗi | Giữ nguyên tinh thần U2: công ty lấy về không sửa dữ liệu chung của hàng |
| D25 | Giá từng ĐVT | Lưu đúng số trong file cho ĐVT đó, không suy từ ĐVT cơ bản × hệ số. Sàn `OwnerPriceFloor` so theo cùng ĐVT. Ô giá trống ⇒ giữ giá hiện có của ĐVT đó (CẬP NHẬT) / không có giá (THÊM MỚI). Giá online (loại 6) tính lại như mục 8 thiết kế cũ, theo từng ĐVT | Giống cách cũ gắn giá vào 1 ĐVT, chỉ mở ra nhiều ĐVT |
| D26 | Hàng được trỏ tới lỗi lúc ghi (rollback ở lô trước) | Mọi hàng trỏ tới nó ở lô sau bị từ chối với câu D8, ghi vào bảng lỗi và file lỗi; không dừng cả lượt, **không bao giờ bỏ lặng lẽ** | D8 |
| D27 | Model, Thương hiệu khi CẬP NHẬT | Theo hướng dẫn file mẫu "CẬP NHẬT: bỏ qua" ⇒ bỏ qua, tô xám (không báo lỗi). Hãng SX: khoá như thiết kế cũ. Code đặt hàng: DB trống thì lấy, đã có thì bỏ qua tô xám | Hướng dẫn file mẫu |

## 4. Popup (V3)

Giữ khung `ProductImportModal.vue`: toolbar File / Hành động / Hiển thị, pill, nút Import, "Bỏ qua dòng lỗi", bảng lỗi
có Sao chép, ghi lô 50 tuần tự, chống kết quả validate cũ (`_validateSeq`), 409 khi có lượt khác đang ghi.

Thay đổi:
1. Lưới thành **10 tab** đặt ngay trên lưới, nhãn `N. <tên sheet> (<số dòng>)` + badge đỏ số dòng lỗi; tab không có dòng ⇒ mờ (vẫn bấm được, để thêm dòng).
2. Mỗi tab là một lưới như hiện tại: sửa trên ô, phân trang 50, ô chỉ thành input khi bấm, đỏ = lỗi, xám = bỏ qua, vàng = cảnh báo; cột đầu "Dòng Excel" của sheet đó.
3. Tab 1 mỗi dòng có nút **Xem dữ liệu con**: lọc mọi tab con theo mã đó, có thanh `Đang lọc: <mã> ×`.
4. Sửa ô Mã ở tab 1 ⇒ đổi theo mọi dòng con đang mang mã cũ (và mọi tham chiếu mã tạm ở Sheet 4–7, 9).
5. Tab con có **+ Thêm dòng** (dòng mới mang sẵn mã đang lọc nếu có) và xoá dòng. Xoá dòng ở tab 1 ⇒ hỏi "Xoá luôn N dòng con của mã này?" (Có ⇒ xoá; Không ⇒ dòng con thành mồ côi, D4).
6. Bảng lỗi cột `Sheet | Dòng Excel | Tên cột | Mô tả`; bấm một lỗi ⇒ chuyển tab, bỏ lọc nếu cần, nhảy trang, tô ô.
7. "Chỉ dòng lỗi" áp dụng tab đang mở.
8. "Bỏ qua dòng lỗi" ⇒ FE chỉ gửi các hàng hợp lệ (và bỏ dòng mồ côi). Dòng/hàng đã ghi rời lưới như hiện tại.
9. Tải File lỗi theo D21 (thay CSV).

Payload gửi BE (gợi ý, người làm có thể đổi tên): `{ products: [ { key: <mã Sheet 1>, row: {...sheet1}, units: [...], attributes: [...], kits: [...], accessories: [...], install_materials: [...], repair_materials: [...], vehicles: [...], machines: [...], catalogs: [...] } ], orphans: [...], created_keys: { <mã tạm>: product_id } }`, mỗi dòng con mang `excelRow` + `sheet` để trả lỗi đúng chỗ. Lỗi trả về `{ sheet, excelRow, column, message, level: error|warning }`.

## 5. API

Giữ 2 route và controller. `import` luôn validate lại toàn bộ lô (không tin FE), mỗi **hàng** một transaction (C12 cũ);
hàng lỗi lúc ghi được rollback trọn và báo trong kết quả. Tra danh mục theo lô cho cả file (không query từng ô).
Kết quả ghi trả thêm `created_keys` (mã tạm ⇒ product_id, mã thật) để FE dùng cho lô sau (D8).

## 6. Validate theo sheet

6.1 Sheet 1: như mục 6 thiết kế cũ cho các cột đơn, với V2 (5 trường), D10, D11, D12, D22. CẬP NHẬT: thứ tự chặn
(mã tồn tại → chưa xoá/U2 → khoá → YCHG mở → trạng thái 1|3) giữ nguyên; khoá Model, Hãng SX, Thương hiệu; Code đặt hàng chỉ
điền khi DB trống (C9 cũ). Kiểm trùng 5 trường ở CẬP NHẬT chỉ khi đổi Tên hoặc điền Code. Ô trống giữ, `0` ghi đè.
Cờ Chuyển KD: như thiết kế cũ (THÊM MỚI Có ⇒ Đang kinh doanh qua `tradeWithoutPrice`, Không ⇒ Đang nhập thông tin;
CẬP NHẬT status 1 + Có ⇒ chuyển; status 3 ⇒ bỏ cờ, tô xám).

6.2 Sheet 2: D13–D15. 6.3 Sheet 3: D17. 6.4–6.7 Sheet 4–7: D6–D8, D18. 6.9 Sheet 9: D19. 6.10 Sheet 10: D20.

6.8 Sheet 8 Phân loại xe (V5):
- Mỗi dòng ứng với **một Model xe**, hoặc chỉ khai Hãng xe / Loại xe (không model).
- Hãng xe, Loại xe: nhiều giá trị cách `;`. Model xe: nhiều giá trị cách `;` **chỉ khi** dòng không khai đời xe (ô "Áp dụng tất cả" trống/Không và cột Đời xe trống); dòng có đời xe ⇒ đúng 1 model.
- "Áp dụng tất cả đời xe cho model" = Có ⇒ mọi đời xe hiện có của model (`vehicle_life` thuộc model); Có mà cột Đời xe có dữ liệu ⇒ lỗi. Không/trống ⇒ lấy Đời xe cách `;`.
- Tên Hãng/Loại/Model/Đời xe phải có trong danh mục; Model xe phải thuộc Hãng xe trên cùng dòng (nếu dòng khai Hãng); đời xe phải thuộc model.
- Gom mọi dòng của hàng ⇒ `vehicle_manufact_ids`, `vehicle_brand_ids`, `vehicle_model_ids`, `vehicle_lives` (payload form), ghi qua `ProductWriteService` (`writeVehicles`).
- Hàng có dòng Sheet 8 mà tính chất (suy từ Loại SP) không `is_auto_parts` ⇒ lỗi `Loại sản phẩm không thuộc phụ tùng ô tô – xe máy, không nhập được Phân loại xe` (form thì bỏ qua lặng lẽ; import báo lỗi).
- CẬP NHẬT: có dòng ⇒ thay toàn bộ dữ liệu xe; không dòng ⇒ giữ.

## 7. Ghi dữ liệu

Giữ mục 7 + 8 thiết kế cũ (dựng `$data` theo form → `ProductWriteService::store/update`, trộn dữ liệu hiện tại khi
CẬP NHẬT, `updateAdminPartial` cho hàng công ty khác, lịch sử ghi chú "Import Excel"), đổi:
- Lưới lấy từ sheet con thay vì tách `;`.
- ĐVT theo D13/D14; giá theo D15 cho từng ĐVT.
- Phân loại xe theo 6.8.
- Thứ tự ghi trong lô theo D8 (topo theo tham chiếu mã tạm).

## 8. Việc để người làm tự quyết

- Tách validator theo sheet thành bao nhiêu class; đặt tên key payload.
- Thư viện sinh `.xlsx` ở client.
- Bố cục tab và màu vàng cảnh báo, miễn dùng token sẵn có.
- Có giữ lại code đọc mẫu 79 cột hay xoá (không còn đường dùng).

## 9. Kiểm thử

API test, trọng tâm:
- V1: lỗi 1 dòng con ⇒ không ghi gì của hàng (kể cả các lưới khác), hàng khác vẫn ghi.
- V2: trùng 5 trường trong file và DB; khác Code đặt hàng thì qua.
- Sheet 2: THÊM MỚI nhiều ĐVT + giá từng ĐVT; thiếu/thừa ĐVT cơ bản; CẬP NHẬT thêm ĐVT mới, ĐVT thiếu trong file vẫn còn, đổi ĐVT cơ bản ⇒ lỗi, hàng Đang kinh doanh bỏ giá.
- Full replace từng lưới 3–10; sheet không có dòng ⇒ giữ nguyên.
- Sheet 8: Có tất cả đời xe; danh sách đời xe; model không thuộc hãng; loại SP không phụ tùng ⇒ lỗi.
- D8: công thức trỏ hàng mới cùng file ghi đúng `product_id`; trỏ vòng ⇒ lỗi; hàng được trỏ lỗi ⇒ hàng trỏ lỗi; qua 2 lô.
- D4 mồ côi; D6 tên lệch không lỗi; D7 ĐVT lệch là cảnh báo.
- Khoá YCHG đủ 6 trạng thái mở với câu lỗi mới; D10 công ty khác.
- Giữ pass các test import cũ còn áp dụng (cập nhật một phần, U2, U6, giá hẹn/đề nghị chờ duyệt còn nguyên).

Playwright tại `http://127.0.0.1:3000`: tải mẫu, load file mẫu nghiệp vụ, tab + badge, Xem dữ liệu con, thêm/xoá dòng con,
sửa mã ở tab 1 lan sang tab con, bấm lỗi nhảy ô, validate lại, tải file lỗi mở lại được bằng Excel và import lại được, import xong danh sách cập nhật.

## Phụ lục — cột từng sheet

Bộ cột + hướng dẫn chính xác của 10 sheet (đúng chữ header, dùng để so khớp D2) nằm ở
`HRM/.plans/import-hang-hoa-12174/cot-va-huong-dan-10-sheet.txt`; bản file mẫu nghiệp vụ tải về lúc 17/11/2026:
`HRM/.plans/import-hang-hoa-12174/Mau_nghiep_vu_10_sheet.xlsx`. Sheet 2 có: Mã, Đơn vị, Đơn vị cơ bản, Hệ số quy đổi,
Giá vốn, rồi 5 nhóm (Bán lẻ, Theo lô, ĐL1, ĐL2, ĐL3) × (Hệ số, Giá bán, ĐM đàm phán giá %).
