"""PIN management: hashing, validation, lockout."""
import bcrypt
from datetime import datetime, timedelta
from app.config import PIN_MAX_ATTEMPTS, PIN_BLOCK_MINUTES

def hash_pin(pin: str) -> str:
    return bcrypt.hashpw(pin.encode(), bcrypt.gensalt(rounds=12)).decode()

def verify_pin(pin: str, pin_hash: str) -> bool:
    return bcrypt.checkpw(pin.encode(), pin_hash.encode())

def is_pin_blocked(bodega: dict) -> bool:
    if bodega.get("pin_bloqueado_hasta"):
        blocked = datetime.fromisoformat(bodega["pin_bloqueado_hasta"].replace("Z", "+00:00"))
        return datetime.now(blocked.tzinfo) < blocked
    return False

def validate_pin_format(pin: str) -> tuple[bool, str]:
    """Validate PIN meets security requirements."""
    if len(pin) != 4 or not pin.isdigit():
        return False, "La clave debe ser de 4 dígitos."
    if pin in ("1234", "4321", "0000", "1111", "2222", "3333", "4444", "5555", "6666", "7777", "8888", "9999"):
        return False, "No uses números consecutivos ni repetitivos."
    return True, ""

def check_pin(pin: str, bodega: dict) -> tuple[bool, str, dict]:
    """Check PIN and manage attempts. Returns (success, message, updates_for_db)."""
    if is_pin_blocked(bodega):
        remaining = datetime.fromisoformat(bodega["pin_bloqueado_hasta"].replace("Z", "+00:00")) - datetime.utcnow().replace(tzinfo=None)
        mins = max(1, int(remaining.total_seconds() / 60))
        return False, f"🔒 Clave bloqueada. Intenta en {mins} minutos.", {}
    
    if verify_pin(pin, bodega["pin_hash"]):
        return True, "", {"pin_intentos": 0, "pin_bloqueado_hasta": None}
    
    attempts = bodega.get("pin_intentos", 0) + 1
    updates = {"pin_intentos": attempts}
    
    if attempts >= PIN_MAX_ATTEMPTS:
        block_until = (datetime.utcnow() + timedelta(minutes=PIN_BLOCK_MINUTES)).isoformat()
        updates["pin_bloqueado_hasta"] = block_until
        return False, f"🔒 Clave incorrecta. Bloqueada por {PIN_BLOCK_MINUTES} min.", updates
    
    remaining = PIN_MAX_ATTEMPTS - attempts
    return False, f"❌ Clave incorrecta. Te quedan {remaining} intento(s).", updates
