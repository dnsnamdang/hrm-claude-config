# Khuôn chuẩn TESTCASE (user chốt 03/11/2026)

Chuẩn chung = tab **"13. DM quốc gia"** trong file Drive "Testcase chuyển đổi" (bản sao: `mau/TC chuan - 13. DM quoc gia.xlsx`)
+ checklist **`mau/Mau tai lieu - checklist TC + SRS.xlsx`** tab "Testcase" (299 case cần kiểm tra, theo Nhóm → Phân nhóm).

Lý do làm lại: 19 tab sinh ngày 02/11 bám skill `testcase-documenter` (nhóm "Phân quyền & truy cập" + mã `TC-ROLE` ĐẦU tab, nhóm
gộp "TẠO / SỬA / XEM", "RÀNG BUỘC NHẬP LIỆU", "E2E FLOW", thiếu dòng 16) → lệch tab Quốc gia và thiếu nhiều case của checklist.

> Từ 03/11/2026 khuôn này đã ĐÓNG GÓI vào skill `testcase-documenter` (assets `tc_chuan.py`, `check_tc.py`, `TC_MAU_QUOC_GIA.xlsx`,
> `CHECKLIST_TC_SRS.xlsx`) — SKILL.md là nguồn chuẩn; file này giữ lại làm ghi chép đợt làm lại.

## Cách sinh — BẮT BUỘC dùng `_tc_chuan.py` (không gọi `tc_engine.build` trực tiếp)
```python
sys.path.insert(0, r'<...>\xuat-tai-lieu-chuyen-doi')
from _tc_chuan import build_chuan
build_chuan(OUT, SHEET, FEATURE, MODULE, DESCRIPTION_BLOCK, SECTIONS, loai='danh_muc' | 'phieu' | 'bao_cao')
```
Tự kiểm sau khi sinh (cũng được build_chuan gọi): `python check_tc.py <file.xlsx> <loai>` → phải **0 lỗi**.

## Bố cục (giống tab Quốc gia)
- Dòng 1–10: khối "MÔ TẢ TÍNH NĂNG" 9 mục (giữ như bản cũ, sửa nếu sai). Dòng 11–16 TEST SUMMARY (dòng 16 "Tổng số testcase").
- Dòng 17: 17 cột chuẩn. Dòng 18+: tiêu đề nhóm (`I. HIỂN THỊ TRANG & TRUY CẬP`) rồi các case.
- Mã case `TC_<số nhóm 2 chữ số>.<3 chữ số>`; nhóm đánh La Mã LIÊN TỤC (I, II, III…). Không còn `TC-ROLE`.
- Cột Module + Nhóm chức năng chỉ ghi ở case đầu mỗi nhóm. KQ thực tế, DNS check 1-3, TP check: ĐỂ TRỐNG.

## Thứ tự nhóm (bỏ nhóm màn không có; nhóm có mặt phải đúng thứ tự)
| Loại | Thứ tự nhóm |
|---|---|
| danh_muc | HIỂN THỊ TRANG & TRUY CẬP · TÌM KIẾM & LỌC DANH SÁCH · THÊM MỚI · CHỈNH SỬA · XÓA · KHÓA / MỞ KHÓA · LỊCH SỬ THAY ĐỔI · XEM CHI TIẾT <ĐỐI TƯỢNG> · TÙY CHỈNH CỘT · XUẤT DANH SÁCH EXCEL · IMPORT TỪ FILE EXCEL · RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC · PHÂN QUYỀN |
| phieu | HIỂN THỊ TRANG & TRUY CẬP · TÌM KIẾM & LỌC DANH SÁCH · THÊM MỚI · CHỈNH SỬA · XÓA · KHÓA / MỞ KHÓA · GỬI DUYỆT · DUYỆT PHIẾU · KHÔNG DUYỆT PHIẾU · HỦY PHIẾU · LỊCH SỬ THAY ĐỔI · XEM CHI TIẾT <PHIẾU> · IN PHIẾU · TÙY CHỈNH CỘT · XUẤT DANH SÁCH EXCEL · IMPORT TỪ FILE EXCEL · RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC · PHÂN QUYỀN |
| bao_cao | HIỂN THỊ TRANG & TRUY CẬP · TÌM KIẾM & LỌC DANH SÁCH · SỐ LIỆU BÁO CÁO · XEM CHI TIẾT <…> (popup) · TÙY CHỈNH CỘT · XUẤT DANH SÁCH EXCEL · IN BÁO CÁO · RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC · PHÂN QUYỀN |

