# Design — Duyệt hợp đồng kết xuất cung ứng

**Người phụ trách:** @khoipv · **Ngày:** 16/09/2026 · **Trạng thái:** đã chốt design

> Spec đầy đủ: [docs/superpowers/specs/2026-09-16-duyet-ket-xuat-hop-dong-cung-ung-design.md](../../docs/superpowers/specs/2026-09-16-duyet-ket-xuat-hop-dong-cung-ung-design.md)

## Mục tiêu

Chèn **1 bước duyệt** vào luồng kết xuất hợp đồng bán sang phân hệ Cung ứng.
Hiện tại người lập HĐ bấm "Kết xuất sang cung ứng" là HĐ sang thẳng Cung ứng.
Sau thay đổi: HĐ phải được người có quyền **"Duyệt hợp đồng kết xuất cung ứng"** duyệt mới sang.

## Vòng đời trạng thái

```
3 Đã duyệt ──gửi──► 10 Chờ duyệt kết xuất ──duyệt──► 9 Đã kết xuất
                        │  ▲                 │
              thu hồi   │  │ gửi lại         │ từ chối (bắt buộc lý do)
                        ▼  │                 ▼
                    3 Đã duyệt        11 Không duyệt kết xuất
```

## Các quyết định lớn

| # | Quyết định |
|---|---|
| 1 | Thêm **2 hằng trạng thái**: `CHO_DUYET_KET_XUAT = 10`, `KHONG_DUYET_KET_XUAT = 11` |
| 2 | `supply_rendered_at` / `_by` **chỉ ghi lúc DUYỆT** → phân hệ Cung ứng **không phải sửa dòng nào** |
| 3 | Thêm 2 cột tra cứu `supply_render_requested_at` / `_by` (index, không khóa ngoại) |
| 4 | `approvedStatuses()` = `[3, 9, 10, 11]` → HĐ chờ duyệt vẫn lập được phụ lục / nghiệm thu / thanh lý, vẫn tính KPI |
| 5 | Quyền mới id **525**, `group = 'Hợp đồng'`, `type = 8`; **chỉ cần có quyền**, không xét phạm vi nhóm |
| 6 | Màn duyệt nằm trong **menu "Phê duyệt" phân hệ Hợp đồng** → `/contract/contract/approve-render-supply` |
| 7 | Duyệt được **cả 2 cách**: nhanh trên dòng danh sách, hoặc mở màn kết xuất xem rồi duyệt |
| 8 | Người lập có nút **"Thu hồi"** đưa HĐ ở 10 về 3 |
| 9 | Thông báo đủ 3 nhịp: gửi duyệt → người có quyền duyệt; duyệt / từ chối → người lập HĐ |

## Trong scope

- BE: 2 hằng + quyền (khai ở `PermissionsTableSeeder`, không migration), 1 migration cột `contracts`, 4 accessor, 3 service method + sửa `renderSupply()`, 3 route/action, resource, nhãn trạng thái
- FE: mục menu mới, màn `approve-render-supply.vue`, nới guard `_id/render.vue`, pill 10/11 ở 4 màn, 8 dropdown phụ lục, nút "Thu hồi"

## Ngoài scope

- Màn `supply/contract_render` và luồng phiếu đề xuất cung ứng — **không đụng tới**
- Không migration dữ liệu (chưa HĐ nào ở 10/11)
- Không đổi `canEdit()`, `canCreateSupplyProposal()`

## Bẫy đã biết

- Không thêm 10/11 vào `approvedStatuses()` + 8 dropdown phụ lục `status=3,9` → HĐ chờ duyệt **biến mất**
  khỏi màn lập phụ lục/nghiệm thu/thanh lý (đúng bẫy đã gặp khi thêm status 9).
- Phải **gán quyền 525 cho vai trò** ở màn Phân quyền, không thì HĐ kẹt ở trạng thái 10.
- File client dùng **CRLF** — script sửa file phải giữ nguyên.
