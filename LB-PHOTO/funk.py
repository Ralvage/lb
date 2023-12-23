from PIL import Image

def cod(File, Text, Save):
    file = (File)

    im = Image.open(file).convert('RGBA')
    pix = im.load()
    w, h = im.size

    nan = str(Text)

    if h < 255:
        if len(nan) > h:
            return 0
    elif len(nan) > 255:
        return 0

    r, g, b, a = pix[0, 0]
    pix[0, 0] = len(nan), g, b, a

    for i in range(len(nan)):
        r, g, b, a = pix[0, i+1]
        pix[0, i+1] = ord(nan[i]), g, b, a

    im.save(Save)

    return Save

def decod(File):
    file2 = (File)

    im = Image.open(file2).convert('RGBA')
    pix = im.load()

    name = ''
    r, g, b, a = pix[0, 0]

    for j in range(int(r)):
        r1, g1, b1, a1 = pix[0, j+1]
        name += chr(r1)

    return name