Gợi ý đặt case vào nhóm:
- HIỂN THỊ: mở từ menu, tiêu đề, nút, cột mặc định hiện/ẩn, trạng thái, rỗng / không khớp lọc, **phân trang** (số dòng mặc định, đổi số
  dòng, trước/sau, đầu/cuối, trạng thái nút, STT liên tục, tổng số, về trang 1) và **sắp xếp** (mặc định, tăng, giảm, ngày tạo/cập nhật,
  cột không sắp xếp, giữ khi chuyển trang, về trang 1), hiệu năng tải.
- TÌM KIẾM & LỌC: từ khóa chính xác/một phần/hoa-thường/có dấu/không tồn tại/ký tự đặc biệt/khoảng trắng/giới hạn/xóa/Enter; từng ô
  lọc, kết hợp, mặc định, tổng & phân trang sau lọc, Làm mới; **lưu trạng thái** (chuyển màn quay lại, F5, tab mới, tài khoản khác).
- THÊM MỚI: giao diện, bắt buộc/mặc định, thành công (đủ / chỉ bắt buộc), lịch sử tạo, validate từng trường (trống, định dạng, ký tự,
  độ dài đúng max / vượt max, trùng, khoảng trắng, chỉ khoảng trắng, lỗi biến mất), Lưu và tiếp tục / Lưu nháp / Lưu và gửi duyệt (nếu
  có), Đóng/X/Thoát/Ở lại/nhập rồi xóa hết, bấm Lưu liên tục, tạo trùng đồng thời 2 tab.
- CHỈNH SỬA: fill đúng, trường sửa/không sửa được, sửa 1/nhiều trường, giữ nguyên của chính mình, trùng bản ghi khác, ngày/người cập
  nhật, lịch sử sửa, không đổi → không ghi lịch sử, hủy sửa, bản ghi khóa / bị xóa / 2 người sửa.
- Phiếu: tác động số liệu sau Lưu/Duyệt (tồn, công nợ, hàng giữ, bút toán) đặt TRONG nhóm thao tác gây ra nó (DUYỆT PHIẾU, THÊM MỚI…);
  luồng nhiều màn → nhóm RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC.
- Báo cáo: mỗi cột/chỉ tiêu, dòng tổng, định dạng số, "lập chứng từ rồi kiểm số tăng/giảm" → SỐ LIỆU BÁO CÁO (luồng chứng từ màn khác
  → RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC).
- PHÂN QUYỀN (cuối): xem DS / chi tiết / thêm / sửa / xóa / khóa / import-export / lịch sử theo quyền, ẨN nút khi thiếu quyền, URL trực
  tiếp khi thiếu quyền, đổi quyền giữa thao tác, **phạm vi dữ liệu** theo quyền. KHÔNG viết case "gọi thẳng API/Postman".

## Câu chữ (bắt chước tab Quốc gia)
- Chức năng: cụm ngắn kiểu "Mở màn hình từ menu", "Thiếu Tên quốc gia thì bị chặn", "Bấm Hủy thì không xóa".
- Tiền điều kiện: 1 câu thường. Bước: "1. …\n2. …". Test data: dữ liệu cụ thể (hoặc trống). Expected: mỗi ý 1 dòng bắt đầu "-  ",
  câu/nhãn/thông báo NGUYÊN VĂN theo code.
- Không thuật ngữ code, không emoji, không chữ ERP / API.

## Độ phủ
Mỗi dòng checklist ÁP DỤNG ĐƯỢC cho màn phải có ≥ 1 case (không áp dụng → bỏ, ghi vào báo cáo cuối "checklist bỏ: …"). Giữ lại
mọi case NGHIỆP VỤ riêng của màn ở bản cũ (đưa vào đúng nhóm), không làm mất nội dung đã viết.
