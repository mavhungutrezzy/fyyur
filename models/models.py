from database import db

# *----------------------------------------------------------------------------#
# * Models
# *----------------------------------------------------------------------------#


class Venue(db.Model):

    __tablename__ = "Venue"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship("Show", backref="venue", lazy=True)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def update(
        cls,
        id,
        name,
        city,
        state,
        address,
        phone,
        genres,
        image_link,
        facebook_link,
        website_link,
        seeking_talent,
        seeking_description,
    ):
        venue = Venue.query.get_or_404(id)
        venue.name = name
        venue.city = city
        venue.state = state
        venue.address = address
        venue.phone = phone
        venue.genres = genres
        venue.image_link = image_link
        venue.facebook_link = facebook_link
        venue.website_link = website_link
        venue.seeking_talent = seeking_talent
        venue.seeking_description = seeking_description
        venue.add()

    def __repr__(self):
        return f"{self.name}"

    def __str__(self):
        return f"{self.name}"


class Artist(db.Model):

    __tablename__ = "Artist"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship("Show", backref="artist", lazy=True)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def update(
        cls,
        id,
        name,
        city,
        state,
        phone,
        genres,
        image_link,
        facebook_link,
        website_link,
        seeking_venue,
        seeking_description,
    ):
        artist = Artist.query.get_or_404(id)
        artist.name = name
        artist.city = city
        artist.state = state
        artist.phone = phone
        artist.genres = genres
        artist.image_link = image_link
        artist.facebook_link = facebook_link
        artist.website_link = website_link
        artist.seeking_venue = seeking_venue
        artist.seeking_description = seeking_description
        artist.add()

    def __repr__(self):
        return f"{self.name}"

    def __str__(self):
        return f"{self.name}"


class Show(db.Model):

    __tablename__ = "Shows"

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("Artist.id"), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.update(self)
        db.session.commit()

    def __repr__(self):
        return f"{self.artist_id} {self.venue_id} {self.start_time}"

    def __str__(self):
        return f"{self.artist_id} {self.venue_id} {self.start_time}"
