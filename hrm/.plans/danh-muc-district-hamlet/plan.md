# Port Quận/Huyện (districts) + Đường/Phố (hamlets) ERP → HRM

Khuôn: HRM Ward (Human module, style cũ b-table/Select2). Rule ERP: "Xóa"=khóa mềm
(status→0), không check tham chiếu; list chỉ status=1. Không lock/unlock. Không code.
Không permission (địa lý HRM không gán quyền). id auto_increment.

- districts: name, province_id, status → thuộc Tỉnh/TP
- hamlets: name, ward_id, status → thuộc Phường/xã (ward→tỉnh)

## Tasks
- [x] BE District: Entity, Service, Controller, Request, 2 Resource, routes /human/districts
- [x] BE Hamlet: Entity, Service, Controller, Request, 2 Resource, routes /human/hamlets
- [x] FE districts: pages/human/districts/{index.vue, components/DistrictModel.vue}
- [x] FE hamlets: pages/human/hamlets/{index.vue, components/HamletModel.vue}
- [x] Menu master-data.js: gắn link 2 mục xám (Quận/Huyện, Đường/Phố)
- [x] php -l + runtime verify

### Checkpoint — 2026-08-04
Vừa hoàn thành: BE+FE Quận/Huyện + Đường/Phố + menu, push gop_db (hrm-api c47ab8d1a, hrm-client 79b5cb578). Bước tiếp: user verify + yarn dev.
Blocked:
