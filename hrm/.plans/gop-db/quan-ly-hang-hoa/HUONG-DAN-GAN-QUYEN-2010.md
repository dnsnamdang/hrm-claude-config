# Hướng dẫn gán quyền sau go-live — Chuyển đổi hàng hoá (21/10/2026)

> Prod 20/10: `permission:sync` đã THÊM 30 quyền mới — **chưa gán cho vai trò nào** ⇒ người dùng chưa thấy menu / nút tương ứng.
> 43 quyền danh mục hàng hoá / xe 2b / catalog cũ đã có gán sẵn (Cty 1) — chỉ cần bổ sung công ty khác nếu cần.
> Danh sách NGƯỜI đang có quyền ERP tương đương (để biết gán cho ai): `catalog-import/golive-2010/gan-quyen-theo-quyen-erp-2010.xlsx`
> (sheet "Tom tat" + 1 sheet / nhóm, đo trên bản sao prod 20/10, chỉ NV còn làm).

## Nguyên tắc (đọc trước)
1. **HRM chỉ đọc quyền qua VAI TRÒ** — tick quyền thẳng cho nhân viên không có tác dụng.
2. **Quyền gán THEO CÔNG TY**: sửa vai trò ⇒ **chọn công ty** ⇒ tick. Người làm ở Cty 1 + Cty 4 cần vai trò được tick ở CẢ 2 công ty.
3. **Super admin KHÔNG tự có quyền** — muốn dùng cũng phải tick.
4. Vai trò HRM ≠ vai trò ERP (HRM 59 vai trò kiểu "Quản lý_TPE", "Kinh doanh Tự xử lý DATKT"…) ⇒ không chép được 1–1; dùng file Excel để biết AI cần quyền.
5. Gán xong: VPS HRM `cd /var/www/tpe/hrm-api && php artisan cache:clear` (HRM tpe dùng cache **file**, an toàn), người dùng đăng xuất / đăng nhập lại.

**Đường vào:** HRM › Quản trị hệ thống › Người dùng & phân quyền › **Danh sách phân quyền** › (Thêm mới hoặc Sửa vai trò) › **chọn công ty** › mở khối phân hệ › mở nhóm › tick › Lưu.
Gán người: Người dùng & phân quyền › Nhân viên › sửa nhân viên › thêm vai trò.

## Cách khuyên dùng: tạo 8 vai trò HRM theo chức năng
Dễ quản lý hơn rải quyền vào vai trò có sẵn; người cần thì thêm vai trò (1 người có thể nhiều vai trò).

| # | Tên vai trò HRM (gợi ý) | Tick các quyền (khối › phân hệ › nhóm) | Ai cần (nguồn: quyền ERP đang có — sheet tương ứng) | Ưu tiên |
|---|---|---|---|---|
| R8 | **Danh mục xe** | QUẢN TRỊ › Danh mục chung › *Danh mục hàng hóa*: Xem / Quản lý danh mục **biển số xe · lái xe ngoài · xe · nhiên liệu** (8 quyền) | ERP "Quản lý dòng xe" / "Quản lý trọng tải xe" (44 NV) — tối thiểu 8 người đang thao tác: Thơm 311, Thúy 34, Lợi 787, Thịnh 408/1035, Ly 332, Dũng 917, Nhung 204, Hồng 336 | **Gấp** — ERP đã chặn ghi xe |
| R3 | **Giá bán - Cập nhật** | 4. KINH DOANH - TÀI CHÍNH › Tài chính › *Hàng hoá*: **Cập nhật giá bán hàng hoá** · **Cấu hình chính sách giá bán nội bộ** | ERP "Quản lý giá" / "Cập nhật nhanh giá hàng hóa" (112 NV) — thực tế: Kế toán quản lý giá bán, Phát triển kinh doanh, XNK… | **Gấp** — ERP đã khoá sửa giá |
| R4 | **Giá bán - Duyệt** | Tài chính › *Hàng hoá*: **Duyệt giá bán hàng hoá** | ERP "Duyệt giá hàng hóa" (31 NV) — Giám đốc, GĐ phòng PTKD, Kế toán quản lý giá bán | **Gấp** |
| R5 | **PTKD - Duyệt hỏi giá** | Tài chính › *Hàng hoá*: **PTKD duyệt yêu cầu hỏi giá** + Danh mục chung › *Hàng hoá*: **Xây dựng thông tin hàng hoá** (thiếu ⇒ ẩn nút Sửa hàng tạm) | ERP "PTKD duyệt yêu cầu hỏi giá" (44 NV) | **Gấp** — YCHG chuyển HRM |
| R6 | **XNK - Xử lý hỏi giá** | Tài chính › *Hàng hoá*: **XNK xử lý yêu cầu hỏi giá** | ERP "XNK duyệt yêu cầu hỏi giá" (63 NV) | **Gấp** |
| R7 | **Tính giá (Kế toán mua hàng)** | Tài chính › *Hàng hoá*: **Tính giá bán hàng hoá** (+ 2. VĂN PHÒNG SỐ › Giao việc › *Báo giá*: **Xem giá vốn hàng hoá** nếu cần cột giá vốn) | ERP "Kế toán mua hàng" (43 NV) | **Gấp** |
| R1 | **Hàng hoá - Xây dựng thông tin** | Danh mục chung › *Hàng hoá*: **Xây dựng thông tin hàng hoá** · **Xem dữ liệu hàng hoá công ty** · **Xuất excel danh sách hàng hoá** (+ các quyền *Xem danh mục …* trong nhóm *Danh mục hàng hóa* cho ô chọn trong form) | ERP "Thêm hàng hóa" / "Sửa hàng hóa" (251 NV — nhiều vai trò rộng; chọn người thật sự nhập hàng: Quản lý hàng hóa, Duyệt hàng hóa, Kế toán quản lý giá bán, XNK, PTKD…) | Cao |
| R2 | **Catalog kinh doanh** | Danh mục chung › *Hàng hoá*: **Xây dựng catalog kinh doanh** (+ Xem danh mục chương · mục · tiểu mục) | ERP "Xem lĩnh vực" / "Xem chương" (28 NV) — Marketing, Quản lý hàng hóa, PTKD | Vừa |

