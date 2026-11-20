# Báo cáo thị trường theo Khu vực kinh doanh — design (#12091 + #11888)

**Người phụ trách:** @junfoke — 2026-11-20
**Redmine:** #12091 (sửa cả nhóm báo cáo thị trường, CSKH trước bán) + #11888 (Phân chia thị trường, có mockup `mockup-11888-phan-chia-thi-truong.html`).
**Nhánh:** `task_12091` ở hrm-api + hrm-client (tách `origin/gop_db` 20/11/2026).
Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-11-20-bao-cao-thi-truong-theo-kvkd-design.md`.

## Mục tiêu
Chiều "thị trường" của các báo cáo đổi từ Tỉnh / Phường-xã sang **Tỉnh → Khu vực kinh doanh (KVKD)**. KVKD gom cụm phường/xã
trong 1 tỉnh (#12040); KH thuộc KVKD qua `customers.ward_id → business_area_wards → business_areas`.

## Phạm vi (8 báo cáo)
| Báo cáo | Việc |
|---|---|
| Kết quả CSKH tiềm năng | Phần Thị trường: Tỉnh → KVKD (thay Phường/xã) |
| Tổng hợp nhu cầu làm dịch vụ | Cây Tỉnh → KVKD → KH, ô lọc, đếm KVKD |
| Kết quả meeting theo thị trường | Cây Tỉnh → KVKD → KH → meeting, ô lọc, khối tổng hợp |
| Phát triển thị trường - KH | Thêm cấp KVKD vào tiêu chí; **snapshot KVKD xuống `meetings`** |
| Phân chia thị trường (#11888) | Theo mockup: nguồn phiếu NV đã duyệt, cây Tỉnh → KVKD → Phòng → NV |
| Tổng hợp CSKH tiềm năng · Phát triển KH theo NVKD · DS đăng ký KH | Thêm ô lọc Tỉnh + KVKD, cột KVKD |
| Kế hoạch & KQ làm việc NV | **Không làm** (4/5 nguồn không gắn KH) |

## Quyết định đã chốt (user 20/11/2026)
1. KVKD **thay** cấp Phường/xã; báo cáo chỉ có Tỉnh thì **thêm** cấp KVKD dưới Tỉnh.
2. Báo cáo chưa có chiều thị trường: thêm lọc + cột — trừ Kế hoạch & KQ làm việc NV.
3. Phân chia thị trường: KVKD thay hẳn Phường/xã (chi tiết theo mockup #11888).
4. Phát triển thị trường: snapshot KVKD cùng luật snapshot tỉnh (ghi lần đầu / đổi KH); seeder bù cả tỉnh + KVKD.

5. (20/11) Tỉnh theo KVKD (L1) · KVKD khoá vẫn hiện (trừ Phân chia TT) · Phân chia TT xếp KVKD **theo tên** · Phân chia TT **giữ tự tải** khi vào màn
   (không theo mockup "chưa Tìm kiếm thì trống") · code ở **repo chính** (không worktree).

## Luật chung (đã chốt 20/11)
- Tỉnh của KH = tỉnh của KVKD nếu KH thuộc KVKD, ngược lại tỉnh của KH (prod 1.580 KH lệch).
- KH không thuộc KVKD ⇒ "Chưa xác định khu vực", xếp cuối trong tỉnh.
- KVKD khoá vẫn gom theo nó — **trừ Phân chia thị trường** (mockup: loại KVKD khoá).
- Không đọc DB ERP cũ: sửa luôn 2 service đang join `DB_DATABASE_SECOND`.

## Triển khai prod
Migration 1 bảng (`meetings` +2 cột) + chạy `BackfillMeetingProvinceSeeder` 1 lần (vá luôn 535 meeting cũ chưa có tỉnh).
