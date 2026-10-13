# Đợt 2-D2 — Tồn trước khi lập plan (09/10/2026)

> 🔴 **09/10/2026 — USER ĐẢO QC-2:** *"bắt buộc phải xử lý bảng giá riêng trước, bây giờ làm màn cập nhật giá + duyệt giá trước sẽ
> không có ý nghĩa gì, vì việc chuyển quản lý giá riêng theo công ty là nội dung chính của lần này. Các chức năng khác đều phải phục
> vụ logic giá mới."*
> ⇒ **Bảng giá theo công ty (Hướng B, A4/A5 30/09; design §19 §24 §25) làm TRƯỚC**, kéo Phase 8 lên thành nội dung chính.
> Màn Cập nhật giá + Duyệt giá dựng TRÊN mô hình giá mới ⇒ các câu D1–D4 dưới đây (đã trả lời) giữ làm đầu vào nhưng phải soát
> lại sau khi chốt mô hình giá mới; D2b, D5–D12 **tạm dừng** (chưa hỏi). Khảo sát `d2-khao-sat-be.md`/`d2-khao-sat-fe.md` viết
> theo giả định bảng chung — phần luồng ERP vẫn dùng được, phần thiết kế HRM phải làm lại.

> Gộp từ `d2-khao-sat-be.md` §F (F1–F10) + `d2-khao-sat-fe.md` §F (F1–F8). Mã gốc ghi trong ngoặc (BE-Fx / FE-Fx).
> Luật cao nhất: `ton.md` mục C (QC-0…QC-10), `../2c-ghi/chot.md`, `SO-CHOT-VA-TON.md`. Hỏi LẦN LƯỢT; chưa trả lời hết thì không lập plan.

## Phát hiện mới so với khảo sát C

- 🔴 Duyệt giá ĐÃ chạy thật (47 ĐVT có `approve_time` 04/07/2025–26/01/2026, Cty 1 + Cty 4); `product_approves` rỗng vì ERP **xoá cứng** sau khi xử lý. Cờ "không duyệt" còn trên 18 ĐVT / 92 dòng giá / 17 giá hiệu lực. (Khảo sát C ghi "0 lần" là sai.)
- 🔴 Duyệt giá là **nhánh của nút Lưu** ở Cập nhật giá nhanh khi công ty tạo hàng bật `is_company_price` (+ hãng) ⇒ 2 màn làm cùng đợt.
- 🔴 ERP Duyệt ⇒ `products.status = 1`, Không duyệt ⇒ `5`. HRM suy "Đang kinh doanh" từ `status = 1`.
- 🔴 Quy định HRM tab Hàng hoá: ô "Hãng cần duyệt" (`brand_ids`, `new_brand_ids`) nạp **Thương hiệu**, ERP so với **Hãng SX** (`manufacture_id`).
- ⚠️ Cty 8 bật `is_new_company`/`is_new_brand` ⇒ duyệt hàng tạm ERP (Phase 6) + Phiếu tính giá ERP (Phase 7) vẫn sinh `product_approves` ⇒ màn Duyệt HRM phải đọc được + xoá bản ghi sau xử lý như ERP.
- ERP duyệt hàng loạt hỏng (FE gửi `price`, BE đọc `prices`), `approvesSubmit` áp giá đề nghị chứ không áp giá đã sửa; 4 route duyệt không gate (N29).
- ERP không hiện công khoán + ĐMGG thanh lý trên màn giá (chỉ gửi lại giá trị cũ) ⇒ HRM không hiện, không ghi (tự chốt).
- Không cần migration: lịch sử vào `catalog_histories` (endpoint riêng có gate vì có giá vốn), bảng duyệt dùng sẵn. Quyền đề xuất **1657** Cập nhật giá bán hàng hoá · **1658** Duyệt giá bán hàng hoá (1679–1698 đã dùng ở `origin/develop`).
- Số mã sửa được theo luật ERP: Cty 1 27.029 · Cty 4 966 · Cty 3 14 · Cty 2 1 · Cty 5–8 0.

## Hỏi user

