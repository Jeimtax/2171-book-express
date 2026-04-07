from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class ManageOrderForm(FlaskForm):
    class Meta:
        csrf = False

    supplier_name = StringField(
        'Supplier Name',
        validators=[DataRequired(), Length(max=120)]
    )
    supplier_phone = StringField(
        'Supplier Phone',
        validators=[DataRequired(), Length(max=30)]
    )
    supplier_address = TextAreaField(
        'Supplier Address',
        validators=[DataRequired(), Length(max=255)]
    )
    items = TextAreaField(
        'Items Ordered',
        validators=[DataRequired(), Length(max=1000)]
    )
    submit = SubmitField('Create Order')
