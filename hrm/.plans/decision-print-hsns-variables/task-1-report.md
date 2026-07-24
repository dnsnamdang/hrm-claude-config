# Task 1 — Bổ sung biến mẫu in HSNS cho các loại quyết định

## STATUS: DONE

## File sửa
`Modules/Human/Entities/PrintTemplateVariable.php` (file duy nhất)

## Số dòng thêm mỗi block

### Nhóm A + B (13 biến HSNS + 2 biến CAP_BAC = 15 dòng)
| Block | Dòng thêm | Biến bỏ vì trùng |
| --- | --- | --- |
| `Decision::TYPE_APPOINT_PERSONNEL` | 15 (13 A + 2 B) | không |
| `Decision::TYPE_TRANSFER_PERSONNEL` | 15 (13 A + 2 B) | không |
| `Decision::TYPE_SALARY_CHANGE` | 15 (13 A + 2 B) | không |

### Nhóm A only (13 dòng)
| Block | Dòng thêm | Biến bỏ vì trùng |
| --- | --- | --- |
| `Decision::TYPE_RETIREMENT` | 13 | không |
| `Decision::TYPE_EMPLOYEE_DISCIPLINE` | 13 | không (block đã có `TRINH_DO` khác `TRINH_DO_HOC_VAN` nên vẫn thêm `TRINH_DO_HOC_VAN`) |

### Nhóm C (9 dòng)
| Block | Dòng thêm | Biến bỏ vì trùng |
| --- | --- | --- |
| `Decision::TYPE_TERMINATION_LABOR_CONTRACT` | 9 | không (đã có sẵn NGAY_SINH, NOI_CU_TRU, CCCD, TRINH_DO_HOC_VAN → không thêm lại) |
| `Decision::TYPE_SUSPEND_LABOR_CONTRACT` | 9 | không (đã có sẵn NGAY_SINH, NOI_CU_TRU, CCCD, TRINH_DO, TRINH_DO_HOC_VAN; GIOI_TINH audit CHƯA có → vẫn thêm) |

### Nhóm D (1 dòng)
| Block | Dòng thêm |
| --- | --- |
| `LABOR_CONTRACT_COMMON_VARIABLES` | 1 (`THOI_GIAN_HDLD_HIEN_TAI`) |

**Tổng: 15×3 + 13×2 + 9×2 + 1 = 45 + 26 + 18 + 1 = 90 dòng.** Không có dòng nào bị bỏ vì trùng.

## Verify

### 1. php -l
```
No syntax errors detected in Modules/Human/Entities/PrintTemplateVariable.php
```

### 2. tinker
```
APPOINT nsCHU gt cb qq
SUSPEND ncSO hdCHU bare_NGAY_CAP_CMTND=hidden
HDLD hdSO
```
Khớp 100% kỳ vọng: `APPOINT nsCHU gt cb qq`, `SUSPEND ncSO hdCHU bare_NGAY_CAP_CMTND=hidden`, `HDLD hdSO`.

Xác nhận: biến `is_date` (NGAY_SINH, NGAY_CAP_CMTND, THOI_GIAN_HDLD_HIEN_TAI) được `expandDateVariables` tự sinh `_CHU`/`_SO` và ẩn biến gốc trong picker (bare_NGAY_CAP_CMTND=hidden).

## Concern
Không có. Chỉ sửa metadata, không đụng value-fill/logic. Không commit git.
