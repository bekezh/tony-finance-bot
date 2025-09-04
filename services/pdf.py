from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from io import BytesIO

def make_plan_pdf(user, plan, habits):
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    w, h = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(20*mm, h-20*mm, "План ЗОЖ (3 недели)")

    c.setFont("Helvetica", 10)
    tz = user.tz if user else "Asia/Almaty"
    c.drawString(20*mm, h-27*mm, f"Пользователь: tg_id={getattr(user,'tg_id', '-')}, TZ={tz}")

    y = h-40*mm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(20*mm, y, "Привычки:")
    y -= 8*mm
    c.setFont("Helvetica", 10)
    for hbt in habits[:20]:
        c.drawString(22*mm, y, f"• {hbt.title} @ {hbt.reminder_time}  (days_mask={hbt.days_mask})")
        y -= 6*mm
        if y < 30*mm:
            c.showPage(); y = h-20*mm

    c.showPage()
    c.setFont("Helvetica-Bold", 12)
    c.drawString(20*mm, h-20*mm, "План по неделям:")
    c.setFont("Helvetica", 10)

    y = h-30*mm
    if plan and plan.plan_json:
        p = plan.plan_json
    else:
        p = plan or {}
    weeks = p.get("weeks", [])
    for i, wdata in enumerate(weeks, start=1):
        c.drawString(20*mm, y, f"Неделя {i}:")
        y -= 6*mm
        for day in wdata.get("days", []):
            title = day.get("title","Задача")
            dur = day.get("duration_min","-")
            c.drawString(25*mm, y, f"— {title} ({dur} мин)")
            y -= 6*mm
            if y < 20*mm:
                c.showPage(); y = h-20*mm

    c.save()
    pdf_bytes = buf.getvalue()
    buf.close()
    return pdf_bytes
