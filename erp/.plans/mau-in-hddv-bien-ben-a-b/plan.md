# Mẫu in HĐ dịch vụ (loại 6, mẫu HĐCUDV 244): bổ sung biến bên A/B theo HĐ bán hàng (chưa có số Redmine) — @junfoke

Repo ERP `TanPhatDev`, nhánh `feat/mau-in-hddv-bien` (tách từ `origin/gop_db`, không track).

## Ngày 18/11/2026 (@junfoke)
- [x] 18/11/2026 — `WarrantyRepairServiceContractPrint::getDataPrint` (dùng chung 3 bản in HĐ, phụ lục, PLBS của HĐ dịch vụ SC-BH): thêm biến lấy giống HĐ bán — `DIA_CHI`, `DIA_CHI_KH`, `SDT`, `DIEN_THOAI_KH`, `EMAIL_KHACH_HANG`, `MST_KH`, `EMAIL_CONG_TY`, `SO_CCCD_OPTION` (chỉ khách cá nhân), `MST_KHACH_HANG_OPTION` (chỉ khách DN), `CCCD_KHACH_HANG`, `NGAY_CAP_CCCD` (0000-00-00 để trống), `NOI_CAP_CCCD`; điền thêm các biến trước in trống: `DIA_CHI_GIAO_HANG`, `FAX_KHACH_HANG`, `NGUOI_DAI_DIEN_CTY`, `CHUC_VU_NGUOI_DAI_DIEN_CTY`, `DON_VI`.
- [x] 18/11/2026 — `PrintTemplateVariable`: khung chọn biến loại 6 thêm bộ biến bên A/B; đổi `CHI_TIET` → `CHI_TIET_HOP_DONG` (mẫu cũ dùng `CHI_TIET` vẫn in được) + thêm `DICH_VU`, `VAT_TU_HANG_HOA`, `CHI_PHI_KHAC`, `TONG_THANH_TOAN`, `THANH_TOAN`, `DIA_CHI_GIAO_HANG`; hàm phụ `buildVariables` dùng riêng trong file.
- [x] 18/11/2026 — Kiểm local HĐ 8881 (DN) + 8156 (cá nhân): 18 biến bôi vàng đều ra dữ liệu, mẫu 216 / 229 không còn biến trống.
- [x] 18/11/2026 — Commit `7435ca2d91` (đã push nhánh) + merge `develop_02` `83aa16c5f2` (đã push). Sau deploy mở `/admin/print-template-variables/update-variables/6` một lần; HĐ cũ giữ bản sao mẫu cũ.
- [x] 18/11/2026 — Hỗ trợ kiểm số thập phân trong các biến: biến bên A/B toàn chữ; dấu phân cách tiền đúng chuẩn, nhưng các bảng có sẵn (`CHI_TIET_HOP_DONG`, `DICH_VU`, `VAT_TU_HANG_HOA`) in SL bằng `number_format` (2.5 → 3) và % CK / VAT làm tròn — lệch HĐ bán (`formatQuantity`). Đã chỉ dòng cần sửa, chưa sửa.
- [ ] Chờ user: sửa SL / % sang `formatQuantity`; công ty bên B đang lấy theo người bấm in (HĐ bán lấy theo người lập) — có đồng bộ không.
