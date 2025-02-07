from src.bar import Bar

def test_initialization() -> None:
    window_height = 600
    window_width = 800
    bottom_padding = 50
    bar = Bar(window_height, window_width, bottom_padding)

    assert bar.bar_x == 0
    assert bar.bar_y == window_height - bottom_padding
    assert bar.bar_width == window_width
    assert bar.bar_height == bottom_padding
    assert bar.total_time == 15 * 1000
    assert bar.main_color == 'gray17'
    assert bar.alt_color == 'ghostwhite'