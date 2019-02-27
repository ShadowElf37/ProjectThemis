def uheb(s):
    return '\u202B'+s+'\u202C'

def ranger(s):
    if '-' in s:
        num = s.split('-')
        return range(int(num[0]), int(num[1]) + 1)
    else:
        return [int(s)]

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, title):
        self.books.append(Anthology(title))


class Anthology:
    def __init__(self, name):
        self.name = name
        self.english = name
        self.books = []
        self.commentaries = []

    def get_length(self):
        return len(self.books)
    def get_book(self, bnum):
        return self.books[bnum-1]

    def add_book(self, name_e, name_h):
        self.books.append(Book(name_e, name_h, self))


class Book:
    def __init__(self, name_e, name_h, anthology):
        self.english = name_e
        self.hebrew = name_h
        self.anthology = anthology
        self.chapters = []
        self.portions = []

    def get_chapter(self, cnum):
        return self.chapters[cnum-1]
    def get_portion(self, pnum):
        return self.portions[pnum-1]
    def get_length(self):
        return len(self.chapters)

    def define_portion(self, name_h, name_e, chap1, verse1, chap2, verse2):
        p = []
        for c in range(chap1, chap2+1):
            print(c, chap1, chap2)
            for v in (range(verse1, verse2+1) if chap1 == chap2 else range(1, self.get_chapter(c).get_length()+1) if c != chap1 and c != chap2 else range(1, verse2+1) if c == chap2 else range(verse1, self.get_chapter(c).get_length()+1)):
                p.append(self.get_chapter(c).get_verse(v))
        pp = Portion(name_h, name_e, p, self.get_chapter(chap1).book)
        for verse in pp.verses:
            verse.portion = pp
        self.portions.append(pp)

    def add_chapter(self, num=-1):
        if num == -1:
            num = len(self.chapters)+1
        self.chapters.append(Chapter(num, self))
        self.chapters.sort(key=lambda c: c.number)


class Portion:
    def __init__(self, name_h, name_e, verses, book):
        self.hebrew = name_h
        self.english = name_e
        self.verses = verses
        self.book = book

        self.commentaries = []

    def get_verse(self, num):
        return self.verses[num-1]

    def add_commentary(self, title, text):
        n = Commentary(title, self, len(self.book.anthology.commentaries), text)
        self.book.anthology.commentaries.append(n)
        self.commentaries.append(n)


class Chapter:
    def __init__(self, n, book=None):
        self.number = n
        self.verses = []
        self.book = book if book else None

        self.commentaries = []

    def get_verse(self, vnum):
        return self.verses[vnum-1]

    def get_length(self):
        return len(self.verses)

    def add_verse(self, en, he, num=-1):
        if num == -1:
            num = len(self.verses)
        self.verses.append(Verse(num, en, he, self))
        self.verses.sort(key=lambda v: v.number)

    def add_commentary(self, title, text):
        n = Commentary(title, self, len(self.book.anthology.commentaries), text)
        self.book.anthology.commentaries.append(n)
        self.commentaries.append(n)

    def status(self):
        if not self.verses:
            return 'Empty'
        elif all([v.hebrew == 'HE EMPTY' for v in self.verses]):
            return 'Unwritten'
        elif all([v.english == 'EN EMPTY' for v in self.verses]):
            return 'Untranslated'
        elif any([v.hebrew == 'HE EMPTY' for v in self.verses]):
            return 'Partly written'
        elif any([v.english == 'EN EMPTY' for v in self.verses]):
            return 'Partly untranslated'
        return 'Complete'


class Verse:
    def __init__(self, n, text_e, text_h, chapter=None):
        self.number = n
        self.english = text_e
        self.hebrew = text_h
        self.chapter = chapter
        self.portion = None
        self.alternate_trans = []

        self.notes = []
        self.commentaries = []

    def get_english(self):
        return self.english
    def get_hebrew(self):
        return self.hebrew

    def translate(self, english):
        self.english = english

    def comment(self, text, ref=None):
        n = Note(text, self, len(self.chapter.book.anthology.commentaries), ref)
        self.chapter.book.anthology.commentaries.append(n)
        self.commentaries.append(n)

    def annotate(self, text, ref=None):
        n = Note(text, self, len(self.chapter.book.anthology.commentaries), ref)
        self.chapter.book.anthology.commentaries.append(n)
        self.notes.append(n)


class Note:
    def __init__(self, text, attached, idn, ref=None):
        self.id = idn
        self.attached = attached
        self.text = text
        self.reference = ref


class Commentary:
    def __init__(self, title, attached, idn, text, author='Yovel Key-Cohen'):
        self.id = idn
        self.attached = attached
        self.title = title
        self.text = text
        self.author = author