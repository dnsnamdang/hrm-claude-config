<template>
    <div class="rc-page v2-styles">
        <!-- ĐẦU TRANG -->
        <div class="page-head">
            <div class="ico"><i class="ri-file-settings-line" /></div>
            <div>
                <h1>Khai báo quy chế – cấu hình</h1>
                <p>
                    Khai cấu hình &amp; quy chế cho công ty của bạn — cấp công ty và cấp phòng ban – bộ phận, gộp về
                    một màn. Hẹn ngày áp dụng theo cả tab (hoặc theo dòng với tab dạng bảng).
                </p>
            </div>
        </div>

        <!-- THANH PHẠM VI -->
        <div class="scopebar">
            <div class="scope-field">
                <span>Công ty đang cấu hình</span>
                <div class="company-badge" :title="`Xác định theo tài khoản đăng nhập`">
                    <i class="ri-building-2-line" />
                    <b>{{ currentCompany }}</b>
                    <span class="lock">theo tài khoản đăng nhập</span>
                </div>
            </div>

            <div class="scope-field">
                <span>Phạm vi áp dụng</span>
                <div class="seg">
                    <button :class="{ on: scope === 'company' }" @click="setScope('company')">
                        <span class="n">1</span> Theo công ty
                    </button>
                    <button :class="{ on: scope === 'department' }" @click="setScope('department')">
                        <span class="n">2</span> Theo phòng ban – bộ phận
                    </button>
                </div>
            </div>

            <div v-if="scope === 'department'" class="scope-field">
                <span>Phòng ban / Bộ phận</span>
                <div style="min-width: 260px">
                    <V2BaseSelect
                        v-model="selectedUnitId"
                        :options="unitOptions"
                        :allow-clear="false"
                        @change="onUnitChange"
                    />
                </div>
            </div>

            <div class="scope-spacer"></div>

            <div class="savebar">
                <V2BaseButton primary size="sm" @click="onSave">
                    <template #prefix><i class="ri-save-3-line" /></template>
                    Lưu cấu hình
                </V2BaseButton>
                <V2BaseButton tertiary size="sm" @click="onCancel">Hủy</V2BaseButton>
            </div>
        </div>

        <!-- GIỚI THIỆU -->
        <div class="hint intro">
            <i class="ri-calendar-schedule-line" />
            <div>
                <b>Hẹn ngày áp dụng theo tab:</b> mỗi tab có <b>một phiên bản đang áp dụng</b> + nút
                <b>Hẹn phiên bản mới</b> (nhập giá trị mới cho cả tab + 1 ngày hiệu lực). Đến ngày, hệ thống
                <b>tự động</b> áp dụng cả tab; phiếu đã lập <b>giữ nguyên</b> giá trị cũ (bản chụp). Riêng tab dạng
                bảng (hoa hồng) hẹn theo <b>từng dòng</b>. Nhóm có
                <i class="ri-time-line hen-inline" /> là đang có lịch hẹn chờ.
            </div>
        </div>

        <!-- MASTER-DETAIL -->
        <div class="md">
            <!-- danh sách nhóm -->
            <div class="grouplist">
                <h3>Danh sách nhóm quy chế</h3>
                <div class="items">
                    <button
                        v-for="(it, i) in curGroups"
                        :key="it.id"
                        class="gitem"
                        :class="{ on: i === groupIdx }"
                        @click="groupIdx = i"
                    >
                        <span class="gi"><i :class="iconClass(it.icon)" /></span>
                        <span class="gt"><b>{{ it.name }}</b><small>{{ it.sub }}</small></span>
                        <span
                            v-if="groupPending(it)"
                            class="hen-mark"
                            :title="`${groupPending(it)} lịch hẹn đang chờ`"
                        ><i class="ri-time-line" /></span>
                        <span class="badge">{{ groupCount(it) }}</span>
                    </button>
                </div>
            </div>

            <!-- chi tiết -->
            <div class="detail">
                <div class="detail-head">
                    <div class="dh-title">
                        <div>
                            <h2>{{ curGroup.name }}</h2>
                            <p>
                                {{ curGroup.sub }}
                                <span v-if="curGroup.note" class="note-inline">⚠ {{ curGroup.note }}</span>
                            </p>
                        </div>
                        <div class="dh-chips">
                            <span v-if="scope === 'department' && selectedUnitName" class="scope-chip unit">
                                {{ unitType === 'part' ? 'Bộ phận' : 'Phòng ban' }}: {{ selectedUnitName }}
                            </span>
                            <span class="scope-chip" :class="curScopeMeta.chip">{{ curScopeMeta.chipText }}</span>
                        </div>
                    </div>
                </div>

                <!-- ===== FORM ===== -->
                <div v-if="curGroup.type === 'form'" class="detail-body">
                    <template v-if="canHen(curGroup.id)">
                        <!-- thanh phiên bản -->
                        <div class="verbar" :class="{ 'has-pend': (curGroup.pending || []).length }">
                            <div class="vcur">
                                <span class="lb">Phiên bản đang áp dụng</span>
                                <b>từ {{ fmtDate(curGroup.eff) }}</b>
                            </div>
                            <div class="vact">
                                <span v-for="(p, pi) in curGroup.pending || []" :key="pi" class="vpend">
                                    <i class="ri-time-line" /> Hiệu lực <b>{{ fmtDate(p.date) }}</b> ·
                                    {{ p.changes.length }} thay đổi
                                </span>
                                <V2BaseButton light status="warning" size="sm" @click="openVer(curGroup)">
                                    <template #prefix><i class="ri-calendar-schedule-line" /></template>
                                    Hẹn phiên bản mới
                                </V2BaseButton>
                            </div>
                        </div>

                        <!-- hàng đợi phiên bản đã hẹn -->
                        <div v-if="(curGroup.pending || []).length" class="vqueue">
                            <div class="vq-head"><i class="ri-time-line" /> Phiên bản đã hẹn (chờ áp dụng)</div>
                            <div v-for="(p, pi) in curGroup.pending" :key="pi" class="vq-item">
                                <div class="vq-date"><i class="ri-time-line" /> {{ fmtDate(p.date) }}</div>
                                <div class="vq-body">
                                    <div class="vq-changes">
                                        <div v-for="(c, ci) in p.changes" :key="ci">
                                            <span class="lbl">{{ c.label }}:</span>
                                            <span class="old">{{ c.old }}{{ c.unit ? ' ' + c.unit : '' }}</span> →
                                            <span class="new">{{ c.new }}{{ c.unit ? ' ' + c.unit : '' }}</span>
                                        </div>
                                    </div>
                                    <div class="vq-meta">
                                        Người tạo: {{ p.who }}<template v-if="p.note"> · {{ p.note }}</template> ·
                                        <span class="pill wait">Chờ áp dụng</span>
                                    </div>
                                </div>
                                <div class="vq-act">
                                    <button class="iconbtn" title="Sửa lịch hẹn" @click="openVer(curGroup, pi)">
                                        <i class="ri-pencil-line" />
                                    </button>
                                    <button class="iconbtn danger" title="Huỷ lịch hẹn">
                                        <i class="ri-delete-bin-line" />
                                    </button>
                                </div>
                            </div>
                        </div>
                    </template>

                    <div v-else class="no-hen-note">
                        <i class="ri-checkbox-circle-line" />
                        <div>Tab này <b>không hẹn ngày áp dụng</b> ({{ noHenReason(curGroup.id) }}) — sửa là áp dụng ngay.</div>
                    </div>

                    <!-- banner chỉ khai cấp phòng ban -->
                    <div v-if="curGroup.deptOnly" class="hint">
                        <i class="ri-information-line" />
                        <div>
                            Nhóm này <b>chỉ khai ở cấp Phòng ban</b> (quỹ rủi ro, % lợi nhuận, hạn mức duyệt của Trưởng
                            phòng). Bộ phận không có các cột này — đúng như ERP hiện tại.
                        </div>
                    </div>

                    <!-- lưới field -->
                    <div class="fgrid">
                        <div
                            v-for="(f, fi) in curGroup.fields"
                            :key="fi"
                            class="f"
                            :class="{ wide: f.wide || f.t === 'logo' || f.t === 'tags' || f.t === 'toggles' || f.t === 'subtable' }"
                        >
                            <label>
                                {{ f.label }}
                                <span v-if="f.t === 'date' && f.fixed" class="fixed-tag">· mốc cố định</span>
                            </label>

                            <!-- logo -->
                            <div v-if="f.t === 'logo'" class="upload">
                                <div class="ph"><i class="ri-image-line" /></div>
                                <div>
                                    <V2BaseButton tertiary size="sm">Chọn ảnh…</V2BaseButton>
                                    <div class="default-note">PNG, JPG tối đa 2MB</div>
                                </div>
                            </div>

                            <!-- text -->
                            <V2BaseInput v-else-if="f.t === 'text'" v-model="f.val" />

                            <!-- textarea -->
                            <V2BaseTextarea v-else-if="f.t === 'area'" v-model="f.val" :rows="3" />

                            <!-- date -->
                            <V2BaseDatePicker v-else-if="f.t === 'date'" v-model="f.val" :disabled="!!f.fixed" />

                            <!-- select -->
                            <V2BaseSelect
                                v-else-if="f.t === 'select'"
                                v-model="f.val"
                                :options="asOptions(f.opts)"
                                :allow-clear="false"
                            />

                            <!-- number (tiền dùng CurrencyInput) -->
                            <V2BaseCurrencyInput
                                v-else-if="f.t === 'number' && f.unit === 'đồng'"
                                v-model="f.val"
                                :precision="0"
                                has-suffix
                            >
                                <template #suffix><span class="unit">đ</span></template>
                            </V2BaseCurrencyInput>
                            <V2BaseInput
                                v-else-if="f.t === 'number'"
                                v-model="f.val"
                                type="number"
                                :has-suffix="!!f.unit"
                            >
                                <template v-if="f.unit" #suffix><span class="unit">{{ f.unit }}</span></template>
                            </V2BaseInput>

                            <!-- tags -->
                            <div v-else-if="f.t === 'tags'" class="tagbox">
                                <span v-for="(v, vi) in f.val" :key="vi" class="tag">
                                    {{ v }} <span @click="f.val.splice(vi, 1)">✕</span>
                                </span>
                                <span class="tag-add">+ thêm…</span>
                            </div>

                            <!-- toggles -->
                            <div v-else-if="f.t === 'toggles'" class="toggles">
                                <div
                                    v-for="(pair, pi) in f.items"
                                    :key="pi"
                                    class="tg"
                                    :class="{ on: pair[1] }"
                                    @click="pair.splice(1, 1, pair[1] ? 0 : 1)"
                                >
                                    <span class="sw"></span>{{ pair[0] }}
                                </div>
                            </div>

                            <!-- subtable -->
                            <div v-else-if="f.t === 'subtable'">
                                <div class="tbl-tools">
                                    <span class="muted">{{ f.rows.length }} dòng</span>
                                    <V2BaseButton tertiary size="sm">+ Thêm dòng</V2BaseButton>
                                </div>
                                <div class="tbl-wrap">
                                    <table class="grid">
                                        <thead>
                                            <tr>
                                                <th v-for="(c, ci) in f.cols" :key="ci">{{ c }}</th>
                                                <th style="width: 80px">Thao tác</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr v-for="(r, ri) in f.rows" :key="ri">
                                                <td v-for="(c, ci) in r" :key="ci">{{ c }}</td>
                                                <td>
                                                    <button class="iconbtn danger"><i class="ri-delete-bin-line" /></button>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div v-if="canHen(curGroup.id)" class="snap-note">
                        <i class="ri-information-line" />
                        <div>
                            Đến ngày hiệu lực, hệ thống <b>tự động</b> áp dụng phiên bản mới cho cả tab. Các phiếu đã
                            lập trước đó <b>giữ nguyên</b> giá trị cũ (đã lưu bản chụp lúc lập) — hẹn không hồi tố phiếu cũ.
                        </div>
                    </div>
                </div>

                <!-- ===== GRID (hoa hồng) ===== -->
                <div v-else-if="curGroup.type === 'grid'" class="detail-body">
                    <div class="hint"><i class="ri-information-line" /><div v-html="curGroup.hint"></div></div>
                    <div class="tbl-tools">
                        <span class="muted"><b>{{ curGroup.rows.length }}</b> quy chế đang khai cho đơn vị này</span>
                        <V2BaseButton primary size="sm" @click="openReg()">
                            <template #prefix><i class="ri-add-line" /></template>
                            Thêm mới
                        </V2BaseButton>
                    </div>
                    <div class="tbl-wrap">
                        <table class="grid">
                            <thead>
                                <tr>
                                    <th style="width: 40px">STT</th>
                                    <th>Áp dụng cho</th>
                                    <th>Bảng giá</th>
                                    <th>Giá net so sánh</th>
                                    <th title="Thưởng năng suất tháng">NS tháng</th>
                                    <th title="Thưởng năng suất quý">NS quý</th>
                                    <th>Phân chia HĐ<br /><small>TP/TBP/NV</small></th>
                                    <th>Phân chia NS<br /><small>TP/TBP/NV</small></th>
                                    <th style="width: 118px">Hiệu lực từ</th>
                                    <th style="width: 130px">Trạng thái</th>
                                    <th style="width: 96px">Thao tác</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(r, i) in curGroup.rows" :key="i" :class="{ 'row-wait': r[7] === 'wait' }">
                                    <td class="num">{{ i + 1 }}</td>
                                    <td><b>{{ r[0] }}</b></td>
                                    <td>{{ r[1] }}</td>
                                    <td>{{ r[2] }}</td>
                                    <td class="num">{{ r[3] }}%</td>
                                    <td class="num">{{ r[4] }}%</td>
                                    <td><div class="split3"><span v-for="(x, xi) in r[5].split(' / ')" :key="xi">{{ x }}</span></div></td>
                                    <td><div class="split3"><span v-for="(x, xi) in r[6].split(' / ')" :key="xi">{{ x }}</span></div></td>
                                    <td class="eff">{{ fmtDate(r[8]) }}</td>
                                    <td><span class="pill" :class="r[7]">{{ statusText(r[7]) }}</span></td>
                                    <td>
                                        <div class="rowact">
                                            <button class="iconbtn" @click="openReg(i)"><i class="ri-pencil-line" /></button>
                                            <button class="iconbtn danger"><i class="ri-delete-bin-line" /></button>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="tbl-foot">
                        <span>Hiển thị 1–{{ curGroup.rows.length }} / {{ curGroup.rows.length }} quy chế</span>
                    </div>
                </div>

                <!-- ===== LADDER (bậc thang lũy tiến) ===== -->
                <div v-else-if="curGroup.type === 'ladder'" class="detail-body">
                    <div class="verbar" :class="{ 'has-pend': (curGroup.pending || []).length }">
                        <div class="vcur">
                            <span class="lb">Phiên bản đang áp dụng</span>
                            <b>từ {{ fmtDate(curGroup.eff) }}</b>
                        </div>
                        <div class="vact">
                            <span v-for="(p, pi) in curGroup.pending || []" :key="pi" class="vpend">
                                <i class="ri-time-line" /> Hiệu lực <b>{{ fmtDate(p.date) }}</b> · {{ p.changes.length }} thay đổi
                            </span>
                            <V2BaseButton light status="warning" size="sm" @click="openVer(curGroup)">
                                <template #prefix><i class="ri-calendar-schedule-line" /></template>
                                Hẹn phiên bản mới
                            </V2BaseButton>
                        </div>
                    </div>

                    <div v-if="(curGroup.pending || []).length" class="vqueue">
                        <div class="vq-head"><i class="ri-time-line" /> Phiên bản đã hẹn (chờ áp dụng)</div>
                        <div v-for="(p, pi) in curGroup.pending" :key="pi" class="vq-item">
                            <div class="vq-date"><i class="ri-time-line" /> {{ fmtDate(p.date) }}</div>
                            <div class="vq-body">
                                <div class="vq-changes">
                                    <div v-for="(c, ci) in p.changes" :key="ci">
                                        <span class="lbl">{{ c.label }}:</span>
                                        <span class="old">{{ c.old }}</span> → <span class="new">{{ c.new }}</span>
                                    </div>
                                </div>
                                <div class="vq-meta">Người tạo: {{ p.who }} · {{ p.note }} · <span class="pill wait">Chờ áp dụng</span></div>
                            </div>
                            <div class="vq-act">
                                <button class="iconbtn" @click="openVer(curGroup, pi)"><i class="ri-pencil-line" /></button>
                                <button class="iconbtn danger"><i class="ri-delete-bin-line" /></button>
                            </div>
                        </div>
                    </div>

                    <div class="hint"><i class="ri-information-line" /><div v-html="curGroup.hint"></div></div>
                    <div class="tbl-tools">
                        <span class="muted">Bậc thang theo <b>Tổng hoa hồng của phòng</b></span>
                        <V2BaseButton tertiary size="sm"><template #prefix><i class="ri-add-line" /></template>Thêm bậc</V2BaseButton>
                    </div>
                    <div class="tbl-wrap">
                        <table class="grid">
                            <thead>
                                <tr>
                                    <th style="width: 40px">Bậc</th>
                                    <th colspan="2">Giá trị từ</th>
                                    <th colspan="2">Đến giá trị</th>
                                    <th style="width: 130px">Tỉ lệ thưởng</th>
                                    <th style="width: 60px"></th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(r, i) in curGroup.ladder" :key="i">
                                    <td class="num">{{ i + 1 }}</td>
                                    <td>
                                        <select v-model="r[0]" class="cellsel">
                                            <option v-for="o in opOptions" :key="o">{{ o }}</option>
                                        </select>
                                    </td>
                                    <td><input v-model="r[1]" class="cellinput" /></td>
                                    <td>
                                        <select v-model="r[2]" class="cellsel">
                                            <option v-for="o in opOptions" :key="o">{{ o }}</option>
                                        </select>
                                    </td>
                                    <td><input v-model="r[3]" class="cellinput" placeholder="—" /></td>
                                    <td>
                                        <div class="cell-unit">
                                            <input v-model="r[4]" class="cellinput" /><span class="unit">%</span>
                                        </div>
                                    </td>
                                    <td><button class="iconbtn danger"><i class="ri-delete-bin-line" /></button></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="rateblock">
                        <div class="rb-title">
                            <i class="ri-percent-line" /> Tỉ lệ chia lũy tiến
                            <span class="sum">Tổng: {{ ladderSum }}%</span>
                        </div>
                        <div class="rate3">
                            <div class="f">
                                <label>Trưởng phòng (TP)</label>
                                <V2BaseInput v-model="curGroup.progressive.tp" type="number" has-suffix>
                                    <template #suffix><span class="unit">%</span></template>
                                </V2BaseInput>
                            </div>
                            <div class="f">
                                <label>Trưởng bộ phận (TBP)</label>
                                <V2BaseInput v-model="curGroup.progressive.tbp" type="number" has-suffix>
                                    <template #suffix><span class="unit">%</span></template>
                                </V2BaseInput>
                            </div>
                            <div class="f">
                                <label>Nhân viên (NV)</label>
                                <V2BaseInput v-model="curGroup.progressive.nv" type="number" has-suffix>
                                    <template #suffix><span class="unit">%</span></template>
                                </V2BaseInput>
                            </div>
                        </div>
                    </div>

                    <div class="snap-note">
                        <i class="ri-information-line" />
                        <div>Đến ngày hiệu lực, hệ thống <b>tự động</b> áp dụng cả phiên bản; phiếu đã lập <b>giữ nguyên</b> giá trị cũ.</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- LỊCH SỬ -->
        <div class="history">
            <div class="hh">
                <h3><i class="ri-history-line" /> Lịch sử thay đổi <span class="muted">· {{ curScopeMeta.chipText }}</span></h3>
                <a class="lnk" href="javascript:void(0)">Xem tất cả lịch sử <i class="ri-arrow-right-line" /></a>
            </div>
            <div class="tbl-wrap flat">
                <table class="grid">
                    <thead>
                        <tr>
                            <th style="width: 150px">Thời gian</th>
                            <th style="width: 150px">Người thực hiện</th>
                            <th>Nội dung thay đổi</th>
                            <th style="width: 210px">Phạm vi áp dụng</th>
                            <th>Ghi chú</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(r, i) in curHistory" :key="i">
                            <td class="t">{{ r[0] }}</td>
                            <td class="who">{{ r[1] }}</td>
                            <td>
                                {{ r[2] }}
                                <span v-if="r[5]" class="badge-hen"><i class="ri-time-line" /> hẹn</span>
                            </td>
                            <td>{{ r[3] }}</td>
                            <td>{{ r[4] || '—' }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- ===== MODAL: HẸN PHIÊN BẢN MỚI ===== -->
        <V2BaseModal
            ref="verModal"
            modal-id="rc-ver-modal"
            :title="verEditing ? 'Sửa phiên bản đã hẹn' : 'Hẹn phiên bản mới'"
            :subtitle="verGroup ? verGroup.name : ''"
            subtitle-label="Tab"
            icon="ri-calendar-schedule-line"
            icon-color="#c9772a"
            icon-background="rgba(201,119,42,0.12)"
            size="lg"
        >
            <div v-if="verGroup" class="rc-scope">
                <div class="fieldset eff-fs">
                    <div class="fs-title">Hiệu lực</div>
                    <div class="eff-row">
                        <div class="f">
                            <label>Hiệu lực từ ngày</label>
                            <V2BaseDatePicker v-model="verForm.date" />
                        </div>
                        <div class="f grow">
                            <label>Ghi chú (lý do ban hành)</label>
                            <V2BaseInput v-model="verForm.note" placeholder="VD: Điều chỉnh chính sách Q4/2026" />
                        </div>
                    </div>
                    <div class="field-hint">
                        Chọn ngày <b>trong tương lai</b> — đến đúng ngày này, <b>toàn bộ tab</b> tự chuyển sang phiên
                        bản mới. Phiếu đã lập giữ nguyên giá trị cũ.
                    </div>
                </div>

                <div v-if="verGroup.type === 'ladder'" class="hint">
                    <i class="ri-information-line" />
                    <div>
                        Phiên bản mới sẽ chụp lại <b>toàn bộ bảng bậc thang + tỉ lệ chia lũy tiến</b>. Sửa trực tiếp
                        bảng bên dưới rồi lưu — đến ngày hiệu lực cả phiên bản sẽ thay.
                    </div>
                </div>

                <div v-else class="fieldset">
                    <div class="fs-title">Giá trị trong phiên bản mới (ô đã sửa được tô vàng)</div>
                    <div class="fgrid">
                        <div v-for="(f, fi) in verEditableFields" :key="fi" class="f" :class="{ changed: verChanged(f.label) }">
                            <label>{{ f.label }}</label>
                            <V2BaseInput
                                v-if="f.t === 'number'"
                                v-model="verForm.values[f.label]"
                                type="number"
                                :has-suffix="!!f.unit"
                            >
                                <template v-if="f.unit" #suffix><span class="unit">{{ f.unit }}</span></template>
                            </V2BaseInput>
                            <V2BaseTextarea v-else-if="f.t === 'area'" v-model="verForm.values[f.label]" :rows="2" />
                            <V2BaseSelectInModal
                                v-else-if="f.t === 'select'"
                                v-model="verForm.values[f.label]"
                                :options="asOptions(f.opts)"
                            />
                            <V2BaseInput v-else v-model="verForm.values[f.label]" />
                            <div v-if="verChanged(f.label)" class="oldhint">Bản hiện tại: {{ verOldValue(f.label) }}</div>
                        </div>
                    </div>
                </div>
            </div>

            <template #footer>
                <V2BaseButton light status="warning" size="sm" @click="saveVer">
                    <template #prefix><i class="ri-calendar-schedule-line" /></template>
                    {{ verEditing ? 'Cập nhật lịch hẹn' : 'Lưu phiên bản đã hẹn' }}
                </V2BaseButton>
                <V2BaseButton tertiary size="sm" @click="$refs.verModal.close()">Hủy</V2BaseButton>
            </template>
        </V2BaseModal>

        <!-- ===== MODAL: THÊM/SỬA QUY CHẾ HOA HỒNG ===== -->
        <V2BaseModal
            ref="regModal"
            modal-id="rc-reg-modal"
            :title="regEditing ? 'Sửa quy chế hoa hồng' : 'Thêm quy chế hoa hồng'"
            icon="ri-gift-line"
            size="lg"
        >
            <div class="rc-scope">
            <div class="fieldset">
                <div class="fs-title">Điều kiện áp dụng</div>
                <div class="fgrid">
                    <div class="f">
                        <label>Áp dụng cho tính chất hàng</label>
                        <V2BaseSelectInModal v-model="regForm.applyFor" :options="asOptions(['Hàng hóa', 'Dịch vụ', 'Hàng khuyến mãi'])" />
                    </div>
                    <div class="f">
                        <label>Bảng giá áp dụng</label>
                        <V2BaseSelectInModal v-model="regForm.priceList" :options="asOptions(['Giá bán lẻ', 'Giá đại lý', 'Giá dịch vụ', 'Giá dự án'])" />
                    </div>
                </div>
            </div>

            <div class="fieldset eff-fs">
                <div class="fs-title">Hẹn ngày áp dụng (theo dòng)</div>
                <div class="eff-row">
                    <div class="f">
                        <label>Hiệu lực từ ngày</label>
                        <V2BaseDatePicker v-model="regForm.eff" />
                    </div>
                    <div class="f grow">
                        <label>Trạng thái</label>
                        <V2BaseSelectInModal v-model="regForm.status" :options="asOptions(['Đang áp dụng', 'Chờ áp dụng', 'Ngừng'])" />
                    </div>
                </div>
                <div class="field-hint">
                    Đặt ngày <b>trong tương lai</b> → dòng này tự áp dụng đúng ngày (trạng thái “Chờ áp dụng”); phiếu đã
                    lập giữ nguyên quy chế cũ.
                </div>
            </div>

            <div class="fieldset">
                <div class="fs-title">So sánh giá net (khoảng chênh lệch)</div>
                <div class="fgrid">
                    <div class="f">
                        <label>Toán tử từ</label>
                        <V2BaseSelectInModal v-model="regForm.opFrom" :options="asOptions(['Lớn hơn', 'Lớn hơn bằng'])" />
                    </div>
                    <div class="f">
                        <label>Giá net từ</label>
                        <V2BaseInput v-model="regForm.netFrom" type="number" has-suffix><template #suffix><span class="unit">%</span></template></V2BaseInput>
                    </div>
                    <div class="f">
                        <label>Toán tử đến</label>
                        <V2BaseSelectInModal v-model="regForm.opTo" :options="asOptions(['Nhỏ hơn', 'Nhỏ hơn bằng', '—'])" />
                    </div>
                    <div class="f">
                        <label>Giá net đến</label>
                        <V2BaseInput v-model="regForm.netTo" type="number" has-suffix><template #suffix><span class="unit">%</span></template></V2BaseInput>
                    </div>
                </div>
            </div>

            <div class="rate2">
                <div class="fieldset">
                    <div class="fs-title">Thưởng năng suất THÁNG</div>
                    <V2BaseInput v-model="regForm.nsMonth" type="number" has-suffix><template #suffix><span class="unit">%</span></template></V2BaseInput>
                </div>
                <div class="fieldset">
                    <div class="fs-title">Thưởng năng suất QUÝ</div>
                    <V2BaseInput v-model="regForm.nsQuarter" type="number" has-suffix><template #suffix><span class="unit">%</span></template></V2BaseInput>
                </div>
            </div>

            <div class="fieldset">
                <div class="fs-title">Phân chia thưởng theo Hợp đồng (%)</div>
                <div class="rate3">
                    <div class="f"><label>Trưởng phòng</label><V2BaseInput v-model="regForm.hdTp" type="number" /></div>
                    <div class="f"><label>Trưởng bộ phận</label><V2BaseInput v-model="regForm.hdTbp" type="number" /></div>
                    <div class="f"><label>Nhân viên</label><V2BaseInput v-model="regForm.hdNv" type="number" /></div>
                </div>
            </div>

            <div class="fieldset">
                <div class="fs-title">Phân chia thưởng theo Năng suất (%)</div>
                <div class="rate3">
                    <div class="f"><label>Trưởng phòng</label><V2BaseInput v-model="regForm.nsTp" type="number" /></div>
                    <div class="f"><label>Trưởng bộ phận</label><V2BaseInput v-model="regForm.nsTbp" type="number" /></div>
                    <div class="f"><label>Nhân viên</label><V2BaseInput v-model="regForm.nsNv" type="number" /></div>
                </div>
            </div>
            </div>

            <template #footer>
                <V2BaseButton primary size="sm" @click="saveReg">
                    <template #prefix><i class="ri-save-3-line" /></template>
                    Lưu quy chế
                </V2BaseButton>
                <V2BaseButton tertiary size="sm" @click="$refs.regModal.close()">Hủy</V2BaseButton>
            </template>
        </V2BaseModal>
    </div>
</template>

<script>
import V2BaseButton from '@/components/V2BaseButton.vue'
import V2BaseInput from '@/components/V2BaseInput.vue'
import V2BaseTextarea from '@/components/V2BaseTextarea.vue'
import V2BaseSelect from '@/components/V2BaseSelect.vue'
import V2BaseSelectInModal from '@/components/V2BaseSelectInModal.vue'
import V2BaseCurrencyInput from '@/components/V2BaseCurrencyInput.vue'
import V2BaseDatePicker from '@/components/V2BaseDatePicker.vue'
import V2BaseModal from '@/components/modal/V2BaseModal.vue'
import { DATA, HIST, SCOPE_UNITS, CURRENT_COMPANY, canHenTab } from './data.js'

const ICON_MAP = {
    cog: 'ri-settings-3-line',
    doc: 'ri-file-list-3-line',
    tech: 'ri-tools-line',
    price: 'ri-price-tag-3-line',
    cut: 'ri-scissors-cut-line',
    market: 'ri-bar-chart-grouped-line',
    debt: 'ri-bank-card-line',
    box: 'ri-inbox-line',
    goods: 'ri-archive-line',
    cal: 'ri-calendar-line',
    gift: 'ri-gift-line',
    check: 'ri-shield-check-line',
}

export default {
    layout: 'default-sidebar',
    components: {
        V2BaseButton,
        V2BaseInput,
        V2BaseTextarea,
        V2BaseSelect,
        V2BaseSelectInModal,
        V2BaseCurrencyInput,
        V2BaseDatePicker,
        V2BaseModal,
    },
    head() {
        return { title: 'Khai Quy chế – Cấu hình' }
    },
    data() {
        return {
            // ⚠️ Dữ liệu MOCK — clone sâu để chỉnh được trên UI mà không đụng module gốc.
            model: JSON.parse(JSON.stringify(DATA)),
            history: HIST,
            currentCompany: CURRENT_COMPANY,
            scope: 'company', // 'company' | 'department'
            groupIdx: 0,
            unitType: 'dept', // 'dept' | 'part'
            selectedUnitId: SCOPE_UNITS[0].id,
            opOptions: ['Lớn hơn', 'Lớn hơn bằng', 'Nhỏ hơn', 'Nhỏ hơn bằng', '—'],

            // modal hẹn phiên bản
            verGroup: null,
            verEditing: false,
            verForm: { date: '', note: '', values: {} },

            // modal quy chế hoa hồng
            regEditing: false,
            regForm: {},
        }
    },
    computed: {
        unitOptions() {
            return SCOPE_UNITS.map((u) => ({ id: u.id, name: u.name }))
        },
        selectedUnit() {
            return SCOPE_UNITS.find((u) => u.id === this.selectedUnitId) || SCOPE_UNITS[0]
        },
        selectedUnitName() {
            return this.selectedUnit ? this.selectedUnit.name : ''
        },
        curScopeMeta() {
            return this.model[this.scope]
        },
        curGroups() {
            const groups = this.model[this.scope].groups
            if (this.scope === 'department' && this.unitType === 'part') {
                return groups.filter((g) => !g.deptOnly)
            }
            return groups
        },
        curGroup() {
            return this.curGroups[this.groupIdx] || this.curGroups[0]
        },
        curHistory() {
            return this.history[this.scope] || []
        },
        ladderSum() {
            const p = this.curGroup && this.curGroup.progressive
            return p ? Number(p.tp) + Number(p.tbp) + Number(p.nv) : 0
        },
        verEditableFields() {
            if (!this.verGroup || !this.verGroup.fields) return []
            const skip = ['logo', 'subtable', 'date', 'tags', 'toggles']
            return this.verGroup.fields.filter((f) => !skip.includes(f.t))
        },
    },
    watch: {
        // đổi phòng ban → nếu group hiện tại bị ẩn (deptOnly) thì về nhóm đầu
        curGroups() {
            if (this.groupIdx >= this.curGroups.length) this.groupIdx = 0
        },
    },
    methods: {
        iconClass(key) {
            return ICON_MAP[key] || 'ri-checkbox-blank-circle-line'
        },
        asOptions(arr) {
            return (arr || []).map((v) => ({ id: v, name: v }))
        },
        fmtDate(d) {
            if (!d) return '—'
            const p = String(d).split('-')
            return p.length === 3 ? `${p[2]}/${p[1]}/${p[0]}` : d
        },
        canHen(gid) {
            return canHenTab(gid)
        },
        noHenReason(gid) {
            if (gid === 'chung') return 'nhận diện & thông tin công ty'
            if (gid === 'thitruong') return 'cơ cấu tổ chức / danh mục thị trường'
            return 'mốc ngày cố định theo năm'
        },
        groupCount(it) {
            if (it.type === 'grid') return it.rows.length
            if (it.type === 'ladder') return it.ladder.length
            return it.fields ? it.fields.length : 0
        },
        groupPending(it) {
            if (it.type === 'grid' && it.rows) return it.rows.filter((r) => r[7] === 'wait').length
            return (it.pending || []).length
        },
        statusText(s) {
            return s === 'ok' ? 'Đang áp dụng' : s === 'wait' ? 'Chờ áp dụng' : 'Ngừng'
        },
        setScope(s) {
            this.scope = s
            this.groupIdx = 0
        },
        onUnitChange() {
            this.unitType = this.selectedUnit.type || 'dept'
            this.groupIdx = 0
        },
        onSave() {
            // TODO(logic): gọi API lưu cấu hình theo phạm vi. Hiện chỉ UI mock.
            this.$toast && this.$toast.success('Đã lưu (demo UI — chưa nối API).')
        },
        onCancel() {
            this.model = JSON.parse(JSON.stringify(DATA))
        },

        /* ----- modal hẹn phiên bản ----- */
        openVer(group, pIdx) {
            this.verGroup = group
            this.verEditing = typeof pIdx === 'number'
            const p = this.verEditing ? group.pending[pIdx] : null
            const values = {}
            this.verEditableFields.forEach((f) => {
                values[f.label] = f.val
            })
            if (p) p.changes.forEach((c) => { values[c.label] = c.new })
            this.verForm = { date: p ? p.date : '', note: p ? p.note : '', values }
            this.$refs.verModal.show()
        },
        verOldValue(label) {
            const f = this.verEditableFields.find((x) => x.label === label)
            return f ? f.val : ''
        },
        verChanged(label) {
            return String(this.verForm.values[label]) !== String(this.verOldValue(label))
        },
        saveVer() {
            // TODO(logic): tạo/ cập nhật bản ghi phiên bản đã hẹn (effective_from, status).
            this.$refs.verModal.close()
        },

        /* ----- modal quy chế hoa hồng ----- */
        openReg(i) {
            const row = typeof i === 'number' && this.curGroup.rows ? this.curGroup.rows[i] : null
            this.regEditing = !!row
            const hd = row ? row[5].split(' / ') : ['40', '30', '30']
            const ns = row ? row[6].split(' / ') : ['50', '30', '20']
            this.regForm = {
                applyFor: row ? row[0] : 'Hàng hóa',
                priceList: row ? row[1] : 'Giá bán lẻ',
                eff: row ? row[8] : '2026-01-01',
                status: row ? this.statusText(row[7]) : 'Đang áp dụng',
                opFrom: 'Lớn hơn bằng',
                netFrom: 0,
                opTo: 'Nhỏ hơn bằng',
                netTo: 5,
                nsMonth: row ? row[3] : 0,
                nsQuarter: row ? row[4] : 0,
                hdTp: hd[0], hdTbp: hd[1], hdNv: hd[2],
                nsTp: ns[0], nsTbp: ns[1], nsNv: ns[2],
            }
            this.$refs.regModal.show()
        },
        saveReg() {
            // TODO(logic): lưu 1 dòng quy chế hoa hồng (kèm hẹn ngày theo dòng).
            this.$refs.regModal.close()
        },
    },
}
</script>

<style lang="scss" scoped>
// `.rc-scope` = lớp bọc nội dung 2 modal. b-modal bị teleport ra <body> nên nằm NGOÀI `.rc-page`
// -> phải cho selector áp cho cả `.rc-scope` thì biến màu (--teal…) + primitive form (.fieldset,
// .fgrid, .f, .rate3…) mới ăn cho nội dung modal. Slot vẫn giữ scope-id nên style scoped vẫn khớp.
.rc-page,
.rc-scope {
    --teal: #0f9e8c;
    --teal-strong: #0c8577;
    --teal-soft: #e3f4f1;
    --card: #ffffff;
    --panel: #f7f9fb;
    --ink: #1c2b3a;
    --ink-2: #5a6b7d;
    --ink-3: #8a99a8;
    --line: #e3e8ee;
    --line-2: #eef2f6;
    --ok: #0f9e6e;
    --ok-soft: #e4f6ee;
    --idle: #94a3b2;
    --idle-soft: #eef1f4;
    --warn: #c9772a;
    --warn-soft: #faeede;
    --radius: 10px;
    --sh-sm: 0 1px 2px rgba(16, 38, 58, 0.06), 0 1px 3px rgba(16, 38, 58, 0.05);

    max-width: 1320px;
    margin: 0 auto;
    padding: 14px 8px 40px;
    color: var(--ink);
    font-size: 14px;

    b { font-weight: 700; }

    /* page head */
    .page-head { display: flex; align-items: flex-start; gap: 13px; margin-bottom: 16px;
        .ico { width: 40px; height: 40px; border-radius: 11px; background: var(--teal-soft); color: var(--teal-strong);
            display: grid; place-items: center; flex: 0 0 auto; font-size: 21px; }
        h1 { margin: 0; font-size: 20px; font-weight: 800; }
        p { margin: 2px 0 0; color: var(--ink-2); font-size: 13px; max-width: 900px; }
    }

    /* scope bar */
    .scopebar { background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); box-shadow: var(--sh-sm);
        padding: 14px 16px; display: flex; align-items: flex-end; gap: 18px; flex-wrap: wrap; margin-bottom: 18px; }
    .scope-field { display: flex; flex-direction: column; gap: 7px;
        > span { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em; color: var(--ink-3); } }
    .company-badge { display: inline-flex; align-items: center; gap: 9px; background: var(--teal-soft); color: var(--teal-strong);
        border: 1px solid var(--teal); border-radius: 9px; padding: 9px 13px; font-size: 13.5px; font-weight: 700;
        .lock { font-size: 11px; font-weight: 600; color: var(--ink-3); background: var(--card); border: 1px solid var(--line);
            border-radius: 20px; padding: 2px 9px; } }
    .seg { display: inline-flex; background: var(--panel); border: 1px solid var(--line); border-radius: 9px; padding: 3px;
        button { border: 0; background: transparent; font: inherit; font-size: 13px; font-weight: 600; color: var(--ink-2);
            padding: 8px 15px; border-radius: 7px; cursor: pointer; display: flex; align-items: center; gap: 7px;
            .n { width: 17px; height: 17px; border-radius: 50%; background: var(--line); color: var(--ink-2); font-size: 11px;
                display: grid; place-items: center; font-weight: 700; }
            &.on { background: var(--teal); color: #fff; box-shadow: var(--sh-sm);
                .n { background: rgba(255, 255, 255, 0.25); color: #fff; } } } }
    .scope-spacer { flex: 1 1 auto; }
    .savebar { display: flex; gap: 9px; }

    /* hint */
    .hint { display: flex; gap: 10px; align-items: flex-start; background: var(--panel); border: 1px solid var(--line);
        border-left: 3px solid var(--teal); border-radius: 8px; padding: 11px 13px; font-size: 12.5px; color: var(--ink-2);
        margin-bottom: 18px;
        i { flex: 0 0 auto; color: var(--teal-strong); font-size: 16px; }
        b { color: var(--ink); }
        &.intro .hen-inline { color: var(--warn); } }

    /* master-detail */
    .md { display: grid; grid-template-columns: 270px 1fr; gap: 18px; align-items: start; }
    @media (max-width: 820px) { .md { grid-template-columns: 1fr; } }

    .grouplist { background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); box-shadow: var(--sh-sm);
        overflow: hidden;
        h3 { margin: 0; padding: 14px 16px 12px; font-size: 11px; font-weight: 800; letter-spacing: 0.08em;
            text-transform: uppercase; color: var(--ink-3); border-bottom: 1px solid var(--line-2); }
        .items { padding: 8px; } }
    .gitem { display: flex; align-items: center; gap: 11px; width: 100%; text-align: left; border: 0; background: transparent;
        font: inherit; padding: 10px 11px; border-radius: 8px; cursor: pointer; color: var(--ink); position: relative;
        .gi { width: 30px; height: 30px; border-radius: 8px; background: var(--panel); color: var(--ink-2); display: grid;
            place-items: center; flex: 0 0 auto; font-size: 16px; }
        .gt { flex: 1; min-width: 0;
            b { display: block; font-weight: 600; font-size: 13.5px; line-height: 1.25; }
            small { color: var(--ink-3); font-size: 11.5px; } }
        .hen-mark { display: flex; align-items: center; color: var(--warn); flex: 0 0 auto; }
        .badge { background: var(--line); color: var(--ink-2); border-radius: 20px; font-size: 11px; font-weight: 700;
            padding: 2px 8px; min-width: 22px; text-align: center; }
        &:hover { background: var(--panel); }
        &.on { background: var(--teal-soft);
            .gi { background: var(--teal); color: #fff; }
            .gt b { color: var(--teal-strong); }
            .badge { background: var(--teal); color: #fff; }
            &::before { content: ''; position: absolute; left: 0; top: 8px; bottom: 8px; width: 3px; border-radius: 3px;
                background: var(--teal); } } }

    .detail { background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); box-shadow: var(--sh-sm);
        min-height: 420px; overflow: hidden; }
    .detail-head { padding: 17px 20px 0;
        .dh-title { display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap; }
        h2 { margin: 0; font-size: 16.5px; font-weight: 800; }
        p { margin: 3px 0 0; color: var(--ink-2); font-size: 12.5px; }
        .dh-chips { display: flex; gap: 8px; align-items: center; } }
    .scope-chip { font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 20px;
        &.chip-com { background: var(--teal-soft); color: var(--teal-strong); }
        &.chip-dep { background: #f0e9f7; color: #7a5aa6; }
        &.unit { background: var(--panel); color: var(--ink-2); border: 1px solid var(--line); } }
    .note-inline { font-size: 12px; color: var(--warn); background: var(--warn-soft); border-radius: 6px; padding: 3px 9px;
        font-weight: 600; margin-left: 6px; }
    .detail-body { padding: 20px; }

    /* form grid */
    .fgrid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px 22px; }
    .f { display: flex; flex-direction: column; gap: 6px;
        &.wide { grid-column: 1 / -1; }
        &.grow { flex: 1; min-width: 240px; }
        label { font-size: 12.5px; font-weight: 600; color: var(--ink);
            .fixed-tag { color: var(--idle); font-weight: 500; font-size: 11px; } }
        .unit { font-size: 12px; color: var(--ink-3); font-weight: 600; }
        &.changed ::v-deep input { border-color: var(--warn); background: var(--warn-soft); }
        .oldhint { font-size: 11px; color: var(--warn); font-weight: 600; } }

    .tagbox { display: flex; flex-wrap: wrap; gap: 6px; padding: 8px; border: 1px solid var(--line); border-radius: 8px;
        min-height: 42px; background: var(--card);
        .tag { background: var(--teal-soft); color: var(--teal-strong); border-radius: 6px; font-size: 12px; font-weight: 600;
            padding: 4px 9px; display: flex; align-items: center; gap: 6px;
            span { opacity: 0.6; cursor: pointer; } }
        .tag-add { color: var(--ink-3); font-size: 12.5px; align-self: center; padding: 0 4px; } }

    .toggles { display: flex; flex-wrap: wrap; gap: 9px;
        .tg { display: flex; align-items: center; gap: 9px; border: 1px solid var(--line); border-radius: 8px; padding: 9px 13px;
            font-size: 13px; font-weight: 500; cursor: pointer; user-select: none;
            .sw { width: 34px; height: 19px; border-radius: 20px; background: var(--line); position: relative; flex: 0 0 auto;
                transition: background 0.15s;
                &::after { content: ''; position: absolute; top: 2px; left: 2px; width: 15px; height: 15px; border-radius: 50%;
                    background: #fff; box-shadow: 0 1px 2px rgba(0, 0, 0, 0.25); transition: left 0.15s; } }
            &.on .sw { background: var(--teal); &::after { left: 17px; } } } }

    .upload { display: flex; align-items: center; gap: 14px;
        .ph { width: 70px; height: 70px; border-radius: 10px; border: 1.5px dashed var(--line); display: grid; place-items: center;
            color: var(--ink-3); background: var(--panel); font-size: 26px; }
        .default-note { font-size: 11.5px; color: var(--ink-3); margin-top: 7px; } }

    /* tables */
    .tbl-tools { display: flex; justify-content: space-between; align-items: center; gap: 12px; margin: 4px 0 12px;
        flex-wrap: wrap; .muted { font-size: 12.5px; color: var(--ink-2); } }
    .tbl-wrap { border: 1px solid var(--line); border-radius: 9px; overflow: auto; &.flat { border: 0; border-radius: 0; } }
    table.grid { width: 100%; border-collapse: collapse; font-size: 13px;
        th, td { text-align: left; padding: 10px 13px; border-bottom: 1px solid var(--line-2); white-space: nowrap; }
        thead th { background: var(--panel); font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;
            color: var(--ink-3); position: sticky; top: 0;
            small { font-weight: 400; text-transform: none; } }
        tbody tr:last-child td { border-bottom: 0; }
        tbody tr:hover { background: var(--panel); }
        tbody tr.row-wait { background: var(--warn-soft); }
        td.num { font-variant-numeric: tabular-nums; text-align: right; }
        td.eff, td.t { color: var(--ink); font-variant-numeric: tabular-nums; }
        .who { font-weight: 600; color: var(--ink); } }
    .cellinput { width: 130px; border: 1px solid var(--line); border-radius: 7px; padding: 6px 9px; font: inherit;
        text-align: right; background: var(--card); color: var(--ink); }
    .cellsel { width: 130px; border: 1px solid var(--line); border-radius: 7px; padding: 6px 9px; font: inherit;
        background: var(--card); color: var(--ink); }
    .cell-unit { display: flex; align-items: center; gap: 5px; .cellinput { width: 80px; } }
    .split3 { display: flex; gap: 3px; font-variant-numeric: tabular-nums;
        span { background: var(--panel); border: 1px solid var(--line-2); border-radius: 5px; padding: 2px 6px; font-size: 11.5px; } }
    .tbl-foot { display: flex; justify-content: space-between; align-items: center; margin-top: 12px; font-size: 12.5px;
        color: var(--ink-3); }

    .pill { display: inline-flex; align-items: center; gap: 6px; font-size: 11.5px; font-weight: 700; padding: 4px 10px;
        border-radius: 20px;
        &::before { content: ''; width: 6px; height: 6px; border-radius: 50%; }
        &.ok { background: var(--ok-soft); color: var(--ok); &::before { background: var(--ok); } }
        &.wait { background: var(--warn-soft); color: var(--warn); &::before { background: var(--warn); } }
        &.idle { background: var(--idle-soft); color: var(--idle); &::before { background: var(--idle); } } }

    .iconbtn { border: 1px solid var(--line); background: var(--card); border-radius: 7px; width: 30px; height: 30px;
        display: inline-grid; place-items: center; cursor: pointer; color: var(--ink-2);
        &:hover { border-color: var(--ink-3); color: var(--ink); }
        &.danger:hover { border-color: #e0918a; color: #c94f42; } }
    .rowact { display: flex; gap: 6px; }

    /* version bar */
    .verbar { display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap;
        background: var(--panel); border: 1px solid var(--line); border-left: 3px solid var(--teal); border-radius: 9px;
        padding: 12px 14px; margin-bottom: 16px;
        &.has-pend { border-left-color: var(--warn); }
        .vcur { font-size: 12.5px; color: var(--ink-2); display: flex; align-items: center; gap: 8px; flex-wrap: wrap;
            .lb { font-size: 10.5px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: var(--ink-3); }
            b { color: var(--ink); } }
        .vact { display: flex; gap: 9px; align-items: center; flex-wrap: wrap; } }
    .vpend { font-size: 11.5px; color: var(--warn); font-weight: 600; background: var(--warn-soft); border-radius: 20px;
        padding: 5px 12px; display: inline-flex; align-items: center; gap: 6px; }

    .vqueue { border: 1px solid var(--line); border-radius: 9px; overflow: hidden; margin-bottom: 16px;
        .vq-head { background: var(--warn-soft); color: var(--warn); font-size: 11px; font-weight: 800; text-transform: uppercase;
            letter-spacing: 0.05em; padding: 9px 13px; display: flex; align-items: center; gap: 8px; } }
    .vq-item { display: flex; align-items: flex-start; gap: 12px; padding: 12px 13px; border-top: 1px solid var(--line-2);
        .vq-date { font-weight: 700; color: var(--ink); background: var(--panel); border: 1px solid var(--line); border-radius: 7px;
            padding: 5px 10px; font-size: 12.5px; white-space: nowrap; display: flex; align-items: center; gap: 6px; }
        .vq-body { flex: 1; min-width: 0; }
        .vq-changes { display: flex; flex-direction: column; gap: 4px; font-size: 12.5px; color: var(--ink-2);
            .lbl { color: var(--ink); }
            .old { text-decoration: line-through; color: var(--ink-3); }
            .new { color: var(--warn); font-weight: 700; } }
        .vq-meta { font-size: 11px; color: var(--ink-3); margin-top: 6px; }
        .vq-act { display: flex; gap: 6px; flex: 0 0 auto; } }

    .snap-note { display: flex; gap: 8px; align-items: flex-start; margin-top: 18px; font-size: 11.5px; color: var(--ink-2);
        background: var(--teal-soft); border-radius: 7px; padding: 9px 11px; line-height: 1.5;
        i { flex: 0 0 auto; color: var(--teal-strong); font-size: 15px; } b { color: var(--ink); } }
    .no-hen-note { display: flex; gap: 9px; align-items: flex-start; background: var(--idle-soft); border: 1px solid var(--line);
        border-radius: 8px; padding: 10px 13px; font-size: 12px; color: var(--ink-2); margin-bottom: 18px;
        i { flex: 0 0 auto; color: var(--idle); font-size: 15px; } }

    .rateblock { margin-top: 20px; border: 1px solid var(--line); border-radius: 10px; padding: 15px 16px; background: var(--panel);
        .rb-title { font-size: 11.5px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.06em; color: var(--teal-strong);
            margin-bottom: 13px; display: flex; align-items: center; gap: 8px;
            .sum { margin-left: auto; font-size: 11px; font-weight: 700; color: var(--ink-3); text-transform: none; letter-spacing: 0; } } }
    .rate3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
    .rate2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; margin-bottom: 14px; }

    /* history */
    .history { background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); box-shadow: var(--sh-sm);
        margin-top: 18px; overflow: hidden;
        .hh { display: flex; justify-content: space-between; align-items: center; padding: 14px 18px;
            border-bottom: 1px solid var(--line-2);
            h3 { margin: 0; font-size: 13.5px; font-weight: 700; display: flex; align-items: center; gap: 9px; color: var(--ink);
                i { color: var(--teal-strong); }
                .muted { color: var(--ink-3); font-weight: 500; } }
            .lnk { color: var(--teal-strong); font-size: 12.5px; font-weight: 700; text-decoration: none; display: flex;
                align-items: center; gap: 6px; } }
        .badge-hen { display: inline-flex; align-items: center; gap: 5px; font-size: 10.5px; font-weight: 700; color: var(--warn);
            background: var(--warn-soft); border-radius: 20px; padding: 2px 8px; margin-left: 6px; } }

    /* modal internals */
    .fieldset { border: 1px solid var(--line); border-radius: 10px; padding: 14px 15px; margin-bottom: 14px;
        &:last-child { margin-bottom: 0; }
        &.eff-fs { border-color: var(--warn); background: var(--warn-soft); }
        .fs-title { font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.06em; color: var(--teal-strong);
            margin-bottom: 12px; }
        &.eff-fs .fs-title { color: var(--warn); } }
    .field-hint { font-size: 11.5px; color: var(--ink-3); margin-top: 8px; b { color: var(--warn); } }
    .eff-row { display: flex; gap: 14px; align-items: flex-end; flex-wrap: wrap; .f { min-width: 200px; } }
}

// Trong modal: bỏ khung trang (max-width/căn giữa/padding) mà `.rc-page` áp dụng chung.
.rc-scope {
    max-width: none;
    margin: 0;
    padding: 0;
}
</style>
