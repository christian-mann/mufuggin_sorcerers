"""
run from toplevel directory
"""
from PIL import Image, ImageDraw

CAMPUSMAP_IMAGE = 'foodfinder/website/static/img/campus-map.png'
CAMPUSMAP_LOCATIONS = 'foodfinder/website/static/img/building_locs.txt'

PIN_IMAGE = Image.open('foodfinder/website/static/img/pin-small.png')

SUBMAP_LOCATION = 'foodfinder/website/static/img/maps/%d.png'
SUBMAP_SIZE = (500, 500)

SATURATED_SIZE = (150, 150)

RECT_SIZE = (160, 160)

im = Image.open(CAMPUSMAP_IMAGE)

width, height = im.size


def get_submap(x, y):
    center = [x, y]
    box = [x-SUBMAP_SIZE[0]/2, y-SUBMAP_SIZE[1]/2, x+SUBMAP_SIZE[0]/2, y+SUBMAP_SIZE[1]/2]
    if box[0] < 0:
        box[2] += -box[0]
        box[0] = 0

    if box[1] < 0:
        box[3] += -box[1]
        box[1] = 0

    if box[2] > width:
        box[0] -= (width - box[2])
        box[2] = width

    if box[3] > height:
        box[1] -= (height - box[3])
        box[3] = height


    # get saturated subregion
    saturated = im.crop((center[0]-SATURATED_SIZE[0]/2, center[1]-SATURATED_SIZE[1]/2, center[0]+SATURATED_SIZE[0]/2, center[1]+SATURATED_SIZE[0]/2))
    #saturated.show()

    # desaturate image
    greyscale = im.convert('L')
    greyscale = greyscale.convert('RGBA')
    # draw red rectangle
    draw = ImageDraw.Draw(greyscale)
    draw.rectangle((center[0]-RECT_SIZE[0]/2, center[1]-RECT_SIZE[1]/2, center[0]+RECT_SIZE[0]/2, center[1]+RECT_SIZE[1]/2), fill=(255,0,0))
    del draw
    #greyscale.show()
    # paste sat. subregion back
    greyscale.paste(saturated, (center[0] - SATURATED_SIZE[0]/2, center[1]-SATURATED_SIZE[1]/2))
    #greyscale.show()

    # add the pin
    greyscale.paste(PIN_IMAGE, (center[0], center[1]-45), mask=PIN_IMAGE)


    region = greyscale.crop(box)
    return region


with open(CAMPUSMAP_LOCATIONS) as f:
    for line in f:
        bldg, x, y = map(int, line.split())
        submap = get_submap(x, y)
        submap.save(SUBMAP_LOCATION % bldg)
