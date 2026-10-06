import sys; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
from _vm import vm_eval
S = 'shots/'
with browser_page() as page:
    page.goto(BASE + '/assign/request-solution/add', wait_until='domcontentloaded')
    page.wait_for_selector('text=Thông tin yêu cầu', timeout=90000); page.wait_for_timeout(6000)
    page.screenshot(path=S + '06-tao-trong.png')
    clip(page, page.get_by_role('button', name='Lưu nháp'), S + 'icon_luunhap.png')
    clip(page, page.get_by_role('button', name='Lưu và gửi'), S + 'icon_luuvagui.png')
    page.get_by_role('button', name='Lưu nháp').click(); page.wait_for_timeout(3000)
    page.screenshot(path=S + '06b-tao-loi.png')
    print(vm_eval(page, 'RequestSolutionForm', "vm.request.project_key = arg; return 'ok'", 155))
    page.wait_for_timeout(5000)
    print(vm_eval(page, 'RequestSolutionForm', """
        vm.request.title = 'Yêu cầu làm giải pháp thiết bị chẩn đoán, cân chỉnh góc lái xưởng Toyota Hải Dương';
        vm.request.receive_dept = 51;
        vm.request.customer_need_quote_date = '2026-11-30';
        vm.request.note = 'Khảo sát mặt bằng 2 khoang sửa chữa chung, đề xuất cấu hình máy cân chỉnh góc lái 3D và máy chẩn đoán đa hãng; đính kèm bản vẽ mặt bằng hiện trạng.';
        return JSON.stringify(vm.request)""", None))
    page.wait_for_timeout(2500)
    page.screenshot(path=S + '07-tao-day.png', full_page=True)
    page.get_by_text('Dự án tiền khả thi', exact=True).first.click(); page.wait_for_timeout(2500)
    page.screenshot(path=S + '07b-tao-tab-tkt.png')
    page.get_by_text('Meetings', exact=True).first.click(); page.wait_for_timeout(3000)
    page.screenshot(path=S + '07c-tao-tab-meet.png')
    page.get_by_text('Thông tin yêu cầu', exact=True).first.click(); page.wait_for_timeout(1500)
    page.get_by_role('button', name='Lưu nháp').click(); page.wait_for_timeout(5000)
    print(page.url)
    page.screenshot(path=S + '07d-sau-luu-nhap.png')
