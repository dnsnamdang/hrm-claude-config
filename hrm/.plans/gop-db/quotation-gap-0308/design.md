# Báo giá QLDA — sửa theo file GAP 0308 (design tóm tắt)

> @cuong61n · nhánh `gop_db` · bắt đầu 26/10/2026
> Nguồn: Google Sheet "GAP_baogia_qlda_erp" tab `bao_gia_QLDA_0308` (bản tải về + ghi chú kết quả: `GAP_baogia_qlda_erp_ghichu_2710_v11.xlsx` cùng thư mục – bản duy nhất). KHÔNG sửa trên link gốc.

## Quyết định (AI đề xuất, cần user xác nhận khi review)
1. ~~Nhu cầu = danh mục ERP chọn nhiều~~ → (chốt 27/10, sửa 28/10) Nhu cầu = 1 nhu cầu Meeting (`quotations.customer_demand_id` → `meeting_investment_demands`), chọn được ở CẢ báo giá độc lập lẫn có dự án: danh sách = nhu cầu Đang theo dõi từ mọi meeting của KH (có dự án: KH của dự án + nhu cầu đang gắn dự án, điền sẵn), nhãn kèm mã meeting + ngày họp; bắt buộc khi Gửi duyệt; không đổi trạng thái nhu cầu. Chưa lọc theo loại/trạng thái meeting (chờ user).
2. Địa chỉ giao hàng = ô nhập text `quotations.delivery_address`; bắt buộc khi Gửi duyệt.
3. File đính kèm = bảng `files` table='quotations', description 'Tài liệu đính kèm' (tách với file xác nhận chốt).
4. Cột Ảnh + Thời gian bảo hành trên lưới báo giá: lấy `image`/`warranty` BE đã trả, hiện trong nhóm "cột chi tiết".

## Ngoài phạm vi đợt này (cần chốt nghiệp vụ) — xem ghi chú trong file Excel
Loại báo giá (1)/(2), Báo giá mẫu / Dữ liệu mẫu, BOM mẫu, GG phân quyền theo phòng, Hàng tự khai thác, quyền lập HĐ theo thành viên dự án, TSKT chính, phần lớn tuỳ chọn In.

## Chương trình khuyến mại (GAP dòng 34 + 46) — port luồng ERP
Nguồn: ERP `FirmQuotation*` (form.blade "Chương trình khuyến mãi", class JS FirmQuotationCombo*, `ComboCategory::checkActive`).
- Danh mục KM đọc thẳng DB gộp (`combo_categories`, `combo_campaigns`, checkpoint/group/option/option_products, `combo_campaign_groups`), KHÔNG mysql2.
- Lọc chương trình áp dụng = đúng `checkActive` ERP: approved, status=1, còn hạn, is_old_campaign=0; phạm vi công ty/phòng ban của NGƯỜI LẬP báo giá (chưa có báo giá → người đang đăng nhập); nhóm khách hàng của KH báo giá.
- 3 kiểu mã: `0` mã KM đơn lẻ (SL mua = Σ SL từng hàng) · `1` combo (SL combo × SL cần mua) · `2` quà tặng theo nhóm mã (SL = Σ SL các mã trong nhóm).
- Mốc tặng: mọi mốc có floor(SL/mốc) > 0 đều được chọn; ràng buộc Σ(SL chọn × mốc) ≤ SL mua; SL quà × SL chọn ≤ SL còn lại (max_qty − used_qty).
- Lệch ERP (có chủ đích): (a) HRM không tự sinh tab "Hàng mua theo …" — SL mua nhập ở mục KM và **Σ SL mua của 1 mã hàng (mọi CTKM, quy đổi ĐVT) ≤ SL mã đó trong báo giá**; (b) nhập vượt thì báo đỏ dưới ô, KHÔNG tự kéo về max như ERP; (c) chỉ lấy mã KM status=1.
- Hàng tặng 0đ, không ảnh hưởng tổng tiền. Lưu `quotation_promotions` (1 dòng/mã KM, JSON products/groups); BE tự dựng lại tên/SL quà từ danh mục, không tin FE.
- KHÔNG đồng bộ sang ERP (chốt 27/10/2026: làm báo giá trên HRM; ERP vẫn chạy song song, lâu dài mới bỏ). Đã gỡ mọi sửa đổi đồng bộ làm ngày 26/10 (HRM `QuotationErpSyncService` + `erpPayload`, ERP `FirmQuotationSyncController` / `SyncFirmQuotationFromHrmRequest`). Luồng đồng bộ cũ đang lỗi → để nguyên, không sửa.
- Kiểm tra lại khi Lưu và khi Gửi duyệt (chương trình hết hạn / SL dòng hàng thay đổi → 422 gắn đúng ô).

## Phase 3 — quyết định đã chốt (27/10/2026)
- Báo giá mẫu / Dữ liệu mẫu: đọc mẫu ERP (`project_quotations` is_template / `quotation_templates`), mẫu vẫn tạo/sửa trên ERP; chọn = thay hết; áp báo giá mẫu bỏ KM đang chọn.
- BOM mẫu: bảng riêng `bom_templates*`, màn quản lý riêng, quyền "Quản lý BOM mẫu", dùng chung mọi công ty, khoá/mở khoá, xoá cứng khi chưa khoá (CHỜ user xác nhận điều kiện xoá).
- Tồn kho: Tồn có thể bán theo công ty (SellableStockReader) + Có thể LR / Đang giữ (ProductStockExtraReader, port ERP getJoinStockDetail / prepick theo người lập + KH).
- Hàng tự khai thác: `product_cate` = `hang_tu_khai_thac`, gắn ở TempProductService::create; khai cả ERP (7 file).
- In: tuỳ chọn trong QuotationPrintConfigModal (dùng chung 4 màn), dữ liệu mở rộng `GET assign/quotations/{id}/print-extras`.
- Để sau: tạo hợp đồng (dòng 61), TSKT chính (dòng 62).
