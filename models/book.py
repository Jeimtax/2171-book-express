from category import Category

class Book:
    def __init__(self, title: str, author: str, isbn: int):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.categories: list[Category] = []
    
    def add_category(self, category: Category):
        if any(c.name == category.name for c in self.categories):
            raise ValueError(f"{category.name} is already assigned to this book")
        self.categories.append(category)
    
    def __str__(self):
        return f"{self.title}, {self.author}, {self.categories}"



