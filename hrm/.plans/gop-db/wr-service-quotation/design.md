# Cụm CCTT + Báo giá dịch vụ — Kết quả KHẢO SÁT (chưa code)

> @namdangit · nhánh `gop_db` · khảo sát 2026-08-21
> User chốt: khảo sát CẢ CỤM trước rồi mới code (vì 2 màn dùng chung một bảng).

## 1. Vì sao gộp thành 1 cụm
`wr_service_quotations` là **một bảng duy nhất** phục vụ nhiều màn, phân biệt bằng cột `type`:

| `type` | Màn | Số bản ghi |
| --- | --- | --- |
| 0 | **Phiếu cung cấp thông tin làm báo giá** (chứng từ 3) | 4.979 |
| 1 | **Báo giá dịch vụ** (chứng từ 4) | 5.170 |

Cột `has_warranty` / `status_warranty` còn tách tiếp ra màn **Phiếu bảo hành**. Ngoài ra 4 màn khác
cũng đọc bảng này: Hợp đồng, Phụ lục hợp đồng, Phụ lục bổ sung, Phiếu bảo hành → **tổng 6 màn ERP
dùng chung 1 bảng**. Thiết kế lệch nhau ở 2 màn đầu sẽ kéo theo sửa lại toàn cụm.

## 2. Quy mô — lớn hơn hẳn 2 chứng từ đã port

| Hạng mục | Chứng từ 1 | Chứng từ 2 | **Cụm 3 + 4** |
| --- | --- | --- | --- |
| Controller ERP | ~450 dòng | 480 dòng | **688 + 883 dòng** |
| Model ERP | ~500 dòng | 484 dòng | **1.554 dòng (dùng chung)** |
| Giao diện ERP | ~700 dòng | ~800 dòng | **5.206 + 3.079 dòng** |
| Bảng dữ liệu | 2 | 3 | **12** (1 chính + 11 con) |
| Trạng thái | 9 | 6 | **9 phiếu + 4 báo giá + 2 bảo hành** |
| Quyền | 4 | 4 | **8** (4 mỗi màn) |

Bảng con và số dòng thật: `products` 13.715 · `costs` 50.935 · `extend_products` 3.488 ·
`extend_product_services` 15.233 · `product_device_errors` 13.785 · `product_items` 6.979 ·
`product_services` 3.823 · `merchandises` 1.535 · 3 bảng nối lỗi thiết bị (2 bảng đang rỗng).
Cấu trúc lồng **3 cấp**: thiết bị → dịch vụ của thiết bị → vật tư của dịch vụ.

## 3. Cấu trúc form (2 màn gần giống nhau)
```
Thông tin khách hàng
A - BẢO HÀNH THIẾT BỊ
B - DỊCH VỤ KIỂM TRA, SỬA CHỮA, BẢO DƯỠNG
     I  Dịch vụ kiểm tra, sửa chữa
     II Danh mục thiết bị cần bảo dưỡng
C - CHI PHÍ KHÁC          (Các khoản chi phí liên quan · Chi phí vận chuyển)
D - TỔNG HỢP BÁO GIÁ      (Bảo hành · Sửa chữa - Bảo dưỡng · Tổng hợp)
Điều khoản báo giá · Ghi chú duyệt
```
Màn Báo giá có thêm khối **C - LOẠI HÀNG HÓA** (`merchandises`). Hai màn **dùng chung** khối nhập
chi tiết `WRInformation.blade.php` (1.519 dòng) — bên báo giá include thẳng file của bên CCTT.

## 4. ⚠️ Rủi ro lớn nhất: TOÀN BỘ TÍNH TIỀN NẰM Ở GIAO DIỆN
ERP không tính tiền ở máy chủ. Các công thức viết bằng class JavaScript đặt trong 6 file
`ProductInformation*.blade.php` (**1.684 dòng**), dạng:

```js
get total_price()          { return this.amount_after_extra - this.discount }
get vat_cost()             { return this.total_price * (this.vat_percent || 0) / 100 }
get total_price_after_vat(){ return this.vat_cost + this.total_price }
get vat_cost_allocated()   { ... }   // phân bổ chi phí cho từng dòng
```

Bảng chính chỉ lưu 4 cột tiền tổng (`vat_percent`, `vat_cost`, `total_before_vat`,
`total_after_vat`); mọi số trung gian do giao diện tính rồi gửi lên. Đây là **khác biệt căn bản với
2 chứng từ trước** (không có tiền) và là chỗ dễ sai nhất: lệch một công thức là sai tiền báo giá cho
khách. Port sang HRM cần đối chiếu số học trên dữ liệu thật, không chỉ so giao diện.

