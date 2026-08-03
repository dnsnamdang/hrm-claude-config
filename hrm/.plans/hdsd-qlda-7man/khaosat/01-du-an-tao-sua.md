# Khảo sát — TẠO MỚI / CHỈNH SỬA DỰ ÁN TIỀN KHẢ THI

## 1. URL
| Màn | URL | File |
|---|---|---|
| Danh sách | `/assign/prospective-projects` | `pages/assign/prospective-projects/index.vue` |
| Tạo mới | `/assign/prospective-projects/add` | `add.vue` |
| Tạo dự án con | `/assign/prospective-projects/add?parent_id={id}` | từ tab "Dự án con" |
| Chỉnh sửa | `/assign/prospective-projects/{id}/edit` | `_id/edit.vue` |
| Quản lý (10 tab) | `/assign/prospective-projects/{id}/manager` | `_id/manager.vue` |
| Xem chi tiết | `/assign/prospective-projects/{id}` | `_id/index.vue` |

API: `POST/PUT /api/v1/assign/prospective-projects` — `Routes/api.php:303,316`. **Nhóm route KHÔNG gắn checkPermission**, chỉ `auth:api`.
Tiêu đề: "Tạo mới dự án tiền khả thi" / "Tạo mới dự án cha"; sửa: "Chỉnh sửa dự án tiền khả thi".
Bố cục 2 cột: trái (8/12) = mục 1,2,3; phải (4/12) = mục 4, Phòng KD hỗ trợ, 5,6,7 + thanh nút.

## 2. Khối 1 — "1. Thông tin khách hàng"

### 1a. "Khách hàng trực tiếp"
| Nhãn | Control | Bắt buộc | Message lỗi | Mặc định | Ẩn/hiện | Options |
|---|---|---|---|---|---|---|
| **Khách hàng** * | input readonly → popup "Chọn khách hàng" | ✅ `customer_id required\|integer` | `Bắt buộc phải nhập` | rỗng | không gõ tay | popup ChooseErpCustomerModal → `GET assign/customers` (nguồn ERP TpCustomer). Popup có 3 ô lọc: Tên/Mã khách hàng, Mã số thuế, Số điện thoại + nút Tìm kiếm/Làm mới; bảng cột STT, Mã KH-Tên khách hàng, Loại, MST, SĐT, Email, Nhóm KH, Địa chỉ, Tỉnh/TP; phân trang 10/25/50/100 |
| **Thêm nhanh khách hàng** | nút chữ xanh cạnh nhãn | – | – | – | chỉ khi có quyền tạo KH (`GET assign/customers/my-permissions` → data.create) | – |
| **KH thương mại dịch vụ** | checkbox | không | – | **bỏ tick** | luôn hiện | – |
| Hộp xám: Mã KH / MST / SĐT / Họ và tên / Địa chỉ / Email / Liên hệ | read-only | – | – | tự điền sau khi chọn KH | chỉ khi đã chọn KH | `GET assign/customers/{id}` |
| **Đối tượng tổ chức** | text read-only | – | – | `customer_type_text` | khi đã chọn KH | 1 Cá nhân, 2 DN tư nhân, 3 DN nước ngoài, 4 Tổ chức phi chính phủ, 5 Cơ quan nhà nước |
| **Loại hình hoạt động khách hàng** * | CspSingleSelect (radio list + ô tìm + nút Bỏ chọn) | ✅ khi KHÔNG tick "KH thương mại dịch vụ" | `Bắt buộc phải nhập` | trống; **tự chọn nếu KH chỉ khai đúng 1** | **Ẩn khi tick "KH thương mại dịch vụ"** | `GET assign/customer-scope-groups/getAll` |
| **Lĩnh vực kinh doanh khách hàng** * | CspSingleSelect 2 cấp | ✅ cùng điều kiện | `Bắt buộc phải nhập` | trống; tự chọn nếu chỉ có 1 | Ẩn khi tick | `GET assign/customer-scopes/getAll` |
| **Email khách hàng** | input email | ❌ `nullable\|email\|max:255` | `Email khách hàng không đúng định dạng.` / `... không quá 255 ký tự.` | email KH | luôn khi đã chọn KH | – |
| **Người liên hệ** * | V2BaseSelectRemote (gõ SĐT đầy đủ để tìm) | ✅ khi KH là **doanh nghiệp** (customer_type ≠ 1) | `Bắt buộc phải nhập` | trống | **Ẩn hoàn toàn khi KH cá nhân** | `GET assign/customers/{id}/contacts` |
| **Thêm nhanh liên hệ** → Họ tên*/Chức vụ*/SĐT* + nút "Lưu & chọn", "Hủy" | inline form | cả 3 bắt buộc | lỗi từ `POST assign/customers/{id}/contacts` | trống | khi đã chọn KH | – |
| Hộp xám Tên/Chức vụ/Điện thoại/Email liên hệ | read-only | – | – | tự điền | khi đã chọn liên hệ | – |

