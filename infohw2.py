# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 12:42:15 2019

@author: Lizerhigh
"""

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

def create_image(i, j):
  image = Image.new("RGB", (i, j), "white")
  return image

def set_pixel(img, i, j, c):
    img[i, j] = (c, c, c)
    
def add_text(draw, xy, text, size, color):
    # draw.text((x, y),"Sample Text",(r,g,b))
    font = ImageFont.truetype('minreg.ttf', size)
    draw.text(xy, text,color, font=font)
    #draw.line((x, y, 100, 100), fill=128)

def add_line(draw, line):
    draw.line(line, fill=128)

def avg(s):
    return sum(s)//len(s)
        
def find_parent(layers, pname):
    for i in range(len(layers)):
        layer_k = list(layers[i].keys())
        for j in range(len(layers[i])):
            if pname == layer_k[j]:
                x = (2000//33)*layers[i][layer_k[j]][1]
                y = i*80 + 40
                return (x, y)

f = open('letterfreq.txt', 'r', encoding='utf-16')
lines = f.readlines()
d = {k[-1]: float(v[:-1]) for k, v in map(lambda x: x.split(': '), lines)}

d = {k: v for k, v in sorted(d.items(), key = lambda x: x[1])}
d_keys = list(d.keys())
layers = [{k: (v, d_keys.index(k), []) for k, v in d.items()}]
while len(d) != 1:
    tmp = sorted(d.items(), key = lambda x: x[1])
    tmp, mins = tmp[2:], tmp[:2]
    d = {k: v for k, v in tmp}
    s_key = ''.join(map(lambda x: x[0], mins))
    s_val = sum(map(lambda x: x[1], mins))
    d[s_key] = s_val
    layers.append({s_key: (s_val, avg([d_keys.index(x) for x in s_key]), [k for k, v in mins])})
   
    
size = (2000, 3000)
img = create_image(*size)
draw = ImageDraw.Draw(img)
letters = {k: '' for k, v in layers[0].items()}
for j in range(len(layers)):
    length = len(layers[j])
    keys = list(layers[j].keys())
    for i in range(length):
        s_val = layers[j][keys[i]]
        add_text(draw, ((size[0]//33)*s_val[1], j*80), keys[i], 24, (0,0,0))
        add_text(draw, ((size[0]//33)*s_val[1], j*80 + 26), str(s_val[0])[:6], 12, (255,0,0))
        for x in range(len(s_val[2])):
            line = ((size[0]//33)*s_val[1], j*80)+find_parent(layers, s_val[2][x])
            add_line(draw, line)
            center = (line[2], line[3])
            add_text(draw, center, str(len(s_val[2])-x-1), 20, (0, 0, 255))
            for y in s_val[2][x]:
                letters[y] += str(len(s_val[2])-x-1)
#print(letters)
f = open('lettercodes.txt', 'wb')
lines = [bytes(f'{k}: {v[::-1]}'+'\n', encoding='utf-16') for k, v in letters.items()]
f.writelines(lines)
f.close()
img.save('haffman_tree.jpg')
img.show()

