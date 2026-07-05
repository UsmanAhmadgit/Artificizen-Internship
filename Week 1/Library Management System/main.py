import json
import os

# 1. CUSTOM EXCEPTIONS
class BookNotFoundError(Exception): pass
class MemberNotFoundError(Exception): pass
class NoCopiesAvailableError(Exception): pass
class DuplicateBorrowError(Exception): pass
class InvalidReturnError(Exception): pass
class DuplicateMemberError(Exception): pass

# 2. DATA MODELS (OOP)
class Book:
    def __init__(self, title, author, isbn, copies_available):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.copies_available = copies_available

    # Convert object to dictionary for JSON saving
    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "copies_available": self.copies_available
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def __str__(self):
        return f"'{self.title}' by {self.author} (ISBN: {self.isbn}) - Copies: {self.copies_available}"


class Member:
    def __init__(self, name, member_id, borrowed_books=None):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = borrowed_books if borrowed_books is not None else []

    def to_dict(self):
        return {
            "name": self.name,
            "member_id": self.member_id,
            "borrowed_books": self.borrowed_books
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


# 3. CONTROLLER (The Library System)
class Library:
    def __init__(self, filepath="library_data.json"):
        self.filepath = filepath
        self.books = {}    
        self.members = {}  
        self.__load_data() 

    def __load_data(self):
        """Private method to load JSON data into objects."""
        if not os.path.exists(self.filepath):
            return

        with open(self.filepath, 'r') as file:
            try:
                data = json.load(file)
                self.books = {isbn: Book.from_dict(b_data) for isbn, b_data in data.get("books", {}).items()}
                self.members = {m_id: Member.from_dict(m_data) for m_id, m_data in data.get("members", {}).items()}
            except json.JSONDecodeError:
                pass 

    def __save_data(self):
        """Private method to save all objects back to JSON."""
        with open(self.filepath, 'w') as file:
            data = {
                "books": {isbn: book.to_dict() for isbn, book in self.books.items()},
                "members": {m_id: member.to_dict() for m_id, member in self.members.items()}
            }
            json.dump(data, file, indent=4)

    # --- Core Features ---
    
    def add_book(self, title, author, isbn, copies):
        if isbn in self.books:
            self.books[isbn].copies_available += copies
        else:
            self.books[isbn] = Book(title, author, isbn, copies)
        self.__save_data()
        print(f"[+] Book added: {title} ({copies} copies)")

    def add_member(self, name, member_id):
        if member_id in self.members:
            raise DuplicateMemberError(f"Registration Failed: Member ID '{member_id}' is already taken.")
            
        self.members[member_id] = Member(name, member_id)
        self.__save_data()
        print(f"[+] Member registered: {name}")

    def search_book(self, query):
        results = [str(book) for book in self.books.values() if query.lower() in book.title.lower()]
        if results:
            print("\n--- Search Results ---")
            for res in results:
                print(res)
        else:
            print(f"[-] No books found matching '{query}'.")

    def issue_book(self, member_id, isbn):
        if member_id not in self.members:
            raise MemberNotFoundError(f"Member ID {member_id} not found.")
        if isbn not in self.books:
            raise BookNotFoundError(f"Book ISBN {isbn} not found.")
            
        member = self.members[member_id]
        book = self.books[isbn]

        if book.copies_available <= 0:
            raise NoCopiesAvailableError(f"No copies of '{book.title}' are currently available.")
        if isbn in member.borrowed_books:
            raise DuplicateBorrowError(f"Member '{member.name}' is already borrowing '{book.title}'.")

        book.copies_available -= 1
        member.borrowed_books.append(isbn)
        self.__save_data()
        print(f"[SUCCESS] '{book.title}' issued to {member.name}.")

    def return_book(self, member_id, isbn):
        if member_id not in self.members:
            raise MemberNotFoundError(f"Member ID {member_id} not found.")
        if isbn not in self.books:
            raise BookNotFoundError(f"Book ISBN {isbn} not found.")

        member = self.members[member_id]
        book = self.books[isbn]

        if isbn not in member.borrowed_books:
            raise InvalidReturnError(f"Member '{member.name}' does not have a copy of '{book.title}'.")

        book.copies_available += 1
        member.borrowed_books.remove(isbn)
        self.__save_data()
        print(f"[SUCCESS] '{book.title}' returned by {member.name}.")


# 4. EXECUTION MENU
if __name__ == "__main__":
    lib = Library()
    print("Initializing Library System... Data loaded.")

    while True:
        print("\n")
        print("  LIBRARY MANAGEMENT SYSTEM  ")
        print("1. Search for a Book")
        print("2. Issue a Book")
        print("3. Return a Book")
        print("4. Add a New Book to Inventory")
        print("5. Register a New Member")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")

        try:
            if choice == '1':
                query = input("Enter book title or keyword: ")
                lib.search_book(query)
                
            elif choice == '2':
                member_id = input("Enter Member ID: ")
                isbn = input("Enter Book ISBN: ")
                lib.issue_book(member_id, isbn)
                
            elif choice == '3':
                member_id = input("Enter Member ID: ")
                isbn = input("Enter Book ISBN: ")
                lib.return_book(member_id, isbn)
                
            elif choice == '4':
                title = input("Enter Book Title: ")
                author = input("Enter Author Name: ")
                isbn = input("Enter ISBN: ")
                copies = int(input("Enter number of copies: ")) 
                lib.add_book(title, author, isbn, copies)
                
            elif choice == '5':
                name = input("Enter Member Name: ")
                member_id = input("Enter New Member ID (e.g., M-01): ")
                lib.add_member(name, member_id)
                
            elif choice == '6':
                print("\nSaving data... Shutting down system. Goodbye!")
                break 
                
            else:
                print("\n[-] Invalid choice. Please enter a number between 1 and 6.")
                
        except ValueError:
            print("\n[INPUT ERROR] Please enter valid numbers where required.")
        except Exception as e:
            print(f"\n[SYSTEM ALERT] {e}")