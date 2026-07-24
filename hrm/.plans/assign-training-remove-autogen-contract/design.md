# Design — Bỏ luồng tự sinh HĐ đào tạo từ QĐ cử đi đào tạo

@manhcuong · Spec chi tiết: `docs/superpowers/specs/2026-07-15-assign-training-remove-autogen-contract-design.md`

## Mục tiêu

Duyệt QĐ cử đi đào tạo (`/decision/assign-training`) KHÔNG còn tự động sinh HĐ đào tạo cho từng học viên nữa. HĐĐT do người dùng lập tay.

## Hiện trạng trước khi sửa

```
toggleApprove(status=5)
  └─ AssignTrainingService::autogenousTrainingContract()
       └─ foreach học viên: CreateTrainingContractJob::dispatch()
            └─ TrainingContract::create(status=Đã duyệt)
               + assign_training_students.training_contract_status = 2
```

## Phát hiện quyết định cách làm

**Luồng lập tay ĐÃ tồn tại đầy đủ, chỉ đang bị luồng tự sinh che mất.** `StudentModal.vue:72` có nút "Tạo HĐĐT" với điều kiện `training_contract_status == 1 && assignTrainingStatus == 5` → trỏ sang `/decision/category/training-contract/add`. Nhưng tự sinh set cờ = 2 ngay khi duyệt, nên điều kiện `cờ == 1 && QĐ == 5` **không bao giờ đúng** → nút là code chết.

Data thật xác nhận: 4/4 học viên trên QĐ đã duyệt đều cờ = 2, đúng 4 HĐĐT trong DB.

→ Gỡ tự sinh không tạo lỗ hổng, mà **làm sống lại** luồng tay đã dựng sẵn. Không cần viết mới gì ở FE.

## Thay đổi

| File | Việc |
|---|---|
| `AssignTrainingController::toggleApprove()` | bỏ khối gọi `autogenousTrainingContract()` |
| `AssignTrainingService` | xoá method `autogenousTrainingContract()` + 2 import thành thừa |
| `Jobs/CreateTrainingContractJob.php` | **xoá file** (0 tham chiếu, 0 job trong queue) |
| `PrintTemplate::PROTECTED_CODES` | giữ `HOP_DONG_DAO_TAO`, sửa comment trỏ Job đã xoá |
| `composer dump-autoload` | classmap còn trỏ file đã xoá → phải nạp lại |

**KHÔNG đụng**: 4 HĐĐT đã tự sinh (dữ liệu thật đã duyệt — chỉ dừng sinh mới); cờ `training_contract_status` (luồng tay tự set: store→2, destroy→1); toàn bộ FE.

## Ảnh hưởng tới tính năng "Tiến trình"

Trước: duyệt xong → tự sinh đủ HĐĐT → Tiến trình nhảy thẳng **"Đã hoàn thành"**, 2 trạng thái kia gần như không xuất hiện.
Sau: duyệt xong → **"Chưa tạo"** → lập tay dần → "Chưa hoàn thành" → "Đã hoàn thành". Cột Tiến trình giờ mới thực sự có ý nghĩa theo dõi.

## Verify

Runtime (transaction + rollback) trên QĐ 3 học viên: 6/6 PASS — không sinh HĐĐT, cờ giữ 1, Tiến trình "Chưa tạo", nút đủ điều kiện hiện, class Job biến mất, 0 job vào queue.

Browser thật: QĐ "Đã duyệt" mà Tiến trình vẫn "Chưa tạo"; popup học viên hiện nút "Tạo HĐĐT" ở cả 3 dòng (`nut-tao-hddt.png`). Data khôi phục nguyên trạng sau test.
