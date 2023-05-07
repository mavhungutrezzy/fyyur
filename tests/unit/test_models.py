import unittest

from flask import Flask

from app import create_app
from database import db
from models.models import Artist, Show, Venue


class FyyurTestCase(unittest.TestCase):
    """This test case will test the models and functionality of the Fyyur app"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client

    def tearDown(self):
        """Enusre that the database is empty after each test"""
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()

    def test_venue_model(self):
        """
        GIVEN a Venue model
        WHEN a new Venue is created with the name, city, state, phone, address, genres
        THEN check the name, city, state, genres, and seeking_talent fields are defined correctly
        """
        venue = Venue(
            name="Boiler Room",
            city="Chicago",
            state="IL",
            phone="312-555-1212",
            address="1234 N. State St.",
            image_link="https://www.google.com",
            facebook_link="https://www.google.com",
            website_link="https://www.google.com",
            genres="Pop",
            seeking_talent=True,
            seeking_description="We are on the lookout for a local artist to play every two weeks. Please call us.",
        )

        self.assertEqual(venue.name, "Boiler Room")
        self.assertEqual(venue.city, "Chicago")
        self.assertEqual(venue.state, "IL")
        self.assertEqual(venue.genres, "Pop")
        self.assertTrue(venue.seeking_talent)

    def test_artist_model(self):
        """
        GIVEN a Artist model
        WHEN a new Artist is created with the name, city, state, phone, genres
        THEN check the name, city, state, genres, and seeking_venue fields are defined correctly
        """
        artist = Artist(
            name="Guns N Petals",
            city="San Francisco",
            state="CA",
            phone="326-123-5000",
            genres="Pop",
            image_link="https://www.google.com",
            facebook_link="https://www.google.com",
            website_link="https://www.google.com",
            seeking_venue=True,
            seeking_description="Looking for shows to perform at in the San Francisco Bay Area!",
        )

        self.assertEqual(artist.name, "Guns N Petals")
        self.assertEqual(artist.city, "San Francisco")
        self.assertEqual(artist.state, "CA")
        self.assertEqual(artist.genres, "Pop")
        self.assertTrue(artist.seeking_venue)

    def test_show_model(self):
        """
        GIVEN a Show model
        WHEN a new Show is created with the venue_id, artist_id, start_time
        THEN check the venue_id, artist_id, and start_time fields are defined correctly
        """
        show = Show(
            venue_id=1,
            artist_id=1,
            start_time="2019-05-21T21:30:00.000Z",
        )

        self.assertEqual(show.venue_id, 1)
        self.assertEqual(show.artist_id, 1)
        self.assertEqual(show.start_time, "2019-05-21T21:30:00.000Z")

    def test_home_page(self):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/' page is requested (GET)
        THEN check the response is valid
        """
        self._base("/", b"Fyyur")

    def test_venues_page(self):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/venues' page is requested (GET)
        THEN check the response is valid
        """
        self._base("/venues", b"Boiler Room")

    def test_artist_page(self):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/artists' page is requested (GET)
        THEN check the response is valid
        """
        self._base("/artists", b"Themba")

    def test_show_page(self):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/shows' page is requested (GET)
        THEN check the response is valid
        """
        self._base("/shows", b"Boiler Room")

    def _base(self, arg0, arg1):
        response = self.client().get(arg0)
        self.assertEqual(response.status_code, 200)
        self.assertIn(arg1, response.data)
