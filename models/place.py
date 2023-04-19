#!/usr/bin/python3
"""This is the place class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    __tablename__ = 'places'
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0)
    number_bathrooms = Column(Integer, default=0)
    max_guest = Column(Integer, default=0)
    price_by_night = Column(Integer, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship("Review", cascade="all, delete-orphan", backref="place")
        amenities = relationship("Amenity", secondary="place_amenity", viewonly=False)

    if os.getenv('HBNB_TYPE_STORAGE') == 'file':
        @property
        def reviews(self):
            return [review for review in models.storage.all(Review).values() if review.place_id == self.id]

        @property
        def amenities(self):
            return [amenity for amenity in models.storage.all(Amenity).values() if amenity.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
