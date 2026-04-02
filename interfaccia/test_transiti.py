import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

print("1. Tentativo di import...")
try:
    from calcoli.transiti import MESSAGGI_TRANSITI
    print("2. ✅ IMPORT RIUSCITO")
    print(f"3. MESSAGGI_TRANSITI = {MESSAGGI_TRANSITI}")
except Exception as e:
    print(f"4. ❌ ERRORE: {e}")