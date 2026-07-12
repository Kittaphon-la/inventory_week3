# Week 3 — Resource, Communication, Quality Gates, SCM และ Regression Testing

> หมายเหตุ: จากบอร์ดที่ได้รับ ช่อง Project Manager ยังแสดงเป็น “(ชื่อ)” จึงใส่เป็น **ชื่อ PM (ยังไม่ระบุ)** ไว้ก่อน ส่วนชื่ออื่นถอดจากภาพที่ส่งมา กรุณาตรวจการสะกดก่อนส่งอาจารย์

## 1. สมาชิกและบทบาท

| บทบาท | สมาชิก |
|---|---|
| Project Manager | ชื่อ PM (ยังไม่ระบุ) |
| Tech Lead | นางสาว กฤตพร แหลมไทย |
| Developer | นายณัฐกิตติ์ แก้วคำยศ |
| QA / Tester | นายวรวิทย์ สุวรรณ |

## 2. RACI Matrix

คำย่อ: **R** = Responsible, **A** = Accountable, **C** = Consulted, **I** = Informed

| กิจกรรม | ชื่อ PM (ยังไม่ระบุ) | นางสาว กฤตพร แหลมไทย | นายณัฐกิตติ์ แก้วคำยศ | นายวรวิทย์ สุวรรณ |
|---|---:|---:|---:|---:|
| ยืนยันขอบเขตและแผนงาน Week 3 | A/R | C | I | I |
| เก็บ Baseline v1.0 และตั้งค่า Repository | I | A/R | R | C |
| ออกแบบ Branching Strategy | I | A/R | C | C |
| Refactor และเปลี่ยนชื่อตัวแปร | I | A | R | C |
| เพิ่ม Input Validation | I | A | R | C |
| ปรับปรุงการอ่านและบันทึก JSON | I | A | R | C |
| ออกแบบ Test Cases | I | C | R | A/R |
| เขียนและรัน PyTest | I | C | R | A/R |
| Code Review / Pull Request Review | I | A/R | R | C |
| ตรวจ Quality Gate ก่อน Merge | I | A | C | R |
| Merge เข้า `develop` | I | A/R | R | C |
| อนุมัติ Release เข้า `main` | A | R | C | C |
| อัปเดต Trello และสรุปรายงาน | A/R | C | I | I |

**กฎ:** ในแต่ละกิจกรรมมี Accountable เพียงหนึ่งคน

## 3. Communication Plan

| รายการสื่อสาร | วัตถุประสงค์ | ผู้เข้าร่วม | ช่องทาง | ความถี่/เวลา | หลักฐาน |
|---|---|---|---|---|---|
| Daily Standup | รายงานงานที่เสร็จ งานวันนี้ และ Blocker | สมาชิกทั้งหมด | ห้องเรียน / Google Meet / Discord | ทุกวันที่ทำงาน ไม่เกิน 15 นาที | Standup note |
| Task Update | แสดงสถานะ To Do, Doing, Review, Done | สมาชิกทั้งหมด | Trello | ทันทีเมื่อสถานะเปลี่ยน | Card activity |
| Blocker Alert | แจ้งปัญหาที่ทำให้งานเดินต่อไม่ได้ | ผู้พบปัญหา, Tech Lead, PM | LINE / Discord | แจ้งทันที | ข้อความและลิงก์ Card |
| Code Review | ตรวจคุณภาพและผลกระทบก่อนรวมโค้ด | Tech Lead, Developer, QA | GitHub Pull Request | ทุก Feature ก่อน Merge | Review comment / Approval |
| Test Report | แจ้งผล PyTest และรายการที่ไม่ผ่าน | QA, Developer, Tech Lead | GitHub PR / Trello | ทุกครั้งก่อน Merge | Test output / Screenshot |
| Weekly Review | สรุปความคืบหน้า ความเสี่ยง และงานค้าง | สมาชิกทั้งหมด | Meeting + Trello | ก่อนส่งงานประจำสัปดาห์ | Meeting summary |
| Release Notice | แจ้ง Baseline/Version ใหม่ | PM, Tech Lead, ทีม | GitHub + กลุ่มแชต | เมื่อ Release | Tag และ CHANGELOG |

### Daily Standup Questions
1. เมื่อวานทำอะไรเสร็จแล้ว?
2. วันนี้จะทำงานอะไร?
3. มี Blocker หรือความเสี่ยงอะไร?

## 4. Quality Gates

### Gate 1 — Ready for Development
- [ ] Card มีวัตถุประสงค์และ Acceptance Criteria ชัดเจน
- [ ] ระบุผู้รับผิดชอบและผู้อนุมัติตาม RACI
- [ ] แตก Branch จาก `develop`
- [ ] ตั้งชื่อ Branch ตามรูปแบบที่กำหนด
- [ ] ระบุ Test Cases ที่เกี่ยวข้อง

