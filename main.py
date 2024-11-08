#Imports
from ursina import *
#Initialization
app = Ursina()
#Var Delclairation
window.color = color._20
gold = 0
#Panel Entities

#Text Entities
counter = Text(text='0', y=.25, z=-1, scale=2, origin=(0,0), background=True)
#Button Entities
button = Button(texture=load_texture("gumball_pink.png"), color=color.white, scale= .225)
button_2 = Button(cost=10, x=.2, scale=.125, color=color.dark_gray, disabled=True)
button_2.tooltip = Tooltip(f'<gold>Gold Generator\n<default>Earn 1 gold every second.\nCosts {button_2.cost} gold.')
#Signals
def button_click():
    global gold
    gold += 1
    counter.text = str(gold)
    button.animate_scale(.240,.2,curve=curve.linear)
    invoke(button.animate_scale, 0.225, duration=0.2, curve=curve.linear, delay=0.2)
def buy_auto_gold():
    global gold
    if gold >= button_2.cost:
        gold -= button_2.cost
        counter.text = str(gold)
        invoke(auto_generate_gold, 1, 1)
#Signal Connections
button.on_click = button_click
button_2.on_click = buy_auto_gold
#Methods
def auto_generate_gold(value=1, interval=1):
    global gold
    gold += 1
    counter.text = str(gold)
    button_2.animate_scale(.125 * 1.1, duration=.1)
    button_2.animate_scale(.125, duration=.1, delay=.1)
    invoke(auto_generate_gold, value, delay=interval)
#Game Loop
def update():
    global gold
    for b in (button_2, ):
        if gold >= b.cost:
            b.disabled = False
            b.color = color.green
        else:
            b.disabled = True
            b.color = color.gray
#Runner
app.run()

