# HDSD QLDA — Rà soát & cập nhật (7 tài liệu)

@manhcuong | Khởi tạo: 2026-07-04

## Mục tiêu
Rà soát 7 HDSD module QLDA trong `HDSD_update/` đối chiếu code hiện hành, sửa chỗ SAI (code đã đổi), bổ sung chỗ THIẾU, chụp lại ảnh các màn đã đổi. Nguồn creds: dev-hrm.eteksofts.com (namdangit@gmail.com).

## Phạm vi (user chốt 2026-07-04)
- Cập nhật **cả 7 file**.
- Ảnh: **chụp lại chỉ màn đã đổi** (Playwright), giữ ảnh cũ còn đúng.
- QLDA_14 x3: **giữ 3 file, chỉ sửa lỗi** (không gộp/không tách lại).

## 7 tài liệu
1. QLDA_12_HDSD_LamBaoGia
2. QLDA_13_HDSD_TongHopBomlist
3. QLDA_14_HDSD_QuyTrinhTongQuan
4. QLDA_14_HDSD_TongQuan_MotPhong
5. QLDA_14_HDSD_TongQuan_LienPhongBan
6. QLDA_16_HDSD_ChuyenDoiBaoGia_EBOM_CBOM
7. QLDA_16_HDSD_DieuChinhBaoGia

## Nguồn dữ liệu
- Text hiện tại: scratchpad/doctxt/*.txt
- Báo cáo gap: scratchpad/report_baogia.md, report_bom.md, report_tongquan.md
- Ảnh hiện có: hdsd_flow_shots/{q_steps,sol_steps,bom-list,quotations,prospective-projects,...}
- Ảnh mới chụp: bổ sung vào các thư mục trên.

## Các điểm SAI trọng yếu (tóm tắt — chi tiết ở report_*.md)
Báo giá: cấp duyệt = max(giá trị đơn, tỷ suất); ERP tự động; tiền tệ đổi được khi tạo mới; cột "Mã BG • BOM" gộp; chốt/huỷ chốt ở tab Báo giá màn Dự án.
BOM: chỉ BOM tổng hợp "Đã duyệt" mới lập báo giá; gộp không cộng dồn SL; thiếu Import Excel; điều kiện nút Sửa/Xoá.
Tổng quan: 3 biến thể trùng; tên trạng thái/tab; task assignee = toàn công ty; 2 trường bắt buộc tạo GP (Nhóm ngành, Nhóm giải pháp).

## Cách tái dựng docx
Generator python-docx theo skill hdsd-documenter: copy 1 file docx hiện có làm khung (giữ Bìa/TOC/TOF/styles), strip body, rebuild nội dung đã sửa, chèn ảnh + caption SEQ, purge media mồ côi, updateFields=true, verify broken=0. Generator lưu scratchpad (ephemeral).
