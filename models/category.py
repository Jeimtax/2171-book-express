class Category:
    def __init__(self, grade_level: str, subject: str):
        if not grade_level.strip():
            raise ValueError("Grade level cannot be empty")
        
        if not subject.strip():
            raise ValueError("Grade level cannot be empty")
        
        self.grade_level = grade_level.strip().title()
        self.subject = subject.strip().title()

    def __str__(self):
        return f"{self.grade_level} - {self.subject}"
    
    def __repr__(self):
        """For printing list items"""
        return f"{self.grade_level} - {self.subject}"
