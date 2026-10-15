# Brief B — Màn Báo giá (Tạo mới / Chỉnh sửa / Sao chép): Thông tin chung + Bảng chi tiết + Công thức + Thay đổi giá

> Nguồn: đọc code nhánh gop_db. Viết tắt đường dẫn:
> - **FE** = `/Users/manhcuong/Desktop/dns/HRM/worktrees/gop_db-client/pages/assign/quotations/_id/edit.vue` (form dùng chung; `create.vue` chỉ `extends` file này)
> - **POP** = `.../pages/assign/quotations/components/QuotationProductSearchModal.vue` (popup thêm hàng hoá / dịch vụ)
> - **PEM** = `.../components/QuotationProductEditModal.vue` (popup Sửa hàng tạm)
> - **CPM** = `.../components/QuotationCopyPreviewModal.vue`, **MIX** = `utils/mixins/Assign/QuotationCopyMixin.js`
> - **CCP** = `pages/assign/components/cost/CostCatalogPanel.vue`, **CQC** = `.../cost/CostQuickCreateModal.vue`
> - **LPW** = `components/assign/quotation/QuotationLowPriceWarningModal.vue`, **VBT** = `.../VatBulkApplyToolbar.vue`, **VFP** = `.../VatFirstEntryPromptModal.vue`
> - **SVC** = `/Users/manhcuong/Desktop/dns/HRM/worktrees/gop_db-api/Modules/Assign/Services/QuotationService.php`
> - **CTL** = `.../Modules/Assign/Http/Controllers/Api/V1/QuotationController.php`
> - **REQ-S / REQ-U** = `.../Http/Requests/Quotation/QuotationStoreRequest.php` / `QuotationUpdateRequest.php`
>
> Thuật ngữ nghiệp vụ dùng trong brief: **Giá nhập = Giá vốn** (cột `estimated_price`), **Giá bán = Đơn giá bán** (`quoted_price`). **Hàng ERP** = hàng có trong danh mục hàng hoá ERP; **Hàng tạm** = hàng chưa có trong danh mục (người dùng tự nhập). **Báo giá tự lập** = không chọn BOM (type 2) — được thêm/sửa/xoá dòng; **Báo giá từ BOM** = chọn BOM tổng hợp đã duyệt (type 1) — cấu trúc khoá, chỉ sửa giá.

---

## 0. Ba chế độ màn hình & ai được sửa

| Chế độ | Cách vào | Đặc điểm | Nguồn |
|---|---|---|---|
| Tạo mới | nút Thêm mới / từ dự án (`?project_id=`) | Tiêu đề "Tạo báo giá"; Mã = "(Chưa tạo)"; Trạng thái hiển thị "Đang tạo" | FE:2301-2375, 1614-1615 |
| Chỉnh sửa | mở báo giá | Tiêu đề "Làm giá: **<mã>** (<trạng thái>)" | FE:1614-1623 |
| Sao chép | nút Sao chép báo giá → màn Tạo mới `?copy_from=<id>` | Điền sẵn theo bản nháp BE dựng (chưa ghi DB); có dòng "Sao chép từ" | FE:2416-2487, MIX |

- **Được sửa (canEdit)**: Tạo mới luôn được; Sửa chỉ khi trạng thái = **Đang tạo** VÀ người đang đăng nhập là **người tạo** (FE:1715-1720). BE chặn tương ứng: "Báo giá không ở trạng thái Đang tạo, không thể sửa." / "Chỉ người tạo báo giá mới có thể sửa." (SVC:4719-4727).
- Không sửa được → banner vàng: "Báo giá ở trạng thái (<tên trạng thái>) — không cho phép sửa." và mọi ô khoá (FE:7-11).
- Tạo báo giá cho dự án: chỉ **Sale phụ trách dự án** (BE 403 "Bạn không phải Sale phụ trách dự án này"); lập từ YCBG thì cần quyền "Xây dựng giá bán theo phòng/công ty" (CTL:244-302). Dự án cha bị chặn: "Dự án cha không lập báo giá riêng. Vui lòng tạo báo giá trên dự án con, hoặc dùng Báo giá tổng ở màn dự án cha." (Concerns/RejectsParentProject.php).
- Cảnh báo "rời trang khi chưa lưu" CHỈ bật cho bản Sao chép chưa lưu (FE:2499-2519).

---

## 1. Khối "Thông tin chung" (FE:13-255)

Khối thu gọn/mở được (bấm tiêu đề). Dạng bảng 2 cột nhãn–giá trị.

| Nhãn trên UI | Control | Bắt buộc | Mặc định / nguồn | Sửa được khi | Ghi chú / ràng buộc | Nguồn |
|---|---|---|---|---|---|---|
| Mã báo giá | chữ (đọc) | — | "(Chưa tạo)" khi tạo; mã do hệ thống sinh lúc Lưu | không | | FE:23-24, SVC:154 |
| YCBG | link mở popup chi tiết YCBG | — | mã YCBG | không | Chỉ hiện với báo giá từ BOM (không phải tự lập). Bản sao KHÔNG kế thừa YCBG | FE:25-36, SVC:530-534 |
| Sao chép từ | chữ xám | — | "<mã BG nguồn> — báo giá mới chỉ được tạo sau khi bấm Lưu" | không | chỉ có ở bản Sao chép | FE:41-47 |
| Dự án | Select tìm kiếm, placeholder "Tìm dự án...", có nút xoá (x) | FE: dấu `*` chỉ hiện ở bản sao chép đã lưu; BE: không bắt buộc (nhưng không có dự án thì bắt buộc Khách hàng) | Nhãn option "Mã — Tên". Danh sách = dự án mà mình là Sale phụ trách, loại dự án cha, tối đa 50 (`getAll?per_page=50&main_sale_mine=1&for_quotation=1`) | Tạo mới; bản Sao chép (đang tạo, người tạo) | Màn Sửa thường: hiện link tên dự án mở tab mới (chỉ đọc). Bản sao chép chỉ liệt kê dự án **chưa có BOM tổng hợp đã duyệt** | FE:48-86, 4700-4714; REQ-S |
| BOM tổng hợp | Select "Chọn BOM..." có nút x | không | BOM tổng hợp cấp giải pháp **đã duyệt** của dự án | chỉ màn Tạo mới | Chưa chọn dự án: "Chọn dự án trước"; dự án không có: "Không có BOM tổng hợp đã duyệt". Dự án có đúng 1 BOM ⇒ tự chọn + nạp hàng (nếu đã có tiền tệ) | FE:89-103, 4903-4931 |
| Giải pháp / Hạng mục / BOM | chữ/link (đọc) | — | theo BOM | không | chỉ màn Sửa báo giá từ BOM | FE:104-132 |
| Khách hàng | Có dự án: chữ (đọc, lấy theo dự án). Không dự án: nút "Chọn khách hàng" / "Đổi khách hàng" mở popup chọn KH | Bắt buộc khi không chọn dự án (FE `*` + BE `required_without_all:project_id,pricing_request_id`) | | Tạo mới không dự án | Dòng gợi ý xám: "Không chọn dự án = báo giá không gắn Dự án TKT, khách hàng chọn trực tiếp." Lỗi: "Bắt buộc phải nhập" + toast "Vui lòng chọn dự án hoặc khách hàng trước khi tạo báo giá" | FE:133-157, 3910-3916 |
| MST | đọc | — | snapshot KH | không | | FE:161-162 |
| Email khách hàng | ô nhập (email), placeholder "Nhập email khách hàng" | không | email KH / dự án | khi canEdit | BE: email hợp lệ, ≤255 ký tự ("Định dạng email không hợp lệ") | FE:163-173, REQ-S |
| Địa chỉ, SĐT liên hệ, Người liên hệ | đọc | — | snapshot dự án; không dự án: địa chỉ KH, SĐT = di động KH, Người liên hệ trống | không | | FE:175-183, SVC:2574-2609 |
| Giao hàng (ngày) * | ô số | Bắt buộc khi **Gửi duyệt** (FE, phải > 0). Lưu nháp không bắt buộc; BE không bắt buộc | trống | canEdit | "Vui lòng nhập thời gian giao hàng" | FE:184-190, 3668-3670 |
| Hiệu lực báo giá | chữ (đọc, ngày dd/mm/yyyy) | — | **Tự tính** (xem §4a) | không | Nếu khác ngày đã lưu: kèm "(đã lưu: dd/mm/yyyy)" | FE:193-197, 1802-1815 |
| Loại tiền tệ * | Select "Chọn loại tiền", có x | Bắt buộc khi Gửi duyệt (FE) | Có dự án: tiền tệ dự án; không dự án: **VNĐ** | Chỉ khi Tạo mới (hoặc đang đổi dự án trên bản sao) VÀ không phải dự án con | "Vui lòng chọn loại tiền tệ"; danh mục `assign/bom-lists/currencies` | FE:198-212, 2399-2405 |
| Bảo hành (tháng) | ô số | không | trống | canEdit | | FE:215-218 |
| Bảng giá * | Select "Chọn bảng giá", có x | Bắt buộc (FE khi Gửi duyệt; BE `required|in:1..6` khi tạo) | **1 = Bán lẻ** | Như Loại tiền tệ | Danh mục ERP `price_types` (6 loại: Bán lẻ / Đại lý cấp 1-3 / Giá bán theo lô / Giá bán TMĐT), cache 10'. "Vui lòng chọn bảng giá" | FE:220-234, CTL:933-948 |
| Giai đoạn dự án * | Select giai đoạn (kèm icon ⓘ mô tả) | Bắt buộc khi Gửi duyệt (FE + BE); lưu nháp được để trống | giai đoạn hiện tại của dự án | canEdit | Chỉ hiện khi có dự án. "Vui lòng chọn giai đoạn dự án". Gửi duyệt mới đồng bộ ngược về dự án | FE:239-253, SVC:3804-3806, 3889-3892 |
| Điều khoản báo giá * (khối cuối "Thanh toán & Ghi chú nội bộ") | Select "Mẫu điều khoản báo giá" + trình soạn thảo | Bắt buộc khi Gửi duyệt | trống | canEdit | Chọn mẫu khi ô đã có nội dung → xác nhận "Xác nhận thay đổi mẫu điều khoản" / "Nếu bạn thay đổi mẫu điều khoản, thông tin điều khoản báo giá sẽ bị thay đổi! Bạn có chắc chắn muốn thực hiện?" [Xác nhận]. Lỗi "Vui lòng nhập điều khoản thanh toán"; BE "Vui lòng nhập điều khoản thanh toán trước khi gửi duyệt." | FE:1164-1186, 2976-3006 |
| Ghi chú nội bộ (chỉ nội bộ) | trình soạn thảo | không | | canEdit | | FE:1187-1196 |

