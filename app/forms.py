from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField, TextAreaField, PasswordField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from app.models.book import Book

class AddBook(FlaskForm):
    title = StringField('Book Title',validators=[DataRequired(), Length(max=120)])
    author = StringField('Book Author',validators=[DataRequired(), Length(max=120)])
    price = FloatField('Price', validators=[DataRequired()])
    grade = StringField('Grade',validators=[DataRequired(), Length(max=120)])
    subject = StringField('Subject',validators=[DataRequired(), Length(max=120)])
    quantity = IntegerField('Quantity',validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Save Book")

class ManageOrderForm(FlaskForm):
    class Meta:
        csrf = False

    supplier_name = StringField('Supplier Name', validators=[DataRequired(), Length(max=120)])
    supplier_phone = StringField('Supplier Phone',validators=[DataRequired(), Length(max=30)])
    supplier_address = TextAreaField('Supplier Address',validators=[DataRequired(), Length(max=255)])
    book_id = SelectField('Book',coerce=int,validators=[DataRequired()])
    title = StringField('Book Title (Optional) ',validators=[Length(max=120)])
    author = StringField('Book Author (Optional)',validators=[Length(max=120)])
    quantity = IntegerField('Quantity',validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Create Order')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        books = Book.query.order_by(Book.title.asc()).all()
        self.book_id.choices = [(0, '-- Select Book --')] + [
            (book.id, f'{book.title} by {book.author}')
            for book in books
        ]

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=80)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    role = SelectField('Role', choices=[('staff', 'Staff'), ('manager', 'Manager')], default='staff', validators=[DataRequired()])
    submit = SubmitField('Register')
