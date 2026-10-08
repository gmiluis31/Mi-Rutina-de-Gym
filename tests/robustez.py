import sys,pathlib;sys.path.insert(0,str(pathlib.Path(__file__).parent))
import h
from h import reg,URL
import sys;sys.path.insert(0,'/tmp'); import h
from playwright.sync_api import sync_playwright
U=URL
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={"width":390,"height":844}); pg=ctx.new_page(); errs=[]
    pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.clock.set_fixed_time("2026-10-08T23:58:00")
    pg.goto(U); pg.wait_for_timeout(300); h.reg(pg); pg.click("#pno")
    print("1) hoy antes de medianoche:",pg.inner_text("#titulo"))
    pg.clock.set_fixed_time("2026-10-09T00:05:00"); pg.evaluate("document.dispatchEvent(new Event('visibilitychange'))"); pg.wait_for_timeout(150)
    print("2) al volver pasada la medianoche:",pg.inner_text("#titulo"),"| día seleccionado:",pg.evaluate("sel"))
    pg.evaluate("sel='2026-10-05';pintar()")
    # --- botón atrás ---
    pg.click("#addBtn"); print("3) hoja abierta:",pg.is_visible("#addsheet")); pg.go_back(); pg.wait_for_timeout(200)
    print("   atrás -> hoja cerrada:",not pg.is_visible("#addsheet"),"| app sigue:",pg.is_visible("#addBtn"),"| estado:",pg.evaluate("history.state"))
    pg.click("#addBtn"); pg.click("#abrirLib"); pg.go_back(); pg.wait_for_timeout(200)
    print("4) dos ventanas: atrás cierra solo la biblioteca:",not pg.is_visible("#lib") and pg.is_visible("#addsheet")); pg.go_back(); pg.wait_for_timeout(200); print("   segundo atrás cierra la hoja:",not pg.is_visible("#addsheet"))
    pg.click("#evoBtn"); pg.click("#ecerrar"); pg.wait_for_timeout(250); print("5) cerrar con el botón deja el historial limpio:",pg.evaluate("history.state"),"| ventana cerrada:",not pg.is_visible("#evo"))
    pg.fill("#n","Press de banca"); pg.click("#nuevo button[type=submit]"); pg.wait_for_timeout(200)
    pg.click("#entrenar"); pg.wait_for_timeout(150); print("6) modo abierto:",pg.is_visible("#modo"))
    pg.dblclick("#mhecha"); pg.wait_for_timeout(250); print("   doble toque en 'Serie hecha' marca solo 1 serie:",pg.evaluate("marks(sel,planDe(sel).ex[0]).filter(Boolean).length")==1)
    pg.go_back(); pg.wait_for_timeout(250); print("   atrás cierra el modo (no la app):",not pg.is_visible("#modo") and pg.is_visible("#addBtn"),"| intervalo del cronómetro detenido:",pg.evaluate("document.querySelector('#modo').hidden"))
    # --- perfil sin teclado ---
    pg.click("#cfg"); pg.wait_for_timeout(150); print("7) al abrir Perfil el foco no va al campo de texto:",pg.evaluate("document.activeElement.id")!="pn")
    print("errores",errs); b.close()
