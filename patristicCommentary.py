import re
from airium import Airium
import os
 
subsectionDict = {
    0: 'a',
    1: 'b',
    2: 'c',
    3: 'd',
    4: 'e',
    5: 'f',
    6: 'g',
    7: 'h',
    8: 'i',
    9: 'j',
    10: 'k',
    11: 'l',
    12: 'm',
    13: 'n',
    14: 'o',
    15: 'p',
    16: 'q',
    17: 'r',
    18: 's',
    19: 't',
    20: 'u',
    21: 'v'
}
 
gospelChapterCounts = {
    'Matthew': 28,
    'Mark': 16,
    'Luke': 24,
    'John': 21
}
 
def generatePatristicCommentaryLines(rawCommentaryFileAddress):
    with open(rawCommentaryFileAddress, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    lines = [re.sub("–","-", x) for x in lines if re.match('\n', x) is None]
    return lines
 
def generateChapterAndVerseSections(lines):
    sections = []
 
    for lineNum, line in zip(range(len(lines)), lines):
        if re.match('\d+:[\d-]', line):
            sections.append(
                {
                    'chapterAndVerse': line.strip(),
                    'sectionLines': []
                }
            )
        else:
            sections[-1]['sectionLines'].append(line)
 
    return sections
 
def generateSubsections(sectionLines):
    subsections = []
 
    subsectionCnt = 0
    for lineNum, line in zip(range(len(sectionLines)), sectionLines):
        if re.match('[A-Z -]+\.', line) is None: #if current line is not commentary
            if subsections != []: #if we have already started to make subsections (so we don't get index error in next check)
                if subsections[-1]['subsectionLines'] == []: #if the last subsection line is empty
                    subsections[-1]['subsectionTextLines'].append(line) #then add line to the verse lines
                else: 
                    subsections.append( 
                        {
                            'subsectionNum': subsectionDict[subsectionCnt],
                            'subsectionTextLines': [line],
                            'subsectionLines': []
                        }
                    ) #
                    subsectionCnt += 1
            else:
                subsections.append(
                    {
                        'subsectionNum': subsectionDict[subsectionCnt],
                        'subsectionTextLines': [line],
                        'subsectionLines': []
                    }
                )
                subsectionCnt += 1
        else:
            subsections[-1]['subsectionLines'].append(line)
 
    return subsections
 
def generateCommentaryHtml(commentaryLines, gospelName, verseText, chapterNum, verseNum, subverseNum=''):
    a = Airium()
    with a.head():
        a.title(_t=f"{gospelName} {chapterNum}:{verseNum}{subverseNum}")
        a.link(href="../../../styles.css", rel="stylesheet")
        a('<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />')
    a.br()
    a.br()
    with a.div(id='wrap'):
        with a.body():

            a.h1(_t=f"{gospelName} Chapter {chapterNum}")

            a.a(style="text-decoration: underline;", href=f"../../patristicCommentaryIndex.html", _t=f"Return to Patristic Commentaries")
            a.br()
            a.br()
            a.a(href="../contents.html", _t=f"Return To Gospel Of {gospelName} Contents", style="text-decoration: underline")

            a.br()
            a.br()

            a.a(href=f"chapter_{chapterNum}.html", _t=f"Return To Chapter", style="text-decoration: underline")

            a.br()
            a.br()

            a.h3(_t=f"{verseText}")
    
            for commentaryLine in commentaryLines:
                a(commentaryLine)
                a.br()
                a.br()
 
    return bytes(a)
 
def commentaryHtmlDriver(subsection, gospelName, chapterNum, verseNum):
    verseText = '<br>'.join(subsection['subsectionTextLines'])
    htmlBytes = generateCommentaryHtml(
        commentaryLines=subsection['subsectionLines'],
        gospelName=gospelName,
        verseText=verseText,
        chapterNum=chapterNum,
        verseNum=verseNum,
        subverseNum=subsection['subsectionNum']
    )
    return htmlBytes

def mainChapterHtmlDriver(sections, chapterNum, gospelName):
    htmlBuilder = Airium()
    with htmlBuilder.head():
        htmlBuilder.title(_t=f"{gospelName} Chapter {chapterNum}")
        htmlBuilder.link(href="../../../styles.css", rel="stylesheet")
        htmlBuilder('<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />')
    
    with htmlBuilder.div(id='wrap'):
        htmlBuilder.h1(_t=f"{gospelName} Chapter {chapterNum}")
    
        htmlBuilder.br()
        htmlBuilder.br()
        
        htmlBuilder.a(style="text-decoration: underline;", href=f"../../patristicCommentaryIndex.html", _t=f"Return to Patristic Commentaries")
        htmlBuilder.br()
        htmlBuilder.br()
        htmlBuilder.a(href="../contents.html", _t=f"Return To Gospel Of {gospelName} Contents", style="text-decoration: underline")
    
        htmlBuilder.br()
        htmlBuilder.br()
    
        htmlBuilder("(Click on verse for commentary)")
    
        htmlBuilder.br()
        htmlBuilder.br()

        for section in sections:
            subsections = generateSubsections(section['sectionLines'])
            chapterAndVerseSearch = re.search('(\d+):([\d–-]+)', section['chapterAndVerse'])
            chapterNum = int(chapterAndVerseSearch.group(1))
            verseNum = re.sub('–','-',chapterAndVerseSearch.group(2))
            if len(subsections) == 1:
                subsections[0]['subsectionNum'] = ''
            for subsection in subsections:
                htmlBuilder.a(href=f"commentary_{chapterNum}.{verseNum}{'.'+subsection['subsectionNum'] if subsection['subsectionNum'] != '' else ''}.html", _t='<br>'.join(subsection['subsectionTextLines']))
                htmlBuilder.br()

        htmlBuilder.br()
        htmlBuilder.br()
        if chapterNum == 1:
            htmlBuilder.a(href=f"../chapter{chapterNum + 1}/chapter_{chapterNum + 1}.html", style="text-decoration: underline", _t=f"To Chapter {chapterNum + 1} >")
        elif chapterNum == gospelChapterCounts[gospelName]:
            htmlBuilder.a(href=f"../chapter{chapterNum - 1}/chapter_{chapterNum - 1}.html", style="text-decoration: underline", _t=f"< To Chapter {chapterNum - 1}")
        else:
            htmlBuilder.a(href=f"../chapter{chapterNum - 1}/chapter_{chapterNum - 1}.html", style="text-decoration: underline", _t=f"< To Chapter {chapterNum - 1}")
            htmlBuilder(" | ")
            htmlBuilder.a(href=f"../chapter{chapterNum + 1}/chapter_{chapterNum + 1}.html", style="text-decoration: underline", _t=f"To Chapter {chapterNum + 1} >")

        htmlBuilder.br()
        htmlBuilder.br()
        htmlBuilder.br()
        htmlBuilder.br()
        htmlBuilder.br()
        htmlBuilder.br()
        htmlBuilder.br()

    return htmlBuilder

def generateAndSaveGospelContentsHtml(gospelName, destinationPatristicCommentaryFolder):
    htmlBuilder = Airium()
    with htmlBuilder.head():
        htmlBuilder.title(_t=f"Patristic Commentary | Gospel Of {gospelName}")
        htmlBuilder.link(href="../../styles.css", rel="stylesheet")

    with htmlBuilder.div(id='wrap'):
        with htmlBuilder.body(style="text-align: center;"):
            htmlBuilder.h1(_t=f"Patristic Commentary | Gospel Of {gospelName}")
            htmlBuilder.a(style="text-decoration: underline;", href=f"../patristicCommentaryIndex.html", _t=f"Return to Patristic Commentaries")
            htmlBuilder.br()
            htmlBuilder.br()
            for chapterNum in range(1, gospelChapterCounts[gospelName] + 1):
                htmlBuilder.a(style="text-decoration: underline;", href=f"chapter{chapterNum}/chapter_{chapterNum}.html", _t=f"Chapter {chapterNum}")
                htmlBuilder.br()

            htmlBuilder.br()
            htmlBuilder.br()

    with open(f"{destinationPatristicCommentaryFolder}/{gospelName.lower()}/contents.html", 'wb') as file:
        file.write(bytes(htmlBuilder))
   
 
def generateAndSaveAllChapterHtmls(folderAddress, gospelName, sections):
    chapterNum = re.match('\d+', sections[0]['chapterAndVerse']).group(0)
    for section in sections:
        subsections = generateSubsections(section['sectionLines'])
        chapterAndVerseSearch = re.search('(\d+):([\d–-]+)', section['chapterAndVerse'])
        chapterNum = chapterAndVerseSearch.group(1)
        verseNum = re.sub('–','-',chapterAndVerseSearch.group(2))
        if len(subsections) == 1:
            subsections[0]['subsectionNum'] = ''
        for subsection in subsections:
            subsectionCommentaryHtmlBytes = commentaryHtmlDriver(
                subsection=subsection,
                gospelName=gospelName,
                chapterNum=chapterNum,
                verseNum=verseNum
            )           
            with open(f"{folderAddress}/commentary_{chapterNum}.{verseNum}{'.'+subsection['subsectionNum'] if subsection['subsectionNum'] != '' else ''}.html", 'wb') as file:
                file.write(subsectionCommentaryHtmlBytes)

    mainChapterHtmlBuilder = mainChapterHtmlDriver(sections=sections, chapterNum=chapterNum, gospelName=gospelName)
 
    with open(f"{folderAddress}/chapter_{chapterNum}.html", 'wb') as file:
        file.write(bytes(mainChapterHtmlBuilder))

def driver(gospelName, rawCommentaryTxtAllGospelsFolder, destinationPatristicCommentaryFolder):
    for chapterNum in range(1, gospelChapterCounts[gospelName] + 1):
        if f'chapter{chapterNum}' not in os.listdir(f'{destinationPatristicCommentaryFolder}/{gospelName.lower()}/'):
            os.mkdir(f'{destinationPatristicCommentaryFolder}/{gospelName.lower()}/chapter{chapterNum}/')
    
        lines = generatePatristicCommentaryLines(f'{rawCommentaryTxtAllGospelsFolder}/{gospelName.lower()}/chapter{chapterNum}.txt')
        sections = generateChapterAndVerseSections(lines)
        generateAndSaveAllChapterHtmls(
            folderAddress=f'{destinationPatristicCommentaryFolder}/{gospelName.lower()}/chapter{chapterNum}/',
            gospelName=gospelName,
            sections=sections
        )
        generateAndSaveGospelContentsHtml(
            gospelName=gospelName,
            destinationPatristicCommentaryFolder=destinationPatristicCommentaryFolder
        )
 
if __name__ == '__main__':
    for gospelName in gospelChapterCounts.keys():
        driver(
            gospelName=gospelName,
            rawCommentaryTxtAllGospelsFolder='C:/Users/jackk/Projects/aquinas/patristicCommentaryTxt/',
            destinationPatristicCommentaryFolder='C:/Users/jackk/Projects/website/patristicCommentary/'
        )