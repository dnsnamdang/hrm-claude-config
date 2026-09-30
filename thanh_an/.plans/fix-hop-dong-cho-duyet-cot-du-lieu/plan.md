# Fix màn Hợp đồng chờ duyệt — cột không lấy được dữ liệu

**Phụ trách:** @khoipv
**Ngày:** 22/09/2026
**File:** `hrm-thanhan-client/pages/contract/contract/approve.vue` (FE only — BE không sửa)

## Bối cảnh

Màn `/contract/contract/approve` (Hợp đồng chờ duyệt) trên nhánh `master` đang đọc các
field mà API `GET category/contracts?request_type=wait-approve` không trả về:

| Cột | master đang dùng (sai) | field API thực tế |
|---|---|---|
| Công ty | `item.main_company_name` | `main_company_code` |
| Giá trị hợp đồng | `item.total_after_vat` | `total_amount` |
| Thời gian hợp đồng | `item.contract_time` | `contract_sign_time` + `contract_end_time` |

Bản fix đã có sẵn trên nhánh `thanhan-dev`. Yêu cầu: port sang `master` **không được
gây conflict** khi sau này merge `thanhan-dev` → `master`.

## Quyết định

- **Đồng bộ nguyên file** `approve.vue` cho 2 nhánh giống hệt nhau (byte-identical)
  → merge sau này file này không có gì để gộp → sạch tuyệt đối.
- Bổ sung cột mới **Mảng hàng hóa** (field `array_product_names`, API đã trả sẵn),
  đặt **sau cột Gói thầu**. Vì là cột mới không có trên `thanhan-dev` nên phải thêm
  **trên cả 2 nhánh** để giữ nguyên tắc byte-identical.
- BE `ContractResource.php` trên master đã trả đủ field → **không sửa BE**.

## Task

- [x] Dựng nội dung file đích = bản `thanhan-dev` + cột Mảng hàng hóa (sau Gói thầu)
- [x] Áp lên nhánh `master` (chưa commit — user tự commit)
- [x] Verify số cột header/body khớp nhau (13/13)
- [x] Verify merge 3 chiều bằng `git merge-file` → **2 vùng conflict** (xem bên dưới)
- [ ] (tuỳ chọn) Áp cột Mảng hàng hóa lên `thanhan-dev` để merge sạch tuyệt đối
- [ ] User tự commit (AI không commit/push)

## Kết quả kiểm chứng merge

Hướng merge thực tế user chọn: **master → thanhan-dev**.

Chạy `git merge-file` với base = `9d513470` (merge-base master/thanhan-dev):

- 3 cột lỗi (`main_company_code`, `total_amount`, `contract_sign_time`/`contract_end_time`)
  → **merge sạch**, vì 2 nhánh sửa giống hệt nhau từng ký tự.
- Cột **Mảng hàng hóa** → **2 vùng conflict** (1 ở `<b-th>`, 1 ở `<b-td>`), do dòng mới
  chèn sát ngay dòng mà `thanhan-dev` cũng sửa (`Gói thầu` → `Gói thầu/ BG`).
  Cả 2 conflict đều dạng "dev trống / master thêm 1 dòng" → xử lý = giữ phía master.

Muốn 0 conflict tuyệt đối: thêm cột Mảng hàng hóa lên `thanhan-dev` trước khi merge.

## Checkpoint

_(cập nhật khi wrap up)_