**Dự án CON** (dự án có dự án cha): Loại tiền tệ, Bảng giá, Phương thức giảm giá **kế thừa từ dự án cha và khoá**; BE ghi đè dù client gửi gì (SVC:121-128, 140-142). Bảng giá dự án con: lấy của dự án; dự án không khai thì lấy theo báo giá mới nhất của dự án cha; không có nữa → Bán lẻ (SVC:2626-2644). Icon ổ khoá + tooltip "Kế thừa từ dự án cha, không sửa được" ở ô GG.

### 1.1 Đổi một trường kéo theo gì

| Thao tác | Xác nhận (nguyên văn) | Hệ quả | Nguồn |
|---|---|---|---|
| Đổi/chọn lại **Dự án** (Tạo mới, không phải bản sao) khi đã có hàng/dịch vụ | Tiêu đề "Xác nhận thay đổi Dự án", nội dung "Việc chọn lại Dự án sẽ xóa toàn bộ thông tin hàng hoá/dịch vụ trên báo giá!" [Xác nhận] (nút đỏ) | Xoá sạch hàng hoá, nhóm, dịch vụ; nạp KH/MST/địa chỉ/email/liên hệ, Tiền tệ, Giai đoạn theo dự án; dự án con → ép GG/Bảng giá/Tiền tệ + nạp Báo giá Mỏ neo; làm tròn mặc định theo tiền tệ; dò BOM tổng hợp. Huỷ → giữ dự án cũ | FE:4715-4760, 4834-4937 |
| Bỏ chọn Dự án (x) | (như trên nếu có dữ liệu) | Xoá KH, BOM, hàng, nhóm, dịch vụ; báo giá thành không gắn dự án → phải Chọn khách hàng | FE:4738-4754 |
| Đổi Dự án trên **bản Sao chép** | "Xác nhận đổi Dự án" / "Đổi Dự án sẽ lấy lại thông tin khách hàng, tiền tệ và bảng giá theo dự án mới. Hàng hoá, dịch vụ và giảm giá đang có trên báo giá được giữ nguyên. Thay đổi chỉ được ghi khi bạn bấm Lưu." [Đồng ý] | GIỮ hàng/dịch vụ/GG; nạp lại KH, tiền tệ, bảng giá, giai đoạn; ngắt BOM (thành báo giá tự lập). Hint dưới ô: "Báo giá sao chép — đổi Dự án giữ nguyên hàng hoá, dịch vụ và giảm giá đã sao chép, chỉ lấy lại khách hàng, tiền tệ và bảng giá theo dự án mới. Danh sách chỉ gồm dự án chưa có BOM tổng hợp đã duyệt. Thay đổi chỉ được ghi khi bấm Lưu." BE chặn dự án đã có BOM: "Dự án "<tên>" đã có BOM tổng hợp đã duyệt nên không thể chọn cho báo giá sao chép. Vui lòng chọn dự án khác hoặc tạo báo giá mới từ BOM của dự án đó." | FE:72-77, 4771-4795; SVC:71-76, 1837-1907 |
| Chọn **BOM** | Chưa có tiền tệ: thông báo "Vui lòng chọn loại tiền tệ trước để tính tỷ giá quy đổi khi tải sản phẩm từ BOM." Đã có dữ liệu: "Xác nhận thay đổi BOM" / "Việc chọn lại BOM sẽ xóa toàn bộ thông tin hàng hoá/dịch vụ trên báo giá!" | Nạp nhóm + hàng + dịch vụ của BOM. Hàng ERP lấy giá vốn & giá bán từ ERP (quy đổi tỷ giá); hàng tạm: giá bán ban đầu = giá vốn BOM; dịch vụ giá = 0. Bỏ chọn BOM → xoá hết, về báo giá tự lập | FE:5059-5106, 4938-5047 |
| Đổi **Bảng giá** khi có hàng ERP | "Xác nhận đổi bảng giá" / "Đổi bảng giá sẽ cập nhật lại đơn giá bán của các hàng hoá ERP theo bảng giá mới. Chiết khấu và hàng tạm giữ nguyên. Bạn có chắc muốn đổi?" [Xác nhận] | Gọi `erp-reprice`: cập nhật **Giá bán + VAT** của mọi dòng ERP theo bảng giá mới (giá vốn KHÔNG đổi trên màn); dòng ERP không có giá ở bảng mới → giữ giá cũ; GG tổng đã phân bổ → đánh dấu phải phân bổ lại. Bấm x (xoá) → chỉ xoá, không tính lại | FE:3610-3629, 3531-3609; CTL:905-926; SVC:2858-2911 |
| Đổi **Loại tiền tệ** khi đã có giá > 0 | "Xác nhận đổi loại tiền tệ" / "Các giá trị tiền tệ đã nhập sẽ không thay đổi khi bạn đổi loại tiền tệ ! Bạn có chắc chắc muốn đổi?" [Xác nhận] | KHÔNG quy đổi số trên màn. Làm tròn: VNĐ/JPY/KRW → ép "Số nguyên (0)"; từ loại không-lẻ sang có-lẻ → về mặc định 2 số lẻ; USD↔EUR giữ nguyên lựa chọn | FE:3630-3660 |
| Đổi **Phương thức GG** khi đã có dữ liệu GG | "Xác nhận đổi phương thức giảm giá" / "Thay đổi phương thức sẽ xóa dữ liệu giảm giá hiện tại. Tiếp tục?" [Xác nhận] (đỏ) | Xoá GG(%), GG(₫), Phân bổ GG mọi dòng + dòng vận chuyển + bảng GG tổng. Huỷ → quay lại phương thức cũ. BE cũng xoá dữ liệu GG khi đổi phương thức | FE:2610-2650, SVC:1923-1937 |
| Chọn **mẫu điều khoản** | xem bảng trên | Điền nội dung mẫu vào ô Điều khoản | FE:2976-3006 |

> ⚠️ Phát hiện khi đọc code (cần QA/BA lưu ý):
> - Đổi tiền tệ **không** quy đổi giá trên màn, nhưng khi bấm **Lưu** ở màn Tạo mới, BE tự tính lại giá hàng ERP theo tiền tệ + bảng giá mới (SVC:2702-2808, nhánh tạo dòng mới). Số trên màn và số sau khi lưu có thể lệch với hàng ERP (hàng tạm/dịch vụ giữ nguyên số đã nhập).
> - Dòng "Tỷ giá" luôn ghi đuôi "- Bảng giá bán lẻ" (chữ cố định), không đổi theo Bảng giá đang chọn (FE:362-368).

---

## 2. Thanh công cụ trên bảng (FE:284-369)

| Thành phần | Mô tả | Nguồn |
|---|---|---|
| **VAT:** [ô %] [Tất cả] [VAT=0] | Áp VAT đồng loạt cho **dòng cha là hàng tạm** (KHÔNG áp cho hàng ERP — VAT ERP khoá; KHÔNG áp cho Dịch vụ & Chi phí). "Tất cả" = mọi dòng; "VAT=0" = chỉ dòng đang 0%. Ô phải trong 0–100 mới bấm được. Toast "Đã áp X% cho N dòng" | VBT; FE:4132-4151 |
| **GG:** [Không GG / GG mặt hàng / GG tổng] | Khoá khi dự án con (tooltip "Kế thừa từ dự án cha, không sửa được") hoặc không có quyền **"Cho phép thêm giảm giá trong báo giá"** (tooltip "Bạn không có quyền áp dụng giảm giá trong báo giá"). BE 403 cùng câu nếu cố đổi GG khi không có quyền | FE:295-318; SVC:4793-4823 |
| **Làm tròn** ⓘ [select] [Áp dụng] | Tooltip: "Khi bấm Áp dụng, hệ thống tự động tính toán giá trị làm tròn dựa trên cấu hình, giá trị làm tròn áp dụng với các cột GIÁ NHẬP, GIÁ BÁN". Lựa chọn: Mặc định (tối đa 2 số lẻ) / Hàng nghìn (-3) / Hàng trăm (-2) / Hàng chục (-1) / Số nguyên (0) / 1 số lẻ (1) / 2 số lẻ (2). VNĐ: select khoá ở "Số nguyên (0)", tooltip "Đồng VNĐ mặc định làm tròn đến số nguyên". Xác nhận "Xác nhận làm tròn giá" / "Bạn có chắc muốn làm tròn đến <hàng nghìn/…> cho toàn bộ đơn giá? Thao tác này không thể hoàn tác." [Áp dụng]; toast "Đã làm tròn đơn giá" | FE:322-345, 3245-3287 |
| **Xóa giảm giá** (GG mặt hàng) / **Xóa phân bổ** (GG tổng) | Chỉ khi có quyền GG + đang có dữ liệu. Xác nhận: "Xóa dữ liệu giảm giá" / "Bạn có chắc chắn muốn xóa toàn bộ dữ liệu giảm giá?" — hoặc "Xóa phân bổ giảm giá" / "Bạn có chắc chắn muốn xóa toàn bộ giá trị phân bổ giảm giá? Tất cả giá trị tại cột Phân bổ GG sẽ được đặt về 0". Toast "Đã xóa toàn bộ dữ liệu giảm giá" / "Đã xóa toàn bộ phân bổ giảm giá". Xóa phân bổ GIỮ bảng khoản GG tổng | FE:347-360, 2686-2710 |
| **Tỷ giá** (chỉ ngoại tệ) | "Tỷ giá: 1 <mã tiền> = <tỷ giá> VND (<ngày tạo báo giá>) - Bảng giá bán lẻ" | FE:362-368 |