**Cascading:** chọn Loại hình → Lĩnh vực lọc theo loại hình; chọn Lĩnh vực con → tự gán ngược Loại hình cha. Đổi Loại hình mà Lĩnh vực cũ không thuộc → xoá Lĩnh vực. Đổi khách hàng → reset Loại hình/Lĩnh vực/Ứng dụng/liên hệ.

### 1b. "Khách hàng thụ hưởng cuối" — CHỈ hiện khi tick "KH thương mại dịch vụ"
Cùng cấu trúc, prefix `customer_benefit_*`, khác:
- **Khách hàng** ✅ bắt buộc
- **Loại hình / Lĩnh vực** ✅ bắt buộc (vì khối trực tiếp bị ẩn 2 ô này)
- **Email khách hàng thụ hưởng cuối** ✅ **bắt buộc**; lỗi `Email khách hàng thụ hưởng cuối không đúng định dạng.`
- **Người liên hệ** ❌ KHÔNG bắt buộc kể cả KH doanh nghiệp

## 3. Khối 2 — "2. Thông tin dự án"
| Nhãn | Control | Bắt buộc | Mặc định | Ẩn/hiện | Options |
|---|---|---|---|---|---|
| **Tên dự án TKT** * | input (max 255) | ✅ | rỗng | luôn | – |
| **Ứng dụng** * (+ icon phiếu thu thập, nút "Xem danh sách giải pháp") | V2BaseSelect | ✅ | rỗng | **Ẩn khi dự án cha** | `GET assign/applications/for-selection?customer_scope_group_id=..&customer_scope_id=..` — **lọc theo Loại hình + Lĩnh vực của KH CUỐI**. Không có ứng dụng → cảnh báo vàng *"Hãy liên hệ với bộ phận quản lý để yêu cầu khởi tạo ứng dụng phù hợp"*. Icon 📄 cạnh nhãn: xanh = "Xem chi tiết mẫu phiếu thu thập thông tin" (mở tab `/assign/form-templates/{id}`), xám = "Chưa cấu hình mẫu phiếu thu thập thông tin cho ứng dụng này" |
| **Quy mô dự án** * | select | ✅ | trống | luôn | 1 Nhỏ (dưới 5 tỷ), 2 Vừa (từ trên 5 tỷ đến dưới 20 tỷ), 3 Lớn (từ trên 20 tỷ đến dưới 50 tỷ), 4 Trọng điểm (từ 50 tỷ trở lên) |
| **Phân loại đầu tư** * | select | ✅ | trống | Ẩn khi dự án cha | 1 Dự án mới, 2 Mở rộng nâng cấp, 3 Thay thế thiết bị, 4 Bổ sung thiết bị, 5 Sửa chữa thiết bị, 6 Cung cấp dịch vụ đi kèm, 7 Khác |
| **Cách triển khai dự án** * | select | ✅ UI; BE `nullable\|in:1,2,3` | **3 – Liên phòng ban** | Ẩn khi dự án cha; khoá khi `is_locked_implementation_type` hoặc trạng thái ≠ Đang tạo/Thu thập TT | 1 Tự triển khai, 2 Triển khai theo Phòng, 3 Liên phòng ban |
| **Địa điểm triển khai** * | input | ✅ `project_address required\|max:255` | rỗng | Ẩn khi dự án cha | – |
| **Mô tả chi tiết** | textarea 3 dòng | ❌ | rỗng | luôn | – |

