from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import threading
import pytz
from datetime import datetime  # <-- AGGIUNGI QUESTO
from kivy.animation import Animation
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.image import Image  # <-- AGGIUNGI PER EVENTUALE LOGO
from kivy.uix.video import Video  # <-- AGGIUNGI QUESTA RIGA
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from calcoli.astrocalc import genera_profilo_caratteriale, interpreta_casa, calcola_posizioni_e_case

try:
    from calcoli.transiti import MESSAGGI_TRANSITI
    print(f"✅ MESSAGGI_TRANSITI importato: {MESSAGGI_TRANSITI}")
    print(f"   Chiavi disponibili: {list(MESSAGGI_TRANSITI.keys())}")
except ImportError as e:
    print(f"❌ Errore import MESSAGGI_TRANSITI: {e}")
    MESSAGGI_TRANSITI = {}

from calcoli.database_locale import DatabaseLocale
from calcoli.transiti import CalcolatoreTransiti

class AstroApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = DatabaseLocale()
        self.soggetti_caricati = []
        self.soggetto_corrente = None
        self.splash = None  # <-- AGGIUNGI QUESTA RIGA
    
    def crea_tab_benvenuto(self):
        """Crea la tab di benvenuto con la prefazione"""
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # ScrollView per rendere il contenuto scorrevole
        scroll = ScrollView(size_hint=(1, 1))
        content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=15, padding=10)
        content.bind(minimum_height=content.setter('height'))
        
        # Titolo
        titolo = Label(
            text="[b]🌸 Benvenuta in Femme 🌸[/b]",
            markup=True,
            font_size='20sp',
            size_hint_y=None,
            height=50
        )
        content.add_widget(titolo)
        
        # Prefazione
        testo = Label(
            text="""
Oroscopo viene dal greco hōroskópos: "osservare l'ora". Quell'ora precisa in cui sei passata dallo stato amniotico alla vita extrauterina, compiendo il tuo primo respiro.

In quel momento, il cielo aveva una configurazione unica. Pianeti, segni, case, aspetti: una geometria perfetta che non si ripeterà mai più. Quella configurazione è la tua impronta. Il tuo destino.

Nella sezione Profilo troverai la spiegazione di questa impronta: ciò che sei, ciò che porti con te, le tue inclinazioni più profonde, le tue attitudini naturali e anche le ragioni per cui a volte è difficile metterle in atto. In quella sezione c'è una spiegazione del tuo modo di porti al mondo e di ciò che in realtà vuoi, o che sei spinta ad avere. Quello sarà il tuo tratto distintivo.

Ma la vita non è statica. I pianeti continuano a muoversi. E quando incontrano la tua mappa natale, accendono qualcosa. Creano transiti. È qui che Femme ti accompagna: nella lettura dei transiti, per capire cosa ti sta succedendo in questo momento. Perché spesso il dolore più grande non è l'evento in sé, ma la sensazione di non capire cosa ci stia accadendo. Di essere sballottate da forze che ci sembrano arbitrarie. Di sentirsi sole.

Femme ti offre una voce che comprende le tue dinamiche, che dà un nome a ciò che senti. Non per predire il futuro, ma per aiutarti a orientarti nel presente. Perché quando capisci cosa sta accadendo, smetti di subirlo e inizi ad abitarlo in modo diverso.

[b]Come usare questa app[/b]

La lettura va capita e misurata con quello che succede intorno a te, dentro di te. Giorno dopo giorno, costruisci dei riferimenti. Annota cosa accade, come ti senti, cosa risuona e cosa no. Con un po' di dedizione e pazienza, questi riferimenti ti aiuteranno a costruire un potente mezzo di supervisione della tua esistenza.

Il senso di questo approccio è rendere attiva la lettura. Non sei spettatrice, ma colei che, attraverso una visione più chiara degli eventi, impara a danzare con essi. La maturità si raggiunge quando, in qualsiasi tipo di situazione tu sia immersa, riesci a capire ciò che è successo, a farlo tuo, e a comprendere come procedere alla costruzione di una nuova visione di vita.

Prospettive diverse inquadrano il problema in maniera diversa. Femme ti aiuta a vedere in un'altra prospettiva.

[b]L'elemento fondamentale[/b]

L'orario di nascita è l'elemento basilare per una lettura fedele e veritiera. 4 minuti sono 1 grado. Quel piccolo spostamento apparentemente insignificante fa la differenza nel percorso della vita. Due gemelli, nati a pochi minuti di distanza, avranno mappe simili ma non identiche, e questo basta a renderli due anime uniche, con percorsi diversi. Usa questa lettura per raffinare e, se necessario, per rettificare l'orario di nascita. È un lavoro di cesello che renderà l'impronta sempre più fedele alla tua essenza.

Femme non è un oracolo che predice il futuro. È una lente che ti aiuta a vedere con più chiarezza il tuo presente, a comprendere il tuo passato e ad affrontare il tuo futuro con la consapevolezza di chi sa che la vera libertà non è scegliere cosa ti capita, ma come scegli di abitare ciò che ti capita.

Benvenuta in questo viaggio. Siamo qui per accompagnarti.
""",
            markup=True,
            font_size='14sp',
            size_hint_y=None,
            text_size=(Window.width - 80, None),
            halign='left',
            valign='top'
        )
        testo.bind(width=lambda instance, value: setattr(instance, 'text_size', (value - 20, None)))
        testo.bind(texture_size=lambda instance, size: setattr(instance, 'height', size[1]))
        content.add_widget(testo)
        
        # Pulsante per iniziare
        btn_inizia = Button(
            text="✨ Inizia il tuo viaggio ✨",
            size_hint_y=None,
            height=50,
            background_color=(0.6, 0.3, 0.5, 1),
            font_size='16sp'
        )
        btn_inizia.bind(on_press=self.porta_a_profilo)
        content.add_widget(btn_inizia)
        
        scroll.add_widget(content)
        layout.add_widget(scroll)
        return layout
    
    def porta_a_profilo(self, instance):
        """Porta l'utente alla tab Profilo"""
        if hasattr(self, 'main_panel'):
            for tab in self.main_panel.tab_list:
                if tab.text == '🔮 Profilo':
                    self.main_panel.switch_to(tab)
                    break
                
    def build(self):
        """Versione base: solo video poi app"""
        return self.crea_splash()

    def crea_splash(self):
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.image import Image
        from kivy.uix.label import Label
        from kivy.clock import Clock
        import os
        
        layout = BoxLayout(orientation='vertical')
        layout.size_hint = (1, 1)
        
        # Sfondo blu notte
        from kivy.graphics import Color, Rectangle
        with layout.canvas.before:
            Color(0.04, 0.06, 0.16, 1)
            Rectangle(size=layout.size, pos=layout.pos)
        
        # Logo PNG
        logo_path = os.path.join(os.path.dirname(__file__), 'assets', 'logo_femme.png')
        
        if os.path.exists(logo_path):
            logo = Image(source=logo_path, allow_stretch=True)
            logo.size_hint = (0.6, 0.4)
            logo.pos_hint = {'center_x': 0.5, 'center_y': 0.55}
            layout.add_widget(logo)
            print("✅ Logo trovato")
        else:
            logo = Label(
                text="FEMME",
                font_size='80sp',
                bold=True,
                color=(0.97, 0.78, 0.87, 1),
                size_hint=(1, 0.4),
                pos_hint={'center_y': 0.55},
                halign='center',
                valign='center'
            )
            layout.add_widget(logo)
        
        # Frase
        frase = Label(
            text="la tua stella, la tua voce",
            font_size='16sp',
            color=(0.85, 0.7, 0.9, 1),
            size_hint=(1, 0.1),
            pos_hint={'center_y': 0.35},
            halign='center',
            valign='center'
        )
        layout.add_widget(frase)
        
        Clock.schedule_once(self.carica_app, 2.5)
        return layout

    def carica_app(self, dt):
        """Carica l'app principale dopo lo splash"""
        from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
        from kivy.clock import Clock
        
        print("✅ Carico app...")
        
        # Ferma il video
        if hasattr(self, 'video') and self.video:
            self.video.state = 'pause'
        
        # Crea l'interfaccia principale
        root = TabbedPanel()
        root.do_default_tab = False
        
        # SALVA IL RIFERIMENTO AL TabbedPanel
        self.main_panel = root
        
        # Tab Benvenuta
        tab_benvenuto = TabbedPanelItem(text='🌸 Benvenuta')
        tab_benvenuto.content = self.crea_tab_benvenuto()
        root.add_widget(tab_benvenuto)
        
        # Tab Profilo
        tab_profilo = TabbedPanelItem(text='🔮 Profilo')
        tab_profilo.content = self.crea_tab_profilo()
        root.add_widget(tab_profilo)
        
        # Tab Transiti
        tab_transiti = TabbedPanelItem(text='✨ Transiti')
        tab_transiti.content = self.crea_tab_transiti()
        root.add_widget(tab_transiti)
        
        # Sostituisci lo splash con l'app
        self.root.clear_widgets()
        self.root.add_widget(root)
        
        # Apri automaticamente la tab Benvenuta
        Clock.schedule_once(lambda dt: root.switch_to(tab_benvenuto), 0.1)
        
        print("✅ App caricata, tab Benvenuta attiva!")

    
        
    def crea_tab_profilo(self):
        """Crea il contenuto della tab Profilo"""
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=5)
            
        # Titolo
        title = Label(text='🔮 ASTRO APP', size_hint_y=0.08, font_size='24sp', color=(0.9, 0.7, 0.2, 1))
        main_layout.add_widget(title)
            
        # Form input con pulsante ricerca
        form = GridLayout(cols=3, spacing=5, size_hint_y=0.35)
            
        # Riga 1: Nome
        form.add_widget(Label(text='Nome:', color=(1,1,1,1)))
        self.nome_input = TextInput(multiline=False)
        self.nome_input.bind(on_double_tap=self.pulisci_campo)
        form.add_widget(self.nome_input)
        form.add_widget(Label(text=''))
            
        # Riga 2: Data
        form.add_widget(Label(text='Data (GG/MM/AAAA):', color=(1,1,1,1)))
        self.data_input = TextInput(text='15/08/1990', multiline=False)
        self.data_input.bind(on_double_tap=self.pulisci_campo)
        form.add_widget(self.data_input)
        form.add_widget(Label(text=''))
            
        # Riga 3: Ora
        form.add_widget(Label(text='Ora (HH:MM):', color=(1,1,1,1)))
        self.ora_input = TextInput(text='12:30', multiline=False)
        self.ora_input.bind(on_double_tap=self.pulisci_campo)
        form.add_widget(self.ora_input)
        form.add_widget(Label(text=''))
            
        # Riga 4: Luogo con pulsante
        form.add_widget(Label(text='Luogo:', color=(1,1,1,1)))
        self.luogo_input = TextInput(text='Roma, Italia', multiline=False)
        self.luogo_input.bind(on_double_tap=self.pulisci_campo)
        form.add_widget(self.luogo_input)
            
        self.cerca_btn = Button(
            text='🔍 Cerca',
            background_color=(0.3, 0.5, 0.9, 1),
            color=(1,1,1,1),
            size_hint_x=0.3,
            font_size='12sp'
            )
        self.cerca_btn.bind(on_press=self.cerca_luogo)
        form.add_widget(self.cerca_btn)
            
        # Riga 5: Latitudine
        form.add_widget(Label(text='Latitudine:', color=(1,1,1,1)))
        self.lat_input = TextInput(text='41.9028', multiline=False)
        self.lat_input.bind(on_double_tap=self.pulisci_campo)
        form.add_widget(self.lat_input)
        form.add_widget(Label(text=''))
            
        # Riga 6: Longitudine
        form.add_widget(Label(text='Longitudine:', color=(1,1,1,1)))
        self.lon_input = TextInput(text='12.4964', multiline=False)
        self.lon_input.bind(on_double_tap=self.pulisci_campo)
        form.add_widget(self.lon_input)
        form.add_widget(Label(text=''))
            
        main_layout.add_widget(form)
            
        # Pulsanti principali
        button_layout = BoxLayout(size_hint_y=0.1, spacing=5)
            
        self.profilo_btn = Button(
            text='📊 PROFILO CARATTERIALE',
            background_color=(0.2, 0.6, 0.2, 1),
            color=(1,1,1,1),
            font_size='14sp'
        )
        self.profilo_btn.bind(on_press=self.calcola_profilo)
        button_layout.add_widget(self.profilo_btn)
            
        self.previsione_btn = Button(
            text='🔮 PREVISIONE RS/RL',
            background_color=(0.6, 0.2, 0.2, 1),
            color=(1,1,1,1),
            font_size='14sp'
        )
        self.previsione_btn.bind(on_press=self.calcola_previsione)
        button_layout.add_widget(self.previsione_btn)
            
        main_layout.add_widget(button_layout)
            
        # Gestione soggetti
        soggetti_layout = BoxLayout(size_hint_y=0.1, spacing=5)
            
        self.salva_soggetto_btn = Button(
            text='💾 Salva Soggetto',
            background_color=(0.3, 0.6, 0.3, 1),
            color=(1,1,1,1),
            font_size='14sp'
        )
        self.salva_soggetto_btn.bind(on_press=self.salva_soggetto)
        soggetti_layout.add_widget(self.salva_soggetto_btn)
            
        self.carica_soggetto_btn = Button(
            text='📂 Carica Soggetto',
            background_color=(0.3, 0.3, 0.6, 1),
            color=(1,1,1,1),
            font_size='14sp'
        )
        self.carica_soggetto_btn.bind(on_press=self.mostra_lista_soggetti)
        soggetti_layout.add_widget(self.carica_soggetto_btn)
            
        main_layout.add_widget(soggetti_layout)
            
        # Pulsante audio e pulisci
        audio_layout = BoxLayout(size_hint_y=0.08, spacing=5)
            
        self.audio_btn = Button(
            text='🔊 SALVA AUDIO',
            background_color=(0.4, 0.4, 0.8, 1),
            color=(1,1,1,1),
            font_size='12sp'
        )
        self.audio_btn.bind(on_press=self.salva_audio_ultimo)
        audio_layout.add_widget(self.audio_btn)
            
        self.pulisci_btn = Button(
            text='🧹 Pulisci',
            background_color=(0.5, 0.5, 0.5, 1),
            color=(1,1,1,1),
            font_size='12sp'
        )
        self.pulisci_btn.bind(on_press=self.pulisci_tutti)
        audio_layout.add_widget(self.pulisci_btn)
            
        main_layout.add_widget(audio_layout)
            
        # Area risultati
        self.risultati_text = TextInput(
            text='I risultati appariranno qui...',
            readonly=True,
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(0.8, 0.8, 0.8, 1),
            font_size='12sp',
            size_hint_y=0.29
        )
        main_layout.add_widget(self.risultati_text)
            
        return main_layout
    
    def crea_tab_transiti(self):
        """Crea il contenuto della tab Transiti"""
        layout = BoxLayout(orientation='vertical', padding=20, spacing=5)
        
        # Titolo
        title = Label(
            text='✨ TRANSITI GIORNALIERI',
            size_hint_y=0.08,
            font_size='20sp',
            color=(0.9, 0.7, 0.2, 1)
        )
        layout.add_widget(title)
        
        # Info soggetto corrente
        self.soggetto_label = Label(
            text='Nessun soggetto selezionato',
            size_hint_y=0.05,
            color=(0.8, 0.8, 0.8, 1)
        )
        layout.add_widget(self.soggetto_label)
        
        # Selezione data
        data_layout = BoxLayout(size_hint_y=0.08, spacing=5)
        data_layout.add_widget(Label(text='Data:', color=(1,1,1,1)))
        
        self.transiti_data_input = TextInput(
            text=datetime.now().strftime('%d/%m/%Y'),
            multiline=False
        )
        data_layout.add_widget(self.transiti_data_input)
        
        self.calcola_transiti_btn = Button(
            text='🔮 Calcola Transiti',
            background_color=(0.3, 0.5, 0.9, 1),
            color=(1,1,1,1)
        )
        self.calcola_transiti_btn.bind(on_press=self.calcola_transiti)
        data_layout.add_widget(self.calcola_transiti_btn)
        
        layout.add_widget(data_layout)
        
        # Lista transiti
        layout.add_widget(Label(
            text='Transiti più significativi:',
            size_hint_y=0.04,
            color=(0.8, 0.8, 0.8, 1)
        ))
        
        self.transiti_list = ScrollView(size_hint_y=0.3)
        self.transiti_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=2,
            padding=2
        )
        self.transiti_container.bind(minimum_height=self.transiti_container.setter('height'))
        self.transiti_list.add_widget(self.transiti_container)
        layout.add_widget(self.transiti_list)
        
        # Area dettaglio
        layout.add_widget(Label(
            text='Dettaglio transito:',
            size_hint_y=0.04,
            color=(0.8, 0.8, 0.8, 1)
        ))
        
        self.transiti_dettaglio = TextInput(
            text='Clicca su un transito per vedere i dettagli...',
            readonly=True,
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(0.8, 0.8, 0.8, 1),
            size_hint_y=0.41
        )
        layout.add_widget(self.transiti_dettaglio)
        
        return layout
    
    def cerca_luogo(self, instance):
        luogo = self.luogo_input.text.strip()
        if not luogo:
            self.risultati_text.text = "❌ Inserisci un luogo da cercare"
            return
        
        self.risultati_text.text = f"⏳ Cerco {luogo}..."
        thread = threading.Thread(target=self._cerca_coordinate, args=(luogo,))
        thread.daemon = True
        thread.start()
    
    def _cerca_coordinate(self, luogo):
        try:
            geolocator = Nominatim(user_agent="astro_app")
            location = geolocator.geocode(luogo)
            
            if location:
                lat = location.latitude
                lon = location.longitude
                tf = TimezoneFinder()
                timezone_str = tf.timezone_at(lat=lat, lng=lon)
                Clock.schedule_once(lambda dt: self._aggiorna_coordinate(lat, lon, timezone_str, location.address))
            else:
                Clock.schedule_once(lambda dt: self._mostra_errore_luogo(f"Luogo '{luogo}' non trovato"))
        except Exception as e:
            Clock.schedule_once(lambda dt: self._mostra_errore_luogo(f"Errore: {str(e)}"))
    
    def _aggiorna_coordinate(self, lat, lon, timezone_str, indirizzo):
        self.lat_input.text = f"{lat:.6f}"
        self.lon_input.text = f"{lon:.6f}"
        
        if "Italy" in indirizzo or "Italia" in indirizzo:
            timezone_str = "Europe/Rome"
        
        if not timezone_str:
            timezone_str = "Europe/Rome"
        
        self.risultati_text.text = f"✅ Trovato: {indirizzo}\nLat: {lat:.6f}, Lon: {lon:.6f}\nFuso: {timezone_str}"
        self.fuso_corrente = timezone_str
    
    def _mostra_errore_luogo(self, messaggio):
        self.risultati_text.text = f"❌ {messaggio}"
    
    def pulisci_campo(self, instance):
        instance.text = ""
    
    def pulisci_tutti(self, instance):
        self.nome_input.text = ""
        self.data_input.text = ""
        self.ora_input.text = ""
        self.luogo_input.text = ""
        self.lat_input.text = ""
        self.lon_input.text = ""
        self.risultati_text.text = "Campi puliti. Inserisci nuovi dati."
    
    def calcola_profilo(self, instance):
        try:
            self.risultati_text.text = "⏳ Calcolo in corso..."
            Clock.tick()
            
            data = self.data_input.text
            ora = self.ora_input.text
            luogo = self.luogo_input.text
            
            try:
                lat = float(self.lat_input.text)
                lon = float(self.lon_input.text)
            except:
                self.risultati_text.text = "❌ Errore: lat/lon non valide"
                return
            
            try:
                gg, mm, aaaa = data.split('/')
                data_iso = f"{aaaa}-{mm}-{gg}"
            except:
                self.risultati_text.text = "❌ Errore: formato data (usa GG/MM/AAAA)"
                return
            
            fuso_da_usare = getattr(self, 'fuso_corrente', 'Europe/Rome')
            
            # Salva i dati per i transiti
            posizioni, cusps, ascendente, mc = calcola_posizioni_e_case(
                data_iso, ora, lat, lon, fuso_da_usare
            )
            
            self.soggetto_corrente = {
                'nome': self.nome_input.text,
                'data_nascita': data_iso,
                'ora_nascita': ora,
                'luogo': luogo,
                'lat': lat,
                'lon': lon,
                'fuso': fuso_da_usare,
                'dati_natali': {
                    'posizioni': posizioni,
                    'cusps': list(cusps),
                    'ascendente': ascendente,
                    'mc': mc
                }
            }
            
            # Aggiorna label nella tab transiti
            self.soggetto_label.text = f"Soggetto: {self.nome_input.text}"
            
            # Calcola il profilo testuale
            risultato = genera_profilo_caratteriale(
                data_iso, ora, luogo, lat, lon, fuso_da_usare
            )
            
            self.risultati_text.text = risultato
            self.ultimo_risultato = risultato
            self.risultati_text.do_cursor_movement('cursor_end')
            
        except Exception as e:
            self.risultati_text.text = f"❌ Errore: {str(e)}"
            import traceback
            traceback.print_exc()
    
    def calcola_previsione(self, instance):
        self.risultati_text.text = "⏳ Funzione PREVISIONE in sviluppo..."
    
    def salva_audio_ultimo(self, instance):
        if hasattr(self, 'ultimo_risultato'):
            self.salva_audio(self.ultimo_risultato, "profilo_audio.mp3")
        else:
            self.risultati_text.text = "⚠️ Prima calcola un profilo!"
    
    def salva_audio(self, testo, nome_file="profilo_audio.mp3"):
        try:
            from gtts import gTTS
            tts = gTTS(text=testo[:500], lang='it', slow=False)
            tts.save(nome_file)
            self.risultati_text.text += f"\n\n✅ Audio salvato: {nome_file}"
        except Exception as e:
            self.risultati_text.text += f"\n\n❌ Errore audio: {e}"
    
    def salva_soggetto(self, instance):
        if not self.soggetto_corrente:
            self.risultati_text.text = "❌ Nessun soggetto da salvare"
            return
        
        # 🔴 CONVERTI LA DATA IN FORMATO ISO 🔴
        data_input = self.data_input.text
        try:
            # Converte da GG/MM/AAAA a AAAA-MM-GG
            gg, mm, aaaa = data_input.split('/')
            data_iso = f"{aaaa}-{mm}-{gg}"
        except:
            data_iso = data_input  # se già in ISO
        
        # Aggiorna il soggetto con i dati attuali dei campi
        self.soggetto_corrente['nome'] = self.nome_input.text
        self.soggetto_corrente['data_nascita'] = data_iso  # <-- usa formato ISO
        self.soggetto_corrente['ora_nascita'] = self.ora_input.text
        self.soggetto_corrente['luogo'] = self.luogo_input.text
        self.soggetto_corrente['lat'] = float(self.lat_input.text) if self.lat_input.text else 0
        self.soggetto_corrente['lon'] = float(self.lon_input.text) if self.lon_input.text else 0
        
        # DEBUG
        print(f"🔍 Salvataggio: {self.soggetto_corrente.get('nome')}")
        print(f"   Data: {self.soggetto_corrente.get('data_nascita')}")
        print(f"   Ora: {self.soggetto_corrente.get('ora_nascita')}")
        
        if self.db.salva_soggetto(self.soggetto_corrente):
            self.risultati_text.text = f"✅ Soggetto {self.soggetto_corrente['nome']} salvato!"
        else:
            self.risultati_text.text = "❌ Errore durante il salvataggio"
    
    def mostra_lista_soggetti(self, instance):
        soggetti = self.db.carica_soggetti()
        if not soggetti:
            self.risultati_text.text = "❌ Nessun soggetto salvato"
            return
        
        # Crea popup con lista
        content = BoxLayout(orientation='vertical', spacing=5, padding=10)
        
        for s in soggetti:
            btn = Button(
                text=s['nome'],
                size_hint_y=None,
                height=40,
                background_color=(0.3, 0.5, 0.7, 1)
            )
            btn.soggetto = s
            btn.bind(on_press=self.carica_soggetto_selezionato)
            content.add_widget(btn)
        
        btn_chiudi = Button(text='Chiudi', size_hint_y=None, height=40)
        content.add_widget(btn_chiudi)
        
        popup = Popup(title='Seleziona Soggetto', content=content, size_hint=(0.8, 0.8))
        btn_chiudi.bind(on_press=popup.dismiss)
        
        for btn in content.children[:-1]:  # Esclude il pulsante chiudi
            btn.bind(on_press=popup.dismiss)
        
        self.popup_soggetti = popup
        popup.open()
    
    def carica_soggetto_selezionato(self, instance):
        s = instance.soggetto
        
        self.nome_input.text = s.get('nome', '')
        if 'data_nascita' in s:
            data_str = s['data_nascita']
            # Se è in formato ISO, converti in GG/MM/AAAA per visualizzare
            if '-' in data_str:
                aaaa, mm, gg = data_str.split('-')
                data_display = f"{gg}/{mm}/{aaaa}"
            else:
                data_display = data_str
            self.data_input.text = data_display
        
        self.ora_input.text = s.get('ora_nascita', '')
        self.luogo_input.text = s.get('luogo', '')
        self.lat_input.text = str(s.get('lat', 0))
        self.lon_input.text = str(s.get('lon', 0))
        
        # Usa i dati natali salvati
        self.soggetto_corrente = s
        
        self.soggetto_label.text = f"Soggetto: {s['nome']}"
        self.risultati_text.text = f"✅ Soggetto {s['nome']} caricato"
    
    def calcola_transiti(self, instance):
        """Calcola i transiti per la data selezionata"""
        try:
            # Verifica se abbiamo un soggetto
            if not hasattr(self, 'soggetto_corrente') or not self.soggetto_corrente:
                self.transiti_dettaglio.text = "❌ Seleziona prima un soggetto nella tab Profilo"
                return
            
            data = self.transiti_data_input.text
            
            try:
                gg, mm, aaaa = data.split('/')
                data_iso = f"{aaaa}-{mm}-{gg}"
            except:
                self.transiti_dettaglio.text = "❌ Formato data non valido (usa GG/MM/AAAA)"
                return
            
            # ============================================
            # GESTIONE ABBONAMENTO
            # ============================================
            abbonamento = 'gratuito'
            if hasattr(self, 'utente_abbonamento'):
                abbonamento = self.utente_abbonamento

            # 🔴 FORZA PER TEST (poi rimuovere) 🔴
            abbonamento = 'settimanale'

            print(f"📱 Versione: {abbonamento.upper()}")
            
            # Verifica che i dati natali esistano
            if 'dati_natali' not in self.soggetto_corrente or not self.soggetto_corrente['dati_natali']:
                self.transiti_dettaglio.text = "❌ Dati natali non disponibili. Ricalcola il tema natale."
                return
            
            # ⭐ CREA IL CALCOLATORE ⭐
            self.calcolatore_transiti = CalcolatoreTransiti(
                self.soggetto_corrente['dati_natali'],
                abbonamento=abbonamento
            )

            # 🔍 STAMPA LE CUSPIDI CARICATE (DEBUG)
            print("🔍 CUSPIDI NEL CALCOLATORE:")
            for i, c in enumerate(self.soggetto_corrente['dati_natali']['cusps']):
                print(f"   Casa {i+1}: {c:.1f}° -> {self.calcolatore_transiti.get_segno_da_grado(c)}")
            
            # SEMPRE: calcola i transiti della Luna
            transiti = self.calcolatore_transiti.calcola_transiti_giornalieri(data_iso)
            print(f"🔍 Transiti Luna trovati: {len(transiti)}")

            # Per versioni a pagamento: calcola anche le configurazioni e i transiti dei pianeti
            if abbonamento in ['settimanale', 'mensile', 'annuale']:
                print("🔍 Calcolo configurazioni planetarie...")
                
                # Calcola le configurazioni (gruppi di pianeti)
                configurazioni = self.calcolatore_transiti.calcola_configurazioni_giornaliere(data_iso)
                print(f"🔍 Configurazioni trovate: {len(configurazioni)}")
                
                # Calcola i transiti singoli degli altri pianeti
                print("🔍 Calcolo transiti singoli pianeti...")
                transiti_pianeti = self.calcolatore_transiti.calcola_transiti_pianeti_giornalieri(data_iso)
                print(f"🔍 Transiti pianeti trovati: {len(transiti_pianeti)}")
                
                # Unisci i transiti
                if transiti_pianeti:
                    transiti.extend(transiti_pianeti)
                    print(f"🔍 Totale transiti dopo unione: {len(transiti)}")
                
                # Mostra tutto
                self.mostra_giornata_completa(transiti, data_iso, configurazioni=configurazioni)
                
            else:
                # Versione gratuita: solo Luna
                print("🔍 Versione gratuita: solo transiti Luna")
                self.mostra_giornata_completa(transiti, data_iso)
                
        except Exception as e:
            self.transiti_dettaglio.text = f"❌ Errore: {str(e)}"
            import traceback
            traceback.print_exc()

    def mostra_giornata_completa(self, transiti, data_transito, configurazioni=None):
        """
        Mostra i transiti UNA VOLTA per tutta la giornata,
        nella fascia in cui iniziano, con l'ora di inizio
        Se configurazioni è fornito, include anche le configurazioni planetarie
        """
        if not transiti and not configurazioni:
            self.transiti_dettaglio.text = "🌙 Nessun transito significativo oggi"
            return
        
        # ============================================
        # FUNZIONE DI CONVERSIONE ORA
        # ============================================
        def ora_a_decimali(ora_str):
            """Converte "HH:MM" in ore decimali (es. "00:00" → 0.0, "23:55" → 23.9167)"""
            try:
                ore, minuti = map(int, ora_str.split(':'))
                return ore + minuti / 60
            except:
                return 0
        
        # Ordina per ora (se ci sono transiti)
        if transiti:
            transiti_ordinati = sorted(transiti, key=lambda x: x.ora)
        else:
            transiti_ordinati = []
        
        # Raccogliamo solo la prima occorrenza di ogni tipo di transito
        transiti_unici = []
        visti = set()
        
        for t in transiti_ordinati:
            if t.pianeta_natale is None:
                continue
            # Includi il pianeta_transito nella chiave per distinguere Sole, Mercurio, ecc.
            chiave = f"{t.pianeta_transito}_{t.pianeta_natale}_{t.aspetto}"
            if chiave not in visti:
                visti.add(chiave)
                transiti_unici.append(t)
        
        # ============================================
        # FILTRO CONFIGURAZIONI: rimuovi i duplicati
        # ============================================
        if configurazioni:
            config_uniche = {}
            for c in configurazioni:
                pianeti_ordinati = sorted(c['pianeti'])
                chiave = f"{','.join(pianeti_ordinati)}_{c['radix']}"
                if chiave not in config_uniche:
                    config_uniche[chiave] = c
            configurazioni = list(config_uniche.values())
            print(f"🔍 Configurazioni uniche dopo filtro: {len(configurazioni)}")
        
        # Raggruppa per fascia oraria
        fascie = {
            'notte': {'inizio': 0, 'fine': 6, 'emoji': '🌙', 'titolo': 'NOTTE (00:00 - 06:00)', 'transiti': [], 'configurazioni': []},
            'primo_mattino': {'inizio': 6, 'fine': 9, 'emoji': '🌅', 'titolo': 'PRIMO MATTINO (06:00 - 09:00)', 'transiti': [], 'configurazioni': []},
            'mattinata': {'inizio': 9, 'fine': 11, 'emoji': '☀️', 'titolo': 'MATTINATA (09:00 - 11:00)', 'transiti': [], 'configurazioni': []},
            'tarda_mattinata': {'inizio': 11, 'fine': 13, 'emoji': '☀️', 'titolo': 'TARDA MATTINATA (11:00 - 13:00)', 'transiti': [], 'configurazioni': []},
            'primo_pomeriggio': {'inizio': 13, 'fine': 15, 'emoji': '⛅', 'titolo': 'PRIMO POMERIGGIO (13:00 - 15:00)', 'transiti': [], 'configurazioni': []},
            'pomeriggio': {'inizio': 15, 'fine': 18, 'emoji': '⛅', 'titolo': 'POMERIGGIO (15:00 - 18:00)', 'transiti': [], 'configurazioni': []},
            'tardo_pomeriggio': {'inizio': 18, 'fine': 20, 'emoji': '🌆', 'titolo': 'TARDO POMERIGGIO (18:00 - 20:00)', 'transiti': [], 'configurazioni': []},
            'sera': {'inizio': 20, 'fine': 24, 'emoji': '🌙', 'titolo': 'SERA (20:00 - 24:00)', 'transiti': [], 'configurazioni': []}
        }
        
        # Distribuisci i transiti
        for t in transiti_unici:
            ora = t.ora
            for fascia, dati in fascie.items():
                if dati['inizio'] <= ora < dati['fine']:
                    dati['transiti'].append(t)
                    break
        
        # Distribuisci le configurazioni
        if configurazioni:
            for c in configurazioni:
                ora_dec = ora_a_decimali(c['ora'])
                for fascia, dati in fascie.items():
                    if dati['inizio'] <= ora_dec < dati['fine']:
                        dati['configurazioni'].append(c)
                        break
        
        # Converti data_transito in oggetto datetime
        data_obj = datetime.strptime(data_transito, "%Y-%m-%d")
        testo = f"🌅 BUONGIORNO! {data_obj.strftime('%d %B %Y')}\n\n"
        
        for fascia, dati in fascie.items():
            if dati['transiti'] or (configurazioni and dati['configurazioni']):
                testo += f"{dati['emoji']} {dati['titolo']}\n"
                
                # PRIMA LE CONFIGURAZIONI
                if configurazioni and dati['configurazioni']:
                    dati['configurazioni'].sort(key=lambda x: ora_a_decimali(x['ora']))
                    
                    for c in dati['configurazioni']:
                        ora_str = c['ora']
                        
                        # Emoji in base al tipo
                        if c['tipo'] == 'armonico':
                            emoji = "✨"
                            tipo = "ARMONICA"
                        else:
                            emoji = "⚠️"
                            tipo = "TESA"
                        
                        testo += f"\n   {emoji} CONFIGURAZIONE {tipo} ({c['num_pianeti']} pianeti)\n"
                        testo += f"      Attiva il tuo {c['radix']} (verso le {ora_str})\n"
                        testo += f"      Pianeti: {', '.join(c['pianeti'])}\n"
                        testo += f"      Punto medio: {c['punto_medio']:.2f}° (diff: {c['diff']:.3f}°)\n\n"
                
                # POI I TRANSITI
                for t in dati['transiti']:
                    print(f"🔍 DEBUG MOSTRA: {t.pianeta_transito} - ora_esatta={t.ora_esatta}, ora={t.ora}")
                    msg_confort = self.calcolatore_transiti.genera_messaggio_confortevole(t)
                    
                    if msg_confort:
                        ore = int(t.ora)
                        minuti = int((t.ora - ore) * 60)
                        ora_str = f"{ore:02d}:{minuti:02d}"
                        
                        linee = msg_confort.strip().split('\n')
                        titolo = linee[0]
                        
                        testo += f"\n   {titolo} (dalle {ora_str})\n"
                        testo += "\n".join(linee[1:]) + "\n\n"
                
                testo += "\n"
        
        self.transiti_dettaglio.text = testo

    def mostra_giornata_completa_con_cluster(self, transiti, cluster):
        """
        Mostra i transiti della Luna e i cluster planetari
        organizzati per fasce orarie
        """
        if not transiti and not cluster:
            self.transiti_dettaglio.text = "🌙 Oggi non ci sono momenti particolarmente significativi."
            return
        
        # ============================================
        # 1. PREPARAZIONE DATI
        # ============================================
        
        # Ordina transiti per ora
        if transiti:
            transiti_ordinati = sorted(transiti, key=lambda x: x.ora)
        else:
            transiti_ordinati = []
        
        # Raccogliamo solo la prima occorrenza di ogni tipo di transito Luna
        transiti_unici = []
        visti = set()
        
        for t in transiti_ordinati:
            if t.pianeta_natale is None:
                continue
            chiave = f"{t.pianeta_natale}_{t.aspetto}"
            if chiave not in visti:
                visti.add(chiave)
                transiti_unici.append(t)
        
        # ============================================
        # 2. FASCE ORARIE (stesse della versione free)
        # ============================================
        fascie = {
            'notte': {'inizio': 0, 'fine': 6, 'emoji': '🌙', 'titolo': 'NOTTE (00:00 - 06:00)', 'transiti': [], 'cluster': []},
            'primo_mattino': {'inizio': 6, 'fine': 9, 'emoji': '🌅', 'titolo': 'PRIMO MATTINO (06:00 - 09:00)', 'transiti': [], 'cluster': []},
            'mattinata': {'inizio': 9, 'fine': 11, 'emoji': '☀️', 'titolo': 'MATTINATA (09:00 - 11:00)', 'transiti': [], 'cluster': []},
            'tarda_mattinata': {'inizio': 11, 'fine': 13, 'emoji': '☀️', 'titolo': 'TARDA MATTINATA (11:00 - 13:00)', 'transiti': [], 'cluster': []},
            'primo_pomeriggio': {'inizio': 13, 'fine': 15, 'emoji': '⛅', 'titolo': 'PRIMO POMERIGGIO (13:00 - 15:00)', 'transiti': [], 'cluster': []},
            'pomeriggio': {'inizio': 15, 'fine': 18, 'emoji': '⛅', 'titolo': 'POMERIGGIO (15:00 - 18:00)', 'transiti': [], 'cluster': []},
            'tardo_pomeriggio': {'inizio': 18, 'fine': 20, 'emoji': '🌆', 'titolo': 'TARDO POMERIGGIO (18:00 - 20:00)', 'transiti': [], 'cluster': []},
            'sera': {'inizio': 20, 'fine': 24, 'emoji': '🌙', 'titolo': 'SERA (20:00 - 24:00)', 'transiti': [], 'cluster': []}
        }
        
        # Distribuisci transiti Luna
        for t in transiti_unici:
            ora = t.ora
            for fascia, dati in fascie.items():
                if dati['inizio'] <= ora < dati['fine']:
                    dati['transiti'].append(t)
                    break
        
        # Distribuisci cluster
        if cluster:
            for c in cluster:
                ora = c['ora']
                for fascia, dati in fascie.items():
                    if dati['inizio'] <= ora < dati['fine']:
                        dati['cluster'].append(c)
                        break
        
        # ============================================
        # 3. GENERAZIONE REPORT
        # ============================================
        testo = f"🌅 BUONGIORNO! {datetime.now().strftime('%d %B %Y')}\n\n"
        
        for fascia, dati in fascie.items():
            if dati['transiti'] or dati['cluster']:
                testo += f"{dati['emoji']} {dati['titolo']}\n"
                
                # PRIMA I CLUSTER (eventi più importanti)
                for c in dati['cluster']:
                    ora = c['ora']
                    ore = int(ora)
                    minuti = int((ora - ore) * 60)
                    ora_str = f"{ore:02d}:{minuti:02d}"
                    
                    # Determina emoji in base al tipo
                    if c.get('tipo_cluster') == 'armonico':
                        emoji = "✨"
                        tipo = "ARMONICA"
                    elif c.get('tipo_cluster') == 'disarmonico':
                        emoji = "⚠️"
                        tipo = "TESA"
                    else:
                        emoji = "🔄"
                        tipo = "MISTA"
                    
                    # Nome del radix attivato
                    radix = c.get('radix', 'punto sensibile')
                    
                    testo += f"\n   {emoji} CONFIGURAZIONE PLANETARIA {tipo}\n"
                    testo += f"      📍 Attiva il tuo {radix}\n"
                    
                    # Pianeti coinvolti
                    if 'pianeti_cluster' in c and c['pianeti_cluster']:
                        pianeti = ', '.join(c['pianeti_cluster'])
                        testo += f"      🪐 Pianeti: {pianeti}\n"
                    
                    # Ora di massima potenza
                    testo += f"      ⏰ Massima potenza alle {ora_str}\n"
                    
                    # Durata
                    if 'durata' in c and c['durata'] > 0.5:
                        testo += f"      ⏱️ Durata: {c['durata']:.1f} ore\n"
                    
                    testo += "\n"
                
                # POI I TRANSITI DELLA LUNA (come nella versione free)
                for t in dati['transiti']:
                    msg_confort = self.calcolatore_transiti.genera_messaggio_confortevole(t)
                    
                    if msg_confort:
                        ore = int(t.ora)
                        minuti = int((t.ora - ore) * 60)
                        ora_str = f"{ore:02d}:{minuti:02d}"
                        
                        linee = msg_confort.strip().split('\n')
                        titolo = linee[0]
                        
                        if t.aspetto == 'TRANSITO' and self._dura_tutto_il_giorno(t, transiti):
                            testo += f"   {titolo} (per tutto il giorno)\n"
                        else:
                            testo += f"   {titolo} (dalle {ora_str})\n"
                        
                        testo += "\n".join(linee[1:]) + "\n\n"
                
                testo += "\n"
        
        self.transiti_dettaglio.text = testo    

    def _dura_tutto_il_giorno(self, transito, tutti_transiti):
        """Controlla se un transito (es. casa) dura tutto il giorno"""
        # Implementazione semplice: se è un TRANSITO e appare in più fasce
        if transito.aspetto != 'TRANSITO':
            return False
        
        conteggio = 0
        for t in tutti_transiti:
            if t.pianeta_natale == transito.pianeta_natale and t.aspetto == 'TRANSITO':
                conteggio += 1
                if conteggio > 5:  # Se appare più di 5 volte, probabilmente è tutto il giorno
                    return True
        return False
    
    
    
    def raccogli_eventi_luna(self, transiti):
        """
        Trasforma i transiti della Luna in una lista di eventi strutturati
        (invece di restituire direttamente il testo)
        """
        eventi_luna = []
        
        # Mappa descrittiva per i pianeti e le case
        descrizioni_pianeti = {
            'Sole': 'identità, vitalità', 'Luna': 'emozioni, sensibilità',
            'Mercurio': 'comunicazione, pensiero', 'Venere': 'amore, relazioni',
            'Marte': 'energia, azione', 'Giove': 'espansione, fortuna',
            'Saturno': 'responsabilità, disciplina', 'Urano': 'cambiamento, libertà',
            'Nettuno': 'intuizione, sogni', 'Plutone': 'trasformazione, potere'
        }
        
        descrizioni_case = {
            'Ascendente': 'la tua immagine', 'II': 'le tue risorse',
            'III': 'la comunicazione', 'FC': 'le tue radici',
            'V': 'la creatività', 'VI': 'il lavoro, la salute',
            'Discendente': 'le relazioni', 'VIII': 'le trasformazioni',
            'IX': 'i viaggi, gli studi', 'MC': 'la carriera',
            'XI': 'le amicizie', 'XII': 'la spiritualità'
        }
        
        for t in transiti:
            if t.pianeta_transito == 'Luna':
                # Determina la descrizione del punto radix
                if t.pianeta_natale in descrizioni_case:
                    descrizione = descrizioni_case[t.pianeta_natale]
                elif t.pianeta_natale in descrizioni_pianeti:
                    descrizione = f"il tuo {t.pianeta_natale}"
                else:
                    descrizione = t.pianeta_natale
                
                eventi_luna.append({
                    'ora': t.ora,
                    'radix': t.pianeta_natale,
                    'descrizione': descrizione,
                    'tipo': 'luna',
                    'aspetto': t.aspetto,
                    'casa': t.casa_natale,
                    'testo': t.fascia_oraria
                })
        
        return eventi_luna

    def genera_report_integrato(self, transiti, cluster):
        """
        Genera un report unico che unisce transiti della Luna e cluster
        organizzato per fasce orarie
        """
        
        # 1. Raccogli eventi strutturati da entrambe le fonti
        eventi_luna = self.raccogli_eventi_luna(transiti)
        
        # 2. UNISCI TUTTI GLI EVENTI
        tutti_eventi = []
        
        # Mappa descrittiva per i pianeti e le case (per i cluster)
        descrizioni_pianeti = {
            'Sole': 'identità, vitalità', 'Luna': 'emozioni, sensibilità',
            'Mercurio': 'comunicazione, pensiero', 'Venere': 'amore, relazioni',
            'Marte': 'energia, azione', 'Giove': 'espansione, fortuna',
            'Saturno': 'responsabilità, disciplina', 'Urano': 'cambiamento, libertà',
            'Nettuno': 'intuizione, sogni', 'Plutone': 'trasformazione, potere'
        }
        
        descrizioni_case = {
            'Ascendente': 'la tua immagine', 'II': 'le tue risorse',
            'III': 'la comunicazione', 'FC': 'le tue radici',
            'V': 'la creatività', 'VI': 'il lavoro, la salute',
            'Discendente': 'le relazioni', 'VIII': 'le trasformazioni',
            'IX': 'i viaggi, gli studi', 'MC': 'la carriera',
            'XI': 'le amicizie', 'XII': 'la spiritualità'
        }
        
        # Aggiungi eventi Luna
        for e in eventi_luna:
            tutti_eventi.append({
                'ora': e['ora'],
                'radix': e['radix'],
                'descrizione': e['descrizione'],
                'tipo_evento': 'luna',
                'aspetto': e['aspetto']
            })
        
        # Aggiungi eventi cluster
        for c in cluster:
            # Converti il nome del punto radix in descrizione
            if c['radix'] in descrizioni_case:
                descrizione = descrizioni_case[c['radix']]
            elif c['radix'] in descrizioni_pianeti:
                descrizione = f"il tuo {c['radix']} ({descrizioni_pianeti[c['radix']]})"
            else:
                descrizione = f"il tuo {c['radix']}"
            
            # Determina emoji in base al tipo
            if c['tipo_cluster'] == 'armonico':
                emoji = "✨"
            elif c['tipo_cluster'] == 'disarmonico':
                emoji = "⚠️"
            else:
                emoji = "🔄"
            
            tutti_eventi.append({
                'ora': c['ora'],
                'radix': c['radix'],
                'descrizione': descrizione,
                'tipo_evento': 'cluster',
                'tipo_cluster': c['tipo_cluster'],
                'emoji': emoji,
                'pianeti': c.get('pianeti', []),
                'durata': c.get('durata', 0.5)
            })
        
        # 3. Se non ci sono eventi
        if not tutti_eventi:
            return "🌙 Oggi non ci sono momenti particolarmente significativi."
        
        # 4. Ordina per ora
        tutti_eventi.sort(key=lambda x: x['ora'])
        
        # 5. RAGGRUPPA PER FASCIA ORARIA (ogni 2 ore)
        fascie = {
            '00-02': {'inizio': 0, 'fine': 2, 'eventi': [], 'radix_unici': set()},
            '02-04': {'inizio': 2, 'fine': 4, 'eventi': [], 'radix_unici': set()},
            '04-06': {'inizio': 4, 'fine': 6, 'eventi': [], 'radix_unici': set()},
            '06-08': {'inizio': 6, 'fine': 8, 'eventi': [], 'radix_unici': set()},
            '08-10': {'inizio': 8, 'fine': 10, 'eventi': [], 'radix_unici': set()},
            '10-12': {'inizio': 10, 'fine': 12, 'eventi': [], 'radix_unici': set()},
            '12-14': {'inizio': 12, 'fine': 14, 'eventi': [], 'radix_unici': set()},
            '14-16': {'inizio': 14, 'fine': 16, 'eventi': [], 'radix_unici': set()},
            '16-18': {'inizio': 16, 'fine': 18, 'eventi': [], 'radix_unici': set()},
            '18-20': {'inizio': 18, 'fine': 20, 'eventi': [], 'radix_unici': set()},
            '20-22': {'inizio': 20, 'fine': 22, 'eventi': [], 'radix_unici': set()},
            '22-24': {'inizio': 22, 'fine': 24, 'eventi': [], 'radix_unici': set()}
        }
        
        for e in tutti_eventi:
            ora = e['ora']
            for fascia, dati in fascie.items():
                if dati['inizio'] <= ora < dati['fine']:
                    dati['eventi'].append(e)
                    dati['radix_unici'].add(e['radix'])
                    break
        
        # 6. GENERA IL REPORT INTEGRATO
        report = "🌅 BUONGIORNO! Ecco i momenti chiave della giornata:\n\n"
        
        for fascia, dati in fascie.items():
            if not dati['eventi']:
                continue
            
            # Separa eventi per tipo in questa fascia
            eventi_luna_fascia = [e for e in dati['eventi'] if e['tipo_evento'] == 'luna']
            eventi_cluster_fascia = [e for e in dati['eventi'] if e['tipo_evento'] == 'cluster']
            
            # Determina l'emoji della fascia in base ai cluster presenti
            tipi_cluster = [e['tipo_cluster'] for e in eventi_cluster_fascia]
            
            if 'armonico' in tipi_cluster and 'disarmonico' in tipi_cluster:
                emoji_fascia = "🔄"
                effetto_fascia = "alternato"
            elif 'armonico' in tipi_cluster:
                emoji_fascia = "✨"
                effetto_fascia = "positivo"
            elif 'disarmonico' in tipi_cluster:
                emoji_fascia = "⚠️"
                effetto_fascia = "teso"
            else:
                # Solo eventi Luna
                emoji_fascia = "🌙"
                effetto_fascia = "lunare"
            
            # Raccogli tutte le aree attivate
            aree = list(dati['radix_unici'])
            
            if len(aree) == 1:
                area_testo = next(iter(aree))
            elif len(aree) == 2:
                area_testo = f"{list(aree)[0]} e {list(aree)[1]}"
            else:
                aree_lista = list(aree)
                area_testo = ", ".join(aree_lista[:-1]) + f" e {aree_lista[-1]}"
            
            # Trova l'ora più significativa
            ore_significative = sorted([e['ora'] for e in dati['eventi']])
            ora_media = sum(ore_significative) / len(ore_significative)
            ore = int(ora_media)
            minuti = int((ora_media - ore) * 60)
            ora_str = f"{ore:02d}:{minuti:02d}"
            
            report += f"{emoji_fascia} **Tra le {dati['inizio']:02d}:00 e le {dati['fine']:02d}:00** (momento chiave alle {ora_str})\n"
            report += f"   Periodo {effetto_fascia} per {area_testo}.\n"
            
            # Dettagli Luna
            if eventi_luna_fascia:
                report += f"   🌙 La Luna:\n"
                # Mostra i cambi di casa
                cambi_casa = [e for e in eventi_luna_fascia if e.get('aspetto') == 'TRANSITO']
                if cambi_casa:
                    report += f"      • Entra in {cambi_casa[0]['descrizione']}\n"
                
                # Mostra aspetti principali (max 3)
                aspetti_mostrati = 0
                for e in eventi_luna_fascia:
                    if e.get('aspetto') != 'TRANSITO' and aspetti_mostrati < 3:
                        report += f"      • {e['aspetto']} con {e['descrizione']}\n"
                        aspetti_mostrati += 1
            
            # Dettagli cluster
            if eventi_cluster_fascia:
                for e in eventi_cluster_fascia:
                    if e.get('durata', 0) > 1:
                        report += f"   {e['emoji']} Momento {e['tipo_cluster']} prolungato ({e['durata']:.1f} ore)\n"
                    else:
                        report += f"   {e['emoji']} Momento {e['tipo_cluster']} concentrato\n"
            
            # Suggerimento
            if 'armonico' in tipi_cluster and 'disarmonico' not in tipi_cluster:
                report += "   ✨ Approfitta per azioni importanti in queste aree.\n"
            elif 'disarmonico' in tipi_cluster and 'armonico' not in tipi_cluster:
                report += "   ⚠ Meglio evitare decisioni importanti in queste aree.\n"
            elif eventi_luna_fascia and not eventi_cluster_fascia:
                report += "   🌙 Segui il tuo umore, ma evita decisioni definitive.\n"
            else:
                report += "   🔄 Momenti alternati: ascolta il tuo intuito.\n"
            report += "\n"
        
        return report
    
    def mostra_dettaglio_transito(self, instance):
        """Mostra il dettaglio di un transito selezionato"""
        t = instance.transito
        
        # PROTEZIONE: se t è None o non ha pianeta_natale, esci
        if t is None or not hasattr(t, 'pianeta_natale') or t.pianeta_natale is None:
            self.transiti_dettaglio.text = "❌ Dettaglio non disponibile"
            return
        
        # Messaggio tecnico
        msg = self.calcolatore_transiti.genera_messaggio_tecnico(t)
        
        # Messaggio confortevole (con protezione)
        msg_confort = None
        if hasattr(self, 'calcolatore_transiti'):
            try:
                msg_confort = self.calcolatore_transiti.genera_messaggio_confortevole(t)
            except Exception as e:
                print(f"❌ Errore nel generare messaggio confortevole: {e}")
                msg_confort = None
        
        
        
        # Costruisci il dettaglio
        dettaglio = f"""
    ╔══════════════════════════════════════════════════════════╗
    ║                     🌙 TRANSITO DEL GIORNO               ║
    ╚══════════════════════════════════════════════════════════╝

    📅 DATA: {t.data}
    ⭐ TRANSITO: {t.pianeta_transito} in {t.aspetto} con {t.pianeta_natale}
    📏 ORBITA: {t.orbita:.1f}°
    🏠 CASA NATALE: {t.casa_natale} - {interpreta_casa(t.casa_natale)}
    ⚡ IMPORTANZA: {t.importanza}/10

    📝 INTERPRETAZIONE TECNICA:
    {msg}
    """
        
        # Se c'è un messaggio confortevole, lo aggiungiamo con un box speciale
        if msg_confort:
            dettaglio += f"""

    ╔══════════════════════════════════════════════════════════╗
    ║                 💖 LA TUA AMICA TI DICE                  ║
    ╚══════════════════════════════════════════════════════════╝

    {msg_confort}
    """
        
        self.transiti_dettaglio.text = dettaglio
    
    def genera_report_unico(self, transiti, intercettazioni):
        """
        Genera un report unico che unisce:
        - Transiti della Luna (quelli che già funzionano)
        - Intercettazioni dei cluster sui punti radix
        """
        
        # 1. Transiti della Luna (già funzionanti)
        testo_luna = self.mostra_giornata_completa(transiti)
        
        # 2. Se non ci sono intercettazioni, solo Luna
        if not intercettazioni:
            return testo_luna
        
        # 3. Costruisci sezione CLUSTER
        testo_cluster = "\n\n✨ MOMENTI DI MASSIMA ENERGIA:\n\n"
        
        for c in intercettazioni:
            ora = c['ora']
            ore = int(ora)
            minuti = int((ora - ore) * 60)
            ora_str = f"{ore:02d}:{minuti:02d}"
            
            # Determina fascia oraria (per contesto)
            if 0 <= ora < 6:
                fascia = "nella notte"
            elif 6 <= ora < 12:
                fascia = "nel mattino"
            elif 12 <= ora < 18:
                fascia = "nel pomeriggio"
            else:
                fascia = "in serata"
            
            # Emoji in base all'effetto
            if c['tipo_effetto'] == 'armonico':
                emoji = "✨"
                suggerimento = "Approfitta per azioni importanti in queste aree."
            elif c['tipo_effetto'] == 'disarmonico':
                emoji = "⚠️"
                suggerimento = "Meglio evitare decisioni importanti in queste aree."
            else:
                emoji = "🔄"
                suggerimento = "Momento alternato: ascolta il tuo intuito."
            
            # Testo principale
            testo_cluster += f"{emoji} **{fascia} (verso le {ora_str})**\n"
            testo_cluster += f"   Periodo {c['tipo_effetto']} per il tuo {c['radix']}.\n"
            testo_cluster += f"   {suggerimento}\n\n"
        
        # 4. Unisci
        return testo_luna + testo_cluster

    def _dura_tutto_il_giorno(self, transito, tutti_transiti):
        """Controlla se un transito (es. casa) dura tutto il giorno"""
        # Implementazione semplice: se è un TRANSITO e appare in più fasce
        if transito.aspetto != 'TRANSITO':
            return False
        
        conteggio = 0
        for t in tutti_transiti:
            if t.pianeta_natale == transito.pianeta_natale and t.aspetto == 'TRANSITO':
                conteggio += 1
                if conteggio > 5:  # Se appare più di 5 volte, probabilmente è tutto il giorno
                    return True
        return False

    def _dura_tutto_il_giorno(self, transito, tutti_transiti):
        """Controlla se un transito (es. casa) dura tutto il giorno"""
        # Implementazione semplice: se è un TRANSITO e appare in più fasce
        if transito.aspetto != 'TRANSITO':
            return False
        
        conteggio = 0
        for t in tutti_transiti:
            if t.pianeta_natale == transito.pianeta_natale and t.aspetto == 'TRANSITO':
                conteggio += 1
                if conteggio > 5:  # Se appare più di 5 volte, probabilmente è tutto il giorno
                    return True
        return False

if __name__ == '__main__':
    AstroApp().run()

