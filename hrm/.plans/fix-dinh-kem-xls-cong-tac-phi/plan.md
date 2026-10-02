# Fix: File .xls (HTML-based) bị chặn "Không hợp lệ" khi đính kèm — Phiếu công tác phí

**Owner:** @junfoke
**Module:** Assign — Đề nghị thanh toán công tác (PaymentBusinessRequest)
**Màn:** Công tác phí / Lưu trú / Chi phí đi đường / Hàng hoá / Chi phí khác (tab File đính kèm)

## Bối cảnh / Triệu chứng
- User đính kèm file `Meeting-theo-thi-truong.xls` (7KB) → BE trả lỗi 422, FE hiện "Không hợp lệ" dưới file.
- Yêu cầu nghiệp vụ (dòng 291): cho đính kèm ảnh (png/jpeg/jpg), word, excel, pdf.

## Nguyên nhân gốc
- File `.xls` của user thực chất là **HTML được lưu thành .xls** (mở bằng Excel vẫn OK — kiểu export phổ biến của hệ thống/hoá đơn). Kiểm tra bằng `file`: `HTML document, UTF-8 (with BOM)`, bytes đầu `<html xmlns...>`.
- BE validate bằng luật `mimes` của Laravel — luật này **đoán định dạng theo nội dung thật**, không theo đuôi tên → ruột HTML bị coi là không phải excel → reject, dù rule đã liệt kê `xls`.

## Quyết định (chốt với user 2026-08-22)
- Validate **theo đuôi tên file** thay vì "ngửi" nội dung (bám pattern có sẵn: TimekeeperController dùng `getClientOriginalExtension()`).
- Giữ giới hạn **10MB** như hiện tại (không đổi về 300KB).

## Tasks
- [x] Tạo Rule dùng chung `Modules/Assign/Rules/AllowedFileExtension.php` (xét `getClientOriginalExtension()` theo whitelist)
- [x] `PaymentBusinessRequestCreateApiRequest`: thay `mimes:...` → `new AllowedFileExtension([...])` cho 4 nhóm (stay_reals / tripCosts / itemCosts / otherCosts)
- [x] `PaymentBusinessRequestUpdateApiRequest`: thay tương tự 4 nhóm
- [x] `php -l` sạch 3 file
- [ ] Verify browser: đính kèm lại `Meeting-theo-thi-truong.xls` ở tab Lưu trú → lưu OK, hết "Không hợp lệ"

## Ghi chú
- `MovingNormController.php:258` vẫn dùng `mimes:xls,xlsx` — đó là import Excel để đọc dữ liệu (cần check nội dung thật), KHÔNG đụng.
- Whitelist đuôi: pdf, png, jpg, jpeg, doc, docx, xls, xlsx.

## Checkpoint — 2026-08-22
Vừa hoàn thành: Tạo Rule + sửa 8 chỗ validate (Create/Update × 4 nhóm), lint sạch.
Bước tiếp theo: User verify trên browser với đúng file đã lỗi.
Blocked: (không)
