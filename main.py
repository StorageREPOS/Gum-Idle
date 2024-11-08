#Imports
import upgrades
from ursina import *
#Init Engine
app = Ursina()
#Set Vars
window.color = color.gray
gum = 0
extended = True
#Set SFX
smack = Audio(sound_file_name=os.path.join('smack.mp3'), loop=False, autoplay=False)
lofi = Audio(sound_file_name=os.path.join('lofi.mp3'),loop=True,autoplay=True)
ding = Audio(sound_file_name=os.path.join('ding.mp3'), loop=False, autoplay=False)
#Set Entities
upanel = Entity(model='quad', scale=(3, 200), color=color.dark_gray, alpha=0.5, x=-5.8)
#Set Texts
counter = Text(text='0', y=.25, z=-1, scale=2, origin=(0, 0), background=True)
#Set Buttons
collapser = Button(texture=load_texture("collapser.png"), color=color.light_gray, scale=.125, z=-3, x=-.6, y=.45)
gumball = Button(texture=load_texture("gumball_pink.png"), color=color.white, scale=.225)
gumball.tooltip = Tooltip(f'<pink>Gum Ball\n<default>Bite this to gain more gum!')
gum_up = Button(text="Gum Gen",cost=10, x=-.71, scale_y =.125, scale_x=.250, color=color.red,y=.33, disabled=True)
gum_up.tooltip = Tooltip(f'<pink>Gum Generator\n<default>Earn 1 gum every second.\nCosts {gum_up.cost} gum.')
#TLD Methods
def mov_ups():
    for outer_key, outer_value in upgrades.upgrades.items():
      if isinstance(outer_value, dict):
            for inner_key, inner_value in outer_value.items():
                if inner_key == "name":
                    mod = globals().get(inner_value,"No such variable")
                    cx=0
                    cy=0
                    ey=0
                    ex=0
                    for ik, iv in outer_value.items():
                        match ik:
                            case "cx":
                                cx = iv
                            case "cy":
                                cy=iv
                            case "ey":
                                ey=iv
                            case "ex":
                                ex=iv
                    if extended == True:
                        invoke(mod.animate('x',ex,duration=1,curve=curve.out_bounce))
                        invoke(mod.animate('y',ey,duration=1,curve=curve.out_bounce))
                    elif extended == False:
                        invoke(mod.animate('x',cx,duration=1,curve=curve.out_bounce))
                        invoke(mod.animate('y',cy,duration=1,curve=curve.out_bounce))
#Signals
def gumball_click():
    global gum
    smack.play()
    gum += 1
    counter.text = str(gum)
    gumball.animate_scale(.240, .2, curve=curve.linear)
    invoke(gumball.animate_scale, 0.225, duration=0.2, curve=curve.out_bounce, delay=0.2)
def buy_auto_gum():
    global gum
    if gum >= gum_up.cost:
        ding.play()
        gum -= gum_up.cost
        counter.text = str(gum)
        gum_up.cost *= 1.5
        gum_up.cost = int(gum_up.cost)
        gum_up.tooltip.text = f'<pink>Gum Generator\n<default>Earn 1 gum every second.\nCosts {gum_up.cost} gum.'
        invoke(auto_generate_gum, 1, 1)
def collapse():
    global extended
    if extended:
        upanel.animate('x', -7.800000190734863, duration=1, curve=curve.out_bounce)
        collapser.animate('x', -0.8300000429153442, duration=1, curve=curve.out_bounce)
        extended = False
        collapser.texture = load_texture('extender.png')  # Change texture instantly
        mov_ups()
    else:
        upanel.animate('x',-5.800000190734863, duration=1, curve=curve.out_bounce)
        collapser.animate('x', -0.6000000238418579, duration=1, curve=curve.out_bounce)
        extended = True
        collapser.texture = load_texture('collapser.png')
        mov_ups()
#Signal Connections
gumball.on_click = gumball_click
gum_up.on_click = buy_auto_gum
collapser.on_click = collapse
#Methods
def auto_generate_gum(value=1, interval=1):
    global gum
    gum += value
    counter.text = str(gum)
    invoke(auto_generate_gum, value, delay=interval)
#Game Loop
def update():
    global gum
    for b in (gum_up, ):
        if gum >= b.cost:
            b.disabled = False
            b.color = color.green
        else:
            b.disabled = True
            b.color = color.red
#Run Game
app.run()
