# Đánh giá từng loại phiếu chờ duyệt trên HRM (từ code đang chạy) — @cuong61n

Ngày 13/11/2026. Khảo sát bằng 4 lượt đọc code `hrm-api` + `hrm-client`, KHÔNG dựa tài liệu cũ. Mục đích: biết mỗi loại phiếu cần hiện trường nào là quan trọng nhất cho người duyệt, và loại nào duyệt nhanh được.

Ký hiệu: **N** = duyệt nhanh 1 bấm được · **N\*** = được nếu có điều kiện · **K** = không (phải nhập thêm / sang màn khác). "Cấp" lấy đúng chữ trạng thái BE trả.

## 1. Tài chính

| Loại phiếu | Cấp chờ → người duyệt | Trường quan trọng nhất | Tiền | Duyệt phải làm gì | Nhanh |
|---|---|---|---|---|---|
| Đề nghị thanh toán | Chờ TP duyệt → Chờ KT công nợ → Chờ KT trưởng → Chờ BGĐ → Chờ tạo phiếu chi | Số tiền (đổi theo cấp), KH/NCC, Loại chi, Lý do chi, Hình thức TM/CK | Có, ai thấy phiếu cũng thấy | Nhập tiền từng dòng (mặc định = số cấp trước); cấp KT trưởng có thêm "Chuyển duyệt BGĐ" | K |
| Đề nghị thu tiền | Chờ KT duyệt → kế toán thanh toán | Tổng tiền, Khách hàng/NCC, Loại thu, Lý do thu | Có | "Đồng ý" = sang màn Tạo phiếu thu; từ chối bắt lý do | K |
| Yêu cầu hạch toán bổ sung | Chờ duyệt → KT thanh toán (loại 7: KT công ty hỗ trợ) | Số tiền, Loại yêu cầu (7 loại), KH/NCC, Diễn giải, Phiếu nguồn | Có | "Lập phiếu kế toán" hoặc Từ chối | K |
| Yêu cầu điều chỉnh công nợ | "Chờ tạo phiếu kế toán" → KT thanh toán | Số tiền, Loại (KH/NCC), Đối tượng, Giấy báo có gốc | Có | Tạo phiếu kế toán hoặc Từ chối | K |
| Duyệt giá bán hàng hoá | Một cấp, quyền `finance.gia_ban_hang_hoa.approve` | Giá cũ → giá mới theo loại giá, giá vốn + hệ số (có gate xem), lý do sửa giá, ngày hiệu lực | Có (giá vốn che theo quyền) | Được sửa giá/hệ số/ngày hiệu lực; có duyệt hàng loạt sẵn | N\* |
| Gia hạn hàng mượn | Chờ TP → Chờ BGĐ (nếu vượt hạn mức) → Chờ KT duyệt | Ngày hẹn trả cũ → mới, phiếu mượn gốc + hàng mượn, lý do gia hạn | Không | TP/BGĐ chỉ xác nhận; KT phải xác nhận ngày hẹn trả mới | N\* (TP, BGĐ) · K (KT) |
| Hàng giữ: xuất giữ / gia hạn / điều chuyển / huỷ | Chờ TP → Chờ BGĐ → Chờ KT | Loại giữ, hợp đồng, khách, ngày giữ đến, ghi chú, người nhận (điều chuyển) | Không ở list | BGĐ xuất giữ nhập lại ngày giữ; KT lập phiếu xuất giữ | N\* (TP) · K |
| Xuất bán hàng mượn | Chờ TP → Chờ BGĐ → KT kho | Loại, hợp đồng, khách, người tạo | — | TP/BGĐ không nhập gì, từ chối bắt lý do | N\* |
| Yêu cầu nhập hàng | Chờ TP → Chờ BKS → Chờ BGĐ | NCC/khách, loại phiếu, giá mua duyệt (khi trả lại) | Chỉ ở chi tiết | 3 endpoint riêng theo cấp, từ chối bắt lý do | N\* |
| Phiếu thu / Phiếu chi | Thủ quỹ (phiếu chi nhánh B: KT trưởng) | Số tiền thực thu/chi, đối tượng | Có | Nhập số thực thu / số duyệt chi từng dòng, có trần | K |
| Quyết toán thưởng năng suất quý | Chờ duyệt | Tổng thưởng NV, tổng thưởng thêm | Có | Không nhập gì | N |
| Quyết toán thưởng cuối năm | Chờ BGĐ duyệt | Quỹ thưởng, còn lại, tổng duyệt | Có | Duyệt từng dòng | K |
| Yêu cầu mua dịch vụ | Chờ TP → Chờ BKS | Ý kiến TP, ý kiến BKS, đối tượng | — | Có "gửi lại BKS", từ chối | N\* |
| Điều chuyển kho | Chờ duyệt → KT kho nguồn | Kho đi/đến, hàng | — | Chỉ có duyệt, KHÔNG có từ chối | N |
| Kiểm kê (hàng hoá / vị trí) | Chờ KT duyệt / Chờ duyệt kết quả | CÓ CHÊNH LỆCH hay không (list chưa có), kho, ngày kiểm kê | Không | Ghi chú tuỳ chọn; từ chối bắt lý do | N\* |
| Biên bản xử lý thừa thiếu sau kiểm kê | Chờ duyệt | Danh sách dòng xử lý | — | Nhập theo dòng | K |
| Chỉ tiêu kinh doanh (phòng ban / nhân viên) | Chờ duyệt, quyền `sale.chi_tieu_...approve` | Năm, đơn vị, TỔNG DOANH SỐ + SL khách mục tiêu (list chưa có) | Doanh số (chỉ ở chi tiết) | Không nhập; từ chối bắt lý do | N\* |
| Phân chia thị trường (nhân viên) | Chờ duyệt | Nhân viên, số tỉnh/vùng/phường | — | Từ chối bắt lý do | N |