---

## 3. Bảng "Chi tiết sản phẩm" (FE:371-947)

Tiêu đề khối: "Chi tiết sản phẩm" (báo giá tự lập) / "Chi tiết sản phẩm — sửa giá" (báo giá từ BOM). Thanh tiêu đề **ghim (sticky)** khi cuộn. Nút trên thanh tiêu đề:
- **Thêm nhóm** (chỉ báo giá tự lập + canEdit)
- **Thu gọn tất cả / Mở rộng tất cả** (đóng/mở mọi nhóm, cả nhóm con)
- **Ẩn cột chi tiết / Hiện cột chi tiết** (ẩn/hiện 5 cột Model, Thương hiệu, Xuất xứ, Thông số kỹ thuật, Ghi chú — mặc định HIỆN)
- **Xuất Excel** (không có ở Tạo mới) — toast lỗi "Không xuất được file Excel. Vui lòng thử lại."
- **Import Excel** (canEdit và không phải Tạo mới) — "Vui lòng lưu báo giá trước khi import." *(phần Import thuộc brief khác)*

Bảng cao tối đa 500px, có thanh cuộn ngang trên + dưới, tiêu đề cột ghim.

### 3.1 Danh sách cột (thứ tự trái → phải)

| Cột | Hiện khi | Ô nhập được? | Ghi chú quyền / hiển thị | Nguồn |
|---|---|---|---|---|
| Thao tác (nút ▾/▸ thu gọn tất cả + "Thao tác") | báo giá tự lập + canEdit | — | chứa tay nắm kéo thả + nút xoá | FE:406-418 |
| STT | luôn | — | cha: 1,2,3 (đánh lại trong từng nhóm); con: 1.1, 1.2 | FE:549, 708 |
| Mã | luôn | — | Hàng tạm CHƯA lưu để TRỐNG mã (mã HHBG chỉ sinh khi Lưu). Hàng ERP có icon ⚠ vàng nếu sắp đổi giá (§4a) | FE:550-559, 3997-4001 |
| Tên hàng | luôn | — | Dịch vụ có badge "DV". Dưới tên: ghi chú nội bộ (từ ERP, chỉ đọc) + nút thao tác dòng (§3.4) | FE:560-589 |
| Model / Thương hiệu / Xuất xứ / Thông số kỹ thuật | "Hiện cột chi tiết" | không | | FE:590-596 |
| Ghi chú | "Hiện cột chi tiết" | **Có** (canEdit), placeholder "Ghi chú" | | FE:597-600 |
| SL | luôn | **Có** — báo giá tự lập + canEdit (số, bước 0.01). Báo giá từ BOM: chỉ đọc | Con công thức ghép bộ (con của hàng ERP): khoá, tooltip "SL theo công thức ghép bộ, tự nhân theo SL cha" | FE:601-604, 734-737 |
| ĐVT | luôn | **Có (select ĐVT)** chỉ với dòng cha hàng ERP không có con, báo giá tự lập | Hàng khác: chữ | FE:605-616, 3359-3412 |
| Giá nhập (<mã tiền>) | luôn | **Có** với hàng tạm không có con (và dịch vụ chưa có tỷ lệ giá vốn) | Hàng ERP: KHOÁ (giá từ ERP); không có quyền **"Xem giá vốn hàng hoá"** → hiện "—". Cha tạm có con: khoá, tự tính, tooltip "Tự động tính từ SP con" | FE:617-630, 741-746, 867-873 |
| Thành tiền nhập | luôn | — | Hàng ERP + không quyền giá vốn → "—" | FE:631-634 |
| Giá bán (<mã tiền>) | luôn | **Có** với hàng tạm (cha và con tạm), dịch vụ | Hàng ERP: khoá. Con của cha ERP: "—". Con ERP của cha tạm: chỉ đọc | FE:635-644, 751-755 |
| GG(%) · GG(₫) · Đơn giá sau GG | Phương thức = GG mặt hàng | GG(%), GG(₫) nhập được nếu canEdit + có quyền GG; 2 ô liên động | chỉ dòng cha + dịch vụ (con hiện "—") | FE:645-665 |
| GG phân bổ tự động ⓘ · Phân bổ GG | Phương thức = GG tổng | "GG phân bổ tự động" chỉ đọc (tooltip "Tham khảo — tự tính theo tỷ lệ giá trị"); "Phân bổ GG" nhập được (khoá khi Tổng GG ≤ 0). Tiêu đề cột "Phân bổ GG" hiện "Còn: <Tổng GG − Đã phân bổ>" (xanh khi khớp, đỏ khi lệch) | | FE:435-445, 666-670 |
| Thành tiền bán | luôn | — | = thành tiền **sau giảm giá, trước VAT** (§5) | FE:671 |
| Tỷ suất LN | luôn | — | Màu: < "Tỷ suất lợi nhuận mức sàn" (cấu hình Quy định chung) → đỏ; ≥ → xanh. Hàng ERP + không quyền giá vốn → "—"; giá nhập = 0 → "—" | FE:672-675, 2602-2608 |
| VAT(%) ⓘ | luôn | **Có** với hàng tạm và dịch vụ; hàng ERP khoá (tooltip "VAT lấy từ danh mục hàng hoá ERP") | Tooltip tiêu đề: "VAT chỉ áp dụng trên dòng CHA hoặc SP độc lập. SP con được cộng gộp vào CHA." | FE:448-455, 677-691 |
| Tiền VAT | luôn | — | | FE:692 |
| Thành tiền sau VAT | luôn | — | | FE:693 |

**Dòng CON**: Thành tiền bán / Tỷ suất LN / VAT / Tiền VAT / Thành tiền sau VAT để "—" (con chỉ là chi tiết cấu thành, không tính tiền riêng) (FE:761-767).

### 3.2 Bố cục phần: A — Hàng hoá / B — Dịch vụ & Chi phí khác / TỔNG

- **Dòng tiêu đề "A — Hàng hoá"** kèm nút **Thêm nhóm**, **Thêm mới** (báo giá tự lập + canEdit). Cùng dòng hiện tổng phần A: Thành tiền nhập (— nếu không quyền giá vốn), Thành tiền bán, Tiền VAT, Thành tiền sau VAT (FE:461-489).
- Mỗi **nhóm**: dòng tiêu đề "I. Tên nhóm (N hàng)" + mũi tên đóng/mở; nút **Thêm mới**, **Thêm nhóm con** (chỉ nhóm cấp 1), ✏ "Đổi tên", 🗑 "Xóa nhóm". Cuối mỗi nhóm đang mở có thanh thêm nhanh: [Thêm mới] [Thêm nhóm con] "vào nhóm I. <tên>" (FE:490-529, 772-800).
  - **KHÔNG có dòng tổng tiền theo nhóm** — tiêu đề nhóm chỉ đếm số hàng.
- **Dòng tiêu đề "B — Dịch vụ & Chi phí khác"** "(N dòng)" + nút **Thêm mới** (canEdit), kèm tổng phần B (FE:803-827).
- **Dòng TỔNG** cuối bảng: Thành tiền nhập (— nếu không quyền), tổng GG theo phương thức, Thành tiền bán, Tỷ suất LN hàng hoá+dịch vụ (— nếu không quyền), Tiền VAT, Thành tiền sau VAT (FE:928-944). **Không gồm chi phí vận chuyển.**

### 3.3 Nhóm hàng (chỉ báo giá tự lập)

- Popup **"Thêm nhóm sản phẩm" / "Sửa nhóm sản phẩm"**: 1 trường **Tên nhóm \*** (placeholder "Nhập tên nhóm"; Enter = lưu). Nút **Thêm** / **Lưu** (bấm được khi tên không rỗng) + **Huỷ** (FE:1322-1337, 4218-4256).
- **2 cấp**: nhóm cấp 1 đánh số La Mã (I, II…), nhóm con cấp 2 đánh "I.1, I.2". Không có cấp 3 (FE:1828-1869).
- Tạo nhóm đầu tiên ⇒ mọi hàng chưa có nhóm tự vào nhóm vừa tạo. Có hàng chưa thuộc nhóm nào ⇒ hiện nhóm ảo **"Không nhóm"** ở đầu; khi Lưu, hàng lẻ tự gán vào nhóm đầu tiên (FE:4249-4253, 4277-4285, 3825).
- **Xoá nhóm**: KHÔNG hỏi xác nhận. Xoá nhóm cấp 1 xoá luôn nhóm con của nó; hàng của các nhóm bị xoá chuyển sang nhóm đầu tiên còn lại (hết nhóm → hàng thành "Không nhóm"). Hàng hoá KHÔNG bị xoá (FE:4257-4275).
- Đóng/mở từng nhóm bằng mũi tên hoặc bấm tên nhóm.

### 3.4 Thao tác trên dòng hàng hoá (báo giá tự lập + canEdit)

