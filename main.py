from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from openai import OpenAI
import json
import os

# 1. Initialize FastAPI
app = FastAPI()

# Enable CORS so your frontend browser is allowed to talk to this Python server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Connect to your local LM Studio server
client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

# 3. User's Purchased Wardrobe Database (Now with real product images!)
user_wardrobe_db = [
    {
        "item_id": 1,
        "name": "Puma Lightweight Windrunner Jacket",
        "brand": "PUMA",
        "category": "Outerwear",
        "color": "Slate Grey",
        "tags": ["sport", "casual", "lightweight", "windbreaker", "pune weather"],
        "image_url": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?auto=format&fit=crop&w=600&q=80"
    },
    {
        "item_id": 2,
        "name": "Nike Air Zoom Pegasus Sneakers",
        "brand": "NIKE",
        "category": "Footwear",
        "color": "Onyx Black",
        "tags": ["sport", "running", "field games", "comfortable", "athletic"],
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=600&q=80"
    },
    {
        "item_id": 3,
        "name": "Tailored Black Athletic Shorts",
        "brand": "ADIDAS",
        "category": "Bottoms",
        "color": "Matte Black",
        "tags": ["casual", "summer", "sport", "field games", "breathable"],
        "image_url": "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?auto=format&fit=crop&w=600&q=80"
    },
    {
        "item_id": 4,
        "name": "Ray-Ban Classic Aviator Sunglasses",
        "brand": "RAY-BAN",
        "category": "Accessories",
        "color": "Gold / Charcoal",
        "tags": ["summer", "sunny", "outdoor", "stylish", "beach"],
        "image_url": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=600&q=80"
    },
    {
        "item_id": 5,
        "name": "Crisp Linen Resort Shirt",
        "brand": "MASSIMO DUTTI",
        "category": "Tops",
        "color": "Ivory White",
        "tags": ["smart casual", "summer", "evening", "brunch", "beach", "baby shower"],
        "image_url": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?auto=format&fit=crop&w=600&q=80"
    },
    {
        "item_id": 6,
        "name": "Tech Crossbody Waist Pack",
        "brand": "NIKE TECH",
        "category": "Bags",
        "color": "Volt / Black",
        "tags": ["casual", "sport", "festival", "hands-free", "field games"],
        "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=600&q=80"
    },
    {
        "item_id": 7,
        "name": "Pleated Chino Trousers",
        "brand": "ZARA",
        "category": "Bottoms",
        "color": "Sand Beige",
        "tags": ["smart casual", "brunch", "baby shower", "evening", "date"],
        "image_url": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?auto=format&fit=crop&w=600&q=80"
    },
    {
        "item_id": 8,
        "name": "Minimalist Leather Loafers",
        "brand": "COLE HAAN",
        "category": "Footwear",
        "color": "Espresso Brown",
        "tags": ["smart casual", "evening", "baby shower", "dinner"],
        "image_url": "https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?auto=format&fit=crop&w=600&q=80"
    }
]

# 4. E-Commerce Store Database (For the Horizontal Upsell Scroll when user has no clothes for an event)
store_catalog_db = [
    {
        "store_id": 101,
        "name": "Double-Breasted Wool Tuxedo",
        "brand": "MANISH MALHOTRA LUXE",
        "price": "₹24,999",
        "category": "Wedding / Formal",
        "image_url": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=600&q=80"
    },
    {
        "store_id": 102,
        "name": "Embroidered Silk Bandhgala",
        "brand": "SABYASACHI EDIT",
        "price": "₹32,500",
        "category": "Wedding / Festive",
        "image_url": "https://images.unsplash.com/photo-1593030761757-71fae45fa0e7?auto=format&fit=crop&w=600&q=80"
    },
    {
        "store_id": 103,
        "name": "Patent Leather Oxford Dress Shoes",
        "brand": "HUGO BOSS",
        "price": "₹18,400",
        "category": "Formal Footwear",
        "image_url": "https://images.unsplash.com/photo-1533867617858-e7b97e060509?auto=format&fit=crop&w=600&q=80"
    },
    {
        "store_id": 104,
        "name": "Chronograph Dress Watch",
        "brand": "TISSOT",
        "price": "₹41,000",
        "category": "Luxury Accessories",
        "image_url": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&w=600&q=80"
    }
]

