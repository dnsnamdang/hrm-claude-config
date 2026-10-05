# Cổng chặn trước khi code Phase 2 — danh sách tồn cần chốt

> Dựng lại 30/09/2026 từ: sổ chốt §3 · design.md §24e/§24f · §26g · §27g · §28f · §29f · §33i.
> (Bản gom ở phiên trước chỉ nằm trong chat, không được lưu — file này là bản chính từ nay.)
> Cách trả lời: ghi **"đồng ý đề xuất"** hoặc đáp án khác vào cột **Chốt**. Chốt hết mới mở code
> (sổ chốt §2b).

## 0. Đã có đáp án suy ra từ các vòng sau — chỉ cần xác nhận

| Tồn | Đáp án suy ra | Nguồn |
|---|---|---|
| 26g-4 "chưa dùng" xét theo đâu | theo **công ty đang đăng nhập** | §26d, §33m |
| 26g-6 công ty đi mượn sửa lớp chung | **không** — chỉ công ty tạo ra sửa thông tin chung | §26c-bis |
| 33i-6 "Chọn tất cả N" với 45.890 dòng | **trần 100 mã/lượt** ⇒ FE gửi danh sách id là đủ, không cần endpoint theo bộ lọc | §33j |
| 33i-8 Kho có hiện hàng công ty khác chưa lấy về | **không** — phải lấy về mới khai | §26d |
| 29f-2 gate giá vốn liên công ty | BE trả `null` khi không có quyền `Quản lý giá` | §4.4 sổ chốt |
| 29f-4 tách phiếu theo công ty quản lý | **không cần** — phiếu đã tách theo nhóm hãng (1 – n), giá tính cho công ty lập yêu cầu | §33p |

## A. CSDL (8)

| # | Câu | Đề xuất | Nếu chọn khác | Chốt |
|---|---|---|---|---|
| A1 | (26g-2) Trạng thái theo (hàng × công ty) lưu ở bảng nào | Dùng **`product_company_coefficients`** làm bảng chủ: + `status`, **UNIQUE(product_id, company_id)** — §24 đã dồn dữ liệu quản trị vào đây | Bảng mới `product_companies` ⇒ 2 bảng cùng khoá (hàng × công ty), phải giữ đồng bộ tạo/xoá ở mọi đường ghi | ✅ Đồng ý đề xuất (30/09) |
| A2 | (26g-5) Lấy hàng công ty khác về: chép hay tham chiếu | **Tham chiếu** — cùng `products.id`, chỉ sinh dòng mới ở bảng A1 (mockup đã giả định vậy) | Chép mã mới ⇒ 171 bảng FK thấy 2 mã cho 1 hàng, báo cáo ma trận §27 sụp, cột *Công ty đang kinh doanh* vô nghĩa | ✅ Đồng ý đề xuất (30/09) |
| A3 | (26g-8) 45.890 hàng cũ vào trạng thái nào | Sinh 1 dòng A1 cho **công ty tạo** (`products.company_id`): hàng đang hoạt động ⇒ **Đang kinh doanh**, hàng đã ngừng ⇒ không sinh dòng. 5 hàng mồ côi (không công ty) xử lý tay | Gán *Đang nhập thông tin* ⇒ popup tìm hàng của **338 màn** (nguồn = Đang kinh doanh) trắng ngay ngày bật | ✅ Đồng ý đề xuất (30/09) |
| A4 | (3.2 / §24f) MỘT hướng cho "thêm chiều công ty" (giá + dữ liệu quản trị) | **Hướng B** (`company_id` NOT NULL, dữ liệu cũ gán về công ty tạo) cho cả hai — khớp quy trình §26: công ty lấy hàng về **tự tính giá của mình**. Chia 2 bước: thêm cột + gán ngay; **xoá cột chung / ép NOT NULL để cuối**, sau khi rà ERP | Hướng A (nullable, NULL = giá chung) ⇒ ERP sửa 0 file, nhưng có "giá chung" song song — công ty mới lấy hàng về **bán luôn giá chung**, bỏ qua bước tính giá của §26 | ✅ Đồng ý đề xuất (30/09) |
| A5 | (3.1) Tách giá vốn/giá mua ngoài khỏi `product_units` | **Có** (đã suy ra từ §26e: phạm vi công ty gồm giá vốn) ⇒ bảng `product_company_units`, sửa **34 file ERP** | Không ⇒ giá vốn dùng chung 8 công ty, trái §26e | ✅ Đồng ý đề xuất (30/09) |
| A6 | (33i-1) Bảng nối catalog: tên + cột | **`product_business_catalogs`** (`product_id`, `company_id`, `job_cluster_id`) + UNIQUE 3 cột; **chỉ lưu Tiểu mục**, 3 cấp trên join ngược | Lưu cả 4 cột ⇒ lọc nhanh hơn chút, nhưng đổi cha của 1 Tiểu mục là lệch dữ liệu im lặng | ✅ Đồng ý đề xuất (30/09) |
| A7 | (33i-2) Mỗi Tiểu mục thuộc đúng 1 Mục | **Có** — `job_clusters.job_group_id` NOT NULL, 1 cha (điều kiện để A6 chỉ lưu 1 cột) | Cho nhiều cha ⇒ không suy ngược được đường cây, A6 buộc lưu 4 cột | ✅ Đồng ý đề xuất (30/09) |
| A8 | (33i-3) 45.890 hàng đang kinh doanh chưa có catalog | Màn *Hàng đang kinh doanh* **bật điều kiện catalog ngay** + dòng nhắc cam (đã có ở mockup §33e); **popup tìm hàng dùng chung chỉ xét trạng thái, KHÔNG xét catalog** | Popup cũng đòi catalog ⇒ 338 màn trắng tới khi khai xong | ✅ Đồng ý đề xuất (30/09)  🔄 04/10: phần "bật điều kiện catalog ngay" bị ĐẢO ở C5 |