## 4. Khối 3 — "3. Timeline"
| Nhãn | Control | Bắt buộc | Mặc định |
|---|---|---|---|
| **Giai đoạn dự án** * | select | ✅ | trống — `optionsSelect/fetchProjectPhases` |
| **Mức độ ưu tiên giải pháp** * | select **luôn disabled** | ✅ BE | **tự điền theo Giai đoạn dự án** |
| **Ngày bắt đầu dự án** | datepicker (chặn quá khứ) | * chỉ khi dự án cha | rỗng |
| **Ngày kết thúc dự án** | datepicker | như trên | rỗng |
| **Ngày KH cần nhận giải pháp** | datepicker | ❌ | rỗng |
| **Ngày chốt GP nội bộ** | datepicker | ❌ | rỗng |
| **Tổng số ngày thực hiện** | input **disabled** | – | tự tính = (kết thúc − bắt đầu) + 1 |

Lỗi ngày (FE hiện ngay + BE lặp lại): `Ngày bắt đầu dự án phải lớn hơn hoặc bằng ngày hiện tại.` · `Ngày kết thúc dự án phải lớn hơn hoặc bằng ngày bắt đầu dự án.` · `Ngày KH cần nhận giải pháp phải lớn hơn hoặc bằng ngày hiện tại.` · `Ngày chốt GP nội bộ phải nhỏ hơn hoặc bằng ngày KH cần nhận giải pháp.`

## 5. Khối 4 — "4. Phụ trách KD nội bộ"
| Nhãn | Control | Bắt buộc | Mặc định |
|---|---|---|---|
| **Nhân viên KD chính** * | SearchPicker **luôn disabled** | ✅ | **= người đang đăng nhập** |
| Hộp xám Họ tên/SĐT/Email | read-only | – | tự điền |
| **Phòng KD phụ trách chính** * | input **disabled** | ✅ | suy từ phòng của NV KD chính |

## 6. Khối "Phòng KD hỗ trợ & KD hỗ trợ" (không đánh số)
Mặc định **rỗng** (hiện "—"). Nút **Thêm phòng** tạo "Phòng hỗ trợ #n":
| Nhãn | Control | Bắt buộc | Ghi chú |
|---|---|---|---|
| **Chọn phòng hỗ trợ** | select | ✅ | trừ phòng KD chính + phòng đã chọn |
| **Chọn KD hỗ trợ (thuộc phòng đã chọn)** | MultiSearchPicker | ✅ ≥1 (`Phải có ít nhất 1 phần tử.`) | chỉ hiện sau khi chọn phòng; trước đó "Vui lòng chọn phòng hỗ trợ." |

## 7. Khối 5 — "5. Giải pháp" (ẩn khi dự án cha)
**Có cần làm GP?** radio Có/Không. BE không validate. Mặc định data = Không, nhưng watcher `implementation_type` chạy immediate nên với mặc định *Liên phòng ban* nó **tự bật "Có" ngay khi mở form**. Disabled khi implementation_type = 2 hoặc 3; và khi trạng thái ≠ Đang tạo/Thu thập TT.
(Phần "Phòng phụ trách làm GP" + "PM làm giải pháp" đã bị comment-out.)

