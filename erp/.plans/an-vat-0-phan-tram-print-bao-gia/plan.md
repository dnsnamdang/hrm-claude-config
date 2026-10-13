# Ẩn "(0%)" nhãn Thuế VAT — Print báo giá tổng hợp firm-quotation

> Loại: bugfix nhỏ. File: `app/Services/PrintTemplate/FirmQuotationPrint.php`

## Bối cảnh
Print báo giá tổng hợp (route `firmQuotation.printSynthe`, template_type=2, template_id=131) hiện nhãn **"Thuế VAT (0%)"** dù tiền VAT > 0 (vd HĐ 49596: `tab.vat_percent=0.00` nhưng `vat_cost=7,280,000` = 8%). Toàn DB `firm_quotation_tabs.vat_percent` luôn = 0 (VAT áp ở cấp sản phẩm, không lưu ở tab) → nhãn "(x%)" ở bảng SP luôn ra "(0%)". User: ẩn phần "(...%)" khi không có % thật.

## Task
- [x] Sửa 2 chỗ trong `FirmQuotationPrint.php` (method `getProductTableExtraContentByGroup2Attribute` cho template_type=2):
  - Dòng ~1546 (nhãn tổng hợp `$vat_label`): chỉ hiện "(x%)" khi `count($vat_percents)===1 && (float)$vat_percents[0] > 0`, ngược lại chỉ "Thuế VAT".
  - Dòng ~1804 (`getTableProductTab`, dòng VAT bảng SP): `'Thuế VAT'.(floatval($tab->vat_percent) > 0 ? ' ('.truncate_number($tab->vat_percent).'%)' : '')`.
- [x] Verify (tinker, erp_new): render `getProductTableExtraContentByGroup2Attribute(49596)` → cả 2 nhãn ra **"Thuế VAT"**, KHÔNG còn "(0%)". `php -l` sạch. Không có tab `vat_percent>0` trong DB → không có case dương nào bị phá; nhãn tổng hợp case dương giữ nguyên nhờ điều kiện `> 0`.
- [ ] Commit (chỉ khi user yêu cầu).

### Checkpoint — 2026-07-21
Vừa hoàn thành: ẩn "(0%)" ở 2 nhãn Thuế VAT (bảng SP + tổng hợp) khi % ≤ 0.
Đang làm dở: (không) — sửa 2 chỗ, chưa commit.
Bước tiếp theo: user duyệt + commit; kiểm lại trên trình duyệt link print-synthe.
Blocked:
