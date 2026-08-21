-- Rollback giá trị companies.header / companies.logo TRƯỚC khi chuẩn hoá thành URL tuyệt đối
-- Sinh ngày 2026-08-21 từ DB gop_db (8 công ty). Chạy nguyên file này là trả về y như cũ.
UPDATE companies SET header = '/uploads/1751696586ts-hn.png', logo = '/uploads/1778661674z7821302147749-02797d8ccc1afe91a1dd40f81fe21a33.jpg' WHERE id = 1;
UPDATE companies SET header = '/uploads/1751696363cn-hp.png', logo = '/uploads/1778662706z7821302147749-02797d8ccc1afe91a1dd40f81fe21a33.jpg' WHERE id = 2;
UPDATE companies SET header = '/uploads/1751696460cn-vinh.png', logo = '/uploads/1778662695z7821302147749-02797d8ccc1afe91a1dd40f81fe21a33.jpg' WHERE id = 3;
UPDATE companies SET header = '/uploads/1751696416tpsg.png', logo = '/uploads/1778662718z7821302147749-02797d8ccc1afe91a1dd40f81fe21a33.jpg' WHERE id = 4;
UPDATE companies SET header = '/uploads/1597649194header-tpa.jpg', logo = '/uploads/1597649189logo-tpa.jpg' WHERE id = 5;
UPDATE companies SET header = '/uploads/1598510760header-up.jpg', logo = '/uploads/1598510755logo-up.jpg' WHERE id = 6;
UPDATE companies SET header = '/uploads/1719282902etek-green.jpg', logo = '/uploads/1719282905etek-green.jpg' WHERE id = 7;
UPDATE companies SET header = '/uploads/1770272858header-etek-group-resize.png', logo = '/uploads/1770255503etek-logo-final-png.png' WHERE id = 8;
