"""Send WhatsApp messages via Twilio — Full interactive templates."""
import json
from twilio.rest import Client
from app.config import (
    TWILIO_SID, TWILIO_TOKEN, TWILIO_FROM,
    TWILIO_TEMPLATE_MENU,
    TWILIO_TEMPLATE_CATEGORIAS,
    TWILIO_TEMPLATE_PRODUCTOS_BEBIDAS,
    TWILIO_TEMPLATE_PRODUCTOS_LACTEOS,
    TWILIO_TEMPLATE_PRODUCTOS_ABARROTES,
    TWILIO_TEMPLATE_PRODUCTOS_CUIDADO,
    TWILIO_TEMPLATE_PACK,
    TWILIO_TEMPLATE_CANTIDAD,
    TWILIO_TEMPLATE_ITEM_AGREGADO,
    TWILIO_TEMPLATE_CARRITO,
    TWILIO_TEMPLATE_MONTO,
    TWILIO_TEMPLATE_PLAZO,
    TWILIO_TEMPLATE_LINEA,
)

client = Client(TWILIO_SID, TWILIO_TOKEN)


def _wa(to: str) -> str:
    return to if to.startswith("whatsapp:") else f"whatsapp:{to}"


def send_whatsapp(to: str, body: str):
    return client.messages.create(from_=TWILIO_FROM, to=_wa(to), body=body)


def send_template(to: str, content_sid: str, variables: dict | None = None):
    """Send a WhatsApp Content Template message."""
    if not content_sid:
        raise ValueError("Content SID is empty — check your .env")
    payload = {"from_": TWILIO_FROM, "to": _wa(to), "content_sid": content_sid}
    if variables:
        payload["content_variables"] = json.dumps(variables)
    return client.messages.create(**payload)


# ═══════════════════════════════════════════════
# TEMPLATE SENDERS
# ═══════════════════════════════════════════════

def send_menu(to: str, linea_disponible: float):
    """Quick Reply: PEDIDO / LINEA / ESTADO"""
    return send_template(to, TWILIO_TEMPLATE_MENU, {"1": f"{linea_disponible:.2f}"})


def send_categorias(to: str):
    """List Picker: Bebidas / Lácteos / Abarrotes / Cuidado"""
    return send_template(to, TWILIO_TEMPLATE_CATEGORIAS)


def send_productos_bebidas(to: str):
    """List Picker: products in Bebidas"""
    return send_template(to, TWILIO_TEMPLATE_PRODUCTOS_BEBIDAS)


def send_productos_lacteos(to: str):
    """List Picker: products in Lácteos"""
    return send_template(to, TWILIO_TEMPLATE_PRODUCTOS_LACTEOS)


def send_productos_abarrotes(to: str):
    """List Picker: products in Abarrotes"""
    return send_template(to, TWILIO_TEMPLATE_PRODUCTOS_ABARROTES)


def send_productos_cuidado(to: str):
    """List Picker: products in Cuidado personal"""
    return send_template(to, TWILIO_TEMPLATE_PRODUCTOS_CUIDADO)


CATEGORY_SENDERS = {
    "bebidas": send_productos_bebidas,
    "lacteos": send_productos_lacteos,
    "abarrotes": send_productos_abarrotes,
    "cuidado": send_productos_cuidado,
}


def send_pack_selection(to: str, producto_nombre: str, p6: float, p12: float, p24: float):
    """Quick Reply: Pack 6 / Pack 12 / Pack 24"""
    return send_template(to, TWILIO_TEMPLATE_PACK, {
        "1": producto_nombre,
        "2": f"{p6:.2f}",
        "3": f"{p12:.2f}",
        "4": f"{p24:.2f}",
    })


def send_cantidad(to: str, producto_nombre: str, pack_label: str, precio: float):
    """Quick Reply: 1 pack / 2 packs / 3 packs"""
    return send_template(to, TWILIO_TEMPLATE_CANTIDAD, {
        "1": producto_nombre,
        "2": pack_label,
        "3": f"{precio:.2f}",
    })


def send_item_agregado(to: str, cantidad: int, pack_label: str, nombre: str, subtotal: float, cart_total: float):
    """Quick Reply: Agregar más / Revisar / Financiar"""
    return send_template(to, TWILIO_TEMPLATE_ITEM_AGREGADO, {
        "1": str(cantidad),
        "2": pack_label,
        "3": nombre,
        "4": f"{subtotal:.2f}",
        "5": f"{cart_total:.2f}",
    })


def send_carrito_resumen(to: str, items_text: str, total: float, financiable: float):
    """Quick Reply: Financiar / Agregar más / Vaciar"""
    return send_template(to, TWILIO_TEMPLATE_CARRITO, {
        "1": items_text,
        "2": f"{total:.2f}",
        "3": f"{financiable:.2f}",
    })


def send_monto_financiar(to: str, linea: float, total_pedido: float, financiable: float):
    """Quick Reply: Total / 50% / 25%"""
    return send_template(to, TWILIO_TEMPLATE_MONTO, {
        "1": f"{linea:.2f}",
        "2": f"{total_pedido:.2f}",
        "3": f"{financiable:.2f}",
    })


def send_plazo(to: str, monto: float, fee7: float, total7: float, fee15: float, total15: float, fee30: float, total30: float):
    """Quick Reply: 7 días / 15 días / 30 días"""
    return send_template(to, TWILIO_TEMPLATE_PLAZO, {
        "1": f"{monto:.2f}",
        "2": f"{fee7:.2f}", "3": f"{total7:.2f}",
        "4": f"{fee15:.2f}", "5": f"{total15:.2f}",
        "6": f"{fee30:.2f}", "7": f"{total30:.2f}",
    })


# ── Legacy aliases ──
def send_catalogo_categorias(to: str):
    return send_categorias(to)


def send_linea_preaprobada(to: str, nombre_bodega: str, monto: str):
    return send_template(to, TWILIO_TEMPLATE_LINEA, {"1": nombre_bodega, "2": monto})


def send_packs(to: str, producto: str):
    """Legacy — use send_pack_selection instead."""
    return send_template(to, TWILIO_TEMPLATE_PACK, {"1": producto, "2": "0", "3": "0", "4": "0"})


def send_plazos_financiamiento(to: str):
    """Legacy — use send_plazo instead."""
    return send_template(to, TWILIO_TEMPLATE_PLAZO)
