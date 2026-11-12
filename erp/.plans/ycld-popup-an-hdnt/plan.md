# #11469 YC lắp đặt bàn giao — popup HĐ không hiện HĐNT

## Hiện trạng
- Popup chọn HĐ (`searchAllContract`, type=assembly_request) → `SearchContractService` cho HĐ hãng có hiệu lực, type [1,4,7,8] → lọt HĐNT (7).
- ĐHNT không load hàng: hàng chỉ lên khi dòng HĐ need_repair=1 (copy từ YCXH "Có lắp đặt" lúc xuất). Kiểm local ĐHNT 22303 có lắp đặt → ra đủ SL. Phiếu test trên dev không có ở DB local → nghi YCXH chọn "Không lắp đặt", ghi chú Redmine.

## Tasks
- [x] T1 Ẩn HĐNT khi có cờ exclude_principle_contract (chỉ màn YCLD gửi; YC công việc khác dùng chung giữ nguyên)
- [x] T2 php -l + gọi service xác nhận không còn type 7
- [x] T3 Commit, push develop_02 + gop_db, Redmine → Code xong chờ test kèm ghi chú phần ĐHNT
