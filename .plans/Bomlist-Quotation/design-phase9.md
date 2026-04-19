# Design Phase 9: Làm giá + Phê duyệt giá BOM

## 1. Tổng quan

Sau khi BOM tổng hợp cấp giải pháp được duyệt (status=4), PM có thể yêu cầu xây dựng giá. User có quyền sẽ nhập Giá nhập + Giá bán cho từng sản phẩm, sau đó gửi duyệt. Hệ thống tự động tính cấp duyệt dựa trên cấu hình ngưỡng (giá trị đơn hàng + tỷ suất lợi nhuận).

## 2. Status flow

```
[Đã duyệt] (4)
  → PM click "Yêu cầu xây dựng giá"
  → [Chờ xây dựng giá] (7) + notify user có quyền build-price
  → User làm giá
    → Lưu nháp → [Đang xây dựng giá] (8)
    → Gửi duyệt → tính cấp:
      - Cấp 1 → popup tự duyệt → [Đã duyệt giá] (11)
      - Cấp 2 → [Chờ TP duyệt giá] (9) + notify TP
      - Cấp 3 → [Chờ BGĐ duyệt giá] (10) + notify BGĐ
  → TP/BGĐ duyệt → [Đã duyệt giá] (11) + notify người làm giá
  → TP/BGĐ từ chối → [Đang xây dựng giá] (8) + lý do + notify người làm giá
```

## 3. Cấp duyệt — Ma trận quyết định

### Công thức
- V = Tổng thành tiền bán = SUM(quoted_price × qty_needed)
- M = Tỷ suất lợi nhuận = ((Tổng bán - Tổng nhập) / Tổng nhập) × 100
- Final_Level = MAX(Level theo V, Level theo M)

### Bảng cấu hình mặc định

| Cấp | Giá trị đơn hàng (V) | Tỷ suất LN (M) | Người duyệt |
|-----|----------------------|-----------------|-------------|
| 1 | ≤ 1 tỷ | ≥ 20% | Người làm giá (tự duyệt) |
| 2 | 1 - 20 tỷ | 10 - 20% | Trưởng phòng |
| 3 | > 20 tỷ | < 10% | Ban giám đốc |

### Ma trận quyết định (V × M)

|  | M ≥ 20% (L1) | 10% ≤ M < 20% (L2) | M < 10% (L3) |
|--|--------------|--------------------|--------------| 
| V ≤ 1B (L1) | Cấp 1 — Tự duyệt | Cấp 2 — TP | Cấp 3 — BGĐ |
| 1B < V ≤ 20B (L2) | Cấp 2 — TP | Cấp 2 — TP | Cấp 3 — BGĐ |
| V > 20B (L3) | Cấp 3 — BGĐ | Cấp 3 — BGĐ | Cấp 3 — BGĐ |

## 4. Database

### Table: bom_price_approval_configs
| Column | Type | Note |
|--------|------|------|
| id | bigint PK | |
| type | enum('order_value','profit_margin') | |
| level | tinyint | 1/2/3 |
| min_value | decimal(15,2) nullable | Ngưỡng dưới |
| max_value | decimal(15,2) nullable | Ngưỡng trên (null = vô cực) |
| description | text nullable | |
| updated_by | bigint nullable | |
| timestamps | | |

### Table: bom_price_approval_config_logs
| Column | Type | Note |
|--------|------|------|
| id | bigint PK | |
| config_id | bigint FK | |
| old_value | json | |
| new_value | json | |
| changed_by | bigint | |
| created_at | timestamp | |

### Cột mới trên bom_lists
| Column | Type | Note |
|--------|------|------|
| price_requested_by | bigint nullable | PM yêu cầu XD giá |
| price_requested_at | timestamp nullable | |
| price_approved_by | bigint nullable | Người duyệt giá |
| price_approved_at | timestamp nullable | |
| price_rejected_reason | text nullable | Lý do từ chối |
| price_approval_level | tinyint nullable | Cấp duyệt (1/2/3) |

## 5. Permissions

| Tên quyền | Guard name | Mô tả |
|-----------|-----------|-------|
| Xây dựng giá Bom giải pháp | assign.bom-list.build-price | Truy cập màn làm giá, edit giá nhập/bán |
| Trưởng phòng duyệt giá Bom giải pháp | assign.bom-list.approve-price-tp | Duyệt/từ chối cấp TP |
| Ban giám đốc duyệt giá Bom giải pháp | assign.bom-list.approve-price-bgd | Duyệt/từ chối cấp BGĐ |

