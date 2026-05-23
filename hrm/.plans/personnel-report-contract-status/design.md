# Personnel Report — Bổ sung cột Hạn HĐLĐ & Trạng thái HĐLĐ

## Mục tiêu

Báo cáo nhân sự (`/human/personnel`) đã có 2 cột "Hạn HĐLĐ" + "Trạng thái HĐLĐ" nhưng logic trạng thái hiện đang map theo workflow duyệt (Đang tạo / Đã duyệt / Có hiệu lực / Hết hiệu lực). Yêu cầu mới: chuyển sang logic dựa trên ngày còn lại đến `end_date`.

## Phạm vi

- **Hạn HĐLĐ** — hiển thị `end_date` (dd/mm/yyyy) của HĐLĐ hiện đang hiệu lực (giữ logic cũ — đã đúng).
- **Trạng thái HĐLĐ** — 4 giá trị:

  | Status         | Text VN           | Điều kiện                                                                    | Màu badge |
  | -------------- | ----------------- | ---------------------------------------------------------------------------- | --------- |
  | `effective`    | Có hiệu lực       | Có HĐLĐ approved + start ≤ today ≤ end (hoặc end null) + còn > 15 ngày        | xanh      |
  | `expiring_soon`| Sắp hết hạn       | Có HĐLĐ approved + còn ≤ 15 ngày đến `end_date` (inclusive, kể cả 0 ngày)     | vàng/cam  |
  | `expired`      | Hết hiệu lực      | Không có HĐLĐ hiệu lực, NHƯNG đã từng có HĐLĐ approved với end_date < today  | đỏ        |
  | `none`         | Chưa có HĐLĐ      | Chưa từng có HĐLĐ approved nào                                               | xám       |

- HĐLĐ vô thời hạn (`end_date = null`) → luôn `effective`, không bao giờ `expiring_soon`.
- Ưu tiên HĐLĐ đang có hiệu lực (logic `currentDecisionLaborContract` đã đúng).
- Mốc 15 ngày tính inclusive: `end_date - today ≤ 15` → `expiring_soon`.

## Hiện trạng code

- BE: `Modules/Human/Entities/EmployeeInfo.php:951-959` — accessor đã có nhưng trả về status int (1-4).
- FE: `pages/human/personnel/index.vue:1021-1048` — map int → text VN cũ.
- Export: `app/ExcelExport/PersonnelExport.php` — chưa có 2 cột này.

## Thay đổi chính

1. **BE accessor** `getLaborContractStatusAttribute()` trả về string trong {`effective`, `expiring_soon`, `expired`, `none`}.
2. **FE** map text + badge class theo bảng trên.
3. **Excel export** bổ sung 2 cột Hạn HĐLĐ + Trạng thái HĐLĐ.
4. **Print page** đồng bộ nếu có.

## Không thuộc phạm vi

- Không thêm filter mới theo trạng thái HĐLĐ (đã có filter end_date_from/to).
- Không sửa logic của module Decision/labor-contract.
- Không gửi notification "sắp hết hạn".