Người chỉ cần XEM hàng hoá (kinh doanh, kế toán…): thêm **Xem dữ liệu hàng hoá công ty** vào vai trò sẵn có của họ (vd "Quản lý_TPE",
"Kinh doanh Tự xử lý DATKT", "Quản lý_CN Sài Gòn"…) — đúng công ty.

## Kho / kiểm kê (feature của đồng đội, cùng đợt — 12 quyền, chưa gán)
Tên quyền TRÙNG tên ERP ⇒ gán cho đúng người đang có quyền ERP cùng tên (Thủ kho, Thủ kho 1/2, Kế toán bán hàng, Kiểm soát…):
Quản lý kho · Khai báo tồn kho đầu kỳ · Điều chuyển vị trí · Xem điều chuyển vị trí theo kho / theo công ty / theo tổng công ty ·
Lập phiếu kiểm kê kho theo hàng hóa · Xử lý phiếu kiểm kê hàng hóa · Xem phiếu kiểm kê hàng hóa - theo công ty / theo tổng công ty ·
Tổng kiểm kê kho theo hàng hóa · Tổng kiểm kê kho theo hàng hóa - tổng công ty. Hỏi đồng đội làm feature kho trước khi gán diện rộng.

## Kiểm sau khi gán (VPS HRM, chỉ đọc)
```sql
-- mỗi quyền mới đã gán cho vai trò nào, ở công ty nào (rỗng cột ⇒ chưa gán)
SELECT p.name, GROUP_CONCAT(DISTINCT CONCAT(COALESCE(NULLIF(r.display_name,''), r.name), '[', rp.company_id, ']') SEPARATOR ' · ') gan
FROM permissions p
LEFT JOIN role_has_permissions rp ON rp.permission_id = p.id
LEFT JOIN roles r ON r.id = rp.role_id
WHERE p.guard_name = 'api' AND p.name IN ('Xây dựng thông tin hàng hoá','Xem dữ liệu hàng hoá công ty','Xuất excel danh sách hàng hoá',
 'Xây dựng catalog kinh doanh','Cập nhật giá bán hàng hoá','Duyệt giá bán hàng hoá','Cấu hình chính sách giá bán nội bộ',
 'PTKD duyệt yêu cầu hỏi giá','XNK xử lý yêu cầu hỏi giá','Tính giá bán hàng hoá','Xem danh mục xe','Quản lý danh mục xe',
 'Xem danh mục biển số xe','Quản lý danh mục biển số xe','Xem danh mục lái xe ngoài','Quản lý danh mục lái xe ngoài',
 'Xem danh mục nhiên liệu','Quản lý danh mục nhiên liệu')
GROUP BY p.name ORDER BY p.name;
```
Rồi nhờ 1 người mỗi nhóm đăng nhập lại kiểm thấy menu: Danh mục xe · Cập nhật / Duyệt giá bán · YC hỏi giá (PTKD / XNK) · YC tính giá / Phiếu tính giá · Dữ liệu hàng hoá công ty.

## Việc nghiệp vụ đi kèm (không phải quyền nhưng thiếu là chức năng chết)
- Phân công XNK theo công ty — Cty 2/5/6/7/8 chưa có ⇒ không gửi được YC hỏi giá.
- Nhập danh mục **Đặc tính sản phẩm** (đang 0) ⇒ chưa có thì không tạo được hàng tạm.
- Cờ "Hàng hoá làm dịch vụ" / "Dùng cho báo giá dịch vụ" trên Tính chất (đang tắt).
