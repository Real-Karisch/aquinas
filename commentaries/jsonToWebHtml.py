from airium import Airium
import os
import re
from variables import bookNameShortToFormalAquinas, bookNameShortToFormalCatena

def generateBookHtml(bookJson, bookNameShort):
    if bookNameShort in bookNameShortToFormalCatena.keys():
        bookNameFormal = bookNameShortToFormalCatena[bookNameShort]
    elif bookNameShort in bookNameShortToFormalAquinas.keys():
        bookNameFormal = bookNameShortToFormalAquinas[bookNameShort]
    bookHtmlBuilder = Airium()
    with bookHtmlBuilder.head():
        bookHtmlBuilder.title(_t=f"Aquinas Commentary: {bookNameFormal}")
        bookHtmlBuilder.link(href="./../styles.css", rel="stylesheet")
        bookHtmlBuilder('<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />')

    with bookHtmlBuilder.div(id='mainwrap'):
        with bookHtmlBuilder.div(style="text-align: center"):
            bookHtmlBuilder.h1(_t=f"Aquinas Commentary: {bookNameFormal}, Contents")
            bookHtmlBuilder.a(href='./../../index.html', _t=f"Main Home Page", style="text-decoration: underline")
            bookHtmlBuilder(' | ')
            bookHtmlBuilder.a(href='./../aquinasCommentaryIndex.html', _t=f"Aquinas Commentary Home Page", style="text-decoration: underline")
            bookHtmlBuilder.br()
            #for chapterNum in range(1, len(bookJson) + 1):
            for chapterJson in bookJson:
                chapterNum = chapterJson['chapterNum']
                supplementalStr = 'sup' if chapterJson['supplementalChapter'] else ''
                bookHtmlBuilder.br()
                bookHtmlBuilder.a(href=f"./chapter{chapterNum}{supplementalStr}/chapterIndex.html", style="text-decoration: underline", _t=f"Chapter {chapterNum}{' Supplement' if chapterJson['supplementalChapter'] else ''} - {chapterJson['chapterTitle']}")

    return bookHtmlBuilder

def generateChapterHtml(chapterJson, bookNameShort):
    if bookNameShort in bookNameShortToFormalCatena.keys():
        bookNameFormal = bookNameShortToFormalCatena[bookNameShort]
    elif bookNameShort in bookNameShortToFormalAquinas.keys():
        bookNameFormal = bookNameShortToFormalAquinas[bookNameShort]
    
    chapterHtmlBuilder = Airium()
    with chapterHtmlBuilder.head():
        chapterHtmlBuilder.title(_t=f"Aquinas Commentary: {bookNameFormal} Chapter {chapterJson['chapterNum']}{' Supplement' if chapterJson['supplementalChapter'] else ''}")
        chapterHtmlBuilder.link(href="./../../styles.css", rel="stylesheet")
        chapterHtmlBuilder('<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />')

    with chapterHtmlBuilder.div(id='mainwrap'):
        with chapterHtmlBuilder.div(style="text-align: center"):
            chapterHtmlBuilder.h1(_t=f"Aquinas Commentary: {bookNameFormal} Chapter {chapterJson['chapterNum']}{' Supplement' if chapterJson['supplementalChapter'] else ''}")
            chapterHtmlBuilder.h2(_t=chapterJson['chapterTitle'])
            chapterHtmlBuilder.a(href='./../../../index.html', _t=f"Main Home Page", style="text-decoration: underline")
            chapterHtmlBuilder(' | ')
            chapterHtmlBuilder.a(href='./../../aquinasCommentaryIndex.html', _t=f"Aquinas Commentary Home Page", style="text-decoration: underline")
            chapterHtmlBuilder(' | ')
            chapterHtmlBuilder.a(href=f'./../{bookNameShort}Index.html', _t=f"{bookNameFormal} Contents", style="text-decoration: underline")
            chapterHtmlBuilder.br()
            

        for lectureJson in chapterJson['lectures']:
            chapterHtmlBuilder.br()  
            chapterHtmlBuilder.a(
                    href=f"lecture{lectureJson['lectureNum']}.html",
                    _t='<br>'.join([x['verseText'] for x in lectureJson['bibleVerses']])
                )   
    return chapterHtmlBuilder

