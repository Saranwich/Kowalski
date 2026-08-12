# Kowalski

เลขาส่วนตัวบน Telegram สำหรับใช้คนเดียว — จดของที่ต้องจำ (การบ้าน / นัด / อาหาร / รายรับ-รายจ่าย),
เตือนก่อนถึงเวลา, และตอบคำถามเกี่ยวกับอดีตได้เหมือนเพื่อนที่จำเราได้

> **สถานะ:** ยังไม่เริ่มเขียนโค้ด — ตอนนี้มีแค่โครง `uv init` เอกสารนี้อธิบายว่ากำลังจะสร้างอะไรและสร้างยังไง

---

## บอททำอะไร

| ความสามารถ | หัวใจ |
|---|---|
| คุยผ่าน Telegram | ประตูเข้า-ออกทั้งหมด |
| **จด** การบ้าน / ประชุม / อาหาร / รายรับ-รายจ่าย ลง DB + สรุป/export ตาราง | ความจำระยะยาว |
| **แจ้งเตือน** ล่วงหน้า | บอททักเราก่อนได้ |
| **ตอบเรื่องอดีต** จากข้อมูลที่จดไว้ | ค้น + เรียบเรียง |

---

## Stack

| ชั้น | ใช้ |
|---|---|
| แชท | Telegram + `python-telegram-bot` (polling) |
| ภาษา | Python 3.13 |
| เก็บข้อมูล | SQLite ไฟล์เดียว (`penguin.db`) หลายตาราง |
| ตรวจ input | Pydantic (validate output จาก LLM) |
| สมอง | LLM (Gemini free tier / Claude) + structured output + tool calling |
| ค้นอดีต | FTS5 (native ใน SQLite) → `sqlite-vec` ทีหลังถ้าต้อง semantic |
| แจ้งเตือน | APScheduler (jobstore เก็บใน SQLite เดียวกัน) |
| ดู/export | Datasette / `pandas.to_excel` |
| แพ็กเกจ/env | uv |
| รัน | VM (Oracle Cloud Free Tier) + systemd → Docker ทีหลัง |

ค่าใช้จ่ายเป้าหมาย ~0 บาท/เดือน (VM free tier + LLM free tier)

---

## สถาปัตยกรรม

LLM อยู่ 2 ตำแหน่งเสมอ — **ขาเข้า** (ภาษาคน → ข้อมูลมีโครงสร้าง) และ **ขาออก** (ข้อมูล → ภาษาคน)
ตรงกลางเป็น SQLite ล้วนๆ

```
penguin.db
├── profile      ตัวตนเจ้านาย (ชื่อ, เรียนอะไร, ชอบอะไร)
├── expenses     รายรับ-รายจ่าย
├── meals        อาหาร
├── schedule     การบ้าน/ประชุม/นัด  ← มีคอลัมน์ job_id ชี้ไป APScheduler
├── messages     ประวัติแชทระยะสั้น
├── notes_fts    โน้ตสำหรับ FTS5
└── apscheduler  jobstore ของงานแจ้งเตือน
```

**ตัวอย่าง flow — จดรายจ่าย**

```
พิมพ์ → Telegram → บอทรับ (polling)
  → ส่งข้อความ + tools/schema ให้ LLM
  → LLM เลือก add_expense + คืน {date, category, amount}
  → Pydantic ตรวจ
  → โค้ดเรา INSERT ลง SQLite
  → บอทตอบยืนยัน
```

**ตัวอย่าง flow — ถามอดีต**

```
"เดือนก่อนกินอะไรแถวมอบ้าง"
  → ค้น FTS5 / SELECT ดึงแถวเก่าที่เกี่ยวข้อง
  → ยัดแถวพวกนั้นเป็น context ให้ LLM
  → LLM เรียบเรียงตอบ
```

---

## กฎที่ยึด

- **LLM ไม่แตะ DB ตรงๆ** — LLM เลือก tool + กรอก args เท่านั้น, Pydantic ตรวจ, โค้ดเราเป็นเจ้าของทุก SQL
  LLM ไม่เคยคาย SELECT/INSERT ออกมาเอง
- **Pydantic ใช้ที่ "ขอบ" เท่านั้น** — เพราะ output ของ LLM คือ trust boundary จริง
  1 model reuse ทั้งเส้น (LLM → validate → `model_dump()` → INSERT) ไม่มี ORM/repository layer หนาๆ
- **แยกความจำสั้น/ยาว** — สั้น = `messages` sliding window ~20 ข้อความล่าสุด,
  ยาว = `profile` + ข้อมูลจริงที่ **ค้นเฉพาะที่เกี่ยว** แล้วค่อยแปะ ไม่เคยแปะประวัติทั้งชีวิต
- **แก้/ลบของเก่าต้อง sync สองก้อน** — นัด 1 อันผูกกับทั้งแถวใน `schedule` และ job ใน APScheduler
  ขั้นตอน: หาให้เจอ → เจอหลายอันถามกลับ / เจอ 0 อันบอกว่าไม่เจอ → ลบต้องยืนยันเสมอ → แก้ทั้งสองก้อน
- **เริ่มเบาที่สุดที่ทำงานได้** — Postgres / Redis / Docker / webhook รอจนเจอ pain จริงค่อยเติมทีละชิ้น

---

## เริ่มใช้งาน

```bash
uv sync
uv run main.py
```

ต้องมี `.env` (ไม่เข้า git):

```
TELEGRAM_BOT_TOKEN=...
LLM_API_KEY=...
```

---

## Roadmap

**เฟส 1 — ทำให้บอทเดินได้**
- [ ] รับ-ส่งข้อความผ่าน `python-telegram-bot` (polling)
- [ ] SQLite schema + INSERT/SELECT ผ่าน `sqlite3`
- [ ] LLM tool calling + Pydantic validation (แกนหลักของทั้งระบบ)
- [ ] APScheduler + แจ้งเตือนที่รอดหลังรีสตาร์ท
- [ ] แก้/ลบนัดแบบ sync สองก้อน

**เฟส 1.5 — ขึ้น VM**
- [ ] Oracle Cloud Free Tier VM + SSH
- [ ] systemd unit + `journalctl`

**เฟส 2 — ทีหลัง (YAGNI จนกว่าจะเจอ pain)**
- [ ] FTS5 ค้นอดีตแบบลึกขึ้น
- [ ] Datasette / export Excel
- [ ] Docker
- [ ] Rolling summary ตอนแชทยาวจน context window ไม่พอ
- [ ] `sqlite-vec` semantic search
- [ ] LINE adapter ตัวที่สอง
- [ ] Postgres (เฉพาะถ้ามีผู้ใช้จริงหลายคน)

---

## เพดานของ stack

เพิ่มฟีเจอร์/ตาราง/tool ใหม่, รับเสียง-รูป, semantic search, หน้าเว็บ — ทำได้เลยไม่ต้องแตะ stack

กำแพงจริงมีอันเดียวที่สำคัญ: **หลายคนเขียนพร้อมกันเยอะ** → สลับ SQLite เป็น Postgres
(SQL/Pydantic แทบไม่เปลี่ยน) ซึ่งใช้คนเดียวจะไม่ชน
