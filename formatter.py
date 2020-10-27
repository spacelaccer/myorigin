import wx
from typing import Dict, Optional, NamedTuple


"""
All modern web browsers support these 140 color names
"""
NAMED_COLORS: Dict[str, str] = {
    "AliceBlue": "#f0f8ff",
    "AntiqueWhite": "#faebd7",
    "Aqua": "#00ffff",
    "Aquamarine": "#7fffd4",
    "Azure": "#f0ffff",
    "Beige": "#f5f5dc",
    "Bisque": "#ffe4c4",
    "Black": "#000000",
    "BlanchedAlmond": "#ffebcd",
    "Blue": "#0000ff",
    "BlueViolet": "#8a2be2",
    "Brown": "#a52a2a",
    "BurlyWood": "#deb887",
    "CadetBlue": "#5f9ea0",
    "Chartreuse": "#7fff00",
    "Chocolate": "#d2691e",
    "Coral": "#ff7f50",
    "CornflowerBlue": "#6495ed",
    "Cornsilk": "#fff8dc",
    "Crimson": "#dc143c",
    "Cyan": "#00ffff",
    "DarkBlue": "#00008b",
    "DarkCyan": "#008b8b",
    "DarkGoldenRod": "#b8860b",
    "DarkGray": "#a9a9a9",
    "DarkGreen": "#006400",
    "DarkGrey": "#a9a9a9",
    "DarkKhaki": "#bdb76b",
    "DarkMagenta": "#8b008b",
    "DarkOliveGreen": "#556b2f",
    "DarkOrange": "#ff8c00",
    "DarkOrchid": "#9932cc",
    "DarkRed": "#8b0000",
    "DarkSalmon": "#e9967a",
    "DarkSeaGreen": "#8fbc8f",
    "DarkSlateBlue": "#483d8b",
    "DarkSlateGray": "#2f4f4f",
    "DarkSlateGrey": "#2f4f4f",
    "DarkTurquoise": "#00ced1",
    "DarkViolet": "#9400d3",
    "DeepPink": "#ff1493",
    "DeepSkyBlue": "#00bfff",
    "DimGray": "#696969",
    "DimGrey": "#696969",
    "DodgerBlue": "#1e90ff",
    "FireBrick": "#b22222",
    "FloralWhite": "#fffaf0",
    "ForestGreen": "#228b22",
    "Fuchsia": "#ff00ff",
    "Gainsboro": "#dcdcdc",
    "GhostWhite": "#f8f8ff",
    "Gold": "#ffd700",
    "GoldenRod": "#daa520",
    "Gray": "#808080",
    "Green": "#008000",
    "GreenYellow": "#adff2f",
    "Grey": "#808080",
    "HoneyDew": "#f0fff0",
    "HotPink": "#ff69b4",
    "IndianRed": "#cd5c5c",
    "Indigo": "#4b0082",
    "Ivory": "#fffff0",
    "Khaki": "#f0e68c",
    "Lavender": "#e6e6fa",
    "LavenderBlush": "#fff0f5",
    "LawnGreen": "#7cfc00",
    "LemonChiffon": "#fffacd",
    "LightBlue": "#add8e6",
    "LightCoral": "#f08080",
    "LightCyan": "#e0ffff",
    "LightGoldenRodYellow": "#fafad2",
    "LightGray": "#d3d3d3",
    "LightGreen": "#90ee90",
    "LightGrey": "#d3d3d3",
    "LightPink": "#ffb6c1",
    "LightSalmon": "#ffa07a",
    "LightSeaGreen": "#20b2aa",
    "LightSkyBlue": "#87cefa",
    "LightSlateGray": "#778899",
    "LightSlateGrey": "#778899",
    "LightSteelBlue": "#b0c4de",
    "LightYellow": "#ffffe0",
    "Lime": "#00ff00",
    "LimeGreen": "#32cd32",
    "Linen": "#faf0e6",
    "Magenta": "#ff00ff",
    "Maroon": "#800000",
    "MediumAquaMarine": "#66cdaa",
    "MediumBlue": "#0000cd",
    "MediumOrchid": "#ba55d3",
    "MediumPurple": "#9370db",
    "MediumSeaGreen": "#3cb371",
    "MediumSlateBlue": "#7b68ee",
    "MediumSpringGreen": "#00fa9a",
    "MediumTurquoise": "#48d1cc",
    "MediumVioletRed": "#c71585",
    "MidnightBlue": "#191970",
    "MintCream": "#f5fffa",
    "MistyRose": "#ffe4e1",
    "Moccasin": "#ffe4b5",
    "NavajoWhite": "#ffdead",
    "Navy": "#000080",
    "OldLace": "#fdf5e6",
    "Olive": "#808000",
    "OliveDrab": "#6b8e23",
    "Orange": "#ffa500",
    "OrangeRed": "#ff4500",
    "Orchid": "#da70d6",
    "PaleGoldenRod": "#eee8aa",
    "PaleGreen": "#98fb98",
    "PaleTurquoise": "#afeeee",
    "PaleVioletRed": "#db7093",
    "PapayaWhip": "#ffefd5",
    "PeachPuff": "#ffdab9",
    "Peru": "#cd853f",
    "Pink": "#ffc0cb",
    "Plum": "#dda0dd",
    "PowderBlue": "#b0e0e6",
    "Purple": "#800080",
    "RebeccaPurple": "#663399",
    "Red": "#ff0000",
    "RosyBrown": "#bc8f8f",
    "RoyalBlue": "#4169e1",
    "SaddleBrown": "#8b4513",
    "Salmon": "#fa8072",
    "SandyBrown": "#f4a460",
    "SeaGreen": "#2e8b57",
    "SeaShell": "#fff5ee",
    "Sienna": "#a0522d",
    "Silver": "#c0c0c0",
    "SkyBlue": "#87ceeb",
    "SlateBlue": "#6a5acd",
    "SlateGray": "#708090",
    "SlateGrey": "#708090",
    "Snow": "#fffafa",
    "SpringGreen": "#00ff7f",
    "SteelBlue": "#4682b4",
    "Tan": "#d2b48c",
    "Teal": "#008080",
    "Thistle": "#d8bfd8",
    "Tomato": "#ff6347",
    "Turquoise": "#40e0d0",
    "Violet": "#ee82ee",
    "Wheat": "#f5deb3",
    "White": "#ffffff",
    "WhiteSmoke": "#f5f5f5",
    "Yellow": "#ffff00",
    "YellowGreen": "#9acd32",
}
_named_colors_lowercase = {key.lower(): value.lstrip('#')
                           for key, value in NAMED_COLORS.items()}


