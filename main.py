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
    else:
        upanel.animate('x',-5.800000190734863, duration=1, curve=curve.linear)
        collapser.animate('x', -0.6000000238418579, duration=1, curve=curve.linear)
        for upgradex in upgrades.upgrades.items():
            print(str(upgradex))
            mod = globals().get(upgradex.name,"No such variable")
            invoke(mod.animate('x',-5,duration=1,curve=curve.linear))        
        extended = True
        collapser.texture = load_texture('collapser.png') 
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
    for b in (gold_gen_upgrade, ):
        if gold >= b.cost:
            b.disabled = False
            b.color = color.green
        else:
            b.disabled = True
            b.color = color.gray
#Run Game
app.run()
