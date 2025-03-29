import os
import re
from bs4 import BeautifulSoup

from variables import classCodeToTypeName, classCodeToTypeNamePsalms, patterns, replacements

printNumbers = False

def getCommentaryItemsOfType(commentaryItems, itemType):
    return [x for x in commentaryItems if x['class'] == itemType]

def generateCombinedCommentaryItems(htmlFolder, psalmsFlag=False):
    chapterFolderNames = os.listdir(htmlFolder)
    chapterNums = [int(re.search('chapter(\d+)', x).group(1)) for x in chapterFolderNames]
    chapterNums.sort()

    combinedCommentaryItems = []
    for chapterNum in chapterNums:
        chapterFolder = f"{htmlFolder}/chapter{chapterNum}/"
        filenames = os.listdir(chapterFolder)
        filenameFirstPart = re.search('([a-z\d._-]+)\d+\.html', filenames[0]).group(1)
        for fileNum in range(1, len(filenames) + 1):
            filename = f"{filenameFirstPart}{fileNum}.html"
            #print(filename)
            with open(f"{chapterFolder}/{filename}", 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file.read(), 'html.parser')
            contentDiv = soup.findAll('div', {'class': 'cl'})[2]
            commentarySections = contentDiv.findAll('vl-r')
            for commentarySection in commentarySections:
                id = commentarySection.get('id')
                classTypeName = classCodeToTypeNamePsalms[commentarySection.findAll('vl-c')[1].get('class')[1]] if psalmsFlag else classCodeToTypeName[commentarySection.findAll('vl-c')[1].get('class')[1]]
                if id not in list([x['id'] for x in combinedCommentaryItems]):
                    combinedCommentaryItems.append(
                        {
                            'id': id,
                            'class': classTypeName,
                            'content': ''.join([str(x) for x in commentarySection.findAll('vl-c')[1].contents])
                        }
                    )
    return combinedCommentaryItems

def calculateCommentaryItemTypeIndices(combinedCommentaryItems, itemType):
    commentaryIndex = 0
    chapterIndices = []
    for commentaryItem in combinedCommentaryItems:
        if commentaryItem['class'] == itemType:
            chapterIndices.append(commentaryIndex)
        commentaryIndex += 1
    return chapterIndices

def splitCommentaryItemsByType(commentaryItems, itemType):
    typeIndices = calculateCommentaryItemTypeIndices(commentaryItems, itemType)
    if typeIndices == []:
        return [commentaryItems]
    typeIndices.append(len(commentaryItems) + 1)
    splitCommentaryItems = []
    for i in range(len(typeIndices) - 1):
        typeItems = commentaryItems[typeIndices[i]:typeIndices[i+1]]
        splitCommentaryItems.append(typeItems)
    return splitCommentaryItems

def generateBookJson(combinedCommentaryItems):
    bookJson = []
    commentaryItemsByChapter = splitCommentaryItemsByType(combinedCommentaryItems, 'chapter')
    for chapterCommentaryItems in commentaryItemsByChapter:
        bookJson.append(
            generateChapterJson(chapterCommentaryItems)
        )
    return bookJson

def generateChapterJson(chapterCommentaryItems):
    chapterNum = int(re.search('(Chapter|Psalm) (\d+)', chapterCommentaryItems[0]['content']).group(2))
    if printNumbers:
        print(f"Chapter {chapterNum}")
    supplementalChapter = re.search('—Supplement', chapterCommentaryItems[0]['content']) is not None
    chapterTitle = chapterCommentaryItems[1]['content']
    commentaryItemsByLecture = splitCommentaryItemsByType(chapterCommentaryItems, 'lecture')
    lectures = []
    for lectureCommentaryItems in commentaryItemsByLecture:
        lectures.append(
            generateLectureJson(lectureCommentaryItems)
        )
    return {
        'chapterNum': chapterNum,
        'supplementalChapter': supplementalChapter,
        'chapterTitle': chapterTitle,
        'lectures': lectures
    }


def generateLectureJson(lectureCommentaryItems):
    lectureSearch = re.search('Lecture (\d+)', lectureCommentaryItems[0]['content'])
    lectureNum = int(lectureSearch.group(1)) if lectureSearch else 1
    if printNumbers:
        print(lectureNum)
    lectureTitle = lectureCommentaryItems[1]['content']

    bibleVerseItems = getCommentaryItemsOfType(lectureCommentaryItems, 'bibleVerse')
    bibleVerses = generateBibleVerseJson(bibleVerseItems)

    commentaryTextItems = getCommentaryItemsOfType(lectureCommentaryItems, 'commentaryText')
    commentary = generateCommentaryJson(commentaryTextItems)

    return {
        'lectureNum': lectureNum,
        'lectureTitle': lectureTitle,
        'bibleVerses': bibleVerses,
        'commentary': commentary
    }

def generateBibleVerseJson(bibleVerseItems):
    bibleVerseJson = []
    for bibleVerseItem in bibleVerseItems:
        activeVerseStr = bibleVerseItem['content'].strip()
        while activeVerseStr != '':
            search = re.search(patterns['bibleVerseWithParagraphNum'], activeVerseStr)
            if search is None:
                bibleVerseJson.append(
                    {
                        'verseText': activeVerseStr,
                        'correspondingCommentaryParagraphNum': -1
                    }
                )
                activeVerseStr = ''
            else:
                bibleVerseJson.append(
                    {
                        'verseText': search.group(1).strip(),
                        'correspondingCommentaryParagraphNum': int(search.group(2))
                    }
                )
                activeVerseStr = search.group(3).strip()
    return bibleVerseJson

def generateCommentaryJson(commentaryTextItems):
    commentaryJson = []
    for commentaryTextItem in commentaryTextItems:
        includesParagraphNum = re.search(patterns['commentaryWithParagraphNum'], commentaryTextItem['content'])
        if not includesParagraphNum:
            commentaryStr = commentaryTextItem['content'].strip()
            for pat, repl in replacements.items():
                commentaryStr = re.sub(pat, repl, commentaryStr)
            commentaryJson.append(
                {
                    'commentaryParagraphNum': -1,
                    'commentaryContent': commentaryStr
                }
            )
        else:
            search = re.search(patterns['commentaryWithParagraphNum'], commentaryTextItem['content'])
            commentaryJson.append(
                {
                    'commentaryParagraphNum': int(search.group(1)),
                    'commentaryContent': search.group(2).strip()
                }
            )

    return commentaryJson

if __name__ == '__main__':
    combinedCommentaryItems = generateCombinedCommentaryItems('C:/Users/jackk/Projects/aquinas/commentaries/sourceHtml/isaiah/')
    generateBookJson(combinedCommentaryItems)