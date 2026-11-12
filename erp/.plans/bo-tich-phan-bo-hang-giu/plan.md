# #12041 — PNK luồng mua: cho phép bỏ tích "Cần giữ" ở tab Phân bổ hàng giữ

Redmine: http://quanly.dnsmedia.vn/issues/12041
Áp dụng: PNK mua ngoài nước mới (type 11), mua trong nước tự do/hãng (15, 2) — tạo + sửa.

## Hiện trạng
- Ô tích "Cần giữ" (header + từng dòng) bị `disabled` cứng → luôn giữ.
- BE đã tôn trọng `customers.*.allocation`: =0 thì không prepick → hàng về tồn kho. Hạn giữ đã `ng-disabled="!d.allocation"`, submit gửi null khi bỏ tích. → KHÔNG sửa BE.
- Bug: setter `allocation_all` (ProductImport.blade.php) chỉ set mức khách hàng cho type 11; 15/2/16 rơi vào set `product.allocation` (getter lại đọc mức khách) → tích header không tác dụng.

## Tasks
- [x] form.blade.php: bỏ `disabled` ô tích header + dòng ở 3 pane (11/15/2), gắn ng-change hỏi xác nhận; id checkbox duy nhất
- [x] formJs.blade.php: `onToggleAllocation(d, product)` / `onToggleAllocationAll()` — bỏ tích thì swal "Bạn chắn chắn không phân bổ giữ <tên hàng>?" / "...tất cả mục hàng?"; Không → trả về tích
- [x] ProductImport.blade.php: setter `allocation_all` xử lý mức khách cho 11/15/2/16
- [x] show.blade.php giữ chỉ-đọc
- [x] Test tay tạo loại 15 (ĐNNK 8910, user 13): dòng + header Không/Đồng ý/tích lại đều đúng, submit `{allocation:0, expire:null}`
- Ghi chú (không có dữ liệu thử): chưa thử màn Sửa (canEdit cần status 3 + người lập, không có dữ liệu) và loại 11/2 (cùng markup + setter)

### Checkpoint — 10/11/2026
Vừa hoàn thành: FE 3 file + test tay loại 15
Đang làm dở: —
Bước tiếp theo: chờ user cho commit — gop_db rồi cherry-pick develop_02 (worktree TanPhatDev-12041)
Blocked:

