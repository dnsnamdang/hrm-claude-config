# Khảo sát — THU THẬP THÔNG TIN DỰ ÁN (Phiếu thu thập thông tin)

> KHÔNG phải màn danh mục độc lập. Là **tab bên trong màn chi tiết dự án tiền khả thi**.

## 0. Bức tranh tổng thể
```
Danh mục "Ngân hàng câu hỏi khảo sát"  →  Danh mục "Phiếu thu thập thông tin" (mẫu phiếu, gắn 1 Ứng dụng)
      (/assign/questions)                         (/assign/form-templates)
                                                            │ Published
                                                            ▼
Tạo/Sửa Dự án TKT, chọn trường "Ứng dụng"  →  BE tự CLONE mẫu phiếu thành SNAPSHOT riêng của dự án
                                                            ▼
        Màn chi tiết dự án → tab "Thu thập thông tin" → nhập đáp án → "Lưu phiếu"
                                                            ▼
 Gate: Gửi "Yêu cầu làm giải pháp" / Tạo "Giải pháp" bị CHẶN nếu còn câu hỏi bắt buộc chưa trả lời
```

## 1. Biểu mẫu định nghĩa ở đâu & gắn vào dự án thế nào

### 1.1 Hai danh mục nguồn
| Menu | Đường dẫn | Quyền để thấy menu |
|---|---|---|
| **Ngân hàng câu hỏi khảo sát** | `/assign/questions` | `Quản lý danh mục câu hỏi khảo sát` hoặc `Xem danh mục câu hỏi khảo sát` |
| **Phiếu thu thập thông tin** | `/assign/form-templates` | `Quản lý danh mục mẫu phiếu thu thập thông tin` |

- `/assign/questions`: khai báo từng câu hỏi (nội dung, **Loại dữ liệu**, đáp án kèm theo, phạm vi áp dụng `Tất cả` / `Theo ứng dụng`, trạng thái `Hoạt động`/`Khóa`).
- `/assign/form-templates`: danh sách **"Danh sách mẫu phiếu"**, nút **"Tạo mẫu phiếu"**, **"Xuất Excel"**, panel **"Bộ lọc danh sách mẫu phiếu"** (Ứng dụng / Trạng thái / Người tạo / Người cập nhật / Cập nhật từ – đến).
- Mẫu phiếu gồm **Section (A, B, C…) → Group (I, II, III…) → Câu hỏi (1, 2, 3…) → Câu hỏi con (3.1, 3.2…)**, dựng bằng `FormBuilder.vue` / `SectionBuilder.vue`, kéo câu hỏi từ `QuestionLibrary.vue`.
- Trạng thái mẫu phiếu: 1 = Nháp, 2 = **Published**, 3 = Khóa. **Mỗi Ứng dụng chỉ được 1 mẫu Published.**

### 1.2 Gắn vào dự án — KHÔNG có thao tác "chọn phiếu"
| Bước | Nơi thao tác | Chi tiết |
|---|---|---|
| 1 | Form dự án TKT, dưới "Tên dự án TKT" | Nhãn **"Ứng dụng"** (*), `V2BaseSelect`, placeholder **"Chọn ứng dụng"** |
| 2 | – | Danh sách Ứng dụng lọc theo **Loại hình + Lĩnh vực của Khách hàng cuối** (`assign/applications/for-selection`). Không có → cảnh báo vàng **"Hãy liên hệ với bộ phận quản lý để yêu cầu khởi tạo ứng dụng phù hợp"** |
| 3 | Icon 📄 cạnh nhãn "Ứng dụng" | Chỉ hiện khi đã chọn Ứng dụng. Tooltip: **"Xem chi tiết mẫu phiếu thu thập thông tin"** (xanh, mở tab `/assign/form-templates/{id}`) hoặc **"Chưa cấu hình mẫu phiếu thu thập thông tin cho ứng dụng này"** (xám) |
| 4 | Lưu dự án (Tạo hoặc Sửa) | BE gọi `handleFormTemplateSnapshot()` |
| 5 | – | BE tìm `FormTemplate::where('application_id',..)->where('status', PUBLISHED)->first()`. **Tiêu chí duy nhất = Ứng dụng + Published.** Không dùng Lĩnh vực/Ngành/Giai đoạn |
| 6 | – | Chưa có snapshot → clone sâu section/group/question/option sang các bảng `form_*_snapshots`, ghi `prospective_projects.form_template_snapshot_id`, ghi lịch sử `create` |

**Lưu ý nghiệp vụ:**
- Không chọn Ứng dụng ⇒ **không có phiếu**.
- Đã snapshot thì **sửa mẫu phiếu gốc không ảnh hưởng** dự án.
- **Đổi Ứng dụng ⇒ sinh snapshot MỚI**, đáp án cũ mồ côi, không chuyển sang được.
- Snapshot còn được tạo từ **Biên bản họp** nếu dự án chưa có.

## 2. Vị trí tab
| Mục | Giá trị |
|---|---|
| File | `pages/assign/prospective-projects/_id/manager.vue` |
| Tên tab | **"Thu thập thông tin"** (icon `ri-clipboard-line`) |
| Vị trí | **Tab CUỐI CÙNG**: Dự án → Yêu cầu → Giải pháp → Task → Issue → Meetings → Files → Hồ sơ → Báo giá → **Thu thập thông tin** |
| Điều kiện hiển thị | Luôn hiện với dự án thường. **Ẩn khi dự án là DỰ ÁN CHA** (chỉ 3 tab: Thông tin chung / Dự án con / Meetings). Không phụ thuộc trạng thái, **không kiểm tra quyền** |
| Props | `:disabled="true"`, `:is-add-form="false"`, `:is-show-save-button="false"` |

> ⚠️ Prop `disabled` khai báo nhưng **không dùng** trong component → ô nhập trên tab **luôn cho phép sửa**, kể cả dự án đã đóng.

Cùng component `FormTabInput` còn xuất hiện ở: màn **Yêu cầu làm giải pháp** tab **"Phiếu thu thập thông tin"** (chỉ khi người dùng là người tiếp nhận `canReceive`); màn **Biên bản họp**.

## 3. Bố cục tab
| Vùng | Nội dung |
|---|---|
| Thanh nút trên cùng (phải) | **"Lịch sử thay đổi"** · **"Lưu phiếu"** · **"Xem mẫu in"** — chỉ khi đã tải được phiếu |
| Empty state | **"Chưa có phiếu thu thập thông tin cho dự án này"** + icon clipboard |
| Loading | **"Đang tải phiếu thu thập thông tin..."** |
| Thẻ phiếu | Header xám ghi **tên mẫu phiếu**; góc phải hiện Người tạo / Ngày tạo nếu có |
| Mục **"1. Thông tin chọn"** | 1 ô: nhãn **"Ứng dụng"** (*), `V2BaseInput` **disabled**, điền sẵn tên ứng dụng của dự án |
| Thân phiếu | Section **A, B, C…** → Group **I, II, III…** → câu hỏi **1, 2, 3…** → câu hỏi con **3.1, 3.2…** |
| Section "Thông tin bổ sung" | Section có cờ `is_addition` — câu hỏi do bộ phận giải pháp yêu cầu bổ sung; mỗi câu là textarea **"Nhập câu trả lời..."** |
| Nút dưới cùng | **"Lưu phiếu"** lặp lại ở cuối phiếu |

### 3.2 Loại câu hỏi
| Nhãn trong danh mục | data_type | type render | Control | Cách nhập |
|---|---|---|---|---|
| Text ngắn | short_text | text | V2BaseInput | placeholder **"Nhập..."** |
| Text dài | long_text | textarea | V2BaseTextarea 3 dòng | **"Nhập chi tiết..."** |
| Số | number | number | V2BaseInput inputmode decimal | định dạng số VN (chấm ngăn nghìn, phẩy thập phân) |
| Ngày | date | date | V2BaseDatePicker | **"Chọn ngày..."** |
| Có / Không | yes_no | boolean | V2BaseRadio boolean | Chọn Có/Không |
| Radio 1 lựa chọn | radio | radio | V2BaseRadio (dọc) | Chọn 1 |
| Checkbox nhiều lựa chọn | checkbox | checkbox | V2BaseCheckbox | Chọn nhiều (mảng) |
| Dropdown | dropdown | select | V2BaseSelect | Chọn 1 |
| File | file | file | V2BaseFile | **"Chọn tệp..."**, multiple, auto-upload |
| Nhóm câu hỏi | hierarchy | parent | – | Khung chứa **câu hỏi con** thụt lề. Rỗng: **"Chưa có câu hỏi con nào."** |

**Không hỗ trợ loại "bảng"/grid.**

### 3.3 Ô "Ghi chú" đi kèm
Mọi câu hỏi **không phải** text/textarea/parent đều có dòng nhỏ **"Ghi chú"** + icon bút; bấm mở textarea 2 dòng, placeholder **"Nhập ghi chú (nếu có)..."**. Lưu dưới khoá riêng `{localId}_note`. Blur hoặc Enter thu gọn lại. Câu hỏi con cũng có.