| Nút (dưới tên hàng) | Hiện với | Hành vi | Nguồn |
|---|---|---|---|
| **Sửa** | hàng tạm (cha và con) | Popup "Sửa hàng hoá": Tên hàng hoá \* (placeholder "Nhập tên hàng hoá"), Mã (khoá), Đơn vị tính \* ("Chọn ĐVT"), Model, Thương hiệu, Xuất xứ (ô tìm từ xa), Đặc điểm / Thông số kỹ thuật, Ghi chú. Lỗi: "Tên là bắt buộc", "Đơn vị tính là bắt buộc". Nút Lưu / Đóng. KHÔNG sửa giá ở popup (giá sửa trên lưới) | FE:565-568, PEM |
| **Nhân bản** (tooltip "Tạo thêm 1 dòng cùng hàng tạm này (dùng chung mã)") | hàng tạm cha không có con | Chèn 1 dòng sao ngay dưới, dùng chung mã hàng tạm khi lưu. Toast "Đã nhân bản hàng tạm (dùng chung mã). Chỉnh số lượng nếu cần rồi Lưu." | FE:569-572, 4318-4342 |
| **Thêm con** | hàng tạm cha | Mở popup Thêm hàng hoá, hàng chọn sẽ thành con của dòng này | FE:573-576, 4296-4306 |
| **Ẩn con / Hiện con** (tooltip "Ẩn/Hiện hàng con khi in/xuất") | hàng ERP có con | Chỉ ẩn/hiện con trên lưới, bản in, file xuất — vẫn tính tổng | FE:577-587, 3046-3049 |
| 🗑 Xoá (cột Thao tác) | mọi dòng cha; dòng con trừ con công thức của hàng ERP | Xác nhận "Xác nhận xóa": có con → "Xoá "<tên>" sẽ xoá cả <N> hàng con kèm theo. Bạn có chắc?"; không con → "Bạn có chắc muốn xoá "<tên>" khỏi báo giá?" [Xóa] (đỏ). Xoá trên màn, ghi DB khi Lưu | FE:546, 705, 4674-4692 |
| ⋮⋮ Kéo thả | xem §3.7 | | |

### 3.5 Thêm hàng hoá có sẵn (popup — POP)

Mở bằng **Thêm mới** (A — Hàng hoá / trong nhóm / thanh thêm nhanh) hoặc **Thêm con**. Điều kiện: phải có Loại tiền tệ, nếu không: hộp thông báo "Vui lòng chọn loại tiền tệ trước khi thêm." (Thêm con: "...trước khi thêm sản phẩm.") (FE:4343-4365, 4296-4300).

- Tiêu đề popup: "Thêm hàng hoá" (báo giá tự lập, mở từ phần A) / "Thêm dịch vụ / chi phí" / "Thêm mới". Rộng 98% màn hình; **bấm ra ngoài không đóng**, chỉ đóng bằng X hoặc **Đóng** (POP:1-11).
- **Nhóm hàng \*** (nếu báo giá có nhóm): select "Chọn nhóm hàng" + gợi ý "Hàng hoá sẽ được thêm vào nhóm này"; mặc định = nhóm vừa bấm (POP:21-31).
- **Ô tìm nhanh**: "Tìm theo tên, mã, model hàng hoá" — tìm khi Enter/bấm Tìm kiếm (POP:40-41).
- **Tìm kiếm nâng cao** (nhãn floating) 19 ô: Tính chất hàng hóa, Loại hàng hóa (chọn nhiều), Công ty (nguồn hàng) — chỉ thu hẹp danh sách, KHÔNG đổi giá, Thương hiệu, Hãng sản xuất (nhiều), Xuất xứ, Lĩnh vực, Chương, Nhóm công việc, Cụm công việc, Nhóm hàng hóa, Dùng cho nhóm máy, Dùng cho máy (tìm từ xa), Hãng xe, Loại xe, Model xe, Đời xe, Model (tìm từ xa), Tồn kho. Các ô cha–con lọc phụ thuộc nhau (POP:706-732).
- Nút **Thêm hàng tạm** đặt cạnh nút Tìm kiếm nâng cao (POP:52-63).
- **Cột kết quả**: ☐ · Ảnh (bấm = xem trước) · Loại hàng hóa · Tên hàng hoá (rê chuột hiện popover "Đặc điểm:" + "Phụ kiện tiêu chuẩn:") · Lĩnh vực · Chương · Model · Mã hàng · Nguồn hàng (mã công ty) · **Giá niêm yết** ("<giá> / <ĐVT>") · Bảo hành · VAT(%) · Định mức đàm phán giá (%) · SL tồn có thể bán · SL KM có thể xuất · SL có thể LR · Ghi chú · Tính chất hàng hóa · Nguồn (badge ERP) (POP:91-119). Phân trang server; rỗng: "Không có dữ liệu phù hợp bộ lọc."
- **Chọn**: bấm vào **dòng** = thêm NGAY 1 hàng; tích **checkbox** (chọn nhiều, giữ qua các trang, có chọn tất cả trang) rồi bấm **"Thêm N hàng hoá"**. Popup **không tự đóng** sau khi thêm; toast "Đã thêm N hàng hoá vào phiếu." (POP:133-142, 1192-1291, 502-511).
- **Giá lấy từ đâu**: Giá bán = giá ERP theo **Bảng giá đang chọn** trên báo giá ("Giá niêm yết") + công ty ghi trên báo giá (Tạo mới: công ty người đăng nhập); Giá vốn = giá vốn ERP **chỉ trả về khi có quyền "Xem giá vốn hàng hoá"**; VAT = VAT ERP; SL mặc định **1** (POP:1097, 1201-1229; CTL:864-883; ErpProductSearchService.php:91-194). Ngoại tệ: giá ÷ tỷ giá, làm tròn 2 số lẻ (FE:4464-4465).
- **Hàng ERP là combo (có công thức ghép bộ)**: tự nạp các hàng con theo công thức; SL con = SL công thức × SL cha, khoá; không xoá riêng được; lỗi nạp: "Không nạp được hàng con (recipe) cho mã ERP <mã>" (FE:4540-4594).
- **Trùng hàng** (cùng mã ERP / cùng mã hàng tạm, cùng nhóm, cùng cấp; hoặc cùng cha khi thêm con): overlay **"Hàng hoá đã tồn tại"** — "Hàng hóa "<tên>" đã tồn tại trong danh sách. Bạn muốn cộng dồn số lượng hay tạo dòng mới?" (nhiều hàng: "<N> hàng hoá đã tồn tại trong danh sách ("a", "b", "c"...). ...") — nút **Cộng dồn số lượng** (cộng SL vào dòng cũ) / **Tạo dòng mới** / **Huỷ** (chỉ thêm hàng không trùng) (POP:472-499, 828-837, 1308-1326; FE:4416-4436).
- **Thêm con**: không được trùng mã với chính cha: toast "Hàng con không được trùng mã với hàng cha (<cha>): <danh sách>" (FE:4380-4389). Không có quyền "Xem giá vốn hàng hoá" ⇒ không được chọn hàng ERP làm con: popup hiện cảnh báo "Bạn không có quyền xem giá vốn nên không thể thêm hàng ERP làm hàng con." và danh sách ERP rỗng; BE chặn: "Bạn không có quyền "Xem giá vốn hàng hoá" nên không thể chọn hàng ERP làm hàng con." (POP:16-18, SVC:2281-2320).

### 3.6 Thêm hàng tạm (overlay "Thêm hàng tạm" trong POP)

Bấm **Thêm hàng tạm** → overlay 2 tab (bấm ngoài không đóng). Có ô **Nhóm hàng \*** dùng chung 2 tab ("Vui lòng chọn nhóm hàng") (POP:250-427).

**Tab 1 — "Chọn từ kho hàng tạm (Tái sử dụng)"** (báo giá tự lập luôn bật): ô "Tìm nhanh theo mã / tên hàng tạm..."; bảng ☐ · Mã hàng · Tên hàng · Model · Thương hiệu · Xuất xứ · ĐVT · Nguồn (badge **Dự án** = hàng tạm đã nằm trên màn Hàng hoá dự án — BOM tổng hợp đã duyệt / báo giá tự lập đã duyệt hoặc trúng thầu của cùng dự án; **Trong phiếu** = hàng tạm đang có trên lưới). Rỗng: "Không có hàng tạm phù hợp.". Nút **"Thêm N hàng hóa"** / Đóng. Chọn 1 cha có con → thêm cả cha lẫn con. Giá vốn, giá bán, VAT lấy theo dòng nguồn (không quy đổi tỷ giá). Mã giữ nguyên mã nguồn. Toast "Đã thêm N hàng hóa" (POP:1362-1485).

**Tab 2 — "Thêm mới thủ công"**:

| Trường | Bắt buộc | Lỗi |
|---|---|---|
| Tên hàng hoá ("Nhập tên hàng hoá") | ✔ | "Tên là bắt buộc" |
| Đơn vị tính ("Chọn ĐVT") | ✔ | "Đơn vị tính là bắt buộc" |
| Model (⊕ thêm nhanh) | — | |
| Thương hiệu (⊕ thêm nhanh) | ✔ | "Thương hiệu là bắt buộc" |
| Xuất xứ (⊕ thêm nhanh) | ✔ | "Xuất xứ là bắt buộc" |
| Số lượng cần dùng ("Nhập số lượng") | — (trống → 1) | |
| Ghi chú | — | |
| Đặc điểm / Thông số kỹ thuật (soạn thảo) | — | |

Nút **Lưu** (thêm + đóng) / **Lưu và tiếp tục** (thêm + xoá form để nhập tiếp) / **Đóng** (POP:344-424, 1563-1617).
- **KHÔNG có ô giá ở form**: hàng tạm vào lưới với Giá nhập = 0, Giá bán = 0, VAT = 0 → **người dùng nhập Giá nhập (giá vốn), Giá bán, VAT trực tiếp trên lưới** (FE:4439-4468).
- Thêm nhanh Model/Thương hiệu/Xuất xứ (⊕): popup "Tên \*" (thương hiệu thêm "Mã thương hiệu \*"), nút Lưu/Huỷ, toast "Đã thêm nhanh thành công." (POP:429-470, ~1730).
- **Mã hàng tạm**: trống trên lưới tới khi Lưu; BE sinh `HHBG` + id đệm 6 số (vd HHBG001222). Ngoại lệ giữ mã: mã trùng hàng tạm của **cùng dự án** đã lên màn Hàng hoá dự án; dòng nhân bản; bản sao chép giữ mã của bản gốc (SVC:2702-2820, 2651-2700).

