# Design — Phiếu xuất hàng mượn (ERP `borrow_exports` → HRM)

> Nhánh `gop_db` · @khoipv · bắt đầu 2026-09-07
> **Spec đầy đủ:** `docs/superpowers/specs/gop-db/2026-09-07-borrow-export-design.md`

## Mục tiêu

Port màn **Phiếu xuất hàng mượn** của ERP (`borrowExport.*`) sang HRM, **đóng kín** luồng đã port
dở ngày 2026-09-04: nút "Duyệt" ở màn *Yêu cầu xuất hàng mượn* hiện chỉ bắn toast *"chưa được
triển khai"* (`pages/finance/borrow-export-requests/_id/index.vue:372`).

## Màn này là gì

Không phải chứng từ do người dùng nghiệp vụ tự lập, mà là **hành động DUYỆT của Kế toán kho** đối
với 1 *Phiếu yêu cầu xuất hàng mượn*, được ERP hiện thực hoá thành chứng từ riêng để lưu "duyệt bao
nhiêu, trừ vào phiếu mượn nào".

Một lần bấm Lưu = 5 việc trong 1 transaction: sinh phiếu `PXHM-NNNNN` → ghi 2 bảng con → ghi ngược
`approved_qty` lên phiếu yêu cầu → cộng `borrow_returned_qty` + `returned_by_other` trên
`product_export_request_details` (phiếu mượn nào trả hết thì `borrow_status = Đã trả`) → duyệt phiếu
yêu cầu cha + bắn thông báo cho người lập.

## Quyết định lớn

| # | Quyết định | Ghi chú |
| --- | --- | --- |
| 1 | **0 migration, 0 permission mới** | 3 bảng ERP có sẵn trên DB gộp (280/655/941 dòng); quyền `Kế toán kho` guard `api` đã có id 1136 |
| 2 | **Quyền y hệt ERP** (user chốt 07/09) | `checkPermission:Kế toán kho` cho cả route group. KHÔNG áp bộ 3 quyền "Xem phiếu hàng mượn theo …" như màn Yêu cầu — 2 màn phục vụ 2 nhóm người khác nhau |
| 3 | **Dòng hàng SL = 0 vẫn tạo** (user chốt 07/09) | Giữ đúng ERP. Đã đo: PHP 7.4.3 `0/0` → `NAN` → MySQL lưu `0.00`, không crash. Code HRM viết `$qty > 0 ? … : 0` — kết quả lưu y hệt, chỉ khác là không rải Warning vào log |
| 4 | **Giữ định dạng mã ERP `PXHM-NNNNN`** | Không đổi sang `PREFIX-YYYY-NNNNN` của HRM: bảng dùng chung với cổng ERP đang chạy |
| 5 | **Không có màn Sửa / nút Xóa** | ERP comment tắt cả route lẫn nút |
| 6 | **Dùng lại `BorrowStockService`** | Docblock của service đó đã ghi sẵn màn này thuộc về nó — không chép công thức "Đang mượn" lần hai |
| 7 | **Phạm vi danh sách: không lọc gì** | ERP `searchByFilter()` không có ràng buộc nào — qua được cửa `Kế toán kho` là thấy hết. Không "chuẩn hoá" cho giống màn Yêu cầu |
| 8 | **Gate quyền trong Controller, KHÔNG dùng middleware `checkPermission`** (phát hiện lúc code 07/09) | Quyền `Kế toán kho` guard `api` (1136) đang gán cho **0 role / 0 người**; bản dùng thật là ERP guard `web` (100080, 19 role). Middleware gọi spatie `getAllPermissions()` chỉ trả quyền cùng guard ⇒ gắn vào là khoá sạch mọi người, super admin cũng 403 (test thật emp 13 role 18). Dùng `BorrowExport::isAccountant()` (trait 2 guard) ở đầu cả 7 action |
| 9 | **Đơn giá vốn gate quyền `Xem giá vốn hàng hoá` (1092)** | ERP đổ thẳng ra màn. CLAUDE.md bắt buộc gate ở BE + trả `null`, không dựa FE ẩn. Lịch sử **không log** giá vốn — log là bản chụp vĩnh viễn, không gate lại được lúc đọc |

## 5 chỗ cố ý làm khác ERP

| # | ERP | HRM | Vì sao |
| --- | --- | --- | --- |
| 1 | Chờ duyệt / Đang tạo tô **đỏ** | Đang tạo xám · Chờ duyệt vàng · Đã duyệt xanh · Không duyệt đỏ | SRS: đỏ chỉ dành cho Từ chối/Khoá |
| 2 | Route In là **code chết** — gọi hằng `ReportTemplate::XUAT_HANG_MUON` không tồn tại, `print_data` comment sạch, nút In đã comment | Dựng bản in thật (blade + `ReportPrintPreviewModal`) | "đầy đủ như ERP" ở đây = ERP không có gì chạy được |
| 3 | Excel lặp 2 cột "Người lập", thiếu Trạng thái | `ExportFieldsModal` cho user chọn trường | Chuẩn HRM + sửa lỗi hiển nhiên |
| 4 | Không có lịch sử | `catalog_histories` — popup ở DS + khối ở Chi tiết | User yêu cầu thêm |
| 5 | Nhãn "Phiếu yêu cầu xuất **bán** hàng mượn" ở màn Tạo/Chi tiết | "Phiếu yêu cầu xuất hàng mượn" | ERP copy nhầm từ màn `borrow_sells`; nguồn dữ liệu là `borrow_export_requests` |

## Ngoài phạm vi

- `ProductExportRequest::dataForBorrowReturn()` thiếu phép trừ `returningQty` (ghi nhận từ 04/09) —
  màn đang chạy thật, cần user duyệt riêng.
- 3 màn còn lại họ "hàng mượn": YC xuất bán · Phiếu xuất bán · YC gia hạn.
