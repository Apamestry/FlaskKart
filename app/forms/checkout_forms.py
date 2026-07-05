from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp


class ShippingForm(FlaskForm):
    full_name = StringField("Full Name", validators=[DataRequired(), Length(max=120)])
    address_line1 = StringField("Address Line 1", validators=[DataRequired(), Length(max=200)])
    address_line2 = StringField("Address Line 2 (optional)", validators=[Length(max=200)])
    city = StringField("City", validators=[DataRequired(), Length(max=100)])
    state = StringField("State / Province", validators=[DataRequired(), Length(max=100)])
    zip_code = StringField("ZIP / Postal Code", validators=[DataRequired(), Length(max=20)])
    phone = StringField(
        "Phone Number",
        validators=[
            DataRequired(),
            Regexp(r"^[\d\s\-\+\(\)]{7,20}$", message="Enter a valid phone number."),
        ],
    )
    submit = SubmitField("Continue to Review")