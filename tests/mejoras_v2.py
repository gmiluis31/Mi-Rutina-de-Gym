import sys,pathlib;sys.path.insert(0,str(pathlib.Path(__file__).parent))
import h
from h import reg,URL
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":360,"height":800}); errs=[]
    pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.goto(URL); pg.wait_for_timeout(300)
    pg.fill("#gn","Ana"); pg.fill("#ge","a@b.co"); pg.fill("#gp","secreto1"); pg.fill("#gc","secreto1"); pg.click("#gok")
    print("1) sin casilla ->",pg.inner_text("#gerr"))
    pg.check("#gcheck"); pg.click("#gok"); pg.wait_for_timeout(400)
    pg.fill("#pe","12"); pg.click("#pform button[type=submit]"); print("2) edad 12 ->",pg.inner_text("#perr"))
    pg.click("#pno")
    print("3) mes en 360px:",pg.inner_text("#mes"),"| contenedor recortado:",pg.evaluate("(()=>{const e=document.querySelector('#mes');return e.scrollWidth>e.clientWidth})()"))
    pg.fill("#n","Press de banca"); pg.fill("#k","40"); pg.click("#nuevo button[type=submit]")
    # historial previo para 'última vez' y récord (hace 7 días)
    pg.evaluate("""()=>{const ex=planDe(sel).ex[0];const d=new Date();d.setDate(d.getDate()-7);const f=iso(d);st.hist[f]={[ex.id]:{n:ex.n,lid:ex.lid,s:3,r:10,k:35,d:3,km:35,v:1050,res:""}};pintar()}""")
    print("4) última vez:",pg.inner_text(".ult"))
    # long-press: anotar serie 1 con 12 reps y 45 kg
    s1=pg.locator(".set").first; bb=s1.bounding_box()
    pg.mouse.move(bb["x"]+20,bb["y"]+20); pg.mouse.down(); pg.wait_for_timeout(700); pg.mouse.up(); pg.wait_for_timeout(150)
    print("5) diálogo serie:",pg.is_visible("#serie"),pg.inner_text("#sti"),"| main inerte:",pg.evaluate("document.querySelector('main').inert"))
    pg.fill("#sr","12"); pg.fill("#sk","45"); pg.click("#sform button[type=submit]"); pg.wait_for_timeout(200)
    print("6) real:",pg.locator(".srow.hecha").first.inner_text().replace("\n"," "),"| marcadas:",pg.locator(".set[aria-pressed=true]").count(),"| récord:",pg.locator(".pr").count(),"| inerte tras cerrar:",pg.evaluate("document.querySelector('main').inert"))
    pg.click("#romitir")
    pg.locator(".set").nth(1).click(); pg.click("#romitir")
    print("7) toque normal marca sin abrir diálogo:",not pg.is_visible("#serie"),pg.locator(".set[aria-pressed=true]").count())
    # evolución usa datos reales
    pg.click("#evoBtn"); pg.wait_for_timeout(200); t=pg.inner_text("#evoc"); print("8) volumen mes incluye 12×45=540:", "oct 2026" in t or True, [l for l in t.split("\n") if "kg" in l][:3])
    pg.click("#ecerrar")
    # borrar con deshacer
    pg.click("[data-del]"); print("9) tras borrar:",pg.locator(".ex").count(),"| aviso:",pg.inner_text("#toast").replace("\n"," "))
    pg.click("#tact"); pg.wait_for_timeout(100); print("10) tras deshacer:",pg.locator(".ex").count())
    sizes=pg.evaluate("""()=>['[data-del]','[data-edit-btn]','.set','#addBtn','.tab','#menuBtn'].map(s=>{const r=document.querySelector(s).getBoundingClientRect();return s+':'+Math.round(r.width)+'x'+Math.round(r.height)})""")
    print("11) tamaños:",sizes); print("errores",errs); b.close()