def generateLectureFixedVerseHtml(lectureJson, bookNameShort, chapterNum, supplementalChapter):
    if bookNameShort in bookNameShortToFormalCatena.keys():
        bookNameFormal = bookNameShortToFormalCatena[bookNameShort]
    elif bookNameShort in bookNameShortToFormalAquinas.keys():
        bookNameFormal = bookNameShortToFormalAquinas[bookNameShort]
    supplementalLongStr = ' Supplement' if supplementalChapter else ''
    lectureHtmlBuilder = Airium()
    with lectureHtmlBuilder.head():
        lectureHtmlBuilder.title(_t=f"Aquinas Commentary: {bookNameFormal} Chapter {chapterNum}{supplementalLongStr}, Lecture {lectureJson['lectureNum']}")
        lectureHtmlBuilder.link(href="./../../styles.css", rel="stylesheet")
        lectureHtmlBuilder('<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />')

    with lectureHtmlBuilder.div(id='mainwrap'):
        with lectureHtmlBuilder.div(id='fixedVerse'):
            with lectureHtmlBuilder.div(style='text-align: center'):
                lectureHtmlBuilder.h1(_t=f"Aquinas Commentary: {bookNameFormal} Chapter {chapterNum}, Lecture {lectureJson['lectureNum']}")#, style="text-align: center")
                lectureHtmlBuilder.a(href='./../../../index.html', _t=f"Main Home Page", style="text-decoration: underline")
                lectureHtmlBuilder(' | ')
                lectureHtmlBuilder.a(href='./../../aquinasCommentaryIndex.html', _t=f"Aquinas Commentary Home Page", style="text-decoration: underline")
                lectureHtmlBuilder(' | ')
                lectureHtmlBuilder.a(href=f'./../{bookNameShort}Index.html', _t=f"{bookNameFormal} Contents", style="text-decoration: underline")
                lectureHtmlBuilder(' | ')
                lectureHtmlBuilder.a(href=f'./chapterIndex.html', _t=f"{bookNameFormal} Chapter {chapterNum}{supplementalLongStr}", style="text-decoration: underline")
            lectureHtmlBuilder.br()
            lectureHtmlBuilder.br()

            #with lectureHtmlBuilder.details():
            #    lectureHtmlBuilder.summary(_t=f"Expand")
            with lectureHtmlBuilder.b():
                versesThatOverflow = 0
                for bibleVerse in lectureJson['bibleVerses']:
                    if bibleVerse['correspondingCommentaryParagraphNum'] != -1:
                        lectureHtmlBuilder.a(href=f"#paragraph{bibleVerse['correspondingCommentaryParagraphNum']}", _t=f"{bibleVerse['verseText']} <i>({bibleVerse['correspondingCommentaryParagraphNum']})</i>")
                    else:
                        lectureHtmlBuilder(bibleVerse['verseText'])
                    #if len(bibleVerse['verseText']) > 130:
                    versesThatOverflow += int(len(bibleVerse['verseText']) / 130) #number of times the verse wraps around
                    lectureHtmlBuilder.br()

            lectureHtmlBuilder.br()

        with lectureHtmlBuilder.div(style=f"margin-top: {105 + (23 * (len(lectureJson['bibleVerses']) + versesThatOverflow))}px"):
            lectureHtmlBuilder.br()
            for commentaryJson in lectureJson['commentary']:
                lectureHtmlBuilder.br()
                cleanedCommentary = re.sub('bsc>', 'b>', commentaryJson['commentaryContent'])
                if commentaryJson['commentaryParagraphNum'] != -1:
                    lectureHtmlBuilder.br()
                    lectureHtmlBuilder.span(klass="anchor", id=f"paragraph{commentaryJson['commentaryParagraphNum']}")
                    lectureHtmlBuilder(f"<b>{commentaryJson['commentaryParagraphNum']}.</b> {cleanedCommentary}")
                else:
                    lectureHtmlBuilder(cleanedCommentary)
                lectureHtmlBuilder.br()

    return lectureHtmlBuilder

