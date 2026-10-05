# Đợt 2-C — Ghi: bảng chốt

> Nguồn câu hỏi: `yeu-cau-ghi.md` (T1–T11) · `erp-ghi-hang-hoa.md` (khảo sát ERP ghi hàng hoá).

| # | Chốt (04/10/2026) |
|---|---|
| T6 | **Hệ số công nghệ (`products.tech_coefficient`) DÙNG CHUNG các công ty** — là thông tin chung của mã hàng, không tách theo công ty, không thêm cột vào `product_company_coefficients`. (Đang hiện ở tab *Quản trị hàng hoá* — quyền sửa theo luật thông tin chung: chỉ công ty tạo.) |
| H1' | **Chưa có luồng Tính giá ⇒ CHƯA có đường chuyển *Đang nhập thông tin → Chờ tính giá*: hàng TREO ở *Đang nhập thông tin*, chờ phase Tính giá.** Bấm Lưu KHÔNG đổi trạng thái (khác mockup `luuVaChuyen` và §26a). Hệ quả: nút tạm "Chuyển kinh doanh" (H1, 2 → 3) không có hàng nào để dùng ⇒ KHÔNG làm ở 2-C |
| H1'' | User xác nhận: **bỏ nút tạm "Chuyển kinh doanh" (H1)**. Hàng HRM tạo mới nằm ở *Đang nhập thông tin* tới phase Tính giá; bật HRM thật chỉ khi đã có Tính giá (hoặc ERP vẫn tạo hàng song song tới lúc đó) |

## Câu còn mở (gộp từ `yeu-cau-ghi.md` T1–T11 + `erp-ghi-hang-hoa.md` R1–R12), xếp theo mức ảnh hưởng

| # | Câu | Vì sao |
|---|---|---|
| G1 | `products.status` của hàng HRM tạo mới (T2/R7/R8) | popup 338 màn ERP lọc `status != 0` ⇒ status 1/2 là hàng *Đang nhập thông tin* chọn được ngay trong chứng từ ERP |
| G2 | Đơn vị cơ bản + 6 dòng giá (bất biến ERP, R-4) | thiếu ⇒ hàng biến mất khỏi danh sách ERP + popup 404 (`firstOrFail` ~290 chỗ) |
| G3 | Lưu nháp (T1) | DB buộc code/name/brand/manufacture/origin/created_by; với H1' Lưu không đổi trạng thái ⇒ Lưu nháp thừa? |
| G4 | Sửa tab Quản trị của hàng CŨ (T3) | phải sinh dòng hàng × công ty `coefficient=1` ⇒ giá popup ERP của mã đó làm tròn nghìn |
| G5 | Ghi kép `min_stock_qty`/`guarantee` sang cột chung (T4) | ERP đọc cột chung ở 29/42 file, chép bảo hành sang chứng từ |
| G6 | Khoá/Mở khoá (T5/R1) | ERP không phân biệt khoá với xoá (`status=0`) |
| G7 | Xoá (T8) | chứng từ tính gì, mềm/cứng, gỡ dòng có hệ số cũ |
| G8 | Sao chép (T9) | sao những gì |
| G9 | Lối vào sửa (T10) + câu nhỏ (T11) | |
| G10 | Phạm vi 2-D (R2/R3/R10) | màn Hãng SX/Thương hiệu ERP ghi đè dữ liệu; route trắng; cron giá — để lúc plan 2-D |
| G1 | **`products.status = 1`** cho hàng HRM tạo mới (giống ERP hiện nay) — chấp nhận hàng *Đang nhập thông tin* chọn được ngay trong popup 338 màn ERP. Trạng thái quy trình vẫn ở dòng hàng × công ty (status 1) nên HRM không bị luật suy ra đè |
| G2 | **Ghi đủ 6 dòng `product_unit_prices` giá 0, hệ số 0** cho mỗi đơn vị (kể cả đơn vị cơ bản); `product_units.cost_price`/`buy_price` = 0 ghi tường minh (HRM chạy MySQL strict). Sửa hàng cũ: KHÔNG đụng dòng giá đã có, chỉ bù 6 dòng cho đơn vị mới thêm. Đúng 1 đơn vị cơ bản (hệ số 1) |
| G3 | **Chỉ 1 nút Lưu**, bỏ Lưu nháp. Lưu bắt buộc đủ trường bắt buộc của form, validate báo đồng thời mọi ô; không đổi trạng thái. Nút chuyển bước thêm ở phase Tính giá |
| G4 | Lưu tab Quản trị của hàng CŨ chưa có dòng ⇒ **sinh dòng hàng × công ty `coefficient = 1`, `status = 3`** (khớp trạng thái đang suy ra). Chấp nhận mã đó bị làm tròn nghìn ở popup ERP (như K2). Ghi chú: popup Xây dựng catalog chỉ ghi `product_business_catalogs`, KHÔNG cần sinh dòng ⇒ xếp catalog không làm đổi giá |
| G5 | **Không ghi kép** sang cột chung. User 04/10: *"Các vấn đề phát sinh ngoài luồng hàng hoá note lại để xử lý tại chức năng đó sau. Sẽ fix hết rồi mới merge vào nhánh prod"* ⇒ HRM chỉ ghi theo công ty; chỗ ERP đọc cột chung (29 + 42 file) ghi vào danh sách việc ngoài luồng bên dưới |

