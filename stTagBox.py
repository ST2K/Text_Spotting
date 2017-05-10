#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python version: 3.6.1 -*-

import os
import numpy as np
from PIL import Image
import matplotlib.path as mplPath

_OLD_TAG_PATH = "./pics_ann/tag_result/"

tb = TagBox()
mib = MiniImageBox()

class TagBox():

    def load_tag_old(self, picname):
        xbox = []
        ybox = []
        content = []
        with open(_TAG_PATH + picname + ".txt", "r") as t:
            text = ' '.join(t.readline().split()).split(";")
            assert(text[0].replace("\t", "").split(" ")[0] == picname)
            text[0] = text[0][text[0].find(" "):-1]
            for line in text:
                line = line.strip().split(" ")
                xbox.append(list(map(int, line[0:-2:2])))
                ybox.append(list(map(int, line[1:-1:2])))
                content.append(line[-1])
        return np.array(xbox), np.array(ybox), content

    def load_tag(self, picname, picpath):
        xbox = []
        ybox = []
        content = []
        with open(picpath + picname.replace(".jpg", ".txt"), "r", encoding = "GBK") as t:
            cnt = 0
            for line in t:
                if (cnt % 3 == 0 and line != ""):
                    line = line.strip().split(",")
                    xbox.append(list(map(int, line[0:-1:2])))
                    ybox.append(list(map(int, line[1::2])))
                if (cnt % 3 == 1):
                    content.append(line.strip())
                cnt += 1
        return (np.array(xbox).astype(int), np.array(ybox).astype(int), content)

    def shrink_tag(self, tag, ratio = 1.0):
        return (np.floor(tag[0] * ratio).astype(int), np.floor(tag[1] * ratio).astype(int), tag[2])

    def tag2array(self, tag, array_size):
        (xbox, ybox, content) = tag
        array = np.zeros(array_size, dtype=np.int)
        xy = np.array([xbox.T, ybox.T]).T
        for i in range(0, len(xy)):
            maxx = max(xbox[i])
            maxy = max(ybox[i])         
            minx = min(xbox[i])
            miny = min(ybox[i])
            if (maxx > array_size[0]):
                maxx = array_size[0]
            if (maxy > array_size[1]):
                maxy = array_size[1]
            if (minx < 0):
                minx = 0
            if (miny < 0):
                miny = 0
            pth = mplPath.Path(xy[i])
            for x in range(minx, maxx):
                for y in range(miny, maxy):
                    if (pth.contains_point((x, y))):
                        array[y][x] = 1
        return array.flatten()

    def get_tag_array(self, tagfile, filepath, array_size):
        tag = self.load_tag(tagfile, filepath)
        return self.tag2array(tag, array_size)

class MiniImageBox():

    def load_image(self, picname, picpath, mode = None):
        im = Image.open(picpath + picname)
        if (mode):
            # "1" for monochrome, "L" for greyscale, "LA" for "L" with alpha
            im = im.convert(mode)
        return im

    def image2nparray(self, img):
        return np.array(img, dtype=np.uint8)

def get_data(picname, picpath):
    im = mib.load_image(picname, picpath, "L")
    imgarr = mib.image2nparray(im).flatten()
    tagarr = tb.get_tag_array(picname, picpath, im.size)
    return imgarr, tagarr

if __name__ == "__main__":
    pass
                