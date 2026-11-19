# Tư vấn: các góc nhìn cho lãnh đạo theo dõi Dự án tiền khả thi (TKT) — 12/11/2026

Dựa trên dữ liệu đang có trong `prospective_projects` + bảng liên quan (DB local `db_gop_6_11`: 586 dự án, 1,242 dòng nhật ký
đổi trạng thái, 189 liên kết meeting, 143 dự án có lý do đóng). Cột "Agent" = TPE SMART AGENT trả lời được chưa.

## A. Bức tranh tổng — "đang có gì trong ống"
| # | Góc nhìn | Câu lãnh đạo hay hỏi | Dữ liệu | Agent |
|---|---|---|---|---|
| A1 | Phễu theo tiến trình (số dự án + tổng ngân sách từng bước) | "Ống dự án đang ở đâu, bao nhiêu tiền?" | `status`, `estimated_budget` | ✅ `thong_ke_du_an_tkt` (tien_trinh) |
| A2 | Theo lĩnh vực / nhóm ngành | "Mảng nào đang nhiều dự án / tiền nhất?" | `scope_id` → nhóm ngành → lĩnh vực | ✅ (12/11) |
| A3 | Theo PHÒNG (so các phòng KD với nhau) | "Phòng nào đang gánh nhiều nhất?" | `department_id` / `main_sale_department_id` | ✅ (12/11) `thong_ke_du_an_tkt` nhom_theo `phong` |
| A4 | Theo NVKD | "Ai đang ôm nhiều dự án / tiền nhất?" · "Anh A tháng 10 có bao nhiêu dự án?" | `main_sale_employee_id` | ✅ (nvkd) · (12/11) `ket_qua_du_an_tkt` theo kỳ, khớp báo cáo Kết quả thực hiện dự án TKT |
| A5 | Top dự án lớn nhất | "10 dự án ngân sách lớn nhất đang theo đuổi?" | `estimated_budget` | ✅ (12/11) `du_an_tkt` sap_xep `ngan_sach_giam` |
| A6 | Pipeline có trọng số (ngân sách × xác suất theo bước) | "Dự kiến chốt được bao nhiêu tiền quý này?" | `status` + bảng hệ số do lãnh đạo chốt | ❌ cần chốt hệ số từng bước |

## B. Sức khoẻ ống — "cái gì đang tắc"
| # | Góc nhìn | Câu hỏi | Dữ liệu | Agent |
|---|---|---|---|---|
| B1 | Dự án "đứng im": không đổi bước / không meeting N ngày | "Dự án nào 30 ngày không ai đụng tới?" | `prospective_project_status_logs.changed_at`, meeting gắn dự án | ✅ (12/11) `du_an_tkt` dung_im_ngay — hoạt động = đổi bước / meeting đã diễn ra / ngày tạo |
| B2 | Sắp / quá hạn KH cần giải pháp | "Giải pháp nào sắp trễ hạn khách?" | `customer_need_solution_date` + giải pháp | ✅ `du_an_tkt` (sap_toi_han_gp), `giai_phap` |
| B3 | Sắp tự đóng / quá hạn dự án | "Dự án nào tuần sau tự đóng?" | `auto_close_date` (527 dự án có), `end_date`, `extended_days`, đơn gia hạn | ✅ (12/11) `du_an_tkt` sap_dong_ngay (mặc định = cấu hình nhắc trước hạn đóng, gồm cả đã quá hạn) |
| B4 | Thời gian trung bình mỗi bước (chu kỳ bán) | "Từ thu thập thông tin tới thương thảo mất bao lâu?" | `status_logs` (from → to, changed_at) | ❌ (cần tính từ nhật ký) |
| B5 | Đơn gia hạn dự án chờ duyệt | "Có đề nghị gia hạn nào chờ tôi?" | `prospective_project_extension_requests` | ✅ (12/11) `gia_han_du_an_tkt` (dùng nguyên pendingQuery 2 cấp TP / BGĐ; cua_toi) |

## C. Kết quả — "thắng / thua vì sao"
| # | Góc nhìn | Câu hỏi | Dữ liệu | Agent |
|---|---|---|---|---|
| C1 | Tỉ lệ thắng theo kỳ / phòng / NVKD / lĩnh vực | "Tỉ lệ thắng năm nay của từng phòng?" | `status` thắng / đóng | ✅ (12/11) theo phòng kèm tỉ lệ thắng |
| C2 | Lý do thua / đóng | "Thua nhiều nhất vì lý do gì?" | `closed_reason_id` (143), `closed_note` | ✅ (12/11) nhom_theo `ly_do_dong` — dữ liệu local: 99/137 là "Hệ thống tự đóng do quá thời gian", 21 "Tạo sai" ⇒ lý do thua thật chỉ ~17 |
| C3 | Giá trị thắng: ngân sách vs giá trị hợp đồng dự kiến / lợi nhuận dự kiến | "Dự án thắng mang về bao nhiêu, lãi dự kiến?" | `expected_contract_amount`, `expected_profit` | ❌ (cần kiểm cột có được nhập đều không) |

## D. Khách hàng & hoạt động
| # | Góc nhìn | Câu hỏi | Agent |
|---|---|---|---|
| D1 | Lịch sử chăm sóc 1 KH, dự án của KH | "KH ABC đang có dự án gì, gặp lần cuối khi nào?" | ✅ `lich_su_cham_soc_khach_hang`, `chi_tiet_du_an_tkt` |
| D2 | Meeting theo thị trường (tỉnh) | "Hà Nội tháng này gặp bao nhiêu KH?" | ✅ `meeting_theo_thi_truong` |
| D3 | Dự án lớn chưa có meeting gần đây | "Dự án > 5 tỷ nào 2 tháng chưa gặp khách?" | ❌ (ghép B1 + A5) |
| D4 | Phòng hỗ trợ / giải pháp đang gánh | "Phòng kỹ thuật đang hỗ trợ bao nhiêu dự án?" | ❌ (`support_departments`, `solution_department_id`) |

## Đề xuất thứ tự làm (giá trị / công sức)
1. **Chiều `phong` + sắp xếp theo ngân sách** (A3, A5, C1 theo phòng) — đang làm theo yêu cầu 12/11.
2. **B1 dự án đứng im** + **C2 lý do thua** — giá trị cao, dữ liệu sẵn, mỗi cái là 1 tham số / 1 chiều nhóm.
3. **B3 sắp tự đóng / quá hạn** + **B5 gia hạn chờ duyệt**.
4. **B4 chu kỳ bán** (tính từ nhật ký) và **A6 pipeline có trọng số** — cần lãnh đạo chốt hệ số xác suất từng bước.
5. Báo cáo định kỳ (gửi tóm tắt tuần cho lãnh đạo qua thông báo) — sau khi các góc trên ổn định.