# Default Styling. Mapping from class names to their style definition
# Warning: Maybe overwriten by resources file
DEFAULT_STYLES = [
    ("prompt", "bg:white fg:red bold"),
    ("completion-menu.completion.current", "bg:#999999 #000000"),
    ("completion-menu.completion", "")
]


# Default style for widgets
# Warning: Maybe overwriten by resources file
WIDGETS_STYLE = [
    ("dialog", "bg:#4444ff"),
    ("dialog.body", "bg:#33ffff"),
    ("button", ""),
    ("button.arrow", "bold"),
    ("button.focused", "bg:#aa0000, #ffffff"),
]

# rules that we actually need
STYLE_RULES = [

]


Attrs = NamedTuple(
    "Attrs",
    [
        ("fg", Optional[str]),
        ("bg", Optional[str]),
        ("bold", Optional[bool]),
        ("underline", Optional[bool]),
        ("italic", Optional[bool]),
        ("blink", Optional[bool]),
        ("reverse", Optional[bool]),
        ("hidden", Optional[bool]),
    ],
)

# default attrs
DEFAULT_ATTRS = Attrs(
    fg = "",
    bg = "",
    bold = False,
    underline = False,
    italic = False,
    blink = False,
    reverse = False,
    hidden = False,
)

# Empty attributes collection
EMPTY_ATTRS = Attrs(
    fg = None,
    bg = None,
    bold = None,
    underline = None,
    italic = None,
    blink = None,
    reverse = None,
    hidden = None,
)



