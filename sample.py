from icrawler.builtin import GoogleImageCrawler
import random
import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

j = 0
collageWidth = 0
collageHeight = 0
filters = dict(type='clipart')
wordList = []
riddleSyllables = []
possibleWords = []
listOfImages = []
possibleWordsSplit = []

def create_collage(width, height, listofimages):
    cols = len(listofimages)
    rows = 1
    thumbnail_width = width//cols
    thumbnail_height = height//rows
    size = thumbnail_width, thumbnail_height
    new_im = Image.new('RGB', (width, height))

    pixels = new_im.load()

    for y in range(new_im.size[1]):
        for x in range(new_im.size[0]):
            pixels[x, y] = (255, 255, 255)

    ims = []
    for p in listofimages:
        im = Image.open(p)
        im.thumbnail(size)
        ims.append(im)
    i = 0
    x = 0
    y = 0
    for col in range(cols):
        for row in range(rows):
            print(i, x, y)
            new_im.paste(ims[i], (x, y))
            i += 1
            y += thumbnail_height
        x += thumbnail_width
        y = 0

    new_im.save("Collage.jpg")


def imageHandler():
    global collageHeight, collageWidth
    for i in range(1, len(possibleWords) + 1):
        print(i)

        try:
            img = Image.open(f'C:/Users/Александр/PycharmProjects/pythonProject/SillyGen/images/00000{i}.jpg')
        except:
            img = Image.open(f'C:/Users/Александр/PycharmProjects/pythonProject/SillyGen/images/00000{i}.png')

        width, height = img.size
        collageWidth += width
        collageHeight += height
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('arial.ttf', 60)
        draw.text((10,10), len(possibleWordsSplit[i - 1][0]) * "' ", (0, 0, 0), font=font)
        draw.text((width - 10, height - 10), len(possibleWordsSplit[i - 1][2]) * "' ", (0, 0, 0), anchor='rs', font=font)

        try:
            img.save(f'C:/Users/Александр/PycharmProjects/pythonProject/SillyGen/images/00000{i}Red.jpg')
            listOfImages.append(f'C:/Users/Александр/PycharmProjects/pythonProject/SillyGen/images/00000{i}Red.jpg')
            os.remove(f'C:/Users/Александр/PycharmProjects/pythonProject/SillyGen/images/00000{i}.jpg')
        except:
            img.save(f'C:/Users/Александр/PycharmProjects/pythonProject/SillyGen/images/00000{i}Red.png')
            listOfImages.append(f'C:/Users/Александр/PycharmProjects/pythonProject/SillyGen/images/00000{i}Red.png')
            os.remove(f'C:/Users/Александр/PycharmProjects/pythonProject/SillyGen/images/00000{i}.png')

def searchQuery(name):
    googleCrawler = GoogleImageCrawler(storage={f'root_dir' : 'C:/Users/Александр/PycharmProjects/pythonProject/SillyGen/images'})
    googleCrawler.crawl(keyword=name, max_num=1, file_idx_offset='auto', filters=filters)
    return

def start():
    for s in range(len(possibleWords)):
        searchQuery(possibleWords[s])

with open('wordList.txt', 'r', encoding='UTF-8') as file:
    for line in file:
        wordList.append(line.rstrip())

for i in range(len(wordList)):
    buff = wordList[i].split('	')
    wordList[i] = buff[1]

riddle = random.choice(wordList)
print(riddle)

while j < len(riddle):
    if j + 3 < len(riddle):
        riddleSyllables.append(riddle[j:j+3])
    else:
        riddleSyllables.append(riddle[j:len(riddle)])
    j += 3

print(riddleSyllables)

for k in riddleSyllables:
    for h in wordList:
        if (k in h) and (h != riddle) and (h not in possibleWords):
            buffer = h.split(k)
            possibleWords.append(h)
            possibleWordsSplit.append([buffer[0], k, buffer[1]])
            break

print(possibleWords)
print(possibleWordsSplit)

start()

imageHandler()
create_collage(collageWidth, collageHeight, listOfImages)