## 2. Công việc

| Loại phiếu | Cấp → người duyệt | Trường quan trọng nhất | Tiền | Duyệt phải làm gì | Nhanh |
|---|---|---|---|---|---|
| Gia hạn dự án TKT | Chờ TP → Chờ BGĐ (theo số ngày xin) | Số ngày xin, lý do, hạn đóng cũ → mới, dự án, cấp duyệt (list đã đủ) | Không | Xác nhận; từ chối bắt lý do — duyệt ngay trên dòng | **N** |
| Báo giá | Chờ TP duyệt → Chờ BGĐ duyệt | Tổng sau VAT, cấp duyệt, khách + dự án, biên lãi (chỉ chi tiết, che theo quyền), có hàng tạm | Có (giá vốn che theo quyền) | Chỉ xác nhận | N\* (cần thêm biên lãi + hàng tạm vào list) |
| Yêu cầu làm giải pháp | Chờ tiếp nhận → phòng tiếp nhận | Tên YC, dự án + khách, giai đoạn + ưu tiên, NGÀY KH CẦN GP, phòng KD | Không | Chọn PM + ngày dự kiến xong (bắt buộc) | K |
| Đề xuất công tác | Chờ duyệt | Khách + hợp đồng, nội dung, thời gian đi, địa điểm, người đi | Không | "Duyệt" = lập phiếu công tác | K |
| Đề xuất công việc | Chờ duyệt (TP phòng yêu cầu) | Tên + mô tả việc, phòng thực hiện, hạn, giờ dự kiến | Không | Qua màn trung gian; từ chối bắt lý do | N\* |
| Giao việc | Chờ duyệt (TP) | Tên việc, phòng thực hiện, tổng công khoán, hạn | Công khoán (điểm) | Đi qua form có thể sửa | K |
| Duyệt kết quả giao việc | Đã nhập kết quả (status 5) | Tổng công khoán, kết quả từng đầu việc, công khoán đề nghị vs duyệt | Điểm công | Nhập công khoán duyệt từng việc | K |
| Giao công tác | Chờ duyệt (TP) | Loại công tác, khách + hợp đồng, thời gian, địa điểm, người đi | Không | Phải rà TRÙNG LỊCH nhân sự | K |
| Duyệt kết quả công tác | status 5 | 4 khoản chi (đi đường, công tác phí, lưu trú, khác), kết quả từng người | Có | Chỉ có "Duyệt kết quả", KHÔNG có từ chối | N\* |
| Đề nghị thanh toán công tác phí | Chờ TP → Chờ KT | Tổng tiền đề nghị (4 khoản), số ngày/đêm đề nghị vs TP duyệt, phiếu công tác gốc | Có (list chưa hiện) | TP chỉnh số ngày/đêm + chi phí | K |
| Quyết toán công khoán theo hợp đồng | Chờ TP → Chờ KT | Hợp đồng, biên bản nghiệm thu, công khoán | Điểm | TP nhập công khoán duyệt, không vượt đã duyệt | K |
| Bàn giao công việc | Chờ TP duyệt | NV bàn giao + lý do, số công việc, người nhận từng mục, ngày bàn giao | Không | Có thể sửa người nhận/hạn; từ chối bắt lý do ≥10 ký tự | N\* |
| Hợp đồng (TKT) | Chờ TP → Chờ pháp chế → Chờ BGĐ | Giá trị HĐ, tổng phát sinh + lý do cần BGĐ, ý kiến pháp chế | Có | Phải qua ý kiến pháp chế; TP có thể chuyển BGĐ | K |
| Gia hạn / kết thúc sớm công tác | Chờ duyệt | Phiếu công tác gốc, ngày kết thúc | — | — | N\* |

