import re
from datetime import datetime
from flask import flash

from flask_wtf import Form
from wtforms import (
    BooleanField,
    DateTimeField,
    SelectField,
    SelectMultipleField,
    StringField,
)
from wtforms.validators import URL, DataRequired

from enums import Genres, States
from models.models import Venue


def validate_phone(phone):
    # regex for phone number validation
    phone_regex = re.compile(r"^\(?([0-9]{3})\)?[-.●]?([0-9]{3})[-.●]?([0-9]{4})$")

    return phone_regex.match(phone)


# check if venue and anddress already exists in the database
def validate_new_venue(form, field):
    if venue := Venue.query.filter_by(name=form.name.data).first():
        if venue.address == form.address.data:
            return True


class ShowForm(Form):
    artist_id = StringField("artist_id")
    venue_id = StringField("venue_id")
    start_time = DateTimeField(
        "start_time", validators=[DataRequired()], default=datetime.now()
    )


class VenueForm(Form):
    name = StringField("name", validators=[DataRequired()])
    city = StringField("city", validators=[DataRequired()])
    state = SelectField(
        "state", validators=[DataRequired()], choices=States.choices(), coerce=str
    )
    address = StringField("address", validators=[DataRequired()])
    phone = StringField("phone")
    image_link = StringField("image_link")
    genres = SelectMultipleField(
        "genres", validators=[DataRequired()], choices=Genres.choices(), coerce=str
    )
    facebook_link = StringField("facebook_link", validators=[URL()])
    website_link = StringField("website_link")

    seeking_talent = BooleanField("seeking_talent")

    seeking_description = StringField("seeking_description")

    def validate(self):
        if not super().validate():
            return False

        if not validate_phone(self.phone.data):
            self.phone.errors.append("Invalid phone number")
            return False

        if validate_new_venue(self, self.name):
            flash("Venue already exists")
            self.name.errors.append("Venue already exists")
            return False

        if self.state.data not in dict(States.choices()).keys():
            flash("Invalid state")
            self.state.errors.append("Invalid state")
            return False

        for genre in self.genres.data:
            if genre not in dict(Genres.choices()).keys():
                flash("Invalid genre")
                self.genres.errors.append("Invalid genre")

        return True


class ArtistForm(Form):

    name = StringField("name", validators=[DataRequired()])
    city = StringField("city", validators=[DataRequired()])
    state = SelectField(
        "state", validators=[DataRequired()], choices=States.choices(), coerce=str
    )
    phone = StringField(
        "phone",
        validators=[DataRequired()],
    )
    image_link = StringField("image_link")
    genres = SelectMultipleField(
        "genres", validators=[DataRequired()], choices=Genres.choices(), coerce=str
    )
    facebook_link = StringField(
        "facebook_link",
        validators=[URL()],
    )

    website_link = StringField("website_link")

    seeking_venue = BooleanField("seeking_venue")

    seeking_description = StringField("seeking_description")

    def validate(self):
        if not super().validate():
            return False

        if not validate_phone(self.phone.data):
            flash("Invalid phone number")
            self.phone.errors.append("Invalid phone number")
            return False

        if self.state.data not in dict(States.choices()).keys():
            flash("Invalid state")
            self.state.errors.append("Invalid state")
            return False

        for genre in self.genres.data:
            if genre not in dict(Genres.choices()).keys():
                flash("Invalid genre")
                self.genres.errors.append("Invalid genre")
                return False

        return True
