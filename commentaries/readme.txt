This works by using beautiful soup to navigate files from aquinas.cc. The commentary content can be found in the third div of class "cl"; each unit of commentary is located in a "vl-r" section; there are two pieces of commentary, each in a "vl-c" section, which can be set to any of a range of languages in aquinas.cc; I am setting the second one to English. Here is the map to content:

    div(class="cl")[2]
        vl-r <- as many of these as commentary sections in the file
            vl-c[1] <- there are only 2 of these per commentary section, and the second will contain English

Each vl-r has an id with format "v[\d]+". This id will be unique for each piece of commentary, and goes in ascending order.

Each vl-c has a class with format "c2-2 t-[ueogqxu]". The last letter determines what kind of commentary section it is. Here is the key to what each one means:

    't-e': chapter
    't-o': chapterTitle
    't-g': lecture
    't-q': lectureTitle
    't-x': bibleVerse
    't-u': commentaryText

The data is prepared first by going into a json file with the following architecture:
    chapters list(list):
        commentaryItems list(dict):
            id: str
            class: str
            content: str

The finished whole book prepared data is organized into a json file with the following architecture:

    chapters list(dict):
        chapterNum: int
        supplementalChapter: bool
        chapterTitle: str
        lectures: list(dict):
            lectureNum: int
            lectureTitle: str
            bibleVerses: list(dict)
                verseText: str
                correspondingCommentaryParagraphNum: int (Only in some commentaries, will be -1 otherwise)
            commentary: list(dict)
                commentaryParagraphNum: int (Only for some paragraphs, will be -1 otherwise)
                commentaryContent: list(str)

Website structure:

    romans/
        styles.css
        romansIndex.html
        chapter1/
            chapterIndex.html
            lecture#.html
        chapter2/
            chapterIndex.html
            lecture#.html