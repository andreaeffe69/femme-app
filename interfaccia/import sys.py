import sys
sys.path.append('C:\\ASTROLOGIA_PROGETTO\\app_mobile')
from calcoli.astrocalc import calcola_potenze_astrologiche

# Test con dati di esempio
risultato = calcola_potenze_astrologiche(
    data_nascita="1990-08-15",
    ora_nascita="12:30",
    lat=41.9028,
    lon=12.4964
)

print("="*50)
print("RISULTATO POTENZE:")
print("="*50)
print(f"Armonici: +{risultato['totali']['armonici']:.1f}")
print(f"Disarmonici: {risultato['totali']['disarmonici']:.1f}")
print(f"Neutri: +{risultato['totali']['neutri']:.1f}")
print(f"TOTALE: {risultato['totali']['totale_complessivo']:.1f}")
print("="*50)

print("\nPRIMI 5 ASPETTI PIANETA-CUSPIDE:")
for a in risultato['aspetti_pianeta_cuspide'][:5]:
    print(f"   {a['pianeta']} - {a['cuspide']}: {a['aspetto']} ({a['potenza']:+.1f})")

input("Premi Invio per uscire...")