class OutfitRequest(BaseModel):
    situation: str

# Route to view the frontend right at http://127.0.0.1:8000
@app.get("/")
async def serve_frontend():
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    return {"message": "Please create index.html in the same folder as main.py"}

# Route to fetch the user's digital closet
@app.get("/wardrobe")
async def get_wardrobe():
    return {"items": user_wardrobe_db}

# Route to generate AI Outfits
@app.post("/get_outfit")
async def get_outfit(request: OutfitRequest):
    # Include the exact item_id so the AI picks the right numbers!
    wardrobe_text = ""
    for item in user_wardrobe_db:
        wardrobe_text += (
            f"- ID: {item['item_id']} | Name: {item['name']} | "
            f"Category: {item['category']} | Color: {item['color']} | "
            f"Tags: {', '.join(item['tags'])}\n"
        )

    system_prompt = f"""
    You are an elite luxury fashion stylist integrated into an e-commerce platform.
    The user has ONLY bought the following items in their personal wardrobe:
    {wardrobe_text}

    RULES:
    1. Analyze the user's situation carefully.
    2. If the user asks for an event they clearly do NOT have clothes for (such as a traditional wedding, black-tie gala, or heavy winter snow), set "has_suitable_outfit" to false, leave "outfits" as an empty list [], and set "message" to "You have not bought any outfits for that event."
    3. Otherwise, set "has_suitable_outfit" to true, and create 2 to 3 complete, stylish outfits using ONLY the exact IDs from the wardrobe above.
    4. Each outfit MUST contain at least 3 complementary items (e.g., Top/Outerwear + Bottoms + Footwear + Accessory).
    """

    outfit_schema = {
        "type": "json_schema",
        "json_schema": {
            "name": "outfit_recommendation",
            "schema": {
                "type": "object",
                "properties": {
                    "has_suitable_outfit": {"type": "boolean"},
                    "message": {"type": "string"},
                    "outfits": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string"},
                                "occasion_tag": {"type": "string"},
                                "item_ids": {
                                    "type": "array",
                                    "items": {"type": "integer"}
                                },
                                "reasoning": {"type": "string"}
                            },
                            "required": ["title", "occasion_tag", "item_ids", "reasoning"]
                        }
                    }
                },
                "required": ["has_suitable_outfit", "message", "outfits"]
            }
        }
    }

    try:
        response = client.chat.completions.create(
            model="local-model",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.situation}
            ],
            temperature=0.2,
            response_format=outfit_schema
        )

        ai_data = json.loads(response.choices[0].message.content)

        # Map each item_id to the full item dictionary (with image_url, brand, color)
        item_lookup = {item["item_id"]: item for item in user_wardrobe_db}
        enriched_outfits = []

        for outfit in ai_data.get("outfits", []):
            full_items = [
                item_lookup[iid]
                for iid in outfit.get("item_ids", [])
                if iid in item_lookup
            ]
            if full_items:
                enriched_outfits.append({
                    "title": outfit["title"],
                    "occasion_tag": outfit.get("occasion_tag", "Curated Look"),
                    "reasoning": outfit["reasoning"],
                    "items": full_items
                })

        # If the user doesn't have suitable clothes (or AI returned empty), send store recommendations
        if not ai_data.get("has_suitable_outfit", True) or len(enriched_outfits) == 0:
            return {
                "status": "success",
                "has_suitable_outfit": False,
                "message": "You have not bought any outfits for that event.",
                "outfits": [],
                "store_recommendations": store_catalog_db
            }

        return {
            "status": "success",
            "has_suitable_outfit": True,
            "message": ai_data.get("message", "Curated from your personal wardrobe."),
            "outfits": enriched_outfits,
            "store_recommendations": []
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