## Việc ngoài luồng hàng hoá — note lại, xử lý tại chức năng đó, PHẢI xong trước khi merge prod

| # | Việc | Nguồn |
|---|---|---|
| N1 | 29 file ERP đọc `products.min_stock_qty` + 42 file đọc `guarantee`/`guarantee_type` (chép sang 23 bảng chứng từ) ⇒ đổi sang đọc dòng theo công ty của chứng từ | §24c, G5 |
| N2 | Màn Hãng SX ERP (`ManufacturesController:185,:270`) ghi đè `company_id` + xoá sạch dòng hàng × công ty của mọi hàng thuộc hãng | 2-A K2, R2 |
| N3 | Màn Thương hiệu ERP (`Brand::updateProducts`) ghi đè `company_id` | R2 |
| N4 | Chặn route `products/*` ERP phải chừa danh sách trắng (`updateEnglishName`, `updateHSCode`, `getData` từ màn mua hàng/popup) | R3 |
| N5 | Cron đưa giá về 0 khi hết tồn lọc theo `products.company_id` + `product_cate` ⇒ bỏ sót hàng HRM tạo | R10 |
| N6 | Cron `sync:crm` chỉ đẩy hàng có `product_template_id` ⇒ hàng HRM tạo không sang CRM | erp-ghi-hang-hoa.md |
| N7 | Hàng HRM tạo `group_id` NULL ⇒ `->group->` trong SearchController (popup 338 màn) lỗi | 2-D |
| N8 | Khoá theo công ty (G6) chỉ HRM biết — popup ERP vẫn cho chọn hàng công ty đã ngừng kinh doanh | G6 |
| G6 | **Khoá theo CÔNG TY**: thêm trạng thái **4 "Ngừng kinh doanh"** trên dòng hàng × công ty (badge `#DC2626`). Mặc định đề xuất (user có thể sửa khi duyệt plan): chỉ khoá được từ *Đang kinh doanh* (3 → 4), mở khoá về 3; quyền 1652 của chính công ty; hàng cũ chưa có dòng ⇒ sinh dòng `coefficient=1` status 4 (như G4). Đã khoá thì BE chặn sửa tab Quản trị (423) tới khi mở khoá (CLAUDE.md). Màn *Đang kinh doanh* + cột *Công ty đang kinh doanh* không tính hàng status 4. ERP KHÔNG biết khoá này ⇒ việc ngoài luồng N8 |
| G7 | **Xoá = kiểm như ERP (5 điều kiện `canDelete`) + điều kiện §35b-4, qua hết thì XOÁ CỨNG** hàng + mọi bảng con (đơn vị, 6 dòng giá 0, dòng công ty, catalog, thuộc tính, phụ kiện, productables theo `productable_type`…) trong 1 transaction; FK 171 bảng là chốt chặn cuối. Hàng công ty khác đã lấy về thì "xoá" = gỡ dòng của công ty mình (dòng có hệ số cũ thì trả `status` về NULL, giữ `coefficient`) + catalog của công ty mình — không đụng `products` |
| G8 | **Sao chép: làm sau** (không thuộc 2-C) |
| G9a | **Nút Sửa ở menu dòng + footer màn chi tiết** (quyền 1652, khớp danh sách = chi tiết) cho hàng mọi trạng thái; công ty tạo sửa mọi tab, công ty lấy về chỉ tab Quản trị; đang Ngừng KD (4) thì ẩn Sửa tới khi mở khoá |
| G9b | Đồng ý: (1) Lấy về hàng loạt trần **100 mã/lượt**; (2) **không cho lấy về** hàng `products.status ≠ 1`; (4) toast Lưu bỏ vế "lập Yêu cầu tính giá". (3) xem G11 |
| G11 | 🔄 **Cờ "Phụ tùng ô tô" đặt ở TÍNH CHẤT HÀNG HOÁ** (thay §18b — bỏ 2 cờ ở Loại sản phẩm): thêm cột (vd `is_auto_parts`) vào `product_natures` + ô tick ở màn danh mục Tính chất hàng hoá. Tab *Phân loại xe* chỉ hiện khi Tính chất (suy từ Loại sản phẩm đã chọn) có tick; Hãng xe không bắt buộc. Tab *Nhóm máy* **luôn hiện** |
| G10 | Phạm vi 2-D (N2–N7) — chốt lúc lập plan 2-D |

