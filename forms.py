from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional

# -------------------------
# Product Form
# -------------------------
class ProductForm(FlaskForm):
    id = IntegerField('Product ID', validators=[Optional()])
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Save')

# -------------------------
# Location Form
# -------------------------
class LocationForm(FlaskForm):
    id = IntegerField('Location ID', validators=[Optional()])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Save')

# -------------------------
# Movement Form
# -------------------------
class MovementForm(FlaskForm):
    product_id = SelectField('Product', coerce=int, validators=[DataRequired()])
    from_location = SelectField('From Location', coerce=str, validators=[Optional()])
    to_location = SelectField('To Location', coerce=str, validators=[Optional()])
    qty = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Save')
