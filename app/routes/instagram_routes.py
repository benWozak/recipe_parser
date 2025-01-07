from fastapi import APIRouter, HTTPException
from ..services.instagram_service import InstagramService
from ..models.recipe import Recipe as RecipeModel  # Rename to avoid confusion
from ..schemas.recipe import InstagramRecipeCreate, Recipe as RecipeSchema
from typing import Dict

router = APIRouter()
instagram_service = InstagramService()

@router.post("/recipes/instagram/import")
async def import_instagram_recipe(url: str) -> Dict:
    recipe_data = instagram_service.get_post_by_url(url)
    if not recipe_data:
        raise HTTPException(status_code=404, detail="Could not fetch Instagram post")
    return recipe_data