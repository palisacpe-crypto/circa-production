"""
Distributor notification service.

Sends order notifications to the distributor via WhatsApp.
The distributor responds with simple buttons to update order status.
"""
import logging
from app.config import DISTRIBUIDOR_WA_NUMERO
from app.services.twilio_client import send_whatsapp

logger = logging.getLogger("circa.distribuidor")


def notificar_pedido_nuevo(pedido: dict, bodega: dict, items: list):
    """Notify distributor of a new order via WhatsApp."""
    if not DISTRIBUIDOR_WA_NUMERO:
        logger.warning("DISTRIBUIDOR_WA_NUMERO not set — skipping notification")
        return
    
    # Format items list
    items_text = "\n".join(
        f"  • {i['cantidad']}x pk{i['pack_size']} {i['nombre']} — S/{i['subtotal']:.2f}"
        for i in items
    )
    
    contado = pedido.get("monto_contado", 0)
    financiado = pedido.get("monto_financiado", 0)
    total = pedido.get("monto_productos", 0)
    
    msg = (
        f"🆕 *NUEVO PEDIDO CIRCA*\n\n"
        f"📋 Pedido: *{pedido['numero']}*\n"
        f"🏪 {bodega['nombre_comercial'] or bodega['razon_social']}\n"
        f"📍 {bodega.get('direccion', 'Sin dirección')}\n"
        f"📞 {bodega.get('telefono_whatsapp', '')}\n\n"
        f"*Productos:*\n{items_text}\n\n"
        f"💰 *Total: S/{total:.2f}*\n"
    )
    
    if financiado > 0:
        msg += (
            f"  💚 Financiado por Circa: S/{financiado:.2f}\n"
            f"  🟠 Contado en entrega: S/{contado:.2f}\n\n"
            f"💡 Circa te paga S/{financiado:.2f} en 24-48h post-entrega.\n"
        )
    
    msg += (
        f"\nResponde:\n"
        f"*RECIBIDO {pedido['numero']}* — confirmar recepción\n"
        f"*LISTO {pedido['numero']}* — pedido armado\n"
        f"*ENVIADO {pedido['numero']}* — en camino\n"
        f"*ENTREGADO {pedido['numero']}* — entregado"
    )
    
    try:
        send_whatsapp(DISTRIBUIDOR_WA_NUMERO, msg)
        logger.info(f"Notified distributor of order {pedido['numero']}")
    except Exception as e:
        logger.error(f"Failed to notify distributor: {e}")


def notificar_pago_circa(pedido: dict, monto: float):
    """Notify distributor that Circa has paid them for an order."""
    if not DISTRIBUIDOR_WA_NUMERO:
        return
    
    msg = (
        f"💚 *PAGO CIRCA*\n\n"
        f"Se ha transferido *S/{monto:.2f}* por el pedido *{pedido['numero']}*.\n"
        f"Revisa tu cuenta bancaria en las próximas horas.\n\n"
        f"Gracias por trabajar con Circa 🤝"
    )
    
    try:
        send_whatsapp(DISTRIBUIDOR_WA_NUMERO, msg)
    except Exception as e:
        logger.error(f"Failed to notify distributor payment: {e}")