## 4. Bảng từng thành phần
| Nhãn / thành phần | Control | Bắt buộc | Mặc định | Ẩn/hiện/readonly |
|---|---|---|---|---|
| Tên mẫu phiếu (header thẻ) | text | – | tên snapshot | khi có phiếu |
| Người tạo / Ngày tạo | text | – | trống ở tab dự án | khi có dữ liệu |
| **Ứng dụng** (mục "1. Thông tin chọn") | V2BaseInput | có `*` | tên ứng dụng của dự án | **Readonly (disabled)** |
| Tiêu đề Section | text | – | từ snapshot; trống → **"Chưa đặt tiêu đề Section"** | – |
| Mô tả Section / Group | text nhỏ | – | từ snapshot | khi có mô tả |
| Nội dung câu hỏi | text + `*` đỏ nếu required | cờ `required` | trống → **"Chưa đặt nội dung câu hỏi"** | ẩn nếu điều kiện `visibility` không thoả |
| Ô trả lời | theo bảng 3.2 | không chặn khi lưu | giá trị đã lưu | không bao giờ readonly |
| **Ghi chú** | textarea 2 dòng | không | trống | chỉ với loại ≠ text/textarea/parent |
| Câu hỏi trong "Thông tin bổ sung" | textarea 2 dòng, **"Nhập câu trả lời..."** | không | đáp án đã lưu | khi snapshot có section `is_addition` |
| Nút **"Thêm câu hỏi"** / **"Yêu cầu bổ sung"** | Button + Input | – | – | **Ẩn ở tab dự án TKT** (`is-add-form=false`); chỉ hiện ở màn Yêu cầu làm giải pháp khi là người tiếp nhận |

**Điều kiện ẩn/hiện câu hỏi (`visibility`)**: có thể cấu hình "chỉ hiện nếu câu hỏi X có giá trị ==/!=/>/</>=/<= Y". Loại `parent` luôn hiện. Không tìm thấy câu hỏi phụ thuộc → vẫn hiện.

## 5. Các nút
| Nút | Vị trí | Điều kiện | API | Kết quả / Toast |
|---|---|---|---|---|
| **"Lịch sử thay đổi"** | thanh trên | khi có phiếu | `GET assign/prospective-projects/{id}/form-answer-histories` | Mở popup lịch sử. Lỗi → **"Lỗi khi tải lịch sử"** |
| **"Lưu phiếu"** | thanh trên **và** cuối phiếu | trên: khi có phiếu; dưới: khi có phiếu và `isAddForm=false` | `POST assign/prospective-projects/{id}/save-form-answers` | Thành công → **"Lưu phiếu thu thập thông tin thành công"**, tự tải lại snapshot. Lỗi → **"Có lỗi xảy ra khi lưu phiếu thu thập thông tin"**. Thiếu id → **"Không tìm thấy ID dự án"**; chưa có snapshot → **"Dự án chưa có snapshot của phiếu"** |
| **"Xem mẫu in"** | thanh trên | khi có phiếu | – | Mở modal **"Xem mẫu in phiếu thu thập thông tin"** |
| **"In"** (trong modal) | footer modal | luôn | – | Mở cửa sổ in. Chưa tải xong → **"Chưa tải xong phiếu thu thập thông tin"**; chặn popup → **"Không thể mở cửa sổ in. Vui lòng cho phép popup."** |
| **"Đóng"** | footer modal | luôn | – | đóng |
| **"Thêm câu hỏi"/"Thêm"/"Hủy"/"Yêu cầu bổ sung"** | section Thông tin bổ sung | **Không hiện ở tab dự án TKT** | `POST assign/form-templates/snapshot/{snapshotId}/additional-questions` | **"Đã lưu yêu cầu bổ sung câu hỏi thành công!"**; lỗi → **"Có lỗi xảy ra khi gửi yêu cầu bổ sung!"**. BE chuyển YC làm GP sang **"Yêu cầu bổ sung"** + gửi thông báo |

**KHÔNG có nút "Lưu nháp", "Gửi", "Sửa", "Chốt"** — chỉ một hành động lưu duy nhất, **sửa lại được không giới hạn**.

**Mẫu in:** tiêu đề **"PHIẾU THU THẬP THÔNG TIN DỰ ÁN"**, header letterhead công ty, khối: Tên khách hàng / Tên dự án / Mã dự án / Ứng dụng / Ngày khảo sát / Người khảo sát; bảng **"NỘI DUNG KHẢO SÁT"** 5 cột **STT | NỘI DUNG | LOẠI CÂU HỎI | GIÁ TRỊ LỰA CHỌN ĐI KÈM | ĐÁP ÁN / GIÁ TRỊ THU THẬP**. *Ghi chú: `Ngày khảo sát` luôn trống vì không truyền `surveyDate`.*

