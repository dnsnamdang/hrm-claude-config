# Demo màn hình phân hệ Kế toán HRM (HTML tĩnh cho khách hàng)

> Spec đầy đủ: `docs/superpowers/specs/2026-07-14-demo-man-hinh-ke-toan-design.md`
> Người phụ trách: @dnsnamdang · Bắt đầu: 2026-07-14 · Phase 1–10 hoàn thành: 2026-07-15

## Mục tiêu
Bộ **file HTML demo tĩnh** (mở double-click, offline, không server) cho khách hàng xem các chức năng sắp phát triển của phân hệ Kế toán HRM. Dữ liệu mẫu tiếng Việt thao tác được, giao diện đúng design system V2 của hrm-client.

## Phạm vi đã dựng (`demo/` — 12 trang + assets)
| Nhóm màn | File | Nguồn |
|---|---|---|
| Khế ước đi vay / cho vay (danh sách, form 4 tab + sinh lịch trả nợ, chi tiết + ghi nhận trả) | `di-vay-*.html`, `cho-vay-*.html` (6 màn) | Khảo sát MISA + Fast qua Playwright (ảnh `tham-khao/`) |
| Sổ nhật ký chung S03a-DN (20 cột mở rộng ERP, lọc 4 cấp cascade, lũy kế kỳ trước, in mẫu chuẩn) | `so-nhat-ky-chung.html` | `Mau_So_Nhat_Ky_Chung_TT99_2025.xlsx` |
| Nhật ký thu / chi tiền S03a1/S03a2 (2 tab, TK đối ứng cột-hóa, cân đối ngang, đối chiếu dòng tiền) | `nhat-ky-thu-chi.html` | `Mau_So_Nhat_Ky_Thu_Chi_TT99_2025.xlsx` |
| Sổ quỹ tiền mặt S04a/S04b (3 tab: VNĐ tồn realtime + cảnh báo chi TM ≥5tr NĐ 181/2025 · ngoại tệ song song USD/VNĐ · đối chiếu "3 số dư phải khớp") | `so-quy.html` | `Mau_So_Quy_TT99_2025.xlsx` |
| Sổ Cái S03b-DN (theo TK × pháp nhân, dẫn xuất từ NKC, Trang/STT NKC hyperlink `?line=`, số dư lũy kế) | `so-cai.html` | `Mau_So_Cai_TT99_2025.xlsx` |
| Bảng cân đối kế toán B01-DN (màn hình ĐÚNG mẫu chuẩn TT99 5 cột: Chỉ tiêu/Mã số/TM/Số cuối năm/Số đầu năm; số hợp nhất đã loại trừ GD nội bộ ngầm, select Phạm vi xem từng pháp nhân, thu gọn cấp) | `bang-can-doi.html` | `Mau_Bang_Can_Doi_Ke_Toan_TT99_2025.xlsx` |
| Bảng kê hóa đơn bán hàng, dịch vụ (theo mẫu Fast rpt_sobk1t: nguồn Phiếu xuất hàng + Phiếu hạch toán dịch vụ ERP; 9 cột chuẩn Ngày ct/Mã ct/Số ct/Mã khách/Tên khách/Tiền/Thuế/Chiết khấu/Phải thu; link Số CT NKC `?line=`; Tổng cộng đầu bảng) | `bang-ke-hoa-don-ban-hang.html` | Khảo sát Fast qua Playwright (`tham-khao/fast-bang-ke-hdbh-*.png`) |
| Bảng kê chứng từ theo mã phí (theo mẫu Fast rpt_gldtbkb: nhóm theo mã phí, mỗi nghiệp vụ hiện 2 vế Nợ/Có cân đối, tổng nhóm + tổng cộng; nguồn = bút toán có gắn mã phí; note-box hướng dẫn dev) | `bang-ke-chung-tu-ma-phi.html` | Excel `Bảng kê chứng từ theo mã phí` + khảo sát Fast (`tham-khao/fast-bkct-maphi-*.png`) |
| Sổ tổng hợp chữ T của một tài khoản (chọn 1 TK → SDĐK + bảng theo TK đối ứng PS Nợ/Có + Tổng phát sinh + SDCK; tái dùng công thức số dư Sổ Cái nên khớp số) | `so-tong-hop-chu-t.html` | Excel `Sổ tổng hợp chữ T của một tài khoản` |
| Báo cáo số dư tiền (3 tab: chi tiết 16 cột / tổng hợp pivot + nhận xét / đối chiếu sao kê NH) | `bao-cao-so-du-tien.html` | `Mau_BC_So_Du_Tien.xlsx` |
| Cấu hình hạch toán cho các loại phiếu (Vue 3 vendor offline: nhóm bút toán, công thức ƒx + điều kiện, kéo thả dòng, lưu cấu hình theo phiên bản + lịch sử chỉnh sửa, select TK có search) | `posting-rule-engine-v3.html` | File user cung cấp, restyle V2 + redesign layout |

