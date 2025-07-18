ALL_COLORS = {
    'screen': {'colors': ['black', 'white'], 'pos': 0},
    'paddle 1': {'colors': ['red', 'blue', 'yellow', 'orange', 'green', 'purple', 'cyan'], 'pos': 0},
    'paddle 2': {'colors': ['blue', 'yellow', 'orange', 'green', 'purple', 'cyan', 'red'], 'pos': 0},
    'ball': {'colors': ['white', 'black', 'red', 'blue', 'yellow', 'orange', 'green', 'purple', 'dark gray'], 'pos': 0},
    'text': {'colors': ['white', 'black'], 'pos': 0},
    'button': {'colors': ['white', 'black'], 'pos': 0},
    'button text': {'colors': ['black', 'white'], 'pos': 0},
    'box': {'colors': ['yellow'], 'pos': 0}  # yellow temp
}


def get_color(colors: dict, key: str):
    return colors[key]['colors'][colors[key]['pos']]