### 3.7 Sắp xếp (kéo thả) — FE:3068-3243

Chỉ khi báo giá tự lập + canEdit (dịch vụ: canEdit). Tay nắm ⋮⋮ ở cột Thao tác (báo giá từ BOM: tay nắm dịch vụ nằm ở cột STT). KHÔNG có nút lên/xuống.
- **Dòng cha**: kéo đổi thứ tự (cả cụm cha + con đi cùng). Thứ tự chỉ đổi, **không đổi nhóm** của hàng.
- **Dòng con**: kéo trong phạm vi cha của nó, không kéo sang cha khác.
- **Nhóm**: kéo tiêu đề nhóm đổi thứ tự giữa các nhóm **cùng cấp, cùng nhóm cha**; kéo sang cấp/cha khác hiện con trỏ cấm và không thả được.
- **Dịch vụ & Chi phí**: kéo đổi thứ tự trong phần B.
- Thứ tự lưu xuống DB khi bấm Lưu.

### 3.8 Thêm dịch vụ / chi phí (phần B)

Nút **Thêm mới** ở dòng "B — Dịch vụ & Chi phí khác" → popup tab **Dịch vụ & Chi phí** (CCP):
- Ô "Tìm theo tên dịch vụ / chi phí..." (tự tìm sau 300ms) + bộ lọc nút: **Tất cả / Dịch vụ có tính DT / Chi phí khác**. Danh sách: tên + badge loại ("Dịch vụ có tính doanh thu" / "Chi phí khác") + "VAT x%". Rỗng: "Không tìm thấy mục nào. Bấm "Thêm mới" để tạo nhanh."
- Bấm 1 mục → thêm 1 dòng (SL luôn = 1, ĐVT trống, VAT theo danh mục, **Giá nhập = 0, Giá bán = 0** → nhập trên lưới). Toast "Đã thêm: <tên>" (POP:1538-1562; FE:4393-4414).
- **Thêm mới nhanh dịch vụ** (nút "Thêm mới" trong panel) → popup **"Tạo nhanh dịch vụ / chi phí"** (CQC):

| Trường | Bắt buộc | Mặc định | Lỗi |
|---|---|---|---|
| Loại (-- Chọn loại -- / Dịch vụ có tính doanh thu / Chi phí khác) | ✔ | trống | "Bắt buộc phải chọn loại" |
| Tên ("Nhập tên dịch vụ / chi phí") | ✔ | từ khoá đang gõ ở ô tìm | "Bắt buộc phải nhập tên" |
| Giá vốn (<mã tiền>) | ✔ | 0 | "Bắt buộc nhập giá vốn" |
| Giá bán (<mã tiền>) | ✔ (> 0) | 0 | "Giá bán phải lớn hơn 0" |
| % VAT | ✔ | 8 | "Bắt buộc phải nhập % VAT" |

  Dòng phụ: "Tỷ lệ giá vốn lưu vào danh mục: **X%**" với X = Giá vốn / Giá bán × 100 (2 số lẻ). Nút **Lưu** / **Đóng**. Lỗi gộp hiện toast. **Lưu vào danh mục Dịch vụ/Chi phí của ERP** (`POST assign/erp-costs`, kind_of = 2, kèm VAT + tỷ lệ giá vốn); toast "Đã tạo mục danh mục"; dòng dịch vụ tự thêm vào báo giá với đúng giá vốn/giá bán vừa nhập.
- **Trên lưới**, dòng dịch vụ: icon 💲 "Chi phí khác" hoặc icon dịch vụ "Dịch vụ"; badge **"Tỷ lệ giá vốn: X%"** (tooltip báo giá tự lập: "Giá vốn = Giá bán × tỷ lệ này"; báo giá từ BOM: "PM tự tính từ giá vốn / giá bán — lưu về danh mục ERP khi lưu báo giá"). SL = 1 (đọc). Giá nhập: **khoá + tự tính = Giá bán × tỷ lệ** nếu danh mục đã có tỷ lệ > 0 (tooltip "Tự tính từ giá bán × tỷ lệ giá vốn"); chưa có tỷ lệ → nhập tay, khi lưu BE ghi ngược tỷ lệ = giá vốn/giá bán × 100 vào danh mục ERP. Giá bán, VAT, GG nhập được. ✏ "Chọn lại dịch vụ / chi phí" (đổi sang mục khác trong danh mục), 🗑 "Xoá dịch vụ" (FE:828-926, 4629-4673; SVC:3410-3446).
- **Xoá dịch vụ**: dòng **đã lưu** → xác nhận "Xác nhận xóa" / "Bạn có chắc muốn xóa dịch vụ này?" [Xóa] → **xoá ngay xuống DB** (không chờ Lưu), toast "Đã xoá dịch vụ" / lỗi "Lỗi xoá dịch vụ". Dòng chưa lưu → xoá ngay không hỏi (FE:4178-4199).

### 3.9 Validate trên bảng (nguyên văn) — FE:3761-3823

Lưu nháp: chỉ kiểm **VAT 0–100**, **GG(%) 0–100**, và các dòng GG tổng (trừ dòng do hệ thống dựng theo Mỏ neo chưa nhập). Gửi duyệt: kiểm đủ. Lỗi hiện **ngay dưới ô** (viền đỏ), tự cuộn tới ô lỗi đầu tiên; không dùng toast.

| Điều kiện | Câu lỗi (dưới ô) | Lúc nào |
|---|---|---|
| Hàng tạm (không có con) Giá nhập ≤ 0 | "Giá nhập phải > 0" | Gửi duyệt |
| Cha tạm: Giá nhập × SL < Σ(Giá nhập con × SL con) (chỉ khi có quyền giá vốn) | "Giá vốn cha phải ≥ tổng giá vốn con" | Gửi duyệt |
| Thành tiền bán (sau GG) ≤ 0 — hàng hoá cha & dịch vụ | "Giá / thành tiền bán phải > 0" | Gửi duyệt |
| Cha tạm có con: Giá bán × SL < Σ(Giá bán con × SL con) | "Giá bán hàng cha phải ≥ tổng giá bán hàng con" | Gửi duyệt |
| GG(%) ngoài 0–100 | "GG (%) phải trong 0–100%" | mọi lần lưu |
| GG(₫)/đơn vị > Đơn giá bán | "GG không được lớn hơn đơn giá bán" | Gửi duyệt |
| VAT ngoài 0–100 (hàng hoá cha, dịch vụ, vận chuyển) | "VAT phải trong 0–100%" | mọi lần lưu |
| Giá nhập vận chuyển < 0 | "Giá nhập không hợp lệ" | Gửi duyệt |
| Chi phí vận chuyển < 0 | "Chi phí vận chuyển không hợp lệ" | Gửi duyệt |
| GG vận chuyển < 0 hoặc > chi phí VC (GG mặt hàng) | "GG vận chuyển không được lớn hơn chi phí" | Gửi duyệt |
| Bảng GG tổng: chưa chọn loại | "Vui lòng chọn loại GG" | mọi lần lưu |
| Bảng GG tổng: giá trị ≤ 0 / > 100% | "Giá trị phải > 0" / "Giá trị tối đa 100%" | mọi lần lưu |
| Số lượng | **Không có câu lỗi riêng**; SL = 0 làm thành tiền = 0 → bắt bằng "Giá / thành tiền bán phải > 0". BE: SL ≥ 0 | |
| Hàng ERP Giá nhập = 0 | **Hợp lệ** (giá ERP, người dùng không sửa được) | |

BE khi Gửi duyệt (SVC:3796-3811, 4729-4785): "Có N sản phẩm/dịch vụ chưa hợp lệ (giá bán > 0, số lượng > 0, giảm giá ≤ đơn giá bán)." · "Giá bán hàng cha "<tên>" phải ≥ tổng giá bán hàng con." · "Giá vốn hàng cha "<tên>" đang nhỏ hơn tổng giá vốn hàng con." (cha ERP được miễn 2 kiểm tra cha–con). Popup Tạo mới khi BE chặn: tiêu đề "Không thể gửi duyệt báo giá" + nguyên văn câu BE.

> ⚠️ Lưu ý code: kiểm tra BE "Có N sản phẩm/dịch vụ chưa hợp lệ" join qua bảng BOM nên với **báo giá tự lập** thực tế chỉ kiểm phần dịch vụ; phần hàng hoá chỉ được chặn ở FE (SVC:4729-4735).

### 3.10 Cảnh báo giá bán thấp (≤ 1,000) — FE:1739-1754, 4012-4064; LPW

- Khi bấm **Gửi duyệt** (cả Tạo mới lẫn Sửa), nếu có **dòng hàng hoá** (cả cha lẫn con) Đơn giá bán **≤ 1,000** → tô nền cam các dòng đó + popup **"Cảnh báo: Tồn tại mặt hàng có đơn giá <= 1.000 vnđ"**: "Hệ thống phát hiện báo giá đang chứa **N** mặt hàng chưa được cập nhật giá bán hoặc là hàng khuyến mãi/giảm giá." + bảng STT · Mã hàng hóa · Tên hàng hóa · Đơn giá bán. Nút **Tiếp tục gửi duyệt** / **Quay lại**. Không chặn.
- Ngưỡng so trên số thô theo loại tiền của báo giá (không quy đổi VND); dịch vụ không thuộc kiểm tra này. Ngưỡng 1,000 cũng là điều kiện "tự duyệt" ở BE (SVC:3548-3583).

### 3.11 Gợi ý áp VAT lần đầu (VFP; FE:4100-4131)