## B. Quyền (3)

> ✅ **04/10/2026 user chốt mô hình quyền riêng, THAY 3 đề xuất dưới đây** — xem `design.md` §35b.
> 5 quyền: Xây dựng thông tin hàng hoá · Xem dữ liệu hàng hoá công ty · Xuất excel danh sách hàng hoá ·
> Xây dựng catalog kinh doanh · Cấu hình chính sách giá bán nội bộ. *Kho dữ liệu* + *Hàng đang kinh doanh* không cần quyền vào.
> 5 chỗ hở đã chốt (§35b): báo cáo không cần quyền · tính giá gác tới 2-tg · xem chi tiết chỉ đọc cho mọi người ·
> xoá hàng chưa dùng theo quyền Xây dựng thông tin · bỏ 1616–1619, cấp **1652–1656**. **Nhóm B ✅ xong.**

| # | Câu | Đề xuất | Chốt |
|---|---|---|---|
| B1 | (26g-3 + 27g-1) Quyền màn *Hàng đang kinh doanh*, *Kho hàng hoá công ty*, *Báo cáo hàng hoá theo công ty* | 1 quyền **"Xem hàng hoá kinh doanh"** cho cả 3 màn chỉ đọc | |
| B2 | (33i-4) Quyền *Xây dựng catalog kinh doanh* | Quyền riêng tên đúng như vậy, gate cả nút lẫn endpoint; id nối tiếp dải 1612+ | |
| B3 | (28f-1) Quyền *Chính sách giá bán nội bộ* | Quyền riêng **"Cấu hình giá bán nội bộ"** (đụng tới tiền, không gộp vào *Tính giá bán hàng hoá*) | |

## C. Luồng chứng từ (7)

> ⏸ **04/10/2026 user chốt: phần TÍNH GIÁ làm ở phase sau, Phase 2 chỉ làm phần Hàng hoá** ⇒ C1, C3, C4 gác tới 2-tg. Còn hỏi C2, C5, C6, C7.

