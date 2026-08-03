# Design (tóm tắt) — Thông báo lỗi import Excel Quyết định khi sheet thông tin chung bị loại

**Người phụ trách:** @junfoke — 2026-07-31

## Mục tiêu

Khi import Excel HĐLĐ / Điều chỉnh lương, nếu dòng ở sheet thông tin chung (`ThongTinHopDong` /
`ThongTinChung`) bị loại vì lỗi, sheet dữ liệu chính đang báo lỗi **sai bản chất** khiến KH tưởng
"email không khớp" và không tìm ra nguyên nhân thật. Sửa để thông báo trỏ thẳng về dòng gốc.

## Bối cảnh (case thật)

KH VNPT HCM import "HĐLĐ không định biên" (~800 NV, đã cắt thử 100 NV) → **mọi dòng** đều báo:

```
Không tìm thấy thông tin hợp đồng lao động trong sheet ThongTinHopDong với email: CTV083020@kasaco.com.vn
Loại hợp đồng chưa có tỷ lệ hưởng lương hợp lệ (1-100).
```

KH khẳng định email khớp ở cả 2 tab — và đúng là khớp.

## Root cause

`DecisionLaborContractNoManpowerInfoImport::collection()` chỉ ghi vào `infoByEmail` khi dòng
**không còn lỗi nào**. Chỉ cần 1 lỗi tra danh mục (Loại HĐ / Chức vụ / Chức danh / Nhiệm vụ) là
dòng bị bỏ → sheet chính không tra được `$info` → sinh 2 thông báo trên cho **mọi** dòng:

- Lỗi 1: `$info === null`.
- Lỗi 2: `$info['salary_percentage']` không tồn tại → cũng do `$info === null`.

Tức **1 nguyên nhân đẻ ra 2 thông báo, cả 2 đều không phải nguyên nhân thật**. Lỗi thật vẫn có
trong danh sách trả về nhưng nằm ở các dòng bị gắn nhãn trong nội dung lỗi (`"ThongTinHopDong - ..."`)
nên KH không nhận ra.

## Quyết định chính

1. Phân biệt 2 tình huống khi `$info` rỗng: **email có trong sheet nhưng dòng bị loại** (báo rõ số
   dòng + chỉ chỗ xem chi tiết) vs **email không có trong sheet** (giữ thông báo cũ).
2. Chỉ kiểm tra tỷ lệ hưởng lương khi đã có `$info`, và thêm tên loại HĐ vào thông báo.
3. Nhãn sheet phụ chuyển từ nội dung lỗi lên **cột "Dòng"** (`[ThongTinHopDong] 101`) để nhìn bảng
   là biết dòng nào thuộc sheet nào.
4. Áp dụng đồng bộ cho **4 file import** (HĐLĐ có/không định biên, Điều chỉnh lương có/không định biên).

**Không** đổi luật validate, không đổi dữ liệu ghi xuống — chỉ đổi thông báo.

## Ngoài scope

Sửa dữ liệu file Excel của KH; nới lỏng scope công ty của `WorkingPosition`/`Title` (xem GOTCHA
trong spec).

Spec đầy đủ: `docs/superpowers/specs/2026-07-31-import-decision-excel-info-sheet-error-design.md`