Lần đầu trong phiên user đổi VAT một dòng hàng hoá từ 0 → > 0 mà còn dòng khác đang 0% → popup **"Áp dụng VAT đồng loạt?"**: "Áp dụng **X%** VAT cho **N** sản phẩm còn đang để 0%?" — **Chỉ dòng này** / **Áp dụng tất cả dòng còn 0%** (toast "Đã áp X% cho N dòng"). Chỉ hỏi 1 lần/phiên.

---

## 4. Giảm giá tổng & bảng Tổng hợp & chân trang (FE:949-1249)

**Khối "Giảm giá tổng đơn hàng"** (phương thức GG tổng, hiện khi có quyền GG hoặc báo giá đã có khoản GG): bảng # · Loại GG ("— Chọn loại GG —", mỗi loại chỉ chọn 1 lần) · Kiểu (% / ₫) · Giá trị % / Giá trị ₫ · Thành tiền GG · 🗑; dòng "Tổng GG". Nút **Thêm khoản GG**; **Phân bổ tự động** (lần đầu) / **Phân bổ lại** (khi đã phân bổ mà lệch hoặc giá bán vừa đổi) — xác nhận "Phân bổ giảm giá tự động" / "Thao tác này sẽ ghi đè toàn bộ giá trị cột "Phân bổ GG" bằng giá trị phân bổ tự động (theo tỷ lệ giá trị). Bạn có chắc chắn?" [Phân bổ], toast "Đã cập nhật cột Phân bổ GG theo phân bổ tự động". Dòng trạng thái: "Đã phân bổ: X / Y ✓" hoặc "— Chênh lệch: Z". Sửa giá bán khi đã phân bổ → toast "Giá bán đã thay đổi, vui lòng phân bổ lại giảm giá".

**Bảng "Tổng hợp giá trị báo giá"**: cột STT · Nhóm chi phí · Thành tiền nhập (— nếu không quyền giá vốn) · Thành tiền trước VAT · [Giảm giá · Thành tiền sau GG (trước VAT)] (khi có phương thức GG) · Thuế VAT · Thành tiền sau VAT. Dòng: I Hàng hoá · II Dịch vụ · III Chi phí · IV Chi phí vận chuyển · V Tổng giá trị báo giá (kèm mã tiền).
- Dòng **IV Chi phí vận chuyển** nhập được: Giá nhập VC (người lập nhập được, không cần quyền giá vốn), Chi phí vận chuyển (= thành tiền trước VAT), GG vận chuyển (GG mặt hàng: cặp % ↔ ₫; GG tổng: ô Phân bổ), **VAT cố định 8%, khoá**.
- Dưới bảng (có quyền giá vốn): "TSLN trước GG: x%" · "TSLN sau GG: y%" (xanh ≥ 0, đỏ < 0).

**Chân trang ghim**: Nhập (— nếu không quyền) · Bán · GG · Sau GG · ~VND (ngoại tệ) · LN (%) · **Cấp duyệt** dự kiến (C1 — Tự duyệt / C2 — TP / C3 — TP & BGĐ; chỉ người có quyền giá vốn thấy) · nút **Quay lại**, **Lưu nháp**, **Gửi duyệt**. Lưu xong: toast "Đã tạo báo giá" / "Đã lưu báo giá" → về danh sách.

---

## 5. CÔNG THỨC (trích đúng code)

Ký hiệu cho 1 dòng: SL = số lượng; GN = Giá nhập (đơn giá vốn); GB = Giá bán (đơn giá); GG% / GG₫ = giảm giá mặt hàng theo % / theo tiền **trên 1 đơn vị**; PB = số tiền Phân bổ GG của dòng (GG tổng, tính cho CẢ dòng); VAT% của dòng.

### 5.1 Dòng hàng hoá (FE:2555-2601; BE SVC:3041-3104, 3112-3220 cùng công thức)

| Đại lượng | Công thức |
|---|---|
| Thành tiền nhập | `SL × GN` |
| Thành tiền bán **trước GG** (dùng trong bảng Tổng hợp cột "Thành tiền trước VAT") | `SL × GB` |
| GG mặt hàng — nhập % | `GG₫ = round(GB × GG% / 100, 2)` |
| GG mặt hàng — nhập ₫ | `GG% = round(GG₫ / GB × 100, 4)` (GB = 0 → 0) |
| Đơn giá sau GG (GG mặt hàng) | `GB − GG₫` |
| **Thành tiền bán** (cột trên lưới) = sau GG, trước VAT | Không GG: `SL × GB` · GG mặt hàng: `SL × GB − GG₫ × SL` · GG tổng: `SL × GB − PB` |
| Tiền VAT | `Thành tiền bán × VAT% / 100` |
| Thành tiền sau VAT | `Thành tiền bán + Tiền VAT` |
| **Tỷ suất LN dòng** | `round((Thành tiền bán − Thành tiền nhập) / Thành tiền nhập × 100, 2)` % — **tính trên GIÁ VỐN (markup), SAU giảm giá, TRƯỚC VAT**. Thành tiền nhập ≤ 0 → hiển thị "—" |

- Chỉ **dòng CHA / dòng độc lập** được cộng vào tổng; dòng CON không cộng (giá cha đã bao gồm con) (FE:1880-1902).
- **Cha hàng tạm có con**: `GN cha = round(Σ(GN con × SL con) / SL cha, theo kiểu làm tròn đang chọn)` — tự tính, khoá ô (SL cha = 0 → 0). **GB cha KHÔNG tự cộng từ con** — người dùng nhập, phải ≥ tổng con (FE:3022-3039).
- **Cha hàng ERP (combo)**: GN, GB giữ nguyên theo ERP (không cộng từ con); SL con = SL công thức × SL cha, làm tròn 2 số lẻ (FE:3057-3064).

**Ví dụ 1 (GG mặt hàng)**: SL 2; GN 1,000,000; GB 1,250,000; GG 10%; VAT 8%.
- GG₫ = 125,000/đv; Đơn giá sau GG = 1,125,000
- Thành tiền nhập = 2,000,000; Thành tiền bán = 2,500,000 − 250,000 = **2,250,000**
- Tỷ suất LN = (2,250,000 − 2,000,000) / 2,000,000 = **12.5%**
- Tiền VAT = 180,000; Thành tiền sau VAT = **2,430,000**

**Ví dụ 2 (cha tạm có con)**: Cha SL 2; con A: SL 4 × GN 300,000; con B: SL 2 × GN 150,000 ⇒ Σ = 1,500,000 ⇒ GN cha = 1,500,000 / 2 = **750,000**. Nếu con A GB 400,000, con B GB 200,000 ⇒ Σ bán con = 2,000,000 ⇒ GB cha phải ≥ 1,000,000 (vì GB cha × 2 ≥ 2,000,000).

### 5.2 Dòng dịch vụ / chi phí (FE:2579-2601, 4664-4669; SVC:3410-3424)

- SL luôn 1. Công thức thành tiền / VAT / Tỷ suất LN y như hàng hoá.
- Danh mục đã có tỷ lệ giá vốn R% > 0: `GN = round(GB × R / 100, 2)` (FE và BE đều tính lại, không tin số nhập).
- Chưa có tỷ lệ: nhập GN tay; khi lưu BE ghi `R = round(GN / GB × 100, 2)` vào danh mục ERP (chỉ khi GB > 0).
- Phân nhóm Tổng hợp: loại "Chi phí khác" (không tính doanh thu) → dòng **III Chi phí**; còn lại → **II Dịch vụ**.

### 5.3 Chi phí vận chuyển (FE:2119-2151, 2175-2182; SVC:3086-3093)

- GG VC: GG mặt hàng → số tiền ô GG VC (cặp `% = round(GG / CPVC × 100, 2)` ↔ `GG = round(CPVC × % / 100, 2)`); GG tổng → ô Phân bổ VC; không GG → 0.
- `VAT VC = (CPVC − GG VC) × 8%` (FE mặc định & khoá 8%) · `Sau VAT VC = CPVC − GG VC + VAT VC` · Giá nhập VC do người dùng nhập (độc lập giá bán).
- Chỉ tính khi CPVC > 0.

### 5.4 Giảm giá tổng (FE:2028-2108, 2735-2742)

- Khoản GG kiểu %: `Thành tiền GG = round((Σ SL×GB các dòng cha hàng hoá + Σ SL×GB dịch vụ + CPVC) × % / 100, 2)` — base = tổng **trước GG, trước VAT, GỒM vận chuyển**. Kiểu ₫: số nhập.
- `Tổng GG = Σ Thành tiền GG các khoản`.
- **Phân bổ tự động** (Largest Remainder, tính theo "xu" ×100 cho khớp tuyệt đối 2 số lẻ): mỗi dòng (cha hàng hoá, dịch vụ, vận chuyển nếu > 0) nhận `floor(TổngGG×100 × giá trị dòng / tổng giá trị) / 100`, phần dư từng xu chia lần lượt cho dòng có phần lẻ lớn nhất. Giá trị dòng = `SL × GB` (VC = CPVC).
- Khớp khi `|Đã phân bổ − Tổng GG| < 1`.
- **Ví dụ 3**: Tổng GG 1,000,000; dòng X bán 6,000,000, dòng Y 3,000,000, VC 1,000,000 (tổng 10,000,000) ⇒ X 600,000; Y 300,000; VC 100,000.

### 5.5 Tổng báo giá & TỶ SUẤT TỔNG (FE:1904-1925, 2152-2192)

Bảng Tổng hợp mỗi nhóm (I Hàng hoá chỉ dòng cha, II Dịch vụ, III Chi phí, IV Vận chuyển):
`nhap = Σ thành tiền nhập` · `truoc_vat = Σ thành tiền trước GG` · `chiet_khau = truoc_vat − Σ thành tiền sau GG` · `sau_ck = truoc_vat − chiet_khau` · `vat = Σ tiền VAT` · `sau_vat = sau_ck + vat`. **V Tổng** = cộng 4 nhóm.

