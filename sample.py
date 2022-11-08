from icrawler.builtin import GoogleImageCrawler
import random
import telebot
from telebot import types
import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

token = 'xxxxx'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def startMessage(message):
    bot.send_message(message.chat.id, 'Бот Генератор-ребусов! \n Начать угадывать: /riddle')

@bot.message_handler(commands=['riddle'])
def riddleSender(message):
    global riddle

    main()
    start()
    imageHandler()
    create_collage(collageWidth, collageHeight, listOfImages)
    bot.send_photo(message.chat.id, photo=open('Collage.jpg', 'rb'))
    bot.send_message(message.chat.id, 'Теперь попробуй угадать, что загадано на картинке: ')
    bot.send_message(message.chat.id, 'Если совсем застрял, напиши "ответ"!')

    @bot.message_handler(content_types=['text'])
    def check(message):
        while True:
            answer = message.text

            if answer == riddle:
                bot.send_message(message.chat.id, 'Молодец! Ты угадал!')
                riddleSender(message)

            elif answer.lower() == 'ответ':
                bot.send_message(message.chat.id, f'Ответ - {riddle} \nЕсли хотите попробовать еще раз, напишите repeat!')

            elif message.text == 'repeat':
                riddleSender(message)

            else:
                bot.send_message(message.chat.id, f'Ты не угадал. Ответ был: {riddle}. \nПопробуй снова.')
                continue

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
    global collageWidth, collageHeight, listOfImages, heights
    for i in range(1, len(possibleWords) + 1):
        print(i)

        try:
            img = Image.open(f'C:/Users/Александр/PycharmProjects/pythonProject/SillyGen/images/00000{i}.jpg')
        except:
            img = Image.open(f'C:/Users/Александр/PycharmProjects/pythonProject/SillyGen/images/00000{i}.png')

        width, height = img.size
        heights.append(height)

        collageWidth += width
        collageHeight = max(heights)

        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('arial.ttf', 60)
        draw.text((10,10), len(possibleWordsSplit[i - 1][0]) * "' ", (0, 0, 0), font=font)
        draw.text((width - 10, height - 10), len(possibleWordsSplit[i - 1][2]) * "' ", (0, 0, 0), anchor='rs', font=font)

        try:
            img.save(f'images/00000{i}Red.jpg')
            listOfImages.append(f'images/00000{i}Red.jpg')
            os.remove(f'images/00000{i}.jpg')
        except:
            img.save(f'00000{i}Red.png')
            listOfImages.append(f'00000{i}Red.png')
            os.remove(f'00000{i}.png')

def searchQuery(name):
    googleCrawler = GoogleImageCrawler(storage={f'root_dir' : 'images'})
    googleCrawler.crawl(keyword=name, max_num=1, file_idx_offset='auto', filters=filters, min_size=(200, 200), max_size=(1000, 1000))
    return

def start():
    global possibleWords
    for s in range(len(possibleWords)):
        searchQuery(possibleWords[s])

def main():
    global j, wordList, riddleSyllables, possibleWords, possibleWordsSplit, riddle, listOfImages, filters, collageWidth, collageHeight, heights

    j = 0
    collageWidth = 0
    collageHeight = 0
    filters = dict(type='clipart')
    heights = []
    wordList = []
    riddleSyllables = []
    possibleWords = []
    listOfImages = []
    possibleWordsSplit = []

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

    if len(possibleWords) != len(riddleSyllables):
        main()

    print(possibleWords)
    print(possibleWordsSplit)

bot.infinity_polling()