## 6. Lịch sử trả lời (FormAnswerHistoryModal)
Mở bằng nút **"Lịch sử thay đổi"**. Tiêu đề **"Lịch sử thay đổi phiếu thu thập thông tin"**. Trống → **"Chưa có lịch sử thay đổi nào."** Footer 1 nút **"Đóng"**.
Dạng **timeline dọc** (không phải bảng):
| Thành phần | Nội dung |
|---|---|
| Chấm màu | Xanh lá = tạo phiếu, hổ phách = cập nhật đáp án, xanh dương = bổ sung câu hỏi |
| Thời điểm | `dd/mm/yyyy HH:ii` |
| Hành động | **"Tạo mới phiếu thu thập thông tin"** / **"Cập nhật câu trả lời"** / **"Yêu cầu bổ sung câu hỏi"** |
| Người thực hiện | `— {tên nhân viên}` |
| Chi tiết (Cập nhật) | **Nhãn câu hỏi: giá trị cũ (đỏ) → giá trị mới (xanh)**; rỗng hiển thị **"(trống)"** |
| Chi tiết (Bổ sung) | Danh sách câu hỏi được thêm, dấu ➕ |

Nguồn: bảng `form_answer_histories`, ghi tự động ở 3 điểm `create` / `update_answers` / `add_questions`. Không phân trang, mới nhất trước.

## 7. Dữ liệu đi đâu (downstream)
Lưu ở `form_answers` + `form_answer_details`. Mỗi lần lưu **xoá sạch chi tiết cũ rồi ghi lại**.

| Ai đọc | Dùng để làm gì |
|---|---|
| Chi tiết dự án TKT | Trả `answers` + `form_template_snapshot_id` để tab render lại |
| Danh sách dự án TKT | Cờ `is_form_complete` — phiếu đã đủ trường bắt buộc chưa |
| **Yêu cầu làm giải pháp** ⭐ | **CHẶN gửi yêu cầu** nếu còn câu hỏi `required` chưa trả lời — HTTP 423 **"Phiếu thu thập thông tin chưa đủ các trường yêu cầu"** |
| **Tạo Giải pháp** ⭐ | Chặn tạo giải pháp khi phiếu chưa đủ trường bắt buộc |
| Yêu cầu bổ sung câu hỏi | Bộ phận GP thêm câu hỏi → YC làm GP chuyển **"Yêu cầu bổ sung"** + thông báo cho Sale |
| Biên bản họp | Cho nhập/xem chính phiếu này ngay trong biên bản họp dự án |
| In phiếu | Xuất bản in "PHIẾU THU THẬP THÔNG TIN DỰ ÁN" kèm đáp án |

**KHÔNG có** service nào của Báo giá, BOM, Hàng hoá dự án, Hợp đồng đọc đáp án phiếu.

**Kết luận cho HDSD:**
- **Thu thập để làm gì:** ghi nhận yêu cầu/hiện trạng kỹ thuật của khách hàng làm đầu vào cho bộ phận giải pháp.
- **Ai đọc:** người làm giải pháp, người dự họp, và hệ thống dùng kiểm tra tính đầy đủ.
- **Chốt thời điểm nào:** không có bước "chốt/khoá". Điểm kiểm soát duy nhất là **lúc gửi YC làm giải pháp / tạo Giải pháp**.
- **Sửa lại được không:** **Có**, bất cứ lúc nào, mọi thay đổi ghi vào Lịch sử. Nếu xoá hết đáp án (payload rỗng) thì hệ thống **không lưu** — không xoá trắng được.

## 8. Phân quyền
| Nơi | Quyền |
|---|---|
| Toàn bộ thao tác danh mục mẫu phiếu | **`Quản lý danh mục mẫu phiếu thu thập thông tin`** (id 1013) |
| Xem danh mục câu hỏi khảo sát | **`Xem danh mục câu hỏi khảo sát`** (id 997) |
| Thao tác danh mục câu hỏi | **`Quản lý danh mục câu hỏi khảo sát`** (id 982) |
| **Tab "Thu thập thông tin" trong dự án** | **KHÔNG có quyền riêng nào.** Route `save-form-answers`, `form-answer-histories`, `form-templates/snapshot/{id}`, `additional-questions` **không gắn checkPermission**, không gate trong controller — chỉ cần đăng nhập |

> Gap: nhóm mẫu phiếu **không có quyền "Xem danh mục mẫu phiếu thu thập thông tin"** (chỉ có "Quản lý…"). Hệ quả: user không có quyền quản lý **không mở được màn danh mục mẫu phiếu**, dù vẫn dùng được phiếu trong dự án.
