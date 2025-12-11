from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, FileField
from wtforms.validators import DataRequired, Email

class TicketForm(FlaskForm):
    scheme_name = StringField('Scheme Name', validators=[DataRequired()])
    unit_no = StringField('Unit Number', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('Finance', 'Finance'),
        ('Maintenance', 'Maintenance'),
        ('Information', 'Information'),
        ('General', 'General')
    ], validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    contact_number = StringField('Contact Number', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    attachment = FileField('Attachment (optional)')
    submit = SubmitField('Submit Ticket')
