from common import *
with browser_page() as page:
    go(page,'/assign/prospective-projects/153/manager',35000)
    page.get_by_text('Thu thập thông tin', exact=True).first.click(); page.wait_for_timeout(10000)
    nums=page.get_by_placeholder('Nhập số...')
    nums.nth(0).fill('120'); nums.nth(1).fill('24')
    page.get_by_placeholder('Nhập...').first.fill('Điện 3 pha 380V, công suất cấp cho xưởng 30 kW')
    page.get_by_placeholder('Nhập chi tiết...').first.fill('Thực hành lắp mạch khí nén cơ bản, điện – khí nén, điều khiển PLC và thủy lực cơ bản; 6 bàn thực hành, mỗi bàn 4 học viên.')
    page.get_by_role('button', name='Lưu phiếu').first.click(); page.wait_for_timeout(8000)
    page.mouse.move(5,5); page.screenshot(path='explore/c1_saved.png')
