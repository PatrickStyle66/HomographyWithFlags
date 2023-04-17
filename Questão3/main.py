import cv2 as cv
import numpy as np

positions = []
positions2 = []
count = 0
# Seleciona-se 4 pontos na imagem que irão ser substituidos pela bandeira
def draw_circle(event, x, y, flags, param):
    global positions, count
    # If event is Left Button Click then store the coordinate in the lists
    if event == cv.EVENT_LBUTTONUP:
        cv.circle(piscina, (x, y), 2, (255, 0, 0), -1)
        positions.append([x, y])
        if (count != 3):
            positions2.append([x, y])
        elif (count == 3):
            positions2.insert(2, [x, y])
        count += 1

imageList = ['Franca','Chile','AfricaDoSul','Suica','Franca','Chile','AfricaDoSul','Suica','banner']
# Após selecionar os 4 pontos, aperte ESC para prosseguir para a próxima seleção!
# A última seleção é a do banner
first = True
for image in imageList:
    positions = []
    positions2 = []
    count = 0
    if first:
        piscina = cv.imread('piscina.jpg')
        first = False
    else:
        piscina = cv.imread('piscinaFinal.jpg')
    franca = cv.imread(f'{image}.png')
    # Defing a window named 'image'
    cv.namedWindow('image')
    cv.setMouseCallback('image', draw_circle)
    while (True):
        cv.imshow('image', piscina)
        k = cv.waitKey(20) & 0xFF
        if k == 27:
            break
    cv.destroyAllWindows()

    height, width = piscina.shape[:2]
    h1, w1 = franca.shape[:2]

    pts1 = np.float32([[0, 0], [w1, 0], [0, h1], [w1, h1]])
    pts2 = np.float32(positions)

    h, mask = cv.findHomography(pts1, pts2, cv.RANSAC, 5.0)

    height, width, channels = piscina.shape
    im1Reg = cv.warpPerspective(franca, h, (width, height))

    mask2 = np.zeros(piscina.shape, dtype=np.uint8)

    roi_corners2 = np.int32(positions2)

    channel_count2 = piscina.shape[2]
    ignore_mask_color2 = (255,) * channel_count2

    cv.fillConvexPoly(mask2, roi_corners2, ignore_mask_color2)

    mask2 = cv.bitwise_not(mask2)
    masked_image2 = cv.bitwise_and(piscina, mask2)

    # Using Bitwise or to merge the two images
    final = cv.bitwise_or(im1Reg, masked_image2)
    cv.imwrite('piscinaFinal.jpg', final)
#Apertar ESC para fechar a imagem
while (True):
    cv.imshow('image', final)
    k = cv.waitKey(20) & 0xFF
    if k == 27:
      break
cv.destroyAllWindows()