| # | Câu | Đề xuất | Chốt |
|---|---|---|---|
| C1 | (26g-1) Trùng *Phiếu yêu cầu hỏi giá / tính giá* đang chạy ở ERP | Luồng mới **THAY** luồng tính giá ERP cho hàng hoá chính thức; phiếu ERP cũ chỉ còn đọc. *Hàng tạm – Hỏi giá* (Phase 6) giữ nguyên | |
| C2 | (26g-7) Hàng *Đang kinh doanh* sửa thông tin có lùi trạng thái không | **Không lùi** — sửa thông tin giữ nguyên *Đang kinh doanh*; muốn đổi giá thì lập yêu cầu tính giá mới | ✅ Không lùi (04/10) |
| C3 | (29f-3) Yêu cầu tính giá có bước **duyệt** như ERP không | **Bỏ duyệt yêu cầu** — gửi là tới thẳng người phụ trách hãng; chỉ phiếu tính giá có bước *Lưu & duyệt giá bán* | |
| C4 | (29f-5) Chụp lại % chính sách nội bộ lúc tính giá | **Có** — lưu % + gốc tính vào dòng phiếu, sau đổi chính sách không làm sai phiếu cũ | |
| C5 | (33i-5) Gỡ nhánh catalog CUỐI CÙNG của hàng đang kinh doanh | **Popup xác nhận** liệt kê N mã sẽ rời màn *Hàng đang kinh doanh*, không chặn | 🔄 Hàng đang KD **không bắt buộc catalog** ⇒ câu này không còn; ĐẢO A8 (04/10) |
| C6 | (28f-2) % chính sách nội bộ: trần/sàn | **0 ≤ % ≤ 100**, cho nhập 0; vượt thì báo đỏ dưới ô, không tự kéo về | ⏸ Gác — màn Chính sách giá nội bộ sang phase Tính giá (04/10) |
| C7 | (28f-3, 28f-4) Khai trước cho hãng chưa có hàng · công ty mua ngừng hợp tác | **Cho khai trước** mọi hãng · ngừng hợp tác thì **khoá dòng**, không xoá (còn lịch sử) | ⏸ Gác — màn Chính sách giá nội bộ sang phase Tính giá (04/10) |

## D. Excel / hiển thị (2)

| # | Câu | Đề xuất | Chốt |
|---|---|---|---|
| D1 | (33i-7 + 27g-2) Xuất Excel: cột Catalog ở màn Kho · báo cáo ma trận | Cột Catalog **1 ô, mỗi nhánh 1 dòng** trong ô · báo cáo xuất **đúng dạng ma trận** như trên màn | D1-a ✅ Catalog chỉ ghi Tiểu mục · D1-b ⏸ báo cáo để sau (04/10) |
| D2 | (27g-3) Ma trận khi > 8 công ty | **Cuộn ngang khối ma trận**, cột mã + tên dính trái | ⏸ Báo cáo để sau (04/10) |

## E. Việc đã lỡ làm vào source trước §22 (2)

| # | Câu | Đề xuất | Chốt |
|---|---|---|---|
| E1 | (3.4) 2 cờ trên Loại sản phẩm · 2 màn Dòng xe/Tải trọng · 6 màn Xe · Task C1 sinh mã. ⚠️ **04/10 soát lại: danh sách này THIẾU** — hrm-api nhánh feat còn 7 commit Phase 2 làm tối 21/09 (trước §22): migration `+product_type_id/product_characteristic_id` vào `products` (`c59fc9036`) · gỡ `can_retail` (`259ad55cb`) · 4 quyền 1616-1619 + 15 route (`6d5fa8663`, đã bỏ ở §35b) · Entity + 13 model (`799b117bb`) · `/form-options` (`4f9184743`) · list + detail (`cbcb359a8`) · BE tab Phân loại xe (`cf5c489a9`) | **Giữ** (đã e2e xanh); riêng C1 rà lại theo §16 + bẫy `iconv` khác nhau theo máy | |
| E2 | (3.5) Cột `status` thêm vào `vehicle_life` | **Giữ** (bỏ thì Xoá là xoá cứng trên 48.736 dòng tham chiếu) + sửa `VehicleLife` ERP lọc `status` (việc sau §5-10) | |

