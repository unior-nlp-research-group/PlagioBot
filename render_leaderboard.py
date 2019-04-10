# -*- coding: utf-8 -*-
import io
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

FONT_SIZE = 20
FONT = ImageFont.truetype("fonts/Symbola.ttf",FONT_SIZE)

MARGIN = 25
#COLUMN_WIDTH = 100
ROW_HEIGHT = 30
TEXT_HEIGHT = FONT.getsize('M')[1]

def get_image_data_from_points(names, points, show=False):
    ranks_players_point = {p: [n for i,n in enumerate(names) if points[i]==p] for p in set(points)}        
    table = []
    for r,(points,name_list) in enumerate(sorted(ranks_players_point.items(),key=lambda x: x[0], reverse=True), 1):
        rank = '🥇' if r==1 else '🥈' if r==2 else '🥉' if r==3 else r
        for name in name_list:
            table.append([rank, name, str(points)])
    img_data = get_image_data_from_table(table, alignment = 'clr', show=show)
    return img_data

def get_image_data_from_table(result_table, alignment, show=False):
    NUMBER_ROWS = len(result_table)
    #NUMBER_COLUMNS = len(result_table[0])    
    COLUMNS_WIDTH = [ 2*MARGIN+max(FONT.getsize(row[j])[0] for row in result_table) for j in range(len(result_table[0]))]
    WIDTH = MARGIN * 2 + sum(COLUMNS_WIDTH)
    HEIGHT = MARGIN * 2 + TEXT_HEIGHT + NUMBER_ROWS * ROW_HEIGHT
    img = Image.new("RGBA", (WIDTH, HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    for i, row in enumerate(result_table):
        for j, text in enumerate(row):
            text = text
            TEXT_WIDTH = FONT.getsize(text)[0]
            aligne = alignment[j]
            if aligne=='l':                
                x = sum(COLUMNS_WIDTH[:j]) + MARGIN 
            elif aligne=='c':
                x = sum(COLUMNS_WIDTH[:j]) + MARGIN + (COLUMNS_WIDTH[j]-TEXT_WIDTH)/2
            else:
                assert(aligne=='r')
                x = sum(COLUMNS_WIDTH[:j]) - TEXT_WIDTH
            y = ROW_HEIGHT*(i+1) + MARGIN - TEXT_HEIGHT
            draw.text((x, y), text, (0, 0, 0), font=FONT)
    with io.BytesIO() as imgData:
        img.save(imgData, format="PNG")
        contents = imgData.getvalue()
    if show:
        img.show()
    return contents

def test(show=False):
    # ['RANK', 'NAME', 'POINTS', 'BADGES'],
    result_table = [
        ['🥇', 'BOB', '5', '4'],
        ['🥈', 'PETER', '3', '2'],
        ['🥉', 'ALEX', '1', '3']
    ]
    alignment = 'clcc'
    #return get_image_data_from_table(result_table, alignment, show)
    return get_image_data_from_points(names=['BOB','PETER','ALEX'], points=[5,3,1], show=show)

if __name__ == "__main__": 
    test(show=True)