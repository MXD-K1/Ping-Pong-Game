ALL_COLORS = {
    'screen': ['black'],
    'paddle 1': ['red', 'blue', 'yellow', 'orange', 'green', 'purple', 'chocolate', 'magenta', 'cyan'],
    'paddle 2': ['blue', 'yellow', 'orange', 'green', 'purple', 'chocolate', 'magenta', 'cyan', 'red'],
    'ball': ['white', 'red', 'blue', 'yellow', 'orange', 'green', 'purple', 'cyan', 'chocolate',
             'dark gray', 'magenta'],
    'text': ['white'],
    'button': ['white'],
    'button text': ['black'],
    'box': ['#6686ff'],
    'line': ['#63666A']  # Gray
}

POSITIONS = {component: 0 for component in ALL_COLORS.keys()}


def get_color(key: str):
    return ALL_COLORS[key][POSITIONS[key]]


def change_color(key: str, value_to_add: int = 1):
    POSITIONS[key] = (value_to_add + POSITIONS[key]) % len(ALL_COLORS[key])
