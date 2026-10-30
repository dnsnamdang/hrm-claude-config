---
name: app-new-model
description: Tạo model dữ liệu cho TPE_APP — freezed 3 (`@freezed abstract class`) + json_serializable với helper parse an toàn, hoặc class thường + fromJson phòng thủ cho model nhỏ, rồi make gen. Use when the user asks to "tạo model", "thêm model/entity từ API", "map JSON response", or "parse API data".
---

# Tạo Model (freezed + json_serializable) — TPE_APP

> Rà lại 29/10/2026 (skill gốc của TuJobs, 06/2026): mẫu cũ `@freezed class` là cú pháp freezed 2 — dự án đã lên
> freezed ^3.2 (commit d701f39) nên phải `@freezed abstract class`. Phần parse an toàn vẫn đúng, giữ nguyên.

**Chọn cách làm model:**
- Model lớn, dùng nhiều nơi, cần `copyWith` / so sánh → freezed theo mẫu dưới.
- Model nhỏ chỉ để hiển thị 1 màn (thẻ việc, dòng danh sách) → class thường + `factory fromJson` đọc phòng thủ,
  không cần build_runner — mẫu `WorkItem` (`data/lib/src/repository/source/remote/api/model/work_item.dart`).
- Chữ + màu trạng thái lấy nguyên từ BE (`status_text`, `status_color`), không thêm enum map số → chữ ở app.

Sinh model dữ liệu chuẩn dự án và chạy code gen. Models app-level nằm ở `app/lib/model/` hoặc trong `data` layer tùy phạm vi; entity nghiệp vụ thuần ở `app/lib/domain/lib/src/entity/`. Hỏi user vị trí nếu không rõ; mặc định cùng layer với nơi sẽ dùng.

## Thông tin cần hỏi
1. **Tên model** (PascalCase, VD: `PhieuMuon`).
2. **Các field**: tên + kiểu + nullable? + key JSON từ API (nếu khác camelCase).
3. **Có nested object / list không?** (cần helper parse an toàn).

## Template chuẩn
```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part '<snake>.freezed.dart';
part '<snake>.g.dart';

@freezed
abstract class <Name> with _$<Name> {   // freezed 3: BẮT BUỘC abstract (hoặc sealed)
  const factory <Name>({
    @JsonKey(name: 'ten_field_api') @Default('') String tenField,
    @JsonKey(name: 'so_luong') @Default(0) int soLuong,
    String? ghiChu,
    @JsonKey(name: 'items', fromJson: _itemsFromJson) @Default([]) List<ItemConModel> items,
  }) = _<Name>;

  factory <Name>.fromJson(Map<String, dynamic> json) => _$<Name>FromJson(json);

  factory <Name>.empty() => const <Name>();
}

// Bọc helper vì safeListFromJson nhận 3 tham số → @JsonKey.fromJson chỉ nhận hàm 1 tham số
List<ItemConModel>? _itemsFromJson(dynamic json) =>
    safeListFromJson(json, ItemConModel.fromJson, 'items');
```

## Quy tắc parse an toàn (rất quan trọng — API backend trả kiểu không nhất quán)
Các helper THẬT nằm ở `app/lib/data/lib/src/repository/source/remote/api/model/json_decode_helpers.dart` (import qua `package:app/data/lib/data.dart`). Chữ ký chính xác:
- `List<T>? safeListFromJson<T>(dynamic json, T Function(Map<String, dynamic>) fromMapJson, String parentField)`
- `List<ApiGalleryData>? galleryListFromJson(dynamic json, String parentField)`
- `Map<String, dynamic>? ensureMap(dynamic e, {String? parentField, int? index})`

Cả ba đều nhận ≥2 tham số nên KHÔNG dùng trực tiếp làm `fromJson:` — phải bọc trong hàm private 1 tham số (theo đúng pattern trong `api_object_data.dart`):
```dart
// Gallery / danh sách ảnh: API có thể trả String, Map, hoặc List → galleryListFromJson lo hết
List<ApiGalleryData>? _galleriesFromJson(dynamic json) =>
    galleryListFromJson(json, 'galleries_field');
// rồi: @JsonKey(name: 'galleries_field', fromJson: _galleriesFromJson) List<ApiGalleryData>? galleries,
```
- **List nested object** có thể null/sai kiểu → bọc `safeListFromJson<T>(json, T.fromJson, 'field')`.
- Số có thể về dạng String từ API → cân nhắc `@JsonKey(fromJson: ...)` ép kiểu, tránh `TypeError` runtime (xem `ai.md/FIX_STRING_TYPEERROR_SUMMARY.md`).
- Luôn cho field default (`@Default(...)`) hoặc nullable để `fromJson` không nổ khi thiếu key.

> Lưu ý: `app/lib/utils/gallery_parser.dart` (`GalleryParser.parseFromRoot`) là helper KHÁC, chuyên tách `constructions`/`handovers` thành `List<AppFile>` cho màn nhập kết quả — đừng nhầm với `galleryListFromJson` ở data layer.

## Bước cuối — BẮT BUỘC
```bash
make gen        # từ gốc repo TPE_APP (build_runner --delete-conflicting-outputs)
```
Sau đó `cd app && fvm dart analyze <file>` để chắc model hợp lệ. Agent chạy nền không chạy `make gen`.

## Lưu ý
- KHÔNG sửa tay file `*.freezed.dart` / `*.g.dart`.
- Nếu model dùng trong `domain` entity nhưng cần fromJson → đặt ở `data`/`model`, domain chỉ giữ entity thuần khi có thể.
- `withOpacity` deprecated nếu model có màu → dùng `Color.withValues(alpha: ...)`.
