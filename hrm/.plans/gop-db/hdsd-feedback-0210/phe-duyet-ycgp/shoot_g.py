from common import *
Q='Vui lòng bổ sung bản vẽ mặt bằng phòng thực hành và vị trí cấp khí nén (máy nén khí hiện có hay cần mua mới)?'
with browser_page() as page:
    go(page,'/assign/request-solution/34?tab=add-form',45000)
    page.get_by_text('Phiếu thu thập thông tin', exact=True).first.click(); page.wait_for_timeout(8000)
    page.get_by_role('button', name='Thêm câu hỏi').first.click(); page.wait_for_timeout(800)
    page.get_by_placeholder('Nhập nội dung câu hỏi...').first.fill(Q)
    page.get_by_role('button', name='Thêm', exact=True).first.click(); page.wait_for_timeout(1000)
    page.get_by_role('button', name='Yêu cầu bổ sung').first.click(); page.wait_for_timeout(15000)
    page.mouse.move(5,5); page.screenshot(path='explore/g_after_sup.png'); print(page.url)