def generateLectureExpandVerseHtml(lectureJson, bookNameShort, chapterNum, supplementalChapter):
    if bookNameShort in bookNameShortToFormalCatena.keys():
        bookNameFormal = bookNameShortToFormalCatena[bookNameShort]
    elif bookNameShort in bookNameShortToFormalAquinas.keys():
        bookNameFormal = bookNameShortToFormalAquinas[bookNameShort]
    supplementalLongStr = ' Supplement' if supplementalChapter else ''
    lectureHtmlBuilder = Airium()
    with lectureHtmlBuilder.head():
        lectureHtmlBuilder.title(_t=f"Aquinas Commentary: {bookNameFormal} Chapter {chapterNum}{supplementalLongStr}, Lecture {lectureJson['lectureNum']}")
        lectureHtmlBuilder.link(href="./../../styles.css", rel="stylesheet")
        lectureHtmlBuilder('<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />')

    with lectureHtmlBuilder.div(id='mainwrap'):
        with lectureHtmlBuilder.div(id='fixedVerse'):
            with lectureHtmlBuilder.div(style='text-align: center'):
                lectureHtmlBuilder.h1(_t=f"Aquinas Commentary: {bookNameFormal} Chapter {chapterNum}, Lecture {lectureJson['lectureNum']}")#, style="text-align: center")
                lectureHtmlBuilder.a(href='./../../../index.html', _t=f"Main Home Page", style="text-decoration: underline")
                lectureHtmlBuilder(' | ')
                lectureHtmlBuilder.a(href='./../../aquinasCommentaryIndex.html', _t=f"Aquinas Commentary Home Page", style="text-decoration: underline")
                lectureHtmlBuilder(' | ')
                lectureHtmlBuilder.a(href=f'./../{bookNameShort}Index.html', _t=f"{bookNameFormal} Contents", style="text-decoration: underline")
                lectureHtmlBuilder(' | ')
                lectureHtmlBuilder.a(href=f'./chapterIndex.html', _t=f"{bookNameFormal} Chapter {chapterNum}{supplementalLongStr}", style="text-decoration: underline")
            lectureHtmlBuilder.br()
            lectureHtmlBuilder.br()

            with lectureHtmlBuilder.details():
                lectureHtmlBuilder.summary(_t=f"Scripture")
                with lectureHtmlBuilder.b():
                    versesThatOverflow = 0
                    for bibleVerse in lectureJson['bibleVerses']:
                        if bibleVerse['correspondingCommentaryParagraphNum'] != -1:
                            lectureHtmlBuilder.a(href=f"#paragraph{bibleVerse['correspondingCommentaryParagraphNum']}", _t=f"{bibleVerse['verseText']} <i>({bibleVerse['correspondingCommentaryParagraphNum']})</i>")
                        else:
                            lectureHtmlBuilder(bibleVerse['verseText'])
                        if len(bibleVerse['verseText']) > 130:
                            versesThatOverflow += 1
                        lectureHtmlBuilder.br()

                lectureHtmlBuilder.br()

        #with lectureHtmlBuilder.div(style=f"margin-top: {100 + (20 * (len(lectureJson['bibleVerses']) + versesThatOverflow))}px"):
        with lectureHtmlBuilder.div(style="margin-top: 150px"):
            lectureHtmlBuilder.br()
            for commentaryJson in lectureJson['commentary']:
                lectureHtmlBuilder.br()
                if commentaryJson['commentaryParagraphNum'] != -1:
                    lectureHtmlBuilder.br()
                    lectureHtmlBuilder.span(klass="anchor", id=f"paragraph{commentaryJson['commentaryParagraphNum']}")
                    lectureHtmlBuilder(f"<b>{commentaryJson['commentaryParagraphNum']}.</b> {commentaryJson['commentaryContent']}")
                else:
                    lectureHtmlBuilder(commentaryJson['commentaryContent'])
                lectureHtmlBuilder.br()

    return lectureHtmlBuilder

def generateLectureScrollVerseHtml(lectureJson, bookNameShort, chapterNum, supplementalChapter):
    if bookNameShort in bookNameShortToFormalCatena.keys():
        bookNameFormal = bookNameShortToFormalCatena[bookNameShort]
    elif bookNameShort in bookNameShortToFormalAquinas.keys():
        bookNameFormal = bookNameShortToFormalAquinas[bookNameShort]
    supplementalLongStr = ' Supplement' if supplementalChapter else ''
    lectureHtmlBuilder = Airium()
    with lectureHtmlBuilder.head():
        lectureHtmlBuilder.title(_t=f"Aquinas Commentary: {bookNameFormal} Chapter {chapterNum}{supplementalLongStr}, Lecture {lectureJson['lectureNum']}")
        lectureHtmlBuilder.link(href="./../../styles.css", rel="stylesheet")
        lectureHtmlBuilder('<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />')

    with lectureHtmlBuilder.div(id='mainwrap'):
        with lectureHtmlBuilder.div(style='text-align: center'):
            lectureHtmlBuilder.h1(_t=f"Aquinas Commentary: {bookNameFormal} Chapter {chapterNum}, Lecture {lectureJson['lectureNum']}")#, style="text-align: center")
            lectureHtmlBuilder.a(href='./../../../index.html', _t=f"Main Home Page", style="text-decoration: underline")
            lectureHtmlBuilder(' | ')
            lectureHtmlBuilder.a(href='./../../aquinasCommentaryIndex.html', _t=f"Aquinas Commentary Home Page", style="text-decoration: underline")
            lectureHtmlBuilder(' | ')
            lectureHtmlBuilder.a(href=f'./../{bookNameShort}Index.html', _t=f"{bookNameFormal} Contents", style="text-decoration: underline")
            lectureHtmlBuilder(' | ')
            lectureHtmlBuilder.a(href=f'./chapterIndex.html', _t=f"{bookNameFormal} Chapter {chapterNum}{supplementalLongStr}", style="text-decoration: underline")
        lectureHtmlBuilder.br()
        lectureHtmlBuilder.br()

        with lectureHtmlBuilder.b():
            versesThatOverflow = 0
            for bibleVerse in lectureJson['bibleVerses']:
                if bibleVerse['correspondingCommentaryParagraphNum'] != -1:
                    lectureHtmlBuilder.a(href=f"#paragraph{bibleVerse['correspondingCommentaryParagraphNum']}", _t=f"{bibleVerse['verseText']} <i>({bibleVerse['correspondingCommentaryParagraphNum']})</i>")
                else:
                    lectureHtmlBuilder(bibleVerse['verseText'])
                if len(bibleVerse['verseText']) > 130:
                    versesThatOverflow += 1
                lectureHtmlBuilder.br()

        for commentaryJson in lectureJson['commentary']:
            lectureHtmlBuilder.br()
            if commentaryJson['commentaryParagraphNum'] != -1:
                lectureHtmlBuilder.br()
                lectureHtmlBuilder.span(klass="anchor", id=f"paragraph{commentaryJson['commentaryParagraphNum']}")
                lectureHtmlBuilder(f"<b>{commentaryJson['commentaryParagraphNum']}.</b> {commentaryJson['commentaryContent']}")
            else:
                lectureHtmlBuilder(commentaryJson['commentaryContent'])
            lectureHtmlBuilder.br()

    return lectureHtmlBuilder

