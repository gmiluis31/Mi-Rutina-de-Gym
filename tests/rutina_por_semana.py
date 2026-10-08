import sys,pathlib;sys.path.insert(0,str(pathlib.Path(__file__).parent))
import h
from h import reg,URL
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":390,"height":900}); errs=[]
    pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.goto(URL); reg(pg); pg.click("#pno")
    names=lambda:[t.strip() for t in pg.locator(".exname").all_inner_texts()]
    F=["2026-09-28","2026-10-05","2026-10-12","2026-10-19","2026-10-26"]
    def lunes(i): pg.evaluate("f=>{sel=f;editId=null;pintar()}",F[i]); pg.wait_for_timeout(60)
    def add(n): pg.fill("#n",n); pg.click("#nuevo button[type=submit]"); pg.wait_for_timeout(60)
    lunes(1); add("A"); pg.locator(".set").first.click(); pg.click("#romitir")
    print("1) Sem2 lunes:",names())
    lunes(0); print("2) Sem1 lunes (anterior, sin cambios):",names())
    lunes(2); print("3) Sem3 lunes hereda:",names())
    add("B"); print("   toast:",pg.inner_text("#toast").replace("\n"," ")[:55]); print("4) Sem3 lunes tras añadir B:",names())
    lunes(1); print("   Sem2 lunes sigue:",names(),"| serie marcada conservada:",pg.locator(".set[aria-pressed=true]").count())
    lunes(3); print("   Sem4 lunes hereda de Sem3:",names())
    lunes(2); pg.click("#copiar"); print("5) panel:",pg.inner_text("#cswt")); pg.click("#csr"); print("   restablecida Sem3:",names())
    pg.click("#tact"); print("   deshacer:",names())
    lunes(1); pg.click("#copiar"); pg.click("#csem"); lunes(2); print("6) copiar Sem2→Sem3:",names())
    lunes(3); pg.click("[data-del]"); pg.wait_for_timeout(50); print("7) borrar en Sem4:",names(),"| Sem3 intacta:",end=" "); lunes(2); print(names())
    pg.reload(); pg.wait_for_timeout(400); lunes(3); print("8) tras recargar Sem4:",names(),end=" | "); lunes(1); print("Sem2:",names())
    lunes(3); pg.click("[data-t=ppl]"); pg.wait_for_timeout(100); print("9) plantilla con rutina existente -> aviso:",pg.inner_text("#avtxt")[:70])
    pg.click("[data-ok]"); pg.wait_for_timeout(100); print("   Sem4 lunes con plantilla:",names()[:2]); lunes(2); print("   Sem3 intacta:",names()); lunes(4); print("   Sem5 hereda plantilla:",names()[:2])
    print("errores",errs); b.close()
