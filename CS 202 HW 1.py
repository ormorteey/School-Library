import collections
"""

Due to new changes in Python lang, this code may need some little tweaking to be compatible with Python 3 compilers


"""
class Book:
    def __init__(self,title,author):
        self.title = title
        self.author = author
        self.waitlist = list()
        self.checkedOutBy = None
        
    def ShowStatus(self):
        fullname = self.title + " (" + self.author + ")"
        print ('{0:>50} :').format(fullname),
        if self.checkedOutBy == None:
            print ("Not currently checked out"),
        else:
            print ("Checked out by"), self.checkedOutBy.name,
        if len(self.waitlist) == 0:
            print ("; No waiting list")
        else:
            print ("; Current waiting list:"),
            for p in self.waitlist:
                print (p.name),
            print ("")

    def CheckoutTo(self, patron):
        if self.checkedOutBy == None:
            if patron.CurrentBookCount() < 3:
                self.checkedOutBy = patron
                patron.AssignBook(self)
                print (patron.name,"has checked out",self.title)
            else:
                print ("Patron", patron.name, "already has 3 books checked out")
        else:
            if patron.pendingBook == None:
                self.waitlist.append(patron)
                patron.pendingBook = self;
                print (patron.name,"is added to the waiting list for",self.title)
            else:
                print (patron.name,"is already on the waiting list for",patron.pendingBook.title)
                
    def Return(self):
        print (self.checkedOutBy.name,"has returned",self.title)
        self.checkedOutBy = None
        if len(self.waitlist) > 0:
            i = 0
            while self.checkedOutBy == None and i < len(self.waitlist):
                p = self.waitlist[i]
                print (p.name, "is next in line")
                print (p.name, "has",p.CurrentBookCount(), "books checked out")
                if p.CurrentBookCount() < 3:
                    print (p.name, "gets it next")
                    self.checkedOutBy = p
                    self.waitlist.pop(i)
                    p.AssignBook(self)
                    p.pendingBook = None
                    break
                i = i+1
        if self.checkedOutBy == None and len(self.waitlist) > 0:
            print ("Nobody on the waiting list is allowed to check out",self.title)

  
class Patron:
    def __init__(self,name):
        self.name = name
        self.books = list()
        self.pendingBook = None
        
    def AssignBook(self, book):
        self.books.append(book)

    def CurrentBookCount(self):
        return len(self.books)

    def ReturnBook(self, book):
        if self != book.checkedOutBy:
            print (self.name,"can't return",book.title,", it is checked out by",book.checkedOutBy.name)
        else:
            book.Return()
            self.books.remove(book)
            if self.pendingBook != None:
                if self.pendingBook.waitlist[0] == self:
                    print (self.name,"is now eligible and next in line for",self.pendingBook.title)
                    self.pendingBook.waitlist.pop(0)
                    self.AssignBook(self.pendingBook)
                    self.pendingBook.checkedOutBy = self
                    self.pendingBook = None
            

    def ReturnAllBooks(self):
        for book in self.books:
            book.Return()
        del self.books[:]

    def ShowStatus(self):
        print ('{0:>50} :'.format("Patron " + self.name)),
        if len(self.books) == 0:
            print ("No books currently checked out")
        else:
            for b in self.books:
                print ("[",b.title,"]"),
            print ("")

def ShowLibrary():
    for i, b in enumerate(library):
        b.ShowStatus()

    print ('{0:=<100}'.format(""))

def ShowPatrons():
    for p in patrons:
        p.ShowStatus()

    print ('{0:=<100}'.format(""))

def TestBookLimit():
    print ("TestBookLimit():")
    
    ShowLibrary()
    ShowPatrons()
    
    b1.CheckoutTo(ade)
    ShowLibrary()
    ShowPatrons()

    b2.CheckoutTo(ade)
    ShowLibrary()
    ShowPatrons()

    b3.CheckoutTo(ade)
    ShowLibrary()
    ShowPatrons()

    b4.CheckoutTo(ade)
    ShowLibrary()
    ShowPatrons()


    ade.ReturnAllBooks()
    ShowLibrary()
    ShowPatrons()

def TestWaitlist():
    print ("TestWaitList():")
    
    b1.CheckoutTo(tola)
    ShowLibrary()
    ShowPatrons()

    b1.CheckoutTo(ade)
    ShowLibrary()
    ShowPatrons()

    b1.CheckoutTo(ayo)
    ShowLibrary()
    ShowPatrons()

    b2.CheckoutTo(ade)
    b3.CheckoutTo(ade)
    b4.CheckoutTo(ade)
    ShowLibrary()
    ShowPatrons()

    tola.ReturnBook(b1)
    ShowLibrary()
    ShowPatrons()

    ade.ReturnBook(b1)
    ShowLibrary()
    ShowPatrons()

    ayo.ReturnBook(b1)
    ShowLibrary()
    ShowPatrons()

    ade.ReturnBook(b3)
    ShowLibrary()
    ShowPatrons()

    ade.ReturnBook(b2)
    ShowLibrary()
    ShowPatrons()

    ade.ReturnBook(b4)
    ShowLibrary()
    ShowPatrons()

    ade.ReturnBook(b1)
    ShowLibrary()
    ShowPatrons()
    
def main():
    TestBookLimit()
    TestWaitlist()
    
b1 = Book("The gods are not to blame","Rotimi, Ola")
b2 = Book("The Lion and the Jewel","Wole, Soyinka")
b3 = Book("There was a country","Chinua, Achebe")
b4 = Book("The Palmwine Drinkard","Amos, Tutuola")
library = b1, b2, b3, b4

ade = Patron("Ade")
ayo = Patron("Ayo")
tola = Patron("Tola")

patrons = ade, ayo, tola

main()