| Chỉ số | Công thức | Hiển thị ở |
|---|---|---|
| TSLN trước GG | `round((Tổng.truoc_vat − Tổng.nhap) / Tổng.nhap × 100, 2)` | dưới bảng Tổng hợp |
| **TSLN sau GG** (= "LN" chân trang, dùng tính cấp duyệt) | `round((Tổng.sau_ck − Tổng.nhap) / Tổng.nhap × 100, 2)` — gồm cả Vận chuyển | dưới bảng Tổng hợp, chân trang |
| Tỷ suất LN dòng TỔNG của bảng chi tiết | như trên nhưng **loại Vận chuyển** (hàng hoá + dịch vụ + chi phí) | dòng TỔNG |
| Tổng nhập = 0 | tỷ suất tổng hiện **0%** (không phải "—") | |
| ~VND (chân trang) | `Tổng.sau_ck × Tỷ giá` | |

- Tỷ suất đều tính **trên giá vốn**, **trước VAT** (VAT không ảnh hưởng tỷ suất và cấp duyệt — xác nhận ở design-phase12-vat.md mục 4).
- **Không có tổng/tỷ suất theo từng nhóm hàng**.
- **Ví dụ 4**: Hàng hoá nhập 2,000,000 / trước VAT 2,500,000 / GG 250,000; Dịch vụ nhập 300,000 / bán 500,000; VC nhập 100,000 / bán 200,000 không GG ⇒ Tổng nhập 2,400,000; Tổng trước VAT 3,200,000; sau GG 2,950,000 ⇒ TSLN trước GG = 33.33%; TSLN sau GG = (2,950,000 − 2,400,000)/2,400,000 = **22.92%**; Tỷ suất dòng TỔNG (loại VC) = (2,750,000 − 2,300,000)/2,300,000 = **19.57%**.

**Cấp duyệt dự kiến (FE)**: `max(cấp theo Giá trị đơn hàng = Tổng.sau_ck × tỷ giá (VND), cấp theo TSLN sau GG)` tra bảng cấu hình duyệt giá (khoảng `[min, max)`; không khớp → cấp 3) (FE:1816-1821, 3302-3313).
**BE (cấp thật khi Gửi duyệt)**: `max(giá trị đơn hàng VND, TSLN tổng, TSLN thấp nhất của các dòng HÀNG TẠM)`; báo giá "sạch" (chỉ hàng/dịch vụ ERP, mọi giá bán > 1,000, không GG) → tự duyệt cấp 1 (SVC:3524-3583). Tỷ suất dòng hàng tạm: cha có con lấy giá vốn = Σ giá vốn con; giá nhập = 0 → 0% (không bỏ qua) (SVC:3685-3738).

> ⚠️ Lệch FE ↔ BE cần lưu ý: (1) FE tính Tổng nhập theo **giá vốn dòng cha** (cha ERP combo giữ giá ERP), còn BE `calculateTotals` tính giá vốn cha-có-con = **Σ giá vốn con** (SVC:3585-3631) ⇒ với combo ERP, TSLN/cấp duyệt chân trang có thể khác số trong popup Gửi duyệt. (2) FE không tính điều kiện "tỷ suất dòng hàng tạm" và "tự duyệt" nên cấp chân trang chỉ là dự kiến.

### 5.6 Làm tròn & tiền tệ (FE:2072-2075, 2549-2554, 3256-3287; SVC:156-163)

- Kiểu làm tròn mặc định: **VNĐ, JPY, KRW → Số nguyên (0)** (VNĐ khoá luôn); ngoại tệ khác → tối đa 2 số lẻ. Chữ số hiển thị mọi số tiền và ô nhập theo kiểu đang chọn (chọn -3 thì hiển thị tròn tới nghìn).
- **Áp dụng làm tròn** (ghi thật vào dữ liệu): làm tròn **Giá nhập** của dòng không có con (cha có con tự tính lại từ con) + **Giá bán** của dòng cha/độc lập + Giá nhập & Giá bán dịch vụ. Không làm tròn thành tiền, VAT, GG.
- **Tỷ giá**: tạo báo giá chốt `Tỷ giá = tỷ giá hiện tại của loại tiền` (VNĐ = 1) và **đóng băng** trên báo giá đó (không cập nhật khi sửa). Giá ERP (lưu VND) quy ra ngoại tệ: `round(giá VND / tỷ giá, 2)`; VNĐ giữ nguyên không làm tròn thêm.
- Định dạng số: `,` ngăn nghìn, `.` thập phân.

---

## 6. THAY ĐỔI GIÁ BÁN / GIÁ VỐN

### 6a. Đang TẠO MỚI mà giá ERP thay đổi

1. **Giá đã lên lịch thay đổi trong tương lai** (bảng `product_expected_prices` có ngày hiệu lực > hôm nay):
   - Mỗi lần thêm hàng ERP (và khi mở báo giá), FE gọi `POST erp-price-change-dates` với id hàng ERP **dòng cha** (FE:3339-3358, 4597; CTL:1932-1952; SVC:5191-5216).
   - Dòng có lịch đổi giá → icon ⚠ vàng cạnh Mã, tooltip **"Giá bán thay đổi ngày dd/mm/yyyy"** (ngày gần nhất) (FE:552-558).
   - **Hiệu lực báo giá** = `min(Hôm nay + số ngày hiệu lực cấu hình ERP "quotation_valid_days" (mặc định 30), ngày đổi giá gần nhất của các hàng ERP cấp cha)` (FE:1802-1815; BE tính lại khi lưu SVC:5141-5189). Không có hành động nào khác — chỉ cảnh báo + rút ngắn hiệu lực.
2. **Giá ERP đổi giữa lúc thêm hàng và lúc bấm Lưu**: màn hình **không tự cập nhật, không cảnh báo**. Khi Lưu (và khi Gửi duyệt — BE dựng bản tạm để xem trước cấp duyệt), BE **tự lấy giá ERP hiện hành** (giá vốn + giá bán theo Bảng giá, ĐVT, tỷ giá) cho mọi dòng ERP — số FE gửi lên bị bỏ qua (SVC:2702-2808). Hàng tạm/dịch vụ giữ số đã nhập.
   > ⚠️ Hệ quả: số trên màn tạo mới có thể khác số lưu/khác popup Gửi duyệt nếu giá ERP vừa đổi, hoặc nếu user đổi Tiền tệ sau khi đã thêm hàng.
3. **Đổi ĐVT** của dòng ERP: Giá bán = giá bán của ĐVT đó, Giá vốn = giá vốn của ĐVT (chỉ khi có quyền giá vốn), quy đổi tỷ giá; GG nhập theo % tự tính lại tiền GG; GG tổng → nhắc phân bổ lại (FE:3388-3412). Lưu ý: danh sách ĐVT/giá lấy theo **bảng giá Bán lẻ (cố định price_type 1)** (CTL:970-994); khi Lưu, BE tính lại theo Bảng giá thật của báo giá.

### 6b. Mở CHỈNH SỬA báo giá cũ mà giá ERP đã đổi (Redmine #10791) — FE:3520-3609; SVC:1810-1815, 2254-2274, 3318-3404

Chỉ chạy khi báo giá **Đang tạo** và người mở là **người tạo** (canEdit). Báo giá đã gửi duyệt/duyệt: chỉ xem, giữ nguyên giá đã chốt.

1. Mở màn → FE gọi `POST erp-reprice` (bảng giá + tiền tệ của báo giá) lấy **giá bán ERP hiện hành** cho MỌI dòng ERP (cha, combo, con). So với giá bán đang lưu, lệch > 0.005 ⇒ popup:
   - Tiêu đề **"Đơn giá hàng hoá đã thay đổi"**
   - Nội dung **"Có sự thay đổi về đơn giá của một số hàng hóa. Bạn có muốn cập nhật đơn giá theo thời giá hiện tại không?"** + danh sách tối đa 10 dòng "`<Tên hàng>: <giá cũ> → <giá mới> VNĐ`" (+ "… và N hàng hoá khác")
   - Nút **Đồng ý** / **Từ chối**
   - Không lệch giá bán ⇒ không hiện popup.
2. **Đồng ý**: trên màn cập nhật **Giá bán + VAT** các dòng ERP theo thời giá; giá vốn trên màn chưa đổi; GG tổng đã phân bổ → phải phân bổ lại. Khi **Lưu**, BE ghi **cả giá vốn lẫn giá bán ERP hiện hành** (theo tỷ giá đã chốt của báo giá) + VAT ERP. Dòng ERP không còn giá ở bảng giá → giữ giá cũ.
3. **Từ chối**: màn giữ giá cũ; khi Lưu gửi cờ `keep_saved_erp_prices` ⇒ BE **khôi phục đúng giá vốn + giá bán đang lưu** của các dòng ERP cũ (không tin số FE). Hàng ERP **mới thêm** trong lần sửa này vẫn lấy giá hiện hành. **VAT ERP luôn cập nhật theo danh mục** dù Từ chối.
4. Giá vốn: **không có cảnh báo riêng cho giá vốn**. Nếu chỉ giá vốn ERP đổi (giá bán không đổi) ⇒ không popup, nhưng khi Lưu BE tự cập nhật giá vốn mới ⇒ Tỷ suất LN đổi sau khi lưu.
5. Hàng tạm, dịch vụ: không bị ảnh hưởng (dịch vụ có tỷ lệ giá vốn vẫn tính lại GN = GB × tỷ lệ hiện tại của danh mục).

> ⚠️ Điểm lệch cần QA/BA biết: (a) popup luôn ghi đơn vị "VNĐ" kể cả báo giá ngoại tệ; (b) `erp-reprice` quy đổi bằng **tỷ giá hiện tại** của loại tiền, còn lúc Lưu BE dùng **tỷ giá đã chốt** trên báo giá ⇒ báo giá ngoại tệ có thể thấy số trong popup khác số sau khi lưu; (c) GG mặt hàng nhập theo % KHÔNG được tính lại số tiền GG khi Đồng ý (khác với đổi ĐVT).

