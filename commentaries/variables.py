classCodeToTypeName = {
    't-e': 'chapter',
    't-o': 'chapterTitle',
    't-g': 'lecture',
    't-q': 'lectureTitle',
    't-x': 'bibleVerse',
    't-u': 'commentaryText',
    't-t': 'subSection'
}

classCodeToTypeNamePsalms = {
    't-g': 'chapter',
    't-q': 'chapterTitle',
    't-x': 'bibleVerse',
    't-u': 'commentaryText',
    't-t': 'subSection',
}

patterns = {
    'bibleVerseWithParagraphNum': '^([^[]+)\[n\. (\d+)\](.*)',
    'commentaryWithParagraphNum': '^<b>(\d+)</b>\.(.*)',
    'catenaAurea': '<bsc>(.+)</bsc>',
}

replacements = {
    '<bsc>': '<b>',
    '</bsc>': '</b>',
}

bookNameShortToFormalAquinas = {
    'psalms': 'Psalms',
    'job': 'Job',
    'jeremiah': 'Jeremiah',
    'lamentations': 'Lamentations',
    'isaiah': 'Isaiah',
    
    'matthew1': 'Matthew Part 1',
    'matthew2': 'Matthew Part 2',
    'john1': 'John Part 1',
    'john2': 'John Part 2',
    'romans': 'Romans',
    'corinthians1': 'First Corinthians',
    'corinthians2': 'Second Corinthians',
    'galatians': 'Galatians',
    'ephesians': 'Ephesians',
    'philippians': 'Philippians',
    'colossians': 'Colossians',
    'thessalonians1': 'First Thessalonians',
    'thessalonians2': 'Second Thessalonians',
    'timothy1': 'First Timothy',
    'timothy2': 'Second Timothy',
    'titus': 'Titus',
    'philemon': 'Philemon',
    'hebrews': 'Hebrews',
}
bookNameShortToFormalCatena = {
    'mark': 'Mark',
    'luke': 'Luke',
    'matthew': 'Matthew',
    'john': 'John',
}
bookNameFormalToShortEpistles = {value: key for key, value in bookNameShortToFormalAquinas.items()}
bookNameFormalToShortGospels = {value: key for key, value in bookNameShortToFormalCatena.items()}