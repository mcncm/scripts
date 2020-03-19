import os
import json

ini_path = os.path.join(os.path.expanduser('~'),
                '.config', 'spicetify', 'Themes', 'wal', 'color.ini')

colors_path = os.path.join(os.path.expanduser('~'),
                '.cache', 'wal', 'colors.json')

def strip_hashes(colors_dict):
    """ '#FFFFFF' -> 'FFFFFF'
    """
    return {key: value[1:] for key, value in colors_dict.items()}

with open(colors_path, 'r') as f:
    contents = json.load(f)
    # contents['special'] contains the keys "background", "foreground", and
    # "cursor".
    all_colors = {**contents['colors'], **contents['special']}
    colors = {key: value[1:] for key, value in all_colors.items()}

ini_contents = f"""
[Base]
main_fg       = {colors['color7']}
secondary_fg  = {colors['color5']}
main_bg       = {colors['background']}
slider_bg     = {colors['color2']}

sidebar_and_player_bg                 = {colors['color0']}
cover_overlay_and_shadow              = 000000
indicator_fg_and_button_bg            = {colors['color7']}
pressing_fg                           = FFFFFF
sidebar_indicator_and_hover_button_bg = {colors['color7']}
scrollbar_fg_and_selected_row_bg      = {colors['color1']}
pressing_button_fg                    = {colors['color7']}
pressing_button_bg                    = {colors['color0']}
selected_button                       = {colors['color7']}
miscellaneous_bg                      = {colors['color5']}
miscellaneous_hover_bg                = {colors['color5']}
preserve_1                            = FFFFFF
"""

if __name__ == '__main__':
    with open(ini_path, 'w') as f:
        f.write(ini_contents)