## Câu phụ

| Câu | Đề xuất | Chốt |
|---|---|---|
| `mockup-hang-hoa.html` (3,2 MB, bản 21/09 lỗi thời) | **Xoá** — bản chốt là `mockup-luong-xay-dung-hang-hoa.html`; để lại dễ mở nhầm | |
| Nhánh code Phase 2 (Task A0) | Merge `feat/p1-danh-muc-hang-hoa` về `gop_db` trước (nghiệm thu Phase 1), rồi mở nhánh Phase 2 **từ `gop_db`** | |

## F. Phát sinh từ vòng sửa mockup §36 (01/10/2026)

| # | Câu | Đề xuất | Chốt |
|---|---|---|---|
| F1 | (§36h-1, §36i) Tab Nhóm máy lưu gì | Lưu **Loại sản phẩm** (`product_type_id`) — câu giải thích nói phụ kiện dùng cho *toàn bộ hàng hoá thuộc 4 cấp*; mã thiết bị chỉ là công cụ chọn | 🔄 Tab Nhóm máy quay về bản trước 01/10 — xem design §35f (04/10) |
| F2 | (§36h-1) Một phụ kiện dùng cho nhiều Loại sản phẩm? | Nếu có ⇒ chọn nhiều + bảng nối `product_accessory_types`; nếu không ⇒ 1 cột | 🔄 Tab Nhóm máy quay về bản trước 01/10 — xem design §35f (04/10) |
| F3 | (§36h-2) Dữ liệu nhóm máy cũ của ERP (`group_ids_use` + máy) | Không di trú (khái niệm đã đổi), ERP chỉ đọc | 🔄 Tab Nhóm máy quay về bản trước 01/10 — xem design §35f (04/10) |
| F4 | (§36h-3) Popup *Xem hàng hoá Công ty khác* còn 2 ô lọc *Dùng cho nhóm máy / máy* | Thay bằng 1 ô *Dùng cho thiết bị* (lọc theo Loại sản phẩm) | 🔄 Tab Nhóm máy quay về bản trước 01/10 — xem design §35f (04/10) |
| F5 | (§36h-4) Tên tab *Nhóm máy* | Đổi thành *Thiết bị sử dụng* (trùng tiêu đề card) | 🔄 Tab Nhóm máy quay về bản trước 01/10 — xem design §35f (04/10) |
| F6 | (§36d) Card *Khai báo hải quan* nay chứa cả *SL tối thiểu nhập mua* | Đổi tên *Thông tin nhập mua* | ✅ Đổi tên "Thông tin nhập mua" (04/10) |
| F7 | (§36e) Bỏ checkbox BVMT — cờ `need_environment_tax` ERP còn đọc | Cờ = 1 khi hệ số có giá trị, = 0 khi trống | ✅ Đồng ý đề xuất + giữ luật 1 ≤ hệ số ≤ 999.999 (04/10) |
| F8 | (§36d) Cột *% giảm giá thanh lý* | Không xoá cột; HRM ngừng hiển thị/ghi; soát ERP còn chỗ đọc | ✅ Bỏ, dùng % Nhóm hàng; 1.251 giá trị cũ đóng băng (04/10) |
| F9 | (§36m, §36n) 11 câu tooltip đề xuất (6 trường quản trị · 4 cấp catalog · 2 tab chính) | Duyệt câu chữ; khi code gom vào 1 hằng chung như `CATALOG_TOOLTIPS` | ✅ Duyệt nguyên văn (04/10) |
