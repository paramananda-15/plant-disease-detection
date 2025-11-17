# backend/predict.py - WITH PRODUCT RECOMMENDATIONS
import tensorflow as tf
import numpy as np
from PIL import Image
import os
import json

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "model", "plant_disease_model.keras")
CLASS_FILE = os.path.join(BASE_DIR, "model", "class_names.json")

with open(CLASS_FILE, "r") as f:
    CLASS_NAMES = json.load(f)

IMG_SIZE = (224, 224)
model = tf.keras.models.load_model(MODEL_PATH)
print(f"✅ Model loaded: {len(CLASS_NAMES)} classes")

# Disease Information Database
DISEASE_INFO = {
    "Apple___Apple_scab": {
        "description": "Fungal disease causing dark, scabby lesions on leaves, fruit, and twigs",
        "symptoms": "Olive-green to brown spots on leaves, cracked and deformed fruits",
        "severity": "Moderate to High"
    },
    "Apple___Black_rot": {
        "description": "Fungal disease causing fruit rot and leaf spots",
        "symptoms": "Purple or red spots on leaves, rotted fruit with concentric rings",
        "severity": "High"
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "description": "Fungal disease causing long elliptical lesions on leaves",
        "symptoms": "Gray-green to tan lesions on leaves, reduced yield",
        "severity": "Moderate"
    },
    "Grape___Black_rot": {
        "description": "Fungal disease affecting leaves, shoots, and fruit",
        "symptoms": "Brown circular leaf spots, shriveled mummified berries",
        "severity": "High"
    },
    "Tomato___Late_blight": {
        "description": "Devastating fungal disease that can destroy entire crops",
        "symptoms": "Water-soaked lesions on leaves and stems, white mold on undersides",
        "severity": "Very High"
    },
    "Potato___Late_blight": {
        "description": "Same pathogen as tomato late blight, highly destructive",
        "symptoms": "Dark brown to black lesions on leaves, tuber rot",
        "severity": "Very High"
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "description": "Viral disease transmitted by whiteflies",
        "symptoms": "Upward curling and yellowing of leaves, stunted growth",
        "severity": "High"
    },
}

