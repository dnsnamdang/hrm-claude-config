# Fix — Cùng 1 khách hàng có 2 người liên hệ trùng số điện thoại

Người phụ trách: @junfoke · Repo: `hrm-cursor/TanPhatDev` (bản B) · Nhánh: `master`
Màn báo lỗi: `/admin/customers/34/manager` (Quản lý khách hàng) — KH 29TPHPTH-1 ETEK GREEN có
"Mr Chương" và "Nguyễn Minh A" cùng SĐT 0123456789.

## Nguyên nhân (đã tái hiện trên bản B local)
Trùng KHÔNG đến từ nút "Thêm mới" — endpoint `customerAddContact` có rule `uniqueContactPhoneFast`
(test lại: trả "Đã tồn tại"). Lọt ở chức năng **Sửa người liên hệ ngay trên màn Quản lý khách hàng**:
`CustomersController@submitEditContact` (route `customer.submitEditContact`) chỉ validate
`required` cho fullname/role/phones — không kiểm tra trùng SĐT, nên đổi SĐT của 1 người liên hệ
thành SĐT của người khác trong cùng KH là lưu thành công.
Phụ: modal sửa ở `customermanager/show_.blade.php` bind lỗi sai key (`errorsContact['used_place']`)
⇒ kể cả khi BE trả lỗi `phones` thì cũng không hiện chữ đỏ nào.

## Task
- [x] Trace: so 3 đường ghi người liên hệ (`customerUpdate` – rule `uniqueContactPhone`;
      `customerAddContact` – `uniqueContactPhoneFast`; `submitEditContact` – KHÔNG có gì)
- [x] BE `submitEditContact`: lấy contact trước, validate `phones` bằng closure — tách theo dấu phẩy,
      chặn trùng trong cùng ô nhập và trùng với người liên hệ khác của CÙNG khách hàng
      (loại chính bản ghi đang sửa), chuẩn hoá lại chuỗi phones khi lưu
- [x] FE modal sửa liên hệ: đổi `errorsContact['used_place']` → `errorsContact['phones']`
- [x] BE `submitEditContact`: ghi lịch sử khách hàng như `updateContact` (CustomerVersion +
      createHistoryRecord bảng `customer_contacts`, chỉ ghi khi dữ liệu thực sự đổi)
- [x] Verify Playwright trên bản B local (:8001), KH 34

## Kết quả verify
| Ca | Trước fix | Sau fix |
| --- | --- | --- |
| Đổi SĐT liên hệ B thành SĐT của liên hệ A (cùng KH) | Lưu thành công ⇒ trùng | Chặn: "Số điện thoại 0123456789 đã tồn tại ở người liên hệ khác của khách hàng này" |
| Lưu lại chính SĐT của mình | — | Vẫn cho lưu (không tự chặn chính nó) |
| Ô nhập nhiều số, 1 số trùng người khác | Lưu được | Chặn |
| Ô nhập 2 số giống nhau | Lưu được | Chặn: "Số điện thoại bị nhập trùng nhau" |
| Hiển thị lỗi trên modal | Không hiện gì | Chữ đỏ dưới ô Điện thoại, modal không đóng |
| Sửa liên hệ (đổi chức vụ + thêm số) | Không để lại vết | Sinh `customer_histories` #82071 "Người liên hệ": giá trị cũ `PGD / 0123456798` → mới `PGD TEST LS / 0123456798, 0911000111`, đúng người sửa; màn `/customers/34/history` hiển thị đúng |

## Còn tồn (chưa làm, cần ý kiến)
- `submitEditContact` KHÔNG kiểm tra quyền `canEditContact()` như `updateContact` — ai vào được màn
  QLKH cũng sửa được người liên hệ. Chưa đụng vào vì ngoài phạm vi bug, cần user chốt.
- Dữ liệu ĐÃ trùng sẵn trên dev/production cần rà + dọn tay (fix chỉ chặn từ nay).
- `addContact` đang chặn khách cá nhân bằng `$customer->type == 1` trong khi cột thật là
  `customer_type` ⇒ điều kiện này không bao giờ đúng.

### Checkpoint — 2026-09-18
Vừa hoàn thành: fix BE + FE + ghi lịch sử khi sửa liên hệ, verify local xong (đã trả dữ liệu test về nguyên trạng).
Bước tiếp theo: user review + commit; quyết định 3 mục "Còn tồn".