| # | Gốc | Câu | ⭐ | Hệ quả | Trả lời |
|---|---|---|---|---|---|
| D1 | BE-F1, FE-F2 | Duyệt/Không duyệt có đổi `products.status` không? | ⭐ (BE) **chỉ đổi khi hàng đang `status = 2`** (2→1 duyệt, 2→5 không duyệt); hàng đang bán giữ nguyên. FE đề xuất "không đổi" | Theo ⭐: hàng tạm/hàng mới Cty 8 chờ duyệt vẫn lên bán được; hàng đang bán bị từ chối giá không biến mất. Không đổi bao giờ: hàng tạm duyệt xong kẹt status 2. Y ERP: một lần Không duyệt là hàng đang bán biến mất khỏi màn HRM | ✅ theo ⭐ (09/10) |
| D2 | BE-F2, FE-F1 | Màn giá hiện hàng nào? | ⭐ mặc định chỉ hàng công ty mình sửa được; ô lọc "Xem toàn bộ" ở chế độ chỉ đọc; hàng không sửa được (Đang nhập thông tin…) hiện khoá | Chỉ hàng sửa được: gọn, Cty 2 không thấy 28.378 mã không sửa được. Hiện tất cả như ERP: tra giá tiện nhưng phần lớn ô bị khoá | 🔄 (09/10) **chỉ lấy hàng hoá ĐANG KINH DOANH ở công ty của user** (trạng thái theo công ty, gồm cả hàng lấy về) — không có chế độ xem toàn bộ. Ý ban đầu: "giá bán tách riêng các công ty tự quản lý". Hàng lấy về sửa được không ⇒ D2b |
| D3 | BE-F3, FE-F4 | Hàng **Ngừng kinh doanh** (4) và **Chờ tính giá** (2) có cho sửa giá? | ⭐ khoá cả 2 (BE chặn 423) | Khoá: giá chỉ đổi khi hàng đang bán; hàng chờ tính giá đợi Phase 7. Cho sửa: lối tắt giống QC-5 đã chặn | ✅ theo ⭐ (09/10) |
| D4 | BE-F9, FE-F3 | Sửa lỗi ô "Hãng cần duyệt" ở màn Quy định (nạp Thương hiệu thay vì Hãng SX) trong 2-D2? | ⭐ sửa luôn trong 2-D2 | Sửa: bật duyệt theo hãng từ HRM áp đúng hàng; +2–3 file + kiểm dữ liệu đã lưu. Để sau (ngoài luồng N-a): ai cấu hình lúc này áp sai hàng im lặng | ✅ theo ⭐ (09/10) — màn = Cấu hình quy định (`/sale/regulation-config`), đổi option `brands` → `manufactures` cho `brand_ids` + `new_brand_ids` |
| D5 | BE-F6 | Người duyệt có được sửa giá trước khi duyệt? | ⭐ cho sửa giá bán + hiệu lực (duyệt đơn và hàng loạt đều áp giá đã sửa), không sửa giá vốn | Cho sửa: đúng ý ERP (ERP hàng loạt đang hỏng). Không cho: chỉ Duyệt/Không duyệt, muốn khác phải trả về người đề nghị | 🔄 (09/10) "khảo sát theo logic đang có của luồng Duyệt giá ERP" ⇒ theo ERP (`PAC:188-274`): người duyệt SỬA được hệ số/giá/ĐMGG + giá hiệu lực (dời effect_date < mai thành mai), duyệt áp giá người duyệt gửi; giá vốn lấy `pa.cost_price` (không sửa). Duyệt hàng loạt ERP lệch do lỗi (`PAC:473`, FE gửi `price` BE đọc `prices`) ⇒ port theo nghĩa của duyệt đơn (lỗi ERP ghi ngoài luồng) |
| D6 | BE-F4, FE-F8 | Ô lọc Còn/Hết tồn (ERP có ô, BE đã comment ⇒ không tác dụng) | BE ⭐ làm thật · FE ⭐ bỏ | Làm thật: thêm query tồn theo công ty (nặng hơn với 27k mã). Bỏ: y hành vi thực tế ERP |✅ (09/10) làm lọc thật theo tồn công ty mình |
| D7 | BE-F5 | Nút "Cập nhật thủ công" (`manualUpdatePrices`, GET có ghi, không lọc cờ chờ duyệt) | ⭐ chặn + ẩn nút (cron 01:00 vẫn chạy) | Chặn: hết đường áp nhầm giá chờ duyệt = 0. Giữ: người dùng còn cách áp giá ngay khi cron chưa chạy |✅ theo ⭐ (09/10) |
| D8 | BE-F7, BE-F8 | Thông báo | ⭐ prefix `[GIA]` báo người có quyền 1658 khi có đề nghị; thêm báo "Đã duyệt/Không duyệt" cho người đề nghị (ERP không có); bản ghi do PTG/hàng tạm ERP sinh thì HRM KHÔNG bắn thêm, chỉ đổi link thông báo ERP sang màn HRM | Theo ⭐: người đề nghị biết kết quả. Không thêm: y ERP |✅ theo ⭐ (09/10) — báo 2 chiều |
| D9 | FE-F5 | Menu | ⭐ Danh mục dùng chung → Hàng hoá (+2 mục: Cập nhật giá bán, Duyệt giá bán); lối phụ Bán hàng → Phê duyệt | |🔄 (09/10) **phân hệ Tài chính** (vị trí nhóm cụ thể chốt ở mockup theo menu Finance hiện có) |
| D10 | FE-F6, BE-F10 | Lịch sử giá | ⭐ theo hàng hoá, popup ở 2 màn giá; chỉ có từ lúc HRM chạy (không chuyển `product_versions` cũ); chưa thêm khối vào chi tiết hàng hoá | Không chuyển lịch sử cũ: lịch sử ERP còn nhưng không xem được (menu HH ERP đã bỏ ở Q1) |✅ theo ⭐ (09/10) — lịch sử theo hàng hoá × công ty |
| D11 | FE-F7 | Xuất Excel | ⭐ màn Duyệt giá có (như ERP); màn Cập nhật giá không làm ở 2-D2 | |✅ theo ⭐ (09/10) |
| D12 | FE-E | Có làm mockup HTML trước khi code? | ⭐ có: `mockup-gia.html` 2 màn + 3 popup, JS tính thật, style V2 đo từ app | Có: chốt bố cục bảng rowspan trước (bẫy sticky đã trả giá). Không: plan thẳng theo ASCII trong khảo sát FE |✅ (09/10) làm mockup trước |


**09/10/2026: user chốt đủ D1–D12** (D2b hết nhờ P5 của `../gia-theo-cong-ty/ton.md`). Bước kế: design giá theo công ty + mockup 2 màn giá (Finance).