## 5. Luồng nghiệp vụ (đã đọc `store()` của chứng từ 3)
- Lập từ Phiếu xử lý yêu cầu (`?warranty_repair_handle_request_id=`), chặn bằng
  `canCreateRepairInformation()` — chính là điều kiện HRM đã có ở chứng từ 2.
- **Lưu nháp** (`Đang tạo`) → phiếu xử lý chuyển "Đang CCTT", phiếu yêu cầu gốc cũng chuyển "Đang CCTT".
- **Gửi đi** (`Chờ làm báo giá`) → phiếu xử lý chuyển "Đã CCTT" + đóng dấu người/ngày xử lý; phiếu
  yêu cầu gốc chuyển "Đã CCTT báo giá"; nếu là hàng bảo hành thì đánh dấu trạng thái bảo hành.
- **Thông báo**: báo cho **người tạo Phiếu yêu cầu** (không phải theo quyền như chứng từ 2), nội
  dung "Bạn có phiếu cung cấp thông tin cần làm báo giá từ <người gửi>", chỉ bắn khi phiếu CÓ dòng
  dịch vụ hoặc thiết bị bảo dưỡng.
- Có thêm thao tác **Không duyệt** (`unApprove`) ở chứng từ 3.

## 6. Quyền (copy nguyên văn ERP)
Chứng từ 3: `Xem phiếu cung cấp thông tin theo tổng công ty / công ty / phòng ban` +
`Tạo phiếu cung cấp thông tin` (HRM **đã tạo** quyền này ở chứng từ 2, id 1514 — dùng lại).
Chứng từ 4: `Xem báo giá dịch vụ SC - BH theo tổng công ty / công ty / phòng ban` +
`Tạo báo giá dịch vụ SC - BH`.

## 7. Đề xuất cách làm
1. **Tầng dữ liệu dùng chung trước**: 1 Entity `WrServiceQuotation` + 11 entity con + 1 service lo
   phần đọc/ghi chung (scope quyền, sync bảng con nhiều cấp), tách rõ nhánh theo `type`.
2. **Chứng từ 3 hoàn chỉnh** (BE + FE + test) → bàn giao.
3. **Chứng từ 4** kế thừa tầng chung, chỉ thêm phần riêng (khối Loại hàng hóa, trạng thái báo giá,
   sao chép báo giá, hết hiệu lực).
4. Phần tính tiền: viết thành **một module tính toán dùng chung** ở FE, có bộ đối chiếu số học với
   dữ liệu ERP thật trước khi cho chạy.

## 8. Quyết định đã chốt (user chốt 2026-08-21)

| Vấn đề | Chốt |
| --- | --- |
| **Phạm vi đợt này** | **CHỈ chứng từ 3** (Phiếu cung cấp thông tin làm báo giá). Dựng tầng dùng chung + làm trọn màn CCTT rồi bàn giao. Chứng từ 4 (Báo giá dịch vụ) để đợt sau, kế thừa tầng chung. |
| **Tính tiền** | **Giữ ở giao diện như ERP** — port nguyên công thức sang MỘT module JS dùng chung (`utils/wrServiceQuotationMoney.js`), không rải công thức trong từng component. Máy chủ vẫn chỉ lưu 4 cột tiền tổng như ERP. Bắt buộc có bộ đối chiếu số học với dữ liệu ERP thật trước khi báo xong. |
| **Khối Phiếu bảo hành** | **Giữ dữ liệu, chưa làm màn.** Các cột `has_warranty` / `status_warranty` và khối "A - Bảo hành thiết bị" vẫn lưu/đọc đúng như ERP để dữ liệu lập ở HRM không thiếu so với ERP, nhưng KHÔNG dựng màn Phiếu bảo hành riêng trong đợt này. |

Hệ quả cho thiết kế:
- Entity + service phải tách sẵn nhánh theo `type` ngay từ đầu (đừng hard-code `type = 0`), để chứng
  từ 4 dùng lại không phải sửa lại tầng chung.
- Module tính tiền là **tài sản chung của cả cụm** — đặt ở `utils/`, không đặt trong thư mục màn CCTT.
- Ghi/đọc đủ cột bảo hành ngay từ đợt này; thiếu thì sau này phải chạy lại dữ liệu.

## 9. Khác biệt CỐ Ý so với ERP (chứng từ 3)