## 8. Khối 6 — "6. Liên kết dữ liệu"
| Nhãn | Control | Bắt buộc | Mặc định | Ghi chú |
|---|---|---|---|---|
| **Chọn meeting khởi tạo (có thể nhiều)** | MultiSearchPicker | ❌ | rỗng | `GET assign/meeting?per_page=1000`, lọc theo KH đã chọn, bỏ meeting status=0. Đổi KH → xoá meeting + dự án cha |
| **Là dự án cha** | checkbox | ❌ | bỏ tick | Disabled khi đã chọn dự án cha hoặc `can_change_project_type=false`; khi khoá hiện *"Chỉ đổi được loại dự án khi dự án còn ở trạng thái "Đang tạo" và chưa có dự án con trực thuộc."* |
| **Chọn dự án cha đang triển khai** | SearchPicker | ❌ | rỗng; điền sẵn + khoá khi vào bằng `?parent_id=` | `GET assign/prospective-projects/parent-options`. Chú thích khi trống: *"Để trống nếu đây là dự án độc lập."* Chọn cha → **kế thừa ngay** Khách hàng, Loại tiền tệ, Giảm giá, Bảng giá |
| Hộp xám thông tin cha: Mã DA/Tên DA/Trạng thái/Khách hàng/Sale chính/Khung thời gian/Tổng ngân sách/Đã phân bổ/Còn lại + ghi chú *"Khách hàng, Giảm giá, Loại tiền tệ và Bảng giá của dự án con kế thừa từ dự án cha, không sửa được."* | read-only | – | – | khi đã chọn cha |

## 9. Khối 7 — "7. Nguồn vốn & kỳ vọng tài chính"
| Nhãn | Control | Bắt buộc | Mặc định | Ẩn/hiện |
|---|---|---|---|---|
| **Nguồn vốn** | select | ❌ | trống | Ẩn khi dự án cha. Options: 1 Vốn tự có, 2 Vốn vay ngân hàng, 3 Ngân sách nhà nước, 4 Kết hợp nhiều nguồn, 5 Khác |
| **Loại tiền tệ** * | select | ✅ | **VNĐ tự chọn khi tạo mới** | khoá khi đã có id + đã có tiền tệ, hoặc là dự án con. `GET assign/bom-lists/currencies` (AUD, CHF, CNY, EURO, IDR, JPY, RUPEE, USD, VNĐ) |
| **Giảm giá** | select | ✅ chỉ khi dự án cha | trống (= Không giảm giá) | Chỉ hiện khi cha/con. Options: null Không giảm giá, 1 Giảm giá theo mặt hàng, 2 Giảm giá theo tổng |
| **Bảng giá** | select | ✅ (cha) | trống | Chỉ khi cha/con. `GET assign/quotations/price-types` |
| **Ngân sách dự kiến** * (cha: **Tổng ngân sách dự kiến**) | V2BaseCurrencyInput | ✅ | rỗng | luôn |
| **Ngân sách đã phân bổ** | currency **disabled** + *"Tự động cộng dồn ngân sách của các dự án con."* | – | 0 | chỉ khi dự án cha |
| **Giá trị HĐ kỳ vọng** | currency | ❌ | rỗng | Ẩn khi dự án cha |
| **Lợi nhuận kỳ vọng** | currency | ❌ | rỗng | Ẩn khi dự án cha |

> **Quan trọng:** bấm **Lưu nháp** (status=1) BE gỡ toàn bộ luật bắt buộc, chỉ giữ `status` và `name`. Mọi ô ✅ chỉ bị chặn khi bấm **Lưu** (status=2).

## 10. Luồng "Thêm nhanh khách hàng"
Nút chữ xanh "＋ Thêm nhanh khách hàng" ngang hàng bên phải nhãn "Khách hàng" trong mỗi khối KH. Chỉ hiện khi có quyền tạo KH.
Popup `QuickAddCustomerModal.vue` tiêu đề **"Thêm nhanh khách hàng"** (size xl), nhúng nguyên `CustomerForm.vue` với prop `modal-mode`.

