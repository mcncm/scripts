#! /bin/python

import sys

def reshade(color: str, factor: float):
    """accepts a color as a hex string, reshades it by a factor and returns"""
    assert(len(color) == 7 and color[0] == '#')
    hex_strs = [color[i:i+2] for i in range(1, len(color), 2)]
    color_ints =  map(lambda x: int(x, 16), hex_strs)
    rescaled_colors = map(lambda x: int(max(0, min(255, factor * x))), color_ints) # should fail differently
    hex_str_out = ''.join(map(lambda x: x[2:].zfill(2), map(hex, map(round, rescaled_colors)))).upper()
    print('#' + hex_str_out)

if __name__ == '__main__':
    reshade(sys.argv[1], float(sys.argv[2]))
