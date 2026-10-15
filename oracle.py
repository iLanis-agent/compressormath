import json, math

def num(x): return isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x)
def pos(x): return num(x) and x>0
def jround(x): return math.floor(x+0.5)
def r1(x): return jround(x*10)/10
def jsnum(x):
    if isinstance(x,float) and x==int(x): return str(int(x))
    return str(x)

DERATE=0.8

def cfm_plan(sticker):
    if not pos(sticker): return {"error":"the sticker CFM must be above zero"}
    return {"cfm90":r1(sticker*DERATE)}

def render_cfm(r,sticker):
    return ("The "+jsnum(sticker)+" CFM on the box was measured at 40 PSI; your tools breathe at 90, where the pump honestly gives about "
            +jsnum(r["cfm90"])+" CFM.")

def recovery_plan(tank,cut_in,cut_out,cfm):
    if not pos(tank): return {"error":"the tank size must be above zero"}
    if not num(cut_in): return {"error":"the cut-in pressure must be a number"}
    if not num(cut_out): return {"error":"the cut-out pressure must be a number"}
    if cut_out<=cut_in: return {"error":"the cut-out must beat the cut-in"}
    if not pos(cfm): return {"error":"the pump CFM must be above zero"}
    free=tank*(cut_out-cut_in)/14.7/7.48
    return {"freeAir":r1(free),"seconds":r1(free/cfm*60)}

def render_recovery(r,tank,cut_in,cut_out,cfm):
    return ("The "+jsnum(tank)+"-gallon tank climbing from "+jsnum(cut_in)+" to "+jsnum(cut_out)+" PSI holds about "
            +jsnum(r["freeAir"])+" cubic feet of free air - at "+jsnum(cfm)+" honest CFM that is about "+jsnum(r["seconds"])
            +" seconds of recovery the tool feels every cycle.")

def duty_plan(tool,pump):
    if not pos(tool): return {"error":"the tool demand must be above zero"}
    if not pos(pump): return {"error":"the pump CFM must be above zero"}
    pct=tool/pump*100
    if pct<=50: verdict="the tool runs all day and the pump barely works"
    elif pct<=80: verdict="the pump keeps up, with pauses for the tank to catch its breath"
    elif pct<=100: verdict="the pump barely keeps up - long runs empty the tank"
    else: verdict="the pump cannot feed it - the tool starves mid-pass"
    return {"pct":r1(pct),"verdict":verdict}

def render_duty(r,tool,pump):
    return ("The tool asks "+jsnum(tool)+" CFM against the pump's honest "+jsnum(pump)+" - a duty of "+jsnum(r["pct"])
            +"% means "+r["verdict"]+".")

cases=[]
def add(tool,args):
    if tool=="cfm": r=cfm_plan(*args); fn=render_cfm
    elif tool=="recovery": r=recovery_plan(*args); fn=render_recovery
    else: r=duty_plan(*args); fn=render_duty
    case={"tool":tool,"args":args,"result":r}
    if "error" not in r: case["render"]=fn(r,*args)
    cases.append(case)

for a in [(5,),(6,),(4.5,),(7,),(3.2,),(10,)]:
    add("cfm",a)
for a in [(20,90,120,4),(30,90,125,4.8),(6,90,120,2),(10,100,135,3.5),(26,90,125,5),(33,95,125,4)]:
    add("recovery",a)
for a in [(5,4),(3,4.8),(2,4),(4,4),(4.05,4),(7,4),(1.5,4),(3.4,4)]:
    add("duty",a)
add("cfm",[0]); add("cfm",["lots"])
add("recovery",[0,90,120,4]); add("recovery",[20,120,120,4]); add("recovery",[20,120,90,4]); add("recovery",[20,90,120,0]); add("recovery",[20,"low",120,4])
add("duty",[0,4]); add("duty",[5,0]); add("duty",["hungry",4])

json.dump(cases,open("expected.json","w"),separators=(",",":"))
print(len(cases),"cases")
