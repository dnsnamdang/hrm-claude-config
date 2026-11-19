# Bảng giá bán hàng hoá hiện hành — Design (tóm tắt)

> Người phụ trách: @dnsnamdang · Nhánh: `gop_db` (hrm-api + hrm-client) · Tạo 28/10/2026
> Spec chi tiết: `docs/superpowers/specs/gop-db/2026-10-28-bang-gia-ban-hien-hanh-design.md`

_(placeholder — điền sau brainstorming)_

## Yêu cầu gốc (28/10/2026)
- Báo cáo "Bảng giá bán hàng hoá hiện hành": giá bán + giá vốn đang áp dụng + giá hiệu lực của từng mã hàng theo Công ty
- Phân quyền: quyền xem theo tổng công ty ⇒ xem giá mọi công ty; không có ⇒ chỉ công ty đang làm việc; quyền xuất Excel/In báo cáo

## Quyết định đã chốt (brainstorm 28/10/2026)
- Màn chỉ xem/in/xuất; mỗi lần xem **1 công ty**; chỉ hàng **Đang kinh doanh**; 1 dòng / mã hàng.
- Cột: STT · Mã · Tên · Hãng SX · Thương hiệu · Model · ĐVT (ô chọn, mặc định ĐVT cơ bản) · Giá vốn (có quyền) · 6 loại giá.
- Giá sắp áp dụng: phương án **A** — dòng phụ **chữ xanh dương #2563EB** (user muốn đỏ, đối chiếu quy ước "đỏ chỉ cho lỗi" ⇒ chốt xanh) `→ giá · ngày` trong ô giá. Mỗi loại giá tối đa 1 giá sắp áp dụng (nghiệp vụ).
- Bộ lọc theo skill list-page (`V2BaseSmartFilterPanel` floating, Cài đặt bộ lọc, chọn xong tìm luôn / ô gõ Enter); khối nâng cao KHÔNG có tiêu đề nhóm. **Ô Công ty KHÔNG nằm ở hàng tìm nhanh**: "Mã - Tên công ty" đang xem hiện ở tiêu đề bảng; ô Công ty chỉ có (ô cuối khối nâng cao) với người có quyền tổng công ty. Các ô: tìm nhanh · Catalog 4 cấp (theo công ty đang xem) · Phân loại 4 cấp · Hãng SX · Thương hiệu · Model · tick "Chỉ hàng có giá sắp áp dụng".
- Quyền: mọi NV xem công ty mình (giá bán công khai) · MỚI "Xem bảng giá bán theo tổng công ty" · MỚI "In/Xuất Excel bảng giá bán" · có sẵn "Xem giá vốn hàng hoá" (không có ⇒ ẩn cột + BE trả null).
- Menu: Tài chính › Quản lý giá - CTKM › Giá bán, ngay sau "Duyệt giá bán". Không isShow.
- In/Xuất: dùng popup chung **`components/modal/export-fields-modal.vue` ("Chọn trường xuất file")** — tick sẵn đúng các cột đang hiện trên bảng theo thứ tự bảng (list-page 14b), thêm/bớt/kéo được. **User chốt phương án 1: MỞ RỘNG popup chung** thêm slot tuỳ chọn (màn khác không truyền ⇒ không đổi) để đặt **Chỉ ĐVT cơ bản / Tất cả ĐVT** + tick **"Kèm giá sắp áp dụng"** (mặc định bật). In dùng cùng popup (tiêu đề "Chọn trường in", nút Xem trước — Claude chốt). STT luôn có trong file. Excel cách (a): mỗi loại giá thêm cột "Sắp áp dụng" + "Từ ngày", ô số thật.
- **Cấu hình cột hiển thị** (user thêm 28/10): khuôn list-page §5 (`columnCustomizationMixin` + `ColumnCustomizationModal`), khoá STT + Mã hàng; mặc định hiện đủ cột; cột Giá vốn chỉ có trong popup khi có quyền.
- **Sắp xếp theo cột** (user thêm 28/10): mọi cột trừ STT + ĐVT, sắp ở BE (phân trang). Mặc định Mã hàng tăng dần. Cột giá / giá vốn sắp theo giá của **ĐVT cơ bản** (Claude chốt — ĐVT chọn ở từng dòng chỉ là hiển thị).
- **Sau builder check (28/10)**: giá ≤ 1 đ = chưa có giá ⇒ ô trống, lịch giá 1 đ không hiện/không lọc/không xuất · quyền giá vốn xét **tại công ty đang xem** · deploy hiện menu ngay (không key ẩn) · ô trống xếp cuối cả 2 chiều sắp.
- **Nhãn loại giá 6 = "Thương mại điện tử"** (28/10, lúc chạy e2e): mockup ghi "TMĐT" nhưng màn Cập nhật/Duyệt giá + file Excel/bản in dùng "Thương mại điện tử" ⇒ trang theo khuôn có sẵn.
- **Chốt khi code (28/10, review cuối đồng ý)**: Excel tiêu đề 1 hàng ghép "<Loại> - Hiện tại / Sắp áp dụng / Từ ngày" (util dùng chung `listExportFile` chỉ 1 hàng tiêu đề), cột "Từ ngày" là chuỗi dd/mm/yyyy · popup Xuất có tiêu đề "Chọn trường xuất Excel" (như 3 màn công nợ), In là "Chọn trường in" + nút "Xem trước" · response danh sách không có `base_unit_id` — ĐVT cơ bản luôn đứng đầu `units[]` · catalog lọc = nhánh có hàng xếp ở công ty xem · giá vốn ≤ 0 = trống · không sửa `ProductPriceListService` / `PermissionService` (service riêng `ProductPriceBoardService`).
- **Phase 3 (28/10, góp ý sau khi xem màn)**: hàng đầu khối nâng cao Công ty · Hãng SX · Thương hiệu · Model; Catalog / Phân loại là bộ lọc TUỲ CHỌN (ẩn mặc định, cờ `defaultHidden` mới của `V2BaseSmartFilterPanel`); cột mặc định STT · Mã · Tên · ĐVT · 6 cột giá, Hãng SX / Thương hiệu / Model / Giá vốn là cột tuỳ chọn; ô tìm nhanh ~40% hàng; công tắc "Chỉ hàng sắp thay đổi giá".
- **Phase 4–6 (28/10)**: cột Mã / Tên / Hãng SX / Thương hiệu / Model hiện ĐỦ chữ (xuống dòng, bỏ "…" + tooltip) · nút **Lịch sử giá** (icon cạnh Mã hàng) mở `ProductPriceHistoryModal` theo công ty xem — ai vào bảng giá đều xem được, Giá vốn + Hệ số chỉ khi có quyền giá vốn tại công ty xem, công ty khác cần quyền tổng công ty · độ rộng: giá 160 (dòng phụ giữ 1 dòng — user chọn), Mã 230, Tên 320, Hãng 200, Model 210, ĐVT 90.
- **Bổ sung 04/11/2026 — Định mức đàm phán + Thuế VAT** (user chọn phương án đề xuất): ĐMĐP = `product_unit_prices.sale_max_percent` THEO TỪNG LOẠI GIÁ (các loại giá lệch % ở 93,472/173,480 ĐVT) ⇒ dòng phụ xám #6b7280 11px "ĐMĐP x%" trong mỗi ô giá, chỉ khi có giá, 0% vẫn hiện · Thuế VAT = `products.vat_percent` (1 giá trị/hàng) ⇒ cột "Thuế VAT (%)" ẩn mặc định, sắp được (`sort_by=vat`) · Excel/In: trường `vat` + cột "<Loại> - ĐMĐP (%)" luôn đi sau mỗi loại giá (không có tuỳ chọn tắt); bản in dòng "ĐMĐP x%" dưới giá. Push gop_db: api `69bb71323` · client `43390a2b3`.
- Giữ nguyên màn ERP "Hàng sắp điều chỉnh tăng giá".
- Mockup: `mockup-bang-gia.html` (cùng thư mục).
