import cv2


if __name__ == '__main__':

    path = 'example/source/男子排球 八強戰 波蘭 - 中華 完整版 2019拿坡里世大運 [i5nb0VvktN8]_cut 182.jpg'
    img = cv2.imread(path)
    
    y = len(img)
    x = len(img[0])

    print('input x1 y1 to draw the line:')
    while True:
        line_index = input()
        if line_index == '':
            break
        index = [int(index) for index in line_index.split(' ')]
        img = cv2.circle(img, (index[0], index[1]), 3, (255, 0, 0), -1)
    
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