| Khối | Trường | Bắt buộc | Ghi chú |
|---|---|---|---|
| Thông tin khách hàng | **Mã khách hàng** | – | disabled, placeholder "(Tự sinh khi lưu)" |
| | **Là nhà cung cấp**, **Là khách hãng** | không | 2 checkbox, bỏ tick |
| | **Tên khách hàng** | ✅ | rỗng |
| | **Loại hình tổ chức** | ✅ | 1 Cá nhân, 2 DN tư nhân, 3 DN nước ngoài, 4 Tổ chức phi chính phủ, 5 Cơ quan nhà nước |
| | **Loại hình hoạt động khách hàng** | ❌ | multi-select chip |
| | **Lĩnh vực kinh doanh khách hàng** | ❌ | multi-select 2 cấp |
| | **Hãng xe** | ✅ chỉ khi tick "Là khách hãng" | multi |
| Thông tin cá nhân (chỉ khi Loại hình tổ chức = Cá nhân) | CCCD/CMT, Ngày cấp, Nơi cấp | ❌ | |
| | **Tên đơn vị** | ✅ | |
| | **Số điện thoại** (bảng động) | ✅ | 1 dòng trống |
| | Email, Website, Sinh nhật | ❌ | |
| | **Quốc gia / Tỉnh, Thành phố / Phường, Xã, Thị trấn** | ✅ | Quốc gia mặc định `nation_id=1` |
| | Đường/Thôn, Số nhà, Ghi chú | ❌ | |
| Thông tin tổ chức (Loại hình ∈ {2,3,4,5}) | Tên viết tắt, Công ty mẹ, MST, Email, SĐT bàn, Website | ❌ | |
| | **Địa chỉ xuất hóa đơn** | ✅ | |
| | **Quốc gia / Tỉnh, Thành phố / Phường, Xã, Thị trấn** | ✅ | |
| Người liên hệ (*) — chỉ khi Tổ chức | **Họ tên**, **Chức vụ**, **Số điện thoại** | ✅ | 1 block trống, thêm nhiều được |
| | Sinh nhật, Email, CCCD/CMT | ❌ | |

Nút: **Lưu** / **Đóng**. `POST assign/customers` → toast **"Tạo khách hàng thành công"**; 422 → lỗi inline + toast **"Bạn chưa nhập đầy đủ thông tin"**; khác → **"Tạo khách hàng thất bại"**.
Lưu xong: tìm lại KH theo `code` rồi điền vào **khối KH đang thao tác** (trực tiếp hoặc thụ hưởng cuối).

## 11. KH thường vs "KH thương mại dịch vụ"
`is_intermediary_customer` — đánh dấu KH trực tiếp chỉ là **trung gian thương mại**, người thụ hưởng thật là bên khác.

| | Không tick | Có tick |
|---|---|---|
| Số khối KH | 1 khối "Khách hàng trực tiếp" | 2 khối + **"Khách hàng thụ hưởng cuối"** |
| Loại hình / Lĩnh vực | Hiện & bắt buộc ở KH trực tiếp | **Ẩn** ở trực tiếp; **bắt buộc** ở thụ hưởng cuối |
| Ứng dụng lọc theo | Loại hình + Lĩnh vực của **KH trực tiếp** | của **KH thụ hưởng cuối** |
| KH thụ hưởng cuối | không nhập | **bắt buộc** |
| Email KH thụ hưởng cuối | – | **bắt buộc** |
| Người liên hệ | bắt buộc nếu KH doanh nghiệp; ẩn nếu cá nhân | trực tiếp: như cũ; thụ hưởng cuối: **không bắt buộc** |
| Dữ liệu lưu | BE copy snapshot KH trực tiếp sang toàn bộ cột `customer_benefit_*` | Lưu 2 bộ KH riêng |

## 12. "Cách triển khai dự án"
| Value | Nhãn UI | Const BE |
|---|---|---|
| 1 | **Tự triển khai** | IMPLEMENTATION_TYPE_SELF |
| 2 | **Triển khai theo Phòng** | IMPLEMENTATION_TYPE_BY_DEPT |
| 3 | **Liên phòng ban** ← mặc định | IMPLEMENTATION_TYPE_CROSS_DEPT |

**Ảnh hưởng trên form:**
- 1 Tự triển khai → radio "Có cần làm GP?" **mở khoá**, tự chọn Có/Không (lựa chọn DUY NHẤT cho phép chọn "Không")
- 2 / 3 → "Có cần làm GP?" **tự set = Có và bị khoá**

Form KHÔNG thêm ô chọn phòng/bộ phận theo implementation_type.