## Quyết định lớn
- **Giao diện trích từ source hrm-client** (feedback user): theme UBold default (Roboto, primary `#1abc9c`, body `#f5f6f8`), shell sidebar trắng condensed + topbar trắng, component V2 (`tp-card`, `v2-btn`, `data-table`, `status-pill`), Remix Icon tải offline `assets/vendor/`. KHÔNG tự chế palette.
- **Pháp nhân thật từ DB hrm_tpe.companies**: TPE (mẹ) · TPSG (con 100%) · TPHP (chi nhánh) — xuyên suốt mọi màn, có cặp giao dịch nội bộ HĐ-IC01 (1368↔3368, cờ GD nội bộ Y) chạy từ NKC → thu/chi → Sổ Cái → loại trừ ở BCĐKT hợp nhất.
- **Dữ liệu sổ sách dẫn xuất 1 nguồn**: `journal.js` (30 bút toán) là nguồn cho Sổ Cái (TK đối ứng, số dư) — thể hiện đúng nguyên tắc "kế thừa từ NKC" trong file mẫu.
- **Chuẩn UI thống nhất mọi màn sổ/báo cáo** (nhiều vòng feedback, helper chung trong `app.js`): (1) Bộ lọc — trường mặc định = trường bắt buộc, khối Công ty–PB–BP là 1 checkbox (`setupFilterSettings` nhóm trường), nút "Ẩn bộ lọc" (`setupFilterHide`), hàng tìm nhanh + nút Tìm kiếm/Nhập lại cùng hàng full-width; (2) Bảng — header 1 hàng (bỏ group), icon sort mọi cột xoay vòng tăng→giảm→bỏ (`setupColumnSort`; lũy kế/tồn quỹ giữ giá trị theo trình tự thời gian), "Cấu hình cột" ẩn/hiện + kéo thả thứ tự với cột chuẩn mẫu sổ bị khóa (`setupColumnConfig`), phân trang 10/25/50/100/Tất cả (`createPager`; dòng tổng luôn tính trên toàn bộ kết quả lọc), dòng tổng sticky đầu bảng (`applyStickyTotals`), bỏ thẻ stat-row — thông tin tổng quan đưa vào bảng; (3) Tách cột Mã/Tên đối tượng (danh mục `OBJECT_NAMES` dùng chung); (4) NKC sắp xếp chuẩn kế toán (ngày ghi sổ → ngày CT → số CT → Nợ trước Có sau, STT đánh lại liên tục); mọi cài đặt lưu localStorage theo màn; bản in mẫu chuẩn TT99 không bị ảnh hưởng bởi sort/cột/phân trang.
- **Quy định chi tiền mặt cập nhật 2025**: Luật Thuế GTGT 48/2024/QH15 + NĐ 181/2025/NĐ-CP (hiệu lực 01/07/2025) — hóa đơn HHDV ≥ 5 triệu phải thanh toán không dùng tiền mặt mới được khấu trừ VAT/chi phí được trừ; sổ quỹ cảnh báo ⚠ trên phiếu vi phạm (thay ngưỡng 20tr cũ).
- Mọi màn có nút **In** đúng mẫu chuẩn TT99 (font Times, header 2 tầng, chữ ký 3 bên, `@media print` chỉ in tờ sổ) + Xuất Excel giả lập; mọi phase verify E2E Playwright đối chiếu số liệu với file Excel nguồn.

## Ngoài phạm vi
BE/API/DB thật, phân quyền, engine hạch toán — sẽ spec riêng khi khách chốt demo.
