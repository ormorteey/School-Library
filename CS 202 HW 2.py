EXIT = ('9','QUIT','quit')
COMMANDS = ('1','2','3','4','5','6','7','8')
MENU = """
        MENU
press 1 find a book
press 2 to add book
press 3 to remove book
press 4 find a patron
press 5 to add patron
press 6 to remove patron
press 7 to assign book to patron
press 8 to free patron of book
press 9 or type QUIT to exit program
"""
class Manager(object):
    def __init__(self):
        self.library = Library()
    def AcceptCommand(self):
        count = 0
        while True:
            command = str(raw_input("Enter a number: "))
            if (not command in COMMANDS) and (not command in EXIT):
                print "Oops! You got the wrong command, check above for the correct keypress"
                if count == 5:
                    print" Thank you for using our program"
                    break
                else:
                    self.AcceptCommand()
            else:
                return command
    def RunCommand(self, command):
        if command == '1':
            if self.library.books == {}:
                print 'Library contains no book'
            else:
                self.library.Find('books')
            self.AnotherOp()
        elif command == '2':
            self.library.Add('books')
            self.AnotherOp()
        elif command == '3':
            if self.library.books == {}:
                print 'Library contains no book'
            else:
                self.library.Remove('books')
            self.AnotherOp()
        elif command == '4':
            if self.library.patrons == {}:
                print 'Library contains no patron'
            else:
                self.library.Find('patrons')
            self.AnotherOp()
        elif command == '5':
            self.library.Add('patrons')
            self.AnotherOp()
        elif command == '6':
            if self.library.patrons == {}:
                print 'Library contains no patron'
            else:
                self.library.Remove('patrons')
            self.AnotherOp()
        elif command == '7':
            count = 0
            while True:
                try:
                    count +=1
                    if count == 3:
                        break
                    title = str(raw_input("Enter book title or 'cancel' to STOP: "))
                    patron = str(raw_input("Enter patron or 'cancel' to STOP: "))
                    self.library.books[title].CheckoutTo(self.library.patrons[patron])
                    break
                except (KeyError, ValueError, ReferenceError):
                    print "Oops! {} is not a book or {} is not a patron in the Library".format(title,patron)
            self.AnotherOp()
        elif command == '8':
            count = 0
            while True:
                try:
                    count +=1
                    if count == 3:
                        break
                    title = str(raw_input("Enter returned book title or 'cancel' to STOP: "))
                    self.library.books[title].Return()
                    break
                except (KeyError, ValueError, ReferenceError):
                    print "Book doesn't exist in the library"
            self.AnotherOp()        
        elif command in EXIT:
            print 'Thank you for using program'
            quit
    def AnotherOp(self):   ##runs another operation
        print MENU
        command = self.AcceptCommand()
        self.RunCommand(command)

class Library(object):

    def __init__(self):
        self.name = str(raw_input('Enter Library name: '))
        self.books = {}
        self.patrons = {}
        self.entity = None ## The kind of obeject be it patrons or books
        print 'welcome to {} Library'.format(self.name),
        print MENU

    def Add(self, entity): ## Adds either a patron or book to the collection of books
        numberOfEntity = None
        while True:
            try:
                numberOfEntity = int(raw_input(('How many {} do you want to add: ').format(entity)))
                break
            except ValueError, ReferenceError:
                print ("Oops!  {} is not a valid number.  Try again...").format(numberOfEntity)
        count = 1
        while(count <= numberOfEntity):
            if entity == 'books':
                title = str(raw_input("Enter  title: "))
                author = str(raw_input("Enter book author: "))
                self.books[title] = Book(title,author)
            else:
                PatronName = str(raw_input("Enter  Patron's name: "))
                self.patrons[PatronName] = Patron(PatronName)
            count += 1
            if count > numberOfEntity:
                check = str(raw_input(("Do you want to add more {}, Yes or No: ").format(entity)))
                if check.upper()== "YES" or check.upper()== "Y":
                    count-=1
                else:
                    break

    def Show(self, entity): ## Shows Items in an entity collection
        if entity == 'books':
            self.entity = self.books
        else:
            self.entity = self.patrons
        if self.entity ==  {}:
            print "The Library contains no {}".format(entity)
        else:
            for count in self.entity:
               print str(self.entity.__getitem__(count))

    def Remove(self, entity): ##Remove a patron or book
        count = 0
        while True:
            try:
                count +=1
                if count == 5:
                    break
                if entity == 'books':
                    bookToRemoveTitle = str(raw_input("Enter title to be removed or 'cancel' to stop: "))
                    bookToRemoveAuthor = str(raw_input("Enter author to be removed or 'cancel' to stop: "))
                    if (bookToRemoveTitle, bookToRemoveAuthor) == ("cancel", "cancel") or (bookToRemoveAuthor, bookToRemoveTitle) == ("CANCEL", "CANCEL"):
                        break
                    else:
                        if (bookToRemoveTitle,bookToRemoveAuthor) == self.books[bookToRemoveTitle].BookProperties():
                            print ("{} has been removed ").format(str(self.books[bookToRemoveTitle]))
                            self.books.__delitem__(bookToRemoveTitle) 
                        break
                if entity == 'patrons':
                    patronName = str(raw_input("Enter name or type 'cancel' to stop: "))
                    if (patronName) == ("cancel") or (patronName) == ("CANCEL"):
                        break
                    else:
                        if (patronName) == self.patrons[patronName].patronProperty():
                            print ("{} has been removed ").format(str(self.patrons[patronName]))
                            self.patrons.__delitem__(patronName) 
                        break
            except (KeyError, ValueError, ReferenceError):
                if entity == 'books':
                    print ("Oops! {} by {} is not a book in the library.  Try again...").format(bookToRemoveTitle, bookToRemoveAuthor)
                elif entity == 'patrons':
                    print ("Oops! {} is not a patron in the library.  Try again...").format(patronName)

    def Find(self,entity): ##find a patron or book
        count = 0
        while True:
            try:
                count +=1
                if count == 5:
                    break
                if entity == 'books':
                    Title = str(raw_input("Enter book title or 'cancel' to STOP: "))
                    Author = str(raw_input("Enter book Author or 'cancel' to STOP: "))
                    if (Title,Author) == self.books[Title].BookProperties():
                        print ("{} by {} is a book in the Library ").format(Title,Author)
                        self.books[Title].ShowStatus()
                        break
                    elif (Title,Author) == ('cancel', 'cancel') or (Title,Author) == ('CANCEL', 'CANCEL'):
                        break
                else:
                    patronName = str(raw_input("Enter patron's name: "))
                    if (patronName) == self.patrons[patronName].patronProperty():
                        print ("{} is a patron in the Library ").format(patronName)
                        self.patrons[patronName].ShowStatus()
                        break
            except (KeyError, ValueError, ReferenceError):
                if entity == 'books':
                    print ("Oops! {} by {} is not a book in the library.  Try again...").format(Title, Author)
                elif entity == 'patrons':
                    print ("{} is not a patron in the Library ").format(patronName)
                        
