import os
import re
import socket
import subprocess
from libqtile import bar, layout, widget, hook, extension
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown, KeyChord
from libqtile.lazy import lazy
#from libqtile.utils import guess_terminal
from typing import List # noqa: F401
from libqtile.widget import spacer
from themes.tokyonight import colors

from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration
from libqtile.log_utils import logger

mod = "mod4"
terminal = "kitty"
browser = "firefox"

keys = [Key(key[0], key[1], *key[2:]) for key in [
    # ------------ Window Configs ------------

    # Switch between windows in current stack pane
    ([mod], "j", lazy.layout.down()),
    ([mod], "k", lazy.layout.up()),
    ([mod], "h", lazy.layout.left()),
    ([mod], "l", lazy.layout.right()),

    # Change window sizes (MonadTall)
    ([mod, "shift"], "l", lazy.layout.grow()),
    ([mod, "shift"], "h", lazy.layout.shrink()),

    # Toggle floating
    ([mod, "shift"], "f", lazy.window.toggle_floating()),

    # Move windows up or down in current stack
    ([mod, "shift"], "j", lazy.layout.shuffle_down()),
    ([mod, "shift"], "k", lazy.layout.shuffle_up()),

    # Toggle between different layouts as defined below
    ([mod], "Tab", lazy.next_layout()),
    ([mod, "shift"], "Tab", lazy.prev_layout()),

    # Kill window
    ([mod], "w", lazy.window.kill()),

    # Switch focus of monitors
    ([mod], "period", lazy.next_screen()),
    ([mod], "comma", lazy.prev_screen()),

    # Restart Qtile
    ([mod, "control"], "r", lazy.restart()),

    ([mod, "control"], "q", lazy.shutdown()),
    ([mod], "r", lazy.spawncmd()),

    # ------------ App Configs ------------

    # Menu
    ([mod], "m", lazy.spawn("rofi -show drun")),

    # Window Nav
    ([mod, "shift"], "m", lazy.spawn("rofi -show")),

    # Browser
    ([mod], "b", lazy.spawn("librewolf")),

    # File Explorer
    ([mod], "e", lazy.spawn("thunar")),

    # Terminal
    ([mod], "Return", lazy.spawn("kitty")),

    # Redshift
    ([mod], "r", lazy.spawn("redshift -O 2400")),
    ([mod, "shift"], "r", lazy.spawn("redshift -x")),

    # Screenshot
    ([mod], "s", lazy.spawn("scrot")),
    ([mod, "shift"], "s", lazy.spawn("scrot -s")),

    # ------------ Hardware Configs ------------

    # Volume
    ([], "XF86AudioLowerVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ -5%"
    )),
    ([], "XF86AudioRaiseVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ +5%"
    )),
    ([], "XF86AudioMute", lazy.spawn(
        "pactl set-sink-mute @DEFAULT_SINK@ toggle"
    )),

    # Brightness
    ([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +5%")),
    ([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5%-")),
]]

groups = [
    Group('1',label="一",layout="max"),
    Group('2', label="二", layout="max", matches=[Match(wm_class=["firefox","librewolf"])]),
    Group('3', label="三", layout="max"),
    Group('4', label="五", layout="max", matches=[Match(wm_class=["spotify"])]), 
    Group('5', label="六", layout="max"), 
    Group('6', label="七", layout="max"), 
    Group('7', label="八", layout="max"), 
    Group('8', label="九", layout="max"), 
    
]


for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

groups.append(ScratchPad("6", [
    DropDown("chatgpt", "chromium --app=https://chat.openai.com", x=0.3, y=0.1, width=0.40, height=0.4, on_focus_lost_hide=False ),
    DropDown("mousepad", "mousepad", x=0.3, y=0.1, width=0.40, height=0.4, on_focus_lost_hide=False ),
    DropDown("terminal", "alacritty", x=0.3, y=0.1, width=0.40, height=0.4, on_focus_lost_hide=False ),
    DropDown("scrcpy", "scrcpy -d", x=0.8, y=0.05, width=0.15, height=0.6, on_focus_lost_hide=False )
]))


colors = colors["night"]

layout_theme = {"border_width": 2,
                "margin": 4,
                "border_focus": colors["magenta"],
                "border_normal": colors["black"]
                }

layouts = [
    #layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.Max(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="CaskaydiaCove Nerd Font",
    fontsize=14,
    padding=5,
    foreground = colors["fg"],
    background = colors["bg"],

)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        
        top=bar.Bar(
            [
                #widget.CurrentLayout(),
                widget.GroupBox(
                    highlight_method="text", 
                    active = colors["amber"], # not current active font color
                    inactive = colors["fg"],
                    rounded = False,
                    disable_drag= True,
                    highlight_color = colors["red"],
                    this_current_screen_border = colors["cyan"], # current active font color - MAIN
                    this_screen_border = colors["magenta"],
                    other_current_screen_border = colors["bg"],
                    other_screen_border = colors["bg"],
                    urgent_border = colors["red"],
                    urgent_text= colors["red"],
                    #foreground = colors["fg"],
                    #background = colors["red"],
                    #hide_unused=True,
                    ),
                widget.Prompt(),
                widget.TextBox(
                    text='',
                    #text="",
                    foreground = colors["red"],
                    ),
                widget.WindowName(
                    format = "{name}",
                    max_chars = 25,
                    empty_group_string = 'Desktop',
                ),
                widget.Spacer(
                    length = bar.STRETCH
                    #background = "#0080FF00"
                    ),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                #widget.TextBox("this is not default       ", name="default"),
                #widget.Sep(),
                widget.CheckUpdates(
                    distro = "Arch_checkupdates",
                    update_interval = 1800,
                    display_format = "{updates}   ",
                    foreground = colors["blue"],
                    background = colors["bg"],
                    colour_have_updates = colors["blue"],
                    colour_no_updates = colors["red"],
                    no_update_string="No Updates"
                    ),
                #widget.TextBox(
                #    text="",
                #    foreground = colors["red"],
                #    ),
                # widget.Wttr(
                #     location={'El Salvador': 'home'},
                #     format = '%C, %t'
                #     ),
                # #widget.TextBox(
                #    text='',
                #    foreground = colors["red"],
                #    ),
                #widget.Sep(),
                widget.TextBox(
                    text="",
                    foreground = colors["red"],
                    ),
                widget.Net(
                    format='{down:6.2f}{down_suffix:<2} ↓↑ {up:6.2f}{up_suffix:<2}',
                    interface="enp0s20f0u1u2",
                    ),
                #widget.TextBox(
                #    text='',
                #    foreground = colors["red"],
                #    ),
                #widget.Sep(),
                widget.TextBox(
                    text="",
                    foreground = colors["red"],
                    ),
                widget.CPU(
                    format='  {load_percent}%'
                    
                    ),
                #widget.TextBox(
                #    text='',
                #    foreground = colors["red"],
                #    ),
                # widget.TextBox(
                #     text="",
                #     foreground = colors["red"],
                #     ),
                # #widget.Sep(),
                # widget.ThermalSensor(
                #     format=' {temp:.0f}{unit}',
                #     tag_sensor='Tctl',
                #     threshold=60,
                #     foreground_alert=colors["red"],
                #     foreground = colors["fg"],
                #     ),
                # #widget.Sep(),
                #widget.TextBox(
                #    text='',
                #    foreground = colors["red"],
                #    ),
                widget.TextBox(
                    text="",
                    foreground = colors["red"],
                    ),
                widget.Backlight(
                    backlight_name = 'intel_backlight',
                    format = '  {percent:2.0%}',
                    ),
                widget.TextBox(
                    #text='',
                    text="",
                    foreground = colors["red"],
                    ),
                #widget.Sep(),
                widget.Clock(format="%d/%m/%Y - %I:%M"),
                widget.TextBox(
                    #text='',
                    text="",
                    foreground = colors["red"],
                    ),
                widget.Systray(),
                #widget.QuickExit(),
            ],
            27, # bar height
            #border_color = [0, 0, 0, 0],    # Borders are transparent
            #border_width = [0, 0, 0, 0],    # Draw top and bottom borders
            #margin =      [15, 60, 6, 60], # Draw top and bottom borders
            margin =[5, 5, 3, 5], # Draw top and bottom borders   [ top, right, bottom, left ]
            
            

        ), 
    ),
]



dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.run([home])
