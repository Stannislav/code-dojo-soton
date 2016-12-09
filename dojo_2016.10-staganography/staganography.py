#!/usr/local/bin/python
from PIL import Image
from numpy import array

def encode(img, img_secret):
    data = array(img)
    data_secret = array(img_secret)
    if len(data) != len(data_secret):
        print "Images not same length"
        return false

    for j in range(0, len(data)):
        for i in range(0, len(data[0])):
            data[j, i, 2] = (data[j, i, 2] >> 1 << 1) | data_secret[j, i]
    return Image.fromarray(data)


def decode(codedim):
    imdata = array(codedim)
    lx = len(imdata)
    ly = len(imdata[0])

    for ipix in range(0, lx):
        for jpix in range(0, ly):
            bit = 255 * (1-imdata[ipix, jpix, 2] % 2)
            imdata[ipix, jpix] = [bit,bit,bit]

    return Image.fromarray(imdata, 'RGB')

def decode2(img):
    data = array(img)
    res = [[(1-entry[2]&1)*255 for entry in row] for row in data]
    return Image.fromarray(array(res).astype('uint8'))

def main():
    img = Image.open("img/duck.png")
    img_secret = Image.open("img/p1bw.png")

    encoded = encode(img, img_secret)
    decoded = decode(encoded)
    decoded2 = decode2(encoded)

    encoded.show()
    decoded.show()
    decoded2.show()

if __name__ == '__main__':
    main()
