from sqlalchemy import Column, Integer, String, JSON, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    ingredients = Column(JSON)
    instructions = Column(JSON)
    
    # Common metadata fields that may be available across sources
    servings = Column(Integer, nullable=True)
    prep_time_minutes = Column(Integer, nullable=True)
    cook_time_minutes = Column(Integer, nullable=True)
    total_time_minutes = Column(Integer, nullable=True)
    
    # Source information
    source_type = Column(String)  # 'instagram', 'website', 'book'
    source_url = Column(String, nullable=True)
    
    # Optional metadata
    cuisine = Column(String, nullable=True)
    course = Column(String, nullable=True)
    calories = Column(Float, nullable=True)
    nutrition = Column(JSON, nullable=True)  # For detailed nutritional info
    
    # Media
    image_urls = Column(JSON, nullable=True)  # List of image URLs
    video_url = Column(String, nullable=True)  # For Instagram videos
    
    # Additional source-specific metadata
    source_metadata = Column(JSON, nullable=True)
    
    household_id = Column(Integer, ForeignKey('households.id'))
    created_by_id = Column(Integer, ForeignKey('users.id'))
    
    # Relationships
    household = relationship("Household", back_populates="recipes")
    created_by = relationship("User")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())