**Downstream:**
| Lựa chọn | Ai xử lý |
|---|---|
| 1 Tự triển khai | **Không được tạo Yêu cầu làm giải pháp** — chặn: `Dự án tự triển khai không cần tạo yêu cầu làm giải pháp.` KD **tự tạo giải pháp**: icon "Tạo giải pháp" hiện trên dòng danh sách khi status=2, `has_solution=true`, chưa có GP, phiếu thu thập đủ trường → `/assign/solutions/add?prospective_project_id={id}`. Không có bước duyệt hồ sơ riêng |
| 2 Theo Phòng | Tạo YC làm GP nhưng **phòng nhận khoá cứng = phòng KD phụ trách chính**. DS "chờ tiếp nhận" chỉ hiện cho người **cùng phòng** |
| 3 Liên phòng ban | User **tự chọn phòng nhận**; YC hiện cho người có quyền *Tiếp nhận yêu cầu làm giải pháp* thuộc phòng mình quản lý |

Tab màn chi tiết: dự án **type 1 + không làm GP** ẩn các tab *Yêu cầu, Giải pháp, Task, Issue, Files, Hồ sơ*.

**Cờ `has_solution`:** bật cờ **KHÔNG sinh gì cả, không gửi thông báo** — tạo YC làm GP là thao tác riêng. Chỉ sửa được khi trạng thái ∈ {Đang tạo, Thu thập thông tin dự án}; ngoài ra BE âm thầm khôi phục giá trị cũ.

## 13. Nút trên form (V2Footer cuối cột phải)
| Nút | Hiện khi | status | Toast | Điều hướng |
|---|---|---|---|---|
| **Lưu nháp** | Tạo mới: luôn. Sửa: chỉ khi status=1 | 1 | **"Đã lưu thành công!"** | `/assign/prospective-projects` |
| **Lưu** | luôn | 2 (Thu thập thông tin dự án) | **"Đã lưu thành công!"** | như trên |
| **Quay lại** | luôn | – | – | như trên |

Toast lỗi: 422 → **"Bạn chưa nhập đầy đủ thông tin"** + lỗi inline + tự cuộn tới ô lỗi đầu; 403 → **"Bạn không có quyền thực hiện chức năng này"**; 423 → *"Thao tác không thành công. Dữ liệu đã được thay đổi hoặc chuyển trạng thái bởi người dùng khác..."*; khác → **"Có lỗi xảy ra"**.
Màn **sửa** khác: mọi lỗi chỉ ra toast **"Vui lòng kiểm tra lại thông tin"** và **không tự cuộn**.

## 14. Tạo mới vs Chỉnh sửa
| Khía cạnh | Tạo mới | Chỉnh sửa |
|---|---|---|
| Nút Lưu nháp | luôn có | chỉ khi trạng thái Đang tạo |
| Loại tiền tệ | tự VNĐ, sửa được | **khoá** khi đã có `currency_id` |
| Cách triển khai | sửa thoải mái | khoá khi dự án **đã có Giải pháp hoặc YC làm GP**; lỗi `Không thể đổi cách triển khai khi dự án đã có giải pháp hoặc yêu cầu làm GP.` Khoá khi trạng thái ∉ {Đang tạo, Thu thập TT} |
| Có cần làm GP? | sửa được | khoá khi trạng thái ∉ {Đang tạo, Thu thập TT} |
| Là dự án cha / Chọn dự án cha | sửa được | chỉ khi status = Đang tạo VÀ chưa có dự án con. Lỗi: `Chỉ được đổi loại dự án khi dự án còn ở trạng thái "Đang tạo" và chưa có dự án con trực thuộc.` |
| Khách hàng | tự do | dự án cha đã có con → không đổi được; dự án con → KH/Giảm giá/Tiền tệ/Bảng giá kế thừa cứng từ cha |
| Mã dự án | chưa có | đã có, không sửa |
| Nút Xoá | – | chỉ khi `can_delete` = người tạo + trạng thái Đang tạo + chưa có dự án con |

