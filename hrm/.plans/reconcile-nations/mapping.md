# Bảng map reconcile nations (bỏ hrm_nations) — chờ user duyệt

Đích: mọi nation_id dùng chung id-space bảng `nations` (32 nước).
nations tham chiếu: 1-4=VN, 5=China, 7=Korea, 8=Japan, 9=India, 10=Germany,
12=Taiwan, 14=Singapore, 22=Portugal, 23=Saudi Arabia, 24=Laos, 27=Indonesia.

## NHÓM 1 — CUSTOMERS cần ĐỔI (6, chắc chắn — sai nước)
| id | Tên KH | nid cũ | → nid mới | Nước đúng |
|----|--------|--------|-----------|-----------|
| 4549  | HIROSHIMA MAZDA              | 2 | **8**  | Japan |
| 5757  | ...LAO SCITEC               | 3 | **24** | Laos |
| 17482 | LANEXANG (PREMIUM AUTO)     | 3 | **24** | Laos |
| 14170 | PT. PIAGGIO INDONESIA       | 4 | **27** | Indonesia |
| 17207 | TENGZHOU DINGRUN (TQ)       | 7 | **5**  | China |
| 17515 | BUHLER (CHINA)              | 7 | **5**  | China |

## NHÓM 2 — CẦN BẠN QUYẾT (3, mơ hồ)
| id | Tên KH | nid hiện | Vấn đề | Đề xuất |
|----|--------|----------|--------|---------|
| 16676 | THE IMAGING SOURCE ASIA CO   | 10 (Germany) | Hãng Đức, VP châu Á (Đài Loan?) | giữ 10 (Germany) hoặc 12 (Taiwan)? |
| 16677 | ELTRONSPOLKA ZOO SP.K       | 14 (Singapore) | Ba Lan — **nations KHÔNG có Ba Lan** | thêm "Poland" vào nations rồi trỏ, hay giữ tạm? |
| 42154 | MR TRƯƠNG HẠNH              | 24 (Laos) | Tên VN, id Laos | giữ 24 (Laos) hay đổi 1 (VN)? |

## NHÓM 3 — GIỮ NGUYÊN (đã đúng nations-space, không đụng)
- customers (8): 40998,41077 (China 5); 31832,34435,36017 (India 9); 31072,34173 (Saudi 23); 35431 (Indonesia 27)
- provinces (11): 68/70/73=China5, 67=Korea7, 66/69=India9, 64=Portugal22, 65=Saudi23, 74=Laos24, 71/72=Indonesia27
- delivery_places (8): 20607/22598/34844=India9, 22228=Saudi23, 31839/36152=Laos24, 24060/29217=Indonesia27
- customers nid=1 (VN): 43.041 + null 462 → giữ nguyên

## ✅ ĐÃ THỰC HIỆN (erp_hrm_check + code gop_db, chưa commit)
- Data: thêm Poland = nations id **33**; remap 6 KH nhóm 1 + KH 16677→33 (Poland).
  16676 giữ Germany(10), 42154 giữ Laos(24) theo user chốt.
- Code: Nation model `$table`=nations + alias `code`↔`country_code` + bỏ sync TpNation;
  NationService→nations; CreateNationRequest unique→nations/country_code;
  Assign customer request `exists:nations,id`.
- Bảng: `hrm_nations` → RENAME `hrm_nations_bak` (backup, có thể DROP hẳn sau).
- Verify: Nation model đọc nations OK, getNations=33/getList=30, KH join nations đúng, không còn lỗi/tham chiếu hrm_nations.

## Sau khi duyệt data → bước code
- Nation model `$table`='nations', `code`→`country_code`, gỡ sync TpNation
- NationService (3 dòng) hrm_nations→nations
- 8 validation exists/unique:hrm_nations → nations
- Drop bảng hrm_nations

### Checkpoint — 2026-08-04
Vừa hoàn thành: bỏ hrm_nations (code Nation model→nations + alias code/country_code, 8 validation, seeder ReconcileNationsSeeder DROP hrm_nations); data reconcile 7 KH + Poland; local đã DROP; push gop_db.
Bước tiếp: chạy seeder trên server test (đọc dòng canh bao KH mo ho server-specific); DROP hrm_nations sau verify.
Blocked:
