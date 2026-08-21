# Design (tóm tắt) — Phiếu yêu cầu điều chỉnh công nợ (ERP → HRM)

> Phụ trách: @khoipv · Nhánh: `gop_db` (cả 2 repo, code thẳng trên nhánh này — không tách nhánh riêng) · Ngày: 2026-08-17
> **Spec đầy đủ**: `docs/superpowers/specs/gop-db/2026-08-17-finance-bill-adjust-dept-request-design.md`
> Feature tham chiếu: `.plans/gop-db/finance-bill-payment-request/` · `.plans/gop-db/finance-prepick-cancel-request/`

---

## Mục tiêu

Port màn ERP `admin/income-expenditure/bill_adjust_dept_requests` sang HRM, phân hệ **Tài chính**,
route `/finance/bill-adjust-dept-requests`. Chứng từ đề nghị **chuyển công nợ từ khách hàng/hợp đồng
này sang khách hàng/hợp đồng khác**, kế toán duyệt rồi tạo phiếu kế toán ghi sổ.

**Nguyên tắc user chốt: bám sát logic ERP.** Chỉ đổi nguồn hợp đồng bán và các quy tắc bắt buộc của HRM.

## Scope

**Trong**: 2 loại phiếu (KH + NCC) · 2 mục menu danh sách · tạo/sửa/xóa nháp · gửi duyệt · từ chối ·
popup chọn Phiếu báo có · in · xuất Excel phiếu + danh sách · thông báo chuông · **lịch sử thay đổi** (mới).

**Ngoài**: màn Phiếu kế toán điều chỉnh công nợ (`bill_adjust_dept`) — phiếu dừng ở *Chờ tạo phiếu kế toán*,
kế toán sang ERP tạo và duyệt · màn Phiếu báo có (chỉ đọc để chọn) · không đụng repo ERP ·
**HRM không ghi sổ cái `account_details`**.

## Quyết định lớn (user chốt 2026-08-17)

| # | Quyết định |
| --- | --- |
| 1 | Dùng chung 3 bảng ERP (`bill_adjust_dept_requests` + `_details` + `_detail_items`), **không migration** cho bảng chính |
| 2 | Port **cả 2 loại**: KH (`request_type=1`) và NCC (`request_type=2`, kèm ngoại tệ + tỷ giá + hợp đồng mua) |
| 3 | **Dừng ở "Chờ tạo phiếu kế toán"** — không port màn phiếu kế toán, HRM không ghi sổ cái |
| 4 | **Hợp đồng bán `firm_contracts` → `hrm_contracts`** ở luồng tạo mới; 3 nguồn ERP còn lại (`ServiceContract`, `OpeningContract`, `WrServiceContract`) giữ nguyên |
| 5 | Giữ `FirmContract` trong `morphMap` để 11.037 dòng phiếu cũ mở được |
| 6 | **2 mục menu** như ERP: *Phiếu yêu cầu điều chỉnh công nợ* + *Chờ duyệt* (gate quyền Kế toán thanh toán) |
| 7 | **Cửa vào "Phiếu báo có" giống hệt ERP**: nhận `?bill_income_report_detail_ids=` (danh sách DÒNG người dùng đã tích ở màn Chi tiết phiếu báo có). ~~Popup tự chọn phiếu~~ đã bỏ 2026-08-17 vì làm mất 3 ràng buộc của ERP (chỉ phiếu loại KH · chỉ dòng còn tiền — **968/10.199** dòng · tích từng dòng) |
| 8 | Dùng lại mẫu in ERP `report_templates` **id 209** qua `ErpReportTemplate` |
| 9 | Thêm **4 quyền guard `api`** trùng tên ERP (`Xem tất cả phiếu yêu cầu điều chỉnh của tổng công ty/công ty/phòng ban/bộ phận`); dùng lại `Kế toán thanh toán` id 1152 |
| 10 | Thêm **Lịch sử thay đổi** — 2 bảng mới, là thay đổi DB duy nhất của feature |
| 11 | Base UI: danh sách bám `pages/assign/customers/index.vue`, form bám `CustomerForm.vue` |

## Khác biệt có chủ đích so với ERP

1. Sinh mã bọc transaction + `lockForUpdate` (2 cổng cùng sinh mã dễ trùng).
2. `canEdit()` / `canDelete()` sửa lỗi ưu tiên toán tử của ERP (`status==1 || status==6 && created_by`
   khiến phiếu *Đang tạo* ai cũng sửa được) → HRM: `status IN [1,6] AND created_by = user.id`.
