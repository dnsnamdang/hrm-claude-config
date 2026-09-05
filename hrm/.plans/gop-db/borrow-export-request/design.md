# Design — Yêu cầu xuất hàng mượn (ERP `borrow_export_requests` → HRM)

> Phụ trách: @khoipv · Nhánh: `gop_db` · 2026-09-04
> **Spec đầy đủ (schema, API, edge case): `docs/superpowers/specs/gop-db/2026-09-04-borrow-export-request-design.md`**
> Plan + kiểm chứng: `plan.md`

## Mục tiêu

Port màn **Phiếu yêu cầu xuất hàng mượn** từ cổng ERP sang HRM. Khách đang mượn hàng theo Phiếu
yêu cầu xuất hàng loại 3; phần hàng **không trả lại nữa mà xuất hẳn** thì người lập gom các phiếu
mượn liên quan vào 1 phiếu này xin **Kế toán kho** tất toán.

Bảng ERP có sẵn trên DB gộp — **KHÔNG migration, KHÔNG đổi schema**.

## Phạm vi (user chốt 2026-09-04)

| Chốt | Nội dung |
| --- | --- |
| Phạm vi | **Đầy đủ như ERP**: danh sách · chi tiết · tạo mới · từ chối · in phiếu · in danh sách · xuất Excel |
| Nút "Tạo phiếu xuất hàng mượn" | Giữ nút, bấm vào **báo "chưa triển khai"** (màn `borrow_exports` chưa port) |
| Phân quyền | **Tạo quyền HRM trùng TÊN quyền ERP** (guard `api`, id 1565-1567) — không sửa id bản ERP |
| Menu | **2 mục** (Bán hàng + Kế toán/Mượn hàng). Mục thứ 3 của ERP (`Chờ duyệt → Hàng mượn`) **bỏ hẳn** — HRM không làm màn "chờ duyệt" nữa (user chốt 2026-09-04) |

## Quyết định lớn

1. **Module `Finance`, đường dẫn `/finance/borrow-export-requests`** — cùng nhà với họ màn hàng
   giữ (`prepick-*`) và đúng nhóm "Mượn hàng" của menu HRM.
2. **2 cửa vào bằng `?type=`**: `all` (người lập) · `accounting` (Kế toán kho). Một màn duy nhất
   + watcher `$route.query.type`. Preset `for-approve` vẫn chạy được nhưng **KHÔNG có mục menu** —
   người duyệt tìm việc bằng **ô lọc Trạng thái**, đúng convention đã chốt ở Phiếu thu
   (2026-08-18) và nhóm hàng giữ (2026-08-22).
3. **Hàm tính "Đang mượn" tách thành `BorrowStockService` dùng chung** — 3 luồng (trả lại / bán
   hàng mượn / xuất hàng mượn) tranh cùng một lượng hàng, chép mỗi màn một bản là vài tháng sau
   lệch nhau. Đặt tên theo chủ đề nghiệp vụ, không theo tên màn.
4. **KHÔNG làm màn Sửa / nút Xóa** — ERP đã comment tắt cả route lẫn nút.
5. **Đính kèm ghi vào cột `attachments`**, KHÔNG dùng bảng `files` chung: cổng ERP đọc cột đó, ghi
   chỗ khác là bên ERP mở phiếu ra mất sạch đính kèm.
6. ~~**Bảng hàng ở màn Tạo dựng TỰ ĐỘNG** từ phiếu mượn đã chọn~~ — **ĐẢO LẠI 2026-09-05 theo yêu
   cầu user: làm Y HỆT ERP.** Chọn phiếu mượn chỉ nạp vào kho dòng con; bảng chi tiết TRỐNG cho tới
   khi bấm nút `+` ở đầu cột cuối và tự chọn hàng hoá (popup tìm trong **toàn bộ** hàng hoá hệ
   thống). Hàng thêm vào mà không nằm trên phiếu mượn nào → dòng bị **khoá, tô mờ, không nhập số
   lượng** (đúng `can_export = details.length` của ERP); BE `storeProducts()` bỏ qua dòng đó nên
   không lọt vào phiếu. Bỏ phiếu mượn KHÔNG xoá dòng hàng, chỉ mất dòng con — cũng đúng ERP.
   Chi tiết + phần ERP không port: `plan.md` Phase 11.

## 3 chỗ SỬA so với ERP (có chủ ý)

| Chỗ | ERP | HRM | Lý do |
| --- | --- | --- | --- |
| Màu trạng thái | "Chờ duyệt" và "Đang tạo" đều ĐỎ | vàng / xám | SRS: đỏ chỉ dành cho Từ chối · Khoá |
| `searchByFilter()` | cuối hàm ép cứng `company_id = công ty mình`, triệt tiêu quyền "tổng công ty" | bỏ dòng đó | tôn trọng ý nghĩa của quyền |
| `canView()` | chỉ Kế toán kho + người tạo → trưởng phòng thấy phiếu ở danh sách nhưng bấm vào ra `not_found` | cộng thêm 3 nhánh quyền cấp | danh sách và chi tiết phải khớp (đã thử 60 nhân viên, khớp 100%) |

Ngoài ra `can_borrow_export` của ERP viết `status != 5 && borrow_status != 2` (AND — lỗi thứ tự
toán tử) nên lọt phiếu sai trạng thái; bản HRM dùng đúng điều kiện của popup ERP ở cả 2 nơi.

**Popup "Chọn phiếu xuất mượn" — ĐỔI 2026-09-05 về ĐÚNG ERP.** Bản đầu lọc thêm "còn ít nhất 1
dòng chưa trả hết" nên ra **25** phiếu trong khi ERP ra **27**. ERP đặt điều kiện
`need_export = 1 AND base_exported_qty > borrow_returned_qty` ở `getDataForBorrowExport()` — lúc
LẤY DÒNG HÀNG, không phải lúc lọc phiếu. User chốt làm y hệt ERP: **đã bỏ** điều kiện đó khỏi
popup, chấp nhận chọn được phiếu góp 0 dòng hàng. ĐỪNG "sửa lại cho chặt" — đây là lựa chọn có
chủ ý, không phải sót (xem `plan.md` Phase 12).

## Nền

| | |
| --- | --- |
| Dữ liệu thật | 292 phiếu (280 Đã duyệt · 11 Không duyệt · 1 Chờ duyệt) · 686 dòng hàng · 990 dòng chi tiết · 607 pivot |
| Bảng mới | 0 |
| Quyền mới | 3 (guard `api`, id 1565-1567) |
| File BE | 12 mới + 4 sửa |
| File FE | 7 mới + 2 sửa (menu) |

## Ngoài phạm vi

- Màn **Phiếu xuất hàng mượn** (`borrow_exports`, 280 dòng) — nơi thao tác duyệt thật sự xảy ra.
- Sửa `dataForBorrowReturn()` của màn Yêu cầu nhập hàng (thiếu phép trừ `returning_qty` so với
  ERP) — màn đang chạy thật, cần user duyệt trước.
