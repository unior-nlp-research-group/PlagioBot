import io
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

FONT_SIZE = 20
EMOJI_FONT = ImageFont.truetype("fonts/Symbola.ttf", FONT_SIZE, encoding="utf-8")
TEXT_FONT = ImageFont.truetype("fonts/Roboto-Regular.ttf", FONT_SIZE, encoding="utf-8")

MARGIN = 25
#COLUMN_WIDTH = 100
ROW_HEIGHT = 30
TEXT_HEIGHT = max(EMOJI_FONT.getsize('M')[1], TEXT_FONT.getsize('M')[1])

def get_image_data_from_points(names, points, show=False):
    ranks_players_point = {p: [n for i,n in enumerate(names) if points[i]==p] for p in set(points)}        
    table = []
    for r,(points,name_list) in enumerate(sorted(ranks_players_point.items(),key=lambda x: x[0], reverse=True), 1):
        rank = '🥇' if r==1 else '🥈' if r==2 else '🥉' if r==3 else str(r)
        for name in name_list:
            table.append([rank, name, str(points)])
    img_data = get_image_data_from_table(table, alignment = 'clr', show=show)
    return img_data

def get_image_data_from_hands_points(names, hands_points, total_points, show=False):
    num_hands = len(hands_points)
    player_index_points_info = {}
    total_points_ordered_set = sorted(set(total_points), reverse=True)
    for i,n in enumerate(names):
        player_index_points_info[i] = {
            'name': n,
            'index': i,
            'rank': total_points_ordered_set.index(total_points[i])+1,
            'points': [hp[i] for hp in hands_points]
        }
    table = []
    table_header = ['', ''] + [str(r) for r in range(1,num_hands+1)] + ['TOT']
    alignment = 'cl' + 'r' * (num_hands+1)
    table.append(table_header)
    # todo: line
    for player_info in sorted(player_index_points_info.values(), key=lambda x: x['rank']):
        r = player_info['rank']
        rank = '🥇' if r==1 else '🥈' if r==2 else '🥉' if r==3 else str(r)
        tp = total_points[player_info['index']]
        table_row = \
            [rank, player_info['name']] + \
            [str(hp) for hp in player_info['points']] + \
            [str(tp)]
        table.append(table_row)
    img_data = get_image_data_from_table(table, alignment, show=show)
    return img_data

def get_image_data_from_table(result_table, alignment, show=False):
    NUMBER_ROWS = len(result_table)
    #NUMBER_COLUMNS = len(result_table[0])    
    COLUMNS_WIDTH = [ 2*MARGIN+max(TEXT_FONT.getsize(row[j])[0] for row in result_table) for j in range(len(result_table[0]))]
    WIDTH = MARGIN * 2 + sum(COLUMNS_WIDTH)
    HEIGHT = MARGIN * 2 + TEXT_HEIGHT + NUMBER_ROWS * ROW_HEIGHT
    img = Image.new("RGBA", (WIDTH, HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    for i, row in enumerate(result_table):
        for j, text in enumerate(row):
            text = text
            FONT = EMOJI_FONT if j==0 else TEXT_FONT
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
    return get_image_data_from_table(result_table, alignment, show)

def test1(show=False):
    # return get_image_data_from_points(names=['BOB','PETER','ALEX'], points=[5,3,1], show=show)
    return get_image_data_from_points(names=['Gülşen Eryiğit','B','C','D','E','F','G','H'], points=[1, 2, 1, 2, 1, 4, 0, 3], show=show)

def test2(show=False):
    names=['Gülşen Eryiğit','Bob','Alice','Rob']
    hands_points = [
        [0, 2, 1, 2],
        [0, 2, 1, 2],
        [0, 2, 1, 2],
        [0, 2, 1, 2],
        [0, 2, 1, 2]
    ]
    total_points = [
        sum([hp[i] for hp in hands_points]) 
        for i in range(len(hands_points[0]))
    ]
    return get_image_data_from_hands_points(
        names, hands_points, total_points, show=show)


if __name__ == "__main__": 
    # test(show=True)
    # test1(show=True)
    test2(show=True)