## 3. Nhân sự – Chấm công – Đào tạo – Văn bản

| Loại phiếu | Cấp → người duyệt | Trường quan trọng nhất | Tiền | Duyệt phải làm gì | Nhanh |
|---|---|---|---|---|---|
| Đơn xin nghỉ | Gửi TP duyệt → Chờ NSHC duyệt (nếu loại nghỉ yêu cầu) | Loại nghỉ, số ngày + khoảng nghỉ, LÝ DO (list chưa hiện), phép còn lại (chỉ chi tiết), người bàn giao | Không | Xác nhận; từ chối bắt lý do; chỉ duyệt được trước ngày 5 tháng sau | N\* |
| Đơn kết thúc nghỉ phép / kết thúc đăng ký đi muộn về sớm | Gửi duyệt | Đơn gốc, ngày kết thúc cũ → mới | Không | Duyệt/từ chối ngay trên dòng, từ chối KHÔNG cần lý do | **N** |
| Đăng ký đi muộn về sớm | Gửi duyệt | Số phút trễ/sớm đầu-giữa ca, khoảng ngày áp dụng, lý do, có trừ lương | Không | Xác nhận | N\* (list chưa có số phút) |
| Đăng ký làm thêm | Gửi duyệt | Giờ làm thêm (bắt đầu–kết thúc, trừ nghỉ giữa ca), lý do, loại việc, hợp đồng | Không | Xác nhận; BE kiểm trần giờ OT/tháng rồi mới cho (có thể 422) | N\* |
| Phiếu yêu cầu làm thêm | Gửi duyệt | Phòng yêu cầu/thực hiện, nội dung việc, khoảng ngày | Không | Xác nhận | N\* |
| Đề nghị tra soát công | Gửi TP duyệt → Chờ NSHC duyệt | Ngày công, giờ cần tra soát, loại lý do, ghi chú, FILE ĐÍNH KÈM | Không | Xác nhận; cấp 2 tự tạo bản ghi chấm công | N\* |
| Phiếu đi công tác | Gửi duyệt | Người đi, từ–đến, địa điểm, khách/hợp đồng | Không | BE chặn trùng lịch; phiếu quá hạn phải nhập lại thời gian | N\* |
| Phiếu giao việc trong ngày | Gửi duyệt | Nội dung việc, khách, thời gian bắt đầu, tổng phút | Không | Xác nhận | N\* |
| Kế hoạch đào tạo | Chờ duyệt | Tên, khoảng thời gian, phiếu khảo sát, môn/khoá bên trong | Không ở list | Từ chối bắt lý do | K |
| Đề xuất đào tạo | Chờ TP duyệt → Chờ QLĐT duyệt | Môn học, loại + hình thức, học viên, chi phí/người (khoá, hỗ trợ, tự trả), tháng cam kết | Có | QLĐT sửa chi phí duyệt + chọn môn | K |
| Đề xuất khoá học / Khoá học | Chờ TP → Chờ BGĐ | Môn học, hình thức nội bộ/thuê ngoài, nền tảng, thời gian, giảng viên, chi phí & doanh thu | Có (list không trả) | Từ chối bắt lý do | K |
| Quyết định (17 loại) | Đã tạo (xem xét) → Đã xem xét (duyệt) | Loại QĐ, ĐỐI TƯỢNG ÁP DỤNG (list chung chưa có), ngày hiệu lực, giá trị chính theo loại (lương mới, tổng thưởng, chức danh mới…) | Một số loại | 2 quyền khác nhau (xem xét / duyệt); từ chối bắt lý do | N\* |
| Biên bản xử lý sự cố | Đã tạo | Tên + loại sự cố, ngày + nơi xảy ra, số người vi phạm | Không | Từ chối bắt lý do | N\* |
| Phiếu đăng ký bảo hiểm | Đã tạo | Nhân viên + phòng, loại + gói, chế độ, tổng phí, phần NV/công ty đóng | Có | Phải nhập số tiền duyệt, không vượt tổng phí | K |
| Đặt phòng họp | Chờ duyệt (quản lý phòng hoặc quyền duyệt) | Thời gian, phòng, mục đích, người đặt, số người vs sức chứa | Không | Duyệt ngay trên dòng; từ chối bắt lý do | **N** |

## 4. Bán hàng – CSKH – Vận chuyển

