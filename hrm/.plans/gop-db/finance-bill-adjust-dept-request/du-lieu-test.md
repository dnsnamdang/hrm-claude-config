# Dữ liệu test — Phiếu yêu cầu điều chỉnh công nợ

> Khảo sát ngày 2026-08-17 trên DB `gop_db`, **kiểm qua đúng API mà popup trên màn gọi** (không chỉ
> đọc DB). **Không phải tạo dữ liệu giả** — dữ liệu thật đã đủ cho mọi nhánh.

---

## 1. Tạo phiếu TAY — loại **Khách hàng**

Vào `/finance/bill-adjust-dept-requests/create` → để loại "Điều chỉnh công nợ khách hàng".

Chọn khách hàng rồi chọn hợp đồng; các khách hàng dưới đây **chắc chắn có hợp đồng kèm công nợ**:

| id KH | Tên | Hợp đồng gợi ý | Công nợ |
| --- | --- | --- | --- |
| **43669** | BỘ TƯ LỆNH THỦ ĐÔ HÀ NỘI | `HĐ-TEST-DNTT-12` | 5.929.766.250 |
| **916** | CÔNG TY CỔ PHẦN HYUNDAI PHẠM VĂN ĐỒNG | `HĐ-TEST-DNTT-09` | 1.210.194.000 |
| **36250** | CHI NHÁNH HÀ TĨNH — CTCP SẢN XUẤT… | `HĐ-TEST-DNTT-26` | 611.301.000 |
| **13102** | CÔNG TY TNHH AUTO VŨ GIA | `HĐ-TEST-DNTT-05` | 810.000 |
| **43235** | CTCP KINH DOANH VÀ TM ĐẠI… | `HĐ-TEST-DNTT-28` | 680.400 |

**Gợi ý một phiếu hoàn chỉnh**: điều chỉnh **từ** KH 43669 / `HĐ-TEST-DNTT-12` **đến** KH 916 /
`HĐ-TEST-DNTT-09`, số tiền 1.000.000 (nhớ để tổng 2 bên bằng nhau thì mới Gửi duyệt được).

## 2. Tạo phiếu TAY — loại **Nhà cung cấp**

Đổi loại phiếu sang "Điều chỉnh công nợ nhà cung cấp" (bảng sẽ xoá sạch và đổi cột).

| id NCC | Tên | Ghi chú |
| --- | --- | --- |
| **21015** | CÔNG TY CỔ PHẦN CẢNG NAM ĐÌNH VŨ | **8/10 hợp đồng có số dư dương** — tốt nhất để test |
| **899** | CÔNG TY CỔ PHẦN EMIN VIỆT NAM | 2 hợp đồng số dư dương: `EMIN-210726` (30.812.400), `EMIN-070726.01` (18.565.200) |
| **34** | CTCP GIẢI PHÁP ETEK GREEN | 10 hợp đồng trong popup |

**Test ngoại tệ (bảng 14 cột)**: chọn Tiền tệ = **USD**, nhập Tỷ giá (vd 26.000) → bảng tự tách đôi
mỗi cột tiền và cột số dư thành *(USD)* và *(VNĐ)*.

## 3. Tạo phiếu TỪ PHIẾU BÁO CÓ — 3 nhánh khác nhau

HRM chưa port màn Phiếu báo có nên chưa có nút dẫn sang; **mở thẳng URL** để test:

### 3a. Nhánh KHOÁ loại phiếu (dòng có khách hàng rõ ràng)

```
/finance/bill-adjust-dept-requests/create?bill_income_report_detail_ids=10182,10181
```
→ phiếu `TPV.PBC0726.00024`, 2 dòng: CÔNG TY TNHH Ô TÔ TRUNG ĐÔ **218.293.169** và
CÔNG TY TNHH DỊCH VỤ Ô TÔ CARPLA **2.527.200**.
**Kiểm**: ô Loại phiếu bị khoá + có dòng chú thích; bên "Điều chỉnh từ" chỉ đọc (không bấm chọn được).

### 3b. Nhánh KHÔNG khoá (mọi dòng là "khách không rõ")

```
/finance/bill-adjust-dept-requests/create?bill_income_report_detail_ids=10227,10228,10229
```
→ phiếu `TPE.PBC0726.00078`, 3 dòng: 2.903.526 · 432.000 · 2.943.000 (tổng 6.278.526).
**Kiểm**: Loại phiếu vẫn đổi được.

