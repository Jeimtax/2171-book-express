class Category:
    def __init__(self, name: str, description: str=""):
        self.name = name.strip().title()
        self.description = description

    def __str__(self):
        return f"{self.name}"
    
    def __repr__(self):
        """For printing list items"""
        return f"{self.name}"
