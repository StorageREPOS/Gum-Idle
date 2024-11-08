from ursina import *

app = Ursina()
window.color = color.gray
gold = 0
extended = True

upanel = Entity(model='quad', scale=(3, 200), color=color.dark_gray, alpha=0.5, x=-5.8)
counter = Text(text='0', y=.25, z=-1, scale=2, origin=(0, 0), background=True)

collapser = Button(texture=load_texture("collapser.png"), color=color.light_gray, scale=.125, z=-3, x=-.6, y=.45)
button = Button(texture=load_texture("gumball_pink.png"), color=color.white, scale=.225)
button_2 = Button(cost=10, x=.2, scale=.125, color=color.dark_gray, disabled=True)
button_2.tooltip = Tooltip(f'<gold>Gold Generator\n<default>Earn 1 gold every second.\nCosts {button_2.cost} gold.')

def button_click():
    global gold
    gold += 1
    counter.text = str(gold)
    button.animate_scale(.240, .2, curve=curve.linear)
    invoke(button.animate_scale, 0.225, duration=0.2, curve=curve.linear, delay=0.2)

def buy_auto_gold():
    global gold
    if gold >= button_2.cost:
        gold -= button_2.cost
        counter.text = str(gold)
        invoke(auto_generate_gold, 1, 1)

def collapse():
    global extended
    collapser.disabled = True  # Disable the button

    if extended:
        upanel.animate('x', -7.800000190734863, duration=1, curve=curve.linear)
        collapser.animate('x', -0.8300000429153442, duration=1, curve=curve.linear)
        extended = False
        collapser.texture = load_texture('extender.png')  # Change texture instantly
    else:
        upanel.animate('x',-5.800000190734863, duration=1, curve=curve.linear)
        collapser.animate('x', -0.6000000238418579, duration=1, curve=curve.linear)
        extended = True
        collapser.texture = load_texture('collapser.png')  # Change texture instantly

    invoke(enable_collapser, delay=1)  # Enable the button after animation

def enable_collapser():
    collapser.disabled = False  # Enable the button

def auto_generate_gold(value=1, interval=1):
    global gold
    gold += value
    counter.text = str(gold)
    button_2.animate_scale(.125 * 1.1, duration=.1)
    button_2.animate_scale(.125, duration=.1, delay=.1)
    invoke(auto_generate_gold, value, delay=interval)

def update():
    global gold
    for b in (button_2, ):
        if gold >= b.cost:
            b.disabled = False
            b.color = color.green
        else:
            b.disabled = True
            b.color = color.gray

button.on_click = button_click
button_2.on_click = buy_auto_gold
collapser.on_click = collapse

app.run()
