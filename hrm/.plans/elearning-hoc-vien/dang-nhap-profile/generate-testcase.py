# -*- coding: utf-8 -*-
"""Testcase Đăng nhập/SSO + Profile (elearning) — theo nhãn UI thật."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _tc_builder import build

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Nhóm màn tài khoản: đăng nhập (SSO cho nhân viên, learner cho học viên ngoài), đăng ký + xác thực email, quên/đặt lại mật khẩu, trang cá nhân (hồ sơ + đổi/thiết lập mật khẩu + avatar)."),
    ("2. Đối tượng được tính / hiển thị",
     "► Nhân viên (badge 'Nhân viên'): SSO, hồ sơ readonly.\n► Học viên (badge 'Học viên'): email/Google, sửa hồ sơ + avatar + mật khẩu.\n► Mật khẩu tối thiểu 8 ký tự."),
    ("3. Đối tượng bị ẩn / không tính",
     "► Nhân viên: không có tab đổi mật khẩu, không đổi avatar, không nút Lưu.\n► Reset không token → ẩn form (khối lỗi)."),
    ("4. Bộ lọc thời gian áp dụng cho", "Không áp dụng."),
    ("5. Cấu trúc dữ liệu / cây phân cấp", "Login/SSO/Register/Forgot/Reset/Verify + Profile (tab Thông tin cá nhân, tab Đổi/Thiết lập mật khẩu)."),
    ("6. Quy tắc cộng dồn / deduplicate", "Email chưa xác thực → banner CTA (không toast). SSO thất bại → /login?sso_failed=1 → banner."),
    ("7. Phân quyền cấp", "Không phân quyền cấp. Phân biệt Nhân viên vs Học viên."),
    ("8. Cách tính các ô thống kê", "Không có."),
    ("9. Ghi chú đọc bảng", "Nút lưu hồ sơ là 'Lưu thay đổi'. Learner Google chưa có mật khẩu → tab 'Thiết lập mật khẩu'."),
]

SECTIONS = [
    ("I", "ĐĂNG NHẬP", [
        ("001", "Đăng nhập bằng HRM (SSO)", "P0", "Là nhân viên có tài khoản HRM",
         "1. Ở /login bấm 'Đăng nhập bằng HRM'\n2. Đăng nhập HRM", "—",
         "- Trao đổi token, toast 'Đăng nhập thành công', vào app", "—"),
        ("002", "SSO thất bại", "P1", "Chưa đăng nhập HRM",
         "1. Quay lại từ SSO thất bại", "—",
         "- Về /login?sso_failed=1 + banner 'Bạn chưa đăng nhập hệ thống công ty...'", "BR-02"),
        ("003", "Đăng nhập learner đúng", "P0", "Có tài khoản learner đã xác thực",
         "1. Nhập Email + Mật khẩu\n2. Bấm 'Đăng nhập'", "email/mật khẩu đúng",
         "- Toast 'Đăng nhập thành công', về trang trước", "—"),
        ("004", "Đăng nhập sai mật khẩu", "P0", "Tài khoản tồn tại",
         "1. Nhập sai mật khẩu\n2. Bấm 'Đăng nhập'", "mật khẩu sai",
         "- Lỗi field đỏ dưới ô (không đăng nhập được)", "—"),
        ("005", "Email chưa xác thực", "P1", "Tài khoản chưa verify email",
         "1. Đăng nhập tài khoản chưa verify", "—",
         "- Banner 'Email {…} chưa được xác thực.' + nút 'Gửi lại mail xác thực'", "BR-01"),
        ("006", "Ẩn/hiện mật khẩu", "P2", "Ở form đăng nhập",
         "1. Bấm icon con mắt ở ô Mật khẩu", "—",
         "- Chuyển ẩn ↔ hiện mật khẩu", "—"),
    ]),
    ("II", "ĐĂNG KÝ & XÁC THỰC", [
        ("001", "Đăng ký hợp lệ", "P0", "Email chưa tồn tại",
         "1. Nhập Họ tên, Email, Mật khẩu (≥8), Xác nhận\n2. Bấm 'Đăng ký'", "hợp lệ",
         "- Khối 'Hãy kiểm tra email của bạn' + 'gửi liên kết xác thực đến {…}'", "—"),
        ("002", "Đăng ký mật khẩu ngắn", "P1", "Form đăng ký",
         "1. Nhập mật khẩu < 8 ký tự\n2. Bấm 'Đăng ký'", "mật khẩu 5 ký tự",
         "- Báo lỗi mật khẩu tối thiểu 8 ký tự", "BR-04"),
        ("003", "Gửi lại mail xác thực", "P2", "Sau đăng ký",
         "1. Bấm 'Gửi lại'", "—",
         "- Toast 'Đã gửi lại mail xác thực'", "—"),
        ("004", "Xác thực email thành công", "P1", "Có link xác thực hợp lệ",
         "1. Mở link /verify-email?token=...", "—",
         "- 'Xác thực thành công!' + toast, tự về trang chủ", "—"),
        ("005", "Xác thực token hỏng", "P2", "Token sai/hết hạn",
         "1. Mở /verify-email token sai", "—",
         "- 'Xác thực thất bại' + nút 'Quay lại đăng nhập'", "—"),
    ]),
    ("III", "QUÊN / ĐẶT LẠI MẬT KHẨU", [
        ("001", "Gửi yêu cầu quên mật khẩu", "P1", "Ở /forgot-password",
         "1. Nhập Email\n2. Bấm 'Gửi yêu cầu'", "email",
         "- Toast 'Nếu email tồn tại, hướng dẫn đã được gửi.'", "—"),
        ("002", "Đặt lại mật khẩu", "P1", "Có link reset hợp lệ",
         "1. Mở /reset-password?token=...\n2. Nhập Mật khẩu mới + Xác nhận\n3. Bấm 'Đặt lại mật khẩu'", "≥8 ký tự",
         "- Toast 'Đặt lại mật khẩu thành công...', tự về /login", "—"),
        ("003", "Reset không có token", "P2", "Mở /reset-password không token",
         "1. Mở /reset-password", "—",
         "- Khối lỗi 'Liên kết không hợp lệ. Vui lòng yêu cầu lại tại Quên mật khẩu.'", "BR-03"),
    ]),
    ("IV", "TRANG CÁ NHÂN", [
        ("001", "Learner sửa hồ sơ", "P0", "Đăng nhập learner",
         "1. Vào /profile tab 'Thông tin cá nhân'\n2. Sửa Số điện thoại/Công ty\n3. Bấm 'Lưu thay đổi'", "—",
         "- Toast 'Cập nhật thông tin thành công'", "—"),
        ("002", "Learner đổi avatar", "P1", "Đăng nhập learner",
         "1. Bấm nút camera 'Đổi ảnh đại diện'\n2. Chọn ảnh", "ảnh jpg/png",
         "- Toast 'Đã cập nhật ảnh đại diện'", "—"),
        ("003", "Nhân viên hồ sơ readonly", "P0", "Đăng nhập nhân viên",
         "1. Vào /profile", "—",
         "- Banner 'Thông tin tài khoản công ty được quản lý tại hệ thống HRM...'; trường readonly; không có nút Lưu; không tab đổi mật khẩu", "BR-05"),
        ("004", "Learner đổi mật khẩu", "P1", "Learner đã có mật khẩu",
         "1. Tab 'Đổi mật khẩu'\n2. Nhập Mật khẩu hiện tại + mới + xác nhận\n3. Bấm 'Đổi mật khẩu'", "≥8 ký tự",
         "- Toast 'Đổi mật khẩu thành công'", "—"),
        ("005", "Learner Google thiết lập mật khẩu", "P2", "Learner Google chưa có mật khẩu",
         "1. Tab 'Thiết lập mật khẩu'\n2. Nhập Mật khẩu mới + xác nhận\n3. Bấm 'Thiết lập mật khẩu'", "≥8 ký tự",
         "- Toast 'Thiết lập mật khẩu thành công'", "BR-06"),
    ]),
]

build(
    output_file=r"d:\CompanyProject\hrm-cursor\.plans\elearning-hoc-vien\dang-nhap-profile\testcase.xlsx",
    sheet_name="DangNhapProfile", feature_name="Đăng nhập / SSO / Đăng ký & Trang cá nhân", module_name="Auth & Profile",
    description_block=DESCRIPTION_BLOCK, sections=SECTIONS, role_tcs=None,
)