### 3c. Nhánh NGOẠI TỆ — tự điền tiền tệ + tỷ giá

```
/finance/bill-adjust-dept-requests/create?bill_income_report_detail_ids=7105
```
→ phiếu `TPE.PBC0426.00046`, USD, tỷ giá **26.015**, còn **5.672 USD** (≈147.557.080 VNĐ).
**Kiểm**: đổi loại phiếu sang NCC → ô Tiền tệ tự thành USD và Tỷ giá tự điền 26.015.

> Số tiền nạp vào bảng luôn là **phần còn lại chưa điều chỉnh**, không phải số gốc của dòng.
> Toàn hệ thống có **968 dòng** còn điều chỉnh được (trên tổng 10.199).

## 4. Sửa / Gửi duyệt / Từ chối / In / Excel / Lịch sử

Dùng 6 phiếu seeder có sẵn (`TEST.DNDCCN.00001` → `00006`), gán cho tài khoản `namdangit@gmail.com`:

| Mã | Loại | Trạng thái | Thử được gì |
| --- | --- | --- | --- |
| `TEST.DNDCCN.00001` | KH | Đang tạo | Sửa · Xóa · Gửi duyệt |
| `TEST.DNDCCN.00002` | KH | Chờ duyệt | Từ chối · In · Excel · Lịch sử |
| `TEST.DNDCCN.00003` | KH | Từ chối | Sửa lại · Gửi duyệt lại |
| `TEST.DNDCCN.00004` | NCC | Đang tạo | Nhánh nhà cung cấp |
| `TEST.DNDCCN.00005` | NCC | Chờ duyệt | Bảng 10 cột |
| `TEST.DNDCCN.00006` | NCC **ngoại tệ** | Từ chối | Bảng 14 cột, cột VNĐ song song |

Tạo lại bộ này bất cứ lúc nào (tự dọn bản cũ trước khi tạo):

```bash
php artisan db:seed --class="Modules\Finance\Database\Seeders\BillAdjustDeptRequestTestDataSeeder"
```

## 5. Dọn dữ liệu test khi xong

```sql
-- xoá phiếu seeder + phiếu tự tạo lúc test (mã TPE.DNDCCN0826.*)
DELETE i FROM bill_adjust_dept_request_detail_items i
  JOIN bill_adjust_dept_request_details d ON d.id = i.bill_adjust_dept_request_detail_id
  JOIN bill_adjust_dept_requests r ON r.id = d.bill_adjust_dept_request_id
 WHERE r.code LIKE 'TEST.DNDCCN%' OR r.code LIKE 'TPE.DNDCCN0826%';
DELETE d FROM bill_adjust_dept_request_details d
  JOIN bill_adjust_dept_requests r ON r.id = d.bill_adjust_dept_request_id
 WHERE r.code LIKE 'TEST.DNDCCN%' OR r.code LIKE 'TPE.DNDCCN0826%';
DELETE ch FROM catalog_histories ch
  JOIN bill_adjust_dept_requests r ON r.id = ch.table_id
 WHERE ch.table_name = 'bill_adjust_dept_requests'
   AND (r.code LIKE 'TEST.DNDCCN%' OR r.code LIKE 'TPE.DNDCCN0826%');
DELETE FROM bill_adjust_dept_requests
 WHERE code LIKE 'TEST.DNDCCN%' OR code LIKE 'TPE.DNDCCN0826%';
```

⚠️ Phiếu bạn tự tạo trong lúc test mang mã `TPE.DNDCCN0826.xxxxx` (mã sinh theo công ty + tháng),
lẫn với phiếu thật cùng dạng nếu tháng 08/2026 có phát sinh thật — kiểm `note` trước khi xoá.

---

## Đính chính số liệu đã báo sai trước đó

Trước đây báo *"`hrm_contracts` có 0 dòng trong `account_details` ⇒ công nợ hợp đồng HRM luôn hiện 0"*
— **SAI**. Đo lại: **33/40 hợp đồng HRM có bút toán TK 1311**, tổng ~25,9 tỷ.
Nguyên nhân: truy vấn qua shell làm mất dấu `\` trong `contractable_type` nên `WHERE` không khớp gì.
Khi đếm theo cột này dùng `LIKE '%Assign%Contract%'`.
