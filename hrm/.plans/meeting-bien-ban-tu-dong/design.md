# Meeting — Tab "AI tạo biên bản" (giai đoạn thử nghiệm)

Ngày: 20/11/2026 · Trạng thái: ĐÃ DUYỆT 20/11 — kế hoạch ở plan.md; code phải hỏi riêng, chờ "làm"

## 1. Mục đích

Họp nhiều người, tranh luận nhanh ⇒ thư ký ghi biên bản thiếu/chậm. Thử để AI nghe ghi âm cuộc họp rồi
soạn sẵn: nội dung chi tiết, tóm tắt, kết luận, và gợi ý nhiệm vụ. Người dùng soát lại, quyết định.

Đã thử thủ công (file `~/Desktop/test 4.webm`, 30', 6 người): user đánh giá "khá ổn cho 1 cuộc họp nhiều
người, tranh luận khá nhanh". Giai đoạn này là **nghiên cứu thử nghiệm** ⇒ ưu tiên nhanh có bản dùng thử,
tách riêng 1 tab, KHÔNG đụng luồng biên bản/nhiệm vụ đang có.

## 2. Mục tiêu / không làm / tránh

**Mục tiêu**
- Tab mới "AI tạo biên bản" ở màn chi tiết Meeting: ghi âm trên web hoặc tải file ghi âm lên.
- Chuyển giọng nói → chữ bằng Whisper chạy CPU trên VPS (không cloud, không GPU — user chốt).
- 4 nút sinh nội dung từ bản chữ: **Nội dung chi tiết · Tóm tắt · Kết luận cuộc họp · Tạo nhiệm vụ tự động**.
- Nhiệm vụ: AI gợi ý sẵn nội dung / hạn / người làm; user sửa, chọn, **tự bấm gửi**.

**Không làm (giai đoạn này)**
- Không tự điền vào tab Biên bản / ô Kết luận cuộc họp (chỉ cho copy). Cân nhắc nút "Điền vào báo cáo" sau.
- Không nhận diện người nói bằng giọng (diarization). Không ghi âm trên app mobile.
- Không gửi dần từng đoạn khi ghi (user chọn ghi xong gửi 1 lần để nhanh có bản thử).
- Không làm cổng ngoài TPE / hrm_crm.

**Tránh (dù chạy được vẫn coi là hỏng)**
- AI tự tạo nhiệm vụ / tự gửi thông báo cho nhân viên khi user chưa bấm gửi.
- Chuyển chữ ăn hết CPU làm chậm HRM (phải 1 việc/lúc, `nice`, giới hạn thread).
- Job dài bị chạy lặp (xem bẫy `retry_after` §5.3).
- Mất bản ghi âm âm thầm (tải lên lỗi mà không báo, không còn bản dự phòng).

## 3. Ràng buộc

- Môi trường thử: **VPS dev** (`devhrmnew`, bộ hrm_crm) — user muốn thử dev trước cho an toàn.
  Prod TPE để sau, hỏi riêng.
- Tốc độ đo thực: dev ≈ RTF 1.07 (họp 30' ⇒ ~30–35' chuyển chữ); prod ≈ RTF 0.74 (~22').
  Model `Systran/faster-whisper-large-v3`, int8, beam 5, 4 thread, VAD bật. RAM ~3.6 GB/lượt.
- Cần cài ffmpeg trên VPS (chưa có) — xin phép riêng. python3-venv không có ⇒ venv `--without-pip` + get-pip.
- Gọi Claude qua REST/Guzzle (SDK PHP không cài được) — dùng lại `Modules/Agent/Claude/HttpClaudeClient.php`
  + config `Modules/Agent/Config/config.php` (`ANTHROPIC_API_KEY`) trên origin/gop_db.
- Hiện/ẩn tab **theo Cài đặt phân hệ của Meeting** (user chốt 20/11): phân hệ `meeting` hoặc mục "Tổng hợp meeting" tắt ⇒ tab ẩn. Không có cờ riêng.
- Ghi âm cần nhắc người họp (NĐ 13/2023 về dữ liệu cá nhân) — dòng nhắc trên tab.

## 4. Phương án đã cân nhắc

| # | Cách | Đánh đổi | Kết quả |
|---|------|----------|---------|
| 1 | HRM (Laravel) xếp job vào hàng đợi riêng, job gọi script Python faster-whisper trên cùng VPS; 3 nút sau gọi Claude trực tiếp | Ít thành phần nhất, dùng lại queue + client Claude sẵn có; cần 1 worker + ffmpeg | **User chọn** |
| 2 | Dịch vụ Python riêng (HTTP), HRM gọi + nhận callback | Dễ dời sang máy GPU sau; thêm dịch vụ phải trông, chậm hơn 1–2 ngày | Bỏ (giai đoạn thử chưa đáng; đổi sau chỉ thay 1 chỗ gọi) |
| 3 | API cloud (Soniox/ElevenLabs/…) | ~1' xong, tốn phí, file ra ngoài | Bỏ — user chốt chạy VPS |

Ghi âm: user chọn **ghi xong gửi 1 lần** (thay vì gửi từng phút) để nhanh có bản thử.
Nhiệm vụ: user chọn **gợi ý → user sửa → user gửi** (thay vì tạo ngay).

## 5. Thiết kế

### 5.1 Màn hình (tab mới trong `hrm-client/pages/assign/meeting/components/MeetingForm.vue`)

- Tab `ai_minutes` "AI tạo biên bản", icon `ri-sparkling-line`. Chỉ hiện khi `isShow && form.id`
  (giống tab Nhiệm vụ) VÀ Cài đặt phân hệ Meeting đang bật. Component mới `MeetingAiMinutes.vue`.

```
[!] Hãy thông báo cho người tham gia trước khi ghi âm cuộc họp.

── Ghi âm ──────────────────────────────────────────────
 ● Ghi âm   (đang ghi: 00:23:41  [Dừng])      hoặc  [Tải file ghi âm lên]
 Sau khi dừng:  [Nghe lại] [Lưu file về máy] [Gửi xử lý] [Ghi lại]
 Trạng thái: Đang chuyển chữ… (dự kiến ~30 phút, có thể rời trang)
             | Đã có bản chữ (30:12, xong lúc 10:42)   [Xem bản chữ]

── Kết quả AI ─────────────────────────────────────────
 [Nội dung chi tiết] [Tóm tắt] [Kết luận cuộc họp] [Tạo nhiệm vụ tự động]
 (khung hiển thị kết quả của nút đang chọn — sửa được, [Lưu] [Tạo lại] [Copy])
```

- Ghi âm: `MediaRecorder` (webm/opus, mono). Đang ghi ⇒ `beforeunload` cảnh báo đóng tab.
  Dừng ⇒ giữ Blob trong trình duyệt, cho nghe lại / lưu về máy / gửi. Gửi lỗi ⇒ báo rõ, vẫn giữ Blob để gửi lại.
- Tải lên: nhận webm, mp3, m4a, wav, ogg, mp4(âm thanh); tối đa ~200 MB / 3 giờ (builder chốt số theo
  `upload_max_filesize` nginx/php của dev).
- Chỉ 1 bản ghi âm "đang dùng" cho mỗi meeting; gửi bản mới ⇒ hỏi xác nhận, thay bản cũ, xoá kết quả cũ.
- 4 nút mờ cho tới khi có bản chữ. Bấm nút lần đầu ⇒ gọi Claude (vài giây, hiện đang tạo); có rồi ⇒ hiện
  bản đã lưu, [Tạo lại] mới gọi lại.
- Trạng thái chuyển chữ: FE hỏi lại mỗi ~15 giây khi tab đang mở (không cần realtime ở giai đoạn thử).

### 5.2 Nhiệm vụ tự động

- Quyền dùng tab: **người tạo hoặc chủ trì meeting** = `Meeting::canEdit()` (Meeting.php ~592). Code
  không có vai thư ký.
- Claude trả danh sách JSON: `{content, assignee_employee_ids[], due_date|null, quote, timestamp}`.
  Người làm chỉ chọn trong **thành phần họp phía công ty** + tên được nhắc khớp nhân viên (ví dụ "Cường"
  không dự họp nhưng được giao việc ⇒ khớp theo tên trong danh sách nhân viên; không chắc ⇒ để trống).
- Bảng gợi ý: mỗi dòng có ô chọn, nội dung (sửa được), người làm (chọn NV), hạn (chọn ngày), trích câu gốc
  + mốc thời gian để soát. Nút **[Gửi các nhiệm vụ đã chọn]** ⇒ tạo nhiệm vụ gắn meeting qua đúng luồng
  giao nhiệm vụ đang có của meeting (dòng biên bản "Giao nhiệm vụ" / TaskPanel) — builder dò và tái dùng
  API sẵn có (`TaskStoreRequest`), KHÔNG viết luồng tạo nhiệm vụ mới. Dòng đã gửi đánh dấu "Đã tạo" + link,
  không gửi lặp.
- Gắn task chỉ bằng `meeting_id` (task có cột này ⇒ hiện ở tab Nhiệm vụ), KHÔNG tạo dòng MeetingReport /
  `meeting_report_id` (tab Biên bản giữ nguyên — đúng mục "Không làm").
- `TaskStoreRequest` bắt buộc `due_date, estimated_hours, priority, task_type, status`: bảng gợi ý có cột
  Hạn (bắt buộc — trống thì đỏ, không gửi), Số giờ dự kiến (mặc định 1, sửa được), Độ ưu tiên (mặc định
  Bình thường). `task_type` = loại thường; `status` = Chờ bắt đầu (TODO), không qua duyệt. Nhiều người làm ⇒
  dùng `assignee_ids` (nhiệm vụ chung, mỗi người 1 task). Thông báo cho NV bắn theo luồng task sẵn có lúc
  user bấm Gửi — đúng ý "user tự quyết định gửi".

### 5.3 Phía máy chủ (`hrm-api`, module Assign)

- Bảng mới `meeting_ai_minutes` (1 meeting : n lượt, 1 lượt `is_current`):
  `meeting_id, audio_path, audio_name, audio_size, duration_sec, status (uploaded|transcribing|done|failed),
  error, transcript_json (segment + mốc giờ), transcript_text, detail, summary, conclusion,
  task_suggestions_json, started_at, finished_at, created_by`.
- File lưu `storage/app/meeting-ai/{meeting_id}/…` (không public).
- API (quyền = sửa được meeting): tải lên · xem trạng thái/kết quả · sinh 1 phần (`detail|summary|conclusion|tasks`)
  · lưu phần đã sửa · gửi nhiệm vụ đã chọn.
- Job `TranscribeMeetingAudio`:
  - Kết nối queue RIÊNG (`meeting_ai`), **`retry_after` ≥ 7200, `timeout` ~ 3h, tries 1**.
    ⚠️ connection `database` hiện có `retry_after = 1` ⇒ job 30' sẽ bị worker khác bốc lại chạy lặp.
  - 1 worker duy nhất cho queue này (1 việc/lúc).
  - Gọi `nice -n 19 python transcribe.py <file> <out.json> --prompt "<tên người dự + thuật ngữ>"`:
    ffmpeg lọc (`highpass=f=100,lowpass=f=7500,afftdn=nf=-25,dynaudnorm=f=150:g=15,loudnorm=…`, mono 16 kHz)
    → faster-whisper large-v3 int8 beam5 4 thread VAD → JSON segment.
  - Lọc câu bịa cuối file kiểu "Hãy subscribe cho kênh…", "Cảm ơn các bạn đã theo dõi".
  - initial_prompt = tên thành phần họp + chủ đề meeting (tăng chất lượng rõ rệt khi thử).
- Sinh bằng Claude — **chạy qua queue** (connection `agent` sẵn có, retry 180 — hoặc `meeting_ai`), KHÔNG
  đồng bộ trong request: họp dài vượt timeout nginx/php-fpm ~60s và `max_tokens` 8000 của Agent. Mỗi phần có
  trạng thái riêng (`detail_status`…), FE hỏi lại như bước chuyển chữ. Bản chữ quá dài ⇒ chia đoạn theo mốc giờ,
  tóm từng đoạn rồi gộp. `max_tokens` riêng cho tính năng (cấu hình).
- **Model cố định Claude** (Sonnet theo config, KHÔNG qua `AgentModelResolver` vì model đang chọn có thể là
  DeepSeek ⇒ nội dung họp nội bộ đi ra nhà cung cấp khác). Không tính vào quota Agent của NV; ghi usage/chi phí
  vào chính bản ghi `meeting_ai_minutes` để theo dõi.
- Đầu vào Claude: đầu vào = bản chữ có mốc giờ + danh sách người dự (tên, chức vụ)
  + tiêu đề/ngày meeting. Model theo config Agent. Prompt riêng cho từng phần; mọi phần phải giữ mốc giờ
  để soát lại. Không bịa — chỗ không rõ ghi "[không nghe rõ mm:ss]".
- Script Python + venv + model đặt ngoài repo (ví dụ `/opt/meeting-ai/`), đường dẫn qua `.env`
  (`MEETING_AI_PYTHON`, `MEETING_AI_SCRIPT`). Script nên đưa vào repo (thư mục `scripts/meeting-ai/`).

## 6. Điểm Claude tự chốt (user soát)

Quyền = người tạo/chủ trì · task gắn meeting_id, không đụng tab Biên bản · hạn bắt buộc, giờ mặc định 1,
ưu tiên Bình thường, trạng thái Chờ bắt đầu · model cố định Claude, không tính quota Agent · sinh nội dung
qua queue · giữ lịch sử các lượt ghi âm, chặn gửi bản mới khi bản trước đang xử lý.

## 6b. Builder tự quyết

- Tên component/route/class, cấu trúc prompt chi tiết, kiểu hiển thị khung kết quả (CKEditor hay textarea).
- Giới hạn dung lượng chính xác, định dạng chấp nhận.
- Cách hiện tiến độ (chỉ "đang xử lý" là đủ).

## 7. Việc phải xin phép riêng trước khi làm

1. Code: repo `hrm-api` + `hrm-client`, nhánh riêng tách từ `origin/gop_db` (merge khi user báo) — nêu file/bảng.
2. Migration `meeting_ai_minutes` — nêu tên file, DB đích.
3. Trên VPS dev: cài ffmpeg (apt), đặt venv/model, thêm worker queue `meeting_ai` (pm2/supervisor), `.env`.
4. Key Cài đặt phân hệ cho tab mới.
5. Deploy lên dev (skill deploy-hrm).

## 8. Còn mở (sau thử nghiệm)

- Thời hạn giữ file ghi âm (đề xuất tự xoá sau N ngày).
- Có nút "Điền vào báo cáo meeting" không; đưa lên prod TPE; gửi dần khi ghi; app mobile.
- `~/whisper-test` trên VPS prod (~3.5 GB) xoá hay giữ.