def generateWebsite(
        bookJson, 
        bookNameShort, 
        siteFolder, 
        lectureFormat='fixed' #must be 'fixed', 'scroll', or 'expand'
    ):
    filenames = os.listdir(siteFolder)
    for chapterJson in bookJson:
        chapterNum = chapterJson['chapterNum']
        supplementStr = 'sup' if chapterJson['supplementalChapter'] else ''
        if f"chapter{chapterNum}{supplementStr}" not in filenames:
            os.mkdir(f"{siteFolder}/chapter{chapterNum}{supplementStr}/")

    bookHtml = generateBookHtml(bookJson, bookNameShort)
    with open(f"{siteFolder}/{bookNameShort}Index.html", 'wb') as file:
        file.write(bytes(bookHtml))

    for chapterJson in bookJson:
        supplementStr = 'sup' if chapterJson['supplementalChapter'] else ''
        chapterHtml = generateChapterHtml(chapterJson, bookNameShort)
        with open(f"{siteFolder}/chapter{chapterJson['chapterNum']}{supplementStr}/chapterIndex.html", 'wb') as file:
            file.write(bytes(chapterHtml))
        
        for lectureJson in chapterJson['lectures']:
            if lectureFormat == 'fixed':
                if len(lectureJson['bibleVerses']) >= 18:
                    lectureHtml = generateLectureExpandVerseHtml(lectureJson, bookNameShort, chapterJson['chapterNum'], chapterJson['supplementalChapter'])
                else:
                    lectureHtml = generateLectureFixedVerseHtml(lectureJson, bookNameShort, chapterJson['chapterNum'], chapterJson['supplementalChapter'])
            elif lectureFormat == 'expand':
                lectureHtml = generateLectureExpandVerseHtml(lectureJson, bookNameShort, chapterJson['chapterNum'], chapterJson['supplementalChapter'])
            elif lectureFormat == 'scroll':
                lectureHtml = generateLectureScrollVerseHtml(lectureJson, bookNameShort, chapterJson['chapterNum'], chapterJson['supplementalChapter'])
            else:
                print("lectureFormat must be one of 'fixed', 'expand', or 'scroll'.")
            with open(f"{siteFolder}/chapter{chapterJson['chapterNum']}{supplementStr}/lecture{lectureJson['lectureNum']}.html", 'wb') as file:
                file.write(bytes(lectureHtml))

if __name__ == '__main__':
    from sourceHtmlToJson import generateCombinedCommentaryItems, generateBookJson

    for lectureFormat in ['scroll', 'expand', 'fixed']:
        print(f"Running commentary, outputting in {lectureFormat} format.")

        for bookNameShort in bookNameShortToFormalAquinas.keys():
            print(bookNameShort)
            psalmsFlag = bookNameShort == 'psalms'
            combinedCommentaryItems = generateCombinedCommentaryItems(f'C:/Users/jackk/Projects/aquinas/commentaries/sourceHtml/{bookNameShort}/', psalmsFlag)
            bookJson = generateBookJson(combinedCommentaryItems)
            generateWebsite(bookJson, bookNameShort, f'C:/Users/jackk/Projects/website/aquinasCommentary{lectureFormat.capitalize()}/{bookNameShort}/', lectureFormat=lectureFormat)