3. Chặn nhảy cóc trạng thái ở BE (ERP gán thẳng `$request->status`).
4. Validate khớp tổng tiền áp cho **cả loại KH** (ERP chỉ kiểm loại NCC).
5. Không dùng middleware `checkPermission` cho route đọc — spatie bỏ sót role `model_type='App\Employee'`.
6. Thêm lịch sử thay đổi.

## Rủi ro đã biết

- ~~`hrm_contracts` có 0 dòng trong `account_details` → công nợ luôn hiện 0~~ → **ĐÍNH CHÍNH
  2026-08-17: SAI**. Thực tế **33/40 hợp đồng HRM có bút toán TK 1311**, tổng công nợ ~25,9 tỷ
  (bộ `HĐ-TEST-DNTT-*` do màn Đề nghị thu tiền tạo). Kết luận sai trước đó do truy vấn qua shell
  bị nuốt dấu `\` trong `contractable_type` nên WHERE không khớp gì.
  ⇒ Quyết định #4 (firm → hrm) **không kéo theo hệ quả mất công nợ** như đã cảnh báo.
- Phiếu HRM tạo gắn `hrm_contracts` có thể lỗi *Class not found* khi mở bên ERP (như màn Đề nghị thu/chi tiền).
- DB gần như không có phiếu ở trạng thái *Đang tạo* (1 phiếu) và *Chờ duyệt* (49 phiếu) → cần seeder dữ liệu test.

## Số liệu nền (DB `gop_db`, 2026-08-17)

10.172 phiếu · loại KH 10.165 · loại NCC 7 · gắn Phiếu báo có 9.504 (93%) ·
trạng thái: Đã duyệt phiếu kế toán 9.998 · Chờ tạo phiếu kế toán 49 · Từ chối 124 · Đang tạo 1.
Dòng "điều chỉnh đến" 13.322 — gắn `FirmContract` 11.037 (83%).

## Kết quả triển khai (2026-08-17) — CODE DONE 5/5 phase

| Lớp | Sản phẩm |
| --- | --- |
| BE | **17 file mới** + 4 file sửa · **20 route** · 4 quyền id 1169–1172 · 2 seeder (quyền + dữ liệu test) |
| FE | **10 file mới** + 1 file sửa (menu) · danh sách 2 chế độ · form + bảng 2 cấp · 3 popup · chi tiết · màn in |
| DB | **0 bảng mới** — dùng bảng log chung `catalog_histories` thay vì tạo bảng lịch sử riêng |

**Thay đổi so với quyết định ban đầu (đều theo hướng ít đụng DB hơn):**
1. Quyết định #10 đổi: **không thêm 2 bảng lịch sử**, dùng bảng chung `catalog_histories` + trait `LogsCatalogHistory` (skill entity-history §5.1) ⇒ feature không thêm bảng nào, FE dùng lại được popup + khối lịch sử có sẵn.
2. Quyết định #8 đổi: **không render mẫu HTML ERP id 209**. Mẫu đó viết cho trang in Blade, không dùng lại được trong màn in Vue; bố cục vẫn bám mẫu ERP nhưng FE tự dựng khung theo dữ liệu BE (khuôn 2 màn Tài chính trước).
3. morphMap **không phải sửa gì** — `FinanceServiceProvider` đã đăng ký sẵn đủ 10 class ERP mà màn này cần.
4. 5 popup gộp còn **3** (KH/NCC chung 1 component, HĐ bán/mua chung 1 component).

**Đã chứng minh bằng số liệu thật:** phạm vi quyền 4 mức khớp SQL tuyệt đối (10.171 / 1.078 / 101 / 72 / pending 40) · công nợ 50 hợp đồng lệch 0 so với công thức ERP · vòng đời ghi 34/34 ca · 5 ca chéo tài khoản chặn đúng · in + Excel 22/22 ca · FE 10/10 file compile sạch.

**Sửa 4 lỗi/lỗ hổng của ERP:** `canEdit()`/`canDelete()` sai thứ tự toán tử (phiếu *Đang tạo* ai cũng sửa/xoá được) · `changeStatus()` gán thẳng trạng thái từ request (nhảy cóc được) · màn chờ duyệt không lọc trạng thái (hiện cả 9.998 phiếu đã xong) · từ chối không lưu người từ chối và không báo lại người lập.

**Còn lại (không chặn):** toàn bộ FE chưa mở trình duyệt — cần user bấm tay, dữ liệu sẵn 6 phiếu `TEST.DNDCCN.*`.
