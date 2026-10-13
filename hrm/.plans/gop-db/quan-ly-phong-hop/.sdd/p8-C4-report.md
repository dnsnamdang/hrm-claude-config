# Phase 8, lượt C4 — báo cáo

Sửa 2 lỗi bố cục nút ở footer popup phiếu đặt phòng.

File: `pages/meeting/bookings/components/BookingFormModal.vue`, khối `<template #footer>`
(dòng ~847-950).

## Việc 1 — Gom nhóm nút

Đọc `.claude/skills/button-convention/SKILL.md` mục 5 (thứ tự nút trong modal footer: action
chính → action phụ → nguy hiểm → reset/phụ trợ → thoát cuối cùng). Skill này viết cho trường hợp
1 nhóm hành động; footer của màn này có **2 domain hành động độc lập** (PHIẾU: Duyệt/Từ chối/Hủy
phiếu và DỊCH VỤ: Đã chuẩn bị dịch vụ/Từ chối dịch vụ) nên skill không có mục riêng cho việc gom
domain. Cách xử lý: áp nguyên tắc "action chính trước, nguy hiểm sau" của skill **cho từng domain
riêng**, rồi 2 domain nối tiếp nhau, "Đóng" luôn cuối cùng — đúng khớp với thứ tự đề xuất trong
brief nên **không có lệch cần confirm lại**.

Thứ tự nút sau khi sửa (điều kiện `v-if` giữ nguyên 100%, không đổi chữ nút):

```
Duyệt · Từ chối · Hủy phiếu · Đã chuẩn bị dịch vụ · Từ chối dịch vụ · Đóng
└──────── nhóm PHIẾU ────────┘ └──── nhóm DỊCH VỤ ────┘
```

Đoạn `<template #footer>` sau khi sửa (rút gọn comment dài, giữ nguyên logic):

```vue
<template #footer>
    <template v-if="isShow">
        <!-- Nhóm PHIẾU: Duyệt → Từ chối → Hủy phiếu -->
        <V2BaseButton v-if="viewDetail && viewDetail.is_can_approve" primary size="sm" class="mb-2"
            @click="$emit('approve', viewDetail)">
            <template #prefix><i class="ri-check-line" style="font-size: 15px"></i></template>
            Duyệt
        </V2BaseButton>
        <V2BaseButton v-if="viewDetail && viewDetail.is_can_reject" primary status="danger" size="sm" class="mb-2"
            @click="$emit('reject', viewDetail)">
            <template #prefix><i class="ri-close-circle-line" style="font-size: 15px"></i></template>
            Từ chối
        </V2BaseButton>
        <V2BaseButton v-if="viewDetail && viewDetail.is_can_cancel" primary status="danger" size="sm" class="mb-2"
            @click="$emit('cancel', viewDetail)">
            <template #prefix><i class="ri-forbid-line" style="font-size: 15px"></i></template>
            Hủy phiếu
        </V2BaseButton>
        <!-- Nhóm DỊCH VỤ: Đã chuẩn bị dịch vụ → Từ chối dịch vụ -->
        <V2BaseButton v-if="viewDetail && viewDetail.is_can_handle_service" primary size="sm" class="mb-2"
            data-testid="booking-service-prepared-button" @click="$emit('service-prepared', viewDetail)">
            <template #prefix><i class="ri-check-line" style="font-size: 15px"></i></template>
            Đã chuẩn bị dịch vụ
        </V2BaseButton>
        <V2BaseButton v-if="viewDetail && viewDetail.is_can_handle_service" primary status="danger" size="sm" class="mb-2"
            data-testid="booking-service-rejected-button" @click="$emit('service-rejected', viewDetail)">
            <template #prefix><i class="ri-close-circle-line" style="font-size: 15px"></i></template>
            Từ chối dịch vụ
        </V2BaseButton>
    </template>
    <!-- Chế độ Thêm/Sửa: nút Lưu -->
    <V2BaseButton v-else primary size="sm" class="mb-2" :interactable="!isSubmitSave"
        data-testid="booking-save-button" @click="submitSave">
        <template #prefix><i :class="needsApproval ? 'ri-send-plane-line' : 'ri-save-3-line'" style="font-size: 15px"></i></template>
        {{ saveButtonText }}
    </V2BaseButton>
    <V2BaseButton tertiary size="sm" class="mb-2" @click="closeModal">
        <template #prefix><i class="fas fa-arrow-left" style="margin-right: 3px"></i></template>
        Đóng
    </V2BaseButton>
</template>
```

## Việc 2 — Về đúng khoảng cách 8px

Bỏ `mr-2` khỏi **toàn bộ 6 nút** trong `<template #footer>` của file này (Duyệt, Từ chối,
Hủy phiếu, Đã chuẩn bị dịch vụ, Từ chối dịch vụ, nút Lưu ở nhánh `v-else`) — mỗi nút chỉ còn
`class="mb-2"`. Nút Đóng vốn đã chỉ có `mb-2`, không đổi. Không đụng gì tới các cụm nút khác
trong file (toolbar/thân form không có — file này chỉ có 1 `<template #footer>`).

`grep -n "mr-2" pages/meeting/bookings/components/BookingFormModal.vue`:

```
944:            <!-- Phase 8, lượt C4 — bỏ `mr-2` khỏi TOÀN BỘ nút trong footer này (kể cả các nút
```

Dòng duy nhất còn chứa chữ `mr-2` là **comment giải thích** (không phải class trên nút), mô tả lý
do đã bỏ `mr-2`. Không còn dòng `class="...mr-2..."` nào trong file — thỏa yêu cầu "KHÔNG còn dòng
nào thuộc footer".

## Compile kiểm tra cú pháp

Dùng `vue-template-compiler` (resolve từ `node_modules` của chính `hrm-client`, không phải bản
global) để compile khối `<template>...</template>` của file:

```
node -e "... compiler.compile(template, {outputSourceRange:true}) ..."
→ OK - no compile errors
```

## Điểm nghi ngờ / lưu ý cho người điều phối

- Chưa đo lại bằng Playwright theo yêu cầu CLAUDE.md gốc (task này cấm tự mở trình duyệt vì chỉ có
  1 trình duyệt dùng chung) — người điều phối cần tự đo lại: (1) khoảng cách 2 nút liền nhau còn
  8px như 73 file kia, (2) thứ tự hiển thị đúng `Duyệt · Từ chối · Hủy phiếu · Đã chuẩn bị dịch vụ
  · Từ chối dịch vụ · Đóng`, (3) nút Lưu (chế độ Thêm/Sửa) cũng cách Đóng 8px thay vì 16px trước đó.
- Việc 2 mở rộng sang nút Lưu (nhánh Thêm/Sửa) dù brief chỉ nêu tên "Duyệt/Từ chối/Hủy phiếu/Đóng"
  — làm vậy để đúng tinh thần "cả footer đều đặn 8px" (mục tiêu ghi rõ trong đầu bài Việc 2). Nếu
  người điều phối muốn giữ nguyên nút Lưu như cũ (không thuộc phạm vi đo đạc), cần revert riêng
  dòng đó.
- Không chạy e2e (theo memory "Không tự chạy e2e mỗi task" + ràng buộc "không dùng Playwright" của
  task này). Spec e2e của màn `meeting/bookings` (nếu có) nên được cập nhật để khớp thứ tự nút mới
  — chưa rà trong phạm vi lượt này.
