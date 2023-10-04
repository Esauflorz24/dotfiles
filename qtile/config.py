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

mod = "mod4"
terminal = "kitty"
browser = "firefox"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "Tab", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "Left", 
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
    ),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "Right", 
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "Down", 
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
    ),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod, "control"], "Up", 
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
    ),

    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # custom    
    Key([mod],"space", lazy.spawn("dmenu_run -l 10 -g 4 -p 'λ' "), desc='dmenu'),
    Key([mod],"b", lazy.spawn("firefox"), desc='dmenu'),
    Key([mod],"v", lazy.spawn("virt-manager"), desc='dmenu'),
    Key([mod],"t", lazy.spawn("telegram-desktop"), desc='dmenu'),
    Key([mod],"m", lazy.spawn("rofi -show drun"), desc='dmenu'),
    # Key([mod],"b", lazy.spawn("bookmark"), desc='dmenu'),
    Key([mod],"s", lazy.spawn("svs"), desc='dmenu'),
    Key([mod],"e", lazy.spawn("alacritty -e nvim"), desc='dmenu'),
    Key([mod], "f", lazy.window.toggle_fullscreen()),

    # Switch focus to specific monitor (out of three)
    Key([mod], "o", lazy.to_screen(0)),
    Key([mod], "i", lazy.to_screen(1)),

    # Switch focus of monitors
    Key([mod], "period", lazy.next_screen()),
    Key([mod], "comma", lazy.prev_screen()),
]

#groups = [Group(i) for i in "123456789"]
groups = [
    Group(
        '1',
        label="一",
        matches=[
            Match(wm_class=["Alacritty", "kitty"]),
            ],
        layout="monadtall"
    ),
    Group('2', label="二", layout="max", matches=[Match(wm_class=["firefox", "brave"])]),
    Group('3', label="三", layout="monadtall", matches=[Match(wm_class=["telegram-desktop"])]),
    Group('4', label="四", layout="monadtall", matches=[Match(wm_class=["qBittorrent"])]),
    Group('5', label="五", layout="monadtall", matches=[Match(wm_class=["discord"])]), 
    Group('6', label="六", layout="monadtall"), 
    Group('7', label="七", layout="monadtall"), 
    Group('8', label="八", layout="monadtall"), 
    Group('9', label="九", layout="monadtall"), 
    Group('0', label="十", layout="max", matches=[Match(wm_class=["mpv"])])
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
    layout.Max(**layout_theme),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
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
                    active = colors["magenta"], # not current active font color
                    inactive = colors["fg"],
                    rounded = False,
                    disable_drag= True,
                    highlight_color = colors["red"],
                    this_current_screen_border = colors["magenta"], # current active font color - MAIN
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
                #widget.WindowName(),
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
                    display_format = "{updates} ",
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
                    prefix='M',
                    format='{down} ↓↑ {up}',
                    interface="wlan0"
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
                widget.MemoryGraph(
                    type="box",
                    border_color="#1A1B26",
                    update_interval=5,
                    ),
                widget.TextBox(
                    #text='',
                    text="",
                    foreground = colors["red"],
                    ),
                #widget.Sep(),
                widget.Clock(format="%d/%m/%Y - %I:%M"),
                #widget.QuickExit(),
            ],
            27, # bar height
            #border_color = [0, 0, 0, 0],    # Borders are transparent
            #border_width = [0, 0, 0, 0],    # Draw top and bottom borders
            #margin =      [15, 60, 6, 60], # Draw top and bottom borders
            margin =      [5, 5, 3, 5], # Draw top and bottom borders   [ top, right, bottom, left ]
        ), 
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
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