class Book(object): ## Book model

    def __init__(self,title,author):
        self.title = title
        self.author = author
        self.waitlist = list()
        self.checkedOutBy = None

    def __str__(self):
        return self.title + " by " + self.author

    def BookProperties(self):
        return( self.title, self.author)

    def ShowStatus(self):
        fullname = self.title + " (" + self.author + ")"
        print '{}'.format(fullname),
        if self.checkedOutBy == None:
            print"Not currently checked out",
        else:
            print "Checked out by", self.checkedOutBy.name,
        if len(self.waitlist) == 0:
            print "; No waiting list"
        else:
            print "; Current waiting list:",
            for p in self.waitlist:
                print p.name,
            print ""

    def CheckoutTo(self, patron):
        if self.checkedOutBy == None:
            if patron.CurrentBookCount() < 3:
                self.checkedOutBy = patron
                patron.AssignBook(self)
                print patron.name,"has checked out",self.title
            else:
                print "Patron", patron.name, "already has 3 books checked out"
        else:
            if patron.pendingBook == None:
                self.waitlist.append(patron)
                patron.pendingBook = self;
                print patron.name,"is added to the waiting list for",self.title
            else:
                print patron.name,"is already on the waiting list for",patron.pendingBook.title

    def Return(self):
        if self.checkedOutBy == None:
            print "Book has not been checked out"
        else:
            print self.checkedOutBy.name,"has returned",self.title
            self.checkedOutBy = None
            if len(self.waitlist) > 0:
                i = 0
                while self.checkedOutBy == None and i < len(self.waitlist):
                    p = self.waitlist[i]
                    print p.name, "is next in line"
                    print p.name, "has",p.CurrentBookCount(), "books checked out"
                    if p.CurrentBookCount() < 3:
                        print p.name, "gets it next"
                        self.checkedOutBy = p
                        self.waitlist.pop(i)
                        p.AssignBook(self)
                        p.pendingBook = None
                        break
                    i = i+1
            if self.checkedOutBy == None and len(self.waitlist) > 0:
                print "Nobody on the waiting list is allowed to check out",self.title


class Patron(object): ##patron model

    def __init__(self,name): 
        self.name = name
        self.books = list()
        self.pendingBook = None

    def __str__(self):
        return 'patron ' + self.name
    
    def patronProperty(self):
        return( self.name)

    def AssignBook(self, book): #assign book to a patron
        self.books.append(book)

    def CurrentBookCount(self): #count the number of books
        return len(self.books)

    def ReturnBook(self, book,title): 
        if self != book.checkedOutBy:
            print self.name,"can't return",book.title,", it is checked out by",book.checkedOutBy.name
        else:
            book.Return()
            self.books.remove(book)
            if self.pendingBook != None:
                if self.pendingBook.waitlist[0] == self:
                    print self.name,"is now eligible and next in line for",self.pendingBook.title
                    self.pendingBook.waitlist.pop(0)
                    self.AssignBook(self.pendingBook)
                    self.pendingBook.checkedOutBy = self
                    self.pendingBook = None

    def ReturnAllBooks(self): #clear patron off all books
        for book in self.books:
            book.Return()
        del self.books[:]

    def ShowStatus(self): ##show patron status
        print '{}'.format("Patron " + self.name),
        if len(self.books) == 0:
            print "No books currently checked out"
        else:
            for b in self.books:
                print "[",b.title,"]",
            print ""

def main():
    manage = Manager() ## Instantiating manager class
    command = manage.AcceptCommand() ## Accepting User input for operation
    manage.RunCommand(command) # Running user input against command 

main()
