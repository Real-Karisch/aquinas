from copy import deepcopy
import re

template = [
    '                        <vl-r id="v[insertNumber]">',
    '                           <vl-c class="c1-2 t-u" id="c1_[insertNumber]" data-id="0"></vl-c>',
    '                           <vl-c class="c2-2 t-u" id="c2_[insertNumber]" data-id="0"><b>[insertCommentatorName]</b>[insertCommentary]</vl-c>',
    '                        </vl-r>'
]

def generateHtmlSegment(
    lineNumber,
    commentatorName,
    commentary
):
    newTemplate = deepcopy(template)
    newTemplate[0] = re.sub('\[insertNumber\]', str(lineNumber), newTemplate[0])
    newTemplate[1] = re.sub('\[insertNumber\]', str(lineNumber), newTemplate[1])
    newTemplate[2] = re.sub('\[insertNumber\]', str(lineNumber), newTemplate[2])
    newTemplate[2] = re.sub('\[insertCommentatorName\]', commentatorName, newTemplate[2])
    newTemplate[2] = re.sub('\[insertCommentary\]', commentary, newTemplate[2])
    return newTemplate

def extractCommentatorName(string):
    search = re.search('(^[^:]+):', string)
    if search:
        commentatorName = search.group(1)
        if len(commentatorName) < 60:
            return commentatorName
    return ''

def extractCommentary(string):
    search = re.search('^[^:]+:(.+)$', string)
    if search:
        return search.group(1)
    else:
        return string
    
def generateAllSampleLines(textFileAddress, startingNumber):
    with open(textFileAddress, 'r') as file:
        lines = file.readlines()

    allSampleLines = []
    lineNumber = startingNumber
    
    for line in lines:
        #print(line)
        nonDuplicated = line[:int(len(line)/2)]
        commentatorName = extractCommentatorName(nonDuplicated)
        commentary = extractCommentary(nonDuplicated)

        htmlSegment = generateHtmlSegment(lineNumber, commentatorName, commentary)
        allSampleLines.extend(htmlSegment)

        lineNumber += 1

    return allSampleLines

if __name__ == '__main__':
    import os
    os.system('cls')

    allSampleLines = generateAllSampleLines('test.txt', 311)

    print(
        '\n'.join(allSampleLines)
    )