## 15. Trạng thái dự án (thường/con)
| # | Nhãn | Chuyển bởi |
|---|---|---|
| 1 | **Đang tạo** | Lưu nháp |
| 2 | **Thu thập thông tin dự án** | Bấm Lưu; hoặc lưu phiếu thu thập từ Meeting |
| 3 | Chờ tiếp nhận làm giải pháp | Gửi YC làm giải pháp (chỉ type 2/3) |
| 4 | Đang làm giải pháp | GP chuyển Đang triển khai / Chờ duyệt |
| 5 | Đã duyệt giải pháp | GP được duyệt |
| 6 | Dự toán | Tạo YC xây dựng giá / Báo giá |
| 7 | Thương thảo giá | luồng báo giá |
| 8 | Thương thảo dự án hợp đồng | **Chốt giải pháp** |
| 9 | Thực hiện hợp đồng | (chưa set trong module Assign) |
| 10 | Nghiệm thu và thanh lý hợp đồng | (chưa set) |
| 11 | **Đóng/Không thực hiện dự án** | **Đóng dự án** — chỉ NV KD phụ trách chính; sai người: `Chỉ NV KD phụ trách mới được đóng dự án.` |
| 12 | Kết thúc và lưu trữ | (chưa set) |

**Dự án cha — bộ trạng thái RIÊNG:** 1 Đang tạo · 2 **Đang thực hiện** (tự động khi lưu dự án con đầu tiên) · 7 Trình duyệt hợp đồng · 8 Thương thảo DA/Hợp đồng · 9 HĐ đủ điều kiện thực hiện · 10 Nghiệm thu & Thanh lý · 11 Đóng/Hủy dự án · 12 Kết thúc & lưu trữ.

Bản nháp (status=1) **chỉ người tạo nhìn thấy** trên danh sách. Mọi lần đổi trạng thái ghi log `prospective_project_status_logs`.

## 16. Mã dự án — tự sinh 100%
| Loại | Pattern | Ví dụ |
|---|---|---|
| Thường/con | `{MÃ_PHÒNG}.{MÃ_ỨNG_DỤNG}.{NĂM}.DA{3 số}` | `DA01.UD.0100.2026.DA067` |
| Dự án cha | `{MÃ_PHÒNG}.{NĂM}.DAC{3 số}` | `TPE.2026.DAC001` |

**Lưu nháp KHÔNG sinh mã** — mã cấp lần đầu bấm **Lưu** chính thức. Dự án thường chỉ sinh mã khi đã chọn Ứng dụng.

## 17. Màn danh sách
Cột: STT · Mã - Tên dự án TKT (+ KD phụ trách, Phòng ban, Bộ phận, Ngày tạo/cập nhật) · Tiến trình dự án · Giải pháp · Version giải pháp · Khách hàng · Khách hàng cuối · Giai đoạn dự án · Quy mô dự án · Phân loại đầu tư · Nguồn vốn · Tổng số ngày hoàn thành · Phòng làm GP · PM giải pháp · Ngày KH cần GP · Ngày dự kiến chốt GP · Ứng dụng · Lĩnh vực kinh doanh khách hàng · Loại hình hoạt động khách hàng.

Panel "Bộ lọc danh sách dự án tiền khả thi": ô nhanh *Tìm theo Mã dự án, Tên dự án, Mã KH, Tên KH* + nút Tìm kiếm / Làm mới / Tìm kiếm nâng cao.
Lọc nâng cao (16 tiêu chí): Công ty · Phòng ban · Bộ phận · Nhân viên KD phụ trách · Khách hàng · Khách hàng cuối · Giai đoạn dự án · Nguồn vốn · Phân loại đầu tư · Quy mô dự án · Tiến trình dự án · Ứng dụng · Loại hình hoạt động khách hàng · Lĩnh vực kinh doanh khách hàng · Ngày tạo từ · Ngày tạo đến.
Nút: **Tạo mới** · **Xuất Excel** · icon **Cấu hình cột hiển thị**.
Thao tác dòng: **Xem** (mắt) · **Sửa** (bút) · **Tạo giải pháp** (chỉ dự án Tự triển khai đủ điều kiện) · **Xoá** (khi can_delete).
