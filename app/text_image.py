import cv2 as cv
import numpy as np


def hconcat_resize(img_list, interpolation=cv.INTER_CUBIC):
    h_min = min(img.shape[0] for img in img_list)

    im_list_resize = [
        cv.resize(img, (int(img.shape[1] * h_min / img.shape[0]), h_min),
                  interpolation=interpolation) for img in img_list
    ]

    return cv.hconcat(im_list_resize)


def text2sign(words):
    characters = list("!-$%&'()*+,./:;<=>?_[]^`{|}~@#")
    characters.append(' ')

    img = np.zeros((0, 0, 3), np.uint8)
    alpha_img = np.zeros((0, 0, 3), np.uint8)
    img_list = []
    alphabet = ''
    count = 0
    for word in words:
        count += 1
        for i in word:
            if i in characters: continue
            alphabet = i.upper()
            alpha_img = cv.imread('text-image_data/' + alphabet + '.png')
            shape = alpha_img.shape
            cv.resize(alpha_img, (150, 250), interpolation=cv.INTER_LINEAR)
            img_list.append(alpha_img)
        if count != len(words):
            img_list.append(cv.imread('text-image_data/space.png'))

    img = hconcat_resize(img_list)
    return img


#inp = input().strip().split()
#text2sign(inp)