## 6. API Endpoints

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | /bom-price-approval-configs | Danh sách cấu hình |
| PUT | /bom-price-approval-configs/{id} | Cập nhật ngưỡng |
| GET | /bom-price-approval-configs/logs | Audit log |
| POST | /bom-lists/{id}/request-pricing | Yêu cầu XD giá |
| PUT | /bom-lists/{id}/save-pricing-draft | Lưu nháp giá |
| POST | /bom-lists/{id}/submit-pricing | Gửi duyệt giá |
| POST | /bom-lists/{id}/self-approve-pricing | Tự duyệt (cấp 1) |
| POST | /bom-lists/{id}/approve-pricing | Duyệt (TP/BGĐ) |
| POST | /bom-lists/{id}/reject-pricing | Từ chối (TP/BGĐ) |

## 7. UI Screens

### 7.1 Cấu hình duyệt giá (`/assign/config/price-approval`)
- Menu: Cấu hình chung → Cấu hình duyệt giá
- 2 bảng cấu hình (V + M), mỗi bảng 3 rows editable
- Audit log timeline bên dưới

### 7.2 Màn làm giá (`/assign/bom-list/:id/pricing`)
- Reuse BomBuilderEditor với prop `pricingMode=true`
- Chỉ unlock 2 cột: Giá nhập, Giá bán
- Footer: Tổng nhập | Tổng bán | Tỷ suất LN | Cấp duyệt dự kiến
- Buttons: Lưu nháp | Gửi duyệt

### 7.3 BOM chờ xây dựng giá (`/assign/bom-list/pending-pricing`)
- Menu: Phê duyệt → BOM chờ xây dựng giá
- Filter: status = 7, quyền: build-price
- Click row → redirect pricing

### 7.4 BOM chờ duyệt giá (`/assign/bom-list/pending-price-approval`)
- Menu: Phê duyệt → BOM chờ duyệt giá
- TP thấy status=9, BGĐ thấy status=9+10
- Click row → review (readonly) + Duyệt/Từ chối

## 8. Notification

| Event | Gửi cho | Message |
|-------|---------|---------|
| request_pricing | Users có quyền build-price | "BOM [code] cần xây dựng giá" |
| submit_pricing (cấp 2) | Users có quyền TP | "BOM [code] chờ Trưởng phòng duyệt giá" |
| submit_pricing (cấp 3) | Users có quyền BGĐ | "BOM [code] chờ Ban giám đốc duyệt giá" |
| approve_pricing | Người làm giá | "BOM [code] đã được duyệt giá" |
| reject_pricing | Người làm giá | "BOM [code] bị từ chối giá — [lý do]" |

Channel: database + broadcast (toast + chuông bell).

## 9. Bổ sung từ test (2026-04-13)

### 9.1 Lịch sử phê duyệt
- Table: `bom_pricing_histories` (action, from_status, to_status, approval_level, note, performed_by)
- Log tự động tại 6 methods: requestPricing, savePricingDraft, submitPricing, selfApprovePricing, approvePricing, rejectPricing
- API: GET /bom-lists/{id}/pricing-history
- FE: BomPricingHistoryModal — modal timeline, button ở 3 list pages + trang show

### 9.2 Cấu hình duyệt giá — logic tỷ suất LN
- Logic ngược: M cao → tự duyệt, M thấp → BGĐ
- Cấp 1,2: sửa "Từ" → auto "Đến" cấp dưới. Cấp 3: Từ=null (bao gồm âm)
- V2BaseCurrencyInput cho giá trị đơn hàng. Mô tả auto-generate

### 9.3 Quy đổi VNĐ
- BOM dùng tiền tệ khác → quy đổi V = totalSale × exchangeRate → so ngưỡng VNĐ
- M% không quy đổi (tỷ lệ). FE hiển thị "Quy đổi VNĐ:" khi rate ≠ 1

### 9.4 Màn show BOM — contextual buttons
- Status 4 + BOM tổng hợp GP: "Yêu cầu xây dựng giá"
- Status 9 + quyền TP: "Duyệt giá" + "Từ chối giá"
- Status 10 + quyền BGĐ: "Duyệt giá" + "Từ chối giá"
- Đã từng pricing: "Lịch sử phê duyệt"
- Luôn hiện: "Quay lại"

### 9.5 Business rules bổ sung
- Chỉ sửa BOM khi status = 1 (Đang tạo) hoặc 2 (Hoàn thành)
- Unique aggregate per version (không phải per giải pháp)
- Validate giá nhập/bán > 0 trước khi gửi duyệt
- Gửi duyệt: calculate → confirm → submit (không đổi status trước confirm)
