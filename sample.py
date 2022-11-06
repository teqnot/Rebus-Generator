from icrawler.builtin import GoogleImageCrawler
import random
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

collection = 'C:/Users/технопарк/Desktop/progprog/PYTHON_PROJECTS/SillyGen/images'
j = 0
wordList = []
riddleSyllables = []
possibleWords = []
possibleWordsSplit = []
possibleRedacted = []

def imageHandler():
    for i in range(1, len(possibleWords) + 1):
        img = Image.open(f'C:/Users/технопарк/Desktop/progprog/PYTHON_PROJECTS/SillyGen/images/00000{i}.jpg')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('arial.ttf', 60)
        draw.text((0,0), len(possibleWordsSplit[0]) * "' ", (0, 0, 0), font=font)
        img.save(f'C:/Users/технопарк/Desktop/progprog/PYTHON_PROJECTS/SillyGen/images/00000{i}.jpg')

def searchQuery(name):
    googleCrawler = GoogleImageCrawler(storage={f'root_dir' : 'C:/Users/технопарк/Desktop/progprog/PYTHON_PROJECTS/SillyGen/images'})
    googleCrawler.crawl(keyword=name, max_num=1, file_idx_offset='auto')
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
            possibleRedacted.append(len(buffer[0]) * " ' " + k + len(buffer[1]) * " ' ")
            break

print(possibleWords)

start()

imageHandler()
