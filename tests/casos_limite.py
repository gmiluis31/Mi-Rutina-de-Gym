import sys,pathlib;sys.path.insert(0,str(pathlib.Path(__file__).parent))
import h
from h import reg,URL
import sys,json
sys.path.insert(0,'/tmp'); import h
from playwright.sync_api import sync_playwright
U=URL
res=[]
def ok(n,c,d=""): res.append((n,bool(c),d)); print(("OK  " if c else "FALLO"),n,d)
with sync_playwright() as p:
    b=p.chromium.launch()
    # 1) fechas: huso horario, cambio de hora, año bisiesto, fin de año
    for tz in ("Europe/Madrid","America/Santiago","America/Mexico_City","Pacific/Auckland","UTC","Asia/Kolkata"):
        ctx=b.new_context(timezone_id=tz,viewport={"width":390,"height":800}); pg=ctx.new_page(); pg.goto(U); pg.wait_for_timeout(200)
        r=pg.evaluate("""()=>{const bad=[];for(let i=0;i<800;i++){const d=new Date(2026,2,1+i,12);const f=iso(d);const L=lunesDe(f);if(wd(parse(L))!==0)bad.push('lunes '+f);if(iso(parse(f))!==f)bad.push('ida y vuelta '+f);
          const s=semanasDe(d.getFullYear(),d.getMonth());if(!s.length||s.some(w=>wd(w)!==0))bad.push('semanas '+f);
          const w=dias7(new Date(parse(L))).map(iso);if(new Set(w).size!==7)bad.push('dias7 repetidos '+f)}return bad.slice(0,3)}""")
        ok(f"fechas en {tz} (800 días, cambios de hora)",not r,str(r)); ctx.close()
    ctx=b.new_context(viewport={"width":390,"height":800}); pg=ctx.new_page(); errs=[]
    pg.on("pageerror",lambda e:errs.append(str(e))); pg.goto(U); pg.wait_for_timeout(200); h.reg(pg); pg.click("#pno")
    # 2) navegación a fin de año / bisiesto
    for f in ("2026-12-31","2027-01-01","2028-02-29","2028-03-01","2026-02-28"):
        pg.evaluate("f=>{sel=f;pintar()}",f); t=pg.inner_text("#titulo"); ok(f"navegar a {f}",pg.locator(".day").count()==7 and "NaN" not in t,t)
    pg.evaluate("sel='2026-12-31';pintar()"); pg.click("#calBtn"); pg.click("#mnext"); ok("mes siguiente desde diciembre",pg.inner_text("#mes").replace("\n","")[-4:]=="2027",pg.inner_text("#mes").replace("\n",""))
    pg.click("#mprev"); pg.click("#mprev"); ok("dos meses atrás",pg.evaluate("sel").startswith("2026-1"),pg.evaluate("sel")); pg.click("#calBtn")
    # 3) texto raro en nombres
    pg.evaluate("sel='2026-10-05';pintar()")
    for n in ('<img src=x onerror="window.__xss=1">','"><script>window.__xss=1</script>',"Comillas ' y \" y &amp;","A"*200,"😀 Sentadilla 💪"):
        pg.fill("#n",n); pg.click("#nuevo button[type=submit]"); pg.wait_for_timeout(60)
    ok("sin XSS con nombres maliciosos",not pg.evaluate("window.__xss"))
    ok("sin desborde con nombre de 200 letras",pg.evaluate("document.documentElement.scrollWidth<=innerWidth"))
    ok("nombres con símbolos se muestran literales",any("&amp;" in t for t in pg.locator(".exname").all_inner_texts()))
    pg.click("[data-edit-btn]"); pg.fill(".ef input[name=n]",'" onfocus="window.__xss=1" x="'); pg.click(".ef button[type=submit]"); pg.wait_for_timeout(60)
    pg.click("[data-edit-btn]"); pg.wait_for_timeout(60); ok("editar con comillas no inyecta atributos",not pg.evaluate("window.__xss")); pg.click(".ef button[data-cancel]")
    # 4) series: cambiar nº de series con marcas hechas
    pg.evaluate("""()=>{const d=planEdit(sel);d.ex=[{id:'t1',n:'Test',lid:null,s:5,r:8,k:40}];const m=marks(sel,d.ex[0]);m[0]=m[1]=m[4]=true;st.log[sel]={t1:m};snap(sel,d.ex[0]);pintar()}""")
    pg.click("[data-edit-btn]"); pg.fill(".ef input[name=s]","2"); pg.click(".ef button[type=submit]"); pg.wait_for_timeout(80)
    ok("bajar de 5 a 2 series conserva las 2 primeras marcadas",pg.locator(".set[aria-pressed=true]").count()==2 and pg.locator(".set").count()==2,f"{pg.locator('.set[aria-pressed=true]').count()} marcadas de {pg.locator('.set').count()}")
    h_=pg.evaluate("JSON.stringify(st.hist[sel].t1)"); ok("historial refleja 2 series hechas tras editar",'"d":2' in h_,h_[:120])
    pg.click("[data-edit-btn]"); pg.fill(".ef input[name=s]","4"); pg.click(".ef button[type=submit]"); pg.wait_for_timeout(80)
    ok("subir de 2 a 4 series: aparecen 2 sin marcar",pg.locator(".set").count()==4 and pg.locator(".set[aria-pressed=true]").count()==2)
    # 5) pesos decimales y límites en el modo entrenamiento
    pg.click("#entrenar"); pg.fill("#mk","0.1"); 
    for _ in range(3): pg.click("[data-st='k'][data-v='2.5']")
    ok("pasos de peso sin errores de coma flotante",pg.input_value("#mk") in("7.6","7.5","7.6"),pg.input_value("#mk"))
    pg.fill("#mk","-5"); pg.fill("#mr","9999"); pg.click("#mhecha"); pg.wait_for_timeout(100)
    rl=pg.evaluate("JSON.stringify(Object.values(st.real[sel]||{}).map(o=>Object.values(o)))"); ok("valores fuera de rango se limitan (reps≤100, kg≥0)","100" in rl and "-5" not in rl,rl)
    pg.click("#romitir") if pg.is_visible("#romitir") else None; pg.click("#msalir")
    ok("sin errores de JavaScript hasta aquí",not errs,str(errs[:2]))
    ctx.close()
    # 6) datos guardados corruptos
    bad={"dias con nulos":{"dias":[None]*7},"dias sin ex":{"dias":[{"foco":"x"}]*7},"log como lista":{"dias":[{"foco":"a","ex":[]}]*7,"log":[]},"hist nulo":{"dias":[{"foco":"a","ex":[]}]*7,"hist":None,"semanas":None},"semanas rotas":{"dias":[{"foco":"a","ex":[]}]*7,"semanas":{"2026-10-05":[1,2]}},"texto":"basura{","perfil raro":{"dias":[{"foco":"a","ex":[]}]*7,"perfil":{"edad":"x"},"perfilVisto":True}}
    for n,v in bad.items():
        ctx=b.new_context(viewport={"width":390,"height":800}); pg=ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)[:90]))
        pg.add_init_script("localStorage.setItem('rutina-gym-v1',%s);localStorage.setItem('rutina-gym-cuenta',JSON.stringify({nombre:'A',email:'a@b.co',salt:'00',hash:'00'}));localStorage.setItem('rutina-gym-sesion','1')"%json.dumps(json.dumps(v)))
        pg.goto(U); pg.wait_for_timeout(300)
        vivo=pg.is_visible("#addBtn") or pg.is_visible("#perfil") or pg.is_visible("#gate")
        ok(f"arranca con datos corruptos: {n}",vivo and not errs,str(errs[:1])); ctx.close()
    b.close()
bad=[r for r in res if not r[1]]; print("\nRESUMEN:",len(res)-len(bad),"correctos,",len(bad),"fallos")
