import sys,pathlib;sys.path.insert(0,str(pathlib.Path(__file__).parent))
import h
from h import reg,URL
import json,re,time
from urllib.parse import urlparse,parse_qs,unquote
from playwright.sync_api import sync_playwright
U=URL
CORS={"access-control-allow-origin":"*","access-control-allow-headers":"*","access-control-allow-methods":"*"}
class FB:
    def __init__(s): s.users={}; s.docs={}; s.mails=[]; s.n=0
    def h(s,route):
        r=route.request; url=r.url; body=r.post_data or ""
        if r.method=="OPTIONS": return route.fulfill(status=204,headers=CORS)
        def ok(j,st=200): route.fulfill(status=st,headers={**CORS,"content-type":"application/json"},body=json.dumps(j))
        def bad(m,st=400,c=None): ok({"error":{"message":m,"status":c or "INVALID"}},st)
        if "accounts:signUp" in url:
            d=json.loads(body)
            if d["email"] in s.users: return bad("EMAIL_EXISTS")
            uid="u%d"%(len(s.users)+1); s.users[d["email"]]={"uid":uid,"pw":d["password"]}
            return ok({"idToken":"tok-"+uid,"refreshToken":"ref-"+uid,"localId":uid,"expiresIn":"3600"})
        if "signInWithPassword" in url:
            d=json.loads(body); u=s.users.get(d["email"])
            if not u or u["pw"]!=d["password"]: return bad("INVALID_LOGIN_CREDENTIALS")
            return ok({"idToken":"tok-"+u["uid"],"refreshToken":"ref-"+u["uid"],"localId":u["uid"],"expiresIn":"3600"})
        if "securetoken" in url:
            uid=body.split("refresh_token=ref-")[1].split("&")[0]
            return ok({"id_token":"tok-"+uid,"refresh_token":"ref-"+uid,"expires_in":"3600","user_id":uid})
        if "sendOobCode" in url: s.mails.append(json.loads(body)["email"]); return ok({})
        if "accounts:delete" in url:
            uid=json.loads(body)["idToken"][4:]; s.users={k:v for k,v in s.users.items() if v["uid"]!=uid}; return ok({})
        if "firestore.googleapis.com" in url:
            pu=urlparse(url); path=unquote(pu.path.split("/documents/")[1]); q=parse_qs(pu.query); uid=path.split("/")[1]
            if r.headers.get("authorization")!="Bearer tok-"+uid: return bad("PERMISSION_DENIED",403,"PERMISSION_DENIED")
            parts=path.split("/")
            if len(parts)==3 and r.method=="GET":   # listar
                docs=[{"name":"projects/p/databases/(default)/documents/"+k,"fields":{"mod":v["fields"].get("mod",{"integerValue":"0"})},"updateTime":v["updateTime"]} for k,v in s.docs.items() if k.startswith(path+"/")]
                return ok({"documents":docs} if docs else {})
            if r.method=="GET": return ok({"name":path,**s.docs[path]}) if path in s.docs else bad("NOT_FOUND",404,"NOT_FOUND")
            if r.method=="PATCH":
                cur=s.docs.get(path)
                if q.get("currentDocument.exists")==["false"] and cur: return bad("exists",409,"ALREADY_EXISTS")
                if "currentDocument.updateTime" in q and (not cur or cur["updateTime"]!=q["currentDocument.updateTime"][0]): return bad("stale",400,"FAILED_PRECONDITION")
                s.n+=1; s.docs[path]={"fields":json.loads(body)["fields"],"updateTime":"t%d"%s.n}; return ok({"name":path,**s.docs[path]})
            if r.method=="DELETE": s.docs.pop(path,None); return ok({})
        route.continue_()
def nuevo(b,fb):
    ctx=b.new_context(viewport={"width":390,"height":844})
    ctx.off=False
    ctx.route(re.compile(r"https://(identitytoolkit|securetoken|firestore)\.googleapis\.com/.*"),lambda route:route.abort("internetdisconnected") if ctx.off else fb.h(route))
    ctx.route("**/firebase-config.js",lambda r:r.fulfill(status=200,content_type="application/javascript",body="window.FIREBASE_CONFIG={apiKey:'k',projectId:'p'}"))
    pg=ctx.new_page(); pg.on("pageerror",lambda e:print("ERROR JS:",e)); pg.goto(U); pg.wait_for_timeout(400); return ctx,pg
def names(pg): return [t.strip() for t in pg.locator(".exname").all_inner_texts()]
def dia(pg,f): pg.evaluate("f=>{sel=f;editId=null;pintar()}",f); pg.wait_for_timeout(40)
def add(pg,f,n): dia(pg,f); pg.fill("#n",n); pg.click("#nuevo button[type=submit]"); pg.wait_for_timeout(40)
def sync(pg): pg.evaluate("subirNube()"); pg.wait_for_timeout(900)
def login(pg,em="ana@correo.com"):
    pg.click("#gcambio"); pg.fill("#ge",em); pg.fill("#gp","secreto1"); pg.click("#gok"); pg.wait_for_timeout(900)
def keys(fb,uid):
    out={}
    for k,v in fb.docs.items():
        if k.startswith(f"usuarios/{uid}/datos/"): out[k.split("/")[-1]]=json.loads(v["fields"]["items"]["stringValue"])
    return out
