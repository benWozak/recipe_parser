from pydantic import BaseModel, HttpUrl, conlist
from typing import List, Dict, Optional, Union
from datetime import datetime

class NutritionInfo(BaseModel):
    calories: Optional[float] = None
    protein: Optional[float] = None
    carbohydrates: Optional[float] = None
    fat: Optional[float] = None
    fiber: Optional[float] = None
    sugar: Optional[float] = None
    # Possibly other nutritional fields

class Ingredient(BaseModel):
    item: str
    amount: Optional[float] = None
    unit: Optional[str] = None
    notes: Optional[str] = None

class RecipeBase(BaseModel):
    title: str
    ingredients: List[Ingredient]
    instructions: List[str]
    servings: Optional[int] = None
    prep_time_minutes: Optional[int] = None
    cook_time_minutes: Optional[int] = None
    total_time_minutes: Optional[int] = None
    cuisine: Optional[str] = None
    course: Optional[str] = None
    nutrition: Optional[NutritionInfo] = None

class InstagramRecipeCreate(RecipeBase):
    source_type: str = "instagram"
    source_url: HttpUrl
    video_url: HttpUrl
    caption: Optional[str] = None
    metadata: Optional[Dict] = None  # For Instagram-specific metadata

class WebsiteRecipeCreate(RecipeBase):
    source_type: str = "website"
    source_url: HttpUrl
    image_urls: Optional[List[HttpUrl]] = None
    metadata: Optional[Dict] = None  # For website-specific metadata

class BookRecipeCreate(RecipeBase):
    source_type: str = "book"
    book_title: str
    page_number: Optional[int] = None
    image_urls: Optional[List[HttpUrl]] = None
    metadata: Optional[Dict] = None  # For book-specific metadata

class RecipeCreate(BaseModel):
    recipe: Union[InstagramRecipeCreate, WebsiteRecipeCreate, BookRecipeCreate]

class Recipe(RecipeBase):
    id: int
    source_type: str
    source_url: Optional[str] = None
    image_urls: Optional[List[str]] = None
    video_url: Optional[str] = None
    metadata: Optional[Dict] = None
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True