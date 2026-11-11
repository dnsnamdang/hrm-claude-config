# Gia hạn SSL *.thuocvietnam.vn (11/2026) — @cuong61n

Redmine: (chưa có số)

## Nghiệp vụ
Cert `*.thuocvietnam.vn` cũ hết hạn 12/11/2026 → cổng GDP (gdp.thuocvietnam.vn) và API (apigpp.thuocvietnam.vn) sẽ báo lỗi chứng chỉ nếu không thay. Thay bằng cert Sectigo mới hạn **28/05/2027**.

## Task
- [x] 11/11/2026 Kiểm bộ cert Sectigo: SAN `*.thuocvietnam.vn` + `thuocvietnam.vn`, key khớp cert (cùng modulus), chain Intermediate R36 → Root R46 → USERTrust.
- [x] 11/11/2026 Đổi nhãn key `RSA PRIVATE KEY` → PKCS#8 (`openssl pkcs8 -topk8 -nocrypt`) để portal CMC nhận.
- [x] 11/11/2026 Tạo cert `star-thuocvietnam-vn-11-2026` trên portal CMC (zone hn-1, Server Certificates) — ACTIVE.
- [x] 11/11/2026 Gắn cert mới vào listener TERMINATED_HTTPS:443 của 2 LB: `thuocvietnam-vn` (Port-443, VIP 42.96.53.211) và `api-thuocvietnam-vn` (api-443, VIP 42.96.53.116). Cert cũ: `start_thuocvietnam_vn_11_2025`.
- [x] 11/11/2026 Kiểm: `openssl s_client` gdp/apigpp/42.96.53.116 đều notAfter 28/05/2027; curl gdp 200, apigpp 302, ssl_verify=0.
- [ ] Còn tồn: nginx trên VM `42.96.41.87` (api-staging.sphacy.vn) và `42.96.40.67` (api-test.sphacy.vn) vẫn dùng cert cũ hết hạn — chưa SSH được.

## Trạng thái
Đã deploy prod ngày 11/11/2026 (áp dụng tức thì, không restart).