# Product Recommendations Database
PRODUCT_RECOMMENDATIONS = {
    # Fungal Diseases
    "Apple___Apple_scab": [
        {"name": "Captan 50 WP", "type": "Fungicide", "usage": "Mix 2g/liter, spray every 10-14 days", "price": "₹450/500g"},
        {"name": "Mancozeb 75% WP", "type": "Fungicide", "usage": "Mix 2.5g/liter water", "price": "₹350/kg"},
        {"name": "Copper Oxychloride", "type": "Fungicide", "usage": "Preventive spray before disease onset", "price": "₹280/kg"},
        {"name": "Neem Oil", "type": "Organic", "usage": "Mix 5ml/liter, spray weekly", "price": "₹120/100ml"}
    ],
    "Apple___Black_rot": [
        {"name": "Thiophanate Methyl", "type": "Fungicide", "usage": "Mix 1g/liter, spray every 15 days", "price": "₹680/kg"},
        {"name": "Ziram 27% SC", "type": "Fungicide", "usage": "Protective fungicide, use before infection", "price": "₹420/liter"},
        {"name": "Bordeaux Mixture", "type": "Fungicide", "usage": "Traditional copper-based fungicide", "price": "₹180/kg"}
    ],
    "Corn_(maize)___Northern_Leaf_Blight": [
        {"name": "Propiconazole 25% EC", "type": "Fungicide", "usage": "1ml/liter at early symptoms", "price": "₹850/liter"},
        {"name": "Azoxystrobin 23% SC", "type": "Fungicide", "usage": "Systemic fungicide, 1ml/liter", "price": "₹1200/liter"},
        {"name": "Mancozeb + Carbendazim", "type": "Fungicide", "usage": "Combination spray for better control", "price": "₹620/kg"}
    ],
    "Grape___Black_rot": [
        {"name": "Myclobutanil 10% WP", "type": "Fungicide", "usage": "0.5g/liter every 2 weeks", "price": "₹920/kg"},
        {"name": "Captan + Hexaconazole", "type": "Fungicide", "usage": "Combination for resistant strains", "price": "₹740/kg"},
        {"name": "Sulfur 80% WP", "type": "Fungicide", "usage": "Organic option, 3g/liter", "price": "₹160/kg"}
    ],
    "Tomato___Late_blight": [
        {"name": "Metalaxyl + Mancozeb", "type": "Fungicide", "usage": "Emergency treatment, 2.5g/liter", "price": "₹890/kg"},
        {"name": "Cymoxanil 8% + Mancozeb 64%", "type": "Fungicide", "usage": "Curative action within 48hrs", "price": "₹780/kg"},
        {"name": "Copper Hydroxide", "type": "Fungicide", "usage": "Preventive, spray before rain", "price": "₹320/kg"},
        {"name": "Potassium Phosphonate", "type": "Fungicide", "usage": "Systemic, boosts plant immunity", "price": "₹650/liter"}
    ],
    "Potato___Late_blight": [
        {"name": "Dimethomorph 50% WP", "type": "Fungicide", "usage": "200g/acre, preventive spray", "price": "₹1100/kg"},
        {"name": "Metalaxyl 8% + Mancozeb 64%", "type": "Fungicide", "usage": "Best for potato blight", "price": "₹890/kg"},
        {"name": "Fosetyl-Al 80% WP", "type": "Fungicide", "usage": "Systemic, 2.5g/liter", "price": "₹950/kg"}
    ],
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": [
        {"name": "Imidacloprid 17.8% SL", "type": "Insecticide", "usage": "Control whitefly vector, 0.5ml/liter", "price": "₹420/liter"},
        {"name": "Thiamethoxam 25% WG", "type": "Insecticide", "usage": "Systemic, 0.2g/liter", "price": "₹580/100g"},
        {"name": "Neem Oil + Soap", "type": "Organic", "usage": "Organic whitefly control", "price": "₹180/liter"},
        {"name": "Acetamiprid 20% SP", "type": "Insecticide", "usage": "Quick knockdown of whiteflies", "price": "₹340/100g"},
        {"name": "Yellow Sticky Traps", "type": "Physical Control", "usage": "10-15 traps per acre", "price": "₹250/10 traps"}
    ],
    # Healthy plants
    "Apple___healthy": [
        {"name": "NPK 19:19:19", "type": "Fertilizer", "usage": "Balanced nutrition, 5g/plant", "price": "₹280/kg"},
        {"name": "Seaweed Extract", "type": "Growth Promoter", "usage": "Foliar spray, 2ml/liter", "price": "₹380/liter"}
    ],
    "Corn_(maize)___healthy": [
        {"name": "Urea 46% N", "type": "Fertilizer", "usage": "Top dressing, 100kg/acre", "price": "₹290/50kg"},
        {"name": "Zinc Sulfate", "type": "Micronutrient", "usage": "Prevents deficiency, 5kg/acre", "price": "₹120/kg"}
    ],
    "Grape___healthy": [
        {"name": "Calcium Nitrate", "type": "Fertilizer", "usage": "Improves fruit quality", "price": "₹340/kg"},
        {"name": "Humic Acid", "type": "Soil Conditioner", "usage": "Enhances nutrient uptake", "price": "₹480/liter"}
    ],
    "Tomato___healthy": [
        {"name": "13:0:45 (Potash)", "type": "Fertilizer", "usage": "Fruit development stage", "price": "₹320/kg"},
        {"name": "Calcium Boron", "type": "Micronutrient", "usage": "Prevents blossom end rot", "price": "₹180/kg"}
    ],
    "Potato___healthy": [
        {"name": "12:32:16 NPK", "type": "Fertilizer", "usage": "High phosphorus for tubers", "price": "₹360/kg"},
        {"name": "Potassium Humate", "type": "Organic", "usage": "Improves tuber quality", "price": "₹420/kg"}
    ]
}

def predict_image(path):
    img = Image.open(path).convert("RGB").resize(IMG_SIZE)
    arr = np.array(img, dtype=np.float32)
    arr = np.expand_dims(arr, axis=0)
    preds = model.predict(arr, verbose=0)
    idx = int(np.argmax(preds))
    conf = float(preds[0][idx])
    return CLASS_NAMES[idx], conf

def predict_top_k(path, k=3):
    img = Image.open(path).convert("RGB").resize(IMG_SIZE)
    arr = np.array(img, dtype=np.float32)
    arr = np.expand_dims(arr, axis=0)
    preds = model.predict(arr, verbose=0)[0]
    top_k_idx = np.argsort(preds)[-k:][::-1]
    return [(CLASS_NAMES[idx], float(preds[idx])) for idx in top_k_idx]

def get_disease_info(label):
    """Get disease information"""
    default = {
        "description": "Information not available for this disease",
        "symptoms": "Monitor plant health regularly",
        "severity": "Unknown"
    }
    return DISEASE_INFO.get(label, default)

def get_products(label):
    """Get product recommendations for detected disease"""
    # Return products for the specific disease, or empty if not found
    return PRODUCT_RECOMMENDATIONS.get(label, [])

def get_treatment_advice(label):
    """Get treatment advice based on disease"""
    advice = {
        "Apple___Apple_scab": [
            "Remove and destroy infected leaves",
            "Apply fungicide preventively before wet periods",
            "Improve air circulation by pruning",
            "Avoid overhead irrigation"
        ],
        "Tomato___Late_blight": [
            "Remove infected plants immediately",
            "Apply fungicide at first sign of disease",
            "Avoid working in wet foliage",
            "Use resistant varieties in future"
        ],
        "Tomato___Tomato_Yellow_Leaf_Curl_Virus": [
            "Control whitefly population immediately",
            "Remove infected plants to prevent spread",
            "Use yellow sticky traps",
            "Plant virus-resistant varieties",
            "Use reflective mulch to repel whiteflies"
        ]
    }
    return advice.get(label, ["Consult local agricultural extension for specific advice"])