with sync_playwright() as p:
    b=p.chromium.launch(); fb=FB()
    cA,A=nuevo(b,fb)
    A.fill("#gn","Ana"); A.fill("#ge","ana@correo.com"); A.fill("#gp","secreto1"); A.fill("#gc","secreto1"); A.check("#gcheck"); A.click("#gok"); A.wait_for_timeout(600); A.click("#pno")
    add(A,"2026-10-06","A-mar"); A.wait_for_timeout(2300)
    d=keys(fb,"u1"); print("1) documentos en la nube:",sorted(d)); print("   elementos de la rutina de la semana (solo los editados):",[k for k in d.get("m-2026-10",{}) if k.startswith("sem:")])
    cB,B=nuevo(b,fb); login(B); dia(B,"2026-10-06"); print("2) 2º dispositivo ve:",names(B))
    cE,E=nuevo(b,fb); E.fill("#gn","X"); E.fill("#ge","ana@correo.com"); E.fill("#gp","secreto1"); E.fill("#gc","secreto1"); E.check("#gcheck"); E.click("#gok"); E.wait_for_timeout(500)
    print("2b) correo repetido ->",E.inner_text("#gerr")); E.click("#gcambio"); E.fill("#ge","ana@correo.com"); E.fill("#gp","mala123"); E.click("#gok"); E.wait_for_timeout(500)
    print("2c) clave mala ->",E.inner_text("#gerr")); E.click("#golv"); E.click("#greset"); E.wait_for_timeout(400); print("2d) restablecer ->",E.inner_text("#gmsg")[:40],"| correos:",fb.mails)
    # ---- ambos sin conexión
    cA.off=True; cB.off=True
    add(A,"2026-10-07","A-mie"); add(A,"2026-10-09","F-A"); A.wait_for_timeout(150)
    add(B,"2026-10-08","B-jue"); dia(B,"2026-10-06"); B.locator(".set").first.click(); B.click("#romitir"); add(B,"2026-10-09","F-B")
    cA.off=False; sync(A); cB.off=False; sync(B); sync(A)
    r=lambda pg,f:(dia(pg,f),names(pg))[1]
    for pg,n in ((A,"A"),(B,"B")):
        print(f"3) dispositivo {n}: mar",r(pg,"2026-10-06"),"marcadas",pg.locator(".set[aria-pressed=true]").count(),"| mié",r(pg,"2026-10-07"),"| jue",r(pg,"2026-10-08"),"| vie",r(pg,"2026-10-09"))
    # ---- muchos datos: 3 años
    A.evaluate("""()=>{for(let i=0;i<1100;i++){const d=iso(new Date(2024,0,1+i));const o={},l={};for(let j=0;j<5;j++){const id='e'+j;o[id]={n:'Press de banca',lid:'press-banca',s:4,r:8,k:40,d:4,km:40,v:1280,res:'8×40, 8×40, 8×40, 8×40'};l[id]=[true,true,true,true]}st.hist[d]=o;st.log[d]=l}pintar()}""")
    A.wait_for_timeout(3500); sync(A); A.wait_for_timeout(800)
    d=keys(fb,"u1"); tam=[len(fb.docs[f"usuarios/u1/datos/{k}"]["fields"]["items"]["stringValue"]) for k in d]
    print("4) documentos:",len(d),"| el mayor pesa:",max(tam)//1024,"KB (límite 1024 KB) | suma:",sum(tam)//1024,"KB")
    cC,C=nuevo(b,fb); login(C); print("5) dispositivo nuevo recupera días de historial:",C.evaluate("Object.keys(st.hist).length"),"de",A.evaluate("Object.keys(st.hist).length"))
    # ---- formato antiguo (un solo documento)
    fb.users["old@c.co"]={"uid":"u9","pw":"secreto1"}
    ant={"dias":[{"foco":"Push","ex":[{"id":"x","n":"Press de banca","s":3,"r":10,"k":40}]}]+[{"foco":"Sin definir","ex":[]}]*6,"log":{},"hist":{"2026-09-01":{"x":{"n":"Press de banca","s":3,"r":10,"k":40,"d":3,"km":40,"v":1200,"res":""}}},"pesos":{"2026-09-01":71.5},"perfil":{"nombre":"Old","edad":30,"peso":71.5,"altura":175,"objetivo":"Mantenerme","nivel":"Intermedio"},"perfilVisto":True,"descanso":60}
    fb.docs["usuarios/u9"]={"fields":{"datos":{"stringValue":json.dumps(ant)},"mod":{"integerValue":"5"}},"updateTime":"old"}
    cD,D=nuevo(b,fb); login(D,"old@c.co")
    print("6) migración del formato antiguo: historial",D.evaluate("Object.keys(st.hist)"),"| peso",D.evaluate("st.pesos"),"| descanso",D.evaluate("st.descanso"),"| documentos nuevos:",sorted(keys(fb,"u9")))
    # ---- cerrar sesión sin conexión y borrar cuenta
    cA.off=True; add(A,"2026-10-12","sin-red"); A.wait_for_timeout(300); A.click("#cfg"); A.click("#salir"); A.wait_for_timeout(300)
    print("7) cerrar sesión sin red:",A.inner_text("#toast")[:45],"| sigue dentro:",not A.is_visible("#gate")); cA.off=False
    A.click("#pno") if A.is_visible("#pno") else None
    A.click("#cfg"); A.click("#borrar"); A.click("#borrar"); A.wait_for_timeout(1200)
    print("8) cuenta borrada: usuarios",list(fb.users),"| documentos de u1:",[k for k in fb.docs if k.startswith("usuarios/u1")])
    b.close()