### Gate 2 — Ready for Pull Request
- [ ] โค้ดรันได้โดยไม่มี Syntax Error
- [ ] ไม่มีการแก้ไข `main` โดยตรง
- [ ] ไม่มีตัวแปรชื่อกำกวมที่เพิ่มใหม่
- [ ] ตรวจสอบ Input Validation แล้ว
- [ ] `python -m pytest -v` ผ่านทั้งหมด
- [ ] Commit มีขนาดเหมาะสมและข้อความสื่อความหมาย
- [ ] อัปเดต Test และ CHANGELOG เมื่อจำเป็น

### Gate 3 — Ready for Merge into `develop`
- [ ] Pull Request อธิบายสิ่งที่เปลี่ยนและผลกระทบ
- [ ] ผ่าน Code Review อย่างน้อย 1 คน
- [ ] QA ยืนยันผล Regression Test
- [ ] ไม่มี Merge Conflict
- [ ] ไม่มี Test ล้มเหลว
- [ ] Trello Card อยู่สถานะ Review
- [ ] Tech Lead อนุมัติ

### Gate 4 — Ready for Release into `main`
- [ ] Integration Test บน `develop` ผ่าน
- [ ] ทุก Card ของ Release อยู่สถานะ Done
- [ ] PM ยืนยันขอบเขตที่ส่งมอบ
- [ ] Tech Lead ยืนยันความเสถียร
- [ ] QA แนบ Test Report
- [ ] อัปเดต Version และ CHANGELOG
- [ ] สร้าง Git Tag ของ Baseline ใหม่
- [ ] สามารถ Rollback ไปยัง Baseline ก่อนหน้าได้

## 5. Definition of Done

งานหนึ่งชิ้นถือว่า **Done** เมื่อ:

1. ทำงานตรงตาม Acceptance Criteria บน Trello
2. โค้ดถูกพัฒนาใน `feature/*` หรือ `fix/*` ไม่ใช่บน `main`
3. โค้ดอ่านง่าย ใช้ชื่อตัวแปรและฟังก์ชันที่สื่อความหมาย
4. มี Input Validation และ Error Handling สำหรับข้อมูลจากผู้ใช้
5. เพิ่มหรือปรับ Test ให้ครอบคลุมพฤติกรรมที่เปลี่ยน
6. PyTest ผ่านทั้งหมด
7. ไม่มี Regression ต่อฟังก์ชันเดิม ได้แก่ Show, Add/Update, Out และ Check Inventory
8. ผ่าน Code Review และแก้ Comment แล้ว
9. Merge เข้า `develop` สำเร็จโดยไม่มี Conflict
10. อัปเดต Trello Card, เอกสาร และ CHANGELOG ที่เกี่ยวข้อง
11. QA ยืนยันผลทดสอบ
12. ผู้มีบทบาท Accountable อนุมัติงาน

## 6. GitFlow Branches

```text
main
└── develop
    ├── feature/refactor-inventory
    ├── feature/input-validation
    ├── feature/json-safety
    ├── test/regression-suite
    └── docs/week3-management
```

### หน้าที่ของ Branch
- `main` — เก็บเฉพาะเวอร์ชันที่เสถียรและพร้อมส่ง
- `develop` — รวมงานที่ผ่านการตรวจเพื่อทดสอบร่วมกัน
- `feature/*` — พัฒนาฟีเจอร์หรือ Refactor
- `fix/*` — แก้บั๊ก
- `test/*` — เพิ่มหรือปรับชุดทดสอบ
- `docs/*` — เอกสาร RACI, Communication, Quality Gate และรายงาน

## 7. ตัวอย่างคำสั่ง Git

```powershell
git init
git add .
git commit -m "chore: establish inventory v1.0 baseline"
git branch -M main

git checkout -b develop
git checkout -b feature/refactor-inventory
```

หลังทำ Refactor:

```powershell
git add test_app.py
git commit -m "refactor: split inventory logic into testable functions"
git checkout develop
git merge --no-ff feature/refactor-inventory
```

ทำ Input Validation:

```powershell
git checkout -b feature/input-validation
git add test_app.py
git commit -m "fix: validate quantity and price input"
git checkout develop
git merge --no-ff feature/input-validation
```

ทำ Regression Test:

```powershell
git checkout -b test/regression-suite
git add tests/test_inventory.py
git commit -m "test: add inventory regression test suite"
git checkout develop
git merge --no-ff test/regression-suite
```

เตรียม Release:

```powershell
python -m pytest -v
git checkout main
git merge --no-ff develop
git tag -a v2.0.0 -m "Inventory System v2.0.0"
```

## 8. ตัวอย่าง Commit Messages

```text
chore: establish inventory v1.0 baseline
refactor: replace global x with descriptive inventory data
refactor: split main menu into reusable functions
fix: validate quantity and price input
fix: reject zero and negative stock withdrawal
fix: save JSON through temporary file
test: add regression tests for stock withdrawal
test: verify inventory total and low-stock alert
docs: add RACI and communication plan
docs: define quality gates and definition of done
chore: update changelog for v2.0.0
```

## 9. คำสั่งติดตั้งและรันทดสอบ

```powershell
python -m pip install pytest
python -m pytest -v
python test_app.py
```
