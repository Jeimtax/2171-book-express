from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class AddBook(FlaskForm):
    title = StringField('Book Title',validators=[DataRequired(), Length(max=120)])
    author = StringField('Book Author',validators=[DataRequired(), Length(max=120)])
    price =StringField('Price',validators=[DataRequired(), Length(max=120)])
    condition = StringField('Condition',validators=[DataRequired(), Length(max=120)])
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
    book_id = StringField('Book ID (optional)', validators=[Optional(), Length(max=20)])
    title = StringField('Book Title',validators=[DataRequired(), Length(max=120)])
    author = StringField('Book Author',validators=[DataRequired(), Length(max=120)])
    quantity = IntegerField('Quantity',validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Create Order')


