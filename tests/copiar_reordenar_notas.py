import sys,pathlib;sys.path.insert(0,str(pathlib.Path(__file__).parent))
import h
from h import reg,URL
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":390,"height":900}); errs=[]
    pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.goto(URL); reg(pg); pg.click("#pno")
    names=lambda:[t.strip() for t in pg.locator(".exname").all_inner_texts()]
    for n,nt in (("Sentadilla","Barra baja"),("Press de banca",""),("Remo con barra","Espalda recta")):
        pg.fill("#n",n); pg.fill("#nt",nt); pg.click("#nuevo button[type=submit]")
    print("orden inicial:",names(),"| notas:",pg.locator(".nota").all_inner_texts())
    # teclado
    pg.locator(".grip").first.focus(); pg.keyboard.press("ArrowDown")
    print("tras flecha abajo:",names(),"| foco en grip:",pg.evaluate("document.activeElement.className"))
    # arrastre con ratón: llevar el primero al final
    g=pg.locator(".grip").first.bounding_box(); last=pg.locator(".ex").last.bounding_box()
    pg.mouse.move(g["x"]+g["width"]/2,g["y"]+g["height"]/2); pg.mouse.down()
    pg.mouse.move(g["x"]+10,last["y"]+last["height"]*0.8,steps=12); pg.mouse.up(); pg.wait_for_timeout(150)
    print("tras arrastrar:",names())
    pg.reload(); pg.wait_for_timeout(200); print("persiste orden:",names())
    # editar nota
    pg.locator("[data-edit-btn]").first.click(); pg.fill(".ef input[name=nota]","Ajustar asiento 4"); pg.click(".ef button[type=submit]")
    print("nota editada:",pg.locator(".nota").first.inner_text())
    # copiar día
    pg.click("#copiar"); 
    print("chips deshabilitados:",pg.locator(".cd:disabled").count())
    pg.click(".cd[data-c='0']"); pg.click(".cd[data-c='4']"); print("info:",pg.inner_text("#cinfo") or "(sin reemplazos)"); pg.click("#csi"); pg.wait_for_timeout(100)
    print("aviso:",pg.inner_text("#toast"))
    pg.locator(".day").nth(0).click(); print("lunes:",names(),pg.locator(".nota").all_inner_texts())
    pg.locator(".day").nth(4).click(); print("viernes:",len(names()),"ejercicios")
    hoy=pg.evaluate("wd(parse(hoyIso))"); otro=next(i for i in (1,2,3) if i!=hoy); pg.locator(".day").nth(otro).click(); print("día no copiado:",len(names()),"ejercicios (debe ser 0)")
    print("errores",errs); b.close()
