"""Circa configuration — all settings from environment variables."""
import os
from dotenv import load_dotenv
load_dotenv()

# ── Supabase ──
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")

# ── Twilio ──
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_FROM = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")

# ── App ──
APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:8000")
YAPE_PHONE = os.getenv("YAPE_PHONE", "987654321")
PLIN_PHONE = os.getenv("PLIN_PHONE", "987654321")

# ── Security ──
PIN_MAX_ATTEMPTS = 3
PIN_BLOCK_MINUTES = 30
SESSION_TIMEOUT_MINUTES = 5
CART_TTL_HOURS = 24

# ── SUNAT / RENIEC API ──
# Supports: apiinti.dev, peruapi.com, apiperu.dev, apis.net.pe
PERU_API_PROVIDER = os.getenv("PERU_API_PROVIDER", "apiinti")  # apiinti | peruapi | apiperu
PERU_API_TOKEN = os.getenv("PERU_API_TOKEN", "")

# ── Content Template SIDs (Twilio) ──
TWILIO_TEMPLATE_MENU = os.getenv("TWILIO_TEMPLATE_MENU", "")
TWILIO_TEMPLATE_CATEGORIAS = os.getenv("TWILIO_TEMPLATE_CATEGORIAS", "")
TWILIO_TEMPLATE_PRODUCTOS_BEBIDAS = os.getenv("TWILIO_TEMPLATE_PRODUCTOS_BEBIDAS", "")
TWILIO_TEMPLATE_PRODUCTOS_LACTEOS = os.getenv("TWILIO_TEMPLATE_PRODUCTOS_LACTEOS", "")
TWILIO_TEMPLATE_PRODUCTOS_ABARROTES = os.getenv("TWILIO_TEMPLATE_PRODUCTOS_ABARROTES", "")
TWILIO_TEMPLATE_PRODUCTOS_CUIDADO = os.getenv("TWILIO_TEMPLATE_PRODUCTOS_CUIDADO", "")
TWILIO_TEMPLATE_PACK = os.getenv("TWILIO_TEMPLATE_PACK", "")
TWILIO_TEMPLATE_CANTIDAD = os.getenv("TWILIO_TEMPLATE_CANTIDAD", "")
TWILIO_TEMPLATE_ITEM_AGREGADO = os.getenv("TWILIO_TEMPLATE_ITEM_AGREGADO", "")
TWILIO_TEMPLATE_CARRITO = os.getenv("TWILIO_TEMPLATE_CARRITO", "")
TWILIO_TEMPLATE_MONTO = os.getenv("TWILIO_TEMPLATE_MONTO", "")
TWILIO_TEMPLATE_PLAZO = os.getenv("TWILIO_TEMPLATE_PLAZO", "")
TWILIO_TEMPLATE_LINEA = os.getenv("TWILIO_TEMPLATE_LINEA", "")

# ── Distribuidor notifications ──
DISTRIBUIDOR_WA_NUMERO = os.getenv("DISTRIBUIDOR_WA_NUMERO", "")  # Para notificar pedidos
