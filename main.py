#Imports
import upgrades
from ursina import *
#Init Engine
app = Ursina()
#Set Vars
window.color = color.gray
gold = 0
extended = True
#Set Entities
upanel = Entity(model='quad', scale=(3, 200), color=color.dark_gray, alpha=0.5, x=-5.8)
#Set Texts
counter = Text(text='0', y=.25, z=-1, scale=2, origin=(0, 0), background=True)
#Set Buttons
collapser = Button(texture=load_texture("collapser.png"), color=color.light_gray, scale=.125, z=-3, x=-.6, y=.45)
gumball = Button(texture=load_texture("gumball_pink.png"), color=color.white, scale=.225)
gold_gen_upgrade = Button(cost=10, x=.2, scale=.125, color=color.dark_gray, disabled=True)
gold_gen_upgrade.tooltip = Tooltip(f'<gold>Gold Generator\n<default>Earn 1 gold every second.\nCosts {gold_gen_upgrade.cost} gold.')
#TLD Methods
def mov_ups():
    for outer_key, outer_value in upgrades.upgrades.items():
      if isinstance(outer_value, dict):
            for inner_key, inner_value in outer_value.items():
                if inner_key == "name":
                    print(f"Found 'name' under key '{outer_key}': {inner_value}")
                    mod = globals().get(inner_value,"No such variable")
                    print(mod)
                    print(outer_key)
                    cx=0
                    cy=0
                    ey=0
                    ex=0
                    for ik, iv in outer_value.items():
                        print(iv)
                        match ik:
                            case "cx":
                                cx = iv
                            case "cy":
                                cy=iv
                            case "ey":
                                ey=iv
                            case "ex":
                                ex=iv
                    print(f"ex:{ex}ey:{ey}cx:{cx}cy:{cy}")
                    if extended == True:
                        invoke(mod.animate('x',ex,duration=1,curve=curve.linear))
                        invoke(mod.animate('y',ey,duration=1,curve=curve.linear))
                    elif extended == False:
                        invoke(mod.animate('x',cx,duration=1,curve=curve.linear))
                        invoke(mod.animate('y',cy,duration=1,curve=curve.linear))
#Signals
def gumball_click():
    global gold
    gold += 1
    counter.text = str(gold)
    gumball.animate_scale(.240, .2, curve=curve.linear)
    invoke(gumball.animate_scale, 0.225, duration=0.2, curve=curve.linear, delay=0.2)
def buy_auto_gold():
    global gold
    if gold >= gold_gen_upgrade.cost:
        gold -= gold_gen_upgrade.cost
        counter.text = str(gold)
        invoke(auto_generate_gold, 1, 1)
def collapse():
    global extended
    if extended:
        upanel.animate('x', -7.800000190734863, duration=1, curve=curve.linear)
        collapser.animate('x', -0.8300000429153442, duration=1, curve=curve.linear)
        extended = False
        collapser.texture = load_texture('extender.png')  # Change texture instantly
        mov_ups()
    else:
        upanel.animate('x',-5.800000190734863, duration=1, curve=curve.linear)
        collapser.animate('x', -0.6000000238418579, duration=1, curve=curve.linear)
        extended = True
        collapser.texture = load_texture('collapser.png')
        mov_ups()
#Signal Connections
gumball.on_click = gumball_click
gold_gen_upgrade.on_click = buy_auto_gold
collapser.on_click = collapse
#Methods
def auto_generate_gold(value=1, interval=1):
    global gold
    gold += value
    counter.text = str(gold)
    gold_gen_upgrade.animate_scale(.125 * 1.1, duration=.1)
    gold_gen_upgrade.animate_scale(.125, duration=.1, delay=.1)
    invoke(auto_generate_gold, value, delay=interval)
#Game Loop
def update():
    global gold
    print(gold_gen_upgrade.position)
    for b in (gold_gen_upgrade, ):
        if gold >= b.cost:
            b.disabled = False
            b.color = color.green
        else:
            b.disabled = True
            b.color = color.gray
#Run Game
app.run()
