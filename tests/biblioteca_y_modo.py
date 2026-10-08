import sys,pathlib;sys.path.insert(0,str(pathlib.Path(__file__).parent))
import h
from h import reg,URL
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":390,"height":844}); errs=[]
    pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.goto(URL); reg(pg); pg.click("#pno")
    # --- biblioteca ---
    pg.click("#abrirLib"); n0=pg.locator(".lrow").count(); print("1) biblioteca abierta:",pg.is_visible("#lib"),"| ejercicios:",n0)
    pg.fill("#lq","banca"); print("2) buscar 'banca':",[t.split("\n")[0] for t in pg.locator(".lrow").all_inner_texts()][:3])
    pg.click(".lchip[data-m='Espalda']"); print("3) filtro Espalda + 'banca' ->",pg.locator(".lrow").count(),"(solo opción propia)")
    pg.click(".lchip[data-m='Todos']"); pg.fill("#lq","press banca"); print("4) alias 'press banca':",pg.locator(".lrow").first.inner_text().split("\n")[0])
    pg.locator(".lrow").first.click(); pg.wait_for_timeout(100)
    print("5) rellenó nombre:",pg.input_value("#n"),"| biblioteca cerrada:",not pg.is_visible("#lib"))
    pg.fill("#s","3"); pg.click("#nuevo button[type=submit]")
    pg.fill("#n","Press banca"); pg.click("#nuevo button[type=submit]")
    pg.click("#abrirLib"); pg.fill("#lq","ejercicio inventado"); pg.locator(".lrow[data-propio]").click(); pg.fill("#s","2"); pg.click("#nuevo button[type=submit]")
    print("6) lid:",pg.evaluate("planDe(sel).ex.map(e=>e.lid)"),"| nombres:",[t.strip() for t in pg.locator(".exname").all_inner_texts()])
    # historial previo con el nombre canónico: debe reconocerse también con el alias
    pg.evaluate("""()=>{const d=new Date();d.setDate(d.getDate()-7);const e=planDe(sel).ex[1];st.hist[iso(d)]={x:{n:'Press de banca',lid:'press-banca',s:3,r:10,k:30,d:3,km:30,v:900,res:'10×30, 10×30, 8×32.5'}};pintar()}""")
    print("7) última vez por enlace (alias):",[t for t in pg.locator(".ult").all_inner_texts()])
    # --- modo entrenamiento ---
    print("8) botón:",pg.inner_text("#entrenar")); pg.click("#entrenar"); pg.wait_for_timeout(200)
    print("9) modo:",pg.is_visible("#modo"),"|",pg.inner_text("#mtit"),"| serie:",pg.inner_text(".msetl"),"| prefill kg/reps:",pg.input_value("#mk"),pg.input_value("#mr"))
    pg.click("[data-st='k'][data-v='2.5']"); pg.click("[data-st='k'][data-v='2.5']"); pg.click("[data-st='r'][data-v='-1']")
    print("10) pasos:",pg.input_value("#mk"),pg.input_value("#mr")); (pg.wait_for_timeout(650),pg.click("#mhecha")); pg.wait_for_timeout(150)
    print("11) descanso visible:",pg.is_visible("#rest"),"| siguiente serie prellenada:",pg.input_value("#mk"),pg.input_value("#mr"),"|",pg.inner_text(".msetl"))
    pg.click("#romitir"); (pg.wait_for_timeout(650),pg.click("#mhecha")); pg.click("#romitir"); (pg.wait_for_timeout(650),pg.click("#mhecha")); pg.click("#romitir")
    print("12) ejercicio completo:",pg.inner_text(".mok"),"| botón:",pg.inner_text("#msig"))
    pg.click("[data-d='1']"); print("13) deshacer serie 2 -> serie actual:",pg.inner_text(".msetl")); (pg.wait_for_timeout(650),pg.click("#mhecha")); pg.click("#romitir")
    pg.click("#msig"); print("14) 2º ejercicio:",pg.inner_text("#mtit"),"|",pg.inner_text(".msetl"))
    for _ in range(12):
        if pg.locator("#mhecha").count():
            (pg.wait_for_timeout(650),pg.click("#mhecha")); pg.wait_for_timeout(60)
            if pg.is_visible("#romitir"): pg.click("#romitir")
        elif pg.locator("#msig").count(): pg.click("#msig")
        else: break
    pg.wait_for_timeout(200); print("15) resumen:",pg.inner_text("#mtit"),"|",pg.inner_text(".mgrid").replace("\n"," "))
    print("   inicio/fin registrados:",pg.evaluate("!!(st.ini[sel]&&st.ini[sel].a&&st.ini[sel].b)"),"| récord:",pg.locator(".mok").count())
    pg.click("#mcerrar"); pg.wait_for_timeout(150); print("16) modo cerrado:",not pg.is_visible("#modo"),"| botón:",pg.inner_text("#entrenar"),"| reales:",pg.locator(".real").all_inner_texts())
    # evolución: un solo ejercicio de 'Press de banca' (unifica alias)
    pg.click("#evoBtn"); pg.wait_for_timeout(150); print("17) opciones de evolución:",pg.locator("#evoSel option").all_inner_texts())
    print("errores",errs); b.close()
