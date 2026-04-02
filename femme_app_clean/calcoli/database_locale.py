"""
Gestione database locale per salvare i soggetti
"""
import json
import os
from pathlib import Path

class DatabaseLocale:
    def __init__(self, file_name="soggetti.json"):
        # Salva nella cartella principale dell'app, non in cloud
        self.file_path = Path(__file__).parent.parent / file_name
        print(f"📁 Database path: {self.file_path}")
    
    def carica_soggetti(self):
        """Carica la lista dei soggetti salvati"""
        if not self.file_path.exists():
            print("📁 Nessun file database trovato")
            return []
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"📁 Caricati {len(data)} soggetti")
                return data
        except Exception as e:
            print(f"❌ Errore caricamento: {e}")
            return []
    
    def salva_soggetto(self, soggetto):
        """Salva un nuovo soggetto"""
        soggetti = self.carica_soggetti()
        
        # Evita duplicati (controlla per nome)
        trovato = False
        for i, s in enumerate(soggetti):
            if s['nome'] == soggetto['nome']:
                soggetti[i] = soggetto
                trovato = True
                print(f"📁 Aggiornato soggetto: {soggetto['nome']}")
                break
        
        if not trovato:
            soggetti.append(soggetto)
            print(f"📁 Aggiunto nuovo soggetto: {soggetto['nome']}")
        
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(soggetti, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Errore salvataggio: {e}")
            return False
    
    def cancella_soggetto(self, nome):
        """Cancella un soggetto"""
        soggetti = self.carica_soggetti()
        soggetti = [s for s in soggetti if s['nome'] != nome]
        
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(soggetti, f, indent=2, ensure_ascii=False)
            print(f"📁 Cancellato soggetto: {nome}")
            return True
        except Exception as e:
            print(f"❌ Errore cancellazione: {e}")
            return False
    
    def get_soggetto_by_nome(self, nome):
        """Cerca un soggetto per nome"""
        soggetti = self.carica_soggetti()
        for s in soggetti:
            if s['nome'] == nome:
                return s
        return None