### 6c. SAO CHÉP báo giá — MIX; CPM; SVC:280-548, 947-1501; CTL:438-512

**Luồng**: bấm "Sao chép báo giá" (ở danh sách, chi tiết, tab báo giá của dự án) → `GET copy-preview` → không có thay đổi ⇒ mở thẳng màn Tạo mới điền sẵn; có thay đổi ⇒ popup → **Xác nhận Sao chép báo giá** → màn Tạo mới `?copy_from=`. **Không ghi gì xuống DB cho tới khi bấm Lưu** (mã BG cấp lúc Lưu). Lỗi: toast "Không kiểm tra được thay đổi từ ERP" / "Không tải được dữ liệu sao chép".

**Quyền sao chép**: BG lập từ YCBG → cần quyền "Xây dựng giá bán theo phòng/công ty" (403); BG tự lập có dự án → chỉ **Sale phụ trách dự án** ("Bạn không phải Sale phụ trách dự án này"); không dự án → chỉ người lập ("Chỉ người lập báo giá mới được sao chép."). Phải nằm trong phạm vi được xem, ngoài phạm vi → "Không tìm thấy báo giá." (SVC:284-303; CTL:438-512).

**Popup "Phát hiện thay đổi dữ liệu từ ERP"** (CPM): dòng phụ "Báo giá này kế thừa cấu trúc từ **<mã nguồn>**. Hệ thống đã tự động cập nhật giá mới nhất và phát hiện các thay đổi sau". Bảng: Loại thay đổi (badge **Thay đổi giá** / **Thay đổi VAT** cam; **Thay đổi cấu trúc** xanh) · Mã / Tên vật tư · Thông tin cũ (V1) · Thông tin mới (Cập nhật) · Hành động hệ thống. Nút **Xác nhận Sao chép báo giá** ("Đang sao chép..." khi chờ) / **Hủy bỏ**. Rỗng: "Không có thay đổi nào."

| Loại | Phát hiện | Tên hiển thị | Hành động hệ thống |
|---|---|---|---|
| Giá vốn (chỉ người có quyền "Xem giá vốn hàng hoá" thấy dòng này) | giá vốn V1 ≠ giá vốn ERP hiện tại (theo ĐVT, tỷ giá hiện tại) | "<tên> (Giá vốn)" | "Đã cập nhật giá mới" |
| Giá bán | giá bán V1 ≠ giá ERP theo Bảng giá của V1 | "<tên> (Giá bán)" | "Đã cập nhật giá mới" |
| VAT hàng hoá ERP / dịch vụ danh mục | VAT V1 ≠ VAT danh mục | tên | "Đã cập nhật VAT mới" |
| Cấu trúc combo | tập hàng con công thức ERP khác cây con V1 | "<tên> (Vật tư con)"; cũ "N vật tư con" → mới "M vật tư con (thêm a, bớt b)" | "(Bỏ qua) — Giữ nguyên cấu trúc V1" |

**User KHÔNG được chọn giữ giá cũ** — chỉ có Xác nhận (lấy giá mới) hoặc Hủy bỏ. Quy tắc dữ liệu bản sao:
- **Hàng ERP**: Giá vốn + Giá bán = **giá ERP hiện tại** (Bảng giá + Loại tiền của V1, theo ĐVT dòng), quy đổi bằng **tỷ giá hiện tại** (không dùng tỷ giá V1); VAT = VAT ERP.
- **Hàng tạm**: giữ nguyên giá vốn, giá bán, VAT, **mã hàng tạm** của V1.
- **Cấu trúc** (thứ tự dòng, nhóm, cha–con, ẩn/hiện con): đóng băng theo V1.
- **GG mặt hàng**: giữ vế user đã nhập (nhập % → giữ %, tính lại tiền GG theo giá mới; nhập ₫ → giữ tiền, tính lại %).
- **GG tổng**: khoản kiểu % giữ %, tính lại tiền theo tổng mới; kiểu ₫ giữ nguyên tiền; **tự phân bổ lại** toàn bộ (Largest Remainder).
- **Dịch vụ**: giữ giá bán; giá vốn tính lại theo tỷ lệ danh mục (nếu có); VAT theo danh mục.
- **Header**: copy Dự án, KH, Giai đoạn, Giao hàng, Bảo hành, Điều khoản, Ghi chú, Tiền tệ, Bảng giá, Phương thức GG, Làm tròn, Vận chuyển. Reset: trạng thái Đang tạo, người tạo = người sao chép, hiệu lực tính lại; **không kế thừa YCBG**. Bản sao luôn là **báo giá tự lập** (BG nguồn từ BOM bị ngắt BOM, bỏ Giải pháp/Hạng mục).
- Trên màn Tạo mới bản sao: vẫn được thêm/xoá/sửa như báo giá thường; đổi Dự án theo §1.1 (giữ chi tiết). Khi Lưu, BE lại lấy giá ERP hiện hành cho dòng ERP (theo tiền tệ/bảng giá đang chọn).

---

## 7. Danh sách API liên quan

| API | Dùng cho | Nguồn |
|---|---|---|
| `GET assign/quotations/price-types` | danh mục Bảng giá | CTL:933 |
| `GET assign/bom-lists/currencies` | danh mục Tiền tệ | FE:3320 |
| `GET assign/quotations/erp-product-search` (+`price_type_id`) | popup tìm hàng ERP | CTL:864 |
| `POST assign/quotations/erp-reprice` | tính lại giá bán ERP khi đổi bảng giá / mở Sửa | CTL:905 |
| `POST assign/quotations/erp-product-units` | ĐVT + giá theo ĐVT (giá vốn null nếu không quyền) | CTL:970 |
| `POST assign/quotations/erp-price-change-dates` | ngày đổi giá sắp tới + hiệu lực mặc định | CTL:1932 |
| `GET assign/bom-lists/erp-recipe-children` | nạp con combo ERP | FE:4542 |
| `GET assign/erp-costs` / `POST assign/erp-costs` | danh mục dịch vụ/chi phí, tạo nhanh | CCP, CQC |
| `GET assign/product-projects?only_temp=1` / `reuse-children` | kho hàng tạm tái sử dụng | POP:1362-1515 |
| `GET {id}/copy-preview`, `GET {id}/copy-draft` | Sao chép | CTL:438, 478 |
| `POST assign/quotations` · `PUT assign/quotations/{id}` · `POST preview-submit` · `POST create-and-submit` | Lưu / Gửi duyệt | CTL:304-360, 608 |
| `DELETE {id}/service-items/{itemId}` | xoá dịch vụ đã lưu (ngay lập tức) | FE:4189 |

---

## 8. Tổng hợp thông báo nguyên văn (ngoài các bảng trên)

- Toast lưu: "Đã tạo báo giá", "Đã lưu báo giá"; lỗi chung "Lỗi lưu" (hoặc câu BE).
- "Không tải được báo giá", "Không tải được thông tin dự án", "Không tải được sản phẩm BOM".
- Popup thông báo: "Dự án này có BOM. Vui lòng chọn loại tiền tệ trước để tính tỷ giá quy đổi khi tải sản phẩm từ BOM."
- Popup Tạo mới khi preview lỗi: "Không tính được cấp duyệt. Vui lòng kiểm tra giá sản phẩm."
- Mỏ neo (dự án con): banner "Báo giá **<mã>** đã được duyệt và là **Báo giá Mỏ neo** của dự án cha. ..." / "Báo giá này đang **lệch N điểm** so với Báo giá Mỏ neo **<mã>** — cần đồng bộ trước khi Trình duyệt. Xem chi tiết"; popup "Không thể trình duyệt — vi phạm quy tắc đồng bộ"; toast sau Lưu nháp "Lưu ý: <lỗi đầu> Hệ thống vẫn lưu nháp, nhưng cần đồng bộ trước khi Trình duyệt." (FE:257-282, 1280-1296, 4004-4011).
- BE tạo-và-gửi: "Cấp duyệt của báo giá vừa thay đổi thành cấp 1 (tự duyệt). Vui lòng bấm Gửi duyệt lại để xác nhận." (SVC:3867).
- BE: "Bạn không có quyền áp dụng giảm giá trong báo giá" (403).
- Popup tìm hàng: "Không thể tải danh mục lọc từ ERP.", "Không thể tải danh sách hàng hoá từ ERP."

## 9. Các điểm code đáng lưu ý (để BA quyết có đưa vào SRS hay báo dev)

1. Tỷ suất LN = (Bán − Vốn)/**Vốn** (markup), không phải biên trên giá bán.
2. Không có tổng tiền/tỷ suất theo nhóm hàng.
3. Xoá nhóm không hỏi xác nhận; xoá dịch vụ đã lưu ghi DB ngay (không chờ Lưu).
4. Ô "—" của Tỷ suất LN dùng class `text-muted` (trong hrm-client bị ép màu đỏ) → có thể hiện "—" màu đỏ.
5. Đổi tiền tệ không quy đổi giá trên màn nhưng BE quy đổi giá ERP khi lưu.
6. Giá theo ĐVT lấy bảng giá Bán lẻ cố định; BE tính lại theo bảng giá thật khi lưu.
7. Popup thay đổi đơn giá (#10791) chỉ so giá bán, ghi cứng "VNĐ", dùng tỷ giá hiện tại; giá vốn đổi âm thầm khi lưu.
8. Kiểm tra BE "giá bán > 0 / GG ≤ giá bán" không áp cho dòng hàng hoá của báo giá tự lập (chỉ FE chặn).
9. Cảnh báo giá thấp ≤ 1,000 so số thô, không quy đổi ngoại tệ.
10. FE và BE tính Tổng nhập khác nhau cho combo ERP (dòng cha vs Σ con) → cấp duyệt chân trang có thể khác popup Gửi duyệt.