| # | ERP làm gì | HRM làm gì | Vì sao |
| --- | --- | --- | --- |
| 1 | Thiết bị mang **nhiều lỗi** được tách thành nhiều dòng, nhưng ERP đọc nhầm khoá (`services` thay vì `service`) nên **các dòng tách ra mất sạch dịch vụ** | Dòng tách ra giữ đúng dịch vụ của lỗi đó | Đây là lỗi gõ nhầm chứ không phải nghiệp vụ (dòng chỉ có 1 lỗi vẫn đủ dịch vụ). Hậu quả ở ERP là **thiếu tiền dịch vụ** trong báo giá gửi khách. |
| 2 | Cột **Giá vốn** hiện cho mọi người mở được form | Ẩn hẳn nếu không có quyền `Xem giá vốn hàng hoá`; máy chủ trả `null` thay vì số | Quy tắc fail-closed của CLAUDE.md. Lưu ý: người không có quyền vẫn **lưu được phiếu mà không xoá mất giá vốn** — máy chủ khôi phục giá vốn cũ theo id dòng. |
| 3 | Phiếu **nháp của người khác**: danh sách ẩn nhưng mở link trực tiếp thì Super admin vẫn đọc được | Không ai đọc được, kể cả Super admin và cả đường IN | Đã chốt ở chứng từ 2 (2026-08-20), áp lại cho cả luồng. |
| 4 | 4 cột tiền tổng của phiếu CCTT luôn để **0** (kiểm 4.979 bản ghi thật) | Ghi số thật (`vat_cost`, `total_before_vat`, `total_after_vat`) | Không ảnh hưởng ERP đọc ngược (ERP không dùng 4 cột này ở chứng từ 3), nhưng báo cáo HRM đọc được ngay. |
| 5 | Bắt buộc **mọi trường** ở cả nút Lưu nháp lẫn Gửi đi | Lưu nháp chỉ cần phiếu xử lý gốc + khách hàng | Đồng nhất với 2 chứng từ trước (skill `form-validate`). |
| 6 | Lấy `pluck` cả mảng id rồi `whereIn` khi lọc theo tên hàng hoá / dịch vụ | Dùng `EXISTS` | Bảng dòng thiết bị 13.715 dòng, dịch vụ 50.935 dòng trên DB gộp. |

## 10. Nơi đặt CÔNG THỨC TIỀN (2 bản, phải sửa cùng nhau)

| Lớp | File | Dùng khi nào |
| --- | --- | --- |
| Giao diện | `hrm-client/utils/wrServiceQuotationMoney.js` | Mọi con số hiện trên form và khối "D - Tổng hợp báo giá" |
| Máy chủ | `Modules/CustomerCare/Services/WrServiceQuotationPrintService` (`summaryCost` / `warrantyTotals` / `repairMaintainTotals` / `grandTotal`) | Bản in |

Đã đối chiếu số học **39 phiếu thật** (có sửa chữa / có bảo dưỡng / có bảo hành): 5 chỉ tiêu
(`amount`, `discount`, `before_vat`, `vat_cost`, `after_vat`) **khớp tuyệt đối, 0 phiếu lệch**.


## 11. Chữ trên nút và trong thông báo (chốt 2026-08-21)

| Chỗ | Dùng gì | Vì sao |
| --- | --- | --- |
| Nút gửi phiếu ở `V2Footer` | `send_and_submit_form` → **"Lưu và gửi"**, popup *"Bạn đồng ý lưu và gửi?"* | Phiếu được GỬI cho người lập Phiếu yêu cầu để họ làm báo giá — **không có ai duyệt nó**. `V2Footer` đã có sẵn nút này, KHÔNG phải thêm tham số cho component dùng chung (`save_and_submit_approve` mới là "Lưu và gửi duyệt"). |
| Nhóm hành động của thông báo | **`Chờ duyệt`** | `.claude/skills/notification-convention/SKILL.md` mục 2 chỉ cho dùng **đúng 14 nhóm cố định**, không có nhóm nào nghĩa "chờ làm tiếp". `Chờ duyệt` là nhóm sát nghĩa nhất (chờ người nhận hành động) và cũng là nhóm 2 chứng từ trước đang dùng. Muốn đổi thì phải sửa bảng 14 nhóm trong skill — là tài sản chung, cần PR riêng. |

✅ **Chứng từ 2 (Phiếu xử lý yêu cầu) đã đổi theo cùng chuẩn** (user chốt 2026-08-21): nút và popup
xác nhận nay là "Lưu và gửi", `testcase.xlsx` (87 TC) + `Mô tả nghiệp vụ` đã sinh lại theo chữ mới.

✅ **Chứng từ 1 (Yêu cầu kiểm tra sửa chữa – bảo hành) cũng đã đổi** (user chốt 2026-08-21):
`testcase.xlsx` (97 TC) + `Mô tả nghiệp vụ` đã sinh lại theo chữ mới.

➡️ **Cả 3 chứng từ của luồng dịch vụ nay dùng chung nút "Lưu và gửi".** Các phân hệ khác (Đào tạo,
Tài chính…) vẫn dùng "Lưu và gửi duyệt" — đúng nghiệp vụ của họ (có người duyệt thật), KHÔNG đổi.