⏳ Tồn nhỏ chốt lúc plan 2-C2: màn *Kho dữ liệu* (2-B) đang hiện cả 17.512 hàng ERP đã xoá/khoá (`products.status = 0`) với nhãn "Chưa sử dụng" — có lọc bỏ không.

## Chốt riêng đợt 2-C3 (popup Xây dựng catalog — đặc tả `c3-popup.md`)

| # | Chốt (04/10/2026) |
|---|---|
| B1 | **Giữ giỏ chờ như mockup + 1 endpoint `sync`**: Lưu gửi cả giỏ (cặp thêm + gỡ, nhiều Tiểu mục) chạy trong 1 transaction — sai 1 cặp thì không lưu gì. Trần **100 mã / mỗi lượt tick** (mockup); mỗi lần Lưu tối đa **1.000 cặp** thay đổi. Đóng popup khi giỏ còn ⇒ cảnh báo chưa lưu. Endpoint `assign`/`unassign` đã viết thay bằng `sync` |
| B2 | **Khoá bất kỳ cấp nào (Lĩnh vực/Chương/Mục/Tiểu mục) = không xếp THÊM** vào nhánh đó: hiện 🔒, không chọn để thêm; vẫn mở tab *Hàng trong tiểu mục* để xem + GỠ. BE chặn tương tự (xét cả 4 cấp) |
| B3 | Hàng **Ngừng kinh doanh (4)**: **ẩn khỏi tab Thêm** (không xếp mới); tab *Hàng trong tiểu mục* vẫn hiện để gỡ. Ô lọc Trạng thái: tab Thêm 3 lựa chọn (1·2·3 — chưa có "Đang tính giá"), tab trong tiểu mục thêm "Ngừng kinh doanh" |
| B4 | "Thông số cơ bản" = **mọi thuộc tính có giá trị** (`attribute_products`), thứ tự `attributes.position`, ghi `Tên: giá trị đơn vị` |
| B5 (tự chốt) | Popup loại hàng `products.status = 0`; số đếm trên cây = số hàng CỦA CÔNG TY đang xếp trong nhánh (đã lưu) ± giỏ chờ |
