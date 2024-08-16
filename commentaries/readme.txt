This works by using beautiful soup to navigate files from aquinas.cc. The commentary content can be found in the third div of class "cl"; each unit of commentary is located in a "vl-r" section; there are two pieces of commentary, each in a "vl-c" section, which can be set to any of a range of languages in aquinas.cc; I am setting the second one to English. Here is the map to content:

    div(class="cl")[2]
        vl-r <- as many of these as commentary sections in the file
            vl-c[1] <- there are only 2 of these per commentary section, and the second will contain English

Each vl-r has an id with format "v[\d]+". This id will be unique for each piece of commentary, and goes in ascending order.

Each vl-c has a class with format "c2-2 t-[ueogqxu]". The last letter determines what kind of commentary section it is. Here is the key to what each one means:

    't-e': Chapter break
    't-o': Chapter title
    't-g': Lecture break
    't-q': Lecture title
    't-x': Bible text
    't-u': Regular commentary

The finished commentary is organized into a json file with the following architecture:

    chapters list(dict):
        chapterNum: int
        chapterTitle: str
        lectures: list(dict):
            lectureNum: int
            lectureTitle: str
            bibleVerses: list(dict)
                verseNum: int
                verseText: str
                correspondingCommentaryParagraphNum: int (Only in some commentaries, will be -1 otherwise)
            commentary: list(dict)
                commentaryParagraphNum: int
                commentaryTexts: list(str)