class ShellFormatter:

    fgcolor = (0, 0, 0)
    bgcolor = (255, 255, 255)
    face = 'Consolas'    # font face
    size = 15
    bold = False
    underline = False
    italic = False
    blink = False
    reverse = False
    hidden = False

    attr = wx.TextAttr()
    font = wx.Font()
    #self.inter.SetFont(wx.Font(wx.FontInfo(self.size).FaceName(self.font)))
    rules = [
        {"prompt": "bg:#ffffff fg:#ff0000 font:Consolas size:15 bold"},
        {"buffer": "bg:#ffffff fg:#0000ff font:Consolas size:15 nobold"},
        {"output": "bg:#ffffff fg:#00ff00 font:Consolas size:15 nobold"},
    ]

    @classmethod
    def add_style_rule(cls, classname, style_str):
        """
        add one style style into style rules
        :param classname:
        :param style_str:
        :return:
        """
        for rule in cls.rules:
            if classname in rule:  # rule is a dict
                rule.update({classname: style_str.strip('"\'')})
                return
        cls.rules.append({classname: style_str.strip('"\'')})

    @staticmethod
    def _parse_color(text: str):
        """
        Parse/Validate color format
        :return:
        """
        try:
            color = _named_colors_lowercase[text.lower()]
            return (int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16))
        except KeyError:
            pass

        # Hexadecimal format color codes
        if text[0:1] == '#':
            color = text[1:]

            if len(color) == 6:     # 6 digits hex color
                return (int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16))
            #   return color
            elif len(color) == 3:   # 3 digits hex color
                return (int(color[0]*2, 16), int(color[1]*2, 16), int(color[2]*2, 16))
            #   return color[0]*2 + color[1]*2 + color[2]*2

        elif text in ("", "default"):
            return text

        raise ValueError("invalid color format: %r" % text)

    @classmethod
    def _parse_format(cls, format_string):
        """
        parsing format string given
        :param format_string:
        :return:
        """
        for part in format_string.split():
            if part == 'bold':
                cls.bold = True
            elif part == 'nobold':
                cls.bold = False
            elif part.startswith("bg:"):
                cls.bgcolor = cls._parse_color(part[3:])
            elif part.startswith("fg:"):
                cls.fgcolor = cls._parse_color(part[3:])
            elif part.startswith("font:"):
                cls.face = part[5:]
            elif part.startswith("size:"):
                cls.size = int(part[5:])
            else:
                print("unrecognizable part: %s" % part)

    @classmethod
    def attr_formatter(cls, style_classname):
        """
        get style object parsed from style_str
        :param style_str: style in the form of string
        :return:
        """
        for rule in cls.rules:
            if style_classname in rule:
                cls._parse_format(rule[style_classname])

                cls.attr.SetFontFaceName(cls.face)
                cls.attr.SetFontSize(cls.size)
                if cls.bold:
                    cls.attr.SetFontWeight(wx.FONTWEIGHT_BOLD)
                else:
                    cls.attr.SetFontWeight(wx.FONTWEIGHT_NORMAL)

                cls.attr.SetBackgroundColour(cls.bgcolor)
                cls.attr.SetTextColour(cls.fgcolor)

                return cls.attr
        raise Exception("%s: classname not found in style rules" % style_classname)

    @classmethod
    def font_formatter(cls):
        cls.font.SetFaceName(cls.face)
        cls.font.SetPointSize(cls.size)
        if cls.bold:
            cls.font.SetWeight(wx.FONTWEIGHT_BOLD)
        return cls.font
