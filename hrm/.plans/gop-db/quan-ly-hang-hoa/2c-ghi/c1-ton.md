# Đợt 2-C1 — Tồn trước khi lập plan

> 07/10/2026 · gộp từ `c1-khao-sat-be.md` §8 (Q1–Q8) + `c1-khao-sat-fe.md` §8 (Q1–Q13), bỏ trùng.
> Luật cao nhất: `chot.md` (G1–G11, T6, H1'). Hỏi LẦN LƯỢT từng câu; chưa trả lời hết thì không lập plan code.

## A. Đã có chốt sẵn — không hỏi lại

| # | Điểm | Theo chốt |
|---|---|---|
| A1 | `products.product_type` (chuỗi) của hàng HRM tạo | `man-danh-muc-hang-hoa/design.md` §6 (user 21/09): KHÔNG ánh xạ ⇒ để NULL. Hệ quả: hàng HRM tạo **chưa hiện ở popup 338 màn ERP** (`SearchController` lọc `!= 'service_product'`, NULL bị loại) tới khi sửa ERP ⇒ thêm việc ngoài luồng **N9** vào `chot.md` |
| A2 | Chủ sửa tab Quản trị của hàng CŨ chưa có dòng công ty | G4 áp ngay ở 2-C1: sinh dòng `coefficient 1, status 3` — upsert (5 dòng hệ số cũ của chính công ty tạo đã tồn tại) |
| A3 | Hệ số công nghệ | T6: cột chung `products.tech_coefficient`, chỉ công ty tạo sửa |

## B. Tự chốt (thuần UI / DB ép) — ghi để user biết, phản đối thì đổi

| # | Điểm | Tự chốt |
|---|---|---|
| B1 | Thương hiệu · Hãng SX · Xuất xứ | gắn `*` bắt buộc — DB NOT NULL không default + Hãng SX là nguồn sinh mã |
| B2 | Video | nhiều dòng như bảng `product_videos` ERP |
| B3 | Lưu tạo mới xong | chuyển sang màn chi tiết hàng vừa tạo (thấy mã vừa sinh) |
| B4 | Cờ Phụ tùng ô tô | cột `product_natures.is_auto_parts` tinyint default 0; ô tick col-6 cạnh *Mẫu in barcode* trong modal; thêm cột ở danh sách Tính chất; KHÔNG làm Excel ở 2-C1 |
| B5 | Báo lỗi | lỗi 422 ⇒ chấm đỏ mọi tab có lỗi, mở tab lỗi đầu tiên rồi `scrollToFirstError` (pane `v-show` ẩn thì util bỏ qua) |

## C. Hỏi user (thứ tự theo mức ảnh hưởng)

| # | Câu | ⭐ đề xuất | Trả lời |
|---|---|---|---|
| C1 | Catalog ≥ 1 nhánh (C5-a) còn bắt buộc khi Lưu sau G3? | còn, cả tạo lẫn sửa | ✅ theo ⭐ (07/10) |
| C2 | Sửa hàng CŨ (45.890 hàng `product_type_id` NULL) có buộc chọn Loại SP? | buộc | ✅ theo ⭐ (07/10) |
| C3 | `tech_coefficient` = 0 ở 11.156 hàng cũ vs rule ERP `min:1` | `min:0`, tạo mới mặc định 1 | ✅ theo ⭐ (07/10) |
| C4 | Rule trùng tên (tên × model × thương hiệu × hãng; 30 nhóm trùng sẵn) | chỉ kiểm khi 1 trong 4 cột đổi | ✅ theo ⭐ (07/10) |
| C5 | Ảnh đại diện bắt buộc? quan hệ với Hình ảnh ≤10 | không bắt buộc; ảnh đầu = avatar | ✅ theo ⭐ (07/10) |
| C6 | Tài liệu kỹ thuật: ERP = chọn loại tài liệu (+ tệp ở bảng `files`) vs mockup = upload | theo ERP: bảng dòng Loại tài liệu + tệp | ✅ theo ⭐ (07/10) |
| C7 | ĐVT đã lưu: xoá / đổi hệ số / đổi đơn vị cơ bản? | khoá dòng đã lưu, chỉ thêm mới | ✅ theo ⭐ (07/10) |
| C8 | Đổi Loại SP sang Tính chất không phụ tùng khi đã khai xe | xoá liên kết xe khi Lưu, cảnh báo trước | ✅ theo ⭐ (07/10) |
| C9 | Thuộc tính: thêm ngoài loại? cờ Bắt buộc ép nhập? đổi loại giữ giá trị? | dòng = thuộc tính theo Loại SP ∪ thuộc tính hàng đang có; tick "Bắt buộc" = dùng (chỉ dòng tick lưu + phải có giá trị, như ERP); đổi loại giữ giá trị trùng; không thêm tự do | ✅ theo ⭐ (07/10) |
| C10 | Chọn Loại SP tự điền % VAT | điền khi ô VAT trống | ✅ theo ⭐ (07/10) |
| C11 | Nút "+" thêm nhanh danh mục | chỉ Model, gọi route danh mục sẵn có, ẩn khi thiếu quyền | ✅ theo ⭐ (07/10) |
| C12 | Nút Sửa ở menu dòng những màn nào | *Nhập thông tin* + *Dữ liệu hàng hoá công ty*; footer chi tiết theo `can_edit` | ✅ theo ⭐ (07/10) |

**07/10/2026: user chốt đủ C1–C12, tất cả theo ⭐.** A/B giữ nguyên. Tiếp: lập `c1-plan.md`.