| Loại phiếu | Cấp → người duyệt | Trường quan trọng nhất | Tiền | Duyệt phải làm gì | Nhanh |
|---|---|---|---|---|---|
| HĐ sửa chữa - bảo dưỡng - bảo trì | Chờ duyệt → `approver_id` hoặc quản lý phòng | Tổng thanh toán (sau VAT), khách hàng, số báo giá gốc, người tạo | Có (ai thấy dòng cũng thấy) | Ghi chú tuỳ chọn; từ chối bắt lý do | N\* |
| Chuyến xe khác | Chờ duyệt → quyền "Duyệt chuyến xe khác" | Cước thực tế, biển số + NCC, tên chuyến, số km (list chưa có) | Có | Không nhập; từ chối bắt lý do | N\* |
| Phiếu nhập kết quả (CSKH) | Chờ duyệt kết quả → quyền "Duyệt phiếu nhập kết quả" | Khách, hợp đồng, phiếu giao việc, người thực hiện | Chỉ ở chi tiết | Duyệt là 1 form lớn sinh phiếu con, đổi serial | K |

## 5. Không phải "chờ duyệt" — nên loại khỏi màn tổng hợp
- Hàng đợi giao việc / làm báo giá của CSKH (chờ người dùng làm việc, không có bước duyệt).
- Chuyến xe chở hàng "chờ hạch toán": việc của kế toán, mở ERP.
- Yêu cầu nhập kho / xuất kho / vận chuyển "Chờ duyệt": thực chất là giao việc cho thủ kho; kiểm kê trạng thái "Chờ xử lý".
- Phiếu báo có: không có trạng thái chờ.

## 6. Mục menu Bán hàng › Phê Duyệt CHƯA có màn trên HRM
HĐ vật tư-hàng hoá-thiết bị (+ PL bổ sung/giảm), PL bổ sung/giảm của HĐ SC-BD-BT, HĐ nguyên tắc (+ PL), ĐH nguyên tắc (+ PL), HĐ dự án (+ PL), biên bản thanh lý, quyết toán HĐ, KH bán hàng, KH phát triển thị trường; trong Công việc: duyệt kết quả giao việc tại công ty, duyệt kết quả công tác nghiệp vụ, yêu cầu lắp đặt bàn giao.

## 7. Kết luận thiết kế
1. **"Cấp duyệt" = chữ trạng thái BE trả** (đúng mockup), mỗi module tự đặt chữ ("Chờ TP duyệt", "Gửi TP duyệt", "Chờ kế toán trưởng duyệt"…), màu BE trả.
2. **Trường quan trọng khác nhau theo từng loại** → KHÔNG làm xem nhanh / ngăn kéo / cột tóm tắt riêng từng loại (user chốt 13/11/2026: không kiểm soát được trường nào quan trọng cho từng loại phiếu). Danh sách chỉ hiện trường chung; muốn xem nội dung thì mở phiếu. Số tiền chỉ là cột tuỳ chọn.
3. **Duyệt nhanh / hàng loạt (nếu còn giữ — chờ user chốt)** chỉ cho loại đánh dấu N / N\* : BE trả cờ `quick_approve`; loại K chỉ "Mở phiếu".
4. **Từ chối gần như luôn bắt lý do**, trường lý do mỗi nơi một tên → màn tổng hợp phải có popup nhập lý do chung và map tên trường theo loại.
5. **Chặn trưởng phòng khi nhân viên còn hàng quá hạn** (`checkDueConfigsManager`) chỉ áp Chấm công/Công việc → duyệt từ màn tổng hợp sẽ gặp 403 đặc thù, phải hiện thông báo đó.
6. **Điều kiện bảo mật trước khi làm duyệt nhanh/hàng loạt:** `AssignJobController::deny/approveResult` không tự kiểm quyền; đề nghị thanh toán công tác phí, quyết toán công khoán, gia hạn/kết thúc sớm chỉ kiểm quyền không kiểm phòng/công ty; tra soát công cho phép NV có cả 2 quyền nhảy cấp NSHC; kế hoạch đào tạo, phiếu bảo hiểm, biên bản sự cố thiếu kiểm quyền ở BE; nhiều màn `type=waiting` trả mọi phiếu của chính người xem khi họ không có quyền duyệt.

## 8. Điều chưa xác minh (agent ghi lại)
Quyền duyệt riêng của kiểm kê hàng hoá; lý do bắt buộc khi từ chối chỉ tiêu và quyết toán thưởng năm; lệch phạm vi công ty ở pending điều chỉnh công nợ; chi tiết FE của vài loại hàng giữ; phân quyền xem số tiền ở đề xuất đào tạo / phiếu bảo hiểm; ý nghĩa nghiệp vụ của vài luồng Payroll/Human (BonusDistribution, P3Salary, SalaryAdvance, EmployeeInfoUpdateRequest).
