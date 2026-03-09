from category import Category

class Book:
    def __init__(self, title: str, author: str, isbn: int):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.categories: list[Category] = []
    
    def add_category(self, category: Category):
        if any(c.grade_level == category.grade_level and c.subject == category.subject for c in self.categories):
            raise ValueError(f"{category} is already assigned to this book")
        self.categories.append(category)
    
    def remove_category(self, category):
        self.categories = [c for c in self.categories if str(c) != str(category)]
    
    def __str__(self):
        return f"{self.title}, {self.author}, {self.categories}"



