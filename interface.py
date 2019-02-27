import pickle
from data import *
from time import sleep

def uheb(s):
    return '\u202B'+s+'\u202C'

def ranger(s):
    if '-' in s:
        num = s.split('-')
        return range(int(num[0]), int(num[1]) + 1)
    else:
        return [int(s)]

def general_cmd(cmd):
    global library
    if cmd == 'reload':
        library = pickle.load(open('tanakh.dat', 'rb'))
    elif cmd == 'py':
        p = input('py> ')
        try:
            print(eval(p))
        except SyntaxError:
            exec(p)
            print('Done.')

    else:
        print('That wasn\'t a valid command.')

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, title):
        self.books.append(Anthology(title))

try:
    library = pickle.load(open('tanakh.dat', 'rb'))
except EOFError:
    library = Library()

location = 'library'
current_object = library
just_entered = False

print('Welcome to the Library of Judaic Artifacts.')
while True:
    if location == 'library':
        print('\nAvailable books:')
        for i,book in enumerate(current_object.books):
            print('\t%s - %s' % (i+1, book.name))
        print('Available commands:\n\t1 - Create book\n\t2 - Open book\n\t3 - Preview book\n\t4 - Delete book\n\tW - Save current library\n\tQ - Quit')

        just_entered = False
        cmd = input('> ').lower()
        if cmd == '1':
            current_object.add_book(input('Enter a title for the book:\n> '))
        elif cmd == '2':
            new = int(input('Enter a book number to open:\n> '))
            current_object = current_object.books[new-1]
            location = 'anthology'
            just_entered = True
        elif cmd == '3':
            anthology = library.books[-1+int(input('Enter a book number to preview it:\n> '))]
            print('Volumes:')
            for vol in anthology.books:
                print('   ', vol.name_e+', %s chapters' % len(vol.chapters))
            print('There are %s commentaries available for this book.' % len(anthology.commentaries))
        elif cmd == '4':
            current_object.books.remove(current_object.books[-1+int(
                input('Enter a book number to remove it from the library:\n> '))])
            print('Operation complete.')
        elif cmd == 'w':
            pickle.dump(library, open('tanakh.dat', 'wb'))
            print('Operation complete.')
        elif cmd == 'q':
            break
        else:
            general_cmd(cmd)

    elif location == 'anthology':
        print('\nBook:', current_object.name)
        print('Volumes:')
        for i,vol in enumerate(current_object.books):
            print('\t\u202D%s - %s (%s), %s chapters' % (i+1, uheb(vol.hebrew), vol.english, len(vol.chapters)))
        print('There are %s notes and commentaries for this book.' % len(current_object.commentaries))
        print('\nAvailable commands:\n\t0 - Collect by address\n\t1 - Create volume\n\t2 - Open volume\n\t3 - Delete volume\n\tW - Save library\n\tB - Back to library\n\tQ - Quit')

        just_entered = False
        cmd = input('> ').lower()
        if cmd == '0':
            addr = input('Enter an address in the form BOOK1 C1:V1-V2, C2:V1-V2; BOOK2 C1:V1-V2\n> ')  # e.g.   Genesis 1   Genesis 1:14   Genesis 1:14-16   Genesis 1:14-16; Exodus 2:5
            # Genesis 1:14-16; Exodus 2:5
            collection = []
            addrs = addr.split(';')
            for book in addrs:
                book = book.strip()
                bname = book[:book.find(' ')]
                chapters = book[book.find(' ')+1:].split(',')
                for chapter in chapters:
                    chap, verses = chapter.strip().split(':')
                    collection += [book.get_chapter(int(chap)).get_verse(i) for i in ranger(verses) for book in current_object.books if book.english == bname]
            for verse in collection:
                print(str(verse.chapter.number)+':'+str(verse.number), verse.english+'\n'+verse.hebrew)
        elif cmd == '1':
            current_object.add_book(input('Enter an English title for the volume:\n> '), input('Enter a Hebrew title for the volume:\n> '))
        elif cmd == '2':
            new = int(input('Enter a volume number to open:\n> '))
            current_object = current_object.get_book(new)
            location = 'book'
            just_entered = True
        elif cmd == '3':
            anthology = current_object.get_book(int(input('Enter a volume number to remove it:\n> ')))
            current_object.books.remove(anthology-1)
            print('Operation complete.')
        elif cmd == 'w':
            pickle.dump(library, open('tanakh.dat', 'wb'))
            print('Operation complete.')
        elif cmd == 'b':
            location = 'library'
            current_object = library
            just_entered = True
        elif cmd == 'q':
            break
        else:
            general_cmd(cmd)

    elif location == 'book':
        print('\nBook:', current_object.anthology.name)
        print('Volume: %s (%s)'% (uheb(current_object.hebrew), current_object.english))
        print('There are %s chapters and %s portions available.' % (current_object.get_length(), len(current_object.portions)))
        print('Available commands:\n\t0 - View full chapter\
        \n\t1 - Create chapter(s)\n\t2 - Open chapter\n\t3 - Define portion\n\t4 - List portions\n\t\
5 - Open portion\n\t6 - Delete chapter\n\t7 - Delete portion\n\t8 - Get chapter statuses\n\t9 - Speed fill chapter verse counts\n\tW - Save library\n\tB - Back to Book\n\t\
Q - Quit')

        just_entered = False
        cmd = input('> ').lower()
        if cmd == '0':
            num = input('Enter chapter number to view:\n> ')
            current_object.get_chapter(int(num))
        elif cmd == '1':
            num = input('Enter number or range of numbers as X-Y for new chapters:\n> ')
            for i in ranger(num):
                current_object.add_chapter(i)
        elif cmd == '2':
            num = int(input('Enter a chapter number to open:\n> '))
            current_object = current_object.get_chapter(num)
            just_entered = True
            location = 'chapter'
        elif cmd == '3':
            current_object.define_portion(input('What is the portion\'s Hebrew name?\n> '),
                                          input('What is its English name?\n> '),
                                          int(input('What chapter does it start on?\n> ')),
                                          int(input('What verse does it start on?\n> ')),
                                          int(input('What chapter does it end on?\n> ')),
                                          int(input('What verse does it end on?\n> ')))
        elif cmd == '4':
            print('Available portions:')
            for i,portion in enumerate(current_object.portions):
                print('\u202D%s    %s (%s) - %s commentaries over %s verses' % (i+1, uheb(portion.hebrew), portion.english, len(portion.commentaries), len(portion.verses)))
        elif cmd == '5':
            current_object = current_object.portions[int(input('Enter a portion number:\n> '))-1]
            just_entered = True
            location = 'portion'
        elif cmd == '6':
            c = input('Enter a chapter number or range of numbers as X-Y to delete:\n> ')
            chaps = [current_object.chapters[chap-1] for chap in ranger(c)]
            for chap in chaps:
                current_object.chapters.remove(chap)
        elif cmd == '7':
            p = int(input('Enter a portion number to delete:\n> '))
            current_object.portions.remove(current_object.portions[p-1])
        elif cmd == '8':
            for chapter in current_object.chapters:
                print('Chapter %s - %s' % (chapter.number, chapter.status()))
        elif cmd == '9':
            print('Type q to quit.')
            for chapter in current_object.chapters:
                if not chapter.verses:
                    num = input('%s %s > ' % (current_object.english, chapter.number))
                    if num == 'q':
                        break
                    for i in ranger('1-'+num):
                        chapter.add_verse('EN EMPTY', 'HE EMPTY', i)
        elif cmd == 'w':
            pickle.dump(library, open('tanakh.dat', 'wb'))
            print('Operation complete.')
        elif cmd == 'b':
            location = 'anthology'
            current_object = current_object.anthology
            just_entered = True
        elif cmd == 'q':
            break
        else:
            general_cmd(cmd)

    elif location == 'chapter':
        if just_entered:
            print('\nBook:', current_object.book.anthology.name)
            print('There are %s commentaries available for this chapter.' % len(current_object.commentaries))
            print('\n%s %s' % (current_object.book.english, current_object.number))
            for verse in current_object.verses:
                print('%s %s  (%s notes)' % (verse.number, verse.english, len(verse.notes+verse.commentaries)))
            print()
        print(
'Available commands:\n\t0 - View verse(s)\n\t1 - Add verse\n\t2 - Open Verse\n\t3 - Add chapter commentary\n\t4 - List chapter commentaries\n\t5 - View chapter commentary\n\t\
6 - Preview verse commentaries\n\t7 - Delete chapter commentary\n\t8 - Delete verse\n\t9 - Speed fill Hebrew\n\t10 - Fill plaintext Hebrew\n\t11 - Speed fill English\n\tW - Save library\n\tB - Back to volume\n\tQ - Quit')

        just_entered = False
        cmd = input('> ').lower()
        if cmd == '0':
            nums = input('Enter a verse or range of verses as X-Y to view in more detail:\n> ')
            for verse in ranger(nums):
                v = current_object.get_verse(verse)
                print('\u202D%s:%s %s\n%s\nThere are %s comments and %s notable items for this verse.\n' % (current_object.number, verse, v.english, uheb(v.hebrew), len(v.commentaries), len(v.notes)))
        elif cmd == '1':
            num = input('Enter a verse number or range of verses as X-Y to add:\n> ')
            for i in ranger(num):
                current_object.add_verse('EN EMPTY', 'HE EMPTY', i)
            just_entered = True
        elif cmd == '2':
            num = int(input('Enter a verse number to open:\n> '))
            current_object = current_object.get_verse(num)
            just_entered = True
            location = 'verse-c'
        elif cmd == '3':
            title = input('Enter a title for this commentary:\n> ')
            author = input('Who authored this commentary? Default is Yovel.\n> ')
            if not author:
                author = 'Yovel Key-Cohen'
            text = input('Enter the text for this commentary (use \\n for newline):\n> ')
            current_object.add_commentary(title, text, author)
        elif cmd == '4':
            print('Available commentaries')
            for i,commentary in enumerate(current_object.commentaries):
                print('%s   - %s' % (i+1, commentary.title))
        elif cmd == '5':
            num = int(input('Enter a commentary number to view:\n> '))
            com = current_object.commentaries[num-1]
            print('\nCommentary: %s\nID: %s\n%s/%s for %s %s\n' % (com.title, com.id, num, len(current_object.commentaries), com.attached.book.english, com.attached.number))
            print(com.text)
        elif cmd == '6':
            for verse in current_object.verses:
                for com in verse.commentaries:
                    print('  %s, %s' % (verse.number, com.reference))
            print()
        elif cmd == '7':
            num = int(input('Enter a commentary number to delete:\n> '))
            current_object.commentaries.remove(current_object.commentaries[num-1])
        elif cmd == '8':
            num = int(input('Enter a verse number to delete:\n> '))
            current_object.verses.remove(current_object.verses[num-1])
        elif cmd == '9':
            print('Type q to quit.')
            for verse in current_object.verses:
                if verse.hebrew == 'HE EMPTY':
                    new = input('%s %s:%s > ' % (verse.chapter.book.english, verse.chapter.number, verse.number))
                    if new == 'q':
                        break
                    verse.hebrew = new
        elif cmd == '10':
            v = input('Enter a block of verses separated by : to fill the chapter:\n> ')
            for i,verse in enumerate(v.split('׃')):
                if i == len(current_object.verses):
                    break
                current_object.verses[i].hebrew = verse.strip()+'׃'
        elif cmd == '11':
            print('Type q to quit.')
            for verse in current_object.verses:
                if verse.english == 'EN EMPTY':
                    new = input('Hebrew: %s\n%s %s:%s > ' % (uheb(verse.hebrew), verse.chapter.book.english, verse.chapter.number, verse.number))
                    if new == 'q':
                        break
                    verse.english = new.strip()
        elif cmd == 'w':
            pickle.dump(library, open('tanakh.dat', 'wb'))
            print('Operation complete.')
        elif cmd == 'b':
            location = 'book'
            current_object = current_object.book
            just_entered = True
        elif cmd == 'q':
            break
        else:
            general_cmd(cmd)

    elif location == 'portion':
        print('\nBook:', current_object.book.english)
        print('Portion:', uheb(current_object.hebrew), '('+current_object.english+')')
        print('There are %s notable items in this portion' % sum([len(v.notes) for v in current_object.verses]))
        if just_entered:
            for i,verse in enumerate(current_object.verses):
                print('(%s) %s:%s    %s' % (i+1, verse.chapter.number, verse.number, verse.english) + ' (%s notables)' % (len(verse.notes)))
        print('\nAvailable commands:\n\t0 - View verse(s)\n\t1 - Open verse\n\t2 - Add portion commentary\n\t3 - List portion commentaries\n\t4 - View portion commentary\n\t5 - Delete portion commentary\n\t\
6 - Preview notable items\n\tW - Save library\n\tB - Back to book\n\tQ - Quit')

        just_entered = False
        cmd = input('> ').lower()
        if cmd == '0':
            nums = input('Enter a verse or range of verses as X-Y to view in more detail:\n> ')
            for verse in ranger(nums):
                v = current_object.verses[verse]
                print('%s:%s %s\n%s\nThere are %s comments and %s notable items for this verse.\n' % (
                current_object.number, verse, v.english, uheb(v.hebrew), len(v.commentaries), len(v.notes)))
        elif cmd == '1':
            num = int(input('Enter a verse number to open:\n> '))
            current_object = current_object.get_verse(num)
            just_entered = True
            location = 'verse-p'
        elif cmd == '2':
            title = input('Enter a title for this commentary:\n> ')
            author = input('Who authored this commentary? Default is Yovel.\n> ')
            if not author:
                author = 'Yovel Key-Cohen'
            text = input('Enter the text for this commentary (use \\n for newline):\n> ')
            current_object.add_commentary(title, text, author)
        elif cmd == '3':
            print('Available commentaries:')
            for i,commentary in enumerate(current_object.commentaries):
                print('%s   - %s' % (i+1, commentary.title))
        elif cmd == '4':
            num = int(input('Enter a commentary number to view:\n> '))
            com = current_object.commentaries[num - 1]
            print('\nCommentary: %s\nID: %s\n%s/%s for %s\n' % (
            com.title, com.id, num, len(current_object.commentaries), com.attached.english))
            print(com.text)
        elif cmd == '5':
            num = int(input('Enter a commentary number to delete:\n> '))
            current_object.commentaries.remove(current_object.commentaries[num-1])
        elif cmd == '6':
            for verse in current_object.verses:
                for com in verse.notes:
                    print('%s:%s - %s' % (verse.chapter.number, verse.number, com.reference))
        elif cmd == 'w':
            pickle.dump(library, open('tanakh.dat', 'wb'))
            print('Operation complete.')
        elif cmd == 'b':
            location = 'book'
            current_object = current_object.book
            just_entered = True
        elif cmd == 'q':
            break
        else:
            general_cmd(cmd)

    elif location == 'verse-c' or location == 'verse-p':
        print('\nBook:', current_object.chapter.book.anthology.name)
        print('There are %s notes available for this verse.' % len(current_object.commentaries+current_object.notes))
        print('\n%s %s:%s' % (current_object.chapter.book.english, current_object.chapter.number, current_object.number))
        print(current_object.hebrew)
        print(current_object.english)
        for alt in current_object.alternate_trans:
            print(alt[1], '(' + alt[0] + ')')
        print('\nNotes:')
        for note in current_object.notes:
            print('    ' + note.reference + ' - ' + note.text)
        print('Commentary:')
        for note in current_object.commentaries:
            print('    ' + note.reference + ' - ' + note.text)

        print('\nAvailable commands:\n\t1 - Edit translation\n\t2 - Add alternate translation\n\t3 - Add note\n\t4 - Add commentary\n\t5 - Edit Hebrew\n\t6 - Delete commentary\n\t\
W - Save library\n\tB - Back to '+('chapter' if location == 'verse-c' else 'portion')+'\n\tQ - Quit')

        just_entered = False
        cmd = input('> ').lower()
        if cmd == '1':
            current_object.english = input('Original translation: '+current_object.english+'\nNew translation: ')
        elif cmd == '2':
            current_object.alternate_trans.append((input('Enter translation source:\n> '), input('Enter alternate translation:\n> ')))
        elif cmd == '3':
            r = input('Enter the part of the verse being referenced:\n> ')
            current_object.annotate(input('Enter note:\n> '), ref=r)
        elif cmd == '4':
            r = input('Enter the part of the verse being referenced:\n> ')
            current_object.comment(input('Enter commentary:\n> '), ref=r)
        elif cmd == '5':
            current_object.hebrew = input('Current Hebrew:' + current_object.hebrew + '\nNew Hebrew: ')
        elif cmd == '6':
            num = int(input('Enter a number for the note or comment to be deleted:\n> '))
            try:
                current_object.notes.remove(current_object.notes[num-1])
            except IndexError:
                current_object.commentaries.remove(current_object.commentaries[num-len(current_object.notes)-1])
        elif cmd == 'w':
            pickle.dump(library, open('tanakh.dat', 'wb'))
            print('Operation complete.')
        elif cmd == 'b':
            just_entered = True
            if location == 'verse-c':
                location = 'chapter'
                current_object = current_object.chapter
            else:
                location = 'portion'
                current_object = current_object.portion
        elif cmd == 'q':
            break
        else:
            general_cmd(cmd)

    else:
        print('An error occurred in location management. Location:', location+'. Exiting...')
        break

    # sleep(0.1)

print('Farewell.')