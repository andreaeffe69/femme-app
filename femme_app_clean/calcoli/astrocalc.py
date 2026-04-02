"""
Modulo di calcolo astrologico per app mobile
Versione completa con case, aspetti, potenze e sezione Donna
"""

import swisseph as swe
import datetime
import math
from datetime import datetime, timedelta
import pytz  # <--- AGGIUNGI QUESTA RIGA

# Configurazione effemeridi
swe.set_ephe_path('')

# ============================================
# CLASSE CALCOLATORE ASPETTI TRADIZIONALI
# ============================================

class CalcolatoreAspettiTradizionali:
    def __init__(self):
        self.soglia_congiunzione = 7
        self.aspetti = [
            {"nome": "Semisestile", "gradi": 30, "tolleranza": 3, "tipo": "+", "peso": 1},
            {"nome": "Sestile", "gradi": 60, "tolleranza": 5, "tipo": "+", "peso": 2},
            {"nome": "Trigono", "gradi": 120, "tolleranza": 7, "tipo": "+", "peso": 3},
            {"nome": "Semiquadrato", "gradi": 45, "tolleranza": 3, "tipo": "-", "peso": -1},
            {"nome": "Quadrato", "gradi": 90, "tolleranza": 7, "tipo": "-", "peso": -3},
            {"nome": "Sesquiquadrato", "gradi": 135, "tolleranza": 3, "tipo": "-", "peso": -1},
            {"nome": "Quinconce", "gradi": 150, "tolleranza": 3, "tipo": "-", "peso": -1},
            {"nome": "Congiunzione", "gradi": 0, "tolleranza": 7, "tipo": "N", "peso": 5}
        ]
        
        self.potenze_pianeti = {
            "Sole": 30, "Luna": 5, "Mercurio": 10, "Venere": 10, "Marte": 10,
            "Giove": 10, "Saturno": 10, "Urano": 10, "Nettuno": 10, "Plutone": 10
        }
        
        self.potenze_case = {
            "Ascendente": 20, "II": 15, "III": 10, "FC": 10, "V": 10, "VI": 10,
            "Discendente": 10, "VIII": 15, "IX": 10, "MC": 20, "XI": 10, "XII": 10
        }
        
        self.domicili = {
            "Ariete": ["Marte"], "Toro": ["Venere"], "Gemelli": ["Mercurio"],
            "Cancro": ["Luna"], "Leone": ["Sole"], "Vergine": ["Mercurio"],
            "Bilancia": ["Venere"], "Scorpione": ["Plutone", "Marte"],
            "Sagittario": ["Giove"], "Capricorno": ["Saturno"],
            "Acquario": ["Urano", "Saturno"], "Pesci": ["Nettuno", "Giove"]
        }
        
        self.esaltazioni = {
            "Ariete": ["Sole"], "Toro": ["Luna"], "Cancro": ["Giove", "Nettuno"],
            "Vergine": ["Mercurio"], "Bilancia": ["Saturno"],
            "Scorpione": ["Urano"], "Capricorno": ["Marte"], "Pesci": ["Venere"]
        }
        
        self.case_naturali = {
            "Ascendente": "Ariete", "II": "Toro", "III": "Gemelli", "FC": "Cancro",
            "V": "Leone", "VI": "Vergine", "Discendente": "Bilancia", "VIII": "Scorpione",
            "IX": "Sagittario", "MC": "Capricorno", "XI": "Acquario", "XII": "Pesci"
        }
        
        # ============================================
        # DATABASE 1: NATURA DEI PIANETI
        # ============================================
        self.natura_pianeti = {
            'Sole': {
                'nome': 'Sole',
                'simbolismo': "Il Sole è il centro del tema natale, come il bambino che cresce e matura attraverso le esperienze. Rappresenta il mondo dell'io, il pensiero cosciente, la volontà e l'immagine che abbiamo di noi stessi. Corrisponde al modello di io al quale cerchiamo di conformarci, sostituendo il narcisismo dell'infanzia. Rappresenta la figura del padre, con la quale possiamo identificarci più o meno felicemente.",
                'positivo': "Il Sole ci fornisce l'impulso a vivere e a creare, donandoci uno spirito brillante e una sana volontà di affermazione. Ci aiuta a esprimere la nostra personalità e i nostri desideri in modo autentico.",
                'negativo': "In eccesso, può manifestarsi come una tendenza a distruggere gli altri o a essere troppo esigenti. Apre la strada a impulsi che possono essere soddisfatti senza tenere conto dei danni che provocano.",
                'parole_chiave': ['identità', 'ego', 'vitalità', 'padre', 'volontà', 'coscienza', 'narcisismo', 'creatività']
            },
            'Luna': {
                'nome': 'Luna',
                'simbolismo': "La Luna rappresenta la nostra parte di femminilità, sia negli uomini che nelle donne. Riunisce tutte le sensazioni e gli impulsi accumulati dal tempo della vita intrauterina. Vulnerabile ed emotiva, è anche la madre, quella che ci protegge e ci infonde sicurezza. Dà forma al bambino, lo aiuta a crescere, modella il suo futuro. Influenza tutta la nostra vita, specialmente la sfera emotiva, circoscrivendo i nostri bisogni affettivi e lo stile di vita che ci conviene. Corrisponde al mondo dell'es: forze sconosciute, non dominabili, che spesso si esprimono con formule come 'non posso trattenermi da...', 'mi è sfuggito...', 'è più forte di me...'.",
                'positivo': "La Luna rappresenta la capacità di adattamento, l'intuizione, la fecondità, la creatività. Ci rende capaci di prevedere le tendenze e di riflettere nella mente il significato dei cicli che si chiudono e di quelli che iniziano.",
                'negativo': "Può portare instabilità emotiva, umoralità, volubilità, dipendenza affettiva. In eccesso, può creare confusione, fascino per l'occulto, passività di fronte a forze elementali, e un'eccessiva apertura all'inconscio collettivo o ai propri complessi personali.",
                'parole_chiave': ['emozioni', 'madre', 'istinto', 'sensibilità', 'inconscio', 'mutevolezza', 'fecondità', 'adattamento']
            },
            'Mercurio': {
                'nome': 'Mercurio',
                'simbolismo': "Mercurio è il messaggero degli dei, dio dei commercianti e dei ladri, protettore dei viaggiatori. Personifica la scaltrezza e l'abilità. È un trasformatore di energia, rappresenta l'intelligenza che ci permette di discernere, capire, classificare, nominare. Ci aiuta a prendere le distanze dal mondo dell'istinto, a intellettualizzare le sensazioni, a ragionare. Per mezzo del linguaggio, ci permette di adattarci alle regole sociali e di dare un nome alle nostre emozioni più profonde.",
                'positivo': "Stimola la comunicazione, suggerisce idee, ci rende adattabili, arrendevoli, comprensivi. Ci insegna a imparare, ci dà la capacità di condurre contrattazioni e realizzare compromessi. Ci permette di stabilire rapporti con gli altri.",
                'negativo': "Può portare a un attivismo eccessivo, a parlare senza dire niente, a errori di distrazione. In ambito morale, può indurre lassismo pur di ottenere vantaggi materiali. Le parole possono diventare armi taglienti, portando a nervosismo, aggressività, frivolezza.",
                'parole_chiave': ['comunicazione', 'intelligenza', 'linguaggio', 'adattabilità', 'scaltrezza', 'ragione', 'apprendimento']
            },
            'Venere': {
                'nome': 'Venere',
                'simbolismo': "Venere rappresenta la maniera in cui reagiamo nel campo affettivo. Può essere considerata la nostra parte femminile. Nell'uomo, indica il tipo di donna capace di sedurlo; nella donna, suggerisce in che modo sedurre, incantare e dar prova della propria femminilità. È il pianeta della socievolezza, del piacere, dell'amore, della sessualità, della gelosia e del possesso. Corrisponde al verbo amare coniugato in tutti i tempi. Rende armonioso tutto ciò che tocca, è il pianeta della felicità. Rappresenta l'amore in tutte le sue forme: amore delle cose belle, della cordialità, del piacere fisico. Corrisponde alla libido freudiana: pulsioni che ci mettono in contatto con oggetti e cose.",
                'positivo': "Favorisce gli scambi, gli incontri, la creatività. Dà una tonalità affettiva positiva a tutte le nostre azioni. Ci rende affascinanti, armoniosi, capaci di creare bellezza.",
                'negativo': "Può sciogliere legami, interrompere dialoghi. Enfatizza i nostri bisogni generando frustrazione e gelosia. Può inibire e frenare la creatività. Porta a desiderare senza amare o ad amare senza desiderare, creando disordine affettivo e instabilità.",
                'parole_chiave': ['amore', 'bellezza', 'armonia', 'seduzione', 'valori', 'piacere', 'affetti', 'sessualità']
            },
            'Marte': {
                'nome': 'Marte',
                'simbolismo': "Marte simboleggia l'energia vitale, spontanea, un'aggressività positiva che ci permette di lottare e vincere. Questa energia ci dà la forza di confrontarci col mondo. Ci fa conoscere il nostro io sociale e ci aiuta a realizzare i nostri desideri. Insieme a Venere, forma una coppia: Venere rappresenta ciò che desideriamo, Marte ci dà il mezzo per ottenerlo. Rappresenta l'azione, il coraggio, la determinazione, ma anche l'impulsività e il conflitto.",
                'positivo': "Dona energia, coraggio, spirito di iniziativa, determinazione. Ci permette di affrontare le sfide, di superare gli ostacoli, di realizzare i nostri progetti. Ci rende dinamici, entusiasti, vincenti.",
                'negativo': "Porta a eccessi di aggressività, impulsività, conflitti. Crea tensioni, insofferenza verso l'autorità, tendenza a seguire gli impulsi senza pensare. Può manifestarsi come violenza interiore mal controllata, temerarietà vana, blocchi di energia.",
                'parole_chiave': ['azione', 'energia', 'coraggio', 'conflitto', 'impulso', 'aggressività', 'determinazione', 'sfida']
            },
            'Giove': {
                'nome': 'Giove',
                'simbolismo': "Giove e Saturno formano una coppia complementare. Giove apporta entusiasmo, energia, espansione e generosità, sostenendoci nei periodi di rinuncia. È il pianeta della socievolezza, ci aiuta a crescere in funzione del nostro ambiente sociale, economico e culturale. Favorisce lo schiudersi e l'espandersi dell'individuo nel suo ambiente. Ci fornisce la volontà e l'ambizione per riuscire nella vita professionale, per ottenere l'approvazione altrui, per svolgere i ruoli sociali che si convengono alla nostra personalità. Conferisce la capacità di giudicare, di arbitrare tra le varie tendenze, di dominare i problemi.",
                'positivo': "Porta una ventata di ottimismo, possibilità di sviluppare la nostra originalità e migliorare il tenore di vita. Favorisce la fortuna, le opportunità, l'espansione in tutti i campi. Ci rende generosi, aperti, estroversi.",
                'negativo': "Può portare a sperpero di energia, egotismo, narcisismo, megalomania, bulimia. Porta a vivere al di sopra dei propri mezzi, a esagerare i meriti altrui, a lanciarsi in imprese troppo audaci. Crea contraddizione tra bisogno di libertà e obblighi, squilibrio tra entusiasmo e rendimento.",
                'parole_chiave': ['espansione', 'fortuna', 'ottimismo', 'abbondanza', 'generosità', 'ambizione', 'saggezza', 'crescita']
            },
            'Saturno': {
                'nome': 'Saturno',
                'simbolismo': "Saturno simboleggia il tempo, la severità, la realtà come costrizione. Rappresenta il padre che punisce e impone la realtà. Nemico di tutto ciò che è vago, indefinito, fantasioso, ci spinge alla riflessione e all'elaborazione razionale dei concetti. Ci insegna che la vita non è un romanzo e che non c'è successo senza lunga fatica. Non crede né al caso né alla fortuna, ma solo a ciò che viene metodicamente costruito. Corrisponde al super-io, alla struttura, alla tradizione culturale e sociale, all'influenza dell'autorità del padre e della legge. È il pianeta del tempo che ci costruisce, ci dà forma e ci insegna la pazienza.",
                'positivo': "Ci permette di verificare le nostre risorse interiori grazie alla maturità e alla padronanza. Ci aiuta a raggiungere obiettivi sociali e professionali. Ci dà realismo, capacità di concentrazione, serietà, disciplina. Ci insegna a conservare ciò che abbiamo acquisito.",
                'negativo': "Porta solitudine, rinuncia, frustrazione, senso di fallimento. Ci fa sentire limitati, indeboliti, schiacciati dal peso degli impegni. Può causare depressione, pessimismo, sensazione che il mondo ci respinga. Ci rende ostinati, rigidi, prigionieri di schemi obsoleti.",
                'parole_chiave': ['disciplina', 'tempo', 'responsabilità', 'limiti', 'struttura', 'maturità', 'pazienza', 'realtà']
            },
            'Urano': {
                'nome': 'Urano',
                'simbolismo': "Urano è rappresentato nel mito di Prometeo, che rubò il fuoco agli dei per donarlo agli uomini, permettendo loro di conquistare la libertà. Rappresenta la ribellione, l'originalità, l'indipendenza, la rottura con le tradizioni. Incarna lo spirito innovatore, la libertà di pensiero, l'anticonformismo.",
                'positivo': "Dona originalità, creatività, intuizione geniale, capacità di innovare. Porta cambiamenti positivi, improvvisi slanci di indipendenza, aperture mentali verso il nuovo. Stimola la ricerca, l'invenzione, la scoperta.",
                'negativo': "Crea ribellione fine a se stessa, provocazione, instabilità, imprevedibilità. Porta a decisioni improvvise e sconsiderate, a voler cambiare a tutti i costi senza costruire nulla di solido. Può causare tensioni nervose, insonnia, conflitti con l'autorità.",
                'parole_chiave': ['libertà', 'ribellione', 'originalità', 'cambiamento', 'innovazione', 'indipendenza', 'rottura']
            },
            'Nettuno': {
                'nome': 'Nettuno',
                'simbolismo': "Nettuno rappresenta il mondo dei sogni, delle illusioni, della spiritualità, dell'inconscio collettivo. Incarna l'ideale, la fusione mistica, la compassione, ma anche l'inganno, la confusione, l'evasione. Scioglie i confini, fonde le cose, rende tutto più sfumato e indefinito.",
                'positivo': "Dona sensibilità artistica, intuizione profonda, capacità di comprendere senza parole. Apre alla spiritualità, alla compassione, all'amore universale. Favorisce l'ispirazione creativa, la connessione con l'inconscio collettivo.",
                'negativo': "Porta confusione, illusione, autoinganno. Ci rende vittime di inganni, ci fa perdere il senso della realtà. Può causare dipendenze, evasioni pericolose, idealizzazione patologica degli altri. Crea nebbia mentale, incapacità di distinguere il vero dal falso.",
                'parole_chiave': ['sogno', 'illusione', 'spiritualità', 'intuizione', 'confusione', 'ideale', 'compassione']
            },
            'Plutone': {
                'nome': 'Plutone',
                'simbolismo': "Plutone rappresenta l'inconscio profondo, le pulsioni primordiali, la trasformazione radicale, la morte e la rinascita. Incarna il potere, la distruzione creativa, la capacità di andare a fondo delle cose. Corrisponde agli istinti più profondi, alle forze elementali che ci spingono a trasformarci o a perire.",
                'positivo': "Dona profondità, capacità di trasformazione, rigenerazione. Ci permette di andare alle radici dei problemi, di scavare fino alla verità. Ci dà potere personale, magnetismo, capacità di influenzare gli altri positivamente.",
                'negativo': "Porta ossessione, manipolazione, desiderio di potere distruttivo. Crea conflitti profondi, lotte di potere, gelosie estreme. Può causare angoscia, sentimenti di persecuzione, tendenza a controllare o a essere controllati.",
                'parole_chiave': ['trasformazione', 'potere', 'inconscio', 'morte-rinascita', 'profondità', 'intensità', 'rigenerazione']
            }
        }

        # ============================================
        # DATABASE 2: SEGNI SULLE CUSPIDI (dai nuovi file)
        # ============================================
        self.segni_sulle_cuspidi = {
            # I CASA (ASCENDENTE)
            1: {
                'Ariete': "energia, slancio vitale, esteriorizzazione, impulsività, coraggio. 'Si agisce per agire'.",
                'Toro': "perseverante, con il gusto del possesso, calmo, lento.",
                'Gemelli': "esteriorizzazione dell'attività mentale, nervoso, curioso, vuole le cose immediatamente.",
                'Cancro': "influenza della Luna sull'IO. Segnato dalla madre, la famiglia, l'eredità.",
                'Leone': "l'IO sarà fiero, orgoglioso, sicuro di sé, ha bisogno di affermarsi, autoritario.",
                'Vergine': "l'IO è intellettualizzato, ha bisogno di analizzare, di selezionare, di perfezionare, inquieto, pignolo.",
                'Bilancia': "l'IO vuole unirsi, associarsi, dipende dall'altro, dagli altri, si confronta per trovare il proprio posto.",
                'Scorpione': "l'IO deve scavare, cercare le risposte e i misteri, si manifesta a livello dell'inconscio.",
                'Sagittario': "l'IO si entusiasma, è generoso, idealista, ha il gusto dei viaggi e il bisogno di espansione.",
                'Capricorno': "l'IO ha le capacità per organizzarsi e l'autorità per dirigere. Gli atti sono profondi e seri.",
                'Acquario': "l'IO afferma la propria indipendenza, la propria originalità; obiettivo: affermare le idee attraverso movimenti umanitari.",
                'Pesci': "difficoltà a vivere il proprio IO, ad affermarlo; sempre all'ascolto del mondo interiore, misterioso e caotico, ambivalente."
            },
            
            # II CASA - IL DENARO CHE GUADAGNO
            2: {
                'Ariete': "le finanze sotto il segno dello slancio. Impulsività, ambizione ed energia servono a guadagnare denaro.",
                'Toro': "il soggetto ha il senso del denaro, degli affari e delle finanze. Denaro guadagnato grazie alle finanze, agli affari o ad una vocazione artistica.",
                'Gemelli': "denaro guadagnato dalle transazioni, gli scritti, la parola, gli spostamenti, aiuto da parte di chi lo circonda.",
                'Cancro': "il soggetto può lavorare all'interno della sua famiglia. Fluttuazione nelle finanze, interesse per il denaro proveniente da un patrimonio.",
                'Leone': "il soggetto si afferma e domina grazie ai guadagni ottenuti. Benefici dagli affari legati alle speculazioni, al gioco, all'arte.",
                'Vergine': "ottiene i guadagni dal servizio, dal metodo, dall'organizzazione. Lavora e guadagna occupandosi degli altri.",
                'Bilancia': "associazione, unione, apportatori di mezzi finanziari. Guadagni provenienti dall'arte o da questioni giuridiche.",
                'Scorpione': "guadagni provenienti dalle ricerche scientifiche o occulte o legati alla carne, alla lotta con la morte. Difficoltà nei guadagni.",
                'Sagittario': "i viaggi, l'estero, la diplomazia, gli affari, la sfera politica, religiosa permettono i successi finanziari.",
                'Capricorno': "guadagni ottenuti con metodo, pazienza e disciplina. Carriera lenta ma solida nel campo degli affari o dell'amministrazione.",
                'Acquario': "guadagni innovativi, legati a tecnologie moderne, lavoro di gruppo, organizzazioni umanitarie.",
                'Pesci': "guadagni incerti, legati a intuizioni creative, ma rischio di confusione finanziaria."
            },
            
            # III CASA - L'AMBIENTE, LA COMUNICAZIONE
            3: {
                'Ariete': "attività mentale intraprendente, spirito pioniere, comunicazione diretta e impulsiva.",
                'Toro': "mente concreta, lenta ma sicura, apprendimento attraverso la pratica.",
                'Gemelli': "mente curiosa, versatile, facilità di comunicazione, adattabilità all'ambiente.",
                'Cancro': "mente sensibile, influenzata dall'ambiente familiare, comunicazione affettiva.",
                'Leone': "mente creativa, espansiva, comunicazione generosa e calorosa.",
                'Vergine': "mente analitica, critica, attenta ai dettagli, comunicazione precisa.",
                'Bilancia': "l'intelletto è alla ricerca dell'armonia, della stabilità; il soggetto sa comparare. Buono per studi giuridici e arte.",
                'Scorpione': "intelletto dotato per il ragionamento psicologico. Il soggetto va a fondo nelle cose. Lavoro di ricerca in profondità.",
                'Sagittario': "entusiasmo per le idee importanti. Importanza degli spostamenti all'estero. Idee indipendenti, studi filosofici.",
                'Capricorno': "concentrazione del pensiero. Intelletto profondo e concreto, conservatore. Studi scientifici, politici.",
                'Acquario': "l'intelletto, le idee vanno in direzione del progresso, della novità. Concezione innovatrice, capacità di trasmettere alle masse.",
                'Pesci': "difficoltà a seguire gli studi, mentale e immaginativo, ispirato. Medianità, cambiamento di idee."
            },
            
            # IV CASA - L'INFANZIA, IL FOCOLARE DOMESTICO
            4: {
                'Ariete': "eredità impulsiva ed energica. Il soggetto rischia di entusiasmarsi per costruire la propria famiglia. Ambiente familiare tormentato.",
                'Toro': "eredità stabile. Il soggetto sa gestire il patrimonio. Aiuto finanziario da parte della famiglia.",
                'Gemelli': "eredità instabile, cambio di focolare domestico. Cambio di residenza, importanza di fratelli e sorelle. Eredità intellettuale.",
                'Cancro': "importanza dell'eredità materna. Importanza dell'influenza del focolare domestico. Immaginazione.",
                'Leone': "autorità maschile in famiglia. I bambini sono importanti, i genitori possono fornire aiuto. Il focolare è luogo di piacere e gioia.",
                'Vergine': "la vita familiare può essere sottomessa a esigenze legate ai parenti. Calcolo e problemi di salute in ambito familiare.",
                'Bilancia': "la vita sociale è importante, il soggetto crea il proprio focolare presso gli altri. Matrimonio vantaggioso. Lusso e benessere.",
                'Scorpione': "eredità passionale e critica. Il soggetto ricerca attraverso la famiglia una risposta fondamentale alla sua ragione esistenziale.",
                'Sagittario': "il soggetto si reca all'estero sistemandosi. Eredità filosofica o spirituale.",
                'Capricorno': "eredità forte e seria. La vita sociale o la realizzazione possono essere più importanti della famiglia. Beni immobili.",
                'Acquario': "abbandono brusco della famiglia, si trova a proprio agio a casa degli altri. Gli amici diventano la sua famiglia.",
                'Pesci': "l'eredità e l'influenza materna rendono il soggetto molto sensibile. Situazione familiare instabile."
            },
            
            # V CASA - LA VITA SENTIMENTALE, LA CREATIVITÀ, LE SPECULAZIONI
            5: {
                'Ariete': "l'amore è vissuto in maniera esagerata, passionale, impulsiva. Abituato al colpo di fulmine.",
                'Toro': "possibilità di creazione artistica. Il soggetto è possessivo nell'amore. Possibilità di speculazioni finanziarie.",
                'Gemelli': "gusto per il flirt, amori multipli. Curiosità e instabilità. Piaceri intellettuali; creatività negli scritti.",
                'Cancro': "incostante in amore, impronta della famiglia che influenza la creatività e l'immaginazione.",
                'Leone': "ardore e generosità, ragionamento ideale nel modo di amare. Amore per i bambini, interesse per il teatro. Speculazione.",
                'Vergine': "analizza i sentimenti, l'amore sottostà alla ragione. Freddezza, piacere scientifico o intellettuale.",
                'Bilancia': "l'amore si esprime solo attraverso l'unione, la coppia, l'associazione. Interesse per l'arte. Matrimonio d'amore.",
                'Scorpione': "sentimenti eccessivi, possessivo, passionale, seduttore.",
                'Sagittario': "idealizzazione degli amori, successo amoroso all'estero. Senso dell'educazione innato. Amore per lo sport e il gioco.",
                'Capricorno': "poche avventure. Controllo del cuore e del potere creativo. Pazienza, fedeltà e costanza. Possibile differenza d'età con il partner.",
                'Acquario': "la vita amorosa non si basa su una sola persona. Amore legato all'amicizia, cuore non convenzionale, originale.",
                'Pesci': "fugge davanti all'amore, ne ha paura, sacrifici affettivi. Molto sentimentale. Instabilità."
            },
            
            # VI CASA - IL LAVORO, LA SALUTE
            6: {
                'Ariete': "lavoro legato alla forza, all'impulsività, alla lotta. Mal di testa, infiammazioni, tendenza a ferite per imprudenza.",
                'Toro': "lavora perseguendo un obiettivo materiale preciso: denaro, banca, finanza, gestione immobiliare. Mal di gola, intossicazioni.",
                'Gemelli': "lavoro intellettuale, spostamenti, relazioni, scritti, parola. Tensione nervosa, malattie dei bronchi, stress mentale.",
                'Cancro': "lavoro a contatto con il pubblico, servizio alla famiglia. Può lavorare a casa. Fastidi digestivi, angoscia.",
                'Leone': "potenza, prestigio, autorità nel lavoro. Tensione arteriosa, debolezza cardiaca.",
                'Vergine': "lavoro = servizio. Metodo e spirito critico. Angoscia, fastidio al sistema neuro-vegetativo.",
                'Bilancia': "lavoro gradevole, contatto con gli altri. Senso della giustizia. Insufficienza renale.",
                'Scorpione': "aggressività al servizio della professione. Capacità di andare a fondo. Malattia genito-urinaria.",
                'Sagittario': "indipendenza, idealismo nel lavoro. Debolezza della vescica.",
                'Capricorno': "lavoro legato al passato, sforzo, pazienza, responsabilità. Problemi articolari, reumatici e delle ossa.",
                'Acquario': "lavoro al servizio della collettività. Originalità. Problemi circolatori e nervosi.",
                'Pesci': "instabilità, indecisione e ispirazione nel lavoro. Problemi con i piedi e con i nervi."
            },
            
            # VII CASA - GLI ALTRI, IL MATRIMONIO, LE ASSOCIAZIONI
            7: {
                'Ariete': "l'unione e l'associazione avvengono in maniera imprevista e impulsiva. Partner energico.",
                'Toro': "bisogno di unioni e associazioni stabili che sono finanziariamente vantaggiose. Coniuge sicuro ma testardo.",
                'Gemelli': "instabilità delle associazioni e delle unioni che vengono intellettualizzate. Curiosità e voglia di cambiamento.",
                'Cancro': "importanza della vita pubblica. Coniuge capriccioso. Importanza della funzione materna in tutte le forme di unione.",
                'Leone': "il partner deve essere brillante e avere una forte personalità. Matrimonio d'amore, importanza dei figli.",
                'Vergine': "le associazioni e l'unione sono fortemente intellettualizzate e legate a motivi di interesse. Possibile incontrare il coniuge nell'ambiente di lavoro.",
                'Bilancia': "eccellente posizione per l'unione e l'associazione. Il soggetto è fatto per il matrimonio. Equilibrio ed armonia.",
                'Scorpione': "passione finalizzata all'unione che corre rischi se la trasformazione non viene compresa dal coniuge.",
                'Sagittario': "matrimonio e associazioni legati all'estero. Il soggetto può sposare uno straniero. Idealizza l'unione.",
                'Capricorno': "matrimonio tardivo; unione e associazione seria che pone il soggetto di fronte a responsabilità pesanti.",
                'Acquario': "unione libera, non convenzionale. Amicizia e amore si fondono. Rapporto basato sulla libertà reciproca.",
                'Pesci': "unione idealizzata, ma rischio di illusioni e delusioni. Sacrificio per il partner."
            },
            
            # VIII CASA - EREDITÀ, INCONSCIO, SESSO, MORTE
            8: {
                'Ariete': "esteriorizzazione della parte inconscia, azione immediata. Coniuge spendaccione. Sessualmente virile, bisogno di conquista.",
                'Toro': "l'inconscio permette di servirsi del lavoro degli altri per un fine materiale. Sessualmente molto sensuale, molto fisico.",
                'Gemelli': "l'intelligenza e l'inconscio sono curiosi. Piccole eredità dall'ambiente familiare. Sessualmente cerebrale.",
                'Cancro': "l'inconscio funziona in stretto contatto con il campo familiare. Importanza delle eredità. Sessualmente dotato, comprende il partner.",
                'Leone': "l'inconscio si rivela creativo. Eredità importante. Sessualmente ardente, erotico, si concede all'altro.",
                'Vergine': "l'inconscio unito all'intelligenza analitica permette di studiare il comportamento. Eredità intellettuale. Sessualmente romantico, cerebrale.",
                'Bilancia': "inconscio che si esprime nelle relazioni con l'altro. Il mondo associativo è soggetto a mutazioni profonde.",
                'Scorpione': "importanza dell'inconscio, della sfera occulta, interesse per la morte. Eredità. Sessualità legata all'esperienza mistica.",
                'Sagittario': "inconscio nutrito di idealismo, fede, entusiasmo. Eredità dall'estero. Sessualmente istintivo, sano, conformista.",
                'Capricorno': "inconscio con difficoltà ad esprimersi. Eredità da persone anziane. Sessualmente esigente o distaccato.",
                'Acquario': "inconscio che deve affrontare la realtà universale. Eredità inattesa. Sessualmente liberale, cerebrale.",
                'Pesci': "inconscio in difficoltà, ricettivo senza difese. Problemi di eredità. Sessualmente dotato, bisogno di provare a se stesso."
            },
            
            # IX CASA - IL PENSIERO SUPERIORE, I GRANDI VIAGGI
            9: {
                'Ariete': "le grandi idee filosofiche si esprimono attraverso l'azione. Idealista, militante. Viaggiatore impulsivo.",
                'Toro': "idee importanti, concezioni realistiche che il soggetto concretizza. Dono per gli affari. Viaggi proficui.",
                'Gemelli': "idee importanti, attività mentale superficiale, manca di concentrazione. Viaggi numerosi.",
                'Cancro': "la famiglia permette la ricerca e la riflessione. Gusto del passato, senso storico, concezioni feconde.",
                'Leone': "le idee e le concezioni superiori sono personali e danno gusto del potere. Successo all'estero.",
                'Vergine': "idee e concezioni superiori legate al bisogno di servire. Concezioni scientifiche.",
                'Bilancia': "concezioni superiori legate all'associazione e all'unione. Matrimoni all'estero, idealista pacifico.",
                'Scorpione': "concezioni superiori che vanno in fondo alle cose, scavano la psiche e l'inconscio.",
                'Sagittario': "idee importanti e attività mentale al loro apogeo. Obiettivo: le concezioni superiori.",
                'Capricorno': "idee filosofiche, profondità del pensiero. Elevazione del pensiero. Riconoscimenti all'estero.",
                'Acquario': "concezioni superiori al servizio della collettività. Entusiasmo, fraternità, altruismo. Viaggi numerosi.",
                'Pesci': "concezioni mentali vissute in maniera positiva o negativa. Oscillazione tra poli opposti."
            },
            
            # X CASA - REALIZZAZIONI DELL'IO, POSIZIONE SOCIALE
            10: {
                'Ariete': "l'azione e l'iniziativa permettono di realizzarsi socialmente. Temperamento da capo.",
                'Toro': "il soggetto sa ciò che vuole, realista e perseverante. Senso degli affari. Può realizzarsi in arte, banca, immobiliare.",
                'Gemelli': "contratti, scritti, spostamenti, carriere intellettuali. Può svolgere molte attività diverse.",
                'Cancro': "successo in attività con contatto con il pubblico. Obiettivo principale: la vita familiare.",
                'Leone': "ambizione sociale. Il soggetto è brillante, comanda e dirige. Onore e successo.",
                'Vergine': "ambizione di servire (medicina, sfera sociale, insegnamento).",
                'Bilancia': "il soggetto si realizza socialmente in rapporto alla coppia, alle associazioni. Carriera giuridica.",
                'Scorpione': "le esperienze dell'inconscio servono da base alla scelta di una carriera scientifica o giudiziaria.",
                'Sagittario': "ambizione e carriera legata all'estero, al pensiero e ai viaggi.",
                'Capricorno': "il soggetto sa ciò che vuole ed ha le possibilità per ottenerlo. Ascesa lenta ma certa. Carriera politica.",
                'Acquario': "bisogno di un obiettivo umanitario. Carriera in organizzazioni moderne e collettive.",
                'Pesci': "sensibilità e ispirazione legate alla carriera. Può realizzare cose poco comuni."
            },
            
            # XI CASA - I PROGETTI, L'AMICIZIA, LE PROTEZIONI
            11: {
                'Ariete': "i progetti sono dinamici e attivi, le amicizie entusiasmanti e virili.",
                'Toro': "progetti stabili. Aiuto materiale e protezione da parte degli amici, tendenza ad essere possessivo.",
                'Gemelli': "progetti e amicizie instabili e multipli. Amici giovani. Amicizia intellettuale.",
                'Cancro': "l'intuizione guida il soggetto nella scelta degli amici. Tendenza ad essere popolare. La madre può essere un'amica.",
                'Leone': "progetti prestigiosi, amici brillanti. Influenza degli amici nella vita affettiva.",
                'Vergine': "progetti e amici mirati nel campo sociale e medico. Analisi e comprensione nella vita degli amici.",
                'Bilancia': "amicizie e progetti si confondono con l'associazione e l'unione. Favorevole al matrimonio.",
                'Scorpione': "progetti e amicizie passionali. Il soggetto va sino in fondo. Amicizie legate alla sessualità.",
                'Sagittario': "progetti entusiasmanti, viaggi e amicizie all'estero, ideali comuni con gli amici. Protezione.",
                'Capricorno': "progetti e amici selezionati, aiutano al miglioramento della carriera. Fedeltà e stabilità.",
                'Acquario': "importanza dell'amicizia e dei progetti con obiettivo collettivo. Progetti di riforma.",
                'Pesci': "amicizie e progetti possono portare al meglio o al peggio. Instabilità, progetti utopici."
            },
            
            # XII CASA - L'ESPERIENZA DELLA SOLITUDINE, LE GRANDI CRISI
            12: {
                'Ariete': "difficoltà a tirare le somme, a isolarsi. Iniziative segrete e violente.",
                'Toro': "crisi e conflitti di origine finanziaria legati al possesso. Presa di coscienza del bisogno di possedere.",
                'Gemelli': "difficoltà a prendere coscienza in profondità, ansietà, problemi in gioventù. Malattia nervosa.",
                'Cancro': "crisi nel campo familiare. La sensibilità è fonte di prove, esperienze che obbligano alla presa di coscienza.",
                'Leone': "crisi personali. Opposizione all'esternamento del bisogno di autorità. Amori sfortunati.",
                'Vergine': "presa di coscienza attraverso la costruzione, il lavoro isolato, l'analisi. Esperienza costruttiva.",
                'Bilancia': "presa di coscienza attraverso l'esperienza di unione o associazione. Crisi causata dagli altri.",
                'Scorpione': "crisi passionali che obbligano a prendere coscienza. Cerca le risposte alle domande essenziali.",
                'Sagittario': "crisi concernenti la vita interiore. Studi religiosi e filosofici. Prove all'estero.",
                'Capricorno': "presa di coscienza legata a pesanti responsabilità. Delusioni, malattie croniche.",
                'Acquario': "crisi legate ad avvenimenti imprevisti da parte degli amici. Invenzioni segrete.",
                'Pesci': "la vita interiore è campo di crisi dolorose: esaltazione dell'anima e depressione, tradimento affettivo."
            }
        }

        # ============================================
        # DATABASE 3: DOMINANTI DELLE CASE (dai nuovi file)
        # ============================================
        self.dominanti_case = {
            # DOMINANTE DELLA I CASA (ASCENDENTE) NELLE VARIE CASE
            'I': {
                1: "il soggetto ha una forte personalità, il suo interesse e la sua realizzazione sono centrati su di lui.",
                2: "l'interesse del soggetto è mirato ai guadagni, al possesso, al lavoro che rende, alle finanze.",
                3: "l'interesse del soggetto è mirato agli studi, ai viaggi, alla concretezza, ai fratelli e sorelle, agli scritti.",
                4: "l'interesse del soggetto è mirato alla famiglia, la casa, il patrimonio, i beni immobiliari, il paese natale.",
                5: "l'interesse del soggetto è verso i bambini, le speculazioni, i giochi, tutte le forme creative, gli amori.",
                6: "l'interesse del soggetto è verso il senso di servizio, il lavoro, la cura delle malattie, la salute.",
                7: "l'interesse del soggetto è verso tutte le forme di associazione, di unione; bisogno di socialità, interesse per gli altri.",
                8: "l'interesse del soggetto è verso il campo delle eredità, delle cose nascoste, delle finanze, della sessualità, le trasformazioni lo obbligano a cambiare, ricerca psicologica.",
                9: "l'interesse del soggetto è verso gli studi importanti, i viaggi, il campo astratto, la filosofia.",
                10: "l'interesse del soggetto è verso l'obbligo di realizzarsi socialmente. 'Uomo che si è fatto da solo', realizza le proprie ambizioni.",
                11: "l'interesse del soggetto è centrato sui progetti, gli amici, la partecipazione ai movimenti comunitari.",
                12: "interesse per le cose nascoste che richiedono isolamento e che obbligano a vivere ritirati."
            },
            
            # DOMINANTE DELLA II CASA NELLE VARIE CASE
            'II': {
                1: "la personalità del soggetto gli permette di realizzarsi materialmente, il denaro arriva.",
                2: "importanza del denaro, guadagni stabili, capacità materiale.",
                3: "le entrate provengono da occupazioni diverse (giornalismo, commercio) dagli scritti, dagli spostamenti, dalle relazioni con l'ambiente.",
                4: "il soggetto può lavorare da casa. Influenza delle questioni finanziarie sulle condizioni di vita familiari (beni immobili provenienti dai genitori).",
                5: "il denaro può provenire da speculazioni in un ambito creativo (legato al divertimento o all'insegnamento). 'Spendo per il piacere'.",
                6: "il denaro proviene dal lavoro, dal servizio, relazione tra guadagno e salute (medico, infermiere), senso del commercio.",
                7: "denaro proveniente dalle associazioni, fortuna legata all'unione.",
                8: "il soggetto guadagna usando il denaro degli altri. Finanze provenienti dalle associazioni, dalle eredità.",
                9: "guadagno proveniente dall'estero o da un'attività legata ai viaggi (libera professione).",
                10: "il soggetto ha successo dal punto di vista sociale e finanziario. Il lavoro ha come scopo il possesso materiale.",
                11: "guadagni provenienti dagli amici, dalle relazioni, dai progetti, dalla politica.",
                12: "denaro guadagnato con discrezione, appoggi finanziari nascosti."
            },
            
            # DOMINANTE DELLA III CASA NELLE VARIE CASE
            'III': {
                1: "importanza dei viaggi, dell'attività mentale, degli studi, dell'ambiente; il soggetto sa farsi apprezzare.",
                2: "guadagno legato agli spostamenti, all'ambiente. Capacità di gestione finanziaria. Si serve dell'intelligenza per guadagnare denaro.",
                3: "importanza delle possibilità intellettuali, grande curiosità. Pensiero concreto. Frequenti traslochi, viaggi numerosi.",
                4: "l'intelligenza si interessa ai problemi concernenti la famiglia, lavoro intellettuale in famiglia.",
                5: "intelligenza creativa. Può incontrare l'amore nel corso di un viaggio. Combinazione finanziaria.",
                6: "intelligenza analitica e al servizio degli altri. Senso del commercio. (Stanchezza nervosa).",
                7: "intelligenza al servizio dei soci o del coniuge. Può incontrare il futuro sposo nel corso di un viaggio. Importanza della clientela.",
                8: "l'intelligenza esplora le sfere dell'inconscio, dell'anima, dell'aldilà, della sessualità, dei capitali, delle eredità.",
                9: "pensiero portato verso gli studi importanti, l'insegnamento. Inclinazione per le lingue straniere e per i viaggi.",
                10: "l'intelligenza gli permette di imporsi, obiettivi ambiziosi nel campo sociale, viaggi, scritti e ambiente 'avranno da dire la loro'.",
                11: "i progetti e i dubbi sono al loro massimo, il soggetto si serve della propria intelligenza per progetti umanitari o intellettuali.",
                12: "gli spostamenti, gli scritti, costringono il soggetto ad un ritiro forzato. L'isolamento può facilitare l'attività mentale."
            },
            
            # DOMINANTE DELLA IV CASA NELLE VARIE CASE
            'IV': {
                1: "il soggetto è influenzato dalle eredità, dalla famiglia, i genitori influenzano il soggetto nella sua affermazione.",
                2: "la famiglia ha un'influenza sui guadagni del soggetto o sui suoi averi (eredità e gestioni di beni immobili).",
                3: "intelligenza segnata dall'eredità (cambiamento di domicilio), scritti intellettuali. Le relazioni con l'ambiente si fanno all'interno della famiglia.",
                4: "importanza del ruolo della madre, delle eredità, della famiglia.",
                5: "importanza degli amori e dei bambini, dell'educazione, dei piaceri. Piacevole fine della vita.",
                6: "il lavoro è legato al domicilio, utilizza il focolare domestico. Malattie ereditarie o contatto con il mondo medico in famiglia.",
                7: "la scelta del coniuge è influenzata dai genitori. La famiglia si trova nella casa degli altri. Le associazioni aiutano ad assicurare il patrimonio.",
                8: "importanza delle questioni ereditarie. Evoluzione nella concezione del focolare domestico nel corso della vita.",
                9: "il focolare domestico può trovarsi all'estero. Interesse per i problemi filosofici, scientifici, legali.",
                10: "la vita sociale, fondamentale per il soggetto, può essere favorita dai genitori.",
                11: "il soggetto crea presso gli amici la famiglia e il focolare domestico, là dove sente le proprie radici.",
                12: "crisi e prove di origine familiare. Bisogno di isolarsi. La famiglia è solitaria."
            },
            
            # DOMINANTE DELLA V CASA NELLE VARIE CASE
            'V': {
                1: "importanza dei bambini, degli amori, delle speculazioni. Il soggetto trova in se stesso la propria fonte di gioia.",
                2: "le speculazioni, il gioco, la creatività hanno come scopo cose concrete, materiali, finanziarie.",
                3: "fecondità mentale. Incontri affettivi nel corso di un viaggio.",
                4: "influenza del cuore nella vita familiare, amore per i bambini, per la casa, per la famiglia.",
                5: "accentua le disposizioni di questa Casa. Individualità, piacere, amore, speculazione, importanza dei bambini.",
                6: "creatività legata al lavoro, l'espansione solare si mette al servizio degli altri e dei bambini.",
                7: "matrimonio d'amore; le associazioni, le unioni sono legalizzate ma dipendenti dall'affettività.",
                8: "gli amori devono subire una trasformazione che non può avvenire senza rinuncia.",
                9: "incontro affettivo nel corso di un viaggio, gioie e piaceri all'estero. Relazioni affettive idealizzate.",
                10: "creatività legata alla riuscita sociale (artistica). Senso delle speculazioni, della finanza.",
                11: "relazioni affettive legate all'amicizia. Il soggetto fiorisce nella collettività, progetti per un vasto pubblico.",
                12: "legami amorosi segreti, crisi affettive. Difficoltà e prove legate alle caratteristiche di questa Casa."
            },
            
            # DOMINANTE DELLA VI CASA NELLE VARIE CASE
            'VI': {
                1: "il soggetto si realizza servendo gli altri nel lavoro. Importanza delle questioni legate alla salute.",
                2: "obiettivo del lavoro: guadagnare il denaro. Attitudine per le questioni mediche.",
                3: "lavoro cerebrale (tensione da superlavoro). Lavoro che ha a che fare con l'intelletto, gli spostamenti, la scrittura.",
                4: "lavoro a casa propria, nella propria famiglia, al servizio di questa (problemi di salute in famiglia).",
                5: "ama il proprio lavoro. Educazione, creatività, teatro, distrazioni, speculazioni, sono legate al lavoro.",
                6: "interessi per la medicina e la dietetica. Spirito analitico al servizio del lavoro.",
                7: "lavoro legato ai contatti con gli altri, ai contratti, alle associazioni.",
                8: "le profondità dell'inconscio al servizio dello spirito. Lo spirito analitico permette di trasformare capitali, psiche, aldilà.",
                9: "il soggetto lavora all'estero, spirito di sintesi nel lavoro. Concezioni superiori, idealismo.",
                10: "la riuscita sarà data dal bisogno di servire e di lavorare con il mondo. Protezione sul lavoro.",
                11: "progetti, lavoro e amicizie sono legati tra loro. Impiego in pubblicità: radio, televisione.",
                12: "può permettere al soggetto di servire il prossimo che soffre in luoghi isolati."
            },
            
            # DOMINANTE DELLA VII CASA NELLE VARIE CASE
            'VII': {
                1: "vita sociale influenzata dalle associazioni, dai contratti e dalle unioni. Gli altri si adattano al soggetto.",
                2: "le associazioni e l'unione influenzano le finanze. Denaro proveniente da contratti.",
                3: "associazione e unione legate agli spostamenti e agli scritti; importanza del fattore intellettuale nelle relazioni.",
                4: "le unioni e le associazioni avvengono all'interno della famiglia. Il soggetto si associa con la famiglia.",
                5: "unione d'amore, il soggetto legalizza il legame. Attitudine alla creatività. Vita sociale.",
                6: "l'associazione e il coniuge hanno a che fare con il lavoro. Il soggetto aiuta il coniuge, lavoro legato ai contratti.",
                7: "vedere gli aspetti importanti di questa Casa. Matrimonio, associazione, senso della realtà.",
                8: "il soggetto eredita dal coniuge o dai soci. Crisi o rinnovamento nell'associazione, nei contratti.",
                9: "matrimonio all'estero con uno straniero, partner che appartiene ad un altro ambiente. Protezione.",
                10: "le associazioni e l'unione sono importanti per il funzionamento della vita sociale del soggetto.",
                11: "associazione e unione legate all'amicizia che permettono di realizzare i propri progetti.",
                12: "unione o associazione segreta perché il soggetto può sentirsi prigioniero di un'unione ufficiale."
            },
            
            # DOMINANTE DELLA VIII CASA NELLE VARIE CASE
            'VIII': {
                1: "importanza e vitalità della vita psichica. Lavoro con capitali, occultismo, tutto ciò che obbliga a trasformare e rinnovare.",
                2: "capacità di gestire i propri beni e quelli degli altri, possibile eredità.",
                3: "può permettere degli studi concernenti il mentale, le idee, l'inconscio, i capitali. 'Scritti sull'argomento'.",
                4: "l'esperienza interiore si svolge in famiglia o è legata all'eredità del soggetto. Sconvolgimenti in questa Casa.",
                5: "esperienze interiori legate all'affettività, la sessualità è legata alla creatività in ogni sua forma.",
                6: "crisi psichica con ripercussioni sulla salute. Collegamento tra lavoro e trasformazioni legate alla salute, alla morte.",
                7: "la trasformazione interiore ha bisogno del prossimo. Sconvolgimento della vita sociale o delle relazioni con il coniuge.",
                8: "accentua il bisogno di sfruttare ciò che sta nel profondo.",
                9: "la trasformazione interiore deve essere sublimata. Eredità dall'estero.",
                10: "le trasformazioni servono alla realizzazione della vita sociale del soggetto. 'Ambizione molto forte'.",
                11: "la trasformazione interiore è in relazione con le esperienze concernenti i progetti e gli amici.",
                12: "importanza dell'istinto, dell'inconscio, difficoltà ad esprimere ciò che si vive interiormente."
            },
            
            # DOMINANTE DELLA IX CASA NELLE VARIE CASE
            'IX': {
                1: "possibilità di insegnare agli altri. Gusto per i problemi astratti, gli studi, la filosofia. 'Il soggetto giudica in profondità'.",
                2: "le relazioni finanziarie avvengono con l'estero. Guadagni ottenuti con l'intelligenza, gli studi, l'insegnamento.",
                3: "viaggi lunghi, studi importanti, pensieri filosofici che si concretizzano. L'estero è importante per l'ambiente.",
                4: "le concezioni morali e filosofiche provengono dai genitori. Idealismo nei confronti della famiglia.",
                5: "esterofilia. Figlio nato durante un viaggio all'estero. Creazioni ispirate da concezioni morali.",
                6: "le concezioni superiori, il mentale, l'idealismo vengono vissute concretamente nel lavoro.",
                7: "gli altri, l'altro, vengono idealizzati. Contratti, unioni, associazioni con l'estero.",
                8: "le concezioni superiori sono legate all'interesse per il campo psichico.",
                9: "studi importanti, concezioni superiori, il soggetto è di livello intellettuale molto elevato.",
                10: "il soggetto esprime le sue concezioni morali e filosofiche alla luce del sole, nel mondo. Successo all'estero.",
                11: "comunanza di idee con gli amici in materia morale e filosofica, progetti umanitari.",
                12: "l'isolamento e l'esilio sono utili allo spirito e permettono studi che obbligano a scavare nel profondo."
            },
            
            # DOMINANTE DELLA X CASA NELLE VARIE CASE
            'X': {
                1: "il soggetto ha i mezzi per realizzare le sue ambizioni sociali, la sua riuscita.",
                2: "situazione remuneratrice, può essere collegata alle finanze (riuscita finanziaria).",
                3: "la realizzazione della situazione sociale dipende dall'intelligenza del soggetto, dagli spostamenti, dagli scritti.",
                4: "la famiglia può intervenire nella realizzazione sociale del soggetto. Realizza le proprie aspirazioni in famiglia.",
                5: "la situazione è legata alle possibilità creative. Il soggetto ama ciò che fa, risplende.",
                6: "le questioni di salute, il senso del servizio influenzano la situazione; il soggetto si realizza servendo il prossimo.",
                7: "realizzazioni sociali attraverso contratti, associazioni, unione, contatto con gli altri.",
                8: "la realizzazione sociale è chiamata a subire una trasformazione. Il soggetto sfrutta i beni e i segreti altrui.",
                9: "la realizzazione sociale è legata alle concezioni morali, all'erudizione, ad una vocazione. Riconoscimenti all'estero.",
                10: "il padre può giocare un ruolo importante nel divenire sociale del soggetto che avrà successo e importanza.",
                11: "gli amici e i progetti permettono la realizzazione sociale. Popolarità e successo.",
                12: "situazione ed ambizioni segrete che non si realizzano alla luce del sole (lavoro ospedaliero, occultismo, astrologia)."
            },
            
            # DOMINANTE DELLA XI CASA NELLE VARIE CASE
            'XI': {
                1: "gli amici e i progetti lo aiutano a realizzarsi. Interesse per la vita politica e sociale.",
                2: "i progetti, gli appoggi, gli amici influenzano finanziariamente il soggetto. Lavoro in collaborazione.",
                3: "amici intellettuali, le relazioni e i progetti aiutano l'attività mentale. Progetti legati agli spostamenti.",
                4: "la famiglia è il luogo in cui si ricevono gli amici. Amicizie che durano sino in tarda età.",
                5: "amicizie che si trasformano in amore. Gli amici partecipano alla vita creativa del soggetto.",
                6: "amicizie e progetti nel lavoro, 'il soggetto è al servizio dei suoi amici'. Progetti legati alla salute.",
                7: "il soggetto sposa un amico. Progetti e amici sono legati all'associazione.",
                8: "gli amici possono aiutare il soggetto in campo finanziario (lasciati, doni) o psicologico.",
                9: "amicizia all'estero. Amici intelligenti, coltivati, appoggi legali. Progetti di origine intellettuale.",
                10: "appoggio degli amici nella riuscita sociale. 'Aiuto nella realizzazione delle ambizioni'.",
                11: "importanza della casa, dei progetti, dell'amicizia, delle speranze, dei movimenti comunitari.",
                12: "i progetti, le amicizie vengono tenuti segreti. Aiuta le società segrete."
            },
            
            # DOMINANTE DELLA XII CASA NELLE VARIE CASE
            'XII': {
                1: "bisogno di isolamento; l'esperienza aiuta l'evoluzione del soggetto. Interesse per le cose segrete.",
                2: "denaro proveniente da fonti nascoste, affari segreti.",
                3: "bisogno di comprendere le cose nascoste, le prove influenzano il mentale del soggetto. Difficoltà di concentrazione.",
                4: "famiglia isolata, il soggetto si ritira, vive dentro di sé una vita segreta.",
                5: "blocco della creazione segreta. Interiormente crisi affettiva e legame segreto.",
                6: "lavoro che ha a che fare con la salute e che si svolge in un luogo isolato. Difficoltà di origine psichica.",
                7: "vita interiore legata alle associazioni, alla coppia che può entrare in crisi.",
                8: "importanza della vita inconscia e segreta. Interesse per le cose occulte e nascoste.",
                9: "ideali e concezioni superiori vissuti interiormente. Crisi concernenti le opinioni del soggetto.",
                10: "ciò che il soggetto apprende nella solitudine è legato al divenire sociale. Deve servirsene per trovare il proprio ruolo.",
                11: "i progetti, le speranze, l'amicizia devono sottostare all'obbligo di una presa di coscienza più o meno dolorosa.",
                12: "rinforza il significato di questa casa, vita interiore profonda, lavori nascosti."
            }
        },
        
        # ============================================
        # DATABASE 4: PIANETI NELLE CASE (RADIX)
        # ============================================
        self.pianeti_case_radix = {
            # ☀️ SOLE - LA TUA IDENTITÀ, LA TUA LUCE
            'Sole': {
                1: {
                    'armonioso': "Il Sole nella tua Prima Casa illumina la tua personalità in modo speciale. Sai chi sei e non hai paura di mostrarlo. La tua presenza è calda e magnetica, e gli altri sentono che puoi essere un punto di riferimento. Hai una naturale autorevolezza che non ha bisogno di imporsi, perché semplicemente traspare da te. La vita ti chiama a essere protagonista della tua storia, e tu rispondi con slancio e generosità.",
                    'dissonante': "Il Sole in Prima Casa in aspetto teso ti porta a volte a dubitare del tuo valore, e per compensare rischi di essere troppo rigida o esigente con te stessa e con gli altri. C'è una luce forte dentro di te, ma fai fatica a regolarne l'intensità. Impara a brillare senza abbagliare, e scoprirai che la tua autorità naturale non ha bisogno di sforzi."
                },
                2: {
                    'armonioso': "Il Sole nella tua Seconda Casa illumina il tuo rapporto con le risorse e i valori. Hai un senso pratico che ti permette di costruire sicurezza con pazienza e intelligenza. Il denaro e i beni materiali non sono un fine, ma uno strumento per esprimere la tua creatività e la tua generosità. Sai che la vera ricchezza è anche interiore, e questo ti aiuta a gestire le cose con saggezza.",
                    'dissonante': "Con il Sole in Seconda Casa in aspetto teso, il tuo valore personale può diventare troppo legato a ciò che possiedi. A volte ti senti insicura e cerchi conferme nei beni materiali o nel successo economico. Ricorda che tu vali per quello che sei, non per quello che hai. La sicurezza vera viene da dentro."
                },
                3: {
                    'armonioso': "Il Sole in Terza Casa accende la tua mente e la tua comunicazione. Hai il dono di esprimerti con chiarezza e calore, e le tue parole arrivano dritte al cuore. Sei curiosa, ami imparare e condividere quello che scopri. I fratelli, le sorelle o le persone vicine sono importanti nella tua vita e ti aiutano a crescere. I viaggi e gli studi ti arricchiscono e ti fanno brillare.",
                    'dissonante': "Il Sole in Terza Casa in aspetto teso può rendere la tua comunicazione a volte troppo diretta o nervosa. Ti capita di sentirti incompresa o di non riuscire a esprimere quello che provi. Cerca di rallentare, di ascoltare prima di parlare. Le tue idee sono preziose, ma hanno bisogno del tempo giusto per essere condivise."
                },
                4: {
                    'armonioso': "Il Sole nella tua Quarta Casa brilla sulle tue radici e sulla tua famiglia. La tua casa è il tuo rifugio, il luogo dove ricaricare le energie. Hai un legame profondo con la tua storia e con le persone che ti hanno cresciuta. Questo ti dà una sicurezza di base che ti accompagna in tutto quello che fai. La tua forza interiore è visibile a chi ti vuole bene.",
                    'dissonante': "Con il Sole in Quarta Casa in aspetto teso, il rapporto con la famiglia o con le tue radici può essere fonte di tensione. Forse hai vissuto situazioni difficili che ti hanno segnata, o senti che il tuo valore non è stato riconosciuto dai tuoi cari. Lavora sulla tua capacità di perdonare e di fare pace con il passato: solo così la tua luce potrà splendere libera."
                },
                5: {
                    'armonioso': "Il Sole in Quinta Casa illumina la tua creatività, il tuo amore e la tua gioia di vivere. Hai un cuore generoso e ami esprimerti in tutto quello che fai. I bambini, se ci sono o se arriveranno, saranno una grande fonte di felicità. L'amore per te è un gioco meraviglioso, fatto di passione e di leggerezza. La tua creatività può esprimersi in mille forme: arte, danza, scrittura, o semplicemente nel modo in cui rendi speciale la vita di chi ami.",
                    'dissonante': "Il Sole in Quinta Casa in aspetto teso può portare a volte eccessi in amore o nella ricerca del piacere. Rischia di cercare fuori conferme che dovresti trovare dentro. Impara a distinguere l'amore vero dalla voglia di apparire, e la creatività genuina dal bisogno di attenzione. Il tuo cuore merita relazioni autentiche."
                },
                6: {
                    'armonioso': "Il Sole in Sesta Casa illumina la tua vita quotidiana e il tuo lavoro. Trovi soddisfazione nel servire gli altri e nel fare le cose con cura e dedizione. La tua salute è buona perché sai ascoltare i bisogni del tuo corpo e rispettare i tuoi ritmi. Il lavoro non è solo un dovere, ma un modo per esprimere chi sei e per sentirti utile. Le piccole cose di ogni giorno hanno per te un sapore speciale.",
                    'dissonante': "Con il Sole in Sesta Casa in aspetto teso, rischi di farti prendere troppo dalle preoccupazioni quotidiane. Il lavoro può diventare un peso, e la salute può risentirne se non impari a rilassarti. Ricorda che non devi dimostrare nulla a nessuno. Prenditi cura di te con la stessa dedizione che riservi agli altri."
                },
                7: {
                    'armonioso': "Il Sole nella tua Settima Casa splende sulle tue relazioni e sui tuoi partner. Sei fatta per la relazione, per la condivisione, per il confronto con l'altro. Il matrimonio o le unioni importanti sono al centro della tua vita e ti aiutano a crescere. Sai dare e ricevere con equilibrio, e questo rende i tuoi legami forti e duraturi. Gli altri ti vedono come una persona giusta e affidabile.",
                    'dissonante': "Il Sole in Settima Casa in aspetto teso può rendere le relazioni un campo di battaglia. Forse tendi a cercare nell'altro ciò che non trovi in te stessa, o a pretendere troppo dal partner. Impara a stare bene anche da sola, e a vedere l'altro non come un tuo completamento, ma come un compagno di viaggio. L'armonia si costruisce in due, ma parte da te."
                },
                8: {
                    'armonioso': "Il Sole in Ottava Casa illumina le tue profondità, la tua capacità di trasformarti e di rinascere. Hai una forza interiore che ti permette di affrontare le crisi e di uscirne più forte. Sei attratta dai misteri della vita, dalla psicologia, dall'occulto, e hai un'intuizione che ti guida nei momenti difficili. Le trasformazioni, anche dolorose, sono per te opportunità di crescita.",
                    'dissonante': "Con il Sole in Ottava Casa in aspetto teso, le crisi e le trasformazioni possono diventare fonte di angoscia. Forse hai paura di perdere il controllo, o fatichi a fidarti degli altri. Impara a lasciar andare, ad accettare che alcune cose devono morire per far posto a qualcosa di nuovo. La tua forza è più grande di quanto credi."
                },
                9: {
                    'armonioso': "Il Sole in Nona Casa illumina la tua mente e il tuo spirito. Hai una sete di conoscenza che ti porta lontano, nei viaggi, negli studi, nella filosofia. Sei aperta a nuove culture e a nuove idee, e questo ti arricchisce profondamente. La tua fede, qualunque essa sia, è una fonte di luce e di speranza. Insegni agli altri con l'esempio, con la tua voglia di imparare e di crescere.",
                    'dissonante': "Il Sole in Nona Casa in aspetto teso può renderti a volte troppo idealista o rigida nelle tue convinzioni. Rischia di perderti in sogni troppo grandi o di giudicare chi non la pensa come te. Ricorda che la verità ha tante facce, e che la saggezza sta anche nell'accettare i limiti del reale."
                },
                10: {
                    'armonioso': "Il Sole nella tua Decima Casa illumina la tua strada, la tua vocazione, il tuo posto nel mondo. Hai una chiara visione di ciò che vuoi diventare e lavori con costanza per realizzarti. Il successo sociale arriva come conseguenza naturale della tua dedizione e della tua autenticità. Gli altri ti riconoscono autorità e rispetto, e tu sai usarli con generosità.",
                    'dissonante': "Con il Sole in Decima Casa in aspetto teso, l'ambizione può diventare un'ossessione. Rischia di sacrificare la tua vita privata per il successo, o di sentirti sempre sotto esame. Ricorda che il tuo valore non dipende dalla carriera o dal riconoscimento degli altri. La vera realizzazione è essere in pace con te stessa."
                },
                11: {
                    'armonioso': "Il Sole in Undicesima Casa illumina le tue amicizie e i tuoi progetti. Sei circondata da persone che ti vogliono bene e che condividono i tuoi ideali. I tuoi sogni sono grandi e hai la capacità di realizzarli insieme agli altri. La vita di gruppo, le associazioni, i movimenti ti danno energia e ti fanno sentire parte di qualcosa di più grande. Gli amici sono la tua famiglia del cuore.",
                    'dissonante': "Il Sole in Undicesima Casa in aspetto teso può rendere le amicizie fonte di delusione. Forse ti aspetti troppo dagli altri, o scegli persone che non ti corrispondono. Impara a distinguere le amicizie vere da quelle interessate, e a non perdere la tua individualità nel gruppo. I tuoi progetti sono importanti, ma non devono diventare un'ossessione."
                },
                12: {
                    'armonioso': "Il Sole in Dodicesima Casa illumina la tua vita interiore, il tuo mondo nascosto. Sei una persona profonda, con una ricca vita spirituale e una grande sensibilità. La solitudine non ti spaventa, anzi è il luogo dove ritrovi te stessa e la tua pace. Hai un dono per aiutare chi soffre, per comprendere il dolore altrui. La tua luce è silenziosa, ma scalda chi ti sta vicino.",
                    'dissonante': "Con il Sole in Dodicesima Casa in aspetto teso, la solitudine può diventare isolamento, e la sensibilità fonte di sofferenza. Forse porti dentro antiche ferite che fatichi a lasciar andare. Impara a perdonare, a perdonarti, e a chiedere aiuto quando ne hai bisogno. La tua luce merita di uscire allo scoperto, anche se a piccoli passi."
                }
            },
            
            # 🌙 LUNA - LE TUE EMOZIONI, LA TUA ANIMA
            'Luna': {
                1: {
                    'armonioso': "La Luna nella tua Prima Casa ti rende una persona di una sensibilità speciale. Le tue emozioni sono a fior di pelle e sai leggere quelle degli altri come poche. Sei intuitiva, empatica, e la tua presenza ha qualcosa di materno e accogliente. I tuoi stati d'animo cambiano come le fasi della luna, ma questo non è un difetto: è il tuo modo di essere in sintonia con la vita. Le persone si fidano di te perché sentono che le capisci davvero.",
                    'dissonante': "Con la Luna in Prima Casa in aspetto teso, la tua sensibilità può diventare una gabbia. Sei così ricettiva che rischi di farti travolgere dalle emozioni, tue e altrui. A volte reagisci in modo impulsivo, e poi ti penti. Impara a proteggerti, a distinguere ciò che senti tu da ciò che assorbi dall'esterno. La tua sensibilità è un dono, ma ha bisogno di confini."
                },
                2: {
                    'armonioso': "La Luna in Seconda Casa illumina il tuo rapporto con le risorse e la sicurezza. Hai un intuito speciale per le questioni pratiche e sai gestire il denaro con saggezza, ascoltando le tue sensazioni più che i calcoli freddi. Per te la sicurezza non è solo materiale, ma anche emotiva. Quando ti senti serena dentro, anche le cose fuori vanno per il verso giusto. La tua casa è il tuo nido, e lo rendi accogliente con amore.",
                    'dissonante': "Con la Luna in Seconda Casa in aspetto teso, la tua sicurezza emotiva può diventare troppo legata a quella materiale. Hai paura di non avere abbastanza, e questa paura ti porta a volte a essere troppo attaccata ai beni o a spendere in modo compulsivo per sentirti meglio. Ricorda che la vera ricchezza è dentro di te. Impara a distinguere i bisogni veri dalle paure."
                },
                3: {
                    'armonioso': "La Luna in Terza Casa accende la tua mente con l'emozione. Pensi con il cuore e parli con l'anima. Le tue parole sanno consolare, incoraggiare, ispirare. Hai un legame speciale con le persone vicine, con i fratelli e le sorelle, e spesso fai da ponte tra loro. La tua curiosità è infinita e impari meglio quando ciò che studi ti parla al cuore. I viaggi sono per te occasioni di crescita emotiva.",
                    'dissonante': "Con la Luna in Terza Casa in aspetto teso, la comunicazione diventa difficile. Le tue parole escono prima che tu le abbia pensate, e spesso dici cose che non vorresti. Ti capita di sentirti incompresa, di litigare con le persone care per un nonnulla. Impara a fare una pausa tra l'emozione e la parola. Respira, ascolta, e poi parla. Le tue idee meritano di essere espresse con calma."
                },
                4: {
                    'armonioso': "La Luna nella tua Quarta Casa è a casa sua, e si sente. Hai un legame profondo con la tua famiglia, con le tue radici, con la tua storia. La tua casa è il tuo rifugio, il luogo dove puoi finalmente essere te stessa senza maschere. La figura materna, o chi ne ha fatto le veci, ha lasciato in te un'impronta dolce e profonda. Porti dentro di te un calore che sai trasmettere a chi ami.",
                    'dissonante': "Con la Luna in Quarta Casa in aspetto teso, il rapporto con la famiglia o con il passato può essere fonte di dolore. Forse hai vissuto un'infanzia difficile, o hai ancora ferite aperte con tua madre. La tua casa, invece di essere un rifugio, a volte ti sembra una prigione. Impara a fare pace con la tua storia. Il passato non si può cambiare, ma puoi scegliere come portarlo. La tua vera casa sei tu."
                },
                5: {
                    'armonioso': "La Luna in Quinta Casa illumina il tuo cuore e la tua creatività. Sei una donna che ama con tutto se stessa, con passione e con dolcezza. I bambini ti adorano perché con te si sentono capiti e liberi di essere se stessi. La tua creatività è come un fiume che scorre spontaneo: dipingi, scrivi, danzi, o semplicemente rendi speciale ogni momento. L'amore per te è gioco, è gioia, è vita.",
                    'dissonante': "Con la Luna in Quinta Casa in aspetto teso, l'amore può diventare una fonte di insicurezza. Hai paura di non essere amata abbastanza, e questa paura ti porta a volte a essere troppo esigente o a cercare conferme continue. La tua creatività si blocca quando non ti senti all'altezza. Ricorda che l'amore vero non si conquista, si accoglie. E la tua creatività è un dono, non una prestazione."
                },
                6: {
                    'armonioso': "La Luna in Sesta Casa illumina la tua vita quotidiana e il tuo lavoro. Trovi soddisfazione nelle piccole cose, nei gesti di cura che ripeti ogni giorno. Il tuo lavoro, anche il più umile, lo fai con amore e dedizione. Sei sensibile ai bisogni degli altri e sai creare un'atmosfera serena dove lavori. La tua salute è legata al tuo benessere emotivo: quando sei in pace, stai bene.",
                    'dissonante': "Con la Luna in Sesta Casa in aspetto teso, la routine può diventare un peso. Ti senti sopraffatta dai doveri quotidiani e la tua salute ne risente. Forse tendi a trascurare i tuoi bisogni per badare a quelli degli altri. Impara a prenderti cura di te con la stessa attenzione che riservi agli altri. Il riposo non è una perdita di tempo, è una necessità. Ascolta il tuo corpo, ti sta parlando."
                },
                7: {
                    'armonioso': "La Luna nella tua Settima Casa illumina le tue relazioni e il tuo partner. Sei fatta per la vita di coppia, per la condivisione profonda. Senti le emozioni dell'altro come se fossero tue, e questo ti rende una compagna empatica e attenta. Il matrimonio o le unioni importanti sono per te un porto sicuro, dove puoi finalmente abbassare la guardia. La tua dolcezza attira persone che sanno apprezzarla.",
                    'dissonante': "Con la Luna in Settima Casa in aspetto teso, le relazioni possono diventare una fonte di sofferenza. Hai paura di essere abbandonata, e questa paura ti porta a volte a essere troppo dipendente o a scegliere partner che non ti rispettano. Impara a stare bene anche da sola. L'amore vero non ti toglie libertà, te ne dà di più. Meriti un partner che ti ami per quello che sei, non per quello che fai per lui."
                },
                8: {
                    'armonioso': "La Luna in Ottava Casa illumina le tue profondità, la tua anima più segreta. Hai una sensibilità quasi magica, che ti permette di intuire cose che gli altri non vedono. Sei attratta dai misteri della vita, dalla psicologia, dall'occulto. Le tue emozioni sono intense, profonde, e ti portano a vivere trasformazioni interiori che ti fanno crescere. La tua intimità è sacra, e la condividi solo con chi merita.",
                    'dissonante': "Con la Luna in Ottava Casa in aspetto teso, le tue emozioni profonde possono diventare fonte di angoscia. Forse hai paura di perdere il controllo, o vivi le relazioni con troppa intensità, fino a soffrirne. Impara a distinguere l'intimità sana dalla fusione che annulla. La tua profondità è un tesoro, ma ha bisogno di confini. Fidati del tuo istinto, ma non lasciare che ti travolga."
                },
                9: {
                    'armonioso': "La Luna in Nona Casa illumina la tua anima in viaggio. Sei una viaggiatrice, nel mondo e dentro te stessa. La spiritualità per te è sentire profondo, non dogma. I viaggi, reali o interiori, ti aprono il cuore e la mente. Sei attratta da culture diverse, da filosofie che parlano all'anima. La tua fede è personale, autentica, e ti sostiene nei momenti difficili. Insegni agli altri con l'esempio della tua ricerca interiore.",
                    'dissonante': "Con la Luna in Nona Casa in aspetto teso, la ricerca di senso può diventare una fuga. Rischia di perderti in ideali troppo astratti, o di sentirti sempre in conflitto tra ciò in cui credi e la realtà. Impara a trovare il sacro anche nel quotidiano. La verità non è solo lontana, è anche qui, nelle piccole cose. Ascolta il tuo cuore, ma tieni i piedi per terra."
                },
                10: {
                    'armonioso': "La Luna in Decima Casa illumina la tua immagine pubblica e la tua carriera. Hai un'intuizione speciale per capire cosa la gente vuole, e questo ti aiuta nel lavoro e nelle relazioni sociali. La tua sensibilità è apprezzata, e la tua autorevolezza è naturale, mai impostata. Sai comunicare con calore e questo ti apre molte porte. La tua carriera è anche un modo per prenderti cura degli altri, su scala più ampia.",
                    'dissonante': "Con la Luna in Decima Casa in aspetto teso, la tua immagine pubblica può diventare fonte di insicurezza. Sei troppo sensibile alle critiche e alle opinioni altrui, e rischi di perdere la tua autenticità per compiacere gli altri. Ricorda che non puoi piacere a tutti, e non devi. La tua sensibilità è un dono, ma non deve farti dimenticare chi sei veramente. L'approvazione più importante è la tua."
                },
                11: {
                    'armonioso': "La Luna in Undicesima Casa illumina le tue amicizie e i tuoi sogni. Hai amiche del cuore che sono come sorelle, e con loro condividi gioie e dolori. I tuoi progetti sono ispirati dal cuore, e spesso coinvolgono gli altri in modo positivo. Sei sensibile ai bisogni della collettività e ti impegni per cause in cui credi. I tuoi ideali sono alti, ma hai anche la capacità di realizzarli, grazie all'aiuto di chi ti vuole bene.",
                    'dissonante': "Con la Luna in Undicesima Casa in aspetto teso, le amicizie possono diventare fonte di delusione. Forse ti aspetti troppo dagli amici, o scegli persone che non ti sono veramente vicine. I tuoi progetti rischiano di naufragare per mancanza di concretezza. Impara a distinguere le amicizie vere da quelle di convenienza, e a non perdere di vista la realtà. I sogni sono belli, ma hanno bisogno di radici per crescere."
                },
                12: {
                    'armonioso': "La Luna in Dodicesima Casa illumina il tuo mondo interiore, il tuo giardino segreto. Sei una donna profonda, con una ricca vita spirituale e una sensibilità quasi medianica. La solitudine non ti pesa, anzi è il luogo dove ritrovi te stessa e la tua pace. Hai un dono per comprendere il dolore altrui e per aiutare chi soffre. La tua anima è antica e saggia, e questo si sente quando ti si conosce veramente.",
                    'dissonante': "Con la Luna in Dodicesima Casa in aspetto teso, la tua sensibilità può diventare una prigione. Porti dentro antiche ferite che non riesci a lasciar andare, e la solitudine si trasforma in isolamento. Forse hai paura di mostrarti per come sei, e ti nascondi dietro un muro. Impara a perdonare, a perdonarti, e a chiedere aiuto. La tua luce merita di uscire allo scoperto. Non sei sola, anche se a volte ti senti così."
                }
            },
            
            # 💬 MERCURIO - LA TUA MENTE, LA TUA COMUNICAZIONE
            'Mercurio': {
                1: {
                    'armonioso': "Mercurio nella tua Prima Casa ti rende una comunicatrice nata. Le parole ti escono facili e arrivano dritte al cuore. Hai una mente vivace, curiosa, sempre pronta a imparare cose nuove. Le tue idee sono chiare e sai esprimerle con calore e convinzione. La gente ti ascolta volentieri perché sai rendere interessante anche l'argomento più banale. La tua intelligenza è al servizio della relazione, e questo è un dono prezioso.",
                    'dissonante': "Con Mercurio in Prima Casa in aspetto teso, la tua mente a volte corre troppo. Parli prima di pensare, e le tue parole possono ferire senza che tu lo voglia. Ti capita di essere fraintesa, e questo ti fa soffrire. Impara a rallentare, a respirare prima di parlare. Le tue idee sono preziose, ma hanno bisogno del tempo giusto per essere espresse. Ascolta di più, parla di meno, e vedrai che tutto migliorerà."
                },
                2: {
                    'armonioso': "Mercurio in Seconda Casa illumina il tuo rapporto con le risorse e i valori. Hai una mente pratica che sa come gestire il denaro con intelligenza. Le tue idee spesso si trasformano in opportunità concrete. Sai comunicare il valore delle cose, e questo ti aiuta nel lavoro e negli affari. Per te, la vera ricchezza è anche intellettuale, e investire nella cultura è importante quanto investire nei beni materiali.",
                    'dissonante': "Con Mercurio in Seconda Casa in aspetto teso, la tua mente può diventare troppo concentrata sul denaro. Rischia di vedere tutto in termini di guadagno e perdita, e questo ti toglie leggerezza. Forse hai paura di non avere abbastanza, e questa paura ti porta a decisioni impulsive. Ricorda che la vera sicurezza non è solo materiale. Impara a fidarti della vita e a non dare troppo peso ai soldi."
                },
                3: {
                    'armonioso': "Mercurio in Terza Casa è a casa sua. La tua mente è vivace, curiosa, sempre in movimento. Ami imparare, comunicare, scambiare idee. Le parole sono la tua passione, e sai usarle con grazia e intelligenza. I fratelli, le sorelle, le persone vicine sono importanti per te e spesso sono i tuoi primi interlocutori. I viaggi, anche brevi, ti arricchiscono e ti stimolano. Sei una persona con cui è bello parlare.",
                    'dissonante': "Con Mercurio in Terza Casa in aspetto teso, la tua mente può diventare troppo agitata. Hai mille pensieri che si accavallano, e fatichi a concentrarti. Le parole ti escono nervose, e rischi di litigare con le persone care per un nonnulla. Impara a fare ordine nella tua testa, a scrivere i pensieri, a rallentare. La tua intelligenza è un dono, ma ha bisogno di calma per esprimersi."
                },
                4: {
                    'armonioso': "Mercurio in Quarta Casa illumina la tua mente legata alle radici. Hai una memoria profonda, che attinge alla storia della tua famiglia e alle tue tradizioni. La tua casa è anche il luogo del pensiero, dove ami leggere, studiare, riflettere. Le conversazioni in famiglia sono importanti e ti nutrono. Spesso fai da mediatore tra i tuoi cari, portando chiarezza e comprensione. La tua intelligenza è intrisa di affetto.",
                    'dissonante': "Con Mercurio in Quarta Casa in aspetto teso, la comunicazione in famiglia può essere difficile. Forse ci sono segreti, incomprensioni, parole non dette che pesano. Ti capita di sentirti intrappolata in vecchi schemi mentali ereditati dalla tua storia. Impara a fare pace con il passato, a dire le cose che non hai mai detto, a liberarti dai pesi che porti. La tua mente merita leggerezza."
                },
                5: {
                    'armonioso': "Mercurio in Quinta Casa illumina la tua creatività e il tuo amore. Hai una mente giocosa, che ama divertirsi e sperimentare. Le tue idee creative sono brillanti e originali. In amore, la comunicazione è fondamentale per te: ami parlare con il partner, scherzare, condividere pensieri. I bambini ti adorano perché parli la loro lingua, quella della fantasia e del gioco. La tua intelligenza è una festa.",
                    'dissonante': "Con Mercurio in Quinta Casa in aspetto teso, la tua mente in amore può diventare troppo cerebrale. Analizzi, giudichi, e perdi la spontaneità. Rischia di confondere l'amore con l'idea dell'amore. La tua creatività si blocca quando ti senti giudicata. Impara a lasciarti andare, a non pensare troppo. L'amore vero non si analizza, si vive. E la creatività fiorisce quando sei libera."
                },
                6: {
                    'armonioso': "Mercurio in Sesta Casa illumina la tua mente al servizio del lavoro e della salute. Hai una capacità di analisi che ti aiuta a risolvere i problemi quotidiani con intelligenza. Il tuo lavoro richiede spesso concentrazione e precisione, e tu hai la mente giusta per farlo. Sei attenta ai dettagli e questo ti rende preziosa in qualsiasi contesto. La tua salute è buona perché sai ascoltare i segnali del tuo corpo e agire di conseguenza.",
                    'dissonante': "Con Mercurio in Sesta Casa in aspetto teso, la tua mente può diventare troppo ansiosa. Ti preoccupi per tutto, analizzi ogni minimo dettaglio, e questo ti stanca. Il lavoro diventa un peso e la salute ne risente, con disturbi nervosi o digestivi. Impara a rilassarti, a non voler controllare tutto. La perfezione non esiste. Concediti il permesso di sbagliare e di respirare."
                },
                7: {
                    'armonioso': "Mercurio in Settima Casa illumina le tue relazioni e i tuoi partner. Hai una mente aperta al dialogo e alla comprensione. Con il partner sai parlare con dolcezza e intelligenza, e questo rende la vostra relazione solida e profonda. Le associazioni, le collaborazioni ti vengono naturali, perché sai metterti nei panni degli altri. La tua comunicazione è il segreto dei tuoi legami felici.",
                    'dissonante': "Con Mercurio in Settima Casa in aspetto teso, la comunicazione nelle relazioni può diventare conflittuale. Litighi per un nonnulla, fraintendi le parole dell'altro, ti senti incompresa. Forse hai paura di dire quello che pensi veramente, o lo dici nel modo sbagliato. Impara ad ascoltare prima di parlare, a chiedere chiarimenti invece di arrabbiarti. Le parole possono ferire, ma possono anche guarire. Scegli di usarle con amore."
                },
                8: {
                    'armonioso': "Mercurio in Ottava Casa illumina la tua mente profonda. Sei attratta dai misteri della vita, dalla psicologia, dall'occulto. La tua intelligenza è come un bisturi: va a fondo, scava, scopre. Capisci le motivazioni nascoste delle persone, e questo ti rende una psicologa naturale. Le trasformazioni della vita le affronti con lucidità, e sai trarre insegnamento anche dalle esperienze più dure. La tua mente non ha paura di guardare nell'ombra.",
                    'dissonante': "Con Mercurio in Ottava Casa in aspetto teso, la tua mente può diventare ossessiva. Ti fissi su pensieri che ti tormentano, fai fatica a lasciar andare. Le paure profonde prendono il sopravvento e ti bloccano. Impara a distinguere l'indagine sana dalla paranoia. La verità è importante, ma non tutte le verità vanno scoperte. A volte è meglio lasciar perdere e fidarsi. La tua mente ha bisogno di pace, non di继续. La tua mente ha bisogno di pace, non di continue tensioni."
                },
                9: {
                    'armonioso': "Mercurio in Nona Casa illumina la tua mente superiore. Hai una sete di conoscenza che ti porta lontano, nei viaggi, negli studi, nella filosofia. La tua intelligenza è aperta, tollerante, curiosa di tutto ciò che è diverso. Ami confrontarti con culture e idee nuove, e questo ti arricchisce profondamente. La tua mente è un ponte tra il tuo cuore e il mondo, e sai comunicare le tue scoperte con entusiasmo e chiarezza.",
                    'dissonante': "Con Mercurio in Nona Casa in aspetto teso, la tua mente può diventare troppo rigida nelle sue convinzioni. Rischia di chiuderti in idee che non ammetti discussioni, di diventare dogmatica. I viaggi o gli studi possono deluderti se non corrispondono alle tue aspettative. Impara ad accettare che la verità ha tante facce, e che la saggezza sta anche nel dubitare. La tua mente è grande, ma non deve diventare una prigione."
                },
                10: {
                    'armonioso': "Mercurio in Decima Casa illumina la tua carriera e la tua immagine pubblica. Hai una mente brillante che ti aiuta a farti strada nel mondo. Sai comunicare con autorità e calore, e questo ti apre molte porte. Le tue idee sono apprezzate e riconosciute. Il lavoro intellettuale è la tua strada, e la percorri con passione e intelligenza. La tua parola ha peso e sai usarla per costruire relazioni importanti.",
                    'dissonante': "Con Mercurio in Decima Casa in aspetto teso, la comunicazione in ambito professionale può diventare fonte di tensioni. Rischia di essere fraintesa, o di parlare in modo troppo diretto, creando inimicizie. Forse hai paura di non essere all'altezza, e questo ti porta a sforzarti troppo. Impara a dosare le parole, a scegliere i momenti giusti. La tua intelligenza è preziosa, ma non deve diventare un'arma. Usala con saggezza e leggerezza."
                },
                11: {
                    'armonioso': "Mercurio in Undicesima Casa illumina le tue amicizie e i tuoi progetti. Hai amici intelligenti, con cui ami scambiare idee e condividere sogni. Le tue amicizie sono spesso anche intellettuali, e questo le rende stimolanti e profonde. I tuoi progetti sono ambiziosi e hai la capacità di coinvolgere gli altri per realizzarli. La tua mente è aperta al futuro, alle innovazioni, a tutto ciò che è nuovo. I gruppi, le associazioni, i movimenti sono il tuo ambiente ideale.",
                    'dissonante': "Con Mercurio in Undicesima Casa in aspetto teso, le amicizie possono diventare fonte di delusione intellettuale. Forse ti senti incompresa dai tuoi amici, o litighi per idee diverse. I progetti rischiano di naufragare per mancanza di comunicazione. Impara a scegliere amici che condividano i tuoi valori, e a non pretendere che tutti la pensino come te. La diversità di opinioni può arricchire, se la sai accogliere."
                },
                12: {
                    'armonioso': "Mercurio in Dodicesima Casa illumina la tua mente interiore. Hai un mondo interiore ricco e complesso, e la solitudine è per te un'opportunità per pensare e riflettere. Le tue idee profonde spesso emergono nei momenti di quiete, e hai un'intuizione che va oltre la ragione. Sei portata per la scrittura, la psicologia, la spiritualità. La tua mente è come un lago profondo: calma in superficie, ma piena di vita e mistero.",
                    'dissonante': "Con Mercurio in Dodicesima Casa in aspetto teso, la tua mente può diventare prigioniera di pensieri confusi e angosciosi. Forse porti dentro segreti o parole non dette che ti pesano. La solitudine, invece di essere rigenerante, diventa isolamento. Impara a condividere i tuoi pensieri con chi merita, a non tenere tutto dentro. La tua mente ha bisogno di luce e di aria. Parla, scrivi, confidati. Ne uscirai più leggera."
                }
            },
            
            # 💖 VENERE - IL TUO AMORE, I TUOI VALORI
            'Venere': {
                1: {
                    'armonioso': "Venere nella tua Prima Casa ti rende una donna di un fascino naturale e spontaneo. La tua bellezza è dentro e fuori, e si vede. Hai un modo di fare gentile e accogliente che attira le persone come un magnete. Ami l'amore in tutte le sue forme, e questo ti rende aperta e generosa nelle relazioni. La tua presenza è armoniosa e chi ti incontra si sente subito a suo agio. Sei nata per piacere, ma senza mai essere superficiale.",
                    'dissonante': "Con Venere in Prima Casa in aspetto teso, il tuo desiderio di piacere può diventare una ricerca continua di approvazione. Rischia di perderti dietro l'apparenza, di curare troppo l'immagine trascurando la sostanza. Forse hai paura di non essere abbastanza bella o amabile, e questo ti porta a sforzarti troppo. Ricorda che la vera bellezza è quella che viene da dentro, e che non devi dimostrare niente a nessuno. Tu sei già abbastanza, così come sei."
                },
                2: {
                    'armonioso': "Venere in Seconda Casa illumina il tuo rapporto con i valori e le risorse. Hai un gusto raffinato e sai apprezzare le cose belle della vita. Il denaro per te non è fine a se stesso, ma uno strumento per creare armonia e benessere. Sai gestire le tue risorse con intelligenza e generosità. I tuoi valori sono solidi e ti guidano nelle scelte. La sicurezza materiale per te è importante, ma mai quanto quella del cuore.",
                    'dissonante': "Con Venere in Seconda Casa in aspetto teso, il tuo valore personale può diventare troppo legato ai beni materiali. Rischia di spendere troppo per sentirti all'altezza, o di confondere l'amore con il possesso. Forse hai paura di non avere abbastanza, e questa paura ti porta a essere troppo attaccata alle cose. Ricorda che la vera ricchezza è dentro di te. Le cose belle sono un di più, non l'essenziale."
                },
                3: {
                    'armonioso': "Venere in Terza Casa illumina la tua comunicazione con il cuore. Hai un modo di parlare dolce e armonioso che mette gli altri a proprio agio. Le tue parole sanno consolare, incoraggiare, ispirare. Con le persone vicine, con i fratelli e le sorelle, hai un legame affettuoso e profondo. I viaggi sono occasione di incontri piacevoli. La tua mente è aperta alla bellezza in tutte le sue forme, e sai apprezzare le piccole gioie di ogni giorno.",
                    'dissonante': "Con Venere in Terza Casa in aspetto teso, la comunicazione affettiva può diventare difficile. Rischia di litigare con le persone care per incomprensioni, o di non riuscire a esprimere quello che provi. Le parole ti escono storte, e poi ti dispiace. Impara a scegliere con cura le parole, a usare il cuore prima della testa. Le tue relazioni vicine meritano cura e attenzione. Parla con amore, anche quando è difficile."
                },
                4: {
                    'armonioso': "Venere in Quarta Casa illumina la tua famiglia e le tue radici. La tua casa è un luogo di armonia e bellezza, dove ami accogliere chi vuoi bene. Hai un legame profondo e affettuoso con la tua famiglia, e i ricordi dell'infanzia sono per te preziosi. La figura materna ha trasmesso dolcezza e amore. Le tue radici sono solide e ti danno la sicurezza per affrontare il mondo. La tua anima ha una casa calda dove tornare sempre.",
                    'dissonante': "Con Venere in Quarta Casa in aspetto teso, l'armonia familiare può essere messa a dura prova. Forse ci sono conflitti con i genitori, o tensioni in casa che ti pesano. La tua casa, invece di essere un rifugio, a volte ti sembra un campo di battaglia. Impara a fare pace con la tua storia, a perdonare e a chiedere perdono. La famiglia è importante, ma la tua serenità viene prima di tutto. Costruisci il tuo nido, anche dentro te stessa."
                },
                5: {
                    'armonioso': "Venere in Quinta Casa illumina il tuo amore e la tua creatività. Sei una donna passionale e romantica, e ami con tutto il cuore. I tuoi amori sono intensi e ti fanno vibrare. La creatività è la tua seconda natura: dipingi, scrivi, canti, danzi, o semplicemente rendi speciale ogni momento. I bambini sono una gioia, e con loro hai un rapporto speciale. La vita per te è un'opera d'arte, e tu ne sei l'artista.",
                    'dissonante': "Con Venere in Quinta Casa in aspetto teso, l'amore può diventare fonte di sofferenza. Rischia di amare persone sbagliate, o di vivere storie tormentate. La tua creatività si blocca quando il cuore è ferito. Forse hai paura di non essere amata abbastanza, e questa paura ti porta a essere troppo esigente. Impara a distinguere l'amore vero dalla passione che brucia e consuma. Meriti un amore che ti faccia fiorire, non appassire."
                },
                6: {
                    'armonioso': "Venere in Sesta Casa illumina il tuo lavoro e la tua vita quotidiana. Porti amore e armonia anche nelle piccole cose. Il tuo lavoro lo fai con cura e dedizione, e questo rende felici anche i colleghi. La tua salute è buona perché sai prenderti cura di te con dolcezza. La routine per te non è noiosa, ma un'occasione per creare bellezza ogni giorno. I gesti semplici, fatti con amore, hanno un sapore speciale.",
                    'dissonante': "Con Venere in Sesta Casa in aspetto teso, il lavoro può diventare una fonte di insoddisfazione. Rischia di sentirti sfruttata o non apprezzata. La tua salute può risentirne se accumuli stress e tensioni. Impara a portare più armonia nella tua vita quotidiana, a non trascurare i tuoi bisogni per accontentare gli altri. Il lavoro è importante, ma tu lo sei di più. Prenditi cura di te con la stessa dedizione che metti nel tuo dovere."
                },
                7: {
                    'armonioso': "Venere nella tua Settima Casa è nel suo elemento. Sei fatta per l'amore, per la relazione, per la condivisione profonda. Il partner è per te un compagno di viaggio prezioso, con cui condividere gioie e dolori. Il matrimonio o le unioni importanti sono al centro della tua vita e ti realizzano. Hai un senso della giustizia e dell'equilibrio che rende le tue relazioni armoniose e durature. Amare è la tua vocazione, e lo fai con grazia e generosità.",
                    'dissonante': "Con Venere in Settima Casa in aspetto teso, le relazioni possono diventare fonte di conflitto. Rischia di idealizzare il partner e poi restare delusa, o di pretendere troppo dall'altro. Forse hai paura di essere lasciata, e questa paura ti porta a essere troppo accomodante o, al contrario, troppo esigente. Impara a stare bene anche da sola, e a vedere l'amore come un incontro tra due persone intere, non come un bisogno da colmare. Meriti una relazione che ti rispetti e ti faccia crescere."
                },
                8: {
                    'armonioso': "Venere in Ottava Casa illumina le tue profondità affettive. Ami in modo intenso, totale, senza riserve. La tua passione è profonda e trasformativa. Sei attratta dai misteri dell'amore, dalla sessualità, dall'intimità più vera. Le tue relazioni ti cambiano, ti fanno crescere, ti portano a scoprire parti di te che non conoscevi. Hai una forza interiore che ti permette di affrontare anche le crisi e di trasformarle in opportunità. Il tuo amore è come un fuoco sacro.",
                    'dissonante': "Con Venere in Ottava Casa in aspetto teso, l'amore può diventare ossessivo o tormentato. Rischia di vivere relazioni complicate, fatte di gelosia e possesso. Forse hai paura di perdere chi ami, e questa paura ti porta a stringere troppo. Impara a distinguere l'amore vero dal bisogno di controllo. La fiducia è la base di tutto. Lascia spazio all'altro, e lascia spazio a te stessa. L'amore che libera è più forte di quello che imprigiona."
                },
                9: {
                    'armonioso': "Venere in Nona Casa illumina il tuo amore per il mondo. Sei una donna dall'anima viaggiatrice, aperta a culture diverse, a filosofie che parlano al cuore. I tuoi amori possono arrivare da lontano, da altri paesi, da altre storie. La tua spiritualità è intrisa di bellezza e di amore universale. I viaggi sono per te occasioni di incontri preziosi. La tua mente è aperta e il tuo cuore anche. Ami senza confini, e questo è meraviglioso.",
                    'dissonante': "Con Venere in Nona Casa in aspetto teso, l'idealizzazione dell'amore può portare a delusioni. Rischia di cercare un amore perfetto che non esiste, o di innamorarti di persone lontane e irraggiungibili. I viaggi possono portare incontri che finiscono male. Impara a trovare la bellezza anche nel quotidiano, a vedere l'amore nelle piccole cose. L'ideale è bello, ma la realtà è l'unico posto dove si vive. Ama il mondo, ma ama anche il tuo vicino."
                },
                10: {
                    'armonioso': "Venere in Decima Casa illumina la tua immagine pubblica e la tua carriera. Hai un fascino che ti apre molte porte nel mondo. La tua professionalità è apprezzata e il tuo modo di fare elegante e armonioso conquista tutti. Il successo sociale arriva anche grazie alla tua capacità di piacere e di creare relazioni positive. La tua carriera è importante, ma non ti fa mai dimenticare i valori del cuore. Sai unire ambizione e dolcezza.",
                    'dissonante': "Con Venere in Decima Casa in aspetto teso, la tua immagine pubblica può diventare fonte di ansia. Rischia di preoccuparti troppo di come appari, di cercare l'approvazione a tutti i costi. Forse usi il fascino in modo manipolatorio, o ti senti giudicata per le tue scelte. Impara a distinguere il successo vero dalla semplice apparenza. La tua luce è autentica, non ha bisogno di riflessi. Sii te stessa, e il mondo ti apprezzerà per quello che sei."
                },
                11: {
                    'armonioso': "Venere in Undicesima Casa illumina le tue amicizie e i tuoi sogni. Hai amiche del cuore che sono come sorelle, e con loro condividi amore e affetto. I tuoi progetti sono ispirati dal cuore e spesso coinvolgono gli altri in modo positivo. Sei una donna che ama stare in gruppo, che sa creare armonia e calore tra le persone. I tuoi ideali sono alti e belli, e hai la capacità di realizzarli grazie all'aiuto di chi ti vuole bene.",
                    'dissonante': "Con Venere in Undicesima Casa in aspetto teso, le amicizie possono diventare fonte di delusione. Rischia di confondere l'amicizia con l'amore, o di aspettarti troppo dagli amici. I tuoi progetti possono naufragare per mancanza di concretezza. Impara a distinguere le amicizie vere da quelle di convenienza. I sogni sono belli, ma hanno bisogno di piedi per terra. Condividi i tuoi ideali con chi li merita, e non perdere di vista la realtà."
                },
                12: {
                    'armonioso': "Venere in Dodicesima Casa illumina il tuo amore segreto, quello che porti nel cuore e non sempre mostri. Sei una donna di una sensibilità rara, capace di amare in silenzio, con discrezione e profondità. La tua anima è romantica e sognatrice, e la solitudine è per te un'opportunità per sentire l'amore in modo più puro. Hai un dono per la compassione, per amare chi soffre, per donare senza chiedere nulla in cambio. Il tuo amore è come una perla nascosta: preziosa e rara.",
                    'dissonante': "Con Venere in Dodicesima Casa in aspetto teso, l'amore segreto può diventare fonte di sofferenza. Rischia di amare persone che non ti corrispondono, o di vivere amori impossibili e tormentati. Forse hai paura di mostrare i tuoi sentimenti, e li tieni dentro fino a farti male. Impara a fidarti, a mostrarti per come sei. L'amore vero non ha paura della luce. Condividi il tuo cuore con chi lo merita, e non restare prigioniera dei tuoi silenzi."
                }
            },
            
            # 🔥 MARTE - LA TUA ENERGIA, LA TUA AZIONE
            'Marte': {
                1: {
                    'armonioso': "Marte in Prima Casa ti rende una donna di grande energia e determinazione. Hai una forza interiore che ti spinge ad agire, a non startene mai ferma. Sei coraggiosa, intraprendente, e non hai paura di affrontare le sfide. La tua vitalità è contagiosa e chi ti sta intorno si sente incoraggiato dalla tua grinta. Sai quello che vuoi e vai dritta per la tua strada, senza troppi giri di parole. La tua energia è un dono prezioso.",
                    'dissonante': "Con Marte in Prima Casa in aspetto teso, la tua energia può diventare aggressività. Rischia di essere impulsiva, di reagire prima di pensare, di creare conflitti inutili. Forse hai dentro una rabbia che non sai gestire, e la riversi sugli altri senza volerlo. Impara a incanalare la tua forza in modo costruttivo. Lo sport, l'attività fisica, possono aiutarti a scaricare la tensione. La tua energia è potente, ma ha bisogno di una guida. Impara a dominarla, e diventerà la tua più grande alleata."
                },
                2: {
                    'armonioso': "Marte in Seconda Casa illumina la tua energia dedicata alle risorse. Hai una determinazione che ti aiuta a costruire sicurezza materiale. Sai lottare per quello che vuoi, e non ti arrendi facilmente. Il denaro per te è anche una questione di orgoglio: vuoi guadagnartelo con le tue forze. La tua energia è pratica e concreta, e ti permette di realizzare i tuoi obiettivi economici con tenacia e intelligenza.",
                    'dissonante': "Con Marte in Seconda Casa in aspetto teso, la tua relazione con il denaro può diventare conflittuale. Rischia di spendere in modo impulsivo, di litigare per soldi, di fare investimenti azzardati. Forse hai paura di non avere abbastanza, e questa paura ti porta a decisioni avventate. Impara a gestire le tue risorse con calma, a non prendere decisioni quando sei arrabbiata o ansiosa. La sicurezza viene dalla pazienza, non dalla fretta."
                },
                3: {
                    'armonioso': "Marte in Terza Casa illumina la tua mente energica. Hai idee chiare e le esprimi con passione. La tua comunicazione è diretta e sincera, e non hai paura di dire quello che pensi. Sei curiosa e intraprendente nello studio e nei viaggi. Le discussioni per te sono stimolanti, non conflittuali. La tua energia mentale è una risorsa preziosa che ti aiuta a imparare e a crescere. Sei una donna che sa farsi sentire, ma con intelligenza.",
                    'dissonante': "Con Marte in Terza Casa in aspetto teso, la tua mente può diventare troppo aggressiva. Rischia di essere polemica, di litigare per un nonnulla, di ferire con le parole. Forse ti senti sempre sotto attacco e reagisci prima ancora di capire. Impara a respirare, a contare fino a dieci prima di parlare. Le parole possono essere un'arma, ma anche uno strumento di pace. Scegli di usarle con saggezza. Ascolta più di quanto parli, e vedrai che i conflitti diminuiranno."
                },
                4: {
                    'armonioso': "Marte in Quarta Casa illumina la tua energia dedicata alla famiglia e alla casa. Hai una forza che metti al servizio di chi ami. Sei pronta a lottare per difendere il tuo nido e le persone care. La tua casa è un luogo attivo, dove le cose succedono, dove c'è movimento e vita. L'energia che metti nelle relazioni familiari è intensa e profonda. Sei una leonessa quando si tratta di proteggere chi ami.",
                    'dissonante': "Con Marte in Quarta Casa in aspetto teso, la tua energia in famiglia può diventare conflittuale. Rischia di litigare con i genitori, con i fratelli, con chi vive con te. La casa, invece di essere un rifugio, diventa un campo di battaglia. Forse hai dentro una rabbia antica, legata alla tua storia familiare, che non sei riuscita a elaborare. Impara a fare pace con il passato, a perdonare, a chiedere perdono. La pace in casa inizia dalla pace dentro te stessa."
                },
                5: {
                    'armonioso': "Marte in Quinta Casa illumina la tua energia creativa e amorosa. Sei una donna passionale, che vive l'amore con intensità e slancio. La tua creatività è dinamica e originale. Ti butti nei progetti con entusiasmo e riesci a coinvolgere gli altri. I bambini ti adorano perché sei giocosa e piena di vita. Lo sport, il gioco, il divertimento sono importanti per te e ti aiutano a scaricare l'energia in modo sano. La tua vitalità è contagiosa.",
                    'dissonante': "Con Marte in Quinta Casa in aspetto teso, l'amore può diventare una battaglia. Rischia di vivere storie turbolente, fatte di litigi e passioni esagerate. La tua creatività si blocca quando sei in conflitto. Forse hai paura di non essere amata abbastanza, e questa paura ti porta a essere troppo esigente o possessiva. Impara a distinguere la passione sana dalla rabbia. L'amore vero non è una guerra. Rallenta, respira, e lasciati amare senza difese."
                },
                6: {
                    'armonioso': "Marte in Sesta Casa illumina la tua energia nel lavoro e nella vita quotidiana. Sei una lavoratrice instancabile, che affronta i compiti con grinta e determinazione. La tua salute è buona perché sei attiva e non stai mai ferma. Le sfide quotidiane per te sono stimolanti, e le affronti con coraggio. Il lavoro fisico o che richiede iniziativa è il tuo forte. Sei una donna che non ha paura di metterci le mani.",
                    'dissonante': "Con Marte in Sesta Casa in aspetto teso, il lavoro può diventare fonte di stress e conflitti. Rischia di litigare con i colleghi, di sentirti sfruttata, di accumulare tensione fino a star male. La tua salute può risentirne, con infiammazioni, mal di testa, disturbi nervosi. Impara a rallentare, a delegare, a non voler fare tutto da sola. Il lavoro è importante, ma la tua salute lo è di più. Ascolta il tuo corpo: ti sta dicendo di fermarti."
                },
                7: {
                    'armonioso': "Marte in Settima Casa illumina la tua energia nelle relazioni. Sei una partner appassionata, che si impegna con tutto se stessa nella coppia. Sai lottare per la tua relazione, e questo può essere positivo se la lotta è per costruire, non per distruggere. Nelle associazioni e nelle collaborazioni, porti slancio e iniziativa. La tua energia è al servizio del noi, e questo rende i tuoi legami forti e dinamici.",
                    'dissonante': "Con Marte in Settima Casa in aspetto teso, le relazioni possono diventare un campo di battaglia. Rischia di litigare spesso con il partner, di essere competitiva invece che collaborativa. I conflitti possono portare a separazioni o a rotture. Forse hai paura di perdere la tua identità nella coppia, e reagisci imponendoti. Impara a distinguere l'affermazione di sé dalla prevaricazione. L'amore vero è danza, non lotta. Cerca l'equilibrio tra dare e ricevere."
                },
                8: {
                    'armonioso': "Marte in Ottava Casa illumina la tua energia profonda, quella che viene dall'inconscio. Sei una donna di passioni intense, che vive la sessualità con slancio e vitalità. Hai una forza interiore che ti permette di affrontare le crisi e di trasformarti. Le esperienze forti non ti spaventano, anzi ti aiutano a crescere. La tua energia è come un fiume sotterraneo: scorre potente e inarrestabile. Sai andare a fondo delle cose, e questo è un dono raro.",
                    'dissonante': "Con Marte in Ottava Casa in aspetto teso, le tue energie profonde possono diventare distruttive. Rischia di vivere la sessualità in modo conflittuale, o di essere ossessionata da pensieri di morte e perdita. Le crisi, invece di trasformarti, ti distruggono. Forse hai paura del tuo stesso potere. Impara a conoscere le tue ombre, a far pace con le tue paure. La tua forza è immensa, ma ha bisogno di essere guidata con amore. Non aver paura di chiedere aiuto, se necessario."
                },
                9: {
                    'armonioso': "Marte in Nona Casa illumina la tua energia per gli ideali e i viaggi. Sei una donna che lotta per ciò in cui crede, con passione e convinzione. I tuoi ideali sono importanti e sei pronta a difenderli. I viaggi, specialmente quelli avventurosi, ti attraggono e ti caricano di energia. La tua mente è aperta e coraggiosa, pronta a esplorare nuovi orizzonti. La tua fede, qualunque essa sia, è vissuta con slancio e vitalità.",
                    'dissonante': "Con Marte in Nona Casa in aspetto teso, la tua passione per gli ideali può diventare fanatismo. Rischia di essere intollerante verso chi non la pensa come te, di litigare per questioni di fede o di opinioni. I viaggi possono portare a conflitti o delusioni. Impara ad accettare che la verità ha tante facce. La tua energia è preziosa, ma non deve diventare arma. Cerca il dialogo, non lo scontro. Ascolta prima di giudicare."
                },
                10: {
                    'armonioso': "Marte in Decima Casa illumina la tua energia per la carriera e il successo. Sei una donna ambiziosa e determinata, che non ha paura di lottare per realizzarsi. La tua forza ti porta lontano nel mondo, e il tuo coraggio è riconosciuto e apprezzato. Sai prendere iniziative e guidare gli altri con autorevolezza. La tua carriera è importante e ci metti tutta te stessa. Sei una leader nata, anche se a volte non lo sai.",
                    'dissonante': "Con Marte in Decima Casa in aspetto teso, l'ambizione può diventare una gabbia. Rischia di essere troppo competitiva, di crearti nemici, di bruciare le tappe. I conflitti con i superiori o con i colleghi possono danneggiare la tua carriera. Forse hai paura di non farcela, e questa paura ti porta a essere aggressiva. Impara a rallentare, a collaborare invece di competere. Il successo vero si costruisce con gli altri, non contro gli altri."
                },
                11: {
                    'armonioso': "Marte in Undicesima Casa illumina la tua energia per le amicizie e i progetti. Hai amici con cui condividi passioni e ideali, e insieme a loro ti senti più forte. I tuoi progetti sono ambiziosi e hai la grinta per realizzarli. Sei una donna che sa coinvolgere gli altri, che sa trascinare con il suo entusiasmo. Le battaglie per cause sociali o umanitarie ti vedono in prima linea. La tua energia è al servizio del gruppo, e questo è meraviglioso.",
                    'dissonante': "Con Marte in Undicesima Casa in aspetto teso, le amicizie possono diventare fonte di conflitto. Rischia di litigare con gli amici, di essere troppo competitiva nel gruppo, di imporre le tue idee. I tuoi progetti possono naufragare per tensioni interne. Impara a collaborare, a mettere da parte l'ego per il bene comune. Le differenze possono arricchire, se sai accoglierle. La tua energia è preziosa, ma deve essere condivisa, non imposta."
                },
                12: {
                    'armonioso': "Marte in Dodicesima Casa illumina la tua energia interiore, quella che agisce nel silenzio. Sei una donna che combatte le sue battaglie dentro di sé, con coraggio e determinazione. La tua forza è nascosta, ma non per questo meno potente. Sai affrontare le crisi con risorse interiori che neppure tu conoscevi. Il lavoro dietro le quinte, l'aiuto a chi soffre, l'impegno spirituale sono il tuo campo. La tua energia è come un fiume sotterraneo: invisibile, ma capace di scavare rocce.",
                    'dissonante': "Con Marte in Dodicesima Casa in aspetto teso, la tua energia interiore può diventare autodistruttiva. Rischia di rivoltare la rabbia contro te stessa, di cadere in depressione o di somatizzare i conflitti. Le battaglie nascoste ti consumano senza che tu possa condividerle. Impara a chiedere aiuto, a non tenere tutto dentro. La tua forza è grande, ma anche tu hai bisogno di sostegno. Parla, confidati, esci allo scoperto. La luce guarisce le ferite nascoste."
                }
            },
            
            # ✨ GIOVE - LA TUA FORTUNA, LA TUA ESPANSIONE
            'Giove': {
                1: {
                    'armonioso': "Giove in Prima Casa ti regala un'aura di ottimismo e fiducia che attira le persone. Sei generosa, espansiva, e la tua presenza riempie la stanza. Hai una fede profonda nella vita e questo ti aiuta ad affrontare le difficoltà con leggerezza. La fortuna ti accompagna perché sai cogliere le opportunità con slancio. Sei una donna che sa essere grande senza perdere la dolcezza. La tua gioia di vivere è contagiosa.",
                    'dissonante': "Con Giove in Prima Casa in aspetto teso, il tuo ottimismo può diventare eccessivo. Rischia di sopravvalutarti, di promettere più di quanto puoi mantenere, di essere invadente senza volerlo. Forse hai paura di non essere abbastanza, e questa paura ti porta a gonfiare la tua immagine. Impara a conoscere i tuoi limiti, ad accettarli con umiltà. La vera grandezza non sta nell'apparire, ma nell'essere autentica."
                },
                2: {
                    'armonioso': "Giove in Seconda Casa illumina la tua fortuna materiale. Hai una capacità naturale di attrarre risorse e denaro. La tua generosità si estende anche al portafoglio: sai dare e ricevere con abbondanza. Le opportunità finanziarie ti vengono incontro quando meno te lo aspetti. La sicurezza economica per te è importante, ma non la cerchi con ansia: sai che arriverà al momento giusto. La tua fiducia nella vita si riflette anche nel conto in banca.",
                    'dissonante': "Con Giove in Seconda Casa in aspetto teso, il tuo rapporto con il denaro può diventare problematico. Rischia di spendere troppo, di fare debiti, di vivere al di sopra delle tue possibilità. Forse hai paura di non avere abbastanza, e questa paura ti porta a eccessi opposti. Impara a gestire le risorse con saggezza, a distinguere i bisogni veri dai desideri impulsivi. L'abbondanza vera è anche equilibrio, non solo quantità."
                },
                3: {
                    'armonioso': "Giove in Terza Casa illumina la tua mente generosa. Hai una curiosità infinita e ami condividere quello che impari. Le tue parole sanno ispirare e incoraggiare. I viaggi sono per te occasioni di crescita e di fortuna. Le relazioni con l'ambiente, con i vicini, con i fratelli sono positive e ti sostengono. La tua intelligenza è aperta e tollerante, e questo ti rende una conversatrice piacevole e ricercata.",
                    'dissonante': "Con Giove in Terza Casa in aspetto teso, la tua comunicazione può diventare troppo dispersiva. Rischia di parlare troppo, di promettere cose che non puoi mantenere, di essere superficiale. Forse hai paura di non essere ascoltata, e questo ti porta a esagerare. Impara a scegliere le parole con cura, a concentrarti su ciò che è veramente importante. La qualità conta più della quantità. Ascolta di più, parla di meno."
                },
                4: {
                    'armonioso': "Giove in Quarta Casa illumina la tua famiglia e le tue radici con abbondanza e gioia. La tua casa è un luogo di accoglienza e calore, dove tutti si sentono a proprio agio. La tua famiglia ti sostiene e ti incoraggia. Le eredità, materiali o spirituali, sono per te fonte di fortuna. Hai radici profonde e sane, che ti danno la sicurezza per affrontare il mondo. La tua storia familiare è un tesoro che porti con orgoglio.",
                    'dissonante': "Con Giove in Quarta Casa in aspetto teso, la tua famiglia può diventare fonte di eccessi. Rischia di essere troppo invadente, di caricarti di responsabilità, di creare aspettative troppo alte. Forse hai paura di deludere i tuoi cari, e questo ti porta a sacrificarti troppo. Impara a stabilire confini sani, a dire di no quando serve. La famiglia è importante, ma anche tu lo sei. Trova un equilibrio tra dare e ricevere."
                },
                5: {
                    'armonioso': "Giove in Quinta Casa illumina il tuo amore e la tua creatività con abbondanza e gioia. Sei una donna che ama con tutto il cuore, e il tuo amore è generoso e espansivo. I tuoi figli, se ci sono, sono una fonte di grande felicità e orgoglio. La tua creatività è feconda e riconosciuta. Le speculazioni e i giochi ti portano fortuna. La vita per te è una festa, e tu sei la padrona di casa.",
                    'dissonante': "Con Giove in Quinta Casa in aspetto teso, l'amore e la creatività possono diventare eccessivi. Rischia di amare in modo troppo esuberante, di soffocare i tuoi cari con le attenzioni. Le speculazioni possono portare a perdite se non stai attenta. Forse hai paura di non essere amata abbastanza, e questa paura ti porta a esagerare. Impara a dosare le tue energie, a godere delle cose senza eccessi. La vera gioia sta nell'equilibrio."
                },
                6: {
                    'armonioso': "Giove in Sesta Casa illumina il tuo lavoro e la tua salute con fortuna e benessere. Il lavoro che fai ti piace e ti dà soddisfazione. I colleghi sono collaborativi e l'ambiente è sereno. La tua salute è buona e hai energia da vendere. La routine quotidiana non ti pesa, anzi la vivi con leggerezza. Sei una donna che sa prendersi cura di sé e degli altri con naturalezza e gioia.",
                    'dissonante': "Con Giove in Sesta Casa in aspetto teso, il lavoro può diventare fonte di stress eccessivo. Rischia di assumerti troppe responsabilità, di non riuscire a dire di no, di trascurare la salute per inseguire obiettivi troppo ambiziosi. Forse hai paura di non essere all'altezza, e questa paura ti porta a sovraccaricarti. Impara a rallentare, a delegare, a prenderti cura di te. La salute è il bene più prezioso. Non trascurarla per il lavoro."
                },
                7: {
                    'armonioso': "Giove in Settima Casa illumina le tue relazioni con abbondanza e fortuna. Il partner è per te un compagno di viaggio prezioso, con cui condividere gioie e crescita. Le associazioni e le collaborazioni ti portano benefici e successo. Il matrimonio è felice e duraturo. La giustizia e la legge sono dalla tua parte quando serve. Sei una donna che sa stare con gli altri in modo generoso e costruttivo.",
                    'dissonante': "Con Giove in Settima Casa in aspetto teso, le relazioni possono diventare fonte di eccessi. Rischia di idealizzare troppo il partner, di pretendere troppo, di essere delusa quando le cose non corrispondono alle tue aspettative. Le associazioni possono portare a conflitti legali o a perdite. Impara a vedere le persone per quello che sono, non per quello che vorresti che fossero. L'amore vero accetta i limiti e le imperfezioni."
                },
                8: {
                    'armonioso': "Giove in Ottava Casa illumina le tue profondità con abbondanza e trasformazione positiva. Le eredità, materiali o spirituali, ti arrivano con facilità. La tua capacità di trasformarti e di rinascere è sostenuta dalla fortuna. Le risorse condivise con gli altri sono gestite con saggezza e ti portano benefici. La tua sessualità è vissuta con gioia e apertura. I misteri della vita ti affascinano e ti arricchiscono.",
                    'dissonante': "Con Giove in Ottava Casa in aspetto teso, le questioni profonde possono diventare fonte di conflitto. Rischia di litigare per eredità, di avere problemi con le risorse condivise, di vivere la sessualità in modo problematico. Le trasformazioni, invece di essere positive, ti spaventano. Forse hai paura di perdere il controllo. Impara a fidarti del processo, a lasciar andare ciò che non serve più. La vera ricchezza è anche saper perdere."
                },
                9: {
                    'armonioso': "Giove in Nona Casa illumina la tua mente superiore con abbondanza di idee e di viaggi. Hai una sete di conoscenza che ti porta lontano, e la fortuna ti accompagna in ogni esplorazione. Gli studi superiori ti riescono bene, e la tua saggezza è riconosciuta. I viaggi all'estero sono fonti di gioia e di crescita. La tua fede è solida e ti sostiene. Sei una donna che sa guardare lontano, con ottimismo e fiducia.",
                    'dissonante': "Con Giove in Nona Casa in aspetto teso, le tue convinzioni possono diventare troppo rigide. Rischia di essere dogmatica, di giudicare chi non la pensa come te, di perderti in ideali troppo astratti. I viaggi possono portare delusioni. Forse hai paura di dubitare, e ti aggrappi a certezze che ti limitano. Impara ad accettare il dubbio come parte della crescita. La vera saggezza è anche saper mettere in discussione."
                },
                10: {
                    'armonioso': "Giove in Decima Casa illumina la tua carriera e il tuo successo con abbondanza e riconoscimento. Hai una strada chiara davanti a te e la percorri con fiducia. Il successo sociale arriva e ti dà soddisfazione. Sei riconosciuta per le tue qualità e il tuo lavoro. La tua ambizione è sana e ti porta lontano. Sei una donna che sa farsi strada con grazia e determinazione, e il mondo ti apre le porte.",
                    'dissonante': "Con Giove in Decima Casa in aspetto teso, l'ambizione può diventare eccessiva. Rischia di sacrificare troppo per la carriera, di dimenticare gli affetti, di inseguire il successo a tutti i costi. Forse hai paura di fallire, e questa paura ti porta a sforzarti troppo. Impara a distinguere il successo vero dalla semplice apparenza. La realizzazione più grande è essere in pace con te stessa, non solo con il mondo."
                },
                11: {
                    'armonioso': "Giove in Undicesima Casa illumina le tue amicizie e i tuoi progetti con abbondanza e fortuna. Hai amici preziosi che ti sostengono e ti incoraggiano. I tuoi progetti sono ambiziosi e hanno successo. La vita di gruppo, le associazioni, i movimenti ti portano gioia e soddisfazione. I tuoi ideali sono alti e hai la capacità di realizzarli insieme agli altri. Sei una donna che sa sognare in grande e trasformare i sogni in realtà.",
                    'dissonante': "Con Giove in Undicesima Casa in aspetto teso, le amicizie possono diventare fonte di delusione. Rischia di fidarti troppo di persone sbagliate, di investire in progetti che falliscono, di perderti in ideali troppo vaghi. Forse hai paura di essere sola, e questo ti porta a circondarti di persone che non ti meritano. Impara a scegliere con cura gli amici, a distinguere chi ti vuole bene da chi ti usa. I progetti hanno bisogno di concretezza, non solo di entusiasmo."
                },
                12: {
                    'armonioso': "Giove in Dodicesima Casa illumina la tua vita interiore con abbondanza di saggezza e spiritualità. La solitudine per te non è un peso, ma un'opportunità per crescere interiormente. Hai una fede profonda che ti sostiene nei momenti difficili. Le esperienze di isolamento ti arricchiscono e ti rendono più saggia. Sei portata per la meditazione, la preghiera, la ricerca spirituale. Il tuo mondo interiore è un tesoro nascosto, ma preziosissimo.",
                    'dissonante': "Con Giove in Dodicesima Casa in aspetto teso, la solitudine può diventare fonte di sofferenza. Rischia di isolarti troppo, di perderti in fantasie e illusioni, di trascurare la realtà. Forse hai paura del mondo, e ti rifugi in un castello interiore che diventa prigione. Impara a trovare un equilibrio tra dentro e fuori. La spiritualità è importante, ma anche la vita pratica lo è. Cerca di portare la tua luce interiore nel mondo, a piccoli passi."
                }
            },
            
            # ⏳ SATURNO - LE TUE RESPONSABILITÀ, LA TUA MATURITÀ
            'Saturno': {
                1: {
                    'armonioso': "Saturno in Prima Casa ti rende una donna seria e responsabile, ma non dura. Hai un senso del dovere che ti guida senza opprimerti. Sai cosa vuoi dalla vita e ci lavori con pazienza e costanza. La tua maturità è evidente e le persone si fidano di te perché sanno che non le deluderai. La tua forza interiore è come una roccia, ma il tuo cuore è capace di tenerezza. Sei una donna che sa costruire, pietra su pietra, la propria vita.",
                    'dissonante': "Con Saturno in Prima Casa in aspetto teso, il senso del dovere può diventare un peso. Rischia di essere troppo severa con te stessa, di sentirti sempre inadeguata, di non permetterti mai di sbagliare. Forse hai paura del giudizio degli altri, e questa paura ti blocca. Impara a perdonarti, a concederti il diritto di essere imperfetta. La perfezione non esiste. La tua serietà è una risorsa, ma non deve diventare una prigione. Concediti anche un po' di leggerezza."
                },
                2: {
                    'armonioso': "Saturno in Seconda Casa illumina il tuo rapporto con le risorse con saggezza e pazienza. Sai gestire il denaro con prudenza, senza ansia. Costruisci la tua sicurezza materiale lentamente ma solidamente. I tuoi valori sono chiari e ti guidano nelle scelte. Non hai bisogno di lussi eccessivi, ma apprezzi la qualità e la durata. La tua ricchezza è anche interiore, e questa è la base della tua stabilità.",
                    'dissonante': "Con Saturno in Seconda Casa in aspetto teso, la tua relazione con il denaro può diventare fonte di ansia. Rischia di essere troppo avara, di avere paura di non avere mai abbastanza, di negarti anche le piccole gioie. Forse hai paura della povertà, e questa paura ti porta a stringere troppo. Impara a distinguere la prudenza dall'ansia. La sicurezza vera non viene dall'accumulare, ma dal sentirsi in pace con ciò che si ha."
                },
                3: {
                    'armonioso': "Saturno in Terza Casa illumina la tua mente con profondità e concentrazione. Hai un pensiero chiaro, metodico, che va al cuore delle cose. Studi con pazienza e raggiungi risultati duraturi. Le tue parole sono ponderate e quando parli, la gente ascolta. Le relazioni con l'ambiente sono stabili e profonde. I viaggi che fai sono significativi, non superficiali. La tua intelligenza è come un albero dalle radici profonde.",
                    'dissonante': "Con Saturno in Terza Casa in aspetto teso, la tua mente può diventare troppo rigida. Rischia di essere pessimista, di vedere sempre il lato negativo, di chiuderti a nuove idee. La comunicazione diventa difficile, ti senti incompresa o giudicata. Forse hai paura di sbagliare, e questo ti blocca. Impara ad aprirti, a fidarti del tuo intuito, a lasciar andare il bisogno di controllo. La mente ha bisogno di leggerezza per volare."
                },
                4: {
                    'armonioso': "Saturno in Quarta Casa illumina le tue radici con profondità e stabilità. La tua famiglia è un punto di riferimento solido. Hai imparato dai tuoi genitori il valore della responsabilità e della perseveranza. La tua casa è un luogo sicuro, dove ti senti protetta. Le tradizioni familiari sono importanti per te, ma sai anche innovare con saggezza. La tua storia personale è una base solida su cui costruire il futuro.",
                    'dissonante': "Con Saturno in Quarta Casa in aspetto teso, il rapporto con la famiglia può essere fonte di dolore. Forse hai vissuto un'infanzia difficile, con genitori troppo severi o assenti. La tua casa, invece di essere un rifugio, ti sembra una prigione. Porti dentro un peso che fatichi a lasciare. Impara a fare pace con il passato, a perdonare, a perdonarti. La tua vera casa è dentro di te, e puoi renderla un luogo di pace, qualunque cosa sia successo."
                },
                5: {
                    'armonioso': "Saturno in Quinta Casa illumina il tuo amore e la tua creatività con profondità e serietà. Ami in modo maturo e responsabile, senza superficialità. Le tue relazioni sono durature perché costruite su basi solide. La tua creatività è disciplinata e produce opere che durano nel tempo. I tuoi figli sono importanti e ti prendi cura di loro con dedizione. Il gioco e il piacere non ti spaventano, ma li vivi con consapevolezza.",
                    'dissonante': "Con Saturno in Quinta Casa in aspetto teso, l'amore può diventare fonte di frustrazione. Rischia di avere paura di amare, di sentirti inadeguata, di vivere relazioni troppo serie e prive di gioia. La tua creatività si blocca per paura di sbagliare. Forse hai paura di non essere abbastanza, e questo ti impedisce di lasciarti andare. Impara a giocare, a divertirti, a non prenderti sempre troppo sul serio. L'amore ha bisogno anche di leggerezza."
                },
                6: {
                    'armonioso': "Saturno in Sesta Casa illumina il tuo lavoro e la tua salute con disciplina e metodo. Sei una lavoratrice instancabile, che affronta i compiti con serietà e costanza. La tua salute è buona perché sai prenderti cura di te con regolarità. Le tue abitudini quotidiane sono sane e ti sostengono. Il lavoro per te non è solo un dovere, ma anche un modo per esprimere la tua responsabilità e il tuo impegno. Sei una donna su cui si può sempre contare.",
                    'dissonante': "Con Saturno in Sesta Casa in aspetto teso, il lavoro può diventare fonte di stress e frustrazione. Rischia di sentirti sfruttata, di accumulare troppe responsabilità, di trascurare la salute per inseguire doveri. Forse hai paura di non farcela, e questo ti porta a sovraccaricarti. Impara a delegare, a dire di no, a prenderti pause. La salute è il bene più prezioso. Non sacrificarla per il lavoro."
                },
                7: {
                    'armonioso': "Saturno in Settima Casa illumina le tue relazioni con serietà e profondità. Scegli partner maturi e responsabili, con cui costruire qualcosa di solido. Il matrimonio è per te un impegno serio, che non prendi alla leggera. Le associazioni e le collaborazioni sono durature perché basate su fiducia e rispetto reciproco. Sei una donna che sa stare con gli altri in modo maturo e costruttivo. Le tue relazioni sono come alberi: crescono lentamente, ma diventano forti.",
                    'dissonante': "Con Saturno in Settima Casa in aspetto teso, le relazioni possono diventare fonte di sofferenza. Rischia di scegliere partner difficili, troppo seri o assenti, di vivere relazioni fredde e distanti. Forse hai paura di essere lasciata, e questa paura ti porta a essere troppo rigida o a sopportare situazioni che ti fanno male. Impara a scegliere con il cuore, non solo con la testa. Meriti una relazione che ti scaldi, non che ti raffreddi."
                },
                8: {
                    'armonioso': "Saturno in Ottava Casa illumina le tue profondità con saggezza e trasformazione. Affronti le crisi con maturità e ne esci più forte. Le eredità, materiali o spirituali, sono gestite con responsabilità. La tua sessualità è vissuta in modo maturo e consapevole. Hai una comprensione profonda dei misteri della vita e della morte. Le trasformazioni non ti spaventano, perché sai che sono necessarie per crescere. La tua anima è antica e saggia.",
                    'dissonante': "Con Saturno in Ottava Casa in aspetto teso, le crisi possono diventare fonte di angoscia. Rischia di avere paura della morte, della perdita, del cambiamento. Le questioni di eredità possono essere fonte di conflitti. La tua sessualità può essere vissuta con inibizioni o paure. Forse hai paura di lasciar andare, e ti aggrappi a ciò che dovresti lasciar morire. Impara a fidarti del ciclo della vita. Ogni fine è un nuovo inizio."
                },
                9: {
                    'armonioso': "Saturno in Nona Casa illumina la tua mente superiore con profondità e saggezza. Hai una fede matura, che non è superficiale ma radicata nell'esperienza. I tuoi studi sono approfonditi e raggiungi una vera competenza. I viaggi che fai sono significativi e ti cambiano dentro. Le tue convinzioni sono solide, ma non rigide. Sei una donna che sa guardare lontano con occhi aperti e mente aperta. La tua saggezza è riconosciuta e apprezzata.",
                    'dissonante': "Con Saturno in Nona Casa in aspetto teso, le tue convinzioni possono diventare troppo rigide. Rischia di essere dogmatica, di chiuderti in idee che non ammetti discussioni. La fede può diventare un peso, non una liberazione. I viaggi possono deluderti o essere fonte di difficoltà. Forse hai paura di dubitare, e ti aggrappi a certezze che ti limitano. Impara ad accettare il dubbio come parte della crescita. La vera fede è anche ricerca, non possesso."
                },
                10: {
                    'armonioso': "Saturno in Decima Casa illumina la tua carriera e il tuo successo con solidità e durata. Hai una chiara visione di ciò che vuoi e lavori con costanza per realizzarla. Il successo arriva lentamente, ma è solido e duraturo. Sei riconosciuta per la tua autorità e la tua competenza. La tua carriera è costruita su basi solide e nulla può scalfirla. Sei una donna che sa farsi strada con pazienza e determinazione.",
                    'dissonante': "Con Saturno in Decima Casa in aspetto teso, la carriera può diventare fonte di frustrazione. Rischia di sentirti bloccata, di non vedere riconosciuti i tuoi sforzi, di avere conflitti con l'autorità. Forse hai paura di non farcela, e questa paura ti porta a lavorare troppo o a scoraggiarti facilmente. Impara a essere paziente con te stessa. Il successo vero non è una corsa. Continua a costruire, anche se i risultati tardano. Arriveranno."
                },
                11: {
                    'armonioso': "Saturno in Undicesima Casa illumina le tue amicizie con profondità e fedeltà. Hai pochi amici, ma veri, quelli che restano per sempre. Le tue amicizie sono solide e durature, basate su rispetto e lealtà. I tuoi progetti sono seri e ben pianificati, e li realizzi con costanza. Le persone su cui puoi contare sono poche, ma preziose. Sei una donna che sa scegliere bene le sue compagnie e che non delude mai chi si fida di lei.",
                    'dissonante': "Con Saturno in Undicesima Casa in aspetto teso, le amicizie possono diventare fonte di delusione. Rischia di sentirti sola anche in mezzo alla gente, di avere amici che ti deludono, di non riuscire a fidarti. I tuoi progetti possono essere bloccati o ritardati. Forse hai paura di essere tradita, e questa paura ti porta a isolarti. Impara ad aprirti, a dare fiducia, anche a rischio di sbagliare. La solitudine è una difesa, ma anche una prigione."
                },
                12: {
                    'armonioso': "Saturno in Dodicesima Casa illumina la tua vita interiore con profondità e saggezza. La solitudine per te è un'opportunità per conoscerti a fondo e crescere spiritualmente. Hai una capacità di introspezione rara, che ti porta a comprendere i tuoi limiti e a superarli. Le prove della vita ti rendono più forte e più saggia. Il lavoro nascosto, la preghiera, la meditazione sono il tuo pane quotidiano. La tua anima è come una miniera: più scavi, più tesori trovi.",
                    'dissonante': "Con Saturno in Dodicesima Casa in aspetto teso, la solitudine può diventare fonte di sofferenza. Rischia di sentirti prigioniera dei tuoi pensieri, di portare pesi antichi che non riesci a lasciare, di cadere in depressione. Forse hai paura del mondo, e ti nascondi in un rifugio che diventa prigione. Impara a chiedere aiuto, a condividere i tuoi pesi, a uscire allo scoperto. La luce guarisce anche le ferite più profonde. Non sei sola, anche se a volte ti sembra."
                }
            },
            
                # ⚡ URANO - LA TUA UNICITÀ, LA TUA LIBERTÀ
            'Urano': {
                1: {
                    'armonioso': "Urano nella tua Prima Casa ti rende una donna unica, originale, che non ha paura di essere diversa. La tua personalità è elettrica, imprevedibile, e questo affascina chi ti sta intorno. Hai un bisogno profondo di libertà e di autenticità, e non tolleri di essere incasellata. Le tue idee sono innovative e il tuo modo di essere apre nuove strade. Sei una pioniera, anche senza saperlo. La tua originalità è un dono prezioso per il mondo.",
                    'dissonante': "Con Urano in Prima Casa in aspetto teso, il tuo bisogno di libertà può diventare ribellione fine a se stessa. Rischia di essere impulsiva, di cambiare direzione all'improvviso, di creare instabilità intorno a te. Forse hai paura di essere ingabbiata, e reagisci prima ancora di capire se il pericolo è reale. Impara a distinguere la libertà autentica dalla fuga. La vera indipendenza non è scappare, ma scegliere con consapevolezza dove e con chi stare."
                },
                2: {
                    'armonioso': "Urano in Seconda Casa illumina il tuo rapporto con le risorse in modo originale e innovativo. Hai idee brillanti su come guadagnare e gestire il denaro. La tua sicurezza non dipende tanto dai beni materiali, ma dalla tua libertà interiore. Sai che la vera ricchezza è anche poter essere te stessa. Le tue finanze possono avere alti e bassi, ma la tua capacità di adattarti ti permette di cavartela sempre. Sei una donna che non si fa imprigionare neppure dal denaro.",
                    'dissonante': "Con Urano in Seconda Casa in aspetto teso, la tua relazione con il denaro può essere instabile e imprevedibile. Rischia di fare scelte finanziarie azzardate, di cambiare lavoro all'improvviso, di vivere momenti di incertezza economica. Forse hai paura di essere limitata dalla mancanza di soldi, e questa paura ti porta a decisioni impulsive. Impara a costruire una base di sicurezza senza perdere la tua libertà. L'equilibrio è possibile: stabilità non significa prigione."
                },
                3: {
                    'armonioso': "Urano in Terza Casa illumina la tua mente con idee originali e innovative. Hai un pensiero fuori dagli schemi, che vede possibilità dove altri vedono limiti. La tua comunicazione è elettrica e sai trasmettere entusiasmo per le novità. I tuoi interessi sono vari e spaziano in campi inesplorati. I viaggi che fai sono spesso avventurosi e ti aprono la mente. Sei una donna che sa pensare con la propria testa, senza seguire la massa.",
                    'dissonante': "Con Urano in Terza Casa in aspetto teso, la tua mente può diventare troppo dispersiva e nervosa. Rischia di passare da un'idea all'altra senza concludere nulla, di essere incoerente nella comunicazione, di creare fraintendimenti. I viaggi possono essere turbolenti o pieni di imprevisti. Forse hai paura di annoiarti, e cerchi continue stimoli senza mai fermarti. Impara a concentrare la tua energia, a dare profondità alle tue idee. La novità è bella, ma anche la costanza ha il suo valore."
                },
                4: {
                    'armonioso': "Urano in Quarta Casa illumina la tua famiglia e le tue radici con un'energia innovativa. La tua famiglia è originale, forse diversa dalle convenzioni, e questo ti ha resa una donna aperta e anticonformista. La tua casa è un luogo dove la libertà è di casa, dove ognuno può essere se stesso. Le tue radici sono profonde, ma non ti imprigionano: sai rinnovarti senza perdere la tua storia. Sei una donna che sa onorare il passato senza esserne schiava.",
                    'dissonante': "Con Urano in Quarta Casa in aspetto teso, la tua famiglia può essere fonte di instabilità e cambiamenti improvvisi. Forse hai vissuto separazioni, traslochi frequenti, situazioni familiari turbolente. La tua casa, invece di essere un rifugio, ti sembra un luogo di tensione. Impara a costruire la tua stabilità interiore, indipendentemente dalle circostanze esterne. La vera casa è dentro di te, e può essere un porto sicuro anche in mezzo alla tempesta."
                },
                5: {
                    'armonioso': "Urano in Quinta Casa illumina il tuo amore e la tua creatività con originalità e passione. Ami in modo libero, senza schemi precostituiti. Le tue storie d'amore sono spesso fuori dal comune, e questo le rende emozionanti. La tua creatività è innovativa, capace di sorprendere. I tuoi figli, se ci sono, sono probabilmente bambini originali e indipendenti. Il gioco, il divertimento, la passione sono per te modi per esprimere la tua autenticità. Sei una donna che sa stupire.",
                    'dissonante': "Con Urano in Quinta Casa in aspetto teso, l'amore può diventare fonte di instabilità e imprevisti. Rischia di vivere storie turbolente, di innamorarti di persone inaffidabili, di passare da una relazione all'altra senza trovare pace. La tua creatività può essere discontinua, fatta di slanci e di blocchi. Forse hai paura di legarti, e questa paura ti porta a sabotare le relazioni quando si fanno serie. Impara a distinguere la libertà dalla paura di impegnarti. L'amore vero non imprigiona, libera insieme."
                },
                6: {
                    'armonioso': "Urano in Sesta Casa illumina il tuo lavoro e la tua vita quotidiana con innovazione e originalità. Non sei una che si accontenta della routine: cerchi modi nuovi e creativi di svolgere i tuoi compiti. Il tuo lavoro è spesso in ambiti innovativi, tecnologici, o comunque fuori dagli schemi. La tua salute è legata alla tua libertà: quando sei libera di essere te stessa, stai bene. Sei una donna che porta freschezza e novità anche nelle cose di tutti i giorni.",
                    'dissonante': "Con Urano in Sesta Casa in aspetto teso, il lavoro può essere fonte di instabilità e cambiamenti improvvisi. Rischia di cambiare spesso occupazione, di avere conflitti con i colleghi, di non riuscire a trovare una routine che ti soddisfi. La tua salute può risentirne con disturbi nervosi o improvvisi. Forse hai paura della noia, e questa paura ti porta a cambiare continuamente senza mai costruire. Impara a trovare la libertà anche nella stabilità. La vera novità è spesso dentro, non fuori."
                },
                7: {
                    'armonioso': "Urano in Settima Casa illumina le tue relazioni con originalità e libertà. Cerchi un partner che rispetti la tua indipendenza e che sia aperto a modelli di relazione non convenzionali. Le tue unioni sono spesso fuori dagli schemi: amore libero, relazioni a distanza, convivenze non tradizionali. Questo non significa che siano meno profonde, anzi. Hai bisogno di uno spazio tutto tuo anche nella coppia, e questo è sano. Sei una donna che sa amare senza possedere.",
                    'dissonante': "Con Urano in Settima Casa in aspetto teso, le relazioni possono essere fonte di improvvisi sconvolgimenti. Rischia di attrarre partner instabili o imprevedibili, di vivere separazioni improvvise, di non riuscire a mantenere una relazione stabile. Forse hai paura di perdere la tua libertà, e questa paura ti porta a sabotare i legami quando si fanno stretti. Impara a distinguere la libertà dalla fuga. L'amore vero è quello in cui puoi essere te stessa senza dover scappare."
                },
                8: {
                    'armonioso': "Urano in Ottava Casa illumina le tue profondità con intuizioni improvvise e trasformazioni inaspettate. Hai una capacità quasi magica di percepire ciò che è nascosto, e questo ti rende una psicologa naturale. Le tue trasformazioni interiori sono spesso improvvise e radicali, e ne esci sempre rinnovata. La sessualità per te è anche esplorazione, scoperta, libertà. Sei attratta dai misteri della vita e hai il coraggio di guardare nell'ombra. La tua anima è come un'esploratrice coraggiosa.",
                    'dissonante': "Con Urano in Ottava Casa in aspetto teso, le trasformazioni possono essere vissute come crisi improvvise e traumatiche. Rischia di essere sconvolta da eventi inaspettati legati a eredità, finanze condivise, o crisi profonde. La tua sessualità può essere vissuta in modo conflittuale o disordinato. Forse hai paura di perdere il controllo, e questa paura ti rende ancora più vulnerabile. Impara a fidarti del flusso della vita. Anche le tempeste passano, e dopo c'è sempre un arcobaleno."
                },
                9: {
                    'armonioso': "Urano in Nona Casa illumina la tua mente superiore con idee rivoluzionarie e visioni profetiche. Hai un pensiero originale, che non si accontenta delle verità date. Le tue convinzioni sono tue, non ereditate. I viaggi che fai sono spesso avventurosi e ti aprono a culture e mondi nuovi. La spiritualità per te è ricerca personale, non dogmi. Sei una donna che sa guardare lontano, con occhi che vedono oltre l'orizzonte. Le tue idee sono semi che possono cambiare il mondo.",
                    'dissonante': "Con Urano in Nona Casa in aspetto teso, le tue idee possono diventare troppo radicali o estremiste. Rischia di rifiutare qualsiasi tradizione senza valutarne il valore, di diventare intollerante verso chi non condivide le tue opinioni. I viaggi possono essere fonte di incidenti o imprevisti. Forse hai paura di essere limitata da credenze comuni, e reagisci rifiutando tutto. Impara a distinguere la libertà di pensiero dall'arroganza intellettuale. La vera apertura mentale sa anche ascoltare."
                },
                10: {
                    'armonioso': "Urano in Decima Casa illumina la tua carriera e la tua immagine pubblica con originalità e successo inaspettato. La tua strada professionale è probabilmente fuori dagli schemi, in ambiti innovativi o creativi. Il successo arriva spesso in modo imprevisto, grazie alla tua unicità. La tua immagine pubblica è quella di una donna originale, che non ha paura di distinguersi. Sei un punto di riferimento per chi cerca strade nuove. La tua carriera è la tua opera d'arte.",
                    'dissonante': "Con Urano in Decima Casa in aspetto teso, la carriera può essere fonte di improvvisi sconvolgimenti. Rischia di cambiare lavoro all'improvviso, di avere conflitti con l'autorità, di vedere la tua immagine pubblica messa in discussione da eventi imprevisti. Forse hai paura di essere ingabbiata in un ruolo, e questa paura ti porta a rifiutare anche le opportunità buone. Impara a costruire una carriera che rispetti la tua natura senza dover sempre lottare. La stabilità non è nemica della libertà."
                },
                11: {
                    'armonioso': "Urano in Undicesima Casa illumina le tue amicizie e i tuoi progetti con originalità e innovazione. Hai amici fuori dal comune, spesso persone creative e anticonformiste. I tuoi progetti sono ambiziosi e guardano al futuro. Sei attratta da movimenti sociali, da idee progressiste, da tutto ciò che è nuovo e avanguardistico. In gruppo sei un elemento prezioso, perché porti idee fresche e originali. Sei una donna che sa sognare in grande e coinvolgere gli altri nei suoi sogni.",
                    'dissonante': "Con Urano in Undicesima Casa in aspetto teso, le amicizie possono essere fonte di delusioni e improvvisi cambiamenti. Rischia di attrarre amici inaffidabili, di vedere progetti naufragare per imprevisti, di sentirti tradita da persone di cui ti fidavi. I tuoi ideali possono essere troppo astratti per realizzarsi. Forse hai paura di essere delusa, e questa paura ti porta a non fidarti abbastanza. Impara a scegliere con cura, ma anche a rischiare. Le amicizie vere valgono la pena di essere coltivate, anche se a volte deludono."
                },
                12: {
                    'armonioso': "Urano in Dodicesima Casa illumina la tua vita interiore con intuizioni improvvise e risvegli spirituali. Hai un mondo interiore ricco e originale, dove le idee nascono come lampi. La solitudine per te è un'opportunità per entrare in contatto con la tua parte più profonda e autentica. Le tue intuizioni possono essere quasi profetiche. Sei attratta da studi occulti, da psicologia, da tutto ciò che è nascosto e misterioso. La tua anima è come un cielo stellato: piena di luci improvvise e meravigliose.",
                    'dissonante': "Con Urano in Dodicesima Casa in aspetto teso, la tua vita interiore può diventare fonte di angoscia e confusione. Rischia di essere sopraffatta da pensieri improvvisi e disturbanti, di vivere crisi notturne, di sentirti persa in un labirinto interiore. Forse hai paura del tuo stesso inconscio, e questa paura ti blocca. Impara a fare amicizia con le tue ombre, a conoscerle senza giudicarle. La luce e l'ombra convivono in ognuna di noi. Accettarle entrambe è il primo passo verso la pace."
                }
            },
            
            # 🌊 NETTUNO - LA TUA ANIMA, I TUOI SOGNI
            'Nettuno': {
                1: {
                    'armonioso': "Nettuno nella tua Prima Casa ti rende una donna di una sensibilità quasi magica. Hai uno sguardo che vede oltre, un'intuizione che coglie l'invisibile. La tua presenza è eterea, sognante, e affascina chi ti incontra. Sei empatica, capace di sentire le emozioni altrui come fossero tue. La tua anima è come un lago profondo: calma in superficie, ma piena di vita e di mistero. Sei una donna che sa sognare e che sa far sognare.",
                    'dissonante': "Con Nettuno in Prima Casa in aspetto teso, la tua sensibilità può diventare una gabbia. Rischia di essere troppo ricettiva, di farti assorbire dalle emozioni altrui fino a perdere te stessa. I confini tra te e il mondo si confondono, e ti senti vulnerabile e confusa. Forse hai paura della realtà, e ti rifugi in un mondo di sogni che diventa prigione. Impara a proteggerti, a distinguere ciò che è tuo da ciò che è degli altri. La tua sensibilità è un dono, ma ha bisogno di confini sani per esprimersi."
                },
                2: {
                    'armonioso': "Nettuno in Seconda Casa illumina il tuo rapporto con le risorse con idealismo e ispirazione. Per te, il denaro non è fine a se stesso, ma uno strumento per realizzare sogni e ideali. Hai un'intuizione speciale per gli investimenti creativi o per trovare risorse in modi inaspettati. La tua vera ricchezza è spirituale, e questo ti rende libera dall'attaccamento materiale. Sai che l'abbondanza vera è anche interiore, e questa consapevolezza ti apre le porte a una fortuna inaspettata.",
                    'dissonante': "Con Nettuno in Seconda Casa in aspetto teso, il tuo rapporto con il denaro può diventare confuso e problematico. Rischia di fare scelte finanziarie poco chiare, di essere ingannata, di avere debiti che non riesci a gestire. Forse idealizzi troppo il denaro o lo disprezzi, senza un equilibrio. Impara a distinguere i sogni dalla realtà anche in campo finanziario. La praticità non è nemica della spiritualità. Cerca consigli concreti da persone fidate prima di investire."
                },
                3: {
                    'armonioso': "Nettuno in Terza Casa illumina la tua comunicazione con poesia e ispirazione. Le tue parole sanno toccare il cuore, arrivano dove la logica non arriva. Hai una mente intuitiva che coglie significati profondi dietro le apparenze. La tua scrittura, se ti dedichi, è poetica e suggestiva. I viaggi per te sono anche interiori, e ogni spostamento diventa un'esperienza dell'anima. Sei una donna che sa parlare al cuore delle persone, con dolcezza e sensibilità.",
                    'dissonante': "Con Nettuno in Terza Casa in aspetto teso, la tua comunicazione può diventare confusa e incomprensibile. Rischia di essere fraintesa, di dire cose che non pensi, di creare malintesi. La tua mente può essere annebbiata da sogni e illusioni, e fatichi a concentrarti. Forse hai paura di esprimerti, e ti rifugi in un linguaggio vago e indefinito. Impara a mettere ordine nei tuoi pensieri, a scegliere parole chiare. La poesia è bella, ma anche la chiarezza ha il suo valore. Cerca di esprimere i tuoi sogni in modo che gli altri possano capirli."
                },
                4: {
                    'armonioso': "Nettuno in Quarta Casa illumina la tua famiglia e le tue radici con una luce spirituale. La tua famiglia ha probabilmente una storia particolare, forse legata alla spiritualità, all'arte, o a qualcosa di misterioso. La tua casa è un luogo quasi magico, dove ci si sente avvolti da un'atmosfera speciale. Il rapporto con tua madre è profondo e intenso, forse anche complesso, ma sicuramente significativo. Le tue radici affondano in un terreno fertile di sogni e di memorie. Sei una donna che porta dentro di sé la poesia delle sue origini.",
                    'dissonante': "Con Nettuno in Quarta Casa in aspetto teso, la tua vita familiare può essere fonte di confusione e illusioni. Forse hai vissuto un'infanzia difficile, con genitori assenti o problematici. La tua casa può essere un luogo di conflitti nascosti o di atmosfere pesanti. Il rapporto con tua madre può essere confuso, fatto di aspettative deluse o di dipendenze emotive. Impara a fare chiarezza nella tua storia, a distinguere i fatti dalle tue fantasie. La verità, anche dolorosa, è meglio di una bella bugia. Cerca di costruire la tua casa interiore su fondamenta solide."
                },
                5: {
                    'armonioso': "Nettuno in Quinta Casa illumina il tuo amore e la tua creatività con romanticismo e ispirazione. Ami in modo idealizzato, e questo rende le tue storie d'amore magiche e indimenticabili. La tua creatività è ispirata, quasi divina. Dipingi, scrivi, canti, danzi con l'anima. I tuoi figli, se ci sono, sono probabilmente bambini sensibili e creativi. Il gioco, l'arte, l'amore sono per te vie per entrare in contatto con il divino. Sei una donna che sa trasformare la vita in poesia.",
                    'dissonante': "Con Nettuno in Quinta Casa in aspetto teso, l'amore può diventare fonte di grandi illusioni e delusioni. Rischia di innamorarti di persone che non esistono, di idealizzare partner che poi ti feriscono. La tua creatività può essere discontinua, fatta di slanci e di blocchi. I sogni d'amore si infrangono contro la realtà. Forse hai paura di affrontare la verità, e preferisci illuderti. Impara a distinguere l'amore vero dall'illusione. Le persone reali sono imperfette, e proprio per questo meravigliose. Cerca la bellezza nella realtà, non solo nei sogni."
                },
                6: {
                    'armonioso': "Nettuno in Sesta Casa illumina il tuo lavoro e la tua salute con un tocco di spiritualità e di cura. Hai un dono per prenderti cura degli altri in modo profondo, quasi terapeutico. Il tuo lavoro è spesso in ambiti legati alla guarigione, all'assistenza, alla spiritualità. La tua salute è legata al tuo benessere emotivo: quando sei in pace con te stessa, stai bene. La routine quotidiana può diventare per te una forma di meditazione. Sei una donna che sa trasformare anche i gesti più semplici in atti d'amore.",
                    'dissonante': "Con Nettuno in Sesta Casa in aspetto teso, il lavoro può essere fonte di confusione e stress. Rischia di sentirti sfruttata, di non vedere riconosciuto il tuo impegno, di lavorare in ambienti poco chiari. La tua salute può essere delicata, con disturbi psicosomatici difficili da diagnosticare. Forse hai paura di non farcela, e questa paura ti porta a trascurare te stessa. Impara a distinguere il dare sano dal sacrificio inutile. Prenditi cura di te con la stessa dedizione che riservi agli altri. La tua salute è preziosa, non trascurarla."
                },
                7: {
                    'armonioso': "Nettuno in Settima Casa illumina le tue relazioni con idealismo e romanticismo. Cerchi un partner che sia anche un'anima gemella, con cui condividere sogni e ideali. Le tue unioni sono spesso ispirate, quasi spirituali. Hai una capacità di amare incondizionatamente che è rara e preziosa. Il matrimonio per te è anche un'unione di anime, non solo di corpi. Sei una donna che sa amare con il cuore e con l'anima, e questo rende le tue relazioni profonde e significative.",
                    'dissonante': "Con Nettuno in Settima Casa in aspetto teso, le relazioni possono diventare fonte di grandi illusioni e delusioni. Rischia di idealizzare troppo il partner, di non vedere i suoi difetti, di restare delusa quando la realtà si mostra. Le unioni possono essere confuse, con confini poco chiari. Forse hai paura di affrontare la verità, e preferisci illuderti. Impara a vedere le persone per quello che sono, non per quello che vorresti che fossero. L'amore vero accetta i limiti e le imperfezioni. Cerca una relazione basata sulla realtà, non solo sui sogni."
                },
                8: {
                    'armonioso': "Nettuno in Ottava Casa illumina le tue profondità con intuizioni spirituali e capacità di trascendenza. Hai una connessione profonda con l'invisibile, con l'aldilà, con i misteri della vita e della morte. Le tue esperienze di trasformazione sono spesso accompagnate da una forte componente spirituale. La sessualità per te è anche unione sacra, non solo fisica. Hai un dono per la psicologia del profondo, per comprendere l'anima altrui. La tua anima è come un ponte tra il visibile e l'invisibile.",
                    'dissonante': "Con Nettuno in Ottava Casa in aspetto teso, le tue profondità possono diventare fonte di angoscia e confusione. Rischia di essere ossessionata da pensieri di morte, di perdita, di misteri irrisolti. La sessualità può essere vissuta in modo confuso o colpevolizzante. Le trasformazioni possono essere traumatiche e disorientanti. Forse hai paura del buio dentro di te, e questa paura ti paralizza. Impara a fare pace con le tue ombre, a vedere la luce anche nel buio. La tua profondità è un tesoro, non una minaccia. Cerca di esplorarla con amore, non con paura."
                },
                9: {
                    'armonioso': "Nettuno in Nona Casa illumina la tua mente superiore con visioni spirituali e ideali elevati. Hai una fede profonda, che non è dogma ma esperienza vissuta. La tua spiritualità è personale, intima, e ti guida nella vita. I viaggi che fai sono spesso pellegrinaggi dell'anima, esperienze che ti cambiano dentro. Sei attratta da filosofie orientali, da misticismo, da tutto ciò che trascende il quotidiano. La tua mente è aperta all'infinito. Sei una donna che sa guardare oltre, con occhi che vedono l'invisibile.",
                    'dissonante': "Con Nettuno in Nona Casa in aspetto teso, le tue convinzioni possono diventare fonte di confusione e fanatismo. Rischia di perderti in sette, in ideologie astratte, in sogni irrealizzabili. La tua fede può diventare superstizione. I viaggi possono deluderti o essere fonte di esperienze negative. Forse hai paura del dubbio, e ti aggrappi a certezze illusorie. Impara a distinguere la vera spiritualità dall'illusione. La ricerca della verità è un cammino, non una meta. Accetta il dubbio come parte del percorso."
                },
                10: {
                    'armonioso': "Nettuno in Decima Casa illumina la tua carriera e la tua immagine pubblica con ispirazione e idealismo. La tua professione è spesso legata all'arte, alla spiritualità, all'aiuto agli altri. La tua immagine pubblica è quella di una donna ispirata, che porta un messaggio di amore e di bellezza. Il successo arriva grazie alla tua capacità di connetterti con qualcosa di più grande di te. Sei un punto di riferimento per chi cerca un senso più profondo nella vita. La tua carriera è la tua missione.",
                    'dissonante': "Con Nettuno in Decima Casa in aspetto teso, la tua carriera può essere fonte di illusioni e delusioni. Rischia di essere ingannata nel lavoro, di vedere la tua immagine pubblica offuscata da malintesi, di inseguire sogni di successo che si rivelano vuoti. Forse hai paura di non essere all'altezza, e questa paura ti porta a illuderti o a illudere. Impara a distinguere la vera vocazione dalla semplice fantasia. Il successo autentico è quello che ti realizza, non quello che appare. Cerca di costruire la tua carriera su basi concrete, senza perdere i tuoi ideali."
                },
                11: {
                    'armonioso': "Nettuno in Undicesima Casa illumina le tue amicizie e i tuoi progetti con idealismo e spiritualità. Hai amici che condividono i tuoi sogni e i tuoi ideali più alti. I tuoi progetti sono spesso legati a cause umanitarie, spirituali, artistiche. Ti senti parte di qualcosa di più grande, di una comunità di anime affini. I gruppi che frequenti sono spesso ispirati e ti nutrono profondamente. Sei una donna che sa sognare insieme agli altri, e questo rende i sogni più reali.",
                    'dissonante': "Con Nettuno in Undicesima Casa in aspetto teso, le amicizie possono diventare fonte di delusioni e tradimenti. Rischia di fidarti di persone sbagliate, di essere ingannata da amici, di vedere i tuoi progetti naufragare per illusioni collettive. I gruppi possono essere fonte di confusione e manipolazione. Forse hai paura di essere sola, e questa paura ti porta a cercare compagnie che non ti meritano. Impara a scegliere con cura gli amici, a distinguere chi condivide davvero i tuoi ideali da chi ti usa. La vera amicizia è rara, ma preziosa."
                },
                12: {
                    'armonioso': "Nettuno in Dodicesima Casa è a casa sua. La tua vita interiore è un oceano profondo e misterioso, pieno di tesori nascosti. Hai un dono straordinario per la spiritualità, la meditazione, il contatto con l'invisibile. La solitudine per te è sacra, è il luogo dove incontri la tua anima. Le tue intuizioni sono profetiche, i tuoi sogni pieni di significato. Sei una donna che sa ascoltare il silenzio, e nel silenzio trova la verità. La tua anima è un tempio, e tu ne sei la sacerdotessa.",
                    'dissonante': "Con Nettuno in Dodicesima Casa in aspetto teso, la tua vita interiore può diventare fonte di angoscia e confusione. Rischia di essere sopraffatta da sogni incubi, da paure irrazionali, da sensi di colpa nascosti. La solitudine, invece di essere sacra, diventa isolamento e prigione. Forse hai paura di guardare dentro di te, e questa paura ti rende vulnerabile a ogni tipo di illusione. Impara a fare luce nelle tue ombre, a distinguere la vera spiritualità dalla fuga. Cerca un aiuto, se necessario. La tua anima merita di essere esplorata con amore, non con paura."
                }
            },
            
            # 🔥 PLUTONE - LA TUA TRASFORMAZIONE, IL TUO POTERE
            'Plutone': {
                1: {
                    'armonioso': "Plutone nella tua Prima Casa ti rende una donna di un potere e di una profondità straordinarie. Hai una forza interiore che ti permette di trasformare te stessa e la tua vita più e più volte. La tua presenza è magnetica, intensa, e chi ti incontra lo sente. Non hai paura di guardare dentro di te, di scavare fino a trovare la verità. Le crisi per te sono opportunità di rinascita. Sei come la fenice: sai risorgere dalle tue ceneri, ogni volta più forte e più bella.",
                    'dissonante': "Con Plutone in Prima Casa in aspetto teso, il tuo potere può diventare distruttivo, per te e per gli altri. Rischia di essere troppo intensa, di vivere ogni cosa come una lotta, di vedere nemici dappertutto. Le tue trasformazioni possono essere traumatiche, vissute come crisi devastanti. Forse hai paura del tuo stesso potere, e questa paura ti porta a usarlo male o a reprimerlo. Impara a conoscere la tua forza, a usarla con saggezza e amore. Il vero potere è quello che serve, non quello che distrugge. Cerca di trasformare te stessa senza distruggerti."
                },
                2: {
                    'armonioso': "Plutone in Seconda Casa illumina il tuo rapporto con le risorse con profondità e potere trasformativo. Hai una capacità di gestire il denaro e i beni con intelligenza e determinazione. Le tue risorse possono trasformarsi radicalmente nel corso della vita, e tu sai adattarti. Sei attratta dagli investimenti profondi, da ciò che ha valore duraturo. La tua sicurezza non è solo materiale, ma anche psicologica: sai che la vera ricchezza è dentro di te. Sei una donna che sa costruire e ricostruire, anche economicamente.",
                    'dissonante': "Con Plutone in Seconda Casa in aspetto teso, il tuo rapporto con il denaro può diventare fonte di conflitti e crisi. Rischia di perdere tutto e di dover ricominciare, di litigare per eredità, di vivere momenti di grave insicurezza materiale. Forse hai paura di non avere abbastanza, e questa paura ti porta a essere troppo attaccata o a fare scelte azzardate. Impara a distinguere il valore vero da quello apparente. Le crisi economiche possono essere opportunità per capire cosa conta davvero. La tua vera ricchezza è dentro di te, e nessuno può portartela via."
                },
                3: {
                    'armonioso': "Plutone in Terza Casa illumina la tua mente con profondità e potere di indagine. Hai un'intelligenza che va a fondo, che scava, che scopre verità nascoste. La tua comunicazione è potente, magnetica, e le tue parole possono trasformare chi ti ascolta. Sei attratta dalla psicologia, dal mistero, da tutto ciò che è nascosto. Le tue idee hanno il potere di cambiare il modo di pensare degli altri. Sei una donna che sa andare oltre le apparenze, che vede ciò che gli altri non vedono.",
                    'dissonante': "Con Plutone in Terza Casa in aspetto teso, la tua mente può diventare ossessiva e distruttiva. Rischia di fissarti su pensieri negativi, di usare le parole come armi, di creare conflitti con la tua intensità. Le tue indagini possono diventare morbose. Forse hai paura di essere ingannata, e questa paura ti porta a sospettare di tutti. Impara a usare il tuo potere mentale con saggezza, a distinguere l'indagine sana dalla paranoia. La verità è importante, ma anche la fiducia lo è. Cerca un equilibrio tra il vedere e il credere."
                },
                4: {
                    'armonioso': "Plutone in Quarta Casa illumina la tua famiglia e le tue radici con profondità e trasformazione. La tua storia familiare è segnata da eventi profondi, forse anche drammatici, ma che ti hanno resa la donna forte che sei. Hai un legame intenso con le tue origini, e porti dentro di te la forza dei tuoi antenati. La tua casa è un luogo di trasformazione, dove le crisi diventano opportunità di crescita. Sei una donna che sa trasformare il dolore della propria storia in forza e saggezza.",
                    'dissonante': "Con Plutone in Quarta Casa in aspetto teso, la tua famiglia può essere fonte di profondi conflitti e traumi. Forse hai vissuto situazioni difficili in famiglia, perdite, abusi, segreti inconfessabili. Le tue radici sono intrise di dolore. La casa, invece di essere un rifugio, è un luogo di tensione. Impara a fare pace con la tua storia, a perdonare, a lasciar andare. Il passato non si può cambiare, ma puoi trasformare il modo in cui lo porti. Cerca di costruire la tua casa interiore su nuove fondamenta, più sane e più forti."
                },
                5: {
                    'armonioso': "Plutone in Quinta Casa illumina il tuo amore e la tua creatività con passione e potere trasformativo. Ami in modo totale, profondo, e le tue storie d'amore ti cambiano per sempre. La tua creatività è potente, capace di creare opere che toccano l'anima. I tuoi figli, se ci sono, sono probabilmente bambini intensi e profondi. Il gioco, l'arte, l'amore sono per te modi per esprimere il tuo potere creativo. Sei una donna che sa amare con tutta se stessa, e questo rende il tuo amore indimenticabile.",
                    'dissonante': "Con Plutone in Quinta Casa in aspetto teso, l'amore può diventare una fonte di ossessione e conflitto. Rischia di vivere passioni tormentate, di essere possessiva, di soffrire per amore in modo devastante. La tua creatività può essere bloccata da conflitti interiori. I figli possono essere fonte di preoccupazioni profonde. Forse hai paura di perdere l'amore, e questa paura ti porta a stringere troppo. Impara a distinguere l'amore vero dal bisogno di possesso. L'amore che libera è più forte di quello che imprigiona. Cerca di amare senza possedere."
                },
                6: {
                    'armonioso': "Plutone in Sesta Casa illumina il tuo lavoro e la tua salute con profondità e potere di trasformazione. Il tuo lavoro è spesso in ambiti che richiedono di andare a fondo: medicina, psicologia, ricerca. La tua salute è legata alla tua capacità di trasformare le tensioni. Sei una lavoratrice instancabile quando credi in ciò che fai. Le crisi sul lavoro sono per te opportunità per cambiare e crescere. Sei una donna che sa trasformare anche le fatiche quotidiane in occasioni di evoluzione.",
                    'dissonante': "Con Plutone in Sesta Casa in aspetto teso, il lavoro può diventare fonte di stress e conflitti profondi. Rischia di essere sopraffatta dalle responsabilità, di litigare con colleghi, di vivere situazioni lavorative difficili e oppressive. La tua salute può risentirne con disturbi profondi e difficili da diagnosticare. Forse hai paura di perdere il controllo, e questa paura ti porta a lavorare troppo o a bloccarti. Impara a distinguere l'impegno sano dall'ossessione. La salute è il bene più prezioso. Cerca di trovare un lavoro che sia anche guarigione, non solo fatica."
                },
                7: {
                    'armonioso': "Plutone in Settima Casa illumina le tue relazioni con profondità e potere trasformativo. I tuoi partner sono spesso persone intense che ti cambiano profondamente. Le tue unioni non sono mai superficiali: sono esperienze di trasformazione reciproca. Il matrimonio o le collaborazioni importanti ti portano a confrontarti con le tue parti più profonde. Attraverso l'altro, scopri te stessa. Sei una donna che sa che l'amore vero è anche un viaggio nell'anima, insieme.",
                    'dissonante': "Con Plutone in Settima Casa in aspetto teso, le relazioni possono diventare fonte di conflitti profondi e distruttivi. Rischia di attrarre partner ossessivi o manipolatori, di vivere relazioni di potere, di subire o infliggere violenza psicologica. Le unioni possono trasformarsi in gabbie. Forse hai paura di perdere te stessa nella relazione, e questa paura ti porta a lottare per il controllo. Impara a distinguere l'intimità sana dalla fusione malata. L'amore vero è quello in cui entrambi potete essere liberi. Cerca un partner che ti rispetti e con cui poter crescere, non distruggerti."
                },
                8: {
                    'armonioso': "Plutone in Ottava Casa è a casa sua. Hai un accesso privilegiato alle tue profondità, ai misteri della vita e della morte. La tua capacità di trasformazione è straordinaria: attraversi le crisi come una farfalla che esce dal bozzolo. La sessualità per te è sacra, un'esperienza di unione profonda e trasformativa. Sei attratta dalla psicologia, dall'occulto, da tutto ciò che è nascosto. Le eredità, materiali e spirituali, sono importanti nella tua vita. La tua anima è un'esploratrice degli abissi, e torna sempre in superficie con tesori preziosi.",
                    'dissonante': "Con Plutone in Ottava Casa in aspetto teso, le tue profondità possono diventare fonte di angoscia e distruzione. Rischia di essere ossessionata dalla morte, di vivere crisi profonde e traumatiche, di avere rapporti sessuali conflittuali o pericolosi. Le eredità possono essere fonte di conflitti e dolori. Forse hai paura del tuo stesso potere distruttivo, e questa paura ti paralizza. Impara a conoscere le tue ombre senza farti divorare. La tua profondità è un tesoro, ma va esplorata con cura e amore. Cerca un aiuto se necessario, per trasformare le tue paure in forza."
                },
                9: {
                    'armonioso': "Plutone in Nona Casa illumina la tua mente superiore con profondità e potere di trasformazione. Le tue convinzioni sono il frutto di profonde ricerche interiori. La tua fede è vissuta in modo intenso e trasformativo. I viaggi che fai sono spesso esperienze che ti cambiano radicalmente. Sei attratta da filosofie profonde, da studi che vanno al cuore delle cose. La tua mente è come un archeologo: scava, scava, fino a trovare verità antiche e preziose. Sei una donna che sa che la verità va cercata in profondità.",
                    'dissonante': "Con Plutone in Nona Casa in aspetto teso, le tue convinzioni possono diventare fonte di fanatismo e distruzione. Rischia di essere dogmatica, intollerante, di usare le tue idee come armi. La fede può diventare ossessione. I viaggi possono portare a esperienze traumatiche. Forse hai paura del dubbio, e ti aggrappi a verità assolute che ti imprigionano. Impara a distinguere la ricerca della verità dalla imposizione della tua verità. La vera saggezza è anche umiltà. Accetta che la verità ha tante facce, e che ognuno ha il diritto di cercare la sua."
                },
                10: {
                    'armonioso': "Plutone in Decima Casa illumina la tua carriera e la tua immagine pubblica con profondità e potere. La tua professione è spesso legata a trasformazioni profonde: psicologa, guaritrice, ricercatrice, leader in momenti di crisi. Il tuo successo è costruito su esperienze profonde e trasformative. La tua immagine pubblica è quella di una donna potente, capace di affrontare le crisi e di uscirne più forte. Sei un punto di riferimento nei momenti difficili. La tua carriera è la tua missione, e la svolgi con intensità e passione.",
                    'dissonante': "Con Plutone in Decima Casa in aspetto teso, la carriera può diventare fonte di conflitti di potere e crisi distruttive. Rischia di essere coinvolta in lotte per il potere, di vedere la tua immagine pubblica distrutta da scandali, di vivere momenti di grande instabilità professionale. Forse hai paura di fallire, e questa paura ti porta a lottare in modo distruttivo. Impara a distinguere l'ambizione sana dalla brama di potere. Il vero successo è quello che ti realizza, non quello che ti distrugge. Cerca di costruire una carriera che sia in armonia con la tua anima, non contro di essa."
                },
                11: {
                    'armonioso': "Plutone in Undicesima Casa illumina le tue amicizie e i tuoi progetti con profondità e potere trasformativo. Hai amici intensi e profondi, con cui condividi esperienze che ti cambiano. I tuoi progetti sono spesso ambiziosi e trasformativi, capaci di incidere sulla società. Sei attratta da movimenti sociali profondi, da cambiamenti radicali. In gruppo, la tua presenza è potente e trasformativa. Sei una donna che sa che insieme si può cambiare il mondo, e ci mette tutta la sua forza.",
                    'dissonante': "Con Plutone in Undicesima Casa in aspetto teso, le amicizie possono diventare fonte di tradimenti e conflitti profondi. Rischia di essere coinvolta in giochi di potere nei gruppi, di essere manipolata da amici, di vedere i tuoi progetti distrutti da lotte interne. I tuoi ideali possono diventare fonte di scontri. Forse hai paura di essere esclusa, e questa paura ti porta a lottare in modo distruttivo per mantenere il tuo posto. Impara a distinguere le alleanze sane dalle dinamiche di potere. Le vere amicizie sono quelle che ti sostengono, non che ti usano. Cerca di collaborare senza competere."
                },
                12: {
                    'armonioso': "Plutone in Dodicesima Casa illumina la tua vita interiore con profondità e potere trasformativo nascosto. Hai un accesso privilegiato al tuo inconscio, e puoi trasformare le tue ombre in luce. La solitudine per te è un'opportunità per incontrare le tue profondità e guarire antiche ferite. Sei attratta dalla psicologia del profondo, dai misteri dell'anima. Le tue crisi interiori sono opportunità di rinascita. La tua anima è come una miniera: più scavi, più tesori trovi. Sei una donna che sa trasformare il dolore in saggezza, nel silenzio del suo cuore.",
                    'dissonante': "Con Plutone in Dodicesima Casa in aspetto teso, la tua vita interiore può diventare fonte di angoscia e autodistruzione. Rischia di essere sopraffatta da paure profonde, da sensi di colpa nascosti, da pensieri ossessivi che ti tormentano. La solitudine diventa isolamento e prigione. Forse hai paura di guardare dentro di te, e questa paura ti rende vulnerabile a ogni tipo di ombra. Impara a fare luce nelle tue tenebre, a poco a poco, con amore e pazienza. Cerca un aiuto, se necessario. La tua anima merita di essere esplorata con cura, non con paura. La trasformazione è possibile, anche nel buio più profondo."
                }
            },
        }
                
        # ============================================
        # MESSAGGI PER LE CONGIUNZIONI RADIX
        # ============================================
        self.messaggi_radix = {
            # LUNA
                'luna_marte': {
                'congiunzione': {
                    'titolo': "🌙⚡ Luna congiunta a Marte",
                    'messaggio': "Le tue emozioni sono intense, impulsive e a volte esplosive...",
                    'consiglio': "🛑 Prima di reagire, fermati un attimo e chiediti: 'È vero quello che sento o è la mia immaginazione?'..."
                }
            },
                                        
            'luna_venere': {
                'congiunzione': {
                    'titolo': "🌙❤️ Luna congiunta a Venere",
                    'messaggio': "Sei una persona semplice, calorosa e senza pretese. Metti gli altri a loro agio e rompi il ghiaccio con naturalezza. Sei molto sensibile alla durezza e ai modi aspri, e soffri quando li incontri. Cerchi l'armonia con tutti e sei apprezzato per questo, ma attento a non sembrare troppo 'gentile' o ad adulare troppo. Nei rapporti sei romantico e ti leghi facilmente, ma a volte ti impegni prima di essere davvero pronto. In amore, con il tempo, troverai l'equilibrio tra dare e ricevere.",
                    'consiglio': "🌸 Sii gentile, ma non esagerare. Lascia spazio anche agli altri per esprimere la loro simpatia. In amore, concediti il tempo di conoscere davvero l'altro prima di legarti."
                }
            },
            'luna_mercurio': {
                'congiunzione': {
                    'titolo': "🌙💬 Luna congiunta a Mercurio",
                    'messaggio': "Hai una mente vivace e un cuore grande. Sei curioso, ami imparare e la tua immaginazione è fervida. Impari più dall'esperienza che dai libri, anche se hai una buona capacità di studio. Sei una persona comprensiva e compassionevole, e gli altri si confidano volentieri con te perché si sentono ascoltati e capiti. A volte fatichi a distinguere tra ciò che senti e ciò che pensi, e questo può creare un po' di confusione. Sei molto sensibile alle critiche e tendi a interpretare le reazioni altrui in modo troppo personale. Come genitore sei affettuoso e presente, e i giovani si trovano bene con te.",
                    'consiglio': "📝 Scrivi ciò che senti e ciò che pensi: ti aiuterà a distinguere le emozioni dalla ragione. E ricorda: ascoltare è un dono, ma non devi farti carico di tutto."
                }
            },
            'luna_urano': {
                'congiunzione': {
                    'titolo': "🌙⚡ Luna congiunta a Urano",
                    'messaggio': "Hai un carattere forte e una personalità unica. Sai esprimerti con chiarezza, specialmente quando sei emotivamente coinvolto. Preferisci la trasparenza e non ami tenere segreti, perché ti pesano. Sei tollerante e comprensivo con gli amici, e cerchi sempre di vedere il buono in entrambe le parti di una discussione. Sei ottimista e aiuti gli altri a sentirsi meglio, ma fai più fatica a risolvere i tuoi problemi. In amore sei attratto da persone 'impossibili' e fuori dagli schemi. Quando ami, ami in modo totale, e soffri profondamente se non sei ricambiato. Hai bisogno della tua libertà e vuoi vivere a modo tuo.",
                    'consiglio': "🌀 Cerca di applicare a te stesso la stessa comprensione che offri agli altri. In amore, non cercare la persona perfetta, ma qualcuno con cui puoi essere semplicemente te stesso."
                }
            },
            'luna_plutone': {
                'congiunzione': {
                    'titolo': "🌙🔥 Luna congiunta a Plutone",
                    'messaggio': "Hai una grande capacità di amare, in modo profondo e costante. Non ami le avventure fuggevoli: cerchi l'anima gemella, qualcuno che sappia amare con la tua stessa intensità. Le amicizie superficiali ti infastidiscono. Con gli anni sviluppi un 'sesto senso' per riconoscere chi cerca solo rapporti casuali. La tua vita sentimentale può essere un alternarsi di incontri profondi e delusioni, ma quando trovi il vero amore, vivi un'appagamento totale. A volte scopri troppo tardi che un amore del passato era quello vero. Sei vulnerabile e questo ti mette sulla difensiva, ma anche tu puoi, senza volere, ferire gli altri.",
                    'consiglio': "🌋 Impara a distinguere ciò che è importante da ciò che non lo è. Non avere paura di amare profondamente, ma dai tempo al tempo per capire se è la persona giusta."
                }
            },
            'luna_saturno': {
                'congiunzione': {
                    'titolo': "🌙⏳ Luna congiunta a Saturno",
                    'messaggio': "Sei una persona riservata, prudente e spesso in apprensione. Probabilmente hai avuto un'infanzia con genitori molto severi, e questo ti ha reso pessimista e diffidente. Fatichi a stringere legami affettivi e tendi ad aspettarti sempre il peggio. Sul lavoro, però, sei efficiente, onesto e serio. Pretendi molto da te stesso e dagli altri. Sei un buon direttore, giusto ma esigente. In amore cerchi persone mature e serie, e per te il rispetto reciproco è fondamentale. Spesso trascuri la tua salute fisica e mentale, accumulando tensioni.",
                    'consiglio': "🌱 Cerca di vedere il lato positivo della vita. Non è colpa tua se l'infanzia è stata dura, ma puoi scegliere di non lasciare che condizioni il tuo futuro. Concediti del tempo per rilassarti e non essere troppo duro con te stesso."
                }
            },
            'luna_giove': {
                'congiunzione': {
                    'titolo': "🌙✨ Luna congiunta a Giove",
                    'messaggio': "Hai una grande sensibilità per ciò che ti circonda e un forte desiderio di aiutare gli altri. Sei generoso, aperto e sempre pronto a dare una mano. Hai una fede incrollabile che tutto possa risolversi per il meglio. Ti dedichi con passione a opere sociali, beneficenza, o ad aiutare chi è in difficoltà. Sei amato e stimato da famiglia, amici e anche da sconosciuti che hai aiutato. Hai una grande capacità di infondere speranza. Il tuo unico difetto è che non ti fermi mai e rischi di esaurirti.",
                    'consiglio': "🌟 Continua a dare, ma ricordati di ricaricare le batterie. Anche tu hai bisogno di riposo e di cure. Non sentirti in colpa se ogni tanto ti rilassi: lo fai per poter dare ancora di più dopo."
                }
            },
            'luna_nettuno': {
                'congiunzione': {
                    'titolo': "🌙🌊 Luna congiunta a Nettuno",
                    'messaggio': "Sei una persona molto immaginativa, emotiva e sensibile. Hai capacità psichiche e percepisci il mondo in modo diverso dagli altri. Sei sensibile alle difficoltà altrui e offri volentieri aiuto e consiglio, ma spesso gli altri si dimenticano di te quando stanno bene. Sul lavoro, hai bisogno di stimoli e sfide; i lavori monotoni ti fanno cadere nei sogni a occhi aperti e rischi di essere giudicato incompetente. In amore sei un romantico idealista: ti crei un'immagine perfetta della persona amata e soffri quando la realtà si manifesta. Hai un grande talento artistico che può darti grandi soddisfazioni.",
                    'consiglio': "🎨 Usa la tua immaginazione nell'arte: dipingi, scrivi, suona. Impara ad accettare le persone per quello che sono, con i loro pregi e difetti. Solo così potrai essere apprezzato per la tua vera comprensione."
                }
            },
            
            # SOLE
            'sole_plutone': {
                'congiunzione': {
                    'titolo': "☀️🔥 Sole congiunto a Plutone",
                    'messaggio': "Hai una personalità potente e magnetica. Sei un estremista: quando ami, ami in modo totale; quando odi, allo stesso modo. La tua ambizione è profonda e vuoi lasciare un segno nel mondo. Non ti accontenti della mediocrità e sei disposto a lottare per ciò in cui credi. Hai un forte senso della giustizia e ti batti per i deboli e gli oppressi. Sul lavoro puoi essere un leader naturale, ma attento a non diventare troppo autoritario o a voler dominare gli altri. La tua energia sessuale è intensa e il rifiuto per te è inaccettabile. Se impari a usare questa forza in modo costruttivo, puoi raggiungere vette altissime.",
                    'consiglio': "🦁 Usa il tuo potere per costruire, non per distruggere. La vera forza sta nel sollevare gli altri, non nel dominarli."
                }
            },
            'sole_nettuno': {
                'congiunzione': {
                    'titolo': "☀️🌊 Sole congiunto a Nettuno",
                    'messaggio': "Hai difficoltà a esprimerti con sicurezza perché non hai molta fiducia in te stesso. Le tue vedute sulla vita sono vaghe, e questo ti aiuta a evitare situazioni spiacevoli e responsabilità. Sei molto creativo, specialmente nell'arte, nella musica, nella poesia. Hai una qualità mistica che ti distingue. Hai bisogno di un lavoro che ti permetta di esprimere la tua creatività, altrimenti ti senti intrappolato. Vai bene in pubblicità, design, medicina, assistenza sociale. È importante che impari ad affrontare la realtà così com'è, anche se a volte fa male. Un consigliere di fiducia può esserti di grande aiuto.",
                    'consiglio': "🎨 Cerca una professione che ti permetta di esprimere la tua creatività. Non fuggire dalla realtà: affrontala con l'aiuto di qualcuno di cui ti fidi."
                }
            },
            'sole_ascendente': {
                'congiunzione': {
                    'titolo': "☀️⬆️ Sole congiunto all'Ascendente",
                    'messaggio': "Hai un forte bisogno di essere notato e trovi modi ingegnosi per attirare l'attenzione. Sei molto sicuro di te e della tua identità, forse anche troppo, al punto da non capire cosa questo significhi per gli altri. Sei intransigente perché temi di doverti sottomettere. Hai grande stima di te e delle tue capacità. Sai come usare le tue doti creative e, sicuro del successo, affronti gli avversari in modo diretto. Se incontri resistenza, puoi diventare anche molto duro. Sai farti amici e influenzare le persone, ma ti stupisci quando qualcuno non si lascia conquistare. Hai bisogno di un lavoro che ti dia autorità.",
                    'consiglio': "👑 La tua sicurezza è un grande dono, ma ricorda che non tutti sono come te. Usa la tua influenza per costruire ponti, non muri. Sii aperto a chi la pensa diversamente."
                }
            },
            'sole_urano': {
                'congiunzione': {
                    'titolo': "☀️⚡ Sole congiunto a Urano",
                    'messaggio': "Hai piena coscienza di te e delle tue capacità. Ti senti a tuo agio nel mondo e ti esprimi in modo anticonvenzionale, senza curarti di chi ti giudica eccentrico. Hai una personalità spiccata e difendi gelosamente la tua libertà e individualità. Se qualcuno tenta di limitarti, combatti per i tuoi diritti. Non sopporti le imposizioni della società e della tradizione. Da bambino eri già difficile da tenere a freno. Raggiungi presto la maturità intellettuale. Il tuo lavoro deve concederti libertà di azione; la carriera è quasi senza limiti in politica, scienza, insegnamento, tecnica. Hai idee progressiste e il tuo contributo è prezioso. Hai bisogno di un partner con i piedi per terra che ti stabilizzi.",
                    'consiglio': "🌟 La tua libertà è sacra, ma ricordati che anche le ali hanno bisogno di un punto d'appoggio per spiccare il volo. Cerca persone che ti ancano alla realtà senza imprigionarti."
                }
            },
            'sole_saturno': {
                'congiunzione': {
                    'titolo': "☀️⏳ Sole congiunto a Saturno",
                    'messaggio': "Sei una persona seria, con un profondo senso di responsabilità. Ogni esperienza per te è una lezione. Non sopporti di essere usato, ma sei pronto a caricarti di pesi e doveri. La vita per te è una dura lotta. Sei maturato presto, probabilmente a causa di una disciplina molto severa nell'infanzia. Conti solo sulle tue forze e sei diffidente verso gli aiuti esterni. Sei abile nello sfruttare le occasioni per la scalata al successo. Parli solo se hai buone ragioni per farlo. Sei tenace e ostinato. Hai successo in campi come direzione, insegnamento, politica, ricerca, legge. Il tuo problema è reagire male agli insuccessi e cadere nel vittimismo. Devi imparare a rilassarti e a vedere il lato positivo.",
                    'consiglio': "🌱 Hai imparato a essere forte da solo, ma non devi portare il mondo sulle spalle. Concediti delle pause, impara a perdonarti gli errori e a vedere la bellezza nella leggerezza."
                }
            },
            'sole_giove': {
                'congiunzione': {
                    'titolo': "☀️✨ Sole congiunto a Giove",
                    'messaggio': "Non riesci quasi mai ad agire con moderazione. Metti entusiasmo in tutto e hai la certezza di non fallire. Questa fiducia assoluta ti porta a volte a sopravvalutarti e a subire delusioni, ma ti rialzi subito e ricominci. Spesso la fortuna ti aiuta nei momenti di bisogno. Non sei mosso dall'ambizione, ma dal desiderio di vivere una vita piena. Sei generoso all'eccesso e per questo fatichi a risparmiare. Vai bene in professioni che offrono crescita ed espansione: medicina, legge, filosofia, insegnamento, viaggi. Ti annoiano i lavori di routine. Hai una grande fede, anche se non segui i riti tradizionali. Sei un po' un 'glossone' emotivo e fatichi a trovare un partner che ti soddisfi pienamente. Il tuo problema è la mancanza di moderazione, che può logorarti.",
                    'consiglio': "🌟 Il tuo entusiasmo è contagioso, ma impara a dosarlo. Fai dei programmi più realistici e ricordati di risparmiare un po' di energie e denaro per il futuro. La salute ringrazierà."
                }
            },
            'sole_mercurio': {
                'congiunzione': {
                    'titolo': "☀️💬 Sole congiunto a Mercurio",
                    'messaggio': "Sei molto soggettivo nelle opinioni e le esprimi con grande energia. Spesso irriti la gente perché non ascolti gli altri e trovi le loro idee poco importanti. Sei piuttosto egocentrico. Inizi le conversazioni e vuoi avere l'ultima parola. Prendi decisioni affrettate e spesso devi ritrattare, ma fatichi a chiedere scusa. Hai molte idee e sai comunicare con chiarezza, ma a volte manchi di obiettività. Sai stimolare le persone prive di entusiasmo. Vai bene in qualsiasi lavoro a contatto con il pubblico. Parli con autorevolezza e ami dare ordini, ma il tuo modo giovanile ti rende poco convincente per i più seri. La tua arroganza può essere antipatica. Hai doti creative e potresti essere un buon leader se imparassi ad ascoltare.",
                    'consiglio': "🗣️ Ascoltare è importante quanto parlare. Cerca di interessarti alle idee degli altri e di essere meno impulsivo nei giudizi. L'umiltà è una grande forza."
                }
            },
            'sole_marte': {
                'congiunzione': {
                    'titolo': "☀️⚡ Sole congiunto a Marte",
                    'messaggio': "Hai una grande sensazione di potenza quando riesci ad affermare la tua volontà. Credi che non si debba mai scendere a compromessi. La tua forza di volontà è intensa e può essere una minaccia per i più deboli. Ambisci al riconoscimento dei tuoi meriti, ma questo attira antagonismi. Sei sempre pronto alla competizione e usi ogni mezzo per vincere. Non tolleri l'apatia. Hai una notevole resistenza fisica e grandi capacità creative e di comando. Vai bene in lavori di concorrenza e rischio: sport, esplorazioni, carriera militare, caccia. In campo intellettuale: medicina, chirurgia, legge, polizia. Sei impulsivo e dimentichi il buon senso. Devi imparare a controllare le tue energie. La tua libido è potente e puoi diventare violento se frustrato. Sei a rischio di incidenti e devi riposare.",
                    'consiglio': "🥊 La tua energia è un dono, ma usa la testa prima dei muscoli. Un buon consigliere può aiutarti a pianificare le tue mosse. Impara a incanalare la tua potenza in modo costruttivo."
                }
            },
            'sole_luna': {
                'congiunzione': {
                    'titolo': "☀️🌙 Sole congiunto alla Luna",
                    'messaggio': "Hai un temperamento unilaterale, quasi disinvolto negli scontri con la volontà altrui. La tua personalità è integrata: sei soddisfatto di te e dei tuoi progetti, che sei sicuro di realizzare. Non ti adatti alle circostanze se non ti è utile. Coordini bene tutte le tue risorse e sai cogliere le occasioni. Non permetti a nessuno di interferire nei tuoi affari e metti una barriera tra te e gli altri. Gli altri devono sempre fare il primo passo. Sei autosufficiente, ma a volte anche disfattista. Hai un tuo metro per misurare il successo, diverso da quello altrui. Vai bene in lavori indipendenti. Sei adatto a posizioni autorevoli, ma puoi essere malvisto per la tua eccessiva sicurezza. Hai il grande timore che la gente si faccia gioco delle tue emozioni, e per questo tieni le persone a distanza. Hai bisogno di momenti di quiete per ricaricarti.",
                    'consiglio': "🛡️ La tua sicurezza è la tua forza, ma non deve diventare un muro. Concediti di essere vulnerabile con le persone giuste. La solitudine ricarica, ma la condivisione arricchisce."
                }
            },
            'sole_venere': {
                'congiunzione': {
                    'titolo': "☀️❤️ Sole congiunto a Venere",
                    'messaggio': "Hai una natura molto affettuosa e hai bisogno della simpatia della gente. Fai di tutto per entrare nelle grazie degli altri, modificando impercettibilmente il tuo comportamento. Non sei sempre disposto a scendere a compromessi, per non sembrare debole. Con le persone più intime sei più naturale. Desideri che gli altri riconoscano i tuoi pregi. Sei un entusiasta ascoltatore e sei sempre allegro e socievole. Se pensi che qualcuno possa esserti utile, fai di tutto per essergli gradito. Tendi a drammatizzare per lasciare un'impressione duratura e non sopporti di passare inosservato. Presumi che gli altri pensino bene di te anche senza motivo. In fondo sei un sentimentale che capitolA davanti a piccole dimostrazioni d'affetto. Apprezzi le cose belle della vita.",
                    'consiglio': "🌷 La tua affabilità è un dono, ma non forzarla. Sii te stesso, senza cercare di compiacere tutti a tutti i costi. La vera simpatia nasce dalla spontaneità, non dalla strategia."
                }
            },
            
            # MARTE
            'marte_ascendente': {
                'congiunzione': {
                    'titolo': "🔥⬆️ Marte congiunto all'Ascendente",
                    'messaggio': "Hai un'energia inesauribile. Sei sempre in movimento, ma manchi di autodisciplina e vai incontro a rischi inutili. Sei considerato coraggioso, ma anche invadente e presuntuoso. Non ascolti nessuno perché sei sicuro di te e vuoi il riconoscimento della tua superiorità. In realtà, dietro questa immagine, si nasconde un complesso di inferiorità. Nelle discussioni sei polemico e urli più forte degli altri per avere ragione, sprecando così energie creative preziose. Non accetti vie di mezzo e trovi la diplomazia una cosa da deboli. Chi ti conosce evita di discutere con te. Il tuo lato positivo è la tua indipendenza e la fiducia in te stesso, che riesce a smuovere le persone e a ottenere il meglio da loro. Preferisci il ruolo di 'istigatore' che agisce dietro le quinte.",
                    'consiglio': "💪 La tua energia è potente, ma impara a dirigerla con intelligenza. Ascoltare gli altri non è una debolezza, ma una strategia per vincere senza fare nemici. Usa la tua forza per ispirare, non per sopraffare."
                }
            },
            'marte_plutone': {
                'congiunzione': {
                    'titolo': "🔥🌋 Marte congiunto a Plutone",
                    'messaggio': "Hai una forte determinazione, perseveranza e risolutezza. Ti butti con foga per ottenere ciò che vuoi, ma poi scopri che la vera soddisfazione è dimostrare a te stesso di esserne capace. Spesso confondi l'ostinazione con il desiderio. Nelle crisi sai aspettare il momento giusto per agire. Hai una forte spinta a mettere in evidenza la tua individualità, specialmente se qualcuno ti intralcia. Non sopporti di essere dominato, ma rispetti l'autorità giusta. Nei rapporti personali sei tu a fare il primo passo, spesso con aggressività. Sei possessivo ed esigente in amore e nelle amicizie. Hai forti appetiti sessuali e puoi usare il sesso come mezzo per ottenere ciò che vuoi. Hai molta coscienza sociale e sei aperto ai problemi della società. Ti impegni in compiti difficili senza paura e sai usare tecniche persuasive.",
                    'consiglio': "🦁 La tua forza è ammirevole, ma usala per costruire relazioni, non per dominarle. In amore, impara a condividere e a ricevere, non solo a pretendere. La tua energia può cambiare il mondo, ma inizia da quello intorno a te."
                }
            },
            'marte_urano': {
                'congiunzione': {
                    'titolo': "🔥⚡ Marte congiunto a Urano",
                    'messaggio': "Hai un'enorme energia vitale che ti spinge ad agire fino al raggiungimento della meta. Stabilisci le tue regole e non tolleri imposizioni. Non hai inibizioni e sei convinto di dover essere libero di fare tutto il necessario per ottenere ciò che vuoi. In compagnia non ci si annoia mai: cerchi l'eccitamento e lo crei se non c'è. Questa impulsività può creare problemi, perché la società ha delle regole. Se vuoi buoni risultati, devi rispettarle. La tua natura spericolata può trovare sfogo in sport, corse, scalate, esplorazioni. Devi però prendere coscienza delle misure di sicurezza. Hai una potente carica sessuale che non sopporta il rifiuto, ma sei piuttosto egoista e ami più ricevere che dare.",
                    'consiglio': "🌀 La tua energia è un'esplosione di vitalità, ma impara a incanalarla. Le regole non sono un limite, ma una protezione. In amore, ricorda che l'altro ha bisogno di emozioni, non solo di sesso. Sii generoso anche nel dare affetto."
                }
            },
            'marte_nettuno': {
                'congiunzione': {
                    'titolo': "🔥🌊 Marte congiunto a Nettuno",
                    'messaggio': "Vivi un conflitto interiore tra l'impulso ad agire e la non accettazione delle conseguenze. Non eviti le conseguenze, ma fatichi a vedere chiaramente la tua colpevolezza. L'immaginazione non ti fa vedere lontano e ti lasci andare all'improvvisazione, con risultati deludenti. Devi ponderare bene le tue azioni. Hai un'attrazione magnetica sulla gente e tendi ad assumere l'atteggiamento che gli altri si aspettano da te. Il teatro e le attività affini sono adatte alla tua fervida immaginazione. Se necessario, per il lavoro che ti interessa, non ti fai scrupolo di usare sotterfugi. Se altri fattori ti danno senso di responsabilità, puoi andare bene in medicina. In amore, quello che sembra il vero amore è spesso solo infatuazione. Le delusioni sono difficili da sopportare. Evita relazioni segrete e sii onesto. La tua salute è delicata, evita le medicine fai-da-te.",
                    'consiglio': "🎭 La tua sensibilità è un dono, ma non deve diventare una trappola. Prima di agire, fermati e chiediti: 'Ne vale davvero la pena?'. In amore, sii onesto e cerca la luce del sole, non l'ombra. La tua salute ringrazierà."
                }
            },
            'marte_giove': {
                'congiunzione': {
                    'titolo': "🔥✨ Marte congiunto a Giove",
                    'messaggio': "Possiedi un'enorme energia ed entusiasmo che ti spingono ad assumerti compiti difficili che spaventerebbero altri. Sfidi i pericoli senza paura per ottenere ciò che vuoi. Hai una fiducia sconfinata nelle tue capacità e tenti la sorte correndo enormi rischi. Mancano di astuzia, ma compensano con l'arroganza. Scatti per un nonnulla e i tuoi concorrenti hanno buoni motivi per temerti. Affronti gli avversari di petto e ti bevi la gloria che ne consegue. Non fai nulla con moderazione e non ti accontenti di vincere: devi vantartene pubblicamente. Ray Charles, Lee Marvin, J.F. Kennedy avevano questo aspetto. Puoi usare questa energia nello sport o nelle attività intellettuali. Non ammetti fallimenti. Il tuo difetto è la mancanza di moderazione, che può logorarti. Devi assolutamente riposare.",
                    'consiglio': "🏆 La tua energia e il tuo entusiasmo sono travolgenti, ma impara a dosarli. La vera vittoria non è solo nello show, ma nella costanza. Ricordati che anche i guerrieri hanno bisogno di riposare. La salute è il tuo bene più prezioso."
                }
            },
            'marte_saturno': {
                'congiunzione': {
                    'titolo': "🔥⏳ Marte congiunto a Saturno",
                    'messaggio': "Hai la fortuna di saper usare le tue energie in modo costruttivo. L'impulso a farti valere è moderato dal ragionamento sulle conseguenze. Questo ti porta a grandi realizzazioni perché non sprechi energie e hai un senso dell'economia che garantisce il successo. Sai come usare il tuo talento per scopi precisi. Sei realistico e usi buon senso prima di agire. L'educazione ricevuta ti mette in grado di assumere grandi responsabilità. Conosci i tuoi limiti e non li oltrepassi. Sei prudente, ma senza paura, e sai essere aggressivo quando serve. Rappresenti l'equilibrio ideale tra aggressività e autocontrollo. Non sei indifferente ai sentimenti altrui, ma ti secchi se interferisci con i tuoi progetti. La frustrazione può scatenare la tua energia più pericolosa. Vai bene in professioni che richiedono resistenza fisica e vitalità: archeologia, esplorazioni, geologia, carriera militare, ricerca industriale. In amore, valuti attentamente la linea di minor difesa dell'altro. Devi evitare sforzi eccessivi e sbalzi di temperatura.",
                    'consiglio': "⚖️ Sei un perfetto equilibrio tra forza e controllo. Usa questa dote per costruire, non per reprimere. In amore, sii strategico ma anche spontaneo. Ascolta il tuo corpo: il riposo è parte della strategia."
                }
            },
            
            # MERCURIO
            'mercurio_ascendente': {
                'congiunzione': {
                    'titolo': "💬⬆️ Mercurio congiunto all'Ascendente",
                    'messaggio': "Sei molto preoccupato per la tua persona e inizi spesso le conversazioni con 'Io'. I tuoi discorsi riguardano soprattutto te stesso. Anche se questo può essere noioso, la tua conversazione è brillante e spiritosa, e quindi tollerata. Ti entusiasmi per le idee nuove e le assimili rapidamente. Sei orgoglioso della tua brillantezza mentale e ti impazientisci con i più lenti, che un po' disprezzi. Sei un impulsivo mentale e spesso rispondi alle tue stesse domande senza aspettare risposta. Nelle feste sei un vero mulino a vento. Incanti l'uditorio con la tua parlantina sciolta e originale. Non hai paura di difendere le tue idee, anche se non sempre hai ragione. Se ti contestano, diventi polemico e discuti accesamente. Non sei certo una mammoletta timida.",
                    'consiglio': "🗣️ La tua mente è brillante, ma lascia spazio anche agli altri. Non devi sempre avere l'ultima parola per essere interessante. Ascoltare può aprirti a nuove prospettive e farti amare ancora di più."
                }
            },
            'mercurio_nettuno': {
                'congiunzione': {
                    'titolo': "💬🌊 Mercurio congiunto a Nettuno",
                    'messaggio': "La tua immaginazione è sbrigliata e quando parli tendi a divagare e a non attenerti troppo ai fatti. La realtà ti disturba, quindi cerchi di distorcerla e di vedere le cose a modo tuo. Sei molto sensibile all'ambiente e alle sue esperienze penose, e cerchi di sfuggirlo ritirandoti in un tuo mondo. Devi trovare un modo per esprimere costruttivamente la tua mente sensibile e profonda. La tua professione deve darti la possibilità di usare il tuo talento artistico: scrivere, recitare, danzare. Hai bisogno di una preparazione adeguata per esprimere al meglio le tue potenzialità. Sei affascinato da ciò che è romanzesco, misterioso e illusorio, ma attento a non farne una scusa per sfuggire alla realtà. In amore idealizzi troppo la persona amata e attribuisci loro qualità impossibili. Rimani affascinato dai personaggi famosi, anche se il loro fascino è illusorio. Sei molto suggestionabile: evita assolutamente stimolanti artificiali.",
                    'consiglio': "🎨 La tua immaginazione è un'oasi meravigliosa, ma non dimenticare di annaffiare anche il giardino della realtà. Usa la tua creatività nell'arte, non nella fuga. In amore, impara a vedere le persone per come sono, non per come le sogni."
                }
            },
            'mercurio_urano': {
                'congiunzione': {
                    'titolo': "💬⚡ Mercurio congiunto a Urano",
                    'messaggio': "Sei brillante, vivace, intuitivo e curioso di tutto. Hai un grande coraggio mentale. Ti interessi a tutto ciò che è originale e fuori dal comune. La tua mente è sempre in fermento, cerchi risposte ai perché e non sopporti l'ignoranza. Da bambino eri affascinato dai meccanismi dei giocattoli. La tua creatività si sviluppa presto, insieme all'amore per la verità. Le scienze, la filosofia, la psicologia, la psicodinamica sono studi adatti a te. Le tue capacità inventive possono essere applicate con successo nella ricerca e sviluppo industriale, o nella redazione di testi tecnici e scientifici. Il tuo partner deve essere simile a te, altrimenti la relazione finisce nella noia. Tendi a formare relazioni platoniche basate su interessi comuni. Se scopri falsità, rompi subito il rapporto. Guardi sempre al futuro e lasci il passato alle spalle. Hai possibilità di autoespressione illimitate, ma non sei costante. Impara a risolvere un problema alla volta.",
                    'consiglio': "💡 La tua mente è un vulcano di idee, ma per dare loro forma, impara a concentrarti su una alla volta. Cerca persone che condividano la tua sete di futuro e di verità, e sii paziente con chi è più lento."
                }
            },
            'mercurio_plutone': {
                'congiunzione': {
                    'titolo': "💬🌋 Mercurio congiunto a Plutone",
                    'messaggio': "Hai una mente profonda e penetrante, che tende agli estremi. Cerchi sempre un'interpretazione analitica delle tue esperienze, come un detective alla ricerca di significati nascosti. Valuti le questioni in modo soggettivo e la tua sensibilità psichica scopre indizi che sfuggono agli altri. Hai una curiosità esagerata e vai agli estremi per raccogliere informazioni. Sei quasi geniale nel trovare modi persuasivi per raggiungere i tuoi scopi. Una volta presa una decisione, non cambi mai idea. Esprimi e difendi le tue idee con veemenza e gli altri possono trovarti offensivo. Sei affascinato dal mistero e dall'occulto. Le tue capacità di osservazione ti rendono adatto a investigazione, chimica, ricerca, medicina, patologia, esplorazioni, consulenza fiscale. Modera le tue tendenze anarchiche. Anche se non ti vendichi, serbi in cuore sentimenti di vendetta. Ti irriti per le ingiustizie sociali e ti dai da fare per cambiarle. Sai drammatizzare per attirare l'attenzione delle autorità. In amore sei esigente e non tolleri la debolezza. Cerchi una persona che si lasci dominare, ma poi la disprezzi per questo. Ammiri la forza di carattere e l'autorevolezza.",
                    'consiglio': "🕵️ La tua mente è un segugio infallibile, ma non tutti i misteri hanno bisogno di essere risolti. Usa la tua profondità per capire te stesso e gli altri, non per giudicarli. In amore, cerca un partner alla tua altezza, non un suddito. La vera forza sta nella collaborazione, non nel dominio."
                }
            },
            'mercurio_saturno': {
                'congiunzione': {
                    'titolo': "💬⏳ Mercurio congiunto a Saturno",
                    'messaggio': "Hai grande senso di responsabilità e serietà. Tendi ad essere contemplativo, in parte per come sei stato allevato. Risolvi i problemi con logica e non ti curi delle cose superficiali. Sei una miniera d'informazioni e fai tesoro di ogni esperienza. Ascolti bene e sei cauto nell'esprimere opinioni. Preferisci le cose realistiche alla fantasia. Spesso sei pessimista e ti abbatti facilmente. Vai bene in matematica, disegno industriale, ingegneria, architettura, insegnamento, politica. Hai un campo vasto, ma perdi interesse se il lavoro non mette a frutto il tuo talento. Lavori meglio da solo e le distrazioni ti irritano. Sei serio, onesto e coscienzioso. Esigi un giusto compenso. Il successo può tardare a causa di colleghi o concorrenti che ti rubano le idee. A volte sembri indifferente, ma sei solo immerso in un pensiero. Sei piuttosto distratto e puoi isolarti anche in mezzo alla gente. Hai bisogno di confidarti con qualcuno di cui ti fidi. In amore sei attratto da persone mature, sincere, oneste e responsabili. La tradizione per te è sicurezza. Vivi in tensione: concediti brevi vacanze e impara a vedere il lato bello della vita senza farti ossessionare dai doveri.",
                    'consiglio': "🧠 La tua mente è un archivio prezioso, ma non tenerlo sempre chiuso a chiave. Condividi le tue idee con chi ti fidi e impara a non prendere tutto così sul serio. La leggerezza non è una perdita di tempo, ma un rigenerante per l'anima."
                }
            },
            'mercurio_giove': {
                'congiunzione': {
                    'titolo': "💬✨ Mercurio congiunto a Giove",
                    'messaggio': "Hai ottime capacità di ragionamento e un costante entusiasmo di sapere sempre di più. Hai una sete di conoscenza insaziabile e la tua mente è una miniera inesauribile di informazioni. Il tuo maggior talento è saper comunicare ed esprimere le tue opinioni in modo persuasivo. Fin da giovane metti a frutto le tue idee creative. Sei curioso e non ti acquieti finché non hai risposte. Questa curiosità ti accompagna per tutta la vita: ogni risposta apre nuove prospettive e nuove domande. Il tuo interesse è proiettato al futuro. Le tue possibilità intellettuali possono essere applicate in campo culturale, filosofia, storia, giornalismo, agenzie di viaggio. Puoi diventare un'autorità nella materia prescelta, come Sir Richard Burton, Emily Dickinson, O. Henry. Puoi avere difficoltà a concentrarti su un solo argomento, ma con autodisciplina ci riuscirai. Sei un formidabile oppositore nei dibattiti. Il tuo punto debole è il sistema nervoso: devi riposare.",
                    'consiglio': "📚 La tua sete di conoscenza è ammirevole, ma ricorda che l'apprendimento è un oceano: non puoi berlo tutto in un giorno. Concentrati su un argomento alla volta e dai al tuo cervello il tempo di assimilare. Il riposo è parte dell'apprendimento."
                }
            },
            'mercurio_marte': {
                'congiunzione': {
                    'titolo': "💬⚡ Mercurio congiunto a Marte",
                    'messaggio': "Hai una mente attiva, piena di immaginazione, desiderosa di conoscenza e creativa. Sei sempre in fermento, ma manchi di pazienza. Parli con eloquenza e veemenza e adori discutere con chi non la pensa come te. Sei sicuro di avere ragione e spesso dai giudizi azzardati. Non è facile farti ammettere di aver sbagliato. Interrompi gli altri anticipando ciò che stanno per dire. Quasi nulla ti sfugge e sei considerato un saputello. La tua acutezza e aggressività ti rendono adatto a insegnamento, pubbliche relazioni, avvocatura, teatro, giornalismo. Sei pieno di energia e lavori a velocità enorme. Rendi di più da solo, perché gli altri ti sembrano lenti e questo ti irrita. Non sopporti i rifiuti sentimentali, ma non ci piangi sopra: pensi di poter trovare un'altra persona. Sei un progressista che non si volta mai indietro, ma così commetti sempre gli stessi errori. La tua agitazione mentale può portare a esaurimenti. Devi imparare a fermarti a riflettere.",
                    'consiglio': "🧠 La tua mente è un motore acceso, ma impara a mettere anche la retromarcia. Rallenta, ascolta, rifletti. Gli errori non sono 'sciocchezze', ma lezioni preziose. In amore, non trattare le persone come numeri. Ognuna merita attenzione."
                }
            },
            'mercurio_venere': {
                'congiunzione': {
                    'titolo': "💬❤️ Mercurio congiunto a Venere",
                    'messaggio': "Hai affabilità e belle maniere. Trovi sempre il punto d'accordo per mantenere rapporti armoniosi. Non vuoi offendere, e per questo cerchi di essere giusto e imparziale. Esprimi le tue opinioni con tatto e diplomazia, raccogliendo fatti a sostegno. Non sei polemico e concedi il beneficio del dubbio. La tua natura pacata e gentile è preziosa, ma hai difficoltà a far fronte alla concorrenza spietata. Meglio lavorare da solo o in piccolo gruppo. Sei portato per l'arte drammatica, l'oratoria e la scrittura. Il tuo stile è fresco e brillante. Hai anche talento per gli affari e i tuoi schemi finanziari sono spesso ben accolti. Sei cauto e non fai nulla se non convinto della buona riuscita, riducendo così i rischi. Rifuggi dai progetti complicati.",
                    'consiglio': "🎭 La tua diplomazia è una lama affilata, ma non temere di usarla anche in terreni più competitivi. La tua grazia può disarmare anche i più agguerriti. Negli affari, la tua cautela è una garanzia di successo."
                }
            },
            
            # VENERE
            'venere_ascendente': {
                'congiunzione': {
                    'titolo': "❤️⬆️ Venere congiunta all'Ascendente",
                    'messaggio': "Hai belle maniere e un fascino sottile che attrae la gente. Desideri essere accettato sopra ogni cosa, e per questo sei disposto anche a scendere a compromessi. Ami le cose belle e frequenti chi la pensa come te per stabilire relazioni durature, ma non sempre ci riesci. Sotto la tua immagine affascinante, c'è una mente calcolatrice che valuta costantemente i pro e i contro di ogni relazione. Sai scoprire le qualità migliori della gente e conquistare ammiratori. All'apparenza sei impeccabile e raffinato, ma se non ottieni ciò che vuoi, sai essere aggressivo e avido. Tutto deve essere in funzione dei tuoi desideri. Dovresti smorzare le tue tendenze egocentriche e mettere più in risalto i tuoi talenti, che sono solidi e piacevoli.",
                    'consiglio': "🪞 Il tuo fascino è una calamita, ma non usarla solo per attirare ciò che vuoi. Sii autentico e lascia che gli altri ti amino per quello che sei, non per quello che puoi dare loro. I tuoi talenti sono un dono da condividere, non una merce di scambio."
                }
            },
            'venere_plutone': {
                'congiunzione': {
                    'titolo': "❤️🌋 Venere congiunta a Plutone",
                    'messaggio': "Hai una natura romantica che cerca sempre l'appagamento emotivo, provocando in te profonde crisi. Vuoi le massime soddisfazioni emotive e fisiche e sei attratto da persone molto diverse tra loro. Sei molto possessivo in amore, ma pronto a troncare se trovi una relazione che promette di più. Pretendi prove d'amore tangibili e sacrifici materiali per essere sicuro della genuinità dell'interesse altrui. Vivi nella speranza di trovare un'unione assoluta e completa, a tutti i livelli. Susciti profondo interesse in chi incontri: alcuni ti trovano irresistibile, altri temono di essere intrappolati dal tuo fascino. Con gli anni, ti libererai delle tue preoccupazioni sessuali e potrai goderti i contatti umani. Attiri le persone come una calamita. Non sopporti le ingiustizie sociali e sei pronto a prestare la tua opera se ce n'è bisogno. Sei adatto per la raccolta fondi per scopi benefici, con tattiche di pressione rispettose.",
                    'consiglio': "🦋 La tua intensità è un fuoco che brucia e illumina. Impara a non farti consumare dalla ricerca della perfezione in amore. Accetta che le relazioni umane sono imperfette e che la vera unione si costruisce giorno per giorno, non con prove eclatanti."
                }
            },
            'venere_urano': {
                'congiunzione': {
                    'titolo': "❤️⚡ Venere congiunta a Urano",
                    'messaggio': "Hai una personalità effervescente, brillante, socievole, con un'immensa gioia di vivere. Cerchi sempre relazioni eccitanti e se non ti senti a tuo agio, le lasci perdere. Sei molto popolare per la tua socievolezza. Sei adatto a lavori che riguardano cose nuove e creative. La routine monotona ti sarebbe insopportabile. Le professioni a contatto con il pubblico sono le più adatte: pubbliche relazioni, organizzazione di eventi, sfilate di moda, decoratore, architetto d'interni, consulente per investimenti. Nei rapporti chiedi libertà assoluta, per poterti ritirare senza rimorsi quando ti stanchi di una persona. Se qualcuno ti affascina, però, stringi rapporti stretti, ma sei sempre pronto a rompere se trovi qualcosa di più interessante. Per te è difficile legarti stabilmente perché consideri carriera e lavoro più importanti dell'amore. È meglio un lungo fidanzamento o un legame libero prima di sposarti. Manca un po' di senso di responsabilità.",
                    'consiglio': "🌈 La tua gioia di vivere è un dono, ma impara a non disperderla in mille rivoli. Cerca relazioni che ti appaghino veramente, non solo che ti eccitino. La vera libertà è anche sapersi impegnare senza sentirsi in gabbia."
                }
            },
            'venere_saturno': {
                'congiunzione': {
                    'titolo': "❤️⏳ Venere congiunta a Saturno",
                    'messaggio': "Hai la sensazione di dover sempre fare concessioni e adeguarti agli altri per avere buoni rapporti. Questo ti rende insoddisfatto e frustrato. Spesso ti rassegni a relazioni in cui dai più di quanto ricevi. Sei sincero e leale negli affetti, ma cerchi di non dimostrarlo per paura di essere usato. Hai molto buonsenso con il danaro, sei prudente e risparmi anche se stai bene. Il risparmio è una compensazione per le delusioni affettive. Sei adatto a professioni che richiedono il rispetto delle regole: istituiti finanziari, banche, immobiliare, vendite, progettazione. Preferisci lavorare in modo indipendente, senza controllo continuo. In amore sei attratto da persone serie, sincere e oneste, magari più mature di te, che ti diano sicurezza. Hai obiettivi precisi e vuoi che il partner collabori per raggiungerli. Il profondo rispetto per la famiglia ti impedisce di coinvolgerti in situazioni pericolose per l'unità familiare. Cerca di vedere il lato positivo della vita, altrimenti la tua salute (gola, tonsille) potrebbe risentirne.",
                    'consiglio': "🏛️ La tua serietà e lealtà sono un porto sicuro, ma non deve diventare una fortezza. Impara a fidarti e a lasciarti andare, anche a costo di qualche delusione. La vita è fatta anche di doni inaspettati, non solo di conquiste faticose. Il sorriso è il miglior investimento."
                }
            },
            'venere_giove': {
                'congiunzione': {
                    'titolo': "❤️✨ Venere congiunta a Giove",
                    'messaggio': "Sei una persona gentile, comprensiva e generosa. Fai di tutto per esprimere queste qualità e sei benevolo con il prossimo anche quando non lo merita. La volgarità e la brutalità ti sono intollerabili. Mantieni il tuo decoro e un certo ottimismo anche nelle avversità. Ami le comodità, la vita facile e le attività sociali. Probabilmente hai avuto genitori affettuosi che ti hanno permesso di sviluppare queste doti. Sei adatto a professioni che ti permettono di esprimere le tue qualità: pubbliche relazioni, viaggi, insegnamento, organizzazione di attività sociali, opere assistenziali. Porti gioia e speranza a chi soffre. La tua natura briosa ti rende popolare. Spesso qualcuno approfitta della tua bontà, ma tu non diventi amaro. Sei ricercato da persone di successo e con le tue stesse qualità. Rispondi all'onestà con onestà e non tolleri gli opportunisti e i fannulloni. Se ricevi aspetti negativi da Saturno, potresti avere difficoltà a raggiungere la felicità che meriti.",
                    'consiglio': "🌸 La tua gentilezza è un balsamo per il mondo, ma impara a dosarlo per non essere prosciugato. Circondati di persone che ti apprezzano per quello che sei e non per quello che dai. La tua felicità merita di essere vissuta appieno."
                }
            },
            'venere_marte': {
                'congiunzione': {
                    'titolo': "❤️🔥 Venere congiunta a Marte",
                    'messaggio': "Hai una potente natura desiderosa che deve essere espressa in continuazione. Puoi esprimerla attraverso le relazioni o con attività artistiche o socio-culturali che ti diano soddisfazione e ti aiutino a fare nuove conoscenze. Hai grande calore umano e generosità, che attraggono la gente. Nel tuo bisogno di contatti umani, non sai discriminare le persone con cui ti associ. In amore sei piuttosto aggressivo e fai il primo passo, ma spesso vieni respinto. Questa aggressività è utile per vincere la concorrenza. Non hai un campo professionale specifico, ma un lavoro a contatto con il pubblico ti darà la sensazione di pienezza di cui hai bisogno. Sei una 'pila elettrica' e non puoi vivere senza i piaceri e le crisi dei contatti umani. Sei attratto da persone attive, aggressive ed estroverse, purché non tentino di dominarti. Non fai concessioni senza pensarci bene, ma ti aspetti che gli altri scendano a compromessi con te. Pretendi molto dagli altri, specialmente dalla persona amata, e spesso la spaventi.",
                    'consiglio': "💞 Il tuo calore è un fuoco che accende chi ti sta intorno, ma impara a non bruciare chi si avvicina troppo. Sii meno esigente e più accogliente. L'amore non è una conquista, ma un giardino da coltivare insieme."
                }
            },
            
            # SATURNO
            'saturno_ascendente': {
                'congiunzione': {
                    'titolo': "⏳⬆️ Saturno congiunto all'Ascendente",
                    'messaggio': "Hai capacità di autodisciplina e un atteggiamento conservatore. Sei modesto e timido, tanto da sembrare quasi indifferente. Dubiti sempre di te e delle tue capacità, e sei molto prudente con gli avversari. Questa mancanza di fiducia può, con l'esperienza, trasformarsi in sicurezza. Non hai la grinta che impressiona a prima vista, ma a lungo andare ispiri sicurezza e solidità. Non ami le luci della ribalta e preferisci stare nell'ombra. Sei lento a muoverti e hai bisogno di piccoli successi iniziali per rassicurarti. Pianifichi tutto con precisione, passo dopo passo. Esiti a prendere decisioni tempestive e ti lasci sfuggire le occasioni. Senti in modo esagerato le responsabilità e non lasci mai a terra chi ha bisogno di te. Impara ad amarti di più e a convincerti che meriti le cose buone che ottieni. Qualcuno potrebbe approfittarsi di te, ma tu non dimentichi i torti subiti. Non sei vendicativo, ma sai aspettare il momento della rivincita, ripagando con fredda indifferenza.",
                    'consiglio': "🛡️ La tua prudenza è uno scudo prezioso, ma non deve diventare una prigione. Impara a fidarti di te stesso e a cogliere le occasioni senza paura. Ricorda che meritavi amore e successo tanto quanto chiunque altro. Il tuo valore non ha bisogno di essere dimostrato, ma solo riconosciuto da te."
                }
            },
            'saturno_plutone': {
                'congiunzione': {
                    'titolo': "⏳🌋 Saturno congiunto a Plutone",
                    'messaggio': "Hai una grande ambizione e una forte spinta verso le mete prefisse, che richiede la concentrazione di tutte le tue capacità. Potresti passare un periodo di austerità, ma hai molta costanza e sopporti molte cose pur di raggiungere ciò che desideri. Il terrore del fallimento è la molla che ti spinge a ottenere il massimo. Nessun sacrificio è troppo piccolo. Tendi verso lavori tradizionali che danno sicurezza. Puoi resistere ai cambiamenti con aria di sfida o adeguarti vivendo in ansia. In ogni caso, il tuo atteggiamento va agli estremi: o ti adegui con fervore o resisti e subisci una sconfitta. Sei molto chiuso e difficilmente confidi i tuoi progetti. Lavori dietro le quinte e accumuli per la vecchiaia. Sei efficiente con il danaro e prudente nello spendere. Sei un ottimo organizzatore e sai gestire posti di comando e responsabilità. Rispetti la legge in modo quasi perfetto e sei sempre giusto. Hai una capacità quasi soprannaturale di capire le motivazioni della gente, e questo ti aiuta a stabilirne la colpevolezza o l'innocenza.",
                    'consiglio': "🏛️ La tua ambizione è una forza titanica, ma ricorda che la vera grandezza non si misura solo dal successo materiale. Usa la tua capacità di comprendere le persone per costruire, non solo per giudicare. La tua perseveranza è ammirevole, ma impara anche a goderti il presente, non solo a preparare il futuro."
                }
            },
            'saturno_urano': {
                'congiunzione': {
                    'titolo': "⏳⚡ Saturno congiunto a Urano",
                    'messaggio': "Hai la capacità di dare forma alle idee, maturità mentale e creatività. Sei molto costruttivo ed efficiente. Ami la libertà e la mantieni in tutti i modi, sostenuto da una forte autodisciplina. Hai un saluto rispetto per le autorità. L'ambizione ti spinge ad addossarti incarichi importanti e a lunga portata. Le tue capacità professionali sono illuminate: non temi responsabilità e doveri. Hai molto da offrire in termini di conoscenza ed esperienza. Capisci la lezione del passato e combatti per un futuro migliore. Il tuo contributo è prezioso in grossi complessi industriali o organizzazioni socio-politiche. Vai bene in scienze, politica, matematica, ricerca, occultismo, insegnamento. Ti trovi a tuo agio con persone dal polso di ferro, avventurose e 'dure'. Non sopporti la superficialità. La tua vita deve avere uno scopo. Devi rilassarti per ricaricare le energie, altrimenti diventi pessimista.",
                    'consiglio': "⚙️ Sei un ponte tra il passato e il futuro. Usa questa dote per costruire qualcosa di solido e innovativo. La tua disciplina al servizio della creatività è una combinazione vincente. Ricordati che anche le macchine più potenti hanno bisogno di manutenzione: concediti del tempo per rigenerarti."
                }
            },
            'saturno_nettuno': {
                'congiunzione': {
                    'titolo': "⏳🌊 Saturno congiunto a Nettuno",
                    'messaggio': "Difficilmente ti lasci ingannare a lungo. Ti tuteli dubitando di tutto ciò che non conosci. Anche in questioni spirituali o religiose, sei restio ad accettare dogmi non spiegabili con la ragione. Se da bambino hai accettato insegnamenti dogmatici, crescendo hai cominciato a dubitarne, provando un senso di colpa. Hai un atteggiamento maturo verso la religione e un profondo senso degli obblighi sociali. Hai doti psichiche, ma in modo realistico, e con l'esperienza sviluppi l'intuizione. Sei adatto a incarichi dirigenziali perché sai prendere decisioni giuste. Sei abile nella professione perché intuisci la disonestà. Temi l'ignoto e sei prudente nel decidere. Le tue intuizioni hanno un valore pratico. In amore sei prudente: sei un idealista, ma con i piedi a terra. Non ti impegni in relazioni serie senza la sicurezza che il sentimento sia ricambiato. Non fai amicizia facilmente. Sei adatto ai rapporti seri. Devi usare prudenza con le medicine.",
                    'consiglio': "🔮 La tua intuizione è un radar prezioso, ma non deve paralizzarti. Fidati del tuo istinto, ma concediti anche il lusso di sbagliare ogni tanto. La vita è fatta anche di scoperta, non solo di certezze. In amore, apri il cuore con cautela, ma aprilo."
                }
            },
            
            # GIOVE
            'giove_plutone': {
                'congiunzione': {
                    'titolo': "✨🌋 Giove congiunto a Plutone",
                    'messaggio': "Hai una forte spinta a goderti la vita in tutta la sua pienezza. Hai una potente ambizione che ti spinge impazientemente verso i traguardi. Non sopporti intralci e ritardi in mete che agli altri sembrano poco realistiche. Proseguì risoluto, senza mai dubitare di riuscire: non accetti la sconfitta. Sei guidato da un insaziabile desiderio di ottenere il massimo dalle tue capacità, e il successo in compiti impossibili è quasi ispirato. Dietro la tua ambizione c'è una fiducia indistruttibile nella tua capacità di superare le difficoltà. I tuoi successi sono fonte di lode e invidia. Hai possibilità di distinguerti in molti campi e spesso cerchi qualcosa che riempia di più la tua vita, come lo sviluppo spirituale. Sei attratto da professioni a stretto contatto con gli altri: medicina, legge, psicologia, sacerdozio. La tua voglia di metterti in mostra può portarti a sport, ricerca, esplorazioni, o persino al gioco d'azzardo. Puoi coinvolgerti in schemi finanziari di vasta portata, con ottimi risultati. Ammiri il successo e frequenti persone di successo. Il tuo partner deve avere carattere e personalità, e tu lo spingi a sempre maggiori conquiste.",
                    'consiglio': "🚀 La tua ambizione è un motore potente, ma non deve diventare l'unico scopo della vita. Goditi il viaggio, non solo la meta. Cerca un partner che sia un compagno di avventure, non un trofeo da esibire. La vera ricchezza è la pienezza dell'esperienza, non solo il successo."
                }
            },
            'giove_ascendente': {
                'congiunzione': {
                    'titolo': "✨⬆️ Giove congiunto all'Ascendente",
                    'messaggio': "Sei un concentrato di ottimismo. Non fai nulla con moderazione, perché pensi che a lungo andare darà ottimi risultati. Sei una miniera di idee che ti spingono a continui progetti, sicuro che andranno in porto. Hai una fiducia infinita nelle tue capacità e nella fortuna. Non ti preoccupi del domani né di ieri. Sei ambizioso e spesso fai il passo più lungo della gamba, esagerando la tua importanza. Questo può essere un problema quando cerchi alleati. Sei molto generoso e benevolo, ma a volte fai promesse che non puoi mantenere. Tuttavia, puoi sempre contare sul suo contributo in campagne di beneficenza. Sei ben informato e ti tieni aggiornato. Appartieni alla categoria di persone che fanno donazioni a scuole o istituti. Hai molte idee, ma non le sai tenere per te, e i concorrenti ne approfittano. Devi imparare a essere più conservatore e serio. Hai la tendenza a ingrassare, specialmente con l'età: frena la tua golosità.",
                    'consiglio': "🌟 Il tuo ottimismo è un sole che illumina chi ti sta intorno, ma impara a non bruciare le tappe. La pazienza e la moderazione sono alleate preziose. Tieni per te le tue idee migliori finché non sono mature. E sì, forse è il caso di dire di no a quel secondo dolce."
                }
            },
            'giove_urano': {
                'congiunzione': {
                    'titolo': "✨⚡ Giove congiunto a Urano",
                    'messaggio': "Ti aspetti molto dal futuro. Hai molto fiuto e sai scegliere il modo migliore per esprimere il tuo talento innato. Hai un profondo rispetto per la cultura e ammiri i grandi geni. Hai un'insaziabile bisogno di imparare, perché sai che sapere significa potere e libertà. Questo amore per lo studio ti è stato probabilmente inculcato nell'infanzia e ti ha innalzato al di sopra della media. Nella ricerca della verità sei un filosofo. Sei affascinato dalla politica, ma dai il massimo nell'insegnamento. Il tuo sguardo è volto al futuro e stimoli gli altri in quella direzione. Non trascuri la lezione del passato. Se non insegni, puoi distinguerti in legge o governo. I tuoi rapporti sociali sono piacevoli con persone che la pensano come te. Nelle relazioni sei estremamente generoso, ma hai bisogno di legarti con persone progressiste che non scoraggino il tuo entusiasmo. Anche la persona amata deve apprezzare le novità e sostenere i tuoi progetti per il futuro. Devi fermarti ogni tanto per non perdere la giusta prospettiva.",
                    'consiglio': "🔭 La tua mente è un telescopio puntato sul futuro, ma non dimenticare di guardare anche il paesaggio intorno a te. La cultura è un viaggio, non solo una meta. Cerca compagni di viaggio che condividano la tua meraviglia, non solo la tua direzione. E ricorda, a volte la cosa più rivoluzionaria è fermarsi ad ammirare un tramonto."
                }
            },
            'giove_nettuno': {
                'congiunzione': {
                    'titolo': "✨🌊 Giove congiunto a Nettuno",
                    'messaggio': "Hai la tendenza a eccedere nelle cose, a parlare diffusamente di argomenti che non conosci bene e a assumerti compiti al di là delle tue capacità. Sei portato a confidarti con gli altri, aspettandoti che mantengano il segreto, e spesso hai delusioni e tradimenti. La tua fiducia nel prossimo è illimitata e la dai indiscriminatamente a tutti. La tua natura filosofica ti spinge a sperare di trovare qualcuno degno di fiducia. Le esperienze ti insegnano a affinare il tuo giudizio. Hai una comprensione spirituale dei tuoi obblighi sociali e vi adempi con talento e immaginazione. Sei adatto ai lavori di assistenza sociale e beneficenza, all'insegnamento in scuole parrocchiali, orfanotrofi, organizzazioni paramediche. Dài comprensione e assistenza a tutti, ma c'è il pericolo che gli altri ne approfittino. Lo stesso può accadere in amore: desideri credere nei sentimenti dell'altro e punti al matrimonio. Cerca di andare a fondo nelle motivazioni altrui per non subire delusioni. Sviluppa maggiore sensibilità per la realtà vera. Evita medicine, droghe e non fidarti di ciarlatani.",
                    'consiglio': "🕊️ La tua fiducia è una fonte inesauribile, ma impara a incanalarla in un ruscello, non in un oceano. Non tutti sono degni della tua acqua preziosa. In amore, asciugati gli occhi dai sogni per vedere la persona reale. La tua spiritualità è un dono, ma la terra ha bisogno di radici solide."
                }
            },
            'giove_saturno': {
                'congiunzione': {
                    'titolo': "✨⏳ Giove congiunto a Saturno",
                    'messaggio': "Hai un enorme potenziale di successo che si ottiene solo a prezzo di grandi sforzi. Nonostante ciò, sei sempre pronto a lottare. Hai forza d'animo e costanza che ti spingono a mobilitare tutte le tue risorse. Devi programmare ogni passo e agire al momento giusto. Hai un'immagine vivida del futuro, che hai già realizzato nei sogni, ma sei realistico e accetti le responsabilità che implica. Sai che la lotta non basta se non soddisfa la tua visione mentale. Hai il coraggio di mostrare la tua fiducia, ma sei cauto e non esci dai limiti. Il tuo successo è proporzionale alla tua buona volontà di accettare autodisciplina e duro lavoro. Non perdi la speranza e sei realistico, impaziente ma serio. Preferisci usare sistemi provati dall'esperienza e non corri rischi. Usi le tue capacità per progetti pratici e fattibili. Vai bene in studi legali, medicina, contabilità, insegnamento, come ministro del culto. Apporti una profonda comprensione dell'essere umano. Sei paziente con i meno dotati e disponibile ad aiutare. Ami leggere libri professionali e partecipare a conferenze. Non sei mai soddisfatto di quanto sai. Rispetti la lezione della storia. Il tuo problema è voler fare troppo: può provocare esaurimenti. Concediti frequenti vacanze.",
                    'consiglio': "🏔️ La tua ascesa verso la vetta è lenta ma inesorabile. Non temere la fatica, ogni passo ti avvicina alla meta. Ricorda che la montagna non si scala in un giorno, e che il riposo in un rifugio è parte dell'impresa. La tua conoscenza è un tesoro, ma il più grande è la saggezza di saperla usare con umanità."
                }
            },
            
            # URANO
            'urano_ascendente': {
                'congiunzione': {
                    'titolo': "⚡⬆️ Urano congiunto all'Ascendente",
                    'messaggio': "Sei la personificazione dell'individualità. La tua alchimia personale attira l'amichevole simpatia della gente. Sei ammirato dai più e temuto da chi si sente insignificante al tuo cospetto. Fraternizzi con tutti senza distinzioni sociali. Non giudichi gli altri dall'abito, dalla scuola o dal censo. Sei pienamente cosciente dell'ingiustizia delle distinzioni sociali e delle limitazioni imposte dalla tradizione. Vedi l'uomo per quello che è: un individuo che non può essere classificato se non come membro della razza umana. Intuisci che il progresso dipende dalla personalità di chi compone la società. Il passato serve solo da lezione; il futuro è la tua preoccupazione. Partecipi attivamente ai movimenti per lo sviluppo della coscienza, rifiutando una realtà basata solo sulla dimensione fisica. Puoi aiutare gli uomini ad acquisire una nuova libertà, e questo è il tuo inestimabile valore per l'umanità.",
                    'consiglio': "🌍 La tua individualità è una bandiera, non usarla per dividerla, ma per unire. Il tuo sguardo al futuro è prezioso, ma non dimenticare che il futuro si costruisce con le mani di tutti, oggi. Sii faro, non isola."
                }
            },
            'urano_nettuno': {
                'congiunzione': {
                    'titolo': "⚡🌊 Urano congiunto a Nettuno",
                    'messaggio': "Sei pienamente cosciente dei tuoi obblighi verso la struttura sociale, che identifichi con la coscienza di massa. Ti rendi conto degli inganni della politica e questo ti disturba enormemente. Sai che certi schemi possono portare alla perdita della libertà. Appartieni a una generazione che non tollera gli abusi di autorità e potere. Ti rendi conto che la perdita di libertà può diventare assoluta se non ci si protegge. Questa congiunzione si è formata nel 1992-94, e l'ultima volta fu nel 1821-24, periodo di importanti innovazioni (impermeabilizzazione dei tessuti, cemento) e lotte per i diritti civili. Questa congiunzione sensibilizza l'uomo ai miglioramenti sociali. Sai che isolato non ottieni nulla, e che l'unione fa la forza per combattere le ingiustizie. Solo lavorando uniti si può ripristinare ordine e libertà dove impera caos e indigenza.",
                    'consiglio': "🤝 La tua sensibilità verso i mali del mondo è un dono prezioso. Unisciti ad altri che la pensano come te: la tua voce, insieme ad altre, può diventare un coro in grado di farsi ascoltare. Non isolarti, la soluzione è nella collettività."
                }
            },
            'urano_plutone': {
                'congiunzione': {
                    'titolo': "⚡🌋 Urano congiunto a Plutone",
                    'messaggio': "Sei pronto a misure estreme pur di preservare la tua libertà. Per te, libertà ha un senso ampio: significa liberazione dall'inquinamento, dalle malattie, dalla disoccupazione, dal monopolio economico. Vuoi il diritto di fare le cose con la tua testa e di dare il tuo contributo all'umanità. La generazione con questa congiunzione (1963-68) appoggia programmi per il miglioramento delle condizioni di vita, a volte partecipandovi attivamente. Ti rendi conto che solo il lavoro di tutti può fermare il saccheggio delle risorse naturali. Hai un profondo rispetto per tutto ciò che è vivente. La pubblicazione di 'Primavera silenziosa' e il rapporto 'Fumo e salute' hanno messo in luce i problemi ambientali e sanitari. Hai due strade: voltare le spalle alla decadenza o cercare di riportare ordine nel caos.",
                    'consiglio': "🌱 Sei un figlio di un'epoca di grandi cambiamenti e consapevolezze. La tua sensibilità per l'ambiente e la giustizia è la tua bussola. Non voltarti dall'altra parte: il tuo contributo, anche piccolo, è una goccia nell'oceano del cambiamento. La terra ha bisogno di te."
                }
            },
            
            # NETTUNO
            'nettuno_ascendente': {
                'congiunzione': {
                    'titolo': "🌊⬆️ Nettuno congiunto all'Ascendente",
                    'messaggio': "Hai una grande sensitività e doti psichiche, ma poca coscienza del mondo reale. Dovresti cercare di essere più pratico. A volte ti crei un mondo tuo per sfuggire alla realtà e alle difficoltà che ti spaventano. Sei così sensibile alle ingiustizie sociali da ammalarti facilmente. Dovresti darti da fare per combattere queste condizioni negative, portando sollievo anche al tuo stato d'ansia. Sei particolarmente sensibile alle disumane condizioni economiche e sociali di molti popoli. Sei compassionevole con i sofferenti e gli oppressi, e comprensivo con chi si ribella. Concedi sempre il beneficio del dubbio e sopporti in silenzio le delusioni. La sensazione di colpa e impotenza ti spinge a ritirarti in un mondo interiore, a volte con l'uso di mezzi artificiali. Devi evitare alcol e droghe. Attiri persone strane e prepotenti che ti dominano. Cerca invece persone serie e pratiche che ti aiutino a tenerti in contatto con la realtà, quella realtà che potresti contribuire a migliorare.",
                    'consiglio': "🕊️ La tua sensibilità è un dono, ma non deve diventare una gabbia. Affronta il mondo con il cuore aperto, ma con i piedi per terra. Cerca guide pratiche che ti aiutino a trasformare la tua compassione in azione. Il mondo ha bisogno della tua visione, ma anche delle tue mani."
                }
            },
            
            # PLUTONE
            'plutone_ascendente': {
                'congiunzione': {
                    'titolo': "🌋⬆️ Plutone congiunto all'Ascendente",
                    'messaggio': "Hai la capacità di visione di un nuovo mondo che può essere edificato con le risorse disponibili. Sei perfettamente conscio delle difficoltà di agire e svilupparsi nelle attuali condizioni ambientali. Sai che il popolo ha la possibilità di fare pressioni su chi detiene il potere. Puoi avere un ruolo importante nello spingere il pubblico a eliminare i parassiti che causano le decadenti condizioni sociali. Hai facilità di parola e autorevolezza. Quando la situazione è grave, usi tutta la tua abilità per costringere le autorità a prendere provvedimenti. Non ti dai pace finché non vedi tutto filare perfettamente. Non tolleri ingerenze nei tuoi affari personali. Sai cosa vuoi dalla vita e usi tutte le tue forze per raggiungerlo. Sai difendere chi è affidato alle tue cure. Devi evitare gli eccessi e non inimicarti persone che potrebbero comportarsi violentemente con te. La tua prerogativa è di riuscire a far venire fuori le qualità peggiori nascoste nelle persone.",
                    'consiglio': "🌋 La tua forza è un vulcano, usala per costruire, non per distruggere. La tua visione è un faro, non accecare chi ti sta intorno. La vera giustizia si costruisce con la perseveranza, non con la sopraffazione. Sii guida, non despota."
                }
            },
        # ============================================
        # MESSAGGI PER I SESTILI RADIX
        # ============================================

            # SOLE (sestili)
            'sole_luna_sestile': {
                'sestile': {
                    'titolo': "☀️🌙 Sole in sestile con la Luna",
                    'messaggio': "C'è un bell'equilibrio dentro di te tra la tua identità e le tue emozioni. Vivi in armonia con te stesso e questo si riflette nei rapporti con gli altri. Hai avuto un'infanzia serena che ti ha regalato la capacità di stare bene con tutti, senza distinzioni. Sei una persona creativa, piena di idee, e sai come realizzarle senza perdere di vista i sentimenti tuoi e altrui. Affronti le sfide con coraggio ma anche con tatto, perché tieni a non ferire. Il successo per te è naturale, qualunque strada tu scelga, purché ti lasci esprimere liberamente.",
                    'consiglio': "🌈 Coltiva questo equilibrio interiore: è la tua forza più grande. Non smettere mai di ascoltare sia la testa che il cuore."
                }
            },

            'sole_marte_sestile': {
                'sestile': {
                    'titolo': "☀️🔥 Sole in sestile con Marte",
                    'messaggio': "Hai un'energia che sembra non finire mai. Riesci a fare cose che per altri sarebbero impossibili, perché metti passione e intelligenza in ogni azione. Le tue idee sono chiare e sai come realizzarle, ma hai anche l'umiltà di ascoltare i suggerimenti degli altri. Non agisci d'impulso: prima valuti, poi decidi. E se sbagli, sai ammetterlo senza farti troppi problemi. La tua comunicazione è il tuo punto forte: sai parlare, sai scrivere, sai insegnare. Sei un leader naturale, ma mai prepotente.",
                    'consiglio': "⚡ La tua energia è contagiosa, ma ricordati di lasciare spazio anche agli altri. La vera forza è saper ascoltare quanto parlare."
                }
            },

            'sole_giove_sestile': {
                'sestile': {
                    'titolo': "☀️✨ Sole in sestile con Giove",
                    'messaggio': "Sei una persona che sa il fatto suo e ha fiducia in ciò che fa. L'educazione che hai ricevuto ti ha preparato bene alla vita: non ti abbatti mai, affronti tutto con ottimismo e ironia. Sai ridere di te stesso, e questo ti rende ancora più simpatico. Cogli le occasioni al volo, a volte anche troppo, ma anche quando sbagli, la fortuna sembra darti una mano. Parli bene, sai convincere, e la gente ti ascolta volentieri. La routine ti ucciderebbe: hai bisogno di novità, di movimento, di aria aperta. Sei generoso con chi lotta per le stesse cose che ami.",
                    'consiglio': "🌟 La vita ti sorride perché sai sorriderle tu per primo. Continua così, ma impara a rallentare ogni tanto: non tutto deve essere una corsa."
                }
            },

            'sole_saturno_sestile': {
                'sestile': {
                    'titolo': "☀️⏳ Sole in sestile con Saturno",
                    'messaggio': "Hai una profondità e una maturità rare. Capisci le cose in modo istintivo e sai aiutare gli altri a capire. Conosci i tuoi limiti e questo ti rende ancora più forte, perché non sprechi energie in imprese impossibili. Rispetti chi sa più di te e non hai bisogno di essere al centro dell'attenzione: preferisci lavorare nell'ombra, con serietà e costanza. Sei ambizioso, ma con calma: costruisci il tuo successo passo dopo passo, senza fretta, senza rumore. I colleghi e i superiori si fidano di te, perché sai essere leale e competente. In amore, cerchi una persona solida come te, con cui costruire qualcosa di duraturo.",
                    'consiglio': "🛤️ La tua forza è la pazienza. Continua a costruire con calma: i tuoi mattoni sono solidi e reggeranno qualsiasi tempesta."
                }
            },

            'sole_urano_sestile': {
                'sestile': {
                    'titolo': "☀️⚡ Sole in sestile con Urano",
                    'messaggio': "Per te la comunicazione è tutto. Non sopporti le persone chiuse, quelle che non sanno condividere. Tu invece parli chiaro, dici quello che pensi, ma lo fai con garbo, senza offendere. La vita è un'avventura eccitante e la noia non fa per te. Vedi il lato positivo in ogni cosa, anche in quelle che sembrano negative, e questo ti rende forte e ottimista. La tua mente è originale, aperta, curiosa. Insegnare è forse la tua strada migliore, perché sai rendere affascinante qualsiasi argomento. Detesti le bugie e chi le dice: se qualcuno ti tradisce, per te è come se non fosse mai esistito.",
                    'consiglio': "🔮 La tua mente è un faro. Usala per illuminare gli altri, ma non pretendere che tutti vedano la tua stessa luce. Rispetta i tempi di chi è più lento."
                }
            },

            'sole_nettuno_sestile': {
                'sestile': {
                    'titolo': "☀️🌊 Sole in sestile con Nettuno",
                    'messaggio': "Hai una sensibilità fuori dal comune e un talento creativo che ti permette di esprimere in modo unico ciò che senti. Sei profondamente consapevole del tuo ruolo nel mondo e del tuo dovere verso chi soffre. Non sei un rivoluzionario, ma un sostenitore silenzioso: preferisci aiutare direttamente chi ha bisogno, piuttosto che cambiare il sistema dall'alto. Sei così sensibile che un rifiuto alla tua offerta di aiuto ti ferisce nel profondo. Sai adattarti a qualsiasi lavoro, come un camaleonte, ma la tua vera casa è il contatto con la gente: viaggi, accoglienza, comunicazione. Nelle relazioni sei aperto e accogliente con tutti, ma ami in modo particolare chi ce la mette tutta per farcela, anche quando la vita è dura.",
                    'consiglio': "🕊️ La tua sensibilità è un dono, ma proteggila. Non tutti meritano il tuo aiuto, e va bene così. Impara a dire di no a chi ti prosciuga."
                }
            },

            'sole_plutone_sestile': {
                'sestile': {
                    'titolo': "☀️🌋 Sole in sestile con Plutone",
                    'messaggio': "Hai una consapevolezza profonda della tua forza interiore. Sai, nel tuo intimo, di poter fare qualsiasi cosa, perché nulla può fermarti quando decidi di agire. E sai anche che senza conoscenza non si va da nessuna parte: studi, impari, ti informi, perché solo così puoi realizzare il tuo destino. Parli in modo magnetico, la gente ti ascolta rapita, e sai usare questa dote per il bene comune. Sei un amministratore nato: gli altri si fidano di te, affidano i loro beni e i loro segreti. Hai un forte senso morale verso la società: combatti le ingiustizie con coraggio, senza mai stancarti di denunciare ciò che non va. In amore, sei una fonte di energia per chi ami, li sostieni e li incoraggi. Ami i misteri, l'occulto, lo yoga, e li capisci senza sforzo.",
                    'consiglio': "🔍 La tua forza è nella verità. Usala per smascherare le ingiustizie, ma anche per proteggere chi ami. La tua intuizione è il tuo radar: ascoltala sempre."
                }
            },

            'sole_ascendente_sestile': {
                'sestile': {
                    'titolo': "☀️⬆️ Sole in sestile con l'Ascendente",
                    'messaggio': "Hai una dote rara: sai esprimerti con eleganza e naturalezza, e quando parli la gente ti ascolta. Hai un'aria autorevole che dà credibilità a tutto ciò che dici. Sei una persona calorosa, e chi ti sta vicino si sente subito a suo agio. La tua freschezza ti permette di andare d'accordo con tutti, giovani e anziani, senza distinzioni. Sei magnetico: la gente è attratta da te e ti offre aiuto senza che tu lo chieda. Sei brillante, spiritoso, e in qualsiasi riunione sei tu a ravvivare l'atmosfera. Sul lavoro, però, a volte soffri perché le tue idee non vengono apprezzate come meritano. La tua sicurezza può persino intimorire i capi, che cercano di metterti in ombra. E non sopporti che si approprino delle tue idee. Sii più cauto nel mostrare il tuo pensiero, ma senza perdere la tua innata simpatia.",
                    'consiglio': "🦋 La tua luce è forte, ma impara a dosarla. Non hai bisogno di mostrare tutto subito: a volte il silenzio protegge le idee più preziose. La tua simpatia è la tua arma migliore, usala con saggezza."
                }
            },

            # LUNA (sestili)
            'luna_mercurio_sestile': {
                'sestile': {
                    'titolo': "🌙💬 Luna in sestile con Mercurio",
                    'messaggio': "Hai una mente pensierosa e sensibile, una curiosità insaziabile e una memoria che non dimentica nulla. Il tuo più grande desiderio è essere utile agli altri, e questo ti spinge a imparare sempre cose nuove. Raramente le tue emozioni ti offuscano la ragione: riesci a risolvere i problemi con chiarezza, senza farti travolgere. Sei indulgente e comprensivo, e per questo hai amici di ogni tipo. Le cose nuove ti affascinano e non ti fermi finché non le hai capite fino in fondo. Sei colto e piacevole da ascoltare: la tua positività è contagiosa e chi ti ascolta si sente subito meglio. Senti quasi a pelle quando qualcuno è falso o disonesto. In amore, cerchi persone colte, brillanti, che sanno quello che vogliono. Per te, comunicare con chi ami è fondamentale: il silenzio lo trovi noioso.",
                    'consiglio': "📖 La tua mente è un giardino rigoglioso. Coltivalo ogni giorno, ma ricordati di lasciare che gli altri possano passeggiarci dentro senza sentirsi giudicati. La tua sensibilità è la tua guida."
                }
            },

            'luna_venere_sestile': {
                'sestile': {
                    'titolo': "🌙❤️ Luna in sestile con Venere",
                    'messaggio': "Hai una naturale disposizione a rendere felici le persone che ami. Sai quello che vuoi dalla vita, ma desideri anche che chi ti sta accanto lo condivida con te. La tua immaginazione è ricca e sai usarla per rendere il tuo rapporto di coppia sempre vivo e interessante. Sei creativo, tenero, affettuoso, e per mantenere viva la fiamma sei disposto al compromesso, purché anche l'altro faccia lo stesso. Superi le piccole crisi con facilità, perché sai che un dialogo sincero risolve tutto. Sei socievole, hai sempre una parola gentile per tutti, e anche nei momenti difficili non perdi l'ottimismo. Amministri bene le tue finanze e ti arrabbi se qualcuno, anche un amico, ti chiede prestiti: temi per la sicurezza della tua famiglia. Ma se capisci che il bisogno è vero, allora aiuti, a patto che siano gli altri a decidere come e quando restituire.",
                    'consiglio': "💖 Il tuo cuore è grande, ma non deve diventare un bancomat. Impara a proteggere la tua serenità familiare senza chiudere la porta a chi ha davvero bisogno. La generosità è bella, ma deve essere ricambiata con rispetto."
                }
            },

            'luna_marte_sestile': {
                'sestile': {
                    'titolo': "🌙🔥 Luna in sestile con Marte",
                    'messaggio': "Sei una persona emotivamente intensa, ma hai imparato a gestire le tue reazioni. Quando qualcuno ti provoca, senti l'impulso di scattare, ma la tua maturità ti porta a fermarti, a ragionare, e solo dopo eventualmente a reagire. Qualche volta perdi le staffe, ma non serbi rancore: preferisci chiarire subito, discutere, e lasciare sempre una porta aperta per tornare a parlare. Questo atteggiamento ti rende grande agli occhi degli altri. Sei vitale, energico, e la tua presenza entusiasma chi ti sta intorno. Vai d'accordo con quasi tutti, colleghi e amici, perché sai di avere un carattere impulsivo e concedi agli altri il beneficio del dubbio. La tua vulnerabilità ti rende umano e sensibile. A casa, dopo una giornata di lavoro, sei come un gatto che si acciambella: il tuo rifugio dove ricaricarti.",
                    'consiglio': "🔥 La tua energia è un fuoco che scalda, ma non deve bruciare. Impara a spegnerlo quando sei a casa: la famiglia è il tuo porto sicuro, non il campo di battaglia. E mai mangiare arrabbiato: il cibo non lo merita."
                }
            },

            'luna_giove_sestile': {
                'sestile': {
                    'titolo': "🌙✨ Luna in sestile con Giove",
                    'messaggio': "Sei una persona che unisce intelligenza e cuore in modo raro. La tua personalità è ricca e affascinante, perché ogni tua emozione è accompagnata dalla curiosità di capire. Vai d'accordo con tutti perché sai leggere dentro le persone, sia negli affari che nelle relazioni. Parli di tutto con competenza e ai party sei sempre al centro dell'attenzione. Non dimentichi mai un favore ricevuto e da ogni esperienza trai il meglio. Brilli in tutte le professioni che richiedono acutezza e cultura: medicina, insegnamento, finanza, assistenza sociale. Hai una memoria eccezionale e una grande comprensione per chi soffre: sai infondere speranza con poche parole. Se tenessi un diario, ne verrebbe fuori un libro meraviglioso. I tuoi rapporti sono sempre sinceri e pieni di calore. Con chi ami, condividi tutto, nel bene e nel male. Sei ottimista, a volte anche un po' vanitoso, ma sempre con il cuore in mano per aiutare chi ha bisogno.",
                    'consiglio': "📚 La tua mente è un tesoro, ma il tuo cuore lo è ancora di più. Usa entrambi per costruire ponti, non per fare sfoggio. L'ottimismo è la tua forza, ma non dimenticare che a volte serve anche un po' di sana prudenza."
                }
            },

            'luna_saturno_sestile': {
                'sestile': {
                    'titolo': "🌙⏳ Luna in sestile con Saturno",
                    'messaggio': "Sei una persona seria, riservata, prudente. Da bambino hai imparato ad ascoltare i problemi degli altri, forse dei fratelli, e ora che sei adulto sei ancora lì, pronto ad aiutare chi è in difficoltà. Sai che per risolvere un conflitto bisogna andare a fondo delle emozioni, e questo tuo approccio funziona quasi sempre. La tua intelligenza unita alla tua integrità ti rende adatto a mille professioni: medicina, legge, politica, insegnamento. Affronti i problemi con calma e praticità, senza perderti in sogni a occhi aperti. Sei ambizioso quanto basta, e impari cose nuove senza mai sacrificare la tua onestà. Se insegni, i tuoi allievi ti adorano perché spieghi con chiarezza e sicurezza. Non sopporti i fannulloni. Hai pochi amici, ma veri, quelli di cui ti fidi ciecamente. In amore, cerchi una persona seria come te, con cui condividere progetti e rispetto. Per te, una relazione solo fisica è inconcepibile: hai bisogno di testa e cuore.",
                    'consiglio': "⏳ La tua serietà è una roccia. Appoggiati a chi la pensa come te, ma non chiudere la porta a chi è diverso. A volte la leggerezza può insegnarti cose che la serietà non vede."
                }
            },

            'luna_urano_sestile': {
                'sestile': {
                    'titolo': "🌙⚡ Luna in sestile con Urano",
                    'messaggio': "Hai capito presto nella vita di essere diverso dagli altri. Hai imparato da situazioni che per molti sarebbero passate inosservate. I tuoi genitori forse si chiedevano perché non fossi come gli altri bambini. La verità è che eri semplicemente più avanti: il tuo sviluppo emotivo e intellettuale è stato precoce, forse perché non sei mai stato troppo legato al passato. Rispetti le lezioni della storia, ma il tuo sguardo è sempre al futuro. Insegnare è la tua strada: sai trasmettere agli studenti l'entusiasmo della scoperta, fai rivivere la storia, la drammatizzi, e così aiuti tutti a capire meglio. Il tuo sogno è liberare l'umanità dall'ignoranza. Che tu sia scrittore, giornalista, politico o ricercatore, hai il dono di smuovere le coscienze. Se fai ricerca, però, lavora da solo: la lentezza altrui ti innervosisce. La tua intuizione è fulminea e risolvi problemi impossibili con facilità. In amore, hai bisogno di una relazione basata sulla logica e l'intelligenza: le sole emozioni non ti bastano.",
                    'consiglio': "⚡ La tua mente è un lampo. Illumina, ma non accecare. Lascia che gli altri ti seguano al loro passo, e non ti scordare che a volte la lentezza è madre della profondità. La tua intuizione è preziosa, ma non sostituisce il confronto con chi è diverso da te."
                }
            },

            'luna_nettuno_sestile': {
                'sestile': {
                    'titolo': "🌙🌊 Luna in sestile con Nettuno",
                    'messaggio': "Hai un'immaginazione vivida e una sensibilità quasi magica. Le sofferenze del mondo ti toccano nel profondo e senti il dovere di fare qualcosa. Quando vedi situazioni inaccettabili, non stai zitto: alzi la voce perché vengano presi provvedimenti. Questa tua passione per la giustizia ti apre molte strade. Scrivere è la tua vocazione, o qualsiasi lavoro che richieda di raccogliere prove e documentare la verità. Sei portato per il giornalismo d'inchiesta, quello che smaschera i poteri sporchi. Hai il dono di alleviare le pene altrui, come un medico che fa una diagnosi o un artista che trasforma il dolore in bellezza. In amore, sei comprensivo e non ti scandalizzi per le debolezze del partner: le capisci, le scusi, e così impari a conoscere ogni sfumatura dell'animo umano. La tua vita è piena e ricca, ma ricordati di ricaricare le energie ogni tanto.",
                    'consiglio': "🌊 La tua sensibilità è un oceano. Nuota in profondità, ma torna a galla per respirare. Il mondo ha bisogno della tua voce, ma anche del tuo sorriso. E quando sei stanco, fermati: il mare ha bisogno di bonaccia per tornare a splendere."
                }
            },

            'luna_plutone_sestile': {
                'sestile': {
                    'titolo': "🌙🌋 Luna in sestile con Plutone",
                    'messaggio': "Capisci l'amore con la testa, non solo con il cuore. Vai sempre a fondo delle motivazioni che spingono le persone ad agire, soprattutto quelle che ami. Per te l'amore è la cosa più importante, e sei così espansivo che ti aspetti che anche gli altri lo siano con te. Sei di quelli che hanno bisogno di sentirsi dire 'ti amo' spesso. La tua emotività è ben incanalata: sai essere tenero con i bambini e gli amici, ma sai anche essere passionale nei momenti giusti. Soffri per le pene altrui e cerchi in tutti i modi di aiutare. Sei pieno di risorse e di idee, sempre pronto a cogliere novità che semplifichino la vita. Hai un forte senso civico, e la tua specialità è capire i giovani e comunicare con loro. Loro si fidano di te e rispettano la tua autorità. Negli affari sei un manager nato: conquisti sicurezza finanziaria con intelligenza e competenza. La tua capacità di leggere la gente ti rende perfetto per lavori a contatto con il pubblico: assicurazioni, finanza, terapia.",
                    'consiglio': "🌋 La tua profondità è un vulcano. Lascia che la lava scorra, ma controllala. L'amore ha bisogno di calore, ma anche di tenerezza. E quando ascolti i giovani, ricordati che a volte hanno solo bisogno di essere ascoltati, non di essere giudicati."
                }
            },

            'luna_ascendente_sestile': {
                'sestile': {
                    'titolo': "🌙⬆️ Luna in sestile con l'Ascendente",
                    'messaggio': "Sei una persona sensibile e comprensiva, e chi si confida con te si sente subito al sicuro. Hai un po' di difficoltà a distinguere la realtà dalla fantasia, forse perché da bambino hai vissuto in un clima di critiche e insicurezze. Anche ora, da adulto, fatichi a separare i fatti dalle tue immaginazioni e tendi a sottovalutarti. Ma gli altri ti vedono diversamente: ti considerano competente e capace, e dovresti credergli. La tua mente è una miniera di idee: impara a sfruttarle, magari suggerendole ai tuoi capi. Per te il lavoro è importante e lo affronti con serietà. Quando superi i tuoi complessi, puoi competere con chiunque. In famiglia, dai tanto e speri che sia apprezzato. Hai tanti amici e ami le feste, dove brilli per la tua conversazione colta e piacevole.",
                    'consiglio': "🌟 Gli altri vedono in te ciò che tu ancora non vedi. Fidati di loro, e impara a fidarti di te. Le tue idee sono preziose: non tenerle nel cassetto. E ricorda, la realtà a volte è meno spaventosa di come la dipingi nella tua testa."
                }
            },

            # MERCURIO (sestili)
            'mercurio_venere_sestile': {
                'sestile': {
                    'titolo': "💬❤️ Mercurio in sestile con Venere",
                    'messaggio': "Sei una persona garbata e piacevole, e con te è facile andare d'accordo. Non sei uno che abbassa la testa: quando qualcuno ha torto, lo dici, ma con tatto e diplomazia, senza offendere. Spieghi le tue ragioni con calma e documenti ciò che dici, ma lasci sempre all'altro la possibilità di esprimere le sue idee. La tua gentilezza è preziosa, ma non ti rende adatto alle lotte di concorrenza spietate. Per questo è meglio che tu lavori da solo o in un piccolo gruppo affiatato. Ami recitare, parlare in pubblico, scrivere. Hai uno stile fresco e piacevole che piace a chi vuole informarsi senza annoiarsi. Sei anche bravo con i soldi: le tue idee finanziarie spesso si trasformano in denaro. I tuoi superiori si fidano di te, perché sanno che sei cauto e che non rischi niente senza prima esserti preparato.",
                    'consiglio': "🎭 La tua diplomazia è una danza elegante. Non aver paura di ballare anche sui terreni più difficili. La tua cautela è una garanzia, ma non farti bloccare dalla paura di osare."
                }
            },

            'mercurio_marte_sestile': {
                'sestile': {
                    'titolo': "💬🔥 Mercurio in sestile con Marte",
                    'messaggio': "Hai una mente acuta e una curiosità che non si ferma mai. Studi in continuazione, ti tieni aggiornato su tutto, vuoi essere sempre sicuro di quello che dici. Il tuo scopo più grande è ottenere l'approvazione degli altri, e per questo ti documenti a fondo prima di aprire bocca. Parli con passione e fantasia, e anche chi non è d'accordo con te finisce per lasciarsi convincere dalle tue argomentazioni, sempre solide e ben preparate. Sei cordiale e non aspetti di essere presentato per attaccare discorso. Adori stare in mezzo alla gente, parlare e ascoltare, perché così accumuli informazioni. Vai bene in mille lavori: legge, insegnamento, scrittura, pubbliche relazioni, giornalismo. La comunicazione è la tua arma. In politica potresti fare strada, perché ami le battaglie verbali. Sei amico di tutti, ma guai a chi ti tradisce: diventi tagliente come un bisturi.",
                    'consiglio': "🗡️ La tua mente è una spada affilata. Usala per difendere la verità, non per ferire. La tua curiosità è un dono, ma non trasformarla in ossessione. E ricordati che a volte il silenzio è più eloquente di mille parole."
                }
            },

            'mercurio_giove_sestile': {
                'sestile': {
                    'titolo': "💬✨ Mercurio in sestile con Giove",
                    'messaggio': "La tua mente è un vulcano in continua eruzione: non ti accontenti mai di quello che sai, devi sempre saperne di più. E non tieni la conoscenza per te: la usi, la metti a frutto, la condividi. Ragioni bene, parli meglio, e le tue parole sono così convincenti che potresti far cambiare idea a chiunque. Sei un pericolo pubblico per gli oratori impreparati: se dicono una cosa sbagliata, tu sei lì pronto a contestarli. Ma attenzione: la conoscenza è un'arma potente. Puoi fare grandi cose come oratore o scrittore, nell'insegnamento o nel giornalismo. I viaggi ti aprono la mente e ti aiutano a capire culture diverse. In campo religioso, non sei bigotto, ma riconosci che credere in qualcosa è importante. Sei tollerante e non imponi le tue idee a nessuno.",
                    'consiglio': "📚 La tua sete di sapere è ammirevole, ma ricordati che la conoscenza senza saggezza è come un motore senza freni. Usa la tua eloquenza per costruire, non solo per vincere dibattiti. E non dimenticare che a volte l'ignoranza è solo diversa conoscenza."
                }
            },

            'mercurio_saturno_sestile': {
                'sestile': {
                    'titolo': "💬⏳ Mercurio in sestile con Saturno",
                    'messaggio': "Hai una mente profonda e disciplinata. Credi in te stesso e sai come dimostrare il tuo valore. Hai il coraggio delle tue opinioni e le sostieni con fatti e numeri. Da bambino hai imparato a contare solo su di te, studiando e impegnandoti, perché sapevi che la cultura ti avrebbe aiutato nella vita. Cerchi risposte che ti facciano progredire, e hai molti campi in cui realizzarti: educazione, politica, scienza, ricerca, architettura. Il successo te lo sudi, non ti cade dal cielo. Sei sempre stato precoce e forse preferivi la compagnia degli adulti. A scuola ti annoiavi perché eri più veloce degli altri. Studierai per tutta la vita, e questo si vede nella tua correttezza e nel tuo buon gusto, che attirano la simpatia di tutti. Forse un giorno scriverai le tue memorie. I tuoi scritti sono profondi, ben documentati. In amore, cerchi persone mature e sincere, e una relazione solo fisica non fa per te. Potresti anche innamorarti di una persona più giovane, purché ci sia intesa intellettuale.",
                    'consiglio': "⏳ La tua mente è un orologio svizzero: precisa, affidabile, inarrestabile. Ma anche gli orologi hanno bisogno di essere caricati. Concediti delle pause, lascia che la tua testa si riposi. E in amore, non cercare la perfezione: a volte il cuore batte per strade che la mente non ha ancora mappato."
                }
            },

            'mercurio_urano_sestile': {
                'sestile': {
                    'titolo': "💬⚡ Mercurio in sestile con Urano",
                    'messaggio': "Hai una mente fuori dal comune. Impari in fretta, ma sei anche tollerante con chi è più lento. Sei sveglio, curioso, colto, e parli in modo così affascinante che chi ti ascolta resta incantato. Ma non tieni la tua conoscenza per te: sei sempre disponibile con chi vuole imparare. Da bambino hai stupito i tuoi genitori con la tua precocità. Da adulto, la tua strada è l'insegnamento o qualsiasi attività che ti permetta di esprimere la tua intelligenza in libertà. La libertà di pensiero è sacra per te. Sei progressista e non ami i metodi tradizionali, anche se rispetti le lezioni del passato. Sei entusiasta e contagi gli altri con la tua fiamma. Per avere successo, però, devi imparare la disciplina e la costanza. La tua vita sarà una continua ricerca dei perché. Ma non aspettare le risposte: realizzati ora. La tua mente è sempre in fermento: impara a rilassarti, o rischi l'esaurimento.",
                    'consiglio': "⚡ La tua mente è un fulmine: illumina, ma può anche bruciare. Impara a incanalare la tua energia in un punto alla volta, e concediti il lusso di non pensare a niente. Il domani arriverà comunque, con o senza risposte."
                }
            },

            'mercurio_nettuno_sestile': {
                'sestile': {
                    'titolo': "💬🌊 Mercurio in sestile con Nettuno",
                    'messaggio': "Hai un'immaginazione fertile e un'intuizione che ti fa risolvere i problemi più difficili con una facilità sorprendente. Hai sete di conoscenza, ma sei anche consapevole che le apparenze ingannano, e per questo vai a fondo in ogni cosa prima di accettarla come vera. Sai interpretare gli avvenimenti e impari dalle esperienze degli altri. Il tuo talento creativo ti apre molte strade: giornalismo, insegnamento, arte, musica, medicina, assistenza sociale. Qualunque cosa tu faccia, però, deve metterti in contatto con la gente. Per esprimere al meglio la tua immaginazione, devi studiare, formarti, andare in profondità. Le tue possibilità sono illimitate. In amore, sei caldo e sincero, ma preferisci persone con una mente filosofica, non assillate da problemi materiali. Sei idealista, ma non pretendi la perfezione: accetti chi lotta per migliorarsi. Sei guidato da una chiara percezione delle tue responsabilità morali e sociali.",
                    'consiglio': "🌊 La tua intuizione è un sestante: ti guida in mari sconosciuti. Usala per esplorare, ma non dimenticare di guardare le stelle. La tua creatività è un dono per il mondo, ma per donarlo devi prima coltivarlo. Studia, impara, cresci."
                }
            },

            'mercurio_plutone_sestile': {
                'sestile': {
                    'titolo': "💬🌋 Mercurio in sestile con Plutone",
                    'messaggio': "Hai una mente analitica che scava in profondità e afferra gli argomenti più oscuri, quelli che di solito sfuggono alla comprensione umana. Hai capacità psichiche molto pronunciate, anche se forse non te ne rendi conto. Con gli anni ne prenderai coscienza e le userai sempre di più. Riesci a trovare spiegazioni plausibili per eventi misteriosi. Puoi fare carriera in molti campi: investigazione, psicologia, ricerca, medicina, chirurgia, insegnamento. Se insegni, lo fai per aiutare gli altri a trovare la verità. Se fai ricerca, arrivi alla soluzione ancora prima di dimostrarla. Hai il compito di guidare chi cerca risposte. Sei aperto a tutte le idee nuove e ti tieni aggiornato. Potresti anche ottenere finanziamenti per sviluppare progetti innovativi, perché trasmetti serietà e onestà. La tua immaginazione è preziosa per risolvere situazioni impossibili. In amore sei sincero e pretendi sincerità. Se scopri una bugia, la relazione finisce per sempre. Hai bisogno di un partner onesto, aperto al dialogo, che creda in te e nelle tue ambizioni. Con i soldi te la cavi bene, anche con poche entrate.",
                    'consiglio': "🔍 La tua mente è uno scandaglio: arriva dove pochi possono. Usa questa dote per scoprire la verità, non per smascherare gli altri. La tua sincerità è la tua forza, ma a volte un po' di diplomazia in più non guasta. E ricordati che i misteri più belli sono quelli che restano tali."
                }
            },

            'mercurio_ascendente_sestile': {
                'sestile': {
                    'titolo': "💬⬆️ Mercurio in sestile con l'Ascendente",
                    'messaggio': "Sei brillante, spiritoso, e hai una curiosità che non si ferma mai. Conosci i tuoi pregi e i tuoi difetti, e quando sei con gli altri mostri sempre il tuo lato migliore per metterli a loro agio. Parli in modo chiaro e non lasci dubbi su ciò che pensi. Sei sempre informato e aggiornato, e in tua compagnia la conversazione non si spegne mai. La comunicazione è la tua arma vincente nel lavoro. Ami discutere, ma non per fare polemica: per te è un piacevole passatempo. Hai tante idee e speri che diventino fonte di guadagno. I tuoi amici ti incoraggiano e ti fanno i complimenti per la tua intelligenza. Metti queste doti al servizio della professione: il tuo giudizio è sicuro e i tuoi suggerimenti sono preziosi. Attento però che i superiori non si approprino delle tue idee. Capisci le motivazioni della gente e questo ti rende perfetto per lavorare a contatto con il pubblico, che tu ami e sai come trattare.",
                    'consiglio': "💡 La tua mente è un faro. Illumina gli altri, ma non abbagliarli. Condividi le tue idee, ma impara a proteggerle. La comunicazione è la tua forza, ma a volte il silenzio è il miglior complice."
                }
            },

            # VENERE (sestili)
            'venere_marte_sestile': {
                'sestile': {
                    'titolo': "❤️🔥 Venere in sestile con Marte",
                    'messaggio': "Hai una natura calda e affettuosa, e sai aspettare la persona giusta prima di mostrare i tuoi sentimenti. Non ti accontenti dell'attrazione fisica: vuoi anche intesa intellettuale e affinità sociale. Sai che per conquistare un'amicizia a volte serve un compromesso, e questo tuo atteggiamento piace alla gente. Non ami i lati squallidi della vita, preferisci goderti le cose belle. La musica, la letteratura, l'arte ti nutrono l'anima. Ami la compagnia e le relazioni sociali piacevoli. Non hai una vocazione specifica, ma qualsiasi lavoro che ti metta in contatto con la gente fa per te. Anche con gli sconosciuti trovi subito un argomento comune per rompere il ghiaccio. Sei ottimista, hai sempre un sorriso. Nelle pubbliche relazioni saresti un fenomeno. Hai molti amici, anche di vecchia data, e dei litigi passati ricordi solo le cose belle. In amore, cerchi una persona che collabori con te per costruire una vita piacevole. Il matrimonio, per amore o per convenienza, ti riuscirà bene. Il tuo problema sono i soldi: spendi più di quanto guadagni. Un po' di prudenza in più non guasterebbe.",
                    'consiglio': "💞 Il tuo cuore è una fiamma che scalda. Impara a dosare il combustibile, altrimenti rischi di bruciare tutto in una volta. I soldi sono importanti, ma non sono tutto: a volte le cose più belle sono gratis. E in amore, la pazienza è la chiave di tutto."
                }
            },

            'venere_giove_sestile': {
                'sestile': {
                    'titolo': "❤️✨ Venere in sestile con Giove",
                    'messaggio': "Sei una persona cordiale, espansiva, e la gente ti vuole bene. Sai sempre cosa dire al momento giusto e ottieni ciò che vuoi con garbo. Sei generoso di lodi anche con chi non le merita, e trovi sempre tempo per chi ha bisogno. Anche i pessimisti più incalliti, dopo averti parlato, si sentono sollevati. Non ti intrometti negli affari altrui, ma se qualcuno ti cerca, ci sei. In amicizia, sei popolare perché non giudichi e non ti imponi. Non hai una vocazione precisa, ma la tua bella presenza è un vantaggio in molte professioni. Vai bene in tutti i lavori a contatto con il pubblico: rappresentanza, guide turistiche, insegnamento. Potresti anche scrivere novelle o articoli, ma niente di troppo impegnativo. Quello che desideri veramente è una bella vita, una casa confortevole, buoni amici e una vivace vita sociale. La vita austera non fa per te. Oltre al lavoro, hai mille interessi: letture, viaggi, musica, teatro. E non sei solo spettatore, ma partecipi attivamente.",
                    'consiglio': "✨ La tua gioia di vivere è un regalo per chi ti sta intorno. Continua a spargere sorrisi, ma ricordati di fare anche il pieno per te. La vita non è solo divertimento, ma tu lo sai già. Usa la tua popolarità per fare del bene, senza perdere di vista la sostanza."
                }
            },

            'venere_saturno_sestile': {
                'sestile': {
                    'titolo': "❤️⏳ Venere in sestile con Saturno",
                    'messaggio': "Sai cosa vuoi dalla vita e sei disposto a sacrificarti per ottenerlo. Sai che niente viene gratis, e per questo accetti le responsabilità e lavori in silenzio, senza lamentarti. La tua infanzia e giovinezza ti hanno preparato ad affrontare impegni pubblici e privati. Sei sincero, onesto, giusto, e la gente ti rispetta. Sanno che possono contare su di te. Tu, però, non chiedi mai niente a nessuno: conti solo sulle tue forze. Fai le cose con ordine e programmi tutto nei minimi dettagli. Hai un fiuto eccezionale e un grande senso del giudizio. Sai comunicare con chiarezza e sai anche ascoltare chi ha più esperienza di te. Vai bene in banca, finanza, immobiliare, assicurazioni, progettazione. Lavorare con te è facile, perché sei paziente e hai tatto. In amore, non ti apri finché non sei sicuro di essere ricambiato. Sai che incontrerai la persona giusta per una vita piena e felice. Qualcuno ti considera timido, ma in realtà sei solo riservato con chi non conta. Hai buone maniere, gusto raffinato, e detesti la volgarità. I tuoi fratelli o sorelle spesso cercano il tuo consiglio.",
                    'consiglio': "⏳ La tua serietà è una cattedrale: imponente e solida. Ma anche le cattedrali hanno bisogno di luce e di colore. Non essere troppo severo con te stesso e con gli altri. A volte la vita è più semplice di come la dipingi. E in amore, il primo passo a volte lo devi fare tu."
                }
            },

            'venere_urano_sestile': {
                'sestile': {
                    'titolo': "❤️⚡ Venere in sestile con Urano",
                    'messaggio': "Sei bravo nei rapporti sociali, risolvi i problemi della vita con competenza e hai un fascino magnetico in amore. Sai come destreggiarti e vai d'accordo con tutti, perché trasmetti comprensione e simpatia. Hai grandi speranze per te stesso, ma senza calpestare quelle degli altri. Comunichi con calore e la gente capisce quanto ti interessi a loro. Non sei una minaccia per nessuno, e questo mette tutti a loro agio. Ami intensamente la libertà, la tua e quella altrui. Ti fai molti amici, e durano nel tempo. La tua creatività può esprimersi in attività sociali o artistiche. Insegnare ai bambini è una delle tue strade: il tuo senso del drammatico rende lo studio un gioco. Vai bene anche con i gruppi: sei distaccato abbastanza per essere obiettivo, ma anche sensibile abbastanza per capire. In politica potresti far bene, perché ti impegneresti per essere all'altezza della fiducia ricevuta. In amore, sei caloroso e romantico, e fai di tutto perché la relazione sia sempre eccitante. I soldi per te sono solo un mezzo, non un fine.",
                    'consiglio': "⚡ La tua libertà è come l'aria: indispensabile. Ma anche l'aria, se è troppo rarefatta, non fa respirare. Cerca un equilibrio tra la tua voglia di indipendenza e la necessità di legami profondi. L'amore vero non imprigiona, ma fa volare più in alto."
                }
            },

            'venere_nettuno_sestile': {
                'sestile': {
                    'titolo': "❤️🌊 Venere in sestile con Nettuno",
                    'messaggio': "Hai un'immaginazione fertile e la capacità di tradurla in realtà. Le tue sensazioni diventano schemi e realizzazioni che tutti possono riconoscere. Trovi sempre il modo di esprimere la tua creatività e la tua ricchezza interiore. Sei compassionevole per natura, capisci le lotte e i problemi degli altri. Puoi fare tante professioni, ma hai un dono speciale: sai consolare e calmare il dolore. La medicina o la fisioterapia potrebbero fare al caso tuo. Sei un mediatore nato: anche nelle situazioni più tese, riesci a riportare un po' di ordine. Organizzare eventi sociali è un altro talento. Se lavori in proprio, l'arte, la musica, la scrittura sono la tua strada. Sei un romantico, emotivamente vulnerabile, e per questo sei attratto da persone raffinate che, come te, detestano le brutture della vita. Quando ami, ti butti anima e corpo, pronto a tutto pur di far funzionare la relazione. Ma quando arrivano le difficoltà, tendi ad abbatterti più degli altri. Impara a reagire.",
                    'consiglio': "🌊 La tua anima è un arcobaleno dopo la pioggia. Splendi di colori che altri non vedono. Usa questa luce per illuminare chi soffre, ma non dimenticare di proteggere il tuo cuore. L'amore è una danza: a volte si guida, a volte ci si lascia guidare. L'importante è non smettere mai di ballare."
                }
            },

            'venere_plutone_sestile': {
                'sestile': {
                    'titolo': "❤️🌋 Venere in sestile con Plutone",
                    'messaggio': "Capisci a fondo il potere che l'amore ha sull'essere umano. Sai che una relazione, per essere vera, richiede adattamento da entrambe le parti. Per te l'armonia è fondamentale, perché permette all'intesa fisica di durare nel tempo. Per questo, prima di impegnarti, cerchi subito di stabilire un buon livello di comunicazione con l'altro. Spesso sei attratto dalla bellezza fisica, ma poi scopri che sotto c'è il vuoto, e allora fai marcia indietro. In generale, però, sai valutare bene le persone e le loro intenzioni, perché sei rimasto fedele ai valori dell'amore che avevi da ragazzo. Non perdi tempo in avventure casuali: vuoi una relazione solida, basata su interessi comuni. Nella vita sociale, non sopporti l'indifferenza dei potenti verso i bisogni umani. Sei capace di arrivare agli estremi pur di smascherare le loro colpe, e poi usi tutti i mezzi di comunicazione per denunciarle. Vai bene in finanza, assicurazioni, amministrazione, notaio. Questi lavori ti permettono di esprimere le tue capacità e di essere utile agli altri.",
                    'consiglio': "🌋 La tua passione è un vulcano. Lascia che la lava scorra, ma controlla che non bruci ciò che ami. La tua capacità di leggere dentro le persone è un dono raro: usalo per costruire relazioni vere, non per smascherare tradimenti. A volte, quello che cerchi è già lì, davanti a te."
                }
            },

            'venere_ascendente_sestile': {
                'sestile': {
                    'titolo': "❤️⬆️ Venere in sestile con l'Ascendente",
                    'messaggio': "Cerchi sempre di mantenere buoni rapporti con tutti, e sei pronto a scendere a compromessi se serve. Sei un mediatore nato, e spesso intervieni per fare da paciere. Quando hai un contrasto con qualcuno, gli concedi sempre il beneficio del dubbio, pensando che prima o poi si renderà conto di aver sbagliato. Non imponi mai le tue idee, preferisci trovare un punto d'incontro a metà strada. Sai cosa vuoi dalla vita, e non ne fai mistero con nessuno. Sei timido, ma non te ne stai in disparte. Quello che vuoi veramente è una vecchiaia sicura, senza problemi economici, e per questo lavori sodo. Sul lavoro, fai tutto quello che ci si aspetta da te, ma attento a non essere troppo confidenziale con superiori e colleghi: a volte sei troppo indulgente e loro ne approfittano. Sei onesto, stai dalla parte della legge, e hai il terrore di finire in situazioni legali spiacevoli. Non farti coinvolgere nei problemi legali degli altri. In generale, però, i tuoi rapporti sono piacevoli e i pochi problemi si risolvono con un po' di compromesso.",
                    'consiglio': "🕊️ La tua anima è una colomba: cerchi pace e armonia. È un dono prezioso, ma non deve diventare una gabbia. Impara a dire di no, a difendere i tuoi confini. La bontà è bella, ma deve essere intelligente. E ricordati che la vera pace non è assenza di conflitti, ma la capacità di gestirli con saggezza."
                }
            },

            # MARTE (sestili)
            'marte_giove_sestile': {
                'sestile': {
                    'titolo': "🔥✨ Marte in sestile con Giove",
                    'messaggio': "Hai la capacità di usare le tue energie mentali e fisiche per raggiungere grandi obiettivi. Sei ambizioso, pieno di idee, e fai di tutto per realizzarle. Da bambino inventavi giochi in cui mettevi alla prova la tua immaginazione e la tua voglia di vincere. Da adulto, sai usare la mente e la parola con abilità. Non ti tiri mai indietro in una discussione, e intervieni con argomenti documentati e un'eloquenza che trascina. Sei anche pronto a difendere chi non sa parlare bene o non ha abbastanza argomenti. Vai bene in mille professioni, ma quelle intellettuali sono le tue preferite: avvocato, insegnante, attore, politico, scrittore. Dovunque tu sia, ti fai notare. Non cerchi tanto i riconoscimenti, quanto la possibilità di usare tutto il tuo talento. Sei franco, non hai peli sulla lingua e non edulcori la verità. In amore, sei attratto da persone con le idee chiare, che sanno quello che vogliono e hanno il coraggio delle proprie opinioni. Per te, onestà e integrità sono condizioni essenziali. Hai sentimenti intensi e hai bisogno di un partner che la pensi come te, con cui condividere tutto.",
                    'consiglio': "🚀 La tua energia è un razzo: decolla diritto verso le stelle. Ma anche i razzi hanno bisogno di carburante e di manutenzione. Non bruciare tutto in una volta. La tua lealtà è la tua forza, ma non pretendere che tutti siano come te. A volte, chi è diverso ha molto da insegnarti."
                }
            },

            'marte_saturno_sestile': {
                'sestile': {
                    'titolo': "🔥⏳ Marte in sestile con Saturno",
                    'messaggio': "Hai la rara capacità di unire braccio e mente. Fai le cose con intelligenza, in modo da non doverle rifare. Prima pensi, poi agisci, e i risultati si vedono. Se qualcuno ti chiede qualcosa, è meglio che lo faccia in modo logico e chiaro, se vuole ottenere qualcosa. Con autodisciplina e pazienza, riesci a fare molto più degli altri e ad avere più successo, perché non hai fretta e vai a fondo in ogni questione. Preferisci i lavori manuali, ma che richiedano anche intelligenza. Per te sono perfetti: archeologia, esplorazioni, servizio forestale, gestione di parchi, ricerca industriale, educazione fisica. I tuoi hobby potrebbero diventare lavori redditizi. Ami le discussioni di gruppo e sai metterti in evidenza con la tua abile oratoria. Quando parli, sei sempre ben documentato. Potresti anche fare politica, almeno a livello locale. In amore, cerchi una persona poliedrica, che completi la tua natura e condivida i tuoi interessi. Rispetti le leggi e le autorità, che vedi come una protezione. Sei tenace e non accetti sconfitte, e trasmetti questo ai tuoi figli, con l'esempio. Sei orgoglioso dei loro successi, anche se fatichi a mostrarlo.",
                    'consiglio': "⚖️ La tua forza è nell'equilibrio tra azione e pensiero. Mantieni questa bilancia in perfetto assetto. La tua tenacia è la tua arma, ma non deve diventare ostinazione. E con i figli, un abbraccio vale più di mille parole non dette."
                }
            },

            'marte_urano_sestile': {
                'sestile': {
                    'titolo': "🔥⚡ Marte in sestile con Urano",
                    'messaggio': "Sei una persona impaziente e piena di energia, sempre alla ricerca di nuovi modi per sfogarti. Sei curioso, hai le idee chiare e non hai paura di dichiararle. Quando decidi di agire, lo fai subito: non sopporti chi rimanda sempre. Hai ottime capacità strategiche e i tuoi progetti non falliscono mai, anche se pensi sempre che si possa migliorare. Godi di ottima salute e hai un'energia enorme, ma attento agli esaurimenti nervosi. Sei portato per lavori che richiedono originalità e prontezza. Sei cosciente del presente ma guardi al futuro, e per questo la ricerca e lo sviluppo industriale fanno per te. Anche l'insegnamento ti si addice, perché puoi dare un contributo importante alla società. Hai mille interessi e partecipi con successo a tutto. Non accetti sconfitte. Sei un ribelle intellettuale, pronto a contestare vecchi ideali che consideri superati. Ti impegni nel sociale, partecipi ad attività benefiche e movimenti di riforma. In amore, cerchi una persona che abbia i tuoi stessi interessi e la tua stessa visione della vita, per evitare conflitti e frustrazioni.",
                    'consiglio': "⚡ La tua mente è un circuito ad alta tensione. Impara a isolarlo quando serve, per non bruciare i fusibili. La tua voglia di futuro è ammirevole, ma non dimenticare che il presente è l'unico tempo che abbiamo. E in amore, le differenze possono essere una ricchezza, non solo un problema."
                }
            },

            'marte_nettuno_sestile': {
                'sestile': {
                    'titolo': "🔥🌊 Marte in sestile con Nettuno",
                    'messaggio': "Capisci la differenza tra passione e compassione. Sai che ci sono momenti in cui devi soddisfare i tuoi desideri, e altri in cui devi assecondare quelli degli altri. Hai la grande responsabilità di servire chi è più debole. La tua strada potrebbe essere la medicina o i campi affini: hai speciali capacità terapeutiche, forse dovute alla tua enorme fede e sincerità. Hai un senso del ritmo molto sviluppato, perfetto per danza, recitazione, cultura fisica. Sei sentimentale e tendi ad attribuire onestà e alti ideali a tutti. Sei indulgente con i difetti altrui e ti aspetti lo stesso. In amore, vedi sempre il lato positivo del partner, anche quando si comporta male. Per te la comunicazione sincera è fondamentale. Scopri la mancanza di sincerità anche se è ben nascosta. I tuoi desideri fisici ed emotivi sono forti, ma non ti abbassi a compromessi con i tuoi ideali per una persona volgare. Queste qualità sono rare e preziose. La tua sensibilità ti fa conoscere i tuoi limiti.",
                    'consiglio': "🌊 La tua anima è un oceano di compassione. Nuota in superficie per goderti la vita, ma tuffati in profondità per capire il dolore altrui. La tua sensibilità è un dono, ma non deve farti annegare. Impara a distinguere chi merita la tua indulgenza e chi no."
                }
            },

            'marte_plutone_sestile': {
                'sestile': {
                    'titolo': "🔥🌋 Marte in sestile con Plutone",
                    'messaggio': "Ami la verità sopra ogni cosa, e sei profondamente convinto della sua importanza. Parli con una forza che attira l'attenzione di tutti, singoli, gruppi, organizzazioni. Riesci a mettere in moto riforme sociali, a denunciare l'incuria delle istituzioni. Capisci le motivazioni della gente e non vieni mai colto di sorpresa. Nei rapporti personali, metti subito in chiaro le tue idee, per evitare malintesi. Pretendi lo stesso dagli altri, amici o nemici che siano. Non sopporti sottintesi e sottigliezze. A volte accetti le idee altrui, se valgono. Parli sempre chiaro e non cambi idea per compiacere. Parli spesso dei tuoi progetti, ma devi anche realizzarli. A volte sembra che tu faccia tante cose, ma sono solo parole. Hai forti desideri sessuali, ma non ti butti in storie basate solo sul fisico: per te una relazione deve avere molte altre affinità.",
                    'consiglio': "🌋 La tua passione per la verità è un vulcano in eruzione. Lascia che la lava scorra, ma controlla che non travolga tutto. Le parole sono importanti, ma i fatti lo sono ancora di più. E in amore, l'affinità elettiva è tutto: non accontentarti di meno."
                }
            },

            'marte_ascendente_sestile': {
                'sestile': {
                    'titolo': "🔥⬆️ Marte in sestile con l'Ascendente",
                    'messaggio': "Hai una forza espressiva che non passa inosservata. Dici sempre quello che pensi, senza giri di parole e senza preoccuparti troppo di chi hai di fronte. Ti metti in mostra con entusiasmo e impulsività. Il tuo modo di parlare, però, a volte è così intenso che mette la gente sulla difensiva. Sei come un cavo dell'alta tensione: pieno di energia, non stai fermo un attimo. Se non muovi il corpo, muovi la lingua, e lì iniziano i guai. In realtà vorresti avere buoni rapporti con tutti, ma il tuo modo di fare dice il contrario. Se solo ti fermassi un attimo a pensare prima di parlare, eviteresti molte gaffe. Cerchi l'ammirazione degli altri per la tua originalità e il tuo coraggio, ma in realtà hai un gran bisogno della loro solidarietà, perché non sei così sicuro come sembri. Lavori sodo, più del dovuto, perché hai una riserva di energia nervosa e vuoi dimostrare di essere bravo come gli altri. Ti tieni aggiornato e sai assumerti responsabilità. Se impari la disciplina, le tue capacità creative daranno grandi frutti. E quando ti concentri su una cosa sola, la porti a termine alla perfezione.",
                    'consiglio': "⚡ La tua energia è un fulmine: colpisce, ma può anche spaventare. Impara a scaricarla a terra prima che faccia danni. La disciplina non è una gabbia, è il binario che permette al treno di correre veloce senza deragliare. E ricorda: a volte, un sorriso vale più di mille parole."
                }
            },

            # GIOVE (sestili)
            'giove_saturno_sestile': {
                'sestile': {
                    'titolo': "✨⏳ Giove in sestile con Saturno",
                    'messaggio': "Ami la cultura sopra ogni cosa. Impari in fretta e ti tieni sempre aggiornato, e sai applicare anche le conoscenze più astratte alla vita pratica. Sei un classico: credi che la conoscenza poggi su solide basi tradizionali. Sei bravissimo a progettare, hai idee creative e buone probabilità di successo. Sei entusiasta e ottimista, ma anche prudente: non ti butti allo sbaraglio, sai che ogni progetto ha bisogno di cure. Sei sempre alla ricerca di nuovi modi per esprimerti, perché vuoi raggiungere il massimo del tuo potenziale. E lo fai sempre nei limiti della legge: per te è un punto d'onore riuscire senza sotterfugi. La tua passione per la filosofia ti ha insegnato che l'onestà alla fine trionfa. Vai bene in legge, insegnamento, giornalismo, politica, religione, scrittura. Lotti per migliorare le condizioni sociali e denunci i malgoverni, sempre con prove inconfutabili. Sei un insegnante nato: spieghi con entusiasmo e fai rivivere la storia. I tuoi allievi più dotati volano alto. In un certo senso, sei un portabandiera della giustizia sociale.",
                    'consiglio': "📚 La tua cultura è una torre, solida e imponente. Usala come faro, non come fortezza. La tua onestà è la tua armatura, ma a volte la flessibilità è più forte della rigidità. E ricordati che la giustizia non è solo denuncia, ma anche costruzione."
                }
            },

            'giove_urano_sestile': {
                'sestile': {
                    'titolo': "✨⚡ Giove in sestile con Urano",
                    'messaggio': "Sei un ottimista che crede nel futuro, e lo sai programmare con idee chiare e lungimiranza. Le tue possibilità di successo sono quasi illimitate. Sei curioso, entusiasta, e hai una sete di conoscenza inesauribile. Guardi sempre avanti, mai indietro: quello che hai davanti è troppo eccitante. Hai mille idee, tutte da realizzare, e quando decidi, niente ti ferma. La tua strada maestra è l'insegnamento, ma vai bene anche in politica, filosofia, religione, scienza, scrittura, occulto. Il tuo pensiero è avanzato e non si ferma davanti a nulla. La tua inventiva trova sempre nuove strade per tenere viva la fiamma dell'interesse per la vita. Per te l'onestà è sacra: se qualcuno ti tradisce, chiudi il rapporto senza rimpianti, in amore come in amicizia. Hai tanti amici, sei generoso e cordiale, ma se la fiducia viene meno, è finita. Senti un'affinità speciale per chi si ribella alle convenzioni e lotta per un futuro migliore.",
                    'consiglio': "⚡ La tua mente è un razzo diretto verso il futuro. Assicurati di avere abbastanza carburante per tornare indietro. La tua onestà è la tua forza, ma a volte il perdono è più forte della rottura. E ricordati che il futuro si costruisce anche con le mani di chi è rimasto indietro."
                }
            },

            'giove_nettuno_sestile': {
                'sestile': {
                    'titolo': "✨🌊 Giove in sestile con Nettuno",
                    'messaggio': "Hai una mente piena di immaginazione, studi la natura umana e cerchi le risposte per il futuro nelle lezioni del passato. Hai grandi speranze, ma sei un teorico: le tue soluzioni non sono sempre realistiche. Sai di avere dei doveri verso la società, ma non sei un uomo d'azione. Dai il tuo contributo in modo quieto, sensibilizzando l'opinione pubblica sui problemi sociali. Sei sensibile al malcostume politico e durante le campagne elettorali sostieni i candidati che promettono cambiamenti. Sei contrario ai gruppi che predicano ideologie senza agire davvero per il bene comune. Sei un idealista, il portavoce di chi non ha voce. Vai bene nelle organizzazioni sociali, politiche, religiose, perché non ti tiri indietro quando si tratta di migliorare l'ordine sociale. Potresti scrivere notiziari o bollettini. Capisci perché le persone si lasciano travolgere da certe ideologie e le aiuti a ritrovare la giusta prospettiva. In amore, però, sei un po' ingenuo: vedi nell'altro qualità che non ha, e quando scopri la verità, soffri. Sii più prudente, e cerca di non perderti nelle nuvole.",
                    'consiglio': "🌊 La tua immaginazione è un mare in tempesta: crea onde maestose, ma può anche affogarti. Impara a navigare con prudenza, senza perdere di vista la costa. In amore, abbassa le vele dell'idealizzazione e guarda l'altro per quello che è, non per quello che sogni. La realtà può essere meno affascinante, ma più vera."
                }
            },

            'giove_plutone_sestile': {
                'sestile': {
                    'titolo': "✨🌋 Giove in sestile con Plutone",
                    'messaggio': "Hai una mente curiosa e penetrante, capace di scoprire le verità nascoste dietro le apparenze. Hai un alto codice morale che ti spinge a impegnarti in organizzazioni che tutelano l'ambiente e la giustizia sociale. Scopri le ingiustizie e fai pressioni perché vengano presi provvedimenti. La legge e la sua amministrazione sono campi perfetti per te. Vai bene anche in finanza, amministrazione, medicina, psicologia. Ovunque tu vada, metti entusiasmo e hai un profondo senso di responsabilità verso chi si rivolge a te. In amore, hai bisogno di un partner che condivida il tuo stesso entusiasmo e lo stesso impegno nel servire l'umanità. La persona che ami deve avere una missione, uno scopo, da perseguire insieme a te. La religione per te è partecipazione attiva: senti il dovere di stimolare gli altri a riconoscere le loro responsabilità spirituali verso la società. E in questo, raggiungi la massima espressione delle tue capacità.",
                    'consiglio': "🌋 La tua profondità è un vulcano: scava in profondità e porta alla luce tesori nascosti. Usa questa forza per smascherare le ingiustizie, ma anche per costruire qualcosa di nuovo. La tua missione è nobile, ma non dimenticare di vivere anche per te stesso. L'amore non è solo un progetto, ma anche un rifugio."
                }
            },

            'giove_ascendente_sestile': {
                'sestile': {
                    'titolo': "✨⬆️ Giove in sestile con l'Ascendente",
                    'messaggio': "Hai un entusiasmo contagioso e una sicurezza che ti fa sembrare imbattibile. Ami stare in mezzo alla gente, e la tua giovialità e il tuo ottimismo ti rendono popolare. Spingi gli altri a darsi da fare e sei generoso con chi ha bisogno. Sei sempre aggiornato nel tuo lavoro e dai il massimo, e ammiri chi è come te. La tua cultura e la tua comprensione degli altri fanno sì che tutti cerchino i tuoi consigli. Sai parlare bene e con competenza, e questo talento può essere messo a frutto nei media, nell'insegnamento, nelle conferenze. Sul lavoro metti entusiasmo e non ti sottrai alle responsabilità. Non solo parli, ma sai anche ascoltare. Sai che la crescita spirituale passa attraverso la cultura, anche se sai che non si può mai raggiungere la conoscenza assoluta. Non sai dire di no a chi ti chiede aiuto. A volte vuoi fare troppo, e per te il riposo sembra non esistere. Impara a staccare ogni tanto.",
                    'consiglio': "✨ La tua luce è un faro nella nebbia. Illumina la strada agli altri, ma non dimenticare di guardare anche dove metti i piedi. La tua generosità è ammirevole, ma non deve prosciugarti. Il riposo non è una perdita di tempo, è il carburante per la prossima corsa."
                }
            },

            # SATURNO (sestili)
            'saturno_urano_sestile': {
                'sestile': {
                    'titolo': "⏳⚡ Saturno in sestile con Urano",
                    'messaggio': "Hai un profondo rispetto per il sapere e sai come usarlo nella pratica. Conosci le tue potenzialità e sai esattamente come sfruttarle. Cerchi la verità in modo istintivo e non ti fermi finché non l'hai trovata. Sai che l'ignoranza limita la libertà, e per questo sviluppi mente e comprensione. Sei efficiente e disciplinato nel lavoro, e porti a termine i compiti meglio e più velocemente degli altri, perché per te il tempo è prezioso. L'insegnamento è la tua strada migliore, ma vai bene anche in scienza, matematica, ricerca, politica, occulto, astrologia. Qualunque cosa tu scelga, ti elevi sopra la media, perché vuoi il massimo dalle tue capacità. Ma questo può infastidire chi è meno dotato. Cerca di non suscitare antagonismi. Ti trovi bene con persone intelligenti come te, perché provi un certo disprezzo per l'incompetenza.",
                    'consiglio': "⚡ La tua mente è un orologio di precisione. Funziona alla perfezione, ma non aspettarti che tutti abbiano il tuo stesso meccanismo. La tua efficienza è una risorsa, ma non deve diventare arroganza. La pazienza con chi è meno dotato è il segno della vera intelligenza."
                }
            },

            'saturno_nettuno_sestile': {
                'sestile': {
                    'titolo': "⏳🌊 Saturno in sestile con Nettuno",
                    'messaggio': "Hai un'acuta percezione delle cose e sai usare la tua ispirazione in modo costruttivo, per te e per gli altri. Sei particolarmente sensibile ai tuoi obblighi sociali. Anche se non partecipi attivamente a campagne contro le ingiustizie, offri consigli e programmi a chi è in prima linea. Valuti le condizioni ambientali con profondità e sai distinguere il giusto dall'ingiusto. Soffri quando le capacità umane vengono sprecate e lotti per una migliore distribuzione dei servizi sociali. Scoprire le cose è il tuo talento: sai raccogliere fatti con pazienza, senza farti notare, e mantenere segreti. Sei disciplinato e discreto, per questo sei un ottimo consigliere per persone potenti. La passione per il lavoro ti lascia poco tempo per l'affettività, e cerchi nella persona amata le tue stesse doti. Non sacrifichi i tuoi ideali per nessuno. Fai fatica a capire chi resta indifferente al male della società.",
                    'consiglio': "🌊 La tua sensibilità è un radar che capta l'invisibile. Usalo per navigare, non per affondare. Il mondo ha bisogno di chi vede oltre, ma ricordati di guardare anche dentro te stesso."
                }
            },

            'saturno_plutone_sestile': {
                'sestile': {
                    'titolo': "⏳🔥 Saturno in sestile con Plutone",
                    'messaggio': "Sai che ogni cosa deve essere programmata accuratamente per avere successo: nulla va lasciato al caso. Per questo ti organizzi per ottenere il massimo. Conosci bene i tuoi pregi e difetti e non fai il passo più lungo della gamba, ma sei pronto a qualsiasi responsabilità per raggiungere posizioni importanti. Il successo, quando arriva, non è mai inaspettato: ci hai dedicato enormi sforzi e hai gettato solide basi. Sai che l'esperienza pratica è la migliore maestra, ma non sottovaluti cultura e formazione. I risultati sono proporzionali al contributo che dai. I superiori lo notano e le promozioni arrivano. Capisci le motivazioni altrui, ma non sopporti l'incompetenza e la negatività. Pretendi molto dai collaboratori e puoi essere vendicativo con chi cerca di salire senza meriti. Preferisci discutere apertamente per non rovinare i rapporti. La sicurezza è importante, ma sai che il denaro non è tutto nella vita.",
                    'consiglio': "🔥 La tua forza è nelle fondamenta che costruisci. Ricorda che il potere vero non sta nell'accumulare, ma nel costruire qualcosa che resista al tempo. La vendetta è un peso: lascialo cadere."
                }
            },

            'saturno_ascendente_sestile': {
                'sestile': {
                    'titolo': "⏳✨ Saturno in sestile con l'Ascendente",
                    'messaggio': "Hai chiarezza di pensiero e di espressione. Sai che ognuno è responsabile della propria condotta e agisci con disciplina e serietà. La tua integrità è tale che la gente ti rispetta, anche se a volte ti considera presuntuoso. Sei efficiente e programmi tutto metodicamente, per non sbagliare. Ti innervosisce vedere gli altri sprecare tempo in tentativi inutili. Nelle conversazioni sei stringato e pensi prima di parlare: consideri superficiali chi parla senza riflettere. Questo tuo atteggiamento conservatore può farti sembrare distaccato, ma in realtà hai bisogno di silenzio e concentrazione per mettere ordine nelle idee. Una volta che ti sei fatto un'idea, è difficile fartela cambiare senza argomenti validi. Hai vedute più ristrette di altri, ma sei più profondo nel comprendere problemi e motivazioni. Sei adatto a posizioni di guida, sai mettere la persona giusta al posto giusto. Ti preoccupi per la sicurezza in vecchiaia e usi tutto il tuo talento per ottenerla.",
                    'consiglio': "✨ La tua serietà è la tua forza, ma non deve diventare una prigione. La vita non è solo programmazione: lasciati sorprendere. A volte gli errori degli altri insegnano più della tua perfezione."
                }
            },

            # URANO (sestili)
            'urano_nettuno_sestile': {
                'sestile': {
                    'titolo': "⚡🌊 Urano in sestile con Nettuno",
                    'messaggio': "Appartieni a una generazione che ha la coscienza collettiva dell'importanza della verità e non tollera che venga nascosta al popolo. La tua sospettosità è rivolta alle grandi organizzazioni, ai complessi finanziari che hanno agganci nel governo, alle religioni organizzate che tengono i membri sotto controllo. Vuoi decidere da solo in cosa credere e a quale disciplina sottoporti. Il tuo pensiero rivoluzionario non accetta di dover sottostare al pensiero di persone verso cui nutri sospetto. L'istituzione è una minaccia per la tua libertà e per i diritti umani, e non lo nascondi. Sai che chi obbedisce ciecamente mette in pericolo il diritto di ogni uomo di essere artefice del proprio destino. Dalla tua generazione verrà il frutto seminato tra il '65 e il '68: chiederete voce in capitolo su educazione, società e politica, perché la libertà di parola non venga limitata. Il tuo credo è che ogni individuo ha un obbligo morale e spirituale verso la società: la fratellanza. Una società basata sul materialismo è un affronto alla dignità umana. Aspiri all'espressione creativa per tutti, indipendentemente dall'estrazione sociale.",
                    'consiglio': "🌊 La tua visione è quella di un mondo più giusto. È un dono prezioso, ma non trasformarlo in rabbia. La vera rivoluzione non è solo gridare la verità, ma seminarla con pazienza, giorno dopo giorno."
                }
            },

            'urano_plutone_sestile': {
                'sestile': {
                    'titolo': "⚡🔥 Urano in sestile con Plutone",
                    'messaggio': "La vista di tutte le ingiustizie nel mondo ti provoca un profondo sconvolgimento interiore e il bisogno impellente di gridare il tuo dissenso. Non tolleri che le grandi potenze – governi o complessi industriali – ottengano appoggio pubblico per i loro scopi nascosti, forti del loro potere economico. Ti ribelli a chi usa raggiri legali e appoggi politici per fare pressioni sui rappresentanti del governo. Non sopporti lo spreco di fondi pubblici e la disonestà imperante. Vuoi che venga fatta luce sul malcostume politico. Sei nato in un periodo di grande instabilità (1942-1946, durante la guerra mondiale) e sai che esiste il pericolo che la libertà personale venga soffocata da politici che favoriscono leggi per interessi particolari. Fortunatamente hai coraggio e forza in altissimo grado per risvegliare l'opinione pubblica. Sei sempre presente ai dibattiti pubblici quando si discutono progetti di legge importanti. La libertà è la cosa essenziale della tua vita.",
                    'consiglio': "🔥 La tua ribellione è sacra, ma non consumarti nell'indignazione. Scegli le tue battaglie con saggezza: la luce che getti sul malcostume illuminerà la strada, ma solo se la tua fiamma non si spegne nella rabbia."
                }
            },

            'urano_ascendente_sestile': {
                'sestile': {
                    'titolo': "⚡✨ Urano in sestile con l'Ascendente",
                    'messaggio': "Hai una mente ribelle, insofferente verso idee e vecchi concetti convenzionali che non danno più risultati. Rimani affascinato da tutto ciò che è nuovo e originale e la tua mente galoppa quando incontri idee geniali. Nonostante la tua irrequietezza e il bisogno di muoverti continuamente, sai che per trovare sostenitori devi dare impressione di solidità e lealtà. Il tuo punto di forza è la creatività originale e progressista, di cui non fai mistero. Hai una grande capacità di comunicare e far partecipi gli altri delle tue idee. Sei molto intuitivo e spesso segui l'ispirazione del momento, che si rivela solida e attendibile. Spesso ciò che dici è profetico. Ami la tua indipendenza e il lavoro deve lasciarti libertà d'azione. La routine quotidiana ti è insopportabile e frustra la tua creatività. In ogni lavoro porti ingegnosità: se esiste un modo per nuove entrate, lo trovi. Hai molti amici di ogni estrazione, ma prediligi chi è creativo come te. Adori competere e batterti per superare gli altri, ma non assumi arie di superiorità quando vinci: sei quasi grato a chi ti ha spronato. Subisci l'invidia di chi ha mente chiusa e non capisce la tua originalità. Per te è difficile andare in pensione: ogni giorno c'è qualcosa di nuovo che ti assorbe.",
                    'consiglio': "⚡ La tua mente è un fulmine: creativa, veloce, geniale. Ma il fulmine ha bisogno di un parafulmine per non bruciare ciò che tocca. La tua originalità sarà più potente se impari a dosarla, senza spegnerti mai."
                }
            },

            # NETTUNO (sestili)
            'nettuno_ascendente_sestile': {
                'sestile': {
                    'titolo': "🌊✨ Nettuno in sestile con l'Ascendente",
                    'messaggio': "Hai una certa difficoltà a esprimerti e spesso dai un'impressione sbagliata agli altri. Hai un'immaginazione fertile e a volte abbellisci i tuoi discorsi al punto da distorcere il vero significato di ciò che dici, creando confusione. Nel tuo immenso desiderio di attirare l'attenzione, inconsciamente crei situazioni che non esistono o inventi avvenimenti mai accaduti. Questo talento può essere usato creativamente nella scrittura e nel teatro. Sei modesto sulle tue vere capacità, ma gli amici riconoscono le tue doti e ti considerano simpatico e piacevole, anche se ingenuo e indifeso. Vai d'accordo con tutti perché sei docile e comprensivo. Non è facile per te prendere decisioni, perché sembri incapace di esaminare i fatti uno per uno per arrivare a un giudizio sicuro. Quando subisci un fallimento, tendi a commiserarti. Spesso vuoi fare cose che non sono per te: devi capire che puoi avere successo solo se rimani nei limiti delle tue capacità e predisposizioni.",
                    'consiglio': "🌊 La tua immaginazione è un oceano sconfinato. Nuotaci dentro, ma impara a tornare a riva. La creatività è un dono, ma la realtà è l'ancora che ti impedisce di perderti. Ascolta chi ti vuole bene: loro vedono ciò che tu non vedi."
                }
            },

            'nettuno_plutone_sestile': {
                'sestile': {
                    'titolo': "🌊🔥 Nettuno in sestile con Plutone",
                    'messaggio': "Questo aspetto accomuna tutti i nati in un lungo periodo che va dal 1942 e continuerà per circa 100 anni. Rappresenta il processo evolutivo che spinge l'umanità alla ricerca della perfezione. Sotto la sua influenza, l'uomo cerca nuove dimensioni ed esperienze, pur rimanendo ancorato all'ordine materiale. Ti rendi conto che possono esistere altri mondi oltre al tuo, e per questo la conoscenza scientifica si volgerà sempre più a scoprirli. Ma lo stesso vale per l'esplorazione del mondo interiore. Nettuno simboleggia l'interiorità, Plutone lo sforzo verso gli spazi infiniti. Entrambi i mondi sono illimitati e l'uomo sta andando in entrambe le direzioni. Alla fine si giungerà allo stesso traguardo, qualunque sia la direzione presa. Cerchi risposte dal mondo fisico o dalle profondità interiori, ma poiché il mondo fisico è tangibile, è una via sicura. Mentre lotti per la ricerca esistenziale, chiedi aiuto anche all'occulto. Il crescente interesse per percezione extrasensoriale, stati alfa, telepatia indica che l'essere umano sospetta che le risposte siano dentro di sé. Non c'è conflitto tra le due ricerche: sono complementari e si aiutano a vicenda.",
                    'consiglio': "🔥 La tua generazione è ponte tra mondi: visibili e invisibili, scientifici e spirituali. Non smettere mai di cercare, ma ricorda che la vera scoperta non è solo fuori, ma dentro di te. Il viaggio più lungo è quello che parte dal cuore."
                }
            },

            # PLUTONE (sestili)
            'plutone_ascendente_sestile': {
                'sestile': {
                    'titolo': "🔥✨ Plutone in sestile con l'Ascendente",
                    'messaggio': "Hai una profonda comprensione del ruolo che hai nella vita di chi ti sta vicino. Sai di poter influenzare gli altri a fare ciò che vuoi e accetti di buon grado le sfide, specialmente dagli avversari a cui vuoi dimostrare la tua competenza. Sei franco e brusco quando parli e hai il coraggio di dire la verità. Quando hai torto difendi i tuoi punti di vista in modo polemico. Sai sempre quello che vuoi e lavori duramente per raggiungere i tuoi obiettivi. Sei la tipica persona su cui contare nei momenti di crisi, sempre pronto a dare assistenza. Rispetti e ammiri chi ha il coraggio delle proprie azioni e ti esasperi quando vedi persone che non reagiscono alle prepotenze. Sei quasi ossessionato dall'idea di perdere la libertà se non combatti contro chi tenta di privarti dei tuoi diritti. Ritieni che i politici che cercano di farlo siano parassiti da estirpare per il bene pubblico.",
                    'consiglio': "🔥 La tua determinazione è una forza della natura. Usala per costruire, non solo per combattere. Il coraggio di dire la verità è raro, ma altrettanto raro è il coraggio di ascoltarla. E a volte, la battaglia più grande è quella contro il proprio orgoglio."
                }
            },
            
            # ============================================
            # MESSAGGI PER LE QUADRATURE RADIX
            # ============================================

            # SOLE (quadrature)
            'sole_luna_quadratura': {
                'quadratura': {
                    'titolo': "☀️🌙 Sole in quadratura con la Luna",
                    'messaggio': "Sei sempre divisa tra quello che vuoi e quello che senti. Non sei mai contenta di quello che fai, ti sembra sempre che la vita ti abbia dato meno di quanto meriti. Cambi lavoro, cambi idee, ma il problema resta: non ti impegni abbastanza per specializzarti in qualcosa di vero. Vorresti una vita comoda, ma senza la fatica di costruirla. I superiori ti stanno antipatici, il lavoro non ti piace, e intanto il tempo passa. Sei sempre sulla difensiva, pronta a polemizzare con tutti. In famiglia, con gli amici, con il partner: sempre a lottare. Forse è il caso di fermarti un attimo e chiederti: cosa voglio veramente? E quanto sono disposta a investire per ottenerlo? La vita non è una lotteria, è un campo che va seminato.",
                    'consiglio': "🌱 La felicità non cade dal cielo, si costruisce con le proprie mani. E a volte, per costruire, bisogna prima mettere da parte la rabbia e ascoltarsi."
                }
            },

            'sole_marte_quadratura': {
                'quadratura': {
                    'titolo': "☀️🔥 Sole in quadratura con Marte",
                    'messaggio': "Hai un'energia che sembra non finire mai. Sei una forza della natura, ma questa tua potenza a volte ti travolge. Parti in quarta, ti entusiasmi, poi qualcosa va storto e vai in tilt. Ti arrabbi, urli, ti senti tradita dal mondo. Ma forse, nella fretta, non hai programmato bene le cose. Non hai previsto gli ostacoli. L'esperienza ti insegnerà a essere più paziente, a pensare prima di agire. Sei una che ama le sfide, non ti tiri mai indietro. Ma attenta a non confondere la grinta con la testardaggine. In amore sei passionale, ma ti stanchi subito. Vuoi tutto e subito, e quando lo hai, ti passa la voglia. Forse devi imparare a goderti il percorso, non solo la meta. E a scegliere un partner che ti stia dietro, senza farti sentire soffocata.",
                    'consiglio': "⚡ L'energia è una risorsa preziosa, ma senza una direzione diventa solo caos. Impara a respirare, a rallentare, a scegliere le tue battaglie. La vera forza è anche saper aspettare."
                }
            },

            'sole_giove_quadratura': {
                'quadratura': {
                    'titolo': "☀️✨ Sole in quadratura con Giove",
                    'messaggio': "Sei una che non si risparmia. Fai, prometti, ti entusiasmi, ma spesso esageri. Metti troppa carne al fuoco e poi ti ritrovi in panico senza sapere da che parte iniziare. Non programmi, non organizzi, e quando qualcuno prova a darti un consiglio, ti offendi. Sei convinta di farcela da sola, che tu sia superiore. Invece no. La vita è fatta di alti e bassi, e a volte c'è bisogno degli altri. In amore sei esigente, pretendi devozione assoluta, vuoi essere il centro del mondo del tuo partner. Ma l'amore non è un palcoscenico. Hai bisogno di ammirazione, di applausi, e se non arrivano, crolli. Forse è il caso di scendere dal piedistallo e guardare le cose con più umiltà. La vera grandezza non è apparire, è essere.",
                    'consiglio': "🌟 L'entusiasmo è bello, ma senza radici diventa solo fumo. Impara a programmare, a chiedere aiuto, a condividere. La vita è più leggera se non devi portare tutto da sola."
                }
            },

            'sole_urano_quadratura': {
                'quadratura': {
                    'titolo': "☀️⚡ Sole in quadratura con Urano",
                    'messaggio': "Sei una ribelle, una che non sta alle regole. Vuoi fare sempre di testa tua, anche quando sai di avere torto. Sei testarda, orgogliosa, e non sopporti che qualcuno ti dica cosa fare. Ti piace andare controcorrente, anche solo per il gusto di farlo. Ma questo tuo modo di fare ti isola. La gente si stanca, si allontana. E tu resti sola con le tue idee geniali. In amore cerchi qualcuno che ti accetti così, che si pieghi alla tua volontà. Ma quando lo trovi, perdi interesse. Perché in realtà non vuoi essere amata, vuoi essere dominante. Forse è il momento di abbassare le difese e scoprire che la vera libertà non è fare quello che si vuole, ma scegliere con chi stare.",
                    'consiglio': "⚡ La ribellione stanca, prima o poi. Prova a fidarti, a lasciarti andare, a non voler avere sempre ragione. La vera forza è anche saper cedere, a volte."
                }
            },

            'sole_nettuno_quadratura': {
                'quadratura': {
                    'titolo': "☀️🌊 Sole in quadratura con Nettuno",
                    'messaggio': "Sei una sognatrice, una sensibile. Da piccola ti hanno spenta, ti hanno detto che non era il caso di sognare troppo, che la vita è dura. E tu ti sei chiusa in un mondo tuo, fatto di fantasie e paure. Oggi fatichi a credere in te stessa, a fidarti delle tue capacità. Vivi nel timore di sbagliare, di ferire, di essere giudicata. In amore, questo è un problema serio: attiri persone che vogliono approfittarsi di te, che ti usano e ti lasciano. E tu ci stai, perché non sai dire di no. Forse dovresti iniziare a credere un po' di più in te stessa. A mettere dei paletti. A scegliere con cura chi far entrare nella tua vita. La tua sensibilità è un dono, non una condanna. Impara a usarla con intelligenza.",
                    'consiglio': "🌊 I sogni sono bellissimi, ma è nella realtà che si vive. Impara a distinguere chi merita la tua fiducia e chi no. La tua dolcezza è preziosa, non sprecarla con chi non la capisce."
                }
            },

            'sole_plutone_quadratura': {
                'quadratura': {
                    'titolo': "☀️🌋 Sole in quadratura con Plutone",
                    'messaggio': "Sei una forza della natura, ma questa forza a volte ti distrugge. Hai una volontà di ferro, non molli mai. Ma il tuo motto sembra essere 'la miglior difesa è l'offesa'. Vedi nemici dappertutto, e combatti anche quando non ce n'è bisogno. La gente ha paura di te, si tiene a distanza. E tu resti sola, con la tua corazza. In amore sei intensa, passionale, ma anche possessiva, gelosa. Vuoi dominare, controllare. E quando l'altro si ribella, è guerra. Forse è il momento di abbassare le armi e scoprire che la vera forza non è combattere, ma fidarsi. Che la vita non è una guerra, ma un viaggio da condividere.",
                    'consiglio': "🌋 La tua forza è immensa, ma se la usi contro gli altri diventa autodistruttiva. Impara a deporre le armi, a fidarti, a lasciare spazio. La pace interiore è la più grande delle vittorie."
                }
            },

            'sole_ascendente_quadratura': {
                'quadratura': {
                    'titolo': "☀️⬆️ Sole in quadratura con l'Ascendente",
                    'messaggio': "Il tuo comportamento a volte irrita, e tu non te ne accorgi. Pensi di essere sincera, onesta, ma gli altri ti percepiscono come aggressiva, prevaricatrice. Non ti adatti, non scendi a compromessi. Vuoi avere sempre ragione, e questo ti rende difficile da sopportare. Desideri essere apprezzata, ma non fai nulla per esserlo. Anzi, fai il contrario. Forse è colpa di un passato difficile, di una carriera costruita a fatica, di superiori che non ti hanno mai dato credito. Ora sei diventata diffidente, dura. Ma la vita non è una guerra. Puoi essere forte senza essere dura. Puoi farti valere senza calpestare gli altri. Prova a essere più morbida, più aperta. Scoprirai che la gente ti apprezzerà di più, e anche tu starai meglio.",
                    'consiglio': "🌟 La forza non sta nell'avere sempre ragione, ma nel saper ascoltare, nel saper chiedere scusa, nel sapersi mettere in discussione. La vera sicurezza è anche umiltà."
                }
            },

            # LUNA (quadrature)
            'luna_mercurio_quadratura': {
                'quadratura': {
                    'titolo': "🌙💬 Luna in quadratura con Mercurio",
                    'messaggio': "Sei una che si fa prendere dalle emozioni. Prima reagisci, poi pensi. E spesso le tue reazioni sono esagerate, fuori luogo. La gente si offende, si allontana, e tu non capisci perché. Ti preoccupi per cose da niente, sprechi energie in pensieri inutili. Sei sempre al centro dei tuoi pensieri, un po' egocentrica. Forse dovresti imparare a guardare anche gli altri, a capire che anche loro hanno problemi, paure, difficoltà. Quando ti senti insicura, diventi dura, critica. Pretendi che gli altri si adattino a te, ma tu non fai nulla per andare incontro a loro. In amore, le incomprensioni sono all'ordine del giorno. Parli senza pensare, dici cose che non pensi, e poi ci stai male. Impara a fare una pausa tra quello che senti e quello che dici. Ascoltare è più importante che parlare.",
                    'consiglio': "🧠 Il cuore e la testa non sono nemici, devono collaborare. Impara a respirare prima di parlare, a contare fino a dieci prima di reagire. La calma è la tua migliore alleata."
                }
            },

            'luna_venere_quadratura': {
                'quadratura': {
                    'titolo': "🌙❤️ Luna in quadratura con Venere",
                    'messaggio': "Sei una romantica, una sentimentale. Ma hai paura di mostrarlo. Hai paura di essere ferita, di essere usata. Forse è colpa della tua famiglia, di genitori troppo possessivi che ti hanno insegnato che amare significa soffrire. Oggi fatichi a fidarti, a lasciarti andare. In amore, attiri persone sbagliate, che si appoggiano a te, che ti usano come spalla su cui piangere. Tu ci stai, perché ti fa sentire importante. Ma alla fine resti con un pugno di mosche. Forse è il momento di fare spazio, di andare via di casa, di costruirti una vita tua. Di frequentare persone sane, che non hanno bisogno di essere salvate. L'amore vero è fatto di due persone intere, non di una che salva e una che affonda.",
                    'consiglio': "💖 Non devi salvare nessuno per essere amata. La persona giusta ti starà accanto senza bisogno che tu ti sacrifichi. Impara a volerti bene, a metterti al primo posto. L'amore vero non chiede di essere comprato."
                }
            },

            'luna_marte_quadratura': {
                'quadratura': {
                    'titolo': "🌙🔥 Luna in quadratura con Marte",
                    'messaggio': "Sei una che reagisce di pancia, e quando lo fai, non vedi più in là del tuo naso. Ti arrabbi, gridi, e dopo ti senti in colpa. Ma intanto i rapporti si incrinano, le persone si allontanano. Sul lavoro litighi con i colleghi, a casa con il partner. Sei sempre tesa, sempre sul chi vive. E la salute ne risente: mal di stomaco, intestino irritato. Forse dovresti chiederti perché sei sempre così arrabbiata. Forse hai paura di non essere all'altezza, e allora attacchi per prima. La cultura, la formazione professionale potrebbero aiutarti a sentirti più sicura. Impara a lasciare i problemi in ufficio, a non portarti a casa il rancore. E impara a respirare, a rilassarti. La vita è più bella se non sei sempre pronta a combattere.",
                    'consiglio': "🔥 La rabbia è come un fuoco: se la alimenti, brucia tutto. Se la lasci spegnere, lascia spazio alla pace. Impara a distinguere le battaglie che valgono la pena da quelle che sono solo rumore."
                }
            },

            'luna_giove_quadratura': {
                'quadratura': {
                    'titolo': "🌙✨ Luna in quadratura con Giove",
                    'messaggio': "Sei una che si butta, che si entusiasma, ma anche una che sbaglia i conti. Prendi decisioni affrettate, e poi devi tornare indietro. Non hai stabilità emotiva, sei sempre in bilico tra l'esaltazione e l'apatia. Sei troppo buona, troppo generosa, e la gente ne approfitta. Poi, quando ti lasciano sola, ti lamenti. Ma forse la colpa è anche tua, che non sai dire di no. Hai bisogno di disciplina, di programmi, di regole. Potresti fare grandi cose in medicina, legge, insegnamento. Ma devi smetterla di scappare dalle responsabilità. In amore, sei prodiga di attenzioni, ma forse troppo. Impara a moderarti, a non dare tutto subito. La salute risente degli eccessi: attenta a cosa mangi e a come vivi.",
                    'consiglio': "✨ La generosità è bella, ma deve avere un limite. Impara a proteggerti, a non dare tutto a tutti. La tua energia è preziosa, non sprecarla in mille rivoli. Scegli con cura chi merita il tuo tempo."
                }
            },

            'luna_saturno_quadratura': {
                'quadratura': {
                    'titolo': "🌙⏳ Luna in quadratura con Saturno",
                    'messaggio': "Sei una persona legata al passato, alla famiglia, alle tradizioni. Fatichi a staccarti, a fare spazio a cose nuove. Ti senti in colpa se non sei fedele a chi conosci da sempre. Questa tua fedeltà è ammirevole, ma a volte ti imprigiona. Non riesci a essere indipendente, a vivere la tua vita. Forse dovresti cercare un lavoro che ti permetta di aiutare gli altri, come l'assistenza agli anziani o ai bambini. Lì potresti dare il meglio di te. In amore, rischi di accontentarti di poco, pur di non stare sola. Ma la solitudine non si cura con la compagnia sbagliata. Impara a starti bene, a coltivare i tuoi interessi. La persona giusta arriverà quando tu sarai pronta a incontrarla senza paura.",
                    'consiglio': "⏳ Il passato è una radice, non una catena. Onora chi ti ha cresciuto, ma vivi la tua vita. La felicità non è un tradimento, è un diritto. Conceditelo."
                }
            },

            'luna_urano_quadratura': {
                'quadratura': {
                    'titolo': "🌙⚡ Luna in quadratura con Urano",
                    'messaggio': "Sei una che scatta per un nonnulla. Impulsiva, emotiva, imprevedibile. Ti arrabbi, ti offendi, e poi passa. Ma intanto hai fatto danni. Non sopporti che qualcuno ti contraddica, vuoi sempre avere ragione. In amore, questo tuo modo di fare è devastante. Pretendi che il partner si adatti a te, ma tu non sei disposta a cambiare di una virgola. E così le storie durano poco. Sei intelligente, creativa, potresti fare grandi cose nell'insegnamento, nella scrittura, nella politica. Ma devi imparare a controllare i tuoi scatti, a essere più tollerante. La libertà che rivendichi per te, concedila anche agli altri. Altrimenti resterai sempre sola.",
                    'consiglio': "⚡ L'impulsività è una fiamma che brucia in fretta. Impara a spegnerla prima che faccia male. La vera libertà è anche saper aspettare, saper ascoltare, saper cedere."
                }
            },

            'luna_nettuno_quadratura': {
                'quadratura': {
                    'titolo': "🌙🌊 Luna in quadratura con Nettuno",
                    'messaggio': "Vivi in un mondo tutto tuo, fatto di sogni e fantasie. La realtà ti spaventa, allora la aggiusti, la colori, la rendi più sopportabile. Ma così facendo, perdi di vista ciò che è vero. Le persone ti ingannano, e tu ci caschi sempre. Sei troppo sensibile, troppo fiduciosa. In amore, non chiarisci i malintesi, lasci che le cose si trascinano, e poi soffri. Hai bisogno di un lavoro che ti metta in contatto con la gente, ma senza troppe responsabilità. Chiedi aiuto a persone fidate per le scelte importanti. E impara a essere più realistica. La vita non è un sogno, è una cosa seria. Ma può essere bella lo stesso, se la vivi con i piedi per terra.",
                    'consiglio': "🌊 I sogni sono ali, ma per volare serve anche un corpo. Impara a stare nella realtà senza paura. La verità, anche se dura, è l'unica base su cui costruire qualcosa di solido."
                }
            },

            'luna_plutone_quadratura': {
                'quadratura': {
                    'titolo': "🌙🌋 Luna in quadratura con Plutone",
                    'messaggio': "Il passato ti tiene prigioniera. Forse hai avuto genitori severi, autoritari, che ti hanno fatto sentire sbagliata. Oggi porti ancora quel peso. Sei diffidente, chiusa, e fatichi a lasciarti andare. In amore sei estremista: o tutto o niente. Pretendi che l'altro si adatti a te, ma tu non sei disposta a cambiare. Così le storie durano poco, e resti sola. Hai bisogno di lavorare a contatto con la gente, per imparare a capire gli altri e te stessa. Terapie, assistenza, sociologia: sono campi in cui potresti dare il meglio. E impara a concedere spazio alla persona che ami. La tenerezza non è debolezza, è forza.",
                    'consiglio': "🌋 Il passato non può essere cambiato, ma può essere guarito. Non sei più quella bambina spaventata. Oggi puoi scegliere. Scegli di fidarti, di amare, di vivere."
                }
            },

            'luna_ascendente_quadratura': {
                'quadratura': {
                    'titolo': "🌙⬆️ Luna in quadratura con l'Ascendente",
                    'messaggio': "Sei una persona emotiva, sensibile, ma fai fatica a mostrarlo. Ti nascondi dietro un'apparenza dura, che allontana gli altri. Ti fai dominare da persone forti, e poi soffri. Hai paura della realtà, e questa paura ti blocca. Sei legata alla famiglia, alla casa, e fatichi a uscire dal guscio. Dovresti liberarti dal passato, acquisire più fiducia in te stessa. Studiare, formarti, per sentirti all'altezza. E attenta a chi ti associ: spesso collabori con incompetenti che poi ti lasciano nei guai. Impara a scegliere bene le tue battaglie e le tue compagnie.",
                    'consiglio': "🌸 La timidezza non è un difetto, ma non deve diventare una prigione. Fai un passo alla volta, ma fallo. Il mondo fuori è meno spaventoso di quanto immagini."
                }
            },

            # MERCURIO (quadrature)
            'mercurio_marte_quadratura': {
                'quadratura': {
                    'titolo': "💬🔥 Mercurio in quadratura con Marte",
                    'messaggio': "Sei una che non la manda a dire. Hai le idee chiare, e le esprimi senza peli sulla lingua. Il problema è che spesso non ti fermi ad ascoltare gli altri. Discuti, ti arrabbi, e alla fine la gente si stanca e ti evita. Hai una mente brillante, piena di idee, ma le sprechi in polemiche inutili. In amore, pretendi che il partner la pensi come te, e quando non è così, diventi aspra, vendicativa. Forse dovresti imparare a tacere, a volte. Ad ammettere di avere torto. A usare la diplomazia. La tua intelligenza è un dono, ma senza umiltà diventa un'arma che ferisce prima te stessa.",
                    'consiglio': "🗣️ La parola è una lama: usala con cura. Impara ad ascoltare, a dubitare, a chiedere scusa. La vera intelligenza non è avere sempre ragione, ma saper costruire ponti."
                }
            },

            'mercurio_giove_quadratura': {
                'quadratura': {
                    'titolo': "💬✨ Mercurio in quadratura con Giove",
                    'messaggio': "Sei una che sa tante cose, o almeno così credi. Ti entusiasmi, inizi studi, progetti, e poi ti stanchi e lasci perdere. Dai giudizi affrettati, superficiali, e la gente ti prende per una che parla a vanvera. Cerchi la strada facile, non ami le responsabilità. In amore, sei esigente, ma non sempre coerente. Pretendi che il partner si pieghi ai tuoi desideri, ma tu non sei disposta a fare altrettanto. Hai bisogno di disciplina, di costanza, di finire ciò che inizi. La cultura è importante, ma se non la metti in pratica, non serve a nulla.",
                    'consiglio': "📚 La conoscenza è un albero che va annaffiato ogni giorno. Non basta piantare il seme, bisogna curarlo. Scegli una cosa, una sola, e portala a termine. I risultati arriveranno."
                }
            },

            'mercurio_saturno_quadratura': {
                'quadratura': {
                    'titolo': "💬⏳ Mercurio in quadratura con Saturno",
                    'messaggio': "Sei una tradizionalista, una che non ama i cambiamenti. Sei attaccata al passato, alle idee vecchie, e fatichi ad accettare il nuovo. Questa tua rigidità ti blocca. Hai paura di sbagliare, di non farcela, e così non provi nemmeno. Sei intelligente, capace, ma la mancanza di fiducia in te stessa ti paralizza. In amore, sei vendicativa se qualcuno ti tradisce. Fai fatica a perdonare. Forse dovresti imparare a vedere il lato positivo della vita, a non fossilizzarti sugli errori. A volte, la colpa è tua se non ottieni ciò che desideri. Apri la mente, accetta le sfide. La vita è movimento.",
                    'consiglio': "⏳ Il passato è una lezione, non una prigione. Impara dagli errori, ma non fermarti. Il futuro è un foglio bianco, puoi scriverlo come vuoi. Basta che tu lo voglia davvero."
                }
            },

            'mercurio_urano_quadratura': {
                'quadratura': {
                    'titolo': "💬⚡ Mercurio in quadratura con Urano",
                    'messaggio': "Hai una mente brillante, originale, piena di idee geniali. Il problema è che sei anche un po' eccentrica, e le tue idee spesso sono troppo avanti per essere capite. Ti ribelli alle regole, non accetti compromessi. E quando parli, sembri sempre sicura di te, anche quando non lo sei. La gente si sente a disagio, non sa come prenderti. In amore, sei affascinante, ma difficile. Non ti comprometti, non ti leghi. E quando l'altro cerca di avvicinarsi, scappi. Hai bisogno di qualcuno di stabile, che ti faccia da ancora. Ma devi anche tu imparare a cedere, a volte. La vera libertà non è scappare, è scegliere di restare.",
                    'consiglio': "⚡ La tua originalità è un dono, ma non deve diventare un muro. Impara ad ascoltare, a mediare, a trovare un punto d'incontro. La persona giusta non ti imprigionerà, ti darà ali per volare insieme."
                }
            },

            'mercurio_nettuno_quadratura': {
                'quadratura': {
                    'titolo': "💬🌊 Mercurio in quadratura con Nettuno",
                    'messaggio': "Sei una sognatrice, una visionaria. La tua immaginazione è sterminata, ma a volte ti gioca brutti scherzi. Non riesci a distinguere la realtà dalla fantasia, e questo ti porta a fare scelte sbagliate. Hai paura delle responsabilità, e per evitarle ti rifugi in un mondo tutto tuo. In amore, sei vulnerabile, ingenua. Attrai persone che si approfittano di te, e poi soffri. Hai bisogno di un lavoro creativo, dove la tua fantasia possa esprimersi senza danni. Arte, scrittura, musica. E impara a fidarti di te stessa, a essere onesta con te. La verità, anche se dura, è meglio di una bella bugia.",
                    'consiglio': "🌊 I sogni sono meravigliosi, ma è nella realtà che si vive. Impara a distinguere le illusioni dalla verità, senza perdere la tua magia. Le persone vanno amate per quello che sono, non per quello che immagini."
                }
            },

            'mercurio_plutone_quadratura': {
                'quadratura': {
                    'titolo': "💬🌋 Mercurio in quadratura con Plutone",
                    'messaggio': "Sei una che va a fondo delle cose. Non ti accontenti delle apparenze, vuoi capire, scavare. Questa tua profondità è una grande risorsa, ma anche un problema. A volte ti perdi nei dettagli, diventi ossessiva. E il tuo modo di parlare, diretto, penetrante, mette a disagio la gente. Sembri sempre sul punto di giudicare. In amore, sei passionale, ma anche possessiva. Vuoi sapere tutto dell'altro, controllarlo. E questo soffoca. Hai bisogno di imparare a lasciar andare, a fidarti, a non voler sempre avere l'ultima parola. La tua intelligenza è uno strumento potente, usala per costruire, non per distruggere.",
                    'consiglio': "🌋 La verità è importante, ma non tutte le verità vanno dette. E non tutto va scoperto. Impara a rispettare i misteri, tuoi e altrui. La fiducia si costruisce, non si impone."
                }
            },

            'mercurio_ascendente_quadratura': {
                'quadratura': {
                    'titolo': "💬⬆️ Mercurio in quadratura con l'Ascendente",
                    'messaggio': "Sei una che cerca di piacere a tutti. Fai favori, sorridi, dici sempre quello che gli altri vogliono sentire. Ma dentro di te sai che non sei sincera. E gli altri lo percepiscono. Non ti prendono sul serio, perché sembri sempre alla ricerca di approvazione. In realtà hai paura di non essere accettata, e allora ti nascondi dietro una maschera di simpatia. In amore, fai lo stesso: ti annulli pur di compiacere. Ma così perdi te stessa. Devi imparare a essere autentica, a mostrare le tue fragilità. Solo così attirerai persone vere, che ti ameranno per quello che sei, non per quello che fingi di essere.",
                    'consiglio': "💬 La maschera stanca, prima o poi. Il trucco cola, e sotto rimani tu. Mostrati così, senza paura. Chi ti amerà, amerà quella. Chi non lo farà, non era per te."
                }
            },

            # VENERE (quadrature)
            'venere_marte_quadratura': {
                'quadratura': {
                    'titolo': "❤️🔥 Venere in quadratura con Marte",
                    'messaggio': "Sei una donna passionale, magnetica. Ma questa tua intensità spesso crea problemi. In amore, vuoi tutto e subito, e quando non ottieni ciò che desideri, ti arrabbi. Non sei disposta a scendere a compromessi, pretendi che sia l'altro a cedere. E così le relazioni diventano un campo di battaglia. In realtà, dentro di te c'è una grande insicurezza. Hai paura di non essere abbastanza, e allora usi il fascino per dominare. Ma l'amore non è dominio, è condivisione. Forse dovresti imparare a essere più morbida, ad ascoltare di più, a non voler sempre avere ragione. L'arte, la musica, la letteratura possono aiutarti a trovare un equilibrio.",
                    'consiglio': "🔥 La passione è un fuoco che scalda, ma se divampa brucia. Impara a dosare la tua energia, a dare spazio, a respirare insieme. L'amore non è una conquista, è un incontro."
                }
            },

            'venere_giove_quadratura': {
                'quadratura': {
                    'titolo': "❤️✨ Venere in quadratura con Giove",
                    'messaggio': "Sei una che ama essere amata, che cerca approvazione in ogni cosa. Sei generosa, ma a volte troppo, e con secondi fini. Quando le cose vanno come vuoi tu, sei la persona più dolce del mondo. Ma guai a contrariarti: ti senti incompresa, vittima. In amore, attiri, piaci, ma fatichi a mantenere una relazione stabile. Forse perché non sei disposta a investire davvero. La generosità non è fare favori sperando di ricevere qualcosa in cambio. È dare senza aspettarsi nulla. Impara a fidarti di più, a non pensare sempre che gli altri vogliano fregarti. La vita è più bella se ti apri, senza calcoli.",
                    'consiglio': "✨ La generosità è un fiore che va annaffiato, non una moneta da scambiare. Impara a dare senza aspettarti nulla. Scoprirai che riceverai molto di più."
                }
            },

            'venere_saturno_quadratura': {
                'quadratura': {
                    'titolo': "❤️⏳ Venere in quadratura con Saturno",
                    'messaggio': "Hai paura di amare, paura di impegnarti. Forse da piccola hai subito un rifiuto, una delusione, e ora ti porti dietro quella cicatrice. Sei diffidente, chiusa, e fatichi a lasciarti andare. In amore, ti aspetti sempre il peggio. E così, puntualmente, il peggio arriva. Perché le tue paure allontanano le persone. Hai bisogno di imparare a fidarti, a essere più ottimista. La vita è troppo breve per passarla a difendersi. Lavora su te stessa, sulla tua autostima. Scoprirai che il mondo non è così ostile. E che l'amore, quando arriva, può essere una meravigliosa sorpresa.",
                    'consiglio': "⏳ Le ferite del passato non sono colpe, sono cicatrici. Non definiscono chi sei, ma chi sei stata. Impara a guardare avanti, con fiducia. La felicità è possibile, se la permetti."
                }
            },

            'venere_urano_quadratura': {
                'quadratura': {
                    'titolo': "❤️⚡ Venere in quadratura con Urano",
                    'messaggio': "Sei una che si innamora delle persone sbagliate. Quelle fuori dal comune, quelle impossibili. Ti attira ciò che è diverso, eccitante, proibito. Ma quando la storia diventa seria, scappi. Hai paura delle responsabilità, di perdere la tua libertà. In amore, confondi l'amicizia con l'amore, e viceversa. Così, le tue relazioni sono sempre un po' confuse, mai definite. Hai bisogno di chiarezza, dentro e fuori. Di capire cosa vuoi veramente. E di imparare che la vera libertà non è scappare, ma scegliere di restare. Con qualcuno che ti ami per quello che sei, senza catene.",
                    'consiglio': "⚡ L'amore non è una gabbia, è un volo in due. Impara a fidarti, a lasciarti andare, a non scappare. La persona giusta non ti imprigionerà, ti darà ali per volare insieme."
                }
            },

            'venere_nettuno_quadratura': {
                'quadratura': {
                    'titolo': "❤️🌊 Venere in quadratura con Nettuno",
                    'messaggio': "Vedi le cose come vorresti che fossero, non come sono. In amore, questo è un disastro. Ti innamori di uomini che non esistono, che costruisci con la fantasia. E quando la realtà si mostra, crolli. Sei troppo sensibile, troppo ingenua. La gente ne approfitta, e tu ci rimani male. Hai bisogno di un lavoro creativo, dove la tua fantasia possa esprimersi senza danni. Arte, musica, scrittura. E impara a essere più realistica, in amore e nella vita. Le persone non sono come le dipingi tu. Sono imperfette, e va bene così. L'amore vero è accettare l'imperfezione.",
                    'consiglio': "🌊 L'ideale è una stella che illumina, ma non scalda. L'amore vero è il fuoco che arde nel camino di casa. Impara a scendere dalle nuvole e a guardare le persone negli occhi. Saranno imperfette, ma saranno vere."
                }
            },

            'venere_plutone_quadratura': {
                'quadratura': {
                    'titolo': "❤️🌋 Venere in quadratura con Plutone",
                    'messaggio': "Sei una che ama in modo totale, totalizzante. Quando ti innamori, ti butti anima e corpo. Ma questo tuo amore è anche possessivo, geloso. Vuoi dominare, controllare. E quando l'altro non si piega, scatta la rabbia. Le tue storie sono spesso tormentate, piene di alti e bassi. In amore, non conosci mezze misure. O tutto o niente. Ma l'amore non è una guerra, è una danza. Devi imparare a lasciare spazio, a fidarti, a non voler possedere. La tua intensità è un dono, ma se la usi male, diventa una maledizione. Impara a dosarla, a condividerla, a trasformarla in tenerezza.",
                    'consiglio': "🌋 L'amore non è possesso, è condivisione. Più stringi, più perdi. Impara a lasciare spazio, a respirare insieme. La vera intimità non è fusione, è danza a due."
                }
            },

            'venere_ascendente_quadratura': {
                'quadratura': {
                    'titolo': "❤️⬆️ Venere in quadratura con l'Ascendente",
                    'messaggio': "Sei una legata alla famiglia, al passato, alle origini. Questo ti dà sicurezza, ma anche tanta nostalgia. Ti sembra di tradire il passato se cerchi la tua indipendenza. Così rimani in situazioni comode, ma che non ti fanno crescere. Hai idee creative, ma non le realizzi. Preferisci startene nell'ombra, a sognare. In amore, rischi di accontentarti di poco, pur di non lasciare il nido. Ma la vita è fuori. È ora di spiccare il volo. Di costruire qualcosa di tuo. Le persone di successo ti affascinano, ma invece di ammirarle da lontano, impara da loro. Mettiti in gioco, rischia. La sicurezza non è stare fermi, è camminare.",
                    'consiglio': "🏡 Il nido è caldo, ma le ali sono fatte per volare. Non aver paura di lasciare ciò che conosci per scoprire ciò che sei. La vita è un'avventura, non un rifugio."
                }
            },

            # MARTE (quadrature)
            'marte_saturno_quadratura': {
                'quadratura': {
                    'titolo': "🔥⏳ Marte in quadratura con Saturno",
                    'messaggio': "Sei una che oscilla tra momenti di grande energia e momenti di totale apatia. Non trovi mai un equilibrio. Quando hai voglia di fare, pensi di non avere tempo. Quando sei ferma, ti rimproveri di non aver approfittato delle occasioni. Questa continua lotta interiore ti logora. In realtà, hai paura di non farcela. E allora eviti, rimandi, ti nascondi. Ma hai delle potenzialità enormi. Se solo imparassi a crederci un po' di più. Sul lavoro, potresti fare carriera in ambiti che richiedono costanza: militare, sport, fisioterapia. In amore, sei passionale ma anche vendicativa. Se ti senti ferita, puoi fare male senza rendertene conto. Impara a perdonare, a lasciar andare. La vita è troppo breve per portare rancore.",
                    'consiglio': "⏳ La costanza è la virtù dei forti. Non serve a nulla partire in quarta se poi ti fermi al primo ostacolo. Impara a camminare al tuo ritmo, senza confrontarti con gli altri. Ogni passo, anche piccolo, è un progresso."
                }
            },

            'marte_giove_quadratura': {
                'quadratura': {
                    'titolo': "🔥✨ Marte in quadratura con Giove",
                    'messaggio': "Sei una piena di energia, di risorse fisiche e mentali. Ma questa tua ricchezza la disperdi in mille rivoli. Inizi tante cose, ma non ne porti a termine nessuna. Vorresti essere come le persone di successo, ma non hai la costanza per fare il lavoro duro che serve. Appena i risultati tardano, ti annoi e cambi strada. Sei impaziente, impulsiva. In famiglia e sul lavoro, hai spesso conflitti perché non accetti le critiche. Ti senti minacciata, trattata male. In realtà, forse sei tu che reagisci in modo sproporzionato. Impara a definire obiettivi chiari, a programmare, a essere costante. La tua energia è un tesoro, non sprecarla.",
                    'consiglio': "✨ La tua energia è un laser, ma se non lo punti su un bersaglio, si disperde. Scegli una direzione, una sola, e perseguila con pazienza. I risultati arriveranno, se non molli."
                }
            },

            'marte_urano_quadratura': {
                'quadratura': {
                    'titolo': "🔥⚡ Marte in quadratura con Urano",
                    'messaggio': "Sei una che ha una gran voglia di libertà, di esplorare, di essere te stessa senza limiti. Ma hai anche paura di rischiare, di perdere qualcosa. Così sei sempre in bilico tra slancio e prudenza. Rimandi, procrastini, e questo ti frustra. Quando finalmente agisci, lo fai con decisione, e i tuoi progetti sono solidi. Ma l'attesa ti logora. In amore, hai forti desideri, ma hai paura delle responsabilità. Forse ti sposerai tardi, o forse no. Dipende da quanto riuscirai a superare le tue paure. Attenta agli incidenti, alla fretta. Moderazione è la parola d'ordine. E non pretendere dagli altri la stessa energia che hai tu.",
                    'consiglio': "⚡ La libertà non è assenza di legami, è scelta consapevole. Impara a bilanciare il desiderio di avventura con la saggezza dell'attesa. La fretta è nemica della perfezione."
                }
            },

            'marte_nettuno_quadratura': {
                'quadratura': {
                    'titolo': "🔥🌊 Marte in quadratura con Nettuno",
                    'messaggio': "Sei una donna complessa, con un mondo interiore ricco e tormentato. Da una parte vorresti agire, buttarti, vivere. Dall'altra, ti blocchi, cadi nell'apatia. Non capisci bene cosa vuoi, cosa senti. La tua vita sessuale è fonte di ansia, di sensi di colpa. Forse per l'educazione ricevuta, forse per esperienze passate. Attrai persone sbagliate, già impegnate, e poi soffri. In amore, è un disastro. Hai bisogno di un lavoro che ti permetta di essere indipendente, di non dipendere dagli altri. La medicina, l'assistenza, possono essere una buona strada. Ma devi imparare a programmare, a tenere tutto sotto controllo. E a non dare la colpa agli altri quando le cose vanno male. La tua salute è delicata, attenta a infezioni e incidenti.",
                    'consiglio': "🌊 La tua anima è un oceano in tempesta. Impara a calmare le onde prima di navigare. La serenità viene da dentro, non dagli altri. Cerca la chiarezza, la semplicità, la pace. E proteggi il tuo corpo, è il tuo tempio."
                }
            },

            'marte_plutone_quadratura': {
                'quadratura': {
                    'titolo': "🔥🌋 Marte in quadratura con Plutone",
                    'messaggio': "Sei una donna di una forza incredibile, ma questa forza a volte ti distrugge. Hai desideri potenti, incontenibili. Ma soddisfarli è sempre difficile. Spesso devi lottare, soffrire, per ottenere ciò che vuoi. In amore, questo si traduce in relazioni tormentate, passioni violente, abbandoni dolorosi. La tua vita è un campo di battaglia. Forse dovresti smettere di combattere e iniziare a scegliere. Le tue energie sono enormi, ma se le disperdi in conflitti inutili, non arrivi da nessuna parte. Impara a incanalare la tua forza in progetti costruttivi, in un lavoro che ti appassiona. La moderazione è la chiave. E impara a perdonare, a lasciar andare. La vendetta è un peso che porti tu, non chi l'ha meritata.",
                    'consiglio': "🌋 La tua forza è un vulcano, ma anche il vulcano ha bisogno di quiete. Impara a dosare la tua energia, a scegliere le tue battaglie. La vera potenza non è distruggere, è costruire. E la vera pace è perdonare."
                }
            },

            # GIOVE (quadrature)
            'giove_urano_quadratura': {
                'quadratura': {
                    'titolo': "✨⚡ Giove in quadratura con Urano",
                    'messaggio': "Sei una donna piena di idee, di progetti, di entusiasmo. Ma spesso fai troppe cose contemporaneamente, e non ne porti a termine nessuna. Sei abile, creativa, ma pretendi troppo da te stessa. Devi imparare a dare priorità, a fare una cosa alla volta. In politica, nell'insegnamento, nella legge, potresti fare grandi cose. Ma se sei guidata solo dal bisogno di applausi, la gente se ne accorge e ti volta le spalle. Devi essere disposta a condividere i successi, non solo a prenderli. In amore, credi di essere irresistibile, ma spesso ti illudi. Impara a moderare gli entusiasmi, ad accettare i fallimenti. La felicità non è un caso, è una costruzione.",
                    'consiglio': "⚡ L'entusiasmo è un motore potente, ma senza un volante, finisci fuori strada. Impara a programmare, a scegliere, a condividere. Il successo vero è quello che si costruisce insieme, non da sole."
                }
            },

            'giove_nettuno_quadratura': {
                'quadratura': {
                    'titolo': "✨🌊 Giove in quadratura con Nettuno",
                    'messaggio': "Hai un grande potenziale creativo, ma fai fatica a realizzarlo. Sei troppo indulgente con te stessa, troppo incline ai sogni e poco alla realtà. Rifiuti le responsabilità, preferisci perdere tempo in cose futili. Sei credulona, ingenua, e la gente ne approfitta. In amore, idealizzi il partner, e quando scopri che è umano, crolli. Hai bisogno di disciplina, di realismo. Di imparare a dire no, a proteggerti. In ambito lavorativo, evita rischi inutili, attieniti alle regole. E non parlare di religione o occulto con chiunque: potresti uscirne male. La tua sensibilità è un dono, ma va protetta.",
                    'consiglio': "🌊 La tua anima è un giardino incantato, ma anche i giardini hanno bisogno di recinzioni. Impara a proteggerti, a non credere a tutti, a vedere le persone per quello che sono. La realtà è meno affascinante dei sogni, ma è l'unico posto dove si vive."
                }
            },

            'giove_plutone_quadratura': {
                'quadratura': {
                    'titolo': "✨🌋 Giove in quadratura con Plutone",
                    'messaggio': "Sei una ribelle, una che non accetta le regole. Cerchi scorciatoie, sistemi facili per ottenere ciò che vuoi. Il tuo motto è 'massimo risultato, minimo sforzo'. Questo ti porta spesso a frequentare ambienti poco raccomandabili, a fare scelte rischiose. In amore, sei attratta da persone incontrate sul lavoro, in affari. Vai dagli estremi: o molto volgare, o estremamente raffinata. Sei in bilico tra l'essere una che approfitta degli altri e una che viene usata. Forse è il momento di fare un esame di coscienza. Di guardarti dentro onestamente. Le regole non sono nemiche, sono confini. Senza confini, si cade.",
                    'consiglio': "🌋 Le scorciatoie portano in posti dove non vuoi stare. La vera libertà non è infrangere le regole, è scegliere quelle giuste. Guardati dentro, onestamente. Il cambiamento inizia da lì."
                }
            },

            'giove_ascendente_quadratura': {
                'quadratura': {
                    'titolo': "✨⬆️ Giove in quadratura con l'Ascendente",
                    'messaggio': "Sei una donna che si lascia andare, che indulge nei piaceri, che fatica a mettere freni. Fai tutto in eccesso, e spesso te ne accorgi troppo tardi. Hai idee grandiose, ma per realizzarle conti sull'aiuto di genitori o amici. Sei una che sa entrare nelle grazie delle persone importanti, che sa farsi volere bene. Ma questa tua capacità può diventare opportunismo. In fondo, sogni una vecchiaia serena, senza pensieri economici. Ma per ottenerla, devi imparare a controllarti, a non voler fare più di quanto è possibile. Lavorare in gruppo potrebbe aiutarti a sfruttare meglio le tue capacità. Da sola rischi di disperderti.",
                    'consiglio': "🌟 La tua simpatia è un dono, ma non deve diventare una strategia. Le persone non sono mezzi per raggiungere un fine, sono fini in sé. Impara a dare senza calcolare, a vivere senza eccessi. La vera ricchezza è la serenità, non il conto in banca."
                }
            },

            # SATURNO (quadrature)
            'saturno_urano_quadratura': {
                'quadratura': {
                    'titolo': "⏳⚡ Saturno in quadratura con Urano",
                    'messaggio': "Sei una donna che fatica a prendere decisioni, specialmente quando si tratta di cambiare. Sei abituata alle tue abitudini, alla tua routine, e qualsiasi novità ti spaventa. È come imparare a guidare la macchina dopo anni di bicicletta. La paura dell'ignoto ti blocca. Forse i tuoi genitori ti hanno trasmesso questa cautela, questa paura di osare. Ma il futuro dipende proprio dalla tua capacità di cambiare, anche se questo significa perdere qualche persona lungo la strada. Sei portata per lavori in grandi complessi, con possibilità di carriera. Politica, industria, scienza, ricerca. Devi imparare a fidarti del nuovo, a lasciare andare il vecchio. La vita è movimento.",
                    'consiglio': "⚡ Il cambiamento fa paura, ma è l'unica strada per crescere. Non sei più quella bambina che aveva bisogno di protezione. Oggi puoi affrontare il mondo. Fidati di te, e vai."
                }
            },

            'saturno_nettuno_quadratura': {
                'quadratura': {
                    'titolo': "⏳🌊 Saturno in quadratura con Nettuno",
                    'messaggio': "Hai paura di tutto. Paura di non farcela, di essere inadeguata, che succeda il peggio. E intanto non fai nulla per calmare questa ansia. Ti senti depressa, incapace di reagire. La verità è che hai paura delle responsabilità, di non essere all'altezza. Ma scappare non risolve niente. Solo accettando le sfide puoi metterti alla prova e scoprire che ce la puoi fare. Anche gli altri hanno paura, anche loro lottano. Chiedi consiglio a persone fidate, lascia che ti aiutino a sviluppare le tue potenzialità. E impara a volerti bene. La mancanza di amore per te stessa è la vera causa dei tuoi fallimenti.",
                    'consiglio': "🌊 La paura è un'ombra che si allunga quando il sole è basso. Cerca la luce dentro di te. Chiedi aiuto, fidati, lasciati guidare. La tua forza è più grande di quanto credi. Devi solo imparare a vederla."
                }
            },

            'saturno_ascendente_quadratura': {
                'quadratura': {
                    'titolo': "⏳⬆️ Saturno in quadratura con l'Ascendente",
                    'messaggio': "Sei una donna timida, riservata. Hai paura di mostrarti, di essere giudicata. Preferisci startene in disparte, piuttosto che combattere. Schivi le sfide, e quando le accetti, sei sempre sulla difensiva. Questa tua eccessiva prudenza ti fa perdere molte occasioni. La gente ti vede fredda, distaccata. In realtà sei solo seria, responsabile. Sai che tutto si guadagna con fatica, e non ti aspetti regali. Ma forse sei troppo dura con te stessa. Il tuo talento c'è, devi solo imparare a vederlo. A poco a poco, con i successi, acquisirai fiducia. E la sicurezza economica compenserà le insicurezze emotive. Ma intanto, cerca di aprire il cuore. La persona giusta capirà la tua serietà e la apprezzerà.",
                    'consiglio': "🛡️ La timidezza è uno scrigno che custodisce tesori. Ma se non lo apri, nessuno potrà vederli. Impara a mostrarti, a rischiare, a essere vulnerabile. La persona giusta non ti giudicherà, ti apprezzerà per quello che sei."
                }
            },

            # URANO (quadrature)
            'urano_plutone_quadratura': {
                'quadratura': {
                    'titolo': "⚡🌋 Urano in quadratura con Plutone",
                    'messaggio': "Hai chiaro cosa andrebbe fatto per difendere la tua libertà, ma preferisci che lo facciano gli altri. Tanto, qualcuno penserà a tutto. Questo è il tuo ragionamento. Ma se il pericolo arriva vicino a te, se tocca i tuoi diritti, allora sì che ti muovi. Sei nata in un periodo storico turbolento, la grande depressione, l'ascesa dei totalitarismi. La storia ti ha insegnato che l'indifferenza delle masse permette il peggio. Eppure, tu sei ancora indifferente. Forse è il momento di svegliarti. Di non aspettare che siano gli altri a lottare per te. La tua voce può fare la differenza. Usala.",
                    'consiglio': "⚡ La libertà non è un diritto che ti viene regalato, è un dovere che va esercitato ogni giorno. Non aspettare che siano gli altri a difendere ciò che è tuo. La storia è piena di esempi: chi tace, perde."
                }
            },

            'urano_nettuno_quadratura': {
                'quadratura': {
                    'titolo': "⚡🌊 Urano in quadratura con Nettuno",
                    'messaggio': "Sei nata in un periodo (1952-1956) in cui il mondo era in fermento. Percepisci l'oppressione, l'ingiustizia, ma fatichi a capire cosa fare. Alcuni della tua generazione hanno scelto di non esporsi, di non rischiare. Altri partecipano, ma da dietro le quinte, per non mettere a repentaglio la loro posizione. Anche tu sei così. Preferisci startene in disparte, tanto qualcuno penserà a tutto. Ma se il pericolo ti toccasse da vicino, allora sì che ti sveglieresti. Peccato che a volte sia troppo tardi. Hai la capacità di risvegliare le coscienze, di spingere all'azione. Non sprecarla. La tua voce può fare la differenza.",
                    'consiglio': "🌊 L'indifferenza è il miglior alleato dei tiranni. Non aspettare che il pericolo bussi alla tua porta. Muoviti ora, finché sei in tempo. La tua voce può cambiare le cose. Usala."
                }
            },

            'urano_ascendente_quadratura': {
                'quadratura': {
                    'titolo': "⚡⬆️ Urano in quadratura con l'Ascendente",
                    'messaggio': "Sei una ribelle nel cuore. Pensi di avere il diritto di fare ciò che vuoi, leggi o non leggi. Non hai grande senso di responsabilità, e non impari dagli errori. Fin da bambina sei stata diversa, in conflitto con la famiglia. Vuoi fare di testa tua, senza ascoltare nessuno. Il denaro non ti interessa, preferisci fare cose eclatanti, che ti mettano in luce. La tua mente è moderna, innovativa, ma non ti rendi conto che anche tu segui una tradizione: quella della tua generazione. Sul lavoro, non sopporti orari fissi, regole, contratti. Ti senti oppressa. Ma attenta a non lasciarti legare da accordi che ti imprigionano. La tua voglia di libertà è sacra, ma non deve diventare una gabbia per te stessa.",
                    'consiglio': "🕊️ La libertà non è assenza di legami, è scelta consapevole. Impara a distinguere le regole giuste da quelle sbagliate. Non tutte le tradizioni sono nemiche, non tutte le ribellioni sono costruttive. Scegli con saggezza le tue battaglie."
                }
            },

            # NETTUNO (quadrature)
            'nettuno_ascendente_quadratura': {
                'quadratura': {
                    'titolo': "🌊⬆️ Nettuno in quadratura con l'Ascendente",
                    'messaggio': "Sei una donna estremamente sensibile alle critiche. Qualsiasi commento negativo ti ferisce, ti blocca. Ti senti insicura, inferiore, e per questo eviti le sfide. Forse da bambina non hai avuto il supporto di cui avevi bisogno, nessuno ti ha guidata nelle scelte. Così sei cresciuta insicura, indecisa. Sogni a occhi aperti, ma non agisci. Hai una grande immaginazione, ma non la grinta per sfruttarla. Preferisci startene nell'ombra, mentre gli altri fanno carriera. Sei troppo pigra per studiare, per migliorarti. E così resti ferma. Hai bisogno di un lavoro che dia sollievo agli altri, che ti faccia sentire utile. L'assistenza sociale, il volontariato. Lì la tua sensibilità sarà un dono, non un limite.",
                    'consiglio': "🌊 La tua sensibilità è un dono, non una condanna. Impara a usarla per capire gli altri, per aiutarli. Ma prima, impara ad aiutare te stessa. La fiducia si costruisce un passo alla volta. Inizia oggi."
                }
            },

            # PLUTONE (quadrature)
            'plutone_ascendente_quadratura': {
                'quadratura': {
                    'titolo': "🌋⬆️ Plutone in quadratura con l'Ascendente",
                    'messaggio': "Sei una donna con una personalità forte, magnetica. Hai la convinzione di essere nel giusto, e in nome di questa certezza, cerchi di cambiare gli altri. Niente ti va mai bene, tutto va modificato secondo le tue vedute. Forse sei cresciuta con l'idea di essere destinata a grandi cose. Questo tuo atteggiamento crea problemi con tutti, specialmente con chi ha autorità. Sul lavoro, ti scontri con capi e colleghi. In amore, sei tirannica, arrogante. Ma se riuscissi a moderarti, a essere più equilibrata, potresti raggiungere la vera grandezza. Hai capacità organizzative enormi, coraggio, audacia. Impara a usarli con saggezza, non con prepotenza.",
                    'consiglio': "🌋 La tua forza è immensa, ma senza equilibrio diventa distruttiva. Impara ad ascoltare, a dubitare, a metterti in discussione. La vera autorità non si impone, si riconosce. La grandezza sta nell'umiltà, non nell'arroganza."
                }
            },

            
            # ============================================
            # MESSAGGI PER I TRIGONI RADIX
            # ============================================

            # SOLE (trigoni)
            'sole_luna_trigono': {
                'trigono': {
                    'titolo': "☀️🌙 Sole in trigono con la Luna",
                    'messaggio': "C'è una naturale armonia tra ciò che sei e ciò che senti. Le tue emozioni e la tua volontà lavorano insieme come una squadra affiatata, senza conflitti interiori. Questa pace con te stesso ti permette di affrontare la vita con serenità e di prendere decisioni equilibrate. Hai avuto un'infanzia che ti ha permesso di crescere rispettando la tua individualità, e questo ti ha regalato una sicurezza di base che non ti abbandona mai. Sei una persona creativa, con una riserva di energia a cui attingere nei momenti di bisogno. I giovani e i bambini si sentono naturalmente attratti da te perché trasmetti protezione e interesse sincero. Anche se a volte potresti essere più ambizioso, la tua capacità di stare bene con te stesso è già una forma di successo. Sul lavoro sai guidare senza imporre, e la tua autorevolezza naturale viene riconosciuta senza bisogno di sforzi. Nelle relazioni sei cordiale con tutti, dai vecchi amici agli sconosciuti, e lasci un'impressione positiva ovunque vai.",
                    'consiglio': "🌱 La tua anima è in pace, e questa è la tua forza più grande. Non lasciare che i dubbi ti facciano sottovalutare. Il mondo ha bisogno della tua luce serena. Continua a brillare, senza fretta, senza paura."
                }
            },

            'sole_marte_trigono': {
                'trigono': {
                    'titolo': "☀️🔥 Sole in trigono con Marte",
                    'messaggio': "Hai una determinazione tranquilla che non ha bisogno di urlare per farsi sentire. Affronti le sfide con coraggio e tenacia, ma senza quella aggressività che mette a disagio gli altri. Sei onesto e trasparente, e ti offri quando qualcuno mette in dubbio la tua etica, perché hai le carte in regola. La tua energia è costante e ben distribuita: non sei un vulcano in eruzione, ma una fiamma che scalda senza bruciare. Sul lavoro sai essere un punto di riferimento senza diventare una minaccia per nessuno. I colleghi ti apprezzano e ti rispettano. Hai una naturale capacità di stare con i giovani, perché li accetti per quello che sono senza pretendere che si comportino da adulti. In amore sei flessibile e accomodante: non hai pretese impossibili e sai adattarti alla persona che ami, purché la relazione sia autentica. La tua vita scorre senza troppi drammi, perché risolvi i problemi con discrezione, senza bisogno di metterli in piazza.",
                    'consiglio': "⚔️ La tua forza è silenziosa, ma profonda. Non serve fare rumore quando si è sicuri di sé. Continua così: la tua calma è la tua arma più potente. E ricordati che a volte la battaglia più importante è quella che non combatti."
                }
            },

            'sole_giove_trigono': {
                'trigono': {
                    'titolo': "☀️✨ Sole in trigono con Giove",
                    'messaggio': "Hai un potenziale creativo enorme, ma c'è il rischio che resti sopito perché non ami farti prendere dalla mischia. Sei intelligente, ottimista, parli bene e ti tieni informato, ma non hai quella spinta in più che ti porta a cercare sfide e competizioni. Preferisci una vita tranquilla, senza troppe pressioni, e questo non è un male, purché non diventi una scusa per non esprimere i tuoi talenti. La tua presenza è rassicurante per chi ti sta intorno: nei momenti difficili, la tua calma e il tuo ottimismo sono un porto sicuro. I bambini ti vogliono bene perché non li incalzi, non pretendi, li lasci essere. Sei generoso con te stesso e con gli altri, forse anche troppo, e questo ti espone al rischio che qualcuno approfitti della tua buona fede. In amore cerchi persone semplici, con una solida fibra morale, perché per te la sostanza conta più dell'apparenza.",
                    'consiglio': "🦋 Il tuo potenziale è un bozzolo: dentro c'è una farfalla che aspetta di volare. Non lasciare che la pigrizia la tenga imprigionata. Il mondo ha bisogno della tua luce. Spiega le ali: il volo è la tua natura."
                }
            },

            'sole_saturno_trigono': {
                'trigono': {
                    'titolo': "☀️⏳ Sole in trigono con Saturno",
                    'messaggio': "Il successo per te non è una questione di fortuna, ma di costruzione solida e paziente. Sai aspettare, sai pianificare, sai assumerti le responsabilità quando è il momento. Questa consapevolezza dei tuoi talenti ti rende sicuro senza essere arrogante. Sul lavoro sei un punto di riferimento: la gente si fida di te perché sai quello che fai e non prometti mai più di quanto puoi mantenere. Non sei uno che si lascia trasportare dall'entusiasmo del momento, ma quando decidi di impegnarti, lo fai sul serio. In amore sei stabile, affidabile, e cerchi una persona che abbia i tuoi stessi valori: serietà, onestà, obiettivi chiari. Quando la persona amata attraversa momenti difficili, sei lì, silenzioso ma presente, a infondere fiducia. La tua salute è buona perché hai uno stile di vita equilibrato e non eccedi in nulla.",
                    'consiglio': "🏛️ La tua vita è una cattedrale: costruita pietra su pietra, con pazienza, con amore. Continua a edificare, ma ricordati di lasciare entrare la luce. La disciplina è il fondamento, ma la gioia ne è l'ornamento."
                }
            },

            'sole_urano_trigono': {
                'trigono': {
                    'titolo': "☀️⚡ Sole in trigono con Urano",
                    'messaggio': "Hai un magnetismo naturale che attira le persone senza che tu debba fare nulla. La tua mente è aperta, liberale, curiosa, e questo ti rende affascinante e piacevole. Sai sempre trovare il modo giusto per esprimere la tua creatività, e lo fai con tale naturalezza che quasi non ti accorgi di essere bravo. Questa mancanza di presunzione ti salva dall'egocentrismo e ti rende ancora più apprezzato. Conosci i tuoi pregi e i tuoi difetti, e sai mettere in risalto i primi senza nascondere i secondi. La gente si fida di te perché capisce che il tuo interesse per gli altri è genuino. Hai un' intuizione speciale per capire quando qualcuno ha bisogno di te, e intervieni con discrezione e generosità. In amore sai mantenere vivo l'interesse con la tua apertura mentale e la tua capacità di sorprendere senza mai essere invadente.",
                    'consiglio': "⚡ La tua mente è un fulmine che illumina il cammino. La tua originalità è un dono prezioso. Usala per sollevare gli altri, non per sovrastarli. La vera grandezza è far sentire importanti coloro che ti stanno accanto."
                }
            },

            'sole_nettuno_trigono': {
                'trigono': {
                    'titolo': "☀️🌊 Sole in trigono con Nettuno",
                    'messaggio': "Hai un talento naturale per l'espressione artistica e creativa, ma fatichi a metterlo a frutto con costanza. Parti con entusiasmo, ma poi ti stanchi e lasci perdere. Impari tutto con facilità, quasi senza sforzo, perché hai una comprensione intuitiva delle cose che altri raggiungono solo dopo anni di studio. Da bambino probabilmente ti annoiavi a scuola perché sapevi già quello che insegnavano. Questo ti ha abituato a non dover lottare per imparare, e da adulto fatichi ad assumerti impegni che richiedono continuità. Hai bisogno di un lavoro che ti lasci libero di seguire i tuoi ritmi, senza scadenze rigide. L'arte, la scrittura, la musica, la ricerca possono essere la tua strada. In amore sei romantico e idealista, ma senza perdere il contatto con la realtà. I tuoi legami sono profondi e rispettosi della libertà reciproca. Con i figli sarai sempre un genitore presente e affettuoso.",
                    'consiglio': "🌊 La tua anima è un oceano di creatività. Non lasciare che la pigrizia lo renda una pozzanghera. La disciplina non è nemica dell'ispirazione, è la sua alleata. Immergiti, esplora, crea. Il mondo aspetta la tua arte."
                }
            },

            'sole_plutone_trigono': {
                'trigono': {
                    'titolo': "☀️🌋 Sole in trigono con Plutone",
                    'messaggio': "Hai una determinazione silenziosa ma incrollabile. Quando decidi di raggiungere un obiettivo, niente può fermarti. Ma non sei mosso dall'ambizione personale: ciò che ti spinge è il desiderio di migliorare le cose intorno a te, di riparare ingiustizie, di portare ordine dove c'è caos. La tua presenza ha un effetto trasformativo sulle persone, quasi magico, e non te ne rendi nemmeno conto. Sei un leader nato, ma le posizioni di potere non ti interessano: preferisci lavorare nell'ombra per risolvere problemi veri. Hai un'intuizione fuori dal comune che ti guida nei momenti di crisi, e spesso la gente si chiede come fai a sapere cose che non ti sono state dette. Sei portato per professioni che richiedono indagine e profondità: investigazione, psicologia, medicina, finanza. La fortuna ti accompagna, ma è una fortuna che ti costruisci da solo con la tua visione e la tua tenacia.",
                    'consiglio': "🌋 La tua forza interiore è un vulcano di energia creativa. Non tenerla sopita. Il mondo ha bisogno della tua visione, del tuo coraggio, della tua capacità di trasformare il caos in ordine. Alzati e agisci: il tuo momento è ora."
                }
            },

            'sole_ascendente_trigono': {
                'trigono': {
                    'titolo': "☀️⬆️ Sole in trigono con l'Ascendente",
                    'messaggio': "La tua personalità traspare con naturalezza e generosità. Sei ottimista senza essere ingenuo, e la gente collabora volentieri con te perché ti percepisce come una persona autentica. La tua creatività è vivida, a volte sembri ispirato, ma c'è il rischio che tu ti adagi sugli allori, pensando di avere tutto il tempo del mondo. Sei il frutto di un'educazione che ti ha dato buone basi, ma hai anche una tua identità ben distinta. Quando accetti le responsabilità, ottieni grandi risultati. Sei sensibile alle critiche, forse troppo, ma guardi al futuro con determinazione, cercando un lavoro che ti dia sicurezza oltre che soddisfazione. Sul lavoro sei competente e pretendi di essere riconosciuto per quello che vali. In amore cerchi una persona che condivida i tuoi entusiasmi e che ti sproni a dare il meglio. Con il partner giusto, diventi inarrestabile.",
                    'consiglio': "🌟 La tua luce è unica. Non nasconderla per paura del giudizio. Il mondo ha bisogno del tuo ottimismo, della tua generosità, della tua autenticità. Credi in te stesso quanto gli altri credono in te. Il successo ti aspetta: basta fare il primo passo."
                }
            },

            # LUNA (trigoni)
            'luna_mercurio_trigono': {
                'trigono': {
                    'titolo': "🌙💬 Luna in trigono con Mercurio",
                    'messaggio': "La tua mente e il tuo cuore dialogano in perfetta armonia. Non c'è conflitto tra ciò che senti e ciò che pensi, e questo ti permette di comprendere te stesso e gli altri con rara chiarezza. Hai una memoria eccellente, specialmente per le cose che hanno un significato emotivo, e sai usare le esperienze passate per crescere, senza restarne imprigionato. La tua mente è flessibile e tollerante, e questo ti rende un amico prezioso e un confidente naturale. La gente si sente a suo agio con te perché capisci senza giudicare. Sul lavoro sai analizzare i problemi con obiettività e non hai paura di chiedere consiglio quando serve. La tua vita è piena di amicizie, attività sociali e serenità familiare. Anche quando l'ansia si affaccia, sai accoglierla senza farti travolgere, e questa tua capacità diventa un esempio per chi soffre di ansia cronica. Le tue possibilità di realizzazione sono immense, perché sai unire ragione ed emozione in modo costruttivo.",
                    'consiglio': "📚 La tua mente è una biblioteca, il tuo cuore il bibliotecario. Insieme creano un equilibrio perfetto. Continua a imparare, a crescere, a condividere. La tua saggezza è un faro per chi si sente perso. Non smettere mai di illuminare."
                }
            },

            'luna_venere_trigono': {
                'trigono': {
                    'titolo': "🌙❤️ Luna in trigono con Venere",
                    'messaggio': "La tua natura è gentile, armoniosa, e chi ti incontra lo sente subito. Hai un modo di fare che mette a proprio agio, una presenza che rassicura senza bisogno di parole. La tua fiducia nelle persone è genuina, e questo spesso le spinge a essere all'altezza della tua stima. Hai una bellezza che viene da dentro, e le tue maniere sono così piacevoli che la gente ti percepisce come bello anche se non lo sei. Sei creativo, onesto, e sai usare le tue doti per costruire relazioni autentiche. Nel lavoro, le relazioni pubbliche sono il tuo campo naturale. Nei gruppi, la tua presenza è sempre gradita perché sai infondere vitalità senza sopraffare. Hai un'ottima capacità di giudizio, ma non la imponi mai. Rifuggi dalla volgarità e dall'equivoco con naturalezza, senza snobismo. In amore cerchi persone sincere come te, e i bambini ti adorano perché con te si sentono compresi e amati. I tuoi hobby creativi sono uno sfogo prezioso e una fonte di gioia.",
                    'consiglio': "💖 Il tuo cuore è un giardino fiorito. La tua gentilezza è la tua forza più grande. Continua a seminare amore e armonia: raccoglierai la stessa moneta. Il mondo ha bisogno della tua dolcezza, non cambiare mai."
                }
            },

            'luna_marte_trigono': {
                'trigono': {
                    'titolo': "🌙🔥 Luna in trigono con Marte",
                    'messaggio': "Le tue emozioni sono intense, ma non ti travolgono. Sai usarle come carburante per la tua creatività e le tue azioni. Hai bisogno di muoverti, di sfogare energia, ma lo fai con misura. Sai quando è il momento di lottare e quando è meglio scendere a compromessi, e questa flessibilità ti apre molte porte. Anche quando non sei soddisfatto di come vanno le cose, non ti lasci andare al vittimismo. Se devi riprendere qualcuno, lo fai senza violenza e senza rancore. Sei indipendente, non ti leghi emotivamente in modo ossessivo, e questo ti permette di avere relazioni leggere e piacevoli con tutti. Rispetti la privacy altrui e chiedi lo stesso rispetto. Le sfide non ti spaventano: le affronti con calma, e se perdi, pace. Non ne fai una tragedia. Sei un punto di riferimento per i bambini, perché li tratti da pari, senza pretendere che siano adulti. La tua tolleranza è quasi eccessiva, ma ti regala una vita sociale ricca e serena.",
                    'consiglio': "🔥 La tua energia è una fiamma che illumina senza bruciare. La tua intensità è un dono, ma la moderazione è la sua guida. Continua a vivere con passione, ma ricordati che a volte la forza più grande è saper aspettare."
                }
            },

            'luna_giove_trigono': {
                'trigono': {
                    'titolo': "🌙✨ Luna in trigono con Giove",
                    'messaggio': "La tua anima è un sole che scalda chi ti sta intorno. La tua generosità è spontanea, il tuo ottimismo contagioso. Anche quando le cose vanno male, trovi il modo di vedere il lato positivo, e questa tua capacità solleva il morale di tutti. Non ti piacciono le complicazioni: vai dritto al punto, risolvi i problemi con pragmatismo e vai avanti. Sei sempre aggiornato, sai conversare di tutto, e la tua compagnia è piacevole e stimolante. Ti interessi ai problemi della comunità e spesso vieni eletto a ruoli di responsabilità. Sostieni con entusiasmo le cause sociali, anche se preferisci non gestirle direttamente. Professioni come relazioni pubbliche, fisioterapia, organizzazione di viaggi sono perfette per te. Attenzione però a non esagerare: tendi a prenderti troppi impegni e a indulgere nei piaceri della vita. Un po' di moderazione ti aiuterà a non esaurire le energie. In amore cerchi persone moralmente solide, sincere, con valori spirituali elevati. Con gli anni, i tuoi legami si approfondiscono e diventano sempre più preziosi.",
                    'consiglio': "✨ La tua generosità è una benedizione, ma non dimenticare di essere generoso anche con te stesso. Impara a dosare le energie, a dire no quando serve. La tua luce non si spegnerà per una pausa: anzi, brillerà ancora più forte."
                }
            },

            'luna_saturno_trigono': {
                'trigono': {
                    'titolo': "🌙⏳ Luna in trigono con Saturno",
                    'messaggio': "Sei prudente per natura, ma non chiuso. Rispetti la tradizione, ma sai accogliere il cambiamento quando è costruttivo. La tua stabilità emotiva è una roccia su cui gli altri possono appoggiarsi. Hai imparato dai tuoi genitori il valore del lavoro e del buonsenso, e questo ti ha reso una persona pratica e affidabile. Sul lavoro sei un punto di riferimento: ingegneria, politica, insegnamento, legge sono campi in cui puoi eccellere. Non hai bisogno di fare carriera a tutti i costi, ma quando serve, sei all'altezza. Hai pochi amici, ma veri, e durano tutta la vita. In amore sei serio e coerente: non ti butti in relazioni frivole, ma quando ti impegni lo fai con tutto te stesso. La persona amata deve essere seria e corretta come te. Come genitore sei severo ma affettuoso, e sai guidare i tuoi figli con mano ferma e cuore aperto.",
                    'consiglio': "⏳ La tua stabilità è una roccia. La tua fedeltà è un tesoro raro. Continua a costruire relazioni solide, ma ricordati di lasciare spazio alla leggerezza. La vita non è solo dovere: è anche gioia. Impara a bilanciare serietà e sorriso."
                }
            },

            'luna_urano_trigono': {
                'trigono': {
                    'titolo': "🌙⚡ Luna in trigono con Urano",
                    'messaggio': "La tua mente è curiosa, vivace, sempre alla ricerca di qualcosa di nuovo. Non ti accontenti delle banalità: vuoi capire, approfondire, andare oltre. Questa tua apertura mentale attira persone interessanti, e le tue conversazioni sono sempre stimolanti. Ma sai anche ascoltare, e questo ti rende un amico prezioso. L'educazione che hai ricevuto ti ha preparato ad affrontare il futuro con flessibilità e coraggio. Rispetti le regole, ma non hai paura di contestare chi le usa male. Il lavoro di gruppo è il tuo ambiente ideale: l'insegnamento, la politica, i programmi sociali ti permettono di esprimere al meglio le tue doti. Quando parli in pubblico, la tua eloquenza è magnetica. Guardi al futuro con ottimismo, ma senza dimenticare le lezioni del passato. Sei attratto dall'occulto e dalla spiritualità. In amore hai bisogno di una persona che sia sulla tua stessa lunghezza d'onda, altrimenti la noia ti uccide.",
                    'consiglio': "⚡ La tua mente è un'esplosione di creatività. La tua visione del futuro è un dono prezioso. Condividila con chi è pronto ad accoglierla. I pionieri sono sempre soli all'inizio, ma alla fine fanno scuola. Non smettere mai di guardare avanti."
                }
            },

            'luna_nettuno_trigono': {
                'trigono': {
                    'titolo': "🌙🌊 Luna in trigono con Nettuno",
                    'messaggio': "La tua anima è un oceano profondo, e la tua intuizione è la bussola che ti guida. Spesso sai le cose senza che nessuno te le abbia dette: è come se percepissi la verità al di là delle apparenze. Questa tua sensibilità si esprime in modo creativo, nell'arte, nella musica, nella poesia. Hai un forte senso del dovere sociale, ma non sei un fanatico: la tua spiritualità è vissuta con discrezione e autenticità. Aiuti chi è in difficoltà, ma non sopporti chi non muove un dito per aiutarsi da solo. In famiglia sei affettuoso e presente, anche se a volte puoi scegliere di non formare una famiglia per non perdere la tua libertà. I giovani si sentono compresi da te, perché non li giudichi. Sei attratto da persone colte e raffinate, ma anche in ambienti difficili sai portare il tuo contributo per migliorare le cose. La tua vocazione è il servizio: programmi sociali, assistenza, aiuto al prossimo.",
                    'consiglio': "🌊 La tua intuizione è una bussola che ti guida nell'ignoto. Fidati di lei, ma non perdere il contatto con la riva. La tua creatività è un dono per il mondo: condividila. Il mare è profondo, ma la superficie è fatta per navigare."
                }
            },

            'luna_plutone_trigono': {
                'trigono': {
                    'titolo': "🌙🌋 Luna in trigono con Plutone",
                    'messaggio': "Le tue emozioni sono profonde come l'abisso, ma tu le controlli con naturalezza, senza reprimerle. Questa padronanza interiore ti permette di amare senza possessività e di aiutare senza invadenza. Sei socievole e amichevole, ma non disperdi il tuo affetto in relazioni superficiali: sai distinguere chi merita il tuo cuore. I bambini e i giovani sono la tua gioia: con loro hai un rapporto speciale, fatto di rispetto e complicità. La tua capacità di prenderti cura degli altri è infinita, e trovi la tua realizzazione nel servizio agli handicappati, ai poveri, a chi soffre. Professionalmente sei portato per le relazioni pubbliche, la fisioterapia, i programmi assistenziali, la consulenza finanziaria. Capisci il potere e il denaro meglio di molti, e sai usarli con saggezza. Lavorare a contatto con gli altri è per te il modo migliore per conoscere te stesso e guarire le tue ferite.",
                    'consiglio': "🌋 La tua profondità emotiva è un abisso di tesori nascosti. Non aver paura di esplorarlo. La tua capacità di amare senza riserve è un dono raro. Usalo con saggezza, donalo a chi merita. Il mondo ha bisogno del tuo calore silenzioso."
                }
            },

            'luna_ascendente_trigono': {
                'trigono': {
                    'titolo': "🌙⬆️ Luna in trigono con l'Ascendente",
                    'messaggio': "La tua personalità è piacevole, sensibile, creativa. Chi ti incontra percepisce subito la tua autenticità e si fida di te. I valori che hai ricevuto dalla tua famiglia sono diventati parte di te, ma non ti imprigionano: li hai fatti tuoi e li vivi con naturalezza. Hai tante idee e iniziative, e spesso trovi il modo di realizzarle, anche quando i mezzi sono limitati. La tua gentilezza a volte attira profittatori: impara a distinguere chi merita la tua fiducia. Sei destinato a fare carriera perché sai sacrificare il tempo libero allo studio e al lavoro. In amore sai mantenere viva la fiamma, perché per te ogni giorno è un'occasione per rivivere l'emozione del primo incontro. Non lasci che la routine offuschi la magia della relazione.",
                    'consiglio': "🌸 La tua sensibilità è un fiore raro. Coltivalo con cura, ma non chiuderlo in una serra. Il mondo ha bisogno della sua bellezza. La tua creatività è il suo profumo: lascialo diffondere. Sii te stesso, senza paura. La tua autenticità è la tua forza."
                }
            },

            # MERCURIO (trigoni)
            'mercurio_marte_trigono': {
                'trigono': {
                    'titolo': "💬🔥 Mercurio in trigono con Marte",
                    'messaggio': "La tua mente è agile e la tua parola è efficace, ma non senti il bisogno di imporre le tue idee a tutti i costi. Conosci i tuoi limiti e le tue capacità, e questa consapevolezza ti permette di muoverti con sicurezza senza diventare arrogante. Sei sempre informato e partecipi alle conversazioni con garbo, senza bisogno di avere sempre l'ultima parola. La tua discrezione è proverbiale: se ti affidano un segreto, puoi essere certo che non uscirà mai dalle tue labbra. Queste doti ti aprono molte strade: legge, politica, insegnamento, relazioni pubbliche, scrittura. Hai una pazienza speciale con i giovani: sai ascoltarli e guidarli senza soffocarli. Lavori bene sia in gruppo che da solo, ma il gruppo ti dà quella carica in più che ti serve per esprimerti al meglio. Nel tempo libero, l'artigianato creativo può diventare molto più di un hobby. In amore cerchi una persona creativa come te, con cui condividere un rapporto di stima e collaborazione reciproca.",
                    'consiglio': "🎯 La tua mente è uno strumento preciso, la tua parola è una carezza. Usali con saggezza. La tua discrezione è la tua forza. Ricorda: a volte ciò che non dici è più importante di ciò che dici."
                }
            },

            'mercurio_giove_trigono': {
                'trigono': {
                    'titolo': "💬✨ Mercurio in trigono con Giove",
                    'messaggio': "Sei una biblioteca vivente, ma con una dote rara: sai condividere la tua conoscenza senza pedanteria, anzi, con quella leggerezza che rende piacevole imparare da te. Sei ottimista, credi in te stesso, e questa fiducia è contagiosa. Hai studiato tanto, e forse ti compiaci un po' della tua cultura, ma senza diventare insopportabile. L'insegnamento è la tua strada maestra, ma anche il giornalismo, la giurisprudenza, le consulenze ti si addicono. Impari in fretta, hai memoria, e sei un collaboratore prezioso in qualsiasi contesto. Le persone importanti ti stimano e si fidano di te, perché hai classe e sai stare al tuo posto senza perdere la tua identità. Sei amato sia dai ricchi che dai poveri, perché non perdi mai il senso delle proporzioni. In amore sei un compagno delizioso, mai noioso, sempre capace di stupire. I bambini ti adorano: con te si sentono capiti, ascoltati, rispettati. La tua salute è buona perché affronti la vita con ottimismo, senza ingigantire i problemi.",
                    'consiglio': "📚 La tua mente è una biblioteca, la tua parola è la voce che dà vita ai libri. Condividi il tuo sapere con generosità, ma senza presunzione. La vera saggezza sa di non sapere. Continua a imparare, a stupirti, a crescere."
                }
            },

            'mercurio_saturno_trigono': {
                'trigono': {
                    'titolo': "💬⏳ Mercurio in trigono con Saturno",
                    'messaggio': "La tua mente è un orologio svizzero: precisa, organizzata, affidabile. Hai le idee chiare e sai esprimerle con ordine e profondità. Non aspetti che le occasioni ti cadano dal cielo: te le vai a cercare. La tua memoria è un archivio ben ordinato dove recuperi qualsiasi informazione ti serva. Sei efficiente, sai distinguere l'essenziale dal superfluo, e affronti compiti complessi che altri nemmeno oserebbero iniziare. L'insegnamento superiore, l'architettura, la politica, la ricerca sono campi in cui eccelli. Non ti perdi in sogni a occhi aperti: sei concreto, realistico, e conosci i tuoi limiti tanto quanto i tuoi pregi. La tua integrità è incrollabile, e chi ti tradisce perde la tua fiducia per sempre. Sei un confessore laico: la gente si confida con te perché sai ascoltare e capire. Anche in pensione, non riuscirai a smettere di fare, perché per te la vita è azione e significato.",
                    'consiglio': "⏳ La tua mente è un orologio di precisione. La tua affidabilità è leggendaria. Ma ricordati che la vita non è solo dovere. Concediti il lusso dell'improvvisazione, della leggerezza, del gioco. Anche gli orologi più preziosi hanno bisogno di essere caricati con gioia."
                }
            },

            'mercurio_urano_trigono': {
                'trigono': {
                    'titolo': "💬⚡ Mercurio in trigono con Urano",
                    'messaggio': "La tua mente è un lampo di genio: intuitiva, originale, sempre pronta a cogliere ciò che gli altri non vedono. Non ti accontenti delle verità preconfezionate: vuoi scoprire da solo, scavare, capire. La libertà di pensiero è il tuo respiro. Hai una comprensione naturale dell'occulto, del mistero, di tutto ciò che sta oltre la superficie. Potresti diventare un grande ricercatore, uno psicologo, un filosofo, o dedicarti ai fenomeni psichici. Ma l'insegnamento è la tua vera vocazione: hai visto la verità e senti il dovere di condividerla. Sai guidare gli altri a sviluppare il proprio potenziale, senza imporre il tuo punto di vista. Sei un precursore, capisci cose che altri capiranno solo anni dopo. La tua spiritualità è solida e integrata con la vita pratica: non c'è conflitto in te tra cielo e terra. Per te la conoscenza non è fine a se stessa, ma strumento di evoluzione umana.",
                    'consiglio': "⚡ La tua mente è un fulmine che squarcia il cielo della mediocrità. La tua originalità è un dono raro. Usala per illuminare, non per abbagliare. La vera saggezza è condividere ciò che sai con umiltà e amore. Sii luce, non lampo."
                }
            },

            'mercurio_nettuno_trigono': {
                'trigono': {
                    'titolo': "💬🌊 Mercurio in trigono con Nettuno",
                    'messaggio': "La tua parola è musica, la tua comunicazione è poesia. Hai il dono di toccare il cuore della gente con le tue parole, perché parli non solo alla mente, ma all'anima. La tua intuizione è affilata: capisci le persone al di là di quello che dicono, percepisci le loro vere intenzioni. Sei artistico, sensibile, e la tua creatività si esprime in mille forme: musica, pittura, scrittura, teatro. Accetti le responsabilità sociali con naturalezza, senza sentirle come un peso. Sei tollerante verso i difetti altrui, e la tua speranza è contagiosa: nei momenti difficili, la tua presenza è un balsamo. Come oratore sei magnetico: ti sintonizzi sull'umore del pubblico e lo trascini con te. Non perdi tempo in chiacchiere futili: vai dritto al cuore delle questioni importanti. La tua vita interiore è così ricca che non senti mai la solitudine. In compagnia di persone raffinate e colte, trovi nutrimento per l'anima.",
                    'consiglio': "🌊 La tua parola è musica, la tua anima è poesia. La tua sensibilità è un dono prezioso. Non tenerla nascosta: condividila, esprimila, donala. L'arte che porti dentro può guarire, consolare, elevare. Il mondo aspetta la tua voce unica."
                }
            },

            'mercurio_plutone_trigono': {
                'trigono': {
                    'titolo': "💬🌋 Mercurio in trigono con Plutone",
                    'messaggio': "La tua mente è uno scandaglio che penetra nei misteri più profondi. Niente ti sfugge, niente ti è estraneo. Hai una capacità di concentrazione fuori dal comune e una passione per l'ignoto che ti spinge a esplorare territori che altri nemmeno osano avvicinare. Criminologia, medicina, ricerca, chimica, finanza: qualsiasi campo richieda indagine e profondità è adatto a te. Ami le sfide, le responsabilità pesanti, i lavori che richiedono dedizione totale. Quando un progetto ti appassiona, non senti stanchezza. La tua scrittura sarebbe perfetta per romanzi gialli o saggi tecnici. Passi con disinvoltura dalla finanza all'occulto, perché il tuo sapere è vasto e integrato. In amore sei esigente, ma anche generoso: pretendi molto, ma dai altrettanto. La tua percezione ti permette di vedere oltre le apparenze e di capire le vere motivazioni della gente. Parli con autorevolezza e sai adattarti a qualsiasi interlocutore. Attenzione però: la tua competenza può suscitare invidie. Lascia spazio anche agli altri.",
                    'consiglio': "🔍 La tua mente è uno scandaglio che penetra nei misteri più profondi. Usalo per cercare la verità, ma anche per costruire bellezza. La conoscenza senza amore è arida. Aggiungi il cuore alla tua mente, e vedrai meraviglie."
                }
            },

            'mercurio_ascendente_trigono': {
                'trigono': {
                    'titolo': "💬⬆️ Mercurio in trigono con l'Ascendente",
                    'messaggio': "Hai il dono della parola e sai come usarlo. Quando parli, la gente ti ascolta, perché la tua comunicazione è teatrale senza essere artificiosa, coinvolgente senza essere invadente. I tuoi genitori hanno creduto in te fin da bambino, e questo ti ha dato una sicurezza che traspare in ogni tua parola. Sei ottimista, resiliente: quando cadi, ti rialzi e ricominci, perché per te la sconfitta non esiste. Da ogni errore impari e trovi nuovi modi per esprimere i tuoi talenti. Hai il dono di trasformare le idee in denaro, quasi senza sforzo. Non sei un gran lavoratore, ma riesci comunque a ottenere risultati, perché hai fiuto e tempismo. Non ti affidi solo alla fortuna: valuti le probabilità con logica e buonsenso. Con i superiori sei un maestro di diplomazia: sai mostrarti interessato ai loro bisogni senza essere servile. Riconosci l'importanza della cultura, ma la tua vera forza è la comunicazione. Sfidi solo quando sai di poter vincere.",
                    'consiglio': "🎭 La tua parola è teatro, la tua presenza è spettacolo. Il mondo è il tuo palcoscenico. Ma ricordati che il miglior attore non è quello che ruba la scena, ma quello che sa far brillare anche gli altri. Usa il tuo carisma per elevare, non per oscurare."
                }
            },

            # VENERE (trigoni)
            'venere_marte_trigono': {
                'trigono': {
                    'titolo': "❤️🔥 Venere in trigono con Marte",
                    'messaggio': "Sei caldo senza essere opprimente, passionale senza essere possessivo. La tua affettuosità è spontanea e sincera, e chi ti sta accanto si sente accolto, mai giudicato. Non pretendi dagli altri più di quanto sei disposto a dare, e questa equità ti rende una persona con cui è facile andare d'accordo. Il tuo sex-appeal è naturale, ma non ne fai un'arma: per te l'attrazione è solo una parte di un rapporto che deve essere completo. Sei sempre pronto al compromesso, e questo invoglia gli altri a fare altrettanto con te. La tua casa è accogliente, e ami ricevere gli amici con originalità e calore. La creatività è la tua linfa: teatro, musica, danza, anche solo come hobby, ti ricaricano le batterie. Il tuo modo di parlare è fluido e piacevole, perfetto per le relazioni pubbliche. Con i bambini sei magico: li stimoli, li incoraggi, li capisci. In amore, la tua allegria a volte può essere fraintesa: chi è più sentimentale potrebbe pensare che tu non prenda le cose sul serio. Ma non è così: semplicemente, la tua serietà non ha bisogno di fare la faccia triste.",
                    'consiglio': "💞 Il tuo cuore è una fiamma che scalda senza bruciare. La tua gioia di vivere è contagiosa. Continua a seminare affetto e armonia. Il mondo ha bisogno del tuo sorriso. Non smettere mai di amare con leggerezza, perché l'amore vero è leggero."
                }
            },

            'venere_giove_trigono': {
                'trigono': {
                    'titolo': "❤️✨ Venere in trigono con Giove",
                    'messaggio': "La tua anima è un arcobaleno dopo la pioggia. Il tuo ottimismo è così radicato che nulla riesce a scalfirlo, e questa tua serenità è un regalo per chi ti sta vicino. Nei momenti bui, la tua presenza è come una carezza: ricordi agli altri che tutto passerà, che dopo la notte viene l'alba. Sei amichevole, generoso, comprensivo, e la gente si fida di te perché sente che non hai secondi fini. Hai un talento naturale per le relazioni pubbliche, l'organizzazione sociale, le attività artistiche. Il design, l'arredamento, la decorazione sono campi in cui la tua sensibilità estetica può esprimersi al meglio. Detesti la volgarità, la grossolanità, e istintivamente ti allontani da chi non ha senso delle proporzioni. La musica, la danza, il teatro sono il cibo della tua anima. In amore cerchi una persona che ti accetti così come sei, senza volerti cambiare. Sei riservato in pubblico, ma nell'intimità sai essere tenero ed espansivo. La tua vita familiare sarà probabilmente felice e armoniosa.",
                    'consiglio': "✨ La tua anima è un arcobaleno. La tua gioia di vivere è un balsamo. Continua a splendere della tua luce unica. L'amore che dai ti tornerà moltiplicato. La vita ti sorride perché tu sai sorriderle per primo."
                }
            },

            'venere_saturno_trigono': {
                'trigono': {
                    'titolo': "❤️⏳ Venere in trigono con Saturno",
                    'messaggio': "Hai un giudizio sulle persone che raramente sbaglia. Sai a chi rivolgerti, di chi fidarti, e questo ti evita molte delusioni. Sei responsabile, ottimista senza essere ingenuo, e sai confidarti con gli amici quando serve, perché hai scelto bene chi ti sta accanto. L'educazione che hai ricevuto ti ha insegnato che senza disciplina non si va lontani, e questa lezione l'hai fatta tua. Non sei uno che spreca affetto: quando dai, dai con criterio, ma quando dai sei presente fino in fondo. Anche se non eserciti un'arte, hai una profonda comprensione della bellezza, e questo arricchisce la tua vita. Il tuo senso dell'ordine e dell'equilibrio ti rende perfetto per professioni come banca, legge, assicurazioni, architettura. Come hobby, potresti insegnare arti e mestieri ai giovani. In amore non ti innamori a prima vista: valuti, soppesi, ma quando scegli, la tua scelta è per sempre. Sei un genitore severo ma giusto, e i tuoi figli te ne saranno grati. La vecchiaia sarà per te un tempo di raccolto e soddisfazioni.",
                    'consiglio': "⏳ Il tuo amore è come una quercia: cresce lentamente, ma le sue radici sono profonde. La tua fedeltà è un tesoro raro. Continua a costruire relazioni solide. La pazienza è la tua alleata, la costanza la tua forza. L'amore vero non ha fretta."
                }
            },

            'venere_urano_trigono': {
                'trigono': {
                    'titolo': "❤️⚡ Venere in trigono con Urano",
                    'messaggio': "Sei una persona cordiale, ottimista, e sai goderti la vita senza sensi di colpa. Il tuo amore per gli altri è sincero, ma mai appiccicoso: sai amare senza possedere, e questo rende la tua compagnia leggera e piacevole. Hai un radar per l'insincerità: chi è falso con te lo scopri subito, e te ne allontani senza drammi. Sei generoso, ma la tua generosità non è ingenua: sai che chi dà riceve, e questa legge cosmica la vivi con naturalezza. Il tuo senso estetico è sviluppato, e l'arte, la musica, il design sono la tua seconda pelle. In qualsiasi lavoro a contatto con il pubblico, brilli: sai mettere la gente a proprio agio, e i bambini in particolare ti adorano. Anche in finanza potresti avere successo, perché la tua intuizione è formidabile. In amore, farai probabilmente un ottimo matrimonio, basato sulla fiducia e sulla comprensione reciproca. Sei esigente, ma anche generoso. La felicità è la tua compagna di viaggio, perché hai la chiave giusta: la gioia di vivere.",
                    'consiglio': "⚡ Il tuo amore è un arcobaleno: colorato, sorprendente, capace di apparire dopo la tempesta. La tua originalità è un dono. Continua a stupire, a innovare, a rendere ogni giorno speciale. La felicità non è una meta, è il modo in cui cammini. E tu sai camminare danzando."
                }
            },

            'venere_nettuno_trigono': {
                'trigono': {
                    'titolo': "❤️🌊 Venere in trigono con Nettuno",
                    'messaggio': "La tua anima è un'opera d'arte vivente. La tua sensibilità è così raffinata che percepisci bellezza dove altri vedono solo ordinario. Sei romantico, idealista, ma non vivi nelle nuvole: i tuoi piedi sono per terra, anche se il tuo cuore vola alto. Hai un talento artistico innato, e l'arte in tutte le sue forme è il tuo linguaggio naturale. La tua gentilezza è proverbiale: riesci a essere gentile anche con chi ti ha ferito, perché comprendi la fragilità umana. Quando l'ambiente è negativo, sai tenerti in disparte senza giudicare, aspettando tempi migliori. Teatro, danza, canto, insegnamento ai giovani: sono solo alcune delle tue possibili strade. Il tuo charme e la tua discrezione conquistano i superiori, che ti affidano responsabilità importanti. In amore, cerchi una persona in evoluzione, che come te rifugge dalla volgarità. Sei un idealista senza incertezze, e questo dà alla tua vita un significato profondo. Non sprecare il tuo talento: il mondo ha bisogno della tua bellezza.",
                    'consiglio': "🌊 Il tuo amore è una poesia scritta con inchiostro di stelle. La tua anima è un'opera d'arte. Non nascondere la tua bellezza interiore: condividila. La tua sensibilità è un dono raro. Illumina chi ti sta intorno con la tua arte, con la tua dolcezza, con il tuo amore."
                }
            },

            'venere_plutone_trigono': {
                'trigono': {
                    'titolo': "❤️🌋 Venere in trigono con Plutone",
                    'messaggio': "L'amore per te è un'esperienza totale, spirituale, trasformativa. Non ti accontenti di mezze misure: quando ami, ami con tutto te stesso, e questa tua intensità è magnetica. Sai aspettare la persona giusta, e intanto vivi relazioni leggere, senza bruciarti. Poi, quando incontri l'anima gemella, è un'esplosione di passione e spiritualità insieme. C'è un che di fatale in quell'incontro, come se fosse scritto nelle stelle. Hai il dono di trasmettere valori profondi, specialmente ai giovani, che riconoscono in te una guida autentica. Negli affari, la tua sincerità è un vantaggio: la gente compra da te perché si fida. Sei un ottimo consulente, in qualsiasi campo. Scegli lavori che rispettano il tuo codice morale: la tua integrità non è negoziabile. Potresti lavorare per il fisco o come esattore: nessuno ti fregherebbe, perché hai un fiuto infallibile per gli imbrogli. La vita ti ripagherà ampiamente, anche con eredità inaspettate. Il tuo amore per il mondo ti ritorna sotto forma di abbondanza.",
                    'consiglio': "🌋 Il tuo amore è un vulcano di passione e profondità. Quando ami, ami con tutto te stesso. Questa tua capacità di amare in modo assoluto è un dono raro. Usalo con saggezza, donalo a chi lo merita. La tua fedeltà è leggendaria, la tua intensità è unica."
                }
            },

            'venere_ascendente_trigono': {
                'trigono': {
                    'titolo': "❤️⬆️ Venere in trigono con l'Ascendente",
                    'messaggio': "Il tuo fascino è la tua firma. Hai modi concilianti, eleganti, che mettono la gente a proprio agio. Sai di piacere, e questa consapevolezza ti dà sicurezza, ma non diventi mai arrogante. Quando hai bisogno di un appoggio, sai chiederlo con garbo, e spesso lo ottieni. Ami ricevere regali, ma preferisci ricambiare con favori piuttosto che con oggetti: per te la relazione conta più della cosa. Se proprio devi fare un regalo, lo porti di persona, perché il gesto è importante. Sei diplomatico: eviti di parlare male di qualcuno, perché temi che il discorso possa tornare su di te. Sul lavoro, ti dai da fare più degli altri per conquistare i superiori, ma non per carrierismo: è il tuo modo di essere. Hai spesso una buona cultura, magari universitaria, e cerchi amici al tuo livello. Coltivi le amicizie utili, ma senza calcolo: la simpatia che provi è genuina. Il tuo fascino apre molte porte, ma sono le tue qualità interiori a tenerle aperte.",
                    'consiglio': "🦋 La tua grazia è una danza, il tuo fascino è una melodia. Il mondo è il tuo palcoscenico. Ma ricordati che la vera bellezza non è solo esteriore: è quella dell'anima che si dona senza calcolo. Usa il tuo fascino per costruire ponti, non per manipolare."
                }
            },

            # MARTE (trigoni)
            'marte_saturno_trigono': {
                'trigono': {
                    'titolo': "🔥⏳ Marte in trigono con Saturno",
                    'messaggio': "Sei uno che non spreca energie. Usi la tua forza con intelligenza, dosandola, e ottieni risultati senza stancarti inutilmente. Con i collaboratori sei paziente e tollerante, e quando vedi qualcuno in difficoltà, dai una mano senza farti pregare. Questa tua calma interiore ti permette di sopportare anche chi lavora senza entusiasmo, senza perdere le staffe. Come insegnante, saresti eccezionale: prendi a cuore i tuoi allievi e sai trasmettere loro passione. Oltre all'insegnamento, la legge, le esplorazioni, la carriera militare, l'ecologia sono campi per te. Tutto ciò che riguarda la conservazione e la preservazione ti è congeniale. Hai doti manageriali e puoi arrivare lontano. La gente si fida di te, si confida, chiede consiglio. In amore sei tradizionalista, quasi puritano: per te una relazione stabile si basa su valori ben più importanti del sesso. La famiglia, la comunità, il dovere: queste sono le tue priorità. E questa tua solidità è la tua forza.",
                    'consiglio': "⚖️ La tua forza è nella disciplina, la tua grandezza nella costanza. Sei come un atleta che si allena ogni giorno. Continua a costruire con pazienza. La vera forza non è quella che piega gli altri, ma quella che costruisce sé stessi."
                }
            },

            'marte_giove_trigono': {
                'trigono': {
                    'titolo': "🔥✨ Marte in trigono con Giove",
                    'messaggio': "Hai un equilibrio perfetto tra mente e corpo. La tua energia è ben distribuita, e raggiungi i tuoi obiettivi con una facilità che gli altri invidiano. Ma a volte, proprio per questa facilità, potresti decidere che non vale la pena impegnarsi. Peccato, perché hai una creatività fuori dal comune, capace di imprese straordinarie. La fortuna ti accompagna: sei nel posto giusto al momento giusto, e questo ti apre molte porte. Ma non ne approfitti in modo sleale: sei onesto e rispetti le regole. Forse anche troppo fiducioso: a volte ti fidi di persone che non lo meritano, e ci rimetti. Impieghi statali, sport, lavoro con i bambini, insegnamento, esplorazioni, artigianato, scrittura: tutto ti è possibile. Il successo in sé non ti interessa: a te basta un lavoro che ami, che ti dia soddisfazione. Sei amico di tutti, senza distinzioni, ma quando una relazione diventa troppo pesante, la lasci andare senza sensi di colpa. Le tue convinzioni religiose sono salde e semplici. In amore cerchi una persona che ami la vita tranquilla come te, e con cui condividere mente, cuore e corpo.",
                    'consiglio': "🏹 La tua energia è una freccia scoccata con grazia. La fortuna ti accompagna, ma non darle tutto il merito. Il mondo ha bisogno della tua leggerezza, del tuo ottimismo. Non sprecare il tuo dono nell'apatia. La vita è ora: vivila."
                }
            },

            'marte_urano_trigono': {
                'trigono': {
                    'titolo': "🔥⚡ Marte in trigono con Urano",
                    'messaggio': "Sei originale, creativa, e hai un modo di esprimerti che è tutto tuo. Quando qualcosa ti appassiona, non vedi l'ora di metterti all'opera, e niente ti ferma. La tua energia è inesauribile, la tua mente sempre in movimento. Soffri per chi è intrappolato in lavori ripetitivi che uccidono la creatività. Per te, un lavoro dalle 9 alle 5 sarebbe una condanna. Hai bisogno di libertà, di decisioni, di movimento. Le attività di gruppo in cui puoi guidare sono perfette per te: esplorazioni, ricerche, invenzioni, viaggi, ingegneria, politica. Ami le persone interessanti, innovative, che guardano al futuro. Attenzione però: la tua insofferenza per i ritmi altrui potrebbe isolarti. Impara a essere più tollerante con chi è più lento. E ricordati di riposare: ti vanti di non averne bisogno, ma il tuo corpo la pensa diversamente. In amore sei impulsivo e passionale. I vincoli tradizionali ti stanno stretti: preferisci una rete di amicizie stimolanti. E in fondo, un po' ti invidiano tutti, per la tua vita eccitante e fuori dagli schemi.",
                    'consiglio': "⚡ La tua energia è un razzo diretto verso nuove galassie. La tua originalità è il carburante. Ma anche i razzi hanno bisogno di soste. Impara a rallentare, a respirare. L'eterna corsa ti farà perdere la bellezza di ciò che hai già raggiunto."
                }
            },

            'marte_nettuno_trigono': {
                'trigono': {
                    'titolo': "🔥🌊 Marte in trigono con Nettuno",
                    'messaggio': "Hai il dono raro di unire azione e spiritualità. La tua forza non è al servizio dell'ego, ma della compassione. Sai soddisfare i tuoi desideri senza mai trascurare i tuoi doveri verso gli altri. Capisci i tuoi istinti più profondi, li controlli, e questa padronanza ti rende comprensivo verso chi non ci riesce. La gente si confida con te, perché sente che non giudichi. La tua intuizione è affilata: scopri l'insincerità al primo sguardo. Medicina, fisioterapia, assistenza sociale, legge: sono i tuoi campi. Hai doti di guaritore, e non solo del corpo: sai curare anche l'anima. La psicologia e le terapie di gruppo sono perfette per te. Oppure, se preferisci la ribalta, il teatro è la tua seconda pelle: la tua voce e la tua presenza scenica sono magnetiche. In amore sei tenero, dolce, e sai amare senza possedere. Se l'amore finisce, restituisci la libertà senza rancore, e spesso rimani amico. Il tuo magnetismo attrae la gente, e la tua compagnia è una gioia per chi ti ama.",
                    'consiglio': "🌊 La tua forza è al servizio della compassione. Sei un guerriero che ha deposto le armi per diventare guaritore. Questa tua capacità di unire azione e spiritualità è un dono raro. Continua a curare, a consolare, a sollevare. Il mondo ha bisogno di guerrieri di pace come te."
                }
            },

            'marte_plutone_trigono': {
                'trigono': {
                    'titolo': "🔥🌋 Marte in trigono con Plutone",
                    'messaggio': "La tua aggressività è al servizio delle cause giuste. Sai risolvere i problemi sociali più complessi perché capisci la radice del male. Sei pronta a offrire il tuo contributo, perché per te il servizio è un dovere. Ma attenzione: questa configurazione può anche portarti all'apatia, a farti da parte. Scegli tu da che parte stare. Per te il potere non è un fine, ma uno strumento per progredire. Sai che la vita è un cammino spirituale, e che ognuno ha i suoi tempi. Per questo sei tollerante con chi arranca: tendi una mano, ma non interferisci. Quando si tratta di difendere i tuoi diritti, sei impavida. Gli amici ti ammirano per il coraggio che mostri nelle difficoltà. Hai una riserva infinita di energia spirituale a cui attingere nei momenti bui. In amore sei ardente ma controllata. Vuoi una persona che ti ami in molti modi, non solo come amante. Per te l'amore fisico senza unione spirituale è vuoto.",
                    'consiglio': "🌋 La tua forza interiore è un vulcano di energia spirituale. Nei momenti di crisi, attingi a riserve che altri non hanno. Continua a combattere per ciò in cui credi. La pace interiore è la più grande delle vittorie."
                }
            },

            'marte_ascendente_trigono': {
                'trigono': {
                    'titolo': "🔥⬆️ Marte in trigono con l'Ascendente",
                    'messaggio': "La tua personalità si afferma con energia positiva. Sei un entusiasta, e il tuo entusiasmo è contagioso: la gente ti segue, ti appoggia, crede in te. A volte sbagli, ma non hai paura di rischiare, e la fortuna sembra premiarti. Hai una forte volontà e non aspetti il permesso per esprimerti. Sei un grande parlatore, ami le discussioni e le competizioni, e le sfide ti esaltano. Lo sport è il tuo sfogo preferito. Hai sempre bisogno di soldi per i tuoi divertimenti, e qualche volta architetti piani folli per procurarteli. Spendaccione cronico, dovresti imparare a moderarti. Il futuro non ti preoccupa: vivi alla giornata, e questo ti rende libero ma anche vulnerabile. Sul lavoro dai l'impressione di essere attivissimo, e i capi ti apprezzano. Peccato che quando serve, fatichi a dimostrare concretamente il tuo valore. La disciplina è la tua sfida: se la impari, il tuo entusiasmo creativo darà frutti straordinari. Sogni un'attività in proprio, ma i soldi finiscono sempre prima.",
                    'consiglio': "⚡ La tua energia è un fuoco che illumina. La tua spontaneità è un dono. Ma senza disciplina si disperde. Scegli una meta, una sola, e perseguila con costanza. I risultati ti sorprenderanno. La pazienza non è nemica dell'entusiasmo, è la sua guida."
                }
            },

            # GIOVE (trigoni)
            'giove_saturno_trigono': {
                'trigono': {
                    'titolo': "✨⏳ Giove in trigono con Saturno",
                    'messaggio': "Hai la saggezza di chi sa unire le lezioni del passato ai progetti per il futuro. Il successo non ti coglie mai impreparato, perché sai di averlo costruito con le tue mani. La gente ti vede come una persona ispirata, ma tu sai che dietro ogni successo c'è un lavoro paziente di raccolta di informazioni e di valutazione dei dettagli. Non corri rischi inutili: quando agisci, hai già calcolato tutto. La tua fiducia in te stesso è solida, e non sprechi tempo in cose insignificanti. Giurisprudenza, consulenze finanziarie, fisioterapia, insegnamento, sacerdozio: sono i tuoi campi. La tua ispirazione, specialmente in ambito religioso, è drammatica ed efficace. Sei tollerante con gli incompetenti, ma attenzione a non cadere nell'apatia. Perché il tuo potenziale è enorme: puoi essere il catalizzatore che risveglia il talento negli altri. Se scegli di stare lontano dalla mischia, puoi dedicarti ai giovani o al tempo libero, e il tuo contributo sarà comunque prezioso.",
                    'consiglio': "🏛️ La tua vita è un tempio costruito con le pietre del passato e le finestre aperte sul futuro. La tua saggezza è antica, la tua visione è moderna. Continua a costruire con pazienza. Il tuo esempio è una guida per chi non sa da che parte andare."
                }
            },

            'giove_urano_trigono': {
                'trigono': {
                    'titolo': "✨⚡ Giove in trigono con Urano",
                    'messaggio': "La tua creatività è immensa e sai come usarla. La tua mente è rapida, cogli le occasioni al volo, e la fortuna ti assiste. Ottieni risultati che altri, con le stesse capacità, non raggiungono. Insegnamento, legge, politica, religione: in questi campi puoi brillare senza sforzo. Hai un rapporto speciale con i giovani: li capisci, ti fidano, e sai guidarli con intuizione. La libertà è sacra per te: non sopporti chi cerca di imprigionarti. I viaggi ti aprono la mente e ti arricchiscono. Sei affettuoso con gli amici, e il tuo amore si estende a tutta l'umanità, nemici compresi. Il tuo ottimismo è incrollabile, e aiuti chi ne ha bisogno. I pessimisti cronici, invece, ti sono insopportabili. In amore, la persona che scegli deve essere onesta, e tu le dai in cambio forza spirituale, integrità e altruismo. Un rapporto così è solido e vero.",
                    'consiglio': "⚡ La tua mente è un razzo diretto verso il futuro. La tua creatività è il carburante. Continua a sognare in grande, ma ricordati che ogni idea ha bisogno di azione. Trasforma i sogni in progetti, e i progetti in opere. Il futuro si costruisce con le mani."
                }
            },

            'giove_nettuno_trigono': {
                'trigono': {
                    'titolo': "✨🌊 Giove in trigono con Nettuno",
                    'messaggio': "La tua anima è un oceano di saggezza e compassione. Comprendi la vita e gli esseri umani a un livello che pochi raggiungono. Vedi il bene dove altri vedono il male, l'ordine dove altri vedono il caos. Questa tua visione è un dono prezioso per l'umanità. Dovresti metterla al servizio degli altri: programmi sociali, assistenza, insegnamento, arte, religione, scrittura. Hai un profondo rispetto per la spiritualità, e puoi aiutare chi è smarrito a ritrovare la via. L'occulto ti affascina, e hai facoltà psichiche notevoli. La moda e l'arte sono altri tuoi possibili sbocchi. In amore, la tua natura raffinata cerca persone dolci e spirituali. Non ti accontenteresti mai di una relazione puramente fisica. Per te, l'amore è unione di anime.",
                    'consiglio': "🌊 La tua anima è un oceano di saggezza. La tua visione del mondo è un dono per chi si è perso. Continua a contemplare, a ispirarti, a servire. Ma ricordati: la contemplazione senza azione è vuota. Trasforma la tua visione in opere concrete."
                }
            },

            'giove_plutone_trigono': {
                'trigono': {
                    'titolo': "✨🌋 Giove in trigono con Plutone",
                    'messaggio': "Hai il dono di risvegliare il potenziale creativo nelle persone e nei gruppi. Vedi i cambiamenti sociali con ottimismo, perché sai che porteranno a un futuro migliore. Afferri il senso profondo della vita e sai comunicarlo anche agli scettici. Il tuo destino è di essere coinvolto nelle vite altrui, e per questo dovresti scegliere un lavoro di pubblica utilità. L'insegnamento è perfetto: puoi aiutare gli altri a liberarsi dalle illusioni e a crescere. Forse sei un'anima antica, venuta per servire. Nelle relazioni, hai bisogno di libertà. Distingui il bene dal male per istinto, e questo ti rende una guida preziosa. I giovani sono affascinati da te, perché sentono che capisci i loro drammi. Anche gli adulti traggono beneficio dalla tua vitalità. La tua presenza è un dono per chi ti incontra.",
                    'consiglio': "🌋 La tua anima è una guida per chi cerca la verità. La tua capacità di vedere oltre le apparenze è un dono raro. Continua a illuminare il cammino degli altri. Ma ricordati: ogni maestro è anche un eterno apprendista. Non smettere mai di cercare."
                }
            },

            'giove_ascendente_trigono': {
                'trigono': {
                    'titolo': "✨⬆️ Giove in trigono con l'Ascendente",
                    'messaggio': "Hai la certezza interiore che riuscirai. Questa fiducia ti spinge a elaborare progetti grandiosi, convinto che la tua creatività sia già una garanzia di successo. Ma a volte questa sicurezza gioca contro di te: pensi di poter fare tutto senza sforzo, e invece i risultati non arrivano. Ami la bella vita, le comodità, e sei disposto a lavorare per ottenerle. Ma in fondo al cuore temi di non farcela nella competizione. I tuoi superiori ti stimano più di quanto tu creda, perché fai più del dovuto per piacere. Ammiri chi ce l'ha fatta e vuoi emularli, ma prima devi imparare l'autodisciplina. Sei un po' troppo incline ai piaceri e poco attento ai soldi, e questo ti fa perdere occasioni. I tuoi talenti sono tanti, ma senza programmi si disperdono. Sii più riservato con le tue idee: non tutti sono onesti. E impara a gestire il denaro, perché le mani bucate ti mettono nei guai.",
                    'consiglio': "✨ Il tuo ottimismo è una benedizione. Ma ricordati che anche il terreno più fertile ha bisogno di cure. Non basta sognare, bisogna programmare. La disciplina non è nemica della libertà, è la sua migliore alleata. Dai forma concreta ai tuoi sogni."
                }
            },

            # SATURNO (trigoni)
            'saturno_urano_trigono': {
                'trigono': {
                    'titolo': "⏳⚡ Saturno in trigono con Urano",
                    'messaggio': "Impari dalle esperienze e sai integrare la disciplina nella tua vita senza sentirti oppresso. Hai un sano equilibrio tra rispetto per la tradizione e apertura al nuovo. I beni materiali li apprezzi, ma con gli anni ti ci affezioni sempre meno, perché capisci cosa conta davvero. Conosci le tue potenzialità e le usi con saggezza. Il successo per te non è una questione di colpi di fortuna, ma di prudenza e capacità di valutare i rischi. Sei un manager nato: hai intuito e giudizio, e sai leggere dentro le persone. I giovani riconoscono la tua autorità perché non è arrogante, ma autentica. Matematica, scienze, ricerca, astrologia, industria: in questi campi puoi esprimere al meglio le tue doti organizzative e di comando.",
                    'consiglio': "⚖️ La tua vita è un equilibrio perfetto tra tradizione e innovazione. Sei come un albero con radici profonde e rami protesi al cielo. Continua a crescere senza paura. La tua saggezza è un dono prezioso per chi cerca orientamento nel caos."
                }
            },

            'saturno_nettuno_trigono': {
                'trigono': {
                    'titolo': "⏳🌊 Saturno in trigono con Nettuno",
                    'messaggio': "Hai il coraggio di assumerti responsabilità enormi, spinte da una profonda motivazione spirituale. Vuoi cambiare le condizioni sociali negative, e questo desiderio nasce da un'etica alta che ti è stata inculcata nell'infanzia. La tua compassione è attiva: non ti limiti a sentire, fai. Sai individuare cosa deve essere migliorato e perché. Hai anche il dono di saperti rivolgere alle autorità competenti, perché conosci i meccanismi burocratici. Certo, potresti anche scegliere di startene in disparte, ma sarebbe un peccato. Nel lavoro porti integrità e saggezza. Cinema, fotografia, legge, servizi sociali, finanza: sono i tuoi campi. Scrivi bene, sai dare forma alle idee. La tua esperienza unita alla conoscenza ti rende in grado di risolvere qualsiasi problema.",
                    'consiglio': "🌊 La tua anima è un ponte tra mondo materiale e spirituale. La tua capacità di unire responsabilità e compassione è rara. Continua a costruire ponti, a tendere mani. La tua integrità è un faro in un mondo di compromessi."
                }
            },

            'saturno_plutone_trigono': {
                'trigono': {
                    'titolo': "⏳🌋 Saturno in trigono con Plutone",
                    'messaggio': "Hai una concentrazione e una capacità organizzative fuori dal comune. Vedi le cose in modo realistico e sei fedele al dovere. Sai ottenere il massimo dal lavoro e accetti le responsabilità che la società ti affida. I cambiamenti sociali non ti spaventano: li capisci e collabori perché siano produttivi. Qualsiasi lavoro richieda manager, tenacia, determinazione è per te. Grandi complessi industriali o finanziari sono il tuo ambiente. Non tolleri ostruzionismi e collaboratori che creano difficoltà. Puoi ambire a posizioni statali per avere voce in capitolo. La tua efficienza è tale che anche i colleghi meno motivati si sentono spinti a fare meglio. Sai distinguere l'utile dal superfluo e potresti fare grandi cose per la collettività. Hai il dono di risvegliare l'interesse della gente, specialmente dei giovani, per la cosa pubblica.",
                    'consiglio': "🌋 La tua forza è nella visione a lungo termine, la tua grandezza nel trasformare il potere in servizio. Continua a costruire con visione, a pianificare con saggezza. Il mondo ha bisogno di leader come te, che sanno che il vero potere è responsabilità."
                }
            },

            'saturno_ascendente_trigono': {
                'trigono': {
                    'titolo': "⏳⬆️ Saturno in trigono con l'Ascendente",
                    'messaggio': "Senti il peso delle responsabilità e sai che il successo si conquista con il lavoro. Non ti aspetti regali dalla vita. Probabilmente i tuoi genitori non ti hanno aiutato economicamente, ma ti hanno insegnato a stare in piedi da solo, e gliene sei grato. Sei tradizionalista e cerchi lavori sicuri. Il tuo obiettivo è una posizione stabile, economicamente solida. Ti piace che si sappia che ti sei fatto da solo. Hai pochi amici, ma leali, e durano tutta la vita. In amore non cerchi avventure: meglio soli che male accompagnati. Prima di impegnarti, devi conoscere a fondo una persona, specialmente i suoi valori morali. Il sesso senza amore non ha senso per te. Ma attenzione: il tuo isolamento ti priva di contatti umani preziosi. Cerca di abbattere le barriere che costruisci intorno a te. La comunicazione è importante, e l'incapacità di comunicare è improduttiva.",
                    'consiglio': "🏔️ La tua vita è una scalata verso la vetta. La tua indipendenza è la tua forza, ma a volte diventa isolamento. Impara ad aprirti, a fidarti. La vetta è più bella se condivisa. Non aver paura di mostrare le tue emozioni: non sono debolezza, sono umanità."
                }
            },

            # URANO (trigoni)
            'urano_nettuno_trigono': {
                'trigono': {
                    'titolo': "⚡🌊 Urano in trigono con Nettuno",
                    'messaggio': "Non accetti le idee tradizionali senza prima averle vagliate con la tua mente. Vuoi essere libero di decidere cosa credere e cosa no. Per te la verità è importante, non l'illusione. Sai che gli ideali possono cambiare il destino delle persone, e per questo li prendi sul serio. Conosci la storia, sai come le masse sono state manipulate da ideologie imposte. Questa configurazione è nata in un periodo storico drammatico (1938-1944), quando i dittatori ipnotizzavano le folle. Tu hai il dono di riconoscere la disonestà e le illusioni. È tuo dovere usare questo dono per risvegliare le coscienze e combattere la corruzione politica. Non stare in silenzio: la tua voce può fare la differenza.",
                    'consiglio': "🔮 La tua visione abbraccia passato e futuro. Sei un veggente in un mondo di ciechi. Non tacere la verità che vedi. Il mondo ha bisogno della tua lucidità. Parla, agisci, risveglia le coscienze. La storia non si ripete se qualcuno ha il coraggio di spezzare il ciclo."
                }
            },

            'urano_plutone_trigono': {
                'trigono': {
                    'titolo': "⚡🌋 Urano in trigono con Plutone",
                    'messaggio': "Sei aperto al cambiamento e sai adattarti ai nuovi sviluppi sociali. Sostieni le riforme necessarie quando le condizioni richiedono di evolvere. Le idee tradizionali che inibiscono la creatività non fanno per te. Sai che il progresso richiede aggiustamenti continui, e per questo ti ribelli allo status quo. Sei nato nei ruggenti anni venti, un periodo di grandi trasformazioni in cui vennero piantati semi importanti: la psicologia del profondo, le teorie dell'evoluzione. Tu godi dei frutti di quel periodo e hai vedute più ampie delle generazioni precedenti. Cerchi il significato profondo della vita, al di là del materialismo. L'occulto ti affascina, e credi nelle infinite potenzialità della mente umana liberata dai condizionamenti. Non hai paura di esplorare la psiche. E sei disposto a condividere le tue scoperte per il bene dell'umanità.",
                    'consiglio': "🌋 La tua mente è un esploratore di nuovi mondi. La tua apertura al cambiamento è il tuo dono più grande. Continua a esplorare, a sperimentare. Ma ogni scoperta ha senso solo se condivisa. Sii ponte, non isola. La consapevolezza collettiva passa attraverso la condivisione."
                }
            },

            'urano_ascendente_trigono': {
                'trigono': {
                    'titolo': "⚡⬆️ Urano in trigono con l'Ascendente",
                    'messaggio': "Hai doti creative notevoli, ma hai bisogno di autodisciplina per svilupparle appieno. La tua privacy è sacra: non sopporti intrusioni. Devi essere libero di agire come credi. Le preoccupazioni non ti assillano, perché sai che quando serve, troverai una soluzione. I pensieri negativi non ti sfiorano. Non sei schiavo dell'orologio: vivi a modo tuo, indipendente. Ti prendi tutti i piaceri che la vita offre, anche i più stravaganti. La tua mente è un vulcano di idee ingegnose, ma non cerchi la fama. In amore, hai bisogno di una persona intelligente e originale, altrimenti ti annoi. Sei convinto di essere importante per chi ti sta intorno, e forse è vero: le persone che ti amano a volte si sentono un po' soffocate dalle tue premure. Ma la cosa incredibile è che capisci gli altri meglio di quanto essi stessi si capiscano. E sei felice quando vedi le nuove generazioni affermare la propria personalità, libere dalle convenzioni.",
                    'consiglio': "⚡ La tua mente è un laboratorio di idee geniali. La tua indipendenza è la tua bandiera. Continua a pensare con la tua testa, a innovare. Ma ricordati che l'originalità fine a se stessa è solo eccentricità. Usa il tuo dono per connettere, non per separare. La vera genialità è quella che serve agli altri."
                }
            },

            # NETTUNO (trigoni)
            'nettuno_ascendente_trigono': {
                'trigono': {
                    'titolo': "🌊⬆️ Nettuno in trigono con l'Ascendente",
                    'messaggio': "La tua sensibilità è così profonda che a volte fatichi a trovare relazioni soddisfacenti. Cerchi l'amore ideale, l'amicizia perfetta, e tendi a idealizzare le persone, per poi soffrire quando ti deludono. Invece di rimuginare, dovresti concentrare le tue energie creative sulla tua immaginazione fertile. Hai il dono di trasformare i pensieri in azioni ispirate: usalo! L'arte può essere la tua salvezza e la tua realizzazione. All'inizio magari non guadagnerai, ma col tempo diventerai un professionista. Anche il lavoro con bambini e adolescenti può darti grandi soddisfazioni. Attenzione agli amici che potrebbero approfittare della tua disponibilità. Metti in luce i tuoi doni spirituali e creativi, e persevera nonostante le delusioni. La tua strada è quella dell'espressione artistica e del servizio agli altri.",
                    'consiglio': "🎨 La tua anima è un artista che dipinge mondi di bellezza. La tua sensibilità è il pennello. Non lasciare che le delusioni ti facciano smettere di dipingere. Ogni opera d'arte nasce dalla sofferenza trasformata in bellezza. Continua a creare, a sognare, a condividere."
                }
            },

            # PLUTONE (trigoni)
            'plutone_ascendente_trigono': {
                'trigono': {
                    'titolo': "🌋⬆️ Plutone in trigono con l'Ascendente",
                    'messaggio': "Hai risorse interiori immense. Quando vuoi qualcosa, non c'è niente che non possa fare. La sicurezza nelle tue idee è tale che ottieni appoggi senza fatica. Il passato ti interessa solo per le sue lezioni: il tuo sguardo è sempre al futuro. La mancanza di soldi non è una scusa per te: se vuoi qualcosa, trovi il modo. Le tue idee si trasformano in realtà con ingegno. Riconosci i tuoi difetti e lavori per cambiarli. Ammiri chi si fa una cultura, perché per te l'ignoranza non è una scusa: la cultura è accessibile a tutti. Affronti rivali e concorrenti con correttezza. Sai come aiutare i collaboratori, ma attento a non essere presuntuoso: molti si farebbero strada anche senza di te. Dare una mano è lodevole, ma intromettersi continuamente è fastidioso.",
                    'consiglio': "🌋 La tua forza interiore è una miniera di tesori. La tua capacità di trasformare idee in realtà è leggendaria. Continua a creare, a costruire. Ma ricordati che la vera grandezza non sta nel potere sugli altri, ma nel potere con gli altri. L'umiltà è la chiave che apre tutte le porte."
                }
            },

            # ============================================
            # MESSAGGI PER I QUINCONCE RADIX
            # ============================================

            # SOLE (quinconce)
            'sole_luna_quinconce': {
                'quinconce': {
                    'titolo': "☀️🌙 Sole in quinconce con la Luna",
                    'messaggio': "C'è un conflitto interiore tra i tuoi legami affettivi e la tua volontà di esprimerti. Le tue emozioni profonde e i tuoi desideri consapevoli non vanno d'accordo, e questo crea una tensione che si riversa su tutte le tue relazioni. Hai un bisogno quasi ossessivo di essere accettato, e per questo tendi a fare più concessioni del necessario, a caricarti di obblighi verso gli altri da cui poi fatichi a liberarti. La gente potrebbe persino pensare che ti piaccia essere sfruttato, tanto sembri cercare situazioni in cui puoi sacrificarti. In realtà hai solo un grande desiderio di essere utile, ma spesso lo fai a tue spese. Forse dovresti incanalare questa tua generosità in un lavoro di aiuto agli altri, dove la tua dedizione potrebbe essere apprezzata e anche remunerata. La salute risente di questo continuo stress, e in amore tendi a idealizzare chi ami, per poi soffrire quando scopri che non è come lo immaginavi.",
                    'consiglio': "🔄 Non puoi riempire gli altri se prima non riempi te stesso. Impara a proteggere i tuoi confini e a dire di no. La persona giusta ti amerà per quello che sei, non per quello che fai per lei."
                }
            },

            'sole_marte_quinconce': {
                'quinconce': {
                    'titolo': "☀️🔥 Sole in quinconce con Marte",
                    'messaggio': "La tua energia è tanta, ma spesso la sprechi con le persone sbagliate. Ti butti a capofitto in qualsiasi impresa, desideroso di dimostrare quanto vali, e finisci per attirare chi approfitta della tua buona volontà. Sei più competente di quanto credi, ma la mancanza di fiducia in te stesso ti porta a cercare l'approvazione degli altri attraverso favori e prestazioni gratuite. I colleghi meno capaci di te ti sfruttano, e tu accumuli delusioni. Solo quando qualcuno ti cercherà per le tue reali competenze, offrendoti un giusto compenso, ti renderai conto del tuo valore. Hai talento in molti campi, dalla ricerca alla fisioterapia, dall'artigianato alla diagnostica. In amore tendi a sminuirti, ma chi sa vedere oltre capisce la tua serietà. Attenzione a chi potrebbe rubare le tue idee.",
                    'consiglio': "⚡ La tua energia è un tesoro, non sprecarla con chi non la merita. Impara a riconoscere il tuo valore prima di pretendere che lo riconoscano gli altri. Non servire chi ti usa, scegli chi ti apprezza."
                }
            },

            'sole_giove_quinconce': {
                'quinconce': {
                    'titolo': "☀️✨ Sole in quinconce con Giove",
                    'messaggio': "Cerchi disperatamente sicurezza e indipendenza, ma non sai bene come ottenerle. Così ti aggrappi all'approvazione degli altri, sperando che le loro lodi ti diano quella fiducia che ti manca. Sei un lavoratore instancabile, sempre pronto a studiare e specializzarti per essere all'altezza di ogni situazione. Il problema è che fai anche il lavoro dei colleghi, ti assumi responsabilità che non ti competono, e poi ti senti sfruttato. Non ti senti mai abbastanza apprezzato, mai pagato abbastanza. In amore dai molto più di quanto ricevi, e la salute ne risente con disturbi digestivi. Hai bisogno di riposo, di staccare, di dormire. E di smetterla di cercare fuori quella sicurezza che devi costruire dentro.",
                    'consiglio': "📚 La conoscenza è importante, ma la saggezza lo è ancora di più. Non cercare fuori la sicurezza che devi costruire dentro. Studia, certo, ma impara anche a proteggerti, a dire no, a pretendere rispetto. Il tuo valore non dipende dai ringraziamenti degli altri."
                }
            },

            'sole_saturno_quinconce': {
                'quinconce': {
                    'titolo': "☀️⏳ Sole in quinconce con Saturno",
                    'messaggio': "Hai imparato fin da piccolo a fare favori a tutti, a renderti utile, a non dire mai di no. Ora che sei adulto, questo atteggiamento ti perseguita. Subisci gli abusi degli altri senza reagire, accetti lavori di secondo piano senza possibilità di carriera, e i superiori nemmeno ti notano. Forse dentro di te pensi di meritartelo, come se dovessi scontare una colpa. In realtà è solo mancanza di fiducia e paura del conflitto. Devi imparare a decidere cosa vuoi davvero, a fare progetti e a seguirli con determinazione. La salute intanto soffre: disturbi digestivi, circolatori, tensione continua. Impara a rilassarti e a metterti al primo posto ogni tanto.",
                    'consiglio': "⏳ La tua umiltà è una virtù, ma non deve diventare una prigione. Non sei qui per servire tutti, sei qui per vivere la tua vita. Impara a riconoscere i tuoi desideri, a dare priorità ai tuoi bisogni. La salute è il bene più prezioso: senza di essa, non puoi aiutare nessuno."
                }
            },

            'sole_urano_quinconce': {
                'quinconce': {
                    'titolo': "☀️⚡ Sole in quinconce con Urano",
                    'messaggio': "Cedi sempre. Basta che qualcuno ti dica che sei l'unico di cui può fidarsi, e tu molli tutto pur di aiutarlo. Poi ci rimani male, ti senti usato, ma la volta dopo ricomincia tutto da capo. Il senso di colpa se rifiuti è più forte della rabbia che provi quando ti sfruttano. Anche al lavoro i colleghi approfittano di te, chiedendo favori e pretendendo il tuo aiuto. E tu non sai dire di no. Sei portato per l'insegnamento, la fisioterapia, i lavori indipendenti dove puoi decidere da solo. In amore attiri persone esigenti che pretendono continue attenzioni. Impara a stare fermo, a lasciare che siano gli altri a fare il primo passo. L'amore vero si dimostra da solo.",
                    'consiglio': "⚡ La tua generosità è ammirevole, ma non deve diventare una debolezza. Impara a distinguere chi ha davvero bisogno da chi vuole solo approfittarsi. La tua libertà interiore vale più di qualsiasi approvazione. Non lasciare che i sensi di colpa decidano per te."
                }
            },

            'sole_nettuno_quinconce': {
                'quinconce': {
                    'titolo': "☀️🌊 Sole in quinconce con Nettuno",
                    'messaggio': "Hai l'anima del martire. Ti senti responsabile di tutti i problemi del mondo, e quando qualcuno ti dice che solo tu puoi risolverli, ci credi ciecamente. Ti perdi in dettagli inutili, esageri l'importanza di cose banali, e il successo ti sfugge. Dovresti pensare di più a te stesso, sviluppare i tuoi talenti creativi. Sei portato per l'assistenza sociale, l'ospedale, le terapie di gruppo, la ricerca medica. Ma attenzione: ti leghi sempre a persone che hanno bisogno di te, e quando sei tu ad aver bisogno non trovi nessuno. Non sei il confessore di nessuno, non è tuo dovere morale salvare il mondo. La tua salute soffre di questo continuo stress emotivo.",
                    'consiglio': "🌊 La tua compassione è un oceano, ma anche l'oceano ha bisogno di rive. Impara a tracciare confini, a proteggere la tua costa. Non devi salvare il mondo da solo. La tua sensibilità è un dono, ma va custodita. Non lasciare che gli altri ti svuotino."
                }
            },

            'sole_plutone_quinconce': {
                'quinconce': {
                    'titolo': "☀️🌋 Sole in quinconce con Plutone",
                    'messaggio': "Ti carichi dei doveri che altri rifiutano, e lo fai con amarezza, ma lo fai. Come se dovessi dimostrare qualcosa, come se avessi una colpa da scontare. Invidichi chi ha potere e posizione, e ti sforzi di attirare la loro ammirazione. Intanto trascuri le tue potenzialità, le tue ambizioni. Forse dovresti diventare un po' più egoista, concentrarti su di te, capire cosa vuoi davvero. I tuoi sforzi, se ben organizzati, possono portarti al successo. Ma devi smetterla di disperderti in mille rivoli, di affrontare battaglie per cui non sei pronto. La tensione che accumuli si riversa sulla salute. Impara a rilassarti, a scegliere le tue battaglie con cura.",
                    'consiglio': "🌋 La tua forza è immensa, ma dispersa. Concentrala come un laser: solo così potrà tagliare le rocce. Non devi dimostrare nulla a nessuno, se non a te stesso. Il tuo valore non dipende da quanto ti sacrifichi per gli altri. Scegli le tue battaglie, combattile con intelligenza."
                }
            },

            'sole_ascendente_quinconce': {
                'quinconce': {
                    'titolo': "☀️⬆️ Sole in quinconce con l'Ascendente",
                    'messaggio': "Sei un perfezionista instancabile. Lavori nell'ombra, cercando di fare tutto alla perfezione, sperando che qualcuno se ne accorga e ti dia il giusto riconoscimento. Hai seguito i consigli dei tuoi genitori, hai studiato, ti sei specializzato, e ora sei un vero esperto nel tuo campo. Ma ti sottovaluti, non sei mai contento, vuoi sempre di più. Pretendi di essere pagato per il tuo giusto valore, e giustamente, ma questo tuo rigore ti logora. Gli amici ti cercano per i tuoi favori, ti adulano, e tu non sai dire di no. Concediti delle pause, dimentica le responsabilità ogni tanto. La vita non è solo dovere, è anche piacere.",
                    'consiglio': "🌟 La tua dedizione è ammirevole, ma la perfezione è un'illusione. Non serve a nulla essere i migliori se poi non ti godi i frutti del tuo lavoro. Impara a staccare, a respirare, a essere imperfetto ogni tanto. La vita non è solo dovere, è anche piacere."
                }
            },

            # LUNA (quinconce)
            'luna_mercurio_quinconce': {
                'quinconce': {
                    'titolo': "🌙💬 Luna in quinconce con Mercurio",
                    'messaggio': "Il cuore e la mente sono in continuo conflitto. Reagisci sempre d'impulso, con le emozioni, e solo dopo ti accorgi che avresti dovuto ragionare. Vedi offese e critiche dappertutto, anche dove non ci sono, e rispondi in modo sproporzionato. La gente ti evita, e tu ti senti in colpa, ma ci ricadi sempre. Hai un bisogno irrefrenabile di essere utile, ma quando offri aiuto lo fai in modo così invadente che invece di ringraziamenti ottieni critiche. Forse è meglio che ti occupi dei fatti tuoi. Se vuoi aiutare, fallo in modo professionale, con un lavoro che lo richieda. Ma limita i tuoi compiti, non fare anche quelli degli altri. In amore, fai di tutto per essere desiderato, ma rischi di essere usato. Impara ad aspettare che sia l'altro a dimostrare interesse.",
                    'consiglio': "🧠 Il tuo cuore parla prima della tua mente, e spesso dice cose sbagliate. Impara a fare una pausa tra lo stimolo e la reazione. Respira, conta fino a dieci, poi agisci. La tua sensibilità è un dono, ma senza il freno della ragione diventa una condanna."
                }
            },

            'luna_venere_quinconce': {
                'quinconce': {
                    'titolo': "🌙❤️ Luna in quinconce con Venere",
                    'messaggio': "Metti sempre i bisogni degli altri davanti ai tuoi. Sembra che tu voglia comprarti l'affetto delle persone con la tua disponibilità. E in effetti loro approfittano, perché è comodo. Poi però ti lamenti, ti senti usato, ma continui a comportarti allo stesso modo. Al lavoro, i colleghi ti scaricano addosso i loro compiti. In amore, attiri persone che pretendono continue dimostrazioni d'affetto. Devi imparare a dire no, a mettere confini, a pretendere rispetto. E attenzione al denaro: prestare soldi agli amici significa perderli. Quando lavori per gli altri, chiedi un compenso adeguato. La gente pensa che tu faccia tutto gratis, e tu glielo lasci credere.",
                    'consiglio': "💖 La tua generosità è bella, ma non deve diventare ingenuità. Non devi comprare l'affetto di nessuno: chi ti ama lo fa gratis. Impara a distinguere chi merita il tuo tempo e chi no. Metti confini chiari, pretendi rispetto. Il tuo cuore è prezioso: non sprecarlo."
                }
            },

            'luna_marte_quinconce': {
                'quinconce': {
                    'titolo': "🌙🔥 Luna in quinconce con Marte",
                    'messaggio': "Non sai difenderti. Stringi amicizie con persone che puntualmente si approfittano di te, e quando lo scopri non hai il coraggio di mandarle via. Sopporti, incassi, e poi sfoghi la rabbia su tutti, anche su chi non c'entra. Dentro di te c'è una guerra tra il desiderio di essere buono e la rabbia per come ti trattano. Sei versatile e puoi fare molti lavori, ma attento al lavoro di gruppo: potresti fare tutto tu e altri prendersi i meriti. Meglio lavorare da solo, anche se ti chiamano egoista. La salute soffre: digestione, intestino, nervi. Meglio perdere qualche falso amico che rovinarsi la salute. Impara a valutare bene chi merita il tuo aiuto.",
                    'consiglio': "🔥 La tua energia è preziosa, non sprecarla in battaglie che non ti appartengono. Impara a dire no senza sensi di colpa. Non sei responsabile della felicità di tutti. Proteggi la tua salute, il tuo tempo, la tua pace. Chi ti vuole bene rispetterà i tuoi confini."
                }
            },

            'luna_giove_quinconce': {
                'quinconce': {
                    'titolo': "🌙✨ Luna in quinconce con Giove",
                    'messaggio': "Fai fatica a capire il senso di quello che ti succede. La vita ti sembra una sequenza di eventi confusi, e tu ti senti sempre inadeguato, sempre meno bravo degli altri. Così accetti ruoli di secondo piano, servi, ubbidisci, e non hai mai il coraggio di mandare via chi ti disturba. Ma un giorno scoprirai che anche tu hai qualcosa da dire, e allora le cose cambieranno. Puoi essere utile in molti modi senza trascurare te stesso: fisioterapia, riabilitazione, viaggi, relazioni pubbliche. In questi campi puoi dare il meglio. Hai bisogno di hobby che sviluppino il tuo potenziale, ma fallo solo se ti senti ben accetto, non per obbligo.",
                    'consiglio': "✨ La tua generosità è infinita, ma anche l'oceano ha bisogno di essere riempito dalle piogge. Non dare solo, ricevi anche. Non servire solo, lasciati servire. Il tuo valore è immenso, ma devi riconoscerlo tu per primo. Trova un equilibrio tra dare e ricevere."
                }
            },

            'luna_saturno_quinconce': {
                'quinconce': {
                    'titolo': "🌙⏳ Luna in quinconce con Saturno",
                    'messaggio': "Ti senti sempre inadeguato, in debito, come se dovessi dimostrare qualcosa a tutti. Forse è l'educazione che hai ricevuto, quei genitori che ti hanno fatto sentire inferiore. Ora, da adulto, continui a comportarti come se gli altri avessero il diritto di approfittare di te. Accetti ruoli subordinati, lavori senza prospettive, e non sai ribellarti. Eppure hai delle qualità: memoria, responsabilità, costanza. Potresti fare strada nell'insegnamento, nella politica, nella medicina. In amore, all'inizio sarà difficile, ma se impari a volerti bene le cose cambieranno. Vuoi essere amato, ma per esserlo devi prima imparare a rispettarti.",
                    'consiglio': "⏳ La tua umiltà è una virtù, ma non deve diventare autolesionismo. Non sei inferiore a nessuno. I tuoi limiti sono solo nella tua testa. Impara a vedere il tuo valore, a pretendere rispetto. Le relazioni sane sono fatte di reciprocità, non di sacrificio. Meriti amore, non sfruttamento."
                }
            },

            'luna_urano_quinconce': {
                'quinconce': {
                    'titolo': "🌙⚡ Luna in quinconce con Urano",
                    'messaggio': "La tua vita è una sequenza di crisi. Non appena ne risolvi una, subito se ne presenta un'altra. Ti sembra di non avere mai pace, di essere sempre in balia degli eventi. Queste difficoltà vengono da lontano, dall'infanzia, da pesi che ti hanno messo sulle spalle quando non eri pronto. Ora, da adulto, puoi liberarti. Scegli un lavoro in cui puoi aiutare gli altri: insegnamento, medicina, ricerca. Questo ti aiuterà a sciogliere i nodi. Ma attenzione alle persone che ti dicono di non poter fare a meno di te: vogliono solo dominarti. La tua resistenza nervosa non è infinita. Il riposo non è un optional, è una necessità. In amore, rischi di finire in relazioni di sottomissione da cui speri di uscire sposandoti. Non funziona così: la libertà viene da dentro.",
                    'consiglio': "⚡ La libertà che cerchi è dentro di te, non fuori. Non sono gli altri a tenerti prigioniero, sono le tue paure. Affrontale una a una, senza fretta. Impara a rilassarti, a respirare, a lasciar andare. La vita non è un'emergenza continua. La pace che cerchi è già qui."
                }
            },

            'luna_nettuno_quinconce': {
                'quinconce': {
                    'titolo': "🌙🌊 Luna in quinconce con Nettuno",
                    'messaggio': "Hai un cuore grande, troppo grande. Proteggi tutti come una chioccia, ti fai carico dei problemi di chiunque, e la tua immaginazione lavora sempre per trovarti nuove preoccupazioni. Al lavoro fai più del dovuto, e i colleghi ti guardano male. Sei portato per la medicina, l'assistenza sociale, la consulenza giovanile. Ma devi imparare a stabilire dei limiti, perché il tuo fisico non regge sforzi infiniti. In amore, idealizzi le persone, vedi qualità che non hanno, e quando scopri la verità soffri come un dannato. Impara a conoscere davvero le persone prima di innamorarti. Sei un romantico, e l'arte può darti la gioia che gli umani a volte ti negano.",
                    'consiglio': "🌊 La tua anima è un dono per il mondo, ma anche i doni vanno incartati con cura. Proteggi la tua sensibilità, non sprecarla con chi non la merita. Impara a vedere le persone per quello che sono, non per quello che sogni. L'amore vero è fatto di realtà, non di illusioni."
                }
            },

            'luna_plutone_quinconce': {
                'quinconce': {
                    'titolo': "🌙🌋 Luna in quinconce con Plutone",
                    'messaggio': "Sei un campo di battaglia. Le tue emozioni sono così forti che fatichi a controllarle, e spesso ti lasci trascinare in reazioni impulsive di cui poi ti penti. Da bambino ti hanno insegnato che amare significa ubbidire, sottomettersi, sacrificarsi. E ora ti ritrovi sempre nella parte di chi viene sfruttato, di chi dice sì anche quando vorrebbe gridare no. Al lavoro, i colleghi approfittano di te. In amore, attiri persone che vogliono dominarti. Devi imparare a dire no, a difendere i tuoi confini. Scegli lavori dove puoi stare dietro le quinte, senza troppa esposizione. E prima di fidarti di qualcuno, osservalo bene, studialo. Il tuo bisogno di una famiglia è così forte che rischi di accontentarti di briciole.",
                    'consiglio': "🌋 La tua profondità emotiva è un abisso, ma anche l'abisso ha bisogno di luce. Impara a distinguere l'amore vero dalla paura di essere solo. Non accontentarti di briciole: meriti una relazione che ti rispetti. Liberati dai vecchi schemi, guarisci le ferite del passato."
                }
            },

            'luna_ascendente_quinconce': {
                'quinconce': {
                    'titolo': "🌙⬆️ Luna in quinconce con l'Ascendente",
                    'messaggio': "Hai un talento innato per farti sfruttare. Sei così ansioso di dimostrare il tuo interesse per gli altri che ti butti a capofitto in qualsiasi richiesta di aiuto, senza chiederti se chi hai davanti meriti la tua attenzione. La tua salute ne risente, il tuo tempo ne risente, ma tu continui. Forse è un modo per sentirti importante, per dimostrare a te stesso che esisti. La verità è che non hai bisogno di comprare l'affetto di nessuno. Sul lavoro sei apprezzato proprio perché non schivi le fatiche, e questo ti apre delle porte. In amore, però, rischi di attrarre solo persone che vogliono approfittarsi. Impara a distinguere, a valutare, a dire no. La tua bontà è preziosa: non sprecarla.",
                    'consiglio': "🌙 La tua bontà è infinita, ma non deve diventare ingenuità. Non tutti meritano il tuo tempo, la tua energia, la tua salute. Impara a distinguere chi ha davvero bisogno da chi vuole solo approfittarsi. Proteggere te stesso non è egoismo, è saggezza. La tua luce è preziosa: non sprecarla."
                }
            },

            # MERCURIO (quinconce)
            'mercurio_marte_quinconce': {
                'quinconce': {
                    'titolo': "💬🔥 Mercurio in quinconce con Marte",
                    'messaggio': "Sai tante cose, leggi, studi, ti informi, ma quando si tratta di applicare quello che sai per il tuo successo, ti perdi. Ti assumi compiti che non ti competono, lavori per gli altri, e poi ti lamenti di non avere tempo per te. I tuoi sforzi non vengono riconosciuti, e tu ci rimani male. Forse dentro di te pensi di doverti punire per qualcosa. Se proprio non puoi fare a meno di aiutare, fallo in modo professionale: assistenza sociale, medicina, terapie. Almeno vieni pagato. Ma attento a non lavorare troppo: il tuo sistema nervoso è fragile. In amore, dai tutto e ricevi poco. Scegli con cura un partner che condivida i tuoi entusiasmi e contribuisca in parti uguali.",
                    'consiglio': "🔥 La tua mente è una lama affilata, ma anche la lama più affilata ha bisogno di un manico. Non perderti in battaglie che non ti appartengono. Impara a usare la tua intelligenza per te stesso, prima che per gli altri. La tua fedeltà è preziosa: donala solo a chi sa ricambiarla."
                }
            },

            'mercurio_giove_quinconce': {
                'quinconce': {
                    'titolo': "💬✨ Mercurio in quinconce con Giove",
                    'messaggio': "Tutti si rivolgono a te per i loro problemi, e tu non sai dire di no. Rimandi continuamente i tuoi interessi, le tue passioni, per aiutare gli altri. Poi ti lamenti di non avere tempo per te, ma non fai nulla per cambiare le cose. Il senso di colpa se rifiuti è troppo forte. Sei colto, informato, preparato, ma fatichi a usare tutto questo per te stesso. Amici e conoscenti ti distraggono con consigli che dicono essere per il tuo bene, ma che ti allontanano dalla tua strada. Insegnamento, viaggi, relazioni pubbliche sono campi in cui puoi eccellere, se ti concentri. In amore, sei troppo umile, ti accontenti di poco. Non fare promesse che non puoi mantenere e non perderti dietro a chi pretende sottomissione.",
                    'consiglio': "📚 La conoscenza è potere, ma solo se sai usarla. Non lasciare che gli altri ti distraggano dal tuo cammino. Le loro urgenze non sono le tue. Impara a mettere te stesso al primo posto, senza sensi di colpa. La tua crescita personale è la base su cui puoi costruire tutto il resto."
                }
            },

            'mercurio_saturno_quinconce': {
                'quinconce': {
                    'titolo': "💬⏳ Mercurio in quinconce con Saturno",
                    'messaggio': "Sei così serio e responsabile che ne diventi il tuo peggior nemico. Fai molto più di quanto ci si aspetta da te, sperando di essere apprezzato, ma ottieni l'effetto opposto: la gente perde rispetto per te, perché ti umili da solo. Questo tuo atteggiamento vittimistico attira i peggiori individui, quelli che amano dominare. Smettila. Hai talento per l'architettura, il disegno tecnico, la ricerca, le scienze. In questi campi puoi dare il tuo contributo senza il fastidio del contatto personale. Impara a dire no, a proteggere il tuo tempo. Concentrati su te stesso, sulle tue capacità, che non sono poche. Il mondo ha bisogno di te, ma ha bisogno di te in salute, non distrutto.",
                    'consiglio': "⏳ La tua dedizione è ammirevole, ma non deve diventare autodistruttiva. Non sei responsabile della felicità di tutti. Impara a stabilire confini, a proteggere il tuo tempo. La tua serietà è una risorsa, ma solo se bilanciata dalla saggezza di saperti proteggere."
                }
            },

            'mercurio_urano_quinconce': {
                'quinconce': {
                    'titolo': "💬⚡ Mercurio in quinconce con Urano",
                    'messaggio': "Hai un bisogno irrefrenabile di aiutare l'umanità, ma lo fai a scapito della tua serenità. La tua mente è sempre in fermento, piena di idee, ma non riesci a portarne a termine nessuna. Parti con entusiasmo, poi crolli nell'angoscia. Dovresti incanalare questa tua energia in un lavoro specifico: raccolte fondi, ricerca, riabilitazione. Ma ricordati che esisti anche tu, non solo gli altri. Stabilisci le tue priorità, vivi la tua vita. In amore, cerchi persone che la pensano come te, idealiste e generose. Ma non giudicare troppo in fretta: potresti trovare qualcuno che sappia frenarti con dolcezza. La salute è a rischio: il sistema nervoso ne soffre. Check-up e riposo sono essenziali.",
                    'consiglio': "⚡ La tua mente è una centrale elettrica, ma anche le centrali hanno bisogno di manutenzione. Non bruciare tutto in una volta. Impara a staccare, a respirare, a non sentirti responsabile del mondo intero. La tua energia è preziosa: usala con saggezza, non sprecarla in mille rivoli."
                }
            },

            'mercurio_nettuno_quinconce': {
                'quinconce': {
                    'titolo': "💬🌊 Mercurio in quinconce con Nettuno",
                    'messaggio': "Fai troppe promesse, troppe. Poi non le mantieni, e ti giustifichi dicendo che almeno ci hai provato. Ma non è così che funziona. Ti crei responsabilità inutili, ti preoccupi per problemi che non esistono, e ti agiti per cose su cui non hai controllo. La tua immaginazione è fervida, la tua fantasia è grande, ma fatichi a esprimere queste doti in modo concreto. Lavorare con programmi fissi è un incubo per te. Meglio il lavoro autonomo, dove decidi tu i ritmi. Ma attenzione a non fare più del dovuto per compiacere: la tua efficienza ne risente. In amore, attirerai persone che vogliono approfittare di te. Assicurati della sincerità di chi ami prima di legarti. La salute richiede riposo, tanto riposo.",
                    'consiglio': "🌊 La tua sensibilità è un oceano, ma anche l'oceano ha bisogno di confini. Impara a distinguere le tue responsabilità da quelle degli altri. Non devi salvare il mondo, devi solo vivere la tua vita. Le tue promesse valgono oro: non sprecarle. Il tuo tempo è prezioso: non sprecarlo."
                }
            },

            'mercurio_plutone_quinconce': {
                'quinconce': {
                    'titolo': "💬🌋 Mercurio in quinconce con Plutone",
                    'messaggio': "Il senso di responsabilità ti schiaccia. Da bambino ti hanno caricato di doveri, e ora non sai più distinguere ciò che è tuo da ciò che è degli altri. Ti assumi compiti che non ti competono, lavori per chi non muove un dito, e lo fai con un'ansia ossessiva di finire tutto subito. Hai una capacità quasi soprannaturale di ficcare il naso dove non dovresti. Ma hai anche grandi doti: medicina, chimica, ricerca, investigazione. La tua determinazione è ammirevole, la tua persistenza fuori dal comune. Ma la tensione ti logora. Hai bisogno di hobby, di staccare, di fare cose piacevoli. Il tuo potenziale è enorme, ma senza relax diventa autodistruttivo.",
                    'consiglio': "🌋 La tua mente è uno strumento potentissimo, ma anche gli strumenti più potenti hanno bisogno di essere spenti ogni tanto. La perfezione è un'illusione, la pace interiore è reale. Impara a distinguere ciò che è davvero importante da ciò che è solo ansia. Concediti il lusso di essere imperfetto."
                }
            },

            'mercurio_ascendente_quinconce': {
                'quinconce': {
                    'titolo': "💬⬆️ Mercurio in quinconce con l'Ascendente",
                    'messaggio': "Devi capire tutti, a tutti i costi. Concedi sempre il beneficio del dubbio, cedi sempre, pensi che gli altri sappiano sempre quello che fanno. Il bello è che spesso le tue valutazioni sono giuste, e questo mette a disagio la gente. Sei un factotum, sai fare tutto, e parli, parli, parli. Parli anche mentre lavori, e disturbi i colleghi. Ma guai a chiederti cosa fai: ti irriti. Preferisci che siano gli altri a chiedere a te. Conosci gli altri meglio di te stesso. Ti preoccupi per cose inutili. Gli amici ti ammirano, i superiori ti stimano. Programmazione e risparmio sono il tuo forte per la vecchiaia. Ma hai bisogno di vacanze frequenti: la tua vita frenetica ti logora.",
                    'consiglio': "💬 La tua mente è un dono prezioso, ma non dimenticare che anche il corpo ha bisogno di riposo. Le tue parole sono sagge, ma a volte il silenzio è più eloquente. Impara a conoscere te stesso come conosci gli altri. Le tue preoccupazioni spesso sono solo ombre. Concediti il permesso di non pensare."
                }
            },

            # VENERE (quinconce)
            'venere_marte_quinconce': {
                'quinconce': {
                    'titolo': "❤️🔥 Venere in quinconce con Marte",
                    'messaggio': "Hai desideri forti, ma fatichi a realizzarli. Per essere accettato, fai favori a tutti, concedi tutto, ti annulli. Poi un giorno ti accorgi che la gente si aspetta questo da te, e ti senti usato. E ti arrabbi, ma ormai è troppo tardi. Invece di confrontarti con gli altri, concentrati su te stesso. Studia i colleghi, impara da loro, ma non competere. Spesso lavori in un angolo, ignorato. Chiediti perché: forse non ti sei mai fatto vedere per quello che sei. In amore, fai di tutto per attirare l'attenzione, e questo attira i profittatori. Potresti finire nelle mani di chi cerca solo di dominarti. Credi solo a chi dimostra coi fatti, non a chi parla.",
                    'consiglio': "🔥 La tua passione è un fuoco, ma non deve bruciare te stesso. Non devi conquistare l'affetto di nessuno con i favori. Chi ti ama lo fa gratis. Impara a distinguere chi ti vuole bene da chi vuole solo approfittarsi. La tua attenzione è preziosa: non sprecarla."
                }
            },

            'venere_giove_quinconce': {
                'quinconce': {
                    'titolo': "❤️✨ Venere in quinconce con Giove",
                    'messaggio': "Ti sforzi di essere all'altezza delle aspettative altrui, e nel farlo trascuri te stesso. La gente approfitta della tua generosità, e tu non sei selettivo, accetti tutti, ti sottometti a tutti. Forse è perché ti senti inferiore, sin da bambino. Hai un grande senso di responsabilità e ti adatti a qualsiasi lavoro. Ma poiché non ti dai valore, non ottieni riconoscimenti. I colleghi ti rubano le idee. In amore, sei sempre la vittima. La tua salute ne risente: lo stress ti logora. Sforzati di essere più ottimista, impara a dire no. Mantieni il rispetto di te stesso. Non sei qui per essere usato.",
                    'consiglio': "✨ La tua generosità è un dono, ma non deve diventare una moneta con cui comprare l'amore. Non sei inferiore a nessuno. Il tuo valore non dipende da quanto ti sacrifichi. Impara a ricevere, a lasciarti amare senza dover fare nulla in cambio. La persona giusta ti amerà per quello che sei."
                }
            },

            'venere_saturno_quinconce': {
                'quinconce': {
                    'titolo': "❤️⏳ Venere in quinconce con Saturno",
                    'messaggio': "Ti senti sempre in debito. Come se gli altri avessero diritto di aspettarsi qualcosa da te, e tu fossi obbligato a darla. In realtà è solo la tua testa che ingigantisce tutto. Il problema è che non ti ami abbastanza, e ti autopunisci pensando di meritare di essere usato. Migliora l'opinione che hai di te stesso e vedrai che la carriera decollerà. Sei serio, responsabile, lavori più degli altri. Sei portato per relazioni pubbliche, architettura, commercio. In amore, rischi di finire con qualcuno che ti tratta male, che ti fa aspettare, che ti ignora. E tu stai lì a soffrire. Reagisci, impara a renderti interessante. La depressione è la tua peggior nemica, anche per la salute.",
                    'consiglio': "⏳ Il tuo cuore è un gioiello, ma se lo tieni nascosto nessuno lo vedrà. Non aspettare che siano gli altri a scoprirti: mostrati. La tua serietà è pregio, non difetto. Impara a volerti bene, a trattarti con la stessa cura che riservi agli altri. Meriti amore, non solo dovere."
                }
            },

            'venere_urano_quinconce': {
                'quinconce': {
                    'titolo': "❤️⚡ Venere in quinconce con Urano",
                    'messaggio': "Sei disposto a sacrificare i tuoi desideri per gli altri, e lo fai con amarezza. La gente dà per scontato che tu debba occuparti di loro, e tu lo fai, anche se ti rode. E quando rifiuti, ti senti in colpa. Hai un gran bisogno di comunicare, di essere amato, ma non comprare l'affetto con i favori. Sei brillante, simpatico, interessante. Perché dovresti pagare per essere accettato? Al lavoro, attento ai colleghi che cercano di rifilarti i compiti noiosi. I campi artistici sono i più adatti a te. In amore, non lasciarti intrappolare dall'attrazione fisica: potrebbe costarti caro.",
                    'consiglio': "⚡ La tua luce è unica, ma non deve accecare te stesso. Non hai bisogno di comprare l'affetto di nessuno. La tua originalità è il tuo vero fascino. Impara a distinguere chi ti apprezza per quello che sei da chi vuole solo approfittarsi. Le relazioni vere non si basano sui favori, ma sulla reciproca stima."
                }
            },

            'venere_nettuno_quinconce': {
                'quinconce': {
                    'titolo': "❤️🌊 Venere in quinconce con Nettuno",
                    'messaggio': "Sei sensibile, ispirato, fantasioso, ma fatichi a usare queste doti perché le accavalli tutte insieme e crei confusione. Fai troppe cose contemporaneamente, e lo stress ti logora. Dai priorità, una cosa alla volta. Al lavoro, non permettere ai colleghi di approfittare del tuo bisogno di fare. Le arti sono il tuo mondo: lì puoi esprimerti senza costrizioni. Sei dolce, sentimentale, arrendevole, e questo ti rende vulnerabile. Soffri enormemente quando vieni ferito. In amore, sii cauto: non credere a tutte le dichiarazioni d'amore che ricevi. Potrebbero essere solo parole.",
                    'consiglio': "🌊 La tua anima è un'opera d'arte, ma anche l'arte più bella ha bisogno di una cornice. Impara a proteggere la tua sensibilità, a dosare la tua dolcezza. Non tutti meritano di entrare nel tuo giardino segreto. Scegli con cura chi ammettere, e fai entrare solo chi sa rispettare i tuoi fiori."
                }
            },

            'venere_plutone_quinconce': {
                'quinconce': {
                    'titolo': "❤️🌋 Venere in quinconce con Plutone",
                    'messaggio': "Esageri in amore. Ti innamori troppo in fretta, ti fidi troppo in fretta, e poi piangi. Le persone ti raccontano storie tristi e tu ci credi, le vuoi salvare, e ti ritrovi in relazioni con gente che non ti merita. L'attrazione fisica ti annebbia il giudizio. Attento: potresti beccarti anche qualche malattia. Nel lavoro, invece, puoi dare il meglio in attività sociali, ricerca medica, dietologia. Ma quando devi prendere decisioni importanti, chiedi consiglio a un esperto. La gente tende ad approfittare di te, anche in piccole cose. Impara a tenerti fuori dai pasticci, anche da quelli piccoli. Paga la tua quota e lascia che siano altri a organizzare.",
                    'consiglio': "🌋 La tua passione è un vulcano, ma anche il vulcano più potente ha bisogno di quiete. Non lasciarti travolgere dalle emozioni del momento. Impara a distinguere l'amore vero dalla compassione, l'attrazione dalla connessione profonda. La tua intensità è un dono, ma va dosata con saggezza. Proteggi il tuo cuore."
                }
            },

            'venere_ascendente_quinconce': {
                'quinconce': {
                    'titolo': "❤️⬆️ Venere in quinconce con l'Ascendente",
                    'messaggio': "Sei troppo accomodante. Fai di tutto per piacere, per essere accettato, per vivere in pace. E la gente ne approfitta. Hai un grande potenziale creativo, ma non lo sviluppi pienamente perché ti accontenti. Per te la felicità non è ciò che ottieni, ma ciò che provi nel fare. In famiglia sei un angelo, fai di tutto per l'armonia, anche a costo di sacrifici. E loro ti vogliono bene, ma a volte ne approfittano. Hai molti amici, sei servizievole, ma guai a toccare i soldi: l'amicizia finisce lì. Nel lavoro ti adatti a tutto, e i capi ti adorano. La sicurezza economica è il tuo chiodo fisso, ma sembra sempre sfuggirti. Potresti sposarti per interesse, ma poi te ne pentiresti.",
                    'consiglio': "💖 La tua dolcezza è un dono, ma non deve diventare una debolezza. Non devi comprare l'affetto di nessuno. L'armonia è importante, ma non a costo di perdere te stesso. Impara a dire di no, a proteggere i tuoi confini. La persona giusta ti amerà per quello che sei, non per quello che fai."
                }
            },

            # MARTE (quinconce)
            'marte_giove_quinconce': {
                'quinconce': {
                    'titolo': "🔥✨ Marte in quinconce con Giove",
                    'messaggio': "Fai fatica a capire cosa è prioritario nella tua vita, soprattutto quando entrano in gioco i rapporti con gli altri. Ti mostri generoso per sentirti in diritto di soddisfare i tuoi desideri. Assumi atteggiamenti protettivi, come se gli altri non fossero in grado di cavarsela da soli. Così facendo, trascuri te stesso e impedisci anche agli altri di crescere. Sei critico, mai contento, interferisci nelle faccende altrui. E poi ti chiedi perché non sei amato. Hai grandi capacità in molti campi: medicina, legge, assistenza, insegnamento. Ma se continui a farti sfruttare, le tue idee verranno rubate. Non raccontare i tuoi progetti a nessuno prima di realizzarli. In amore, sei generoso e arrendevole, forse troppo.",
                    'consiglio': "🔥 La tua generosità è una fiamma, ma non deve bruciare la tua autostima. Aiutare è bello, ma non deve diventare un modo per sentirti superiore. Lascia che gli altri imparino a camminare da soli. La tua vera forza è nel riconoscere i tuoi limiti e i tuoi talenti. Usali per te, prima che per gli altri."
                }
            },

            'marte_saturno_quinconce': {
                'quinconce': {
                    'titolo': "🔥⏳ Marte in quinconce con Saturno",
                    'messaggio': "Non sai più cosa sia veramente tuo dovere e cosa no. Ti butti in mille cose, perdi fiducia in te stesso, e finisci per sottostare ai capricci altrui. Forse è un vecchio senso di colpa che ti spinge a dimostrare che non sei indifferente. Ma così facendo, ti annulli. Hai qualità per la carriera militare, lo sport, la tutela ambientale, la fisioterapia. Ma se non sei sicuro di te, troverai sempre qualcuno pronto a metterti i piedi in testa. In amore, niente avventure volgari: non fanno per te. La salute è a rischio: incidenti, fratture, artrite. Con gli anni, rischi di diventare troppo sedentario. Muoviti, ma con giudizio.",
                    'consiglio': "⏳ La tua forza è un'ancora, ma non deve tenerti fermo in un porto che non ti appartiene. Non sei responsabile del mondo intero. La tua lealtà è preziosa, ma va data a chi la merita. Impara a distinguere i veri doveri dalle false colpe. La tua salute è la base di tutto: senza di essa, non puoi aiutare nessuno."
                }
            },

            'marte_urano_quinconce': {
                'quinconce': {
                    'titolo': "🔥⚡ Marte in quinconce con Urano",
                    'messaggio': "Sei sempre in tensione. Vuoi dimostrare qualcosa a te stesso e agli altri, e per farlo rischi la salute. Ti comporti come se tutti si aspettassero il massimo da te, e ti butti in mille imprese senza pensare alle conseguenze. Sotto questa ansia di fare, c'è un senso di colpa. Le pretese degli altri possono essere eccessive, ma se tu le assecondi, il problema è tuo. Ammiri chi ce l'ha fatta, e questo ti frustra. Invece di competere, usa la tua creatività. Sei originale, unico. Sfrutta questo. In amore, preferisci persone sicure di sé, anche se pretendono tanto. Sei ammirevole per come non rifiuti mai aiuto a chi ha veramente bisogno.",
                    'consiglio': "⚡ La tua energia è un fulmine, ma anche il fulmine ha bisogno di un parafulmine. Non devi dimostrare nulla a nessuno. La tua originalità è il tuo vero valore. Impara a incanalare la tua tensione in creatività, non in autodistruzione. Rilassati, respira, concediti il permesso di essere imperfetto. La vera forza è nella calma."
                }
            },

            'marte_nettuno_quinconce': {
                'quinconce': {
                    'titolo': "🔥🌊 Marte in quinconce con Nettuno",
                    'messaggio': "Cerchi di fare del bene, di realizzarti in modo costruttivo, ma i risultati sono sempre deludenti. Sei troppo ansioso, troppo impaziente, e trascuri i dettagli importanti. Poi ti agiti, sprechi energie, e tutto peggiora. Devi imparare a programmare, a controllare le tue mosse, a rimandare i progetti fatti in fretta. Evita lavori pericolosi o con macchinari. Il tuo fisico non regge sforzi prolungati. Cerca un'attività con ritmi tuoi, magari artistica. In amore, ti trovi sempre con persone che approfittano di te. Dai tutto, ricevi niente. Hai forti desideri sessuali, ma frequenti persone sbagliate. Ci saranno inganni e delusioni. La tua salute è fragile: infezioni, malattie psicosomatiche. Abbi cura di te.",
                    'consiglio': "🌊 La tua anima è un oceano in tempesta. Impara a calmare le onde prima di navigare. Non hai bisogno di dimostrare nulla a nessuno. La tua sensibilità è un dono, ma va protetta. Non perderti in relazioni che ti svuotano. Cerca l'amore vero, quello che ti accetta per quello che sei, non per quello che fai."
                }
            },

            'marte_plutone_quinconce': {
                'quinconce': {
                    'titolo': "🔥🌋 Marte in quinconce con Plutone",
                    'messaggio': "Sei ipersensibile alle esigenze degli altri, e ti carichi di un'infinità di compiti. Ne fai troppi, più di quanto puoi materialmente portare a termine. Il pensiero di tutto ciò che devi fare ti perseguita, diventa un'ossessione. Hai tanti bisogni, ma fatichi a soddisfarli. La tua vita sessuale è intensa, ma ti debilita. Moderazione è la parola d'ordine. Quando le cose vanno male, ti senti in colpa e diventi insopportabile. I problemi di denaro ti agitano. Fatti un programma, stabilisci priorità, metti da parte ciò che non è urgente. Impara a rilassarti, a non fare nulla. Un giorno scoprirai di essere importante, e forse allora dirai no a qualcuno. E tutti rimarranno a bocca aperta.",
                    'consiglio': "🌋 La tua forza è immensa, ma dispersa. Concentrala come un raggio laser. Non devi salvare il mondo da solo. Impara a delegare, a lasciare che gli altri facciano la loro parte. Il tuo tempo è prezioso: non sprecarlo in mille rivoli. La vera potenza non è nel fare tutto, ma nello scegliere cosa fare."
                }
            },

            'marte_ascendente_quinconce': {
                'quinconce': {
                    'titolo': "🔥⬆️ Marte in quinconce con l'Ascendente",
                    'messaggio': "Fai più di quanto il tuo corpo possa sopportare, per paura che gli altri pensino che non ti impegni abbastanza. Sei imprudente, non usi le protezioni, vuoi sembrare coraggioso. Se qualcuno dubita di te, ti butti a capofitto per dimostrare il contrario, e spesso te ne penti. Sei stato educato così: reagire subito, senza pensare. Ma questa impulsività è il tuo tallone d'Achille. Impara a riflettere prima di agire, a valutare i rischi. Ti piace discutere, confrontarti, anche se perdi. Le tue energie possono trovare sfogo nello sport, nelle competizioni. Meglio lì che nella vita.",
                    'consiglio': "⚡ La tua energia è un cavallo selvaggio: magnifico, ma pericoloso senza una guida. Impara a frenare l'impulso, a pensare prima di agire. Il coraggio non è nell'imprudenza, ma nella consapevolezza. La vera forza è saper attendere il momento giusto. Respira, rifletti, poi agisci."
                }
            },

            # GIOVE (quinconce)
            'giove_saturno_quinconce': {
                'quinconce': {
                    'titolo': "✨⏳ Giove in quinconce con Saturno",
                    'messaggio': "Le responsabilità ti pesano come macigni, e non sai perché. Forse in passato hai scansato i tuoi doveri, e ora ne paghi le conseguenze. Ma non è detto che l'unica soluzione sia sacrificarti per sempre. Hai bisogno di un consiglio saggio, di qualcuno che ti aiuti a distinguere ciò che è davvero tuo dovere da ciò che non lo è. Devi imparare che anche tu hai diritto alla felicità, al piacere, al tempo per te. Hai talento in molte cose: medicina, terapie, insegnamento, edilizia. Lavora in proprio, se puoi, per evitare sfruttatori. Non ci sono limiti a ciò che puoi fare, se ti liberi dai sensi di colpa. La salute richiede moderazione e movimento: cammina, viaggia, cambia aria.",
                    'consiglio': "⏳ La tua responsabilità è un dono, ma non deve diventare una croce. Non sei venuto al mondo per espiare colpe che non hai. La vita è anche leggerezza, gioia, piacere. Concediti il permesso di essere felice, senza sensi di colpa. Cerca l'equilibrio tra servire e vivere."
                }
            },

            'giove_urano_quinconce': {
                'quinconce': {
                    'titolo': "✨⚡ Giove in quinconce con Urano",
                    'messaggio': "I tuoi sogni vengono spesso infranti da circostanze impreviste. Forse è perché sono troppo ambiziosi, poco realistici. Dovresti essere più disciplinato, più organizzato. Ma invece ascolti i consigli di chi ti spinge a osare oltre i limiti. Sei un gran lavoratore, capace di fare molte cose. Ma attento a chi cerca di scaricare su di te i propri pesi. Sei così cordiale che la gente si sente autorizzata ad approfittare. Medicina, legge, ricerca, insegnamento: in questi campi puoi eccellere, se ti concentri. Ma hai bisogno di ordine, di priorità, di un consigliere fidato che ti aiuti a mettere a fuoco le idee. In amore, non farti sfruttare: chi ti ama non chiede solo favori. La salute richiede riposo e moderazione.",
                    'consiglio': "⚡ La tua visione è quella di un futuro radioso, ma il presente è l'unico tempo che hai. Non vivere solo di sogni, costruisci con i piedi per terra. I tuoi progetti sono preziosi, ma senza una base solida crollano. Impara a distinguere i consigli utili dalle pressioni dannose. La tua strada è unica: seguila con fiducia, ma con saggezza."
                }
            },

            'giove_nettuno_quinconce': {
                'quinconce': {
                    'titolo': "✨🌊 Giove in quinconce con Nettuno",
                    'messaggio': "Le tue emozioni offuscano la ragione. Sai che non dovresti esagerare nel dedicarti agli altri, ma i sentimenti ti travolgono e non sai dire di no. Ti crei problemi inesistenti, ti carichi di colpe immaginarie. Sembra che tu voglia soffrire, espiare qualcosa. Sei attratto da lavori duri, in prigioni, riformatori, con i reietti. Il tuo contributo è prezioso, ma rischi di assorbire tutta la negatività dell'ambiente. La tua salute ne risente: malattie strane, difficili da diagnosticare, psicosomatiche. Il tuo corpo ti sta dicendo che stai sbagliando qualcosa. Ascoltalo.",
                    'consiglio': "🌊 La tua compassione è un oceano, ma anche l'oceano più vasto ha bisogno di essere alimentato da fiumi puliti. Non puoi salvare il mondo assorbendone il dolore. La tua missione non è espiazione, è amore. Impara a distinguere il vero bisogno dalla tua necessità di sacrificio. Aiuta, ma proteggiti."
                }
            },

            'giove_plutone_quinconce': {
                'quinconce': {
                    'titolo': "✨🌋 Giove in quinconce con Plutone",
                    'messaggio': "La vita ti costringe continui aggiustamenti psicologici, e tu cerchi sempre la strada più facile. Ti lamenti del destino, ti ribelli, ma non fai nulla per cambiare. A volte diventi opportunista, vuoi prendere ciò che credi sia tuo diritto. Altre volte, all'opposto, rinunci a tutto per servire gli altri. Sono due estremi, e nessuno dei due funziona. Cerca la via di mezzo, l'equilibrio. Solo così potrai esprimere le tue potenzialità e dare un vero contributo al mondo. Non essere né vittima né profittatore. Sii semplicemente umano.",
                    'consiglio': "🌋 La tua anima è un campo di battaglia tra opposti estremi. Cerca il centro, l'equilibrio. Non sei né salvatore né profittatore, sei semplicemente umano. Accetta la tua umanità, con le sue luci e le sue ombre. Il contributo che puoi dare al mondo non sta nell'estremismo, ma nella saggezza della moderazione."
                }
            },

            'giove_ascendente_quinconce': {
                'quinconce': {
                    'titolo': "✨⬆️ Giove in quinconce con l'Ascendente",
                    'messaggio': "Sei generoso, sempre pronto ad aiutare. Ma quando si tratta dei tuoi affari, fatichi a gestirli con la stessa efficienza. Fai promesse a destra e a manca, e poi non le mantieni, non perché sei in malafede, ma perché te ne dimentichi. Inizi mille progetti e non ne porti a termine nessuno. Hai un cuore tenero e ti fai impietosire facilmente. Ma attenzione: ci sono amici che vengono da te solo quando hanno bisogno, e spariscono quando stanno bene. Impara a riconoscerli. I tuoi progetti sono grandi, ma senza costanza restano sogni. Scegli una direzione, una sola, e seguila fino in fondo. La realizzazione è più bella del sogno.",
                    'consiglio': "✨ La tua generosità è un dono, ma non deve diventare ingenuità. Non tutti quelli che piangono meritano le tue lacrime. I tuoi progetti sono magnifici, ma senza costanza restano sogni. Scegli una direzione, una sola, e seguila fino in fondo. La realizzazione è più bella del sogno."
                }
            },

            # SATURNO (quinconce)
            'saturno_urano_quinconce': {
                'quinconce': {
                    'titolo': "⏳⚡ Saturno in quinconce con Urano",
                    'messaggio': "Ti assumi impegni con gli altri, ma poi fatichi a organizzarli. Forse lo fai per compiacere, per essere accettato. Ma c'è un problema di fondo: sei troppo attaccato al passato, ai vecchi metodi, e rifiuti le innovazioni. Ogni cambiamento ti sembra una minaccia. Ma il progresso avanza comunque, che tu lo voglia o no. Meglio accettarlo e adattarsi, altrimenti resterai indietro. La vera insicurezza non è nel cambiamento, ma nel non riuscire a stargli dietro. In amore, il partner riconoscerà le tue potenzialità più di te. Fidati di lui, anche se dovrete scendere a compromessi. Il pessimismo ti rovinerebbe la salute: arterie, artrosi, carattere irascibile. Lascia andare.",
                    'consiglio': "⚡ Il cambiamento non è nemico, è alleato. Non puoi fermare il fiume del tempo, puoi solo imparare a nuotare. La tua sicurezza non è nel passato, è nella tua capacità di adattarti. Abbraccia il nuovo con curiosità, non con paura. La vita è movimento, e tu sei parte di questo movimento."
                }
            },

            'saturno_nettuno_quinconce': {
                'quinconce': {
                    'titolo': "⏳🌊 Saturno in quinconce con Nettuno",
                    'messaggio': "Hai bisogno di giustificare i tuoi talenti, di metterli al servizio del prossimo. Senti il peso delle ingiustizie del mondo come se fossero colpa tua. Hai la tempra del martire: ti assumi più responsabilità del dovuto, ti sacrifichi per cause sociali. Ma attento a non lasciarti trascinare in programmi loschi, o a farti plagiare da qualcuno. In realtà, forse stai solo usando il prossimo per alleviare i tuoi sensi di colpa. Il bisogno di essere necessario ti spinge a esporti troppo. La salute ne risente: malattie strane, psicosomatiche, difficili da diagnosticare. Evita contatti con persone malate, fai check-up regolari. Non trascurare i sintomi, non aver paura delle analisi. La prevenzione è tutto.",
                    'consiglio': "🌊 La tua anima è un ponte tra cielo e terra, ma anche i ponti hanno bisogno di manutenzione. Non devi espiare colpe che non hai. Il tuo servizio è prezioso, ma non a costo della tua vita. La salute è il tempio del tuo spirito: custodiscilo. Non temere le analisi, temi l'ignoranza. Conoscere è prevenire."
                }
            },

            'saturno_plutone_quinconce': {
                'quinconce': {
                    'titolo': "⏳🌋 Saturno in quinconce con Plutone",
                    'messaggio': "Sei serio, responsabile, e vorresti migliorare il mondo. Il problema è che ti carichi di troppi compiti, e la tua salute ne risente. Hai paura di essere giudicato se non aiuti, e allora ti butti in mille cose. Inoltre, sei perfezionista: perdi tempo in dettagli inutili e trascuri l'essenziale. I colleghi meno capaci di te si appoggiano sulle tue spalle. In amore, attiri persone che vogliono dominarti. Devi imparare a difenderti, a mettere nero su bianco, a non fidarti della parola. Il tuo giudizio a volte è offuscato, ma con la pratica migliorerà. Non farti mettere i piedi in testa.",
                    'consiglio': "🌋 La tua serietà è una roccia, ma non deve diventare una prigione. Non sei responsabile dell'incompetenza altrui. Impara a distinguere i tuoi compiti da quelli degli altri. La perfezione è una meta, non un'ossessione. L'importante è fare del tuo meglio, non essere perfetto. In amore, non accettare catene. La persona giusta cammina al tuo fianco."
                }
            },

            'saturno_ascendente_quinconce': {
                'quinconce': {
                    'titolo': "⏳⬆️ Saturno in quinconce con l'Ascendente",
                    'messaggio': "Sei troppo serio, troppo preso dalle tue responsabilità. La salute ne risente. Programmazione e strategia sono i tuoi punti di forza, ma ti isolano. La gente ti vede come distante, inavvicinabile. Tu offri aiuto solo a pochi eletti, e quando lo fai, lo fai con rigore, con durezza. La tua sincerità è totalitaria, senza sconti. L'esperienza ti ha insegnato a contare solo su te stesso, e ormai è difficile chiedere aiuto. Cerchi lavori sicuri, solidi, senza rischi. La sicurezza è tutto per te. Ma questa fortezza in cui vivi ti protegge, ma ti imprigiona. Apri le porte ogni tanto. La vita è anche relazione, contatto, scambio.",
                    'consiglio': "⏳ La tua serietà è un tempio, ma anche i templi hanno bisogno di luce e di aria. Non chiuderti nella tua fortezza. La vita è anche leggerezza, contatto, condivisione. Impara a fidarti, a chiedere aiuto, a mostrare le tue fragilità. Non sei un'isola, sei parte di un arcipelago. La vera forza non è nell'indipendenza assoluta, ma nella capacità di chiedere e ricevere."
                }
            },

            # URANO (quinconce)
            'urano_nettuno_quinconce': {
                'quinconce': {
                    'titolo': "⚡🌊 Urano in quinconce con Nettuno",
                    'messaggio': "Le ingiustizie del mondo ti tormentano. Soffri per i poveri, per gli oppressi, per le vittime della storia. Ti senti in colpa, impotente, e questo ti spinge a voler fare qualcosa. Forse lavori per un ente di assistenza, per un'organizzazione umanitaria. Ti identifichi con le loro battaglie, le fai tue. Sei nato in un periodo storico complesso, tra le due guerre, e porti dentro le contraddizioni di quegli anni. Il tuo contributo alla causa dell'umanità sarà importante, se riuscirai a trasformare la tua indignazione in azione concreta. Non basta sentire, bisogna fare.",
                    'consiglio': "🌊 La tua sensibilità alle ingiustizie è un dono, ma non deve paralizzarti. Non puoi cambiare il mondo da solo, ma puoi fare la tua parte. Scegli una battaglia, una sola, e combattila con costanza. La storia è fatta di piccoli gesti che insieme diventano rivoluzione. Non sentirti in colpa per ciò che non puoi fare, ma impegnati in ciò che puoi fare."
                }
            },

            'urano_plutone_quinconce': {
                'quinconce': {
                    'titolo': "⚡🌋 Urano in quinconce con Plutone",
                    'messaggio': "Ti senti impotente di fronte al potere dei grandi, delle corporation, della politica. La tua libertà di espressione è limitata, e questo ti amareggia. Sei nato in un'epoca di grandi trasformazioni industriali, e porti dentro la paura di essere schiacciato da questi giganti. Hai cercato protezione nei sindacati, nelle organizzazioni collettive, e continui a lottare per la sicurezza economica. La tua battaglia è legittima, ma non dimenticare che la vera ricchezza è dentro di te. I giganti passano, i valori dello spirito restano. Coltiva la tua forza interiore: è l'unico investimento che nessuno potrà mai portarti via.",
                    'consiglio': "🌋 La tua lotta per la sicurezza è legittima, ma non dimenticare che la vera ricchezza è dentro di te. I giganti dell'industria passano, i valori dello spirito restano. Combatti per i tuoi diritti, ma non perdere la tua anima in battaglie materiali. La sicurezza vera non è nel conto in banca, ma nella consapevolezza di poter affrontare qualsiasi tempesta."
                }
            },

            'urano_ascendente_quinconce': {
                'quinconce': {
                    'titolo': "⚡⬆️ Urano in quinconce con l'Ascendente",
                    'messaggio': "La tua mente è un vulcano di idee innovative, originali, a volte geniali. Sei sempre alla ricerca di modi nuovi per fare le cose, e spesso ci riesci. Ma le tue idee sono troppo avanti per i tuoi tempi, e la gente non le capisce. Così lavori di nascosto, sviluppi progetti in solitudine, e solo quando sono pronti li mostri al mondo. Sei interessato alle nuove tecnologie, ai metodi che possono migliorare la vita delle persone. Ma attento a proteggere le tue invenzioni: brevetti, tutele legali. I furbi sono in agguato. Hai molte risorse, e guadagnarti da vivere non è un problema. Gli amici ti stimano e ti danno buoni consigli. Se lavori in società, però, rischi di trascurare il partner perché troppo concentrato su di te. Cerca un equilibrio.",
                    'consiglio': "⚡ La tua mente è un laboratorio di idee geniali. La tua originalità è il tuo marchio. Non aver paura di essere diverso, ma impara a proteggere le tue creazioni. Il mondo ha bisogno della tua innovazione, ma anche della tua saggezza. Non isolarti nel tuo genio: condividi, collabora, ascolti. Le grandi idee nascono dalla mente, ma diventano realtà grazie alla comunità."
                }
            },

            # NETTUNO (quinconce)
            'nettuno_ascendente_quinconce': {
                'quinconce': {
                    'titolo': "🌊⬆️ Nettuno in quinconce con l'Ascendente",
                    'messaggio': "Fai di tutto per piacere, per essere accettato, ma i tuoi sforzi sono spesso vani. La gente percepisce un fondo egoistico nelle tue attenzioni, e non si fida. Inizi mille progetti e non ne porti a termine nessuno, perché ti mancano organizzazione e praticità. Hai bisogno di una guida, di qualcuno che ti aiuti a mettere ordine nelle idee. Con i soldi sei un disastro: ti fai convincere da amici improvvisati e perdi tutto. Sei compassionevole, sempre pronto ad aiutare, ma trascuri i tuoi affari. Dovresti lavorare in proprio, dove nessuno ti dice cosa fare. Se sbagli, sono cavoli tuoi, ma almeno impari. La tua sensibilità è un dono, ma senza disciplina diventa un handicap. Metti ordine nella tua vita, e poi potrai veramente aiutare gli altri.",
                    'consiglio': "🌊 La tua sensibilità è un dono, ma senza disciplina diventa un handicap. Impara a organizzare la tua creatività, a dare forma ai tuoi sogni. Non lasciare che gli amici ti distraggano dalla tua strada. La tua compassione è preziosa, ma non deve diventare autolesionismo. Metti ordine nella tua vita, e poi potrai veramente aiutare gli altri."
                }
            },

            # PLUTONE (quinconce)
            'plutone_ascendente_quinconce': {
                'quinconce': {
                    'titolo': "🌋⬆️ Plutone in quinconce con l'Ascendente",
                    'messaggio': "Prendi le tue responsabilità verso il mondo molto seriamente. Le ingiustizie sociali ti toccano nel profondo, e ti offri volontario per migliorare le cose. Il problema è che così trascuri i tuoi affari personali. Sei un lavoratore eccellente, ma hai bisogno di sicurezza finanziaria, e per questo ti preoccupi di pensione e assicurazioni. Sei un po' presuntuoso, e quando hai torto fatichi ad ammetterlo. Le tue idee sono solide, e tendi a imporle agli altri, inimicandoti la gente. Dici quello che pensi senza peli sulla lingua, specialmente di chi è al potere. Ami la competizione e speri di arrivare in alto per dimostrare il tuo valore. Ma la presunzione può chiuderti porte che la competenza potrebbe aprire. Impara a dosare forza e umiltà.",
                    'consiglio': "🌋 La tua forza è nella determinazione, ma la tua debolezza nella rigidità. Le tue idee sono preziose, ma non sono le uniche. Impara ad ascoltare, a dubitare, a metterti in discussione. La vera autorità non si impone, si riconosce. La tua grandezza sta nell'equilibrio tra forza e umiltà."
                }
            },
            # ============================================
            # MESSAGGI PER LE OPPOSIZIONI RADIX
            # ============================================

            # SOLE (opposizioni)
            'sole_luna_opposizione': {
                'opposizione': {
                    'titolo': "☀️🌙 Sole in opposizione alla Luna",
                    'messaggio': "Dentro di te convivono due anime: una che vorrebbe spiccare il volo e l'altra che ha bisogno di radici profonde. Questo contrasto ti rende a volte difficile da capire, anche per te stessa. Ti entusiasmi per un progetto, ma poi la paura di sbagliare ti frena. Desideri l'indipendenza, ma il senso di lealtà verso chi ami ti trattiene. In realtà stai cercando un equilibrio, un modo per essere te stessa senza perdere gli affetti. Le relazioni per te sono fondamentali, ma a volte chiedi troppo, pretendi che l'altro sia tutto: amico, amante, sostenitore. Forse puoi imparare a dare prima di ricevere, a fidarti che l'amore vero non ha bisogno di prove continue. La vita è fatta anche di delusioni, ma sono quelle che ti insegnano ad apprezzare i momenti belli.",
                    'consiglio': "🌓 Non devi scegliere tra essere te stessa e amare. Puoi avere entrambe le cose, con pazienza e fiducia. Le relazioni sono come giardini: vanno coltivate giorno per giorno, con dolcezza. E a volte bisogna accettare che non tutti i semi germogliano."
                }
            },

            'sole_marte_opposizione': {
                'opposizione': {
                    'titolo': "☀️🔥 Sole in opposizione a Marte",
                    'messaggio': "Hai una energia travolgente, una voglia di affermarti che ti rende determinata e coraggiosa. A volte però questa tua forza viene percepita come aggressività, e la gente si mette sulla difensiva senza che tu lo voglia. In realtà dietro la tua grinta c'è una grande sensibilità: hai paura di non essere all'altezza, e allora combatti per dimostrare il tuo valore. Ma la vera forza non sta nel vincere tutte le battaglie, ma nel conoscere i propri limiti e accettarli con dolcezza. In amore sei passionale, intensa, ma a volte ti stanchi presto. Forse perché cerchi qualcuno che sappia starti accanto senza farti sentire in competizione. Impara a rallentare, a goderti il percorso, a fidarti che puoi essere amata anche quando non stai lottando.",
                    'consiglio': "⚡ La tua energia è un dono prezioso, ma non devi usarla per dimostrare qualcosa a qualcuno. Rallenta, respira, scegli con cura le tue battaglie. La vera forza è anche saper aspettare, saper essere dolce."
                }
            },

            'sole_giove_opposizione': {
                'opposizione': {
                    'titolo': "☀️✨ Sole in opposizione a Giove",
                    'messaggio': "Sei una donna piena di entusiasmo, di idee, di progetti. La tua vitalità è contagiosa e sai trascinare gli altri con la tua energia. A volte però prometti più di quanto puoi mantenere, non per cattiveria, ma perché ti lasci prendere dall'euforia. E quando non riesci a mantenere gli impegni, ti senti in colpa e cerchi giustificazioni. Hai un grande talento, ma la costanza non è il tuo forte: inizi mille cose e fatichi a portarle a termine. Forse hai paura di impegnarti davvero, di scoprire che anche dando il massimo i risultati possono tardare. In amore, pretendi molto dal partner, ma forse non sei pronta a dare altrettanto. Rallenta, scegli una strada e percorrila con pazienza. I frutti arriveranno, se impari a coltivare con cura.",
                    'consiglio': "🌟 L'entusiasmo è un motore meraviglioso, ma ha bisogno di costanza per portarti lontano. Impara a finire ciò che inizi, a mantenere le promesse. La tua luce brillerà ancora più forte quando saprai darle una direzione."
                }
            },

            'sole_saturno_opposizione': {
                'opposizione': {
                    'titolo': "☀️⏳ Sole in opposizione a Saturno",
                    'messaggio': "Hai un senso del dovere molto sviluppato, una serietà che ti porta a prendere la vita con impegno. Ma questa tua responsabilità a volte si trasforma in un peso: ti senti sempre inadeguata, sempre sotto esame. Cerchi conferme dagli altri, ma nemmeno quelle bastano a calmare la tua insicurezza. Forse da piccola hai imparato che per essere amata dovevi dimostrare qualcosa, e ora non sai più startene in pace. In realtà hai tutte le qualità per essere apprezzata: la tua dedizione, la tua onestà, la tua profondità. La persona che ami potrebbe essere il tuo porto sicuro, se tu imparassi a mostrarti fragile, a chiedere aiuto senza vergogna. La vera forza è mostrarsi per quello che si è, con pregi e difetti.",
                    'consiglio': "⏳ Non devi dimostrare niente a nessuno, tanto meno a te stessa. La sicurezza non viene dagli applausi, ma dalla pace che trovi dentro. E quella pace puoi trovarla solo se smetti di giudicarti e inizi ad amarti per quello che sei."
                }
            },

            'sole_urano_opposizione': {
                'opposizione': {
                    'titolo': "☀️⚡ Sole in opposizione a Urano",
                    'messaggio': "Sei una donna originale, anticonformista, con una mente brillante e innovativa. La tua indipendenza è il tuo orgoglio, e non sopporti imposizioni o limiti alla tua libertà. A volte però questa tua voglia di distinguerti ti porta a essere sempre in tensione, sempre pronta a difenderti da attacchi che forse non esistono. La gente ti percepisce come nervosa, irritabile, e si allontana senza che tu capisca perché. In realtà dietro la tua ribellione c'è una grande sensibilità: hai paura di essere giudicata, di non essere all'altezza, e allora ti nascondi dietro un atteggiamento di sfida. In amore, cerchi qualcuno che ti capisca senza volerti cambiare. Forse puoi imparare a rilassarti, a fidarti, a mostrarti per quello che sei, senza maschere.",
                    'consiglio': "⚡ La tua originalità è un dono, ma non deve diventare un muro. Impara a respirare, a lasciar andare la tensione. La vera libertà non è combattere contro tutto, ma scegliere con amore ciò che merita la tua energia."
                }
            },

            'sole_nettuno_opposizione': {
                'opposizione': {
                    'titolo': "☀️🌊 Sole in opposizione a Nettuno",
                    'messaggio': "Hai un'anima sognatrice, una sensibilità fuori dal comune. Vedi la bellezza dove altri non la vedono, percepisci le emozioni con una profondità speciale. A volte però questo tuo mondo interiore ti allontana dalla realtà: fatichi a distinguere ciò che è vero da ciò che desideri che sia vero. Le persone ti sembrano migliori di quello che sono, e quando mostrano i loro limiti, resti delusa. In amore, questo è particolarmente doloroso: ti innamori dell'idea che ti sei fatta, non della persona reale. E poi soffri, e ti chiudi. Hai bisogno di imparare a stare con i piedi per terra senza perdere la tua magia. La realtà può essere meno affascinante dei sogni, ma è l'unico posto dove puoi trovare l'amore vero, fatto di imperfezioni e di autenticità.",
                    'consiglio': "🌊 I tuoi sogni sono ali meravigliose, ma per volare hai bisogno anche di un corpo. Impara a distinguere l'illusione dalla verità, senza perdere la tua sensibilità. Le persone vanno amate per quello che sono, non per quello che immagini. E l'amore vero, quello imperfetto, è l'unico che scalda davvero."
                }
            },

            'sole_plutone_opposizione': {
                'opposizione': {
                    'titolo': "☀️🌋 Sole in opposizione a Plutone",
                    'messaggio': "Sei una donna di una forza straordinaria. Quando vuoi qualcosa, niente può fermarti. Questa determinazione ti ha portata lontano, ma a volte ti gioca brutti scherzi. Vedi nemici dappertutto, ti senti sempre in pericolo, e reagisci con tutta la tua potenza, anche quando basterebbe un sorriso. Le persone ti percepiscono come intensa, a volte troppo, e si tengono a distanza. In realtà dietro la tua corazza c'è una grande paura: paura di essere ferita, tradita, abbandonata. In amore, questo si traduce in relazioni intense ma tormentate, fatte di alti e bassi, di passione e conflitto. Forse è il momento di abbassare le difese, di fidarti un po' di più. La vita non è una guerra, è un viaggio da condividere. E gli altri non sono nemici, ma compagni di strada.",
                    'consiglio': "🌋 La tua forza è immensa, ma se la usi per combattere, ti logora. Impara a deporre le armi, a fidarti, a lasciare spazio. La vera potenza non è dominare, ma trasformare. E la pace interiore è la più grande delle vittorie."
                }
            },

            'sole_ascendente_opposizione': {
                'opposizione': {
                    'titolo': "☀️⬆️ Sole in opposizione all'Ascendente",
                    'messaggio': "Hai una grande ammirazione per le persone di successo, per chi ce l'ha fatta. E in fondo al cuore speri che loro possano ammirare te. Per questo ti adatti, ti annulli, cerchi di compiacere. Ma così facendo, perdi la tua identità. La gente non ti prende sul serio perché non capisce chi sei veramente. Invece di cercare conferme fuori, dovresti cercarle dentro. Hai tutte le qualità per farti valere, ma devi smettere di aspettare il permesso. La prossima volta, prova a dire quello che pensi davvero. Qualcuno storcerà il naso, ma qualcun altro ti rispetterà di più. E tu ti sentirai finalmente viva, finalmente te stessa.",
                    'consiglio': "🦎 Il camaleonte si mimetizza per sopravvivere, ma tu non devi sopravvivere, devi vivere. Mostra il tuo vero colore, anche se è scomodo. Chi ti ama amerà quello, non il travestimento. E l'amore che riceverai sarà finalmente vero."
                }
            },

            # LUNA (opposizioni)
            'luna_mercurio_opposizione': {
                'opposizione': {
                    'titolo': "🌙💬 Luna in opposizione a Mercurio",
                    'messaggio': "Il tuo cuore e la tua mente a volte vanno in direzioni opposte. Quando dovresti usare la logica, ti fai trascinare dalle emozioni. Quando dovresti ascoltare i sentimenti, diventi fredda e razionale. Questa confusione ti porta a dire o fare la cosa sbagliata al momento sbagliato, e la gente si allontana senza che tu capisca perché. In realtà sei una persona sensibile, che ha solo bisogno di imparare a fare una pausa tra ciò che senti e ciò che dici. Ascoltare di più, parlare di meno. E soprattutto, essere più indulgente con te stessa. Non sei obbligata a essere perfetta, a dire sempre la cosa giusta. Basta che tu sia autentica.",
                    'consiglio': "🧠 Il cuore e la mente non sono nemici, sono due amiche che devono imparare a collaborare. Ascoltale entrambe, ma decidi con calma. Le parole sono come frecce: una volta lanciate, non tornano indietro. Sceglile con cura, e impara a perdonarti quando sbagli."
                }
            },

            'luna_venere_opposizione': {
                'opposizione': {
                    'titolo': "🌙❤️ Luna in opposizione a Venere",
                    'messaggio': "Hai un grande bisogno di amare e di essere amata. Per questo fai di tutto per piacere, per essere accettata. Fai complimenti, regali, favori, sperando che gli altri ti ricambino con affetto. Ma spesso questo tuo modo di fare viene frainteso: la gente pensa che tu voglia qualcosa in cambio, e si mette sulla difensiva. In realtà cerchi solo un po' di calore, di conferma. Ma l'amore non si compra con i favori, né si ottiene con le lusinghe. Forse dovresti provare a startene un po' in silenzio, a osservare, a dare senza pretendere nulla. E a capire che il tuo valore non dipende da quanto gli altri ti apprezzano. Tu vali, punto. Anche quando nessuno te lo dice.",
                    'consiglio': "💖 L'amore non si compra, non si merita, non si conquista. L'amore semplicemente c'è, quando due anime si riconoscono. Impara a startene in silenzio accanto, a dare senza aspettarti nulla. La tua presenza vale più di mille regali."
                }
            },

            'luna_marte_opposizione': {
                'opposizione': {
                    'titolo': "🌙🔥 Luna in opposizione a Marte",
                    'messaggio': "Sei una donna di passione, di slancio. Quando ti arrabbi, è un temporale. Quando ami, è un incendio. Questa tua intensità è affascinante, ma a volte spaventa. Ti butti in relazioni senza pensarci, e poi scopri che hai scelto la persona sbagliata. Sul lavoro, non sopporti critiche e regole, e i superiori ce l'hanno con te. Dici che sono loro il problema, ma forse sei tu che reagisci in modo troppo impulsivo. La tua rabbia è come un fuoco: se la alimenti, brucia tutto. Se impari a controllarla, ti scalda. Forse hai solo bisogno di respirare, di contare fino a dieci, di scegliere le battaglie che meritano di essere combattute. La vita è più bella se non sei sempre pronta a lottare.",
                    'consiglio': "🔥 La tua passione è un dono, ma non deve trasformarsi in rabbia. Impara a respirare, a contare fino a dieci, a distinguere ciò che merita la tua energia da ciò che è solo rumore. La calma non è resa, è saggezza."
                }
            },

            'luna_giove_opposizione': {
                'opposizione': {
                    'titolo': "🌙✨ Luna in opposizione a Giove",
                    'messaggio': "Hai un cuore grande, generoso. Ti butti nelle relazioni con entusiasmo, fai di tutto per gli altri, a volte troppo. Questa tua generosità è meravigliosa, ma rischi di essere sfruttata. La gente si abitua al tuo dare e non si chiede mai cosa ricevi tu in cambio. E quando resti sola, ti lamenti, ma forse non hai mai imparato a dire di no. In amore, per conquistare qualcuno, faresti qualsiasi cosa. Ma così ti svendi. Prima di buttarti, assicurati che chi hai davanti meriti il tuo tempo. E impara a coltivare anche i tuoi interessi, la tua vita, al di là delle relazioni. La felicità non dipende solo da quanto dai, ma anche da quanto sai ricevere e, soprattutto, da quanto sai stare bene con te stessa.",
                    'consiglio': "✨ La tua generosità è un dono prezioso, ma non devi regalarla a tutti. Impara a distinguere chi merita il tuo tempo da chi vuole solo approfittare. Il tuo valore non si misura da quanto ti sacrifichi, ma da quanto sei capace di amarti per prima."
                }
            },

            'luna_saturno_opposizione': {
                'opposizione': {
                    'titolo': "🌙⏳ Luna in opposizione a Saturno",
                    'messaggio': "Hai un'anima antica, profonda. Porti dentro di te il peso di responsabilità che ti sono state affidate fin da bambina. Forse sei cresciuta troppo in fretta, e ora fatichi a lasciarti andare, a fidarti della vita. Hai sempre la sensazione che qualcosa possa andare storto, e questa paura ti blocca. Preferisci stare con persone più grandi, più esperte, perché con i coetanei non ti senti al sicuro. In amore, rivivi le stesse dinamiche di sottomissione che hai conosciuto in famiglia. Ma non sei più quella bambina. Oggi puoi scegliere. Puoi permetterti di essere felice, senza sensi di colpa. Il passato è una radice, non una catena. Onora chi ti ha cresciuto, ma vivi la tua vita.",
                    'consiglio': "⏳ Il passato ti ha resa forte, ma non deve imprigionarti. Non sei più quella bambina che doveva dimostrare qualcosa. Oggi puoi scegliere di essere felice. Permettitelo. La gioia non è un tradimento, è un diritto."
                }
            },

            'luna_urano_opposizione': {
                'opposizione': {
                    'titolo': "🌙⚡ Luna in opposizione a Urano",
                    'messaggio': "Sei una donna unica, originale, con una mente libera e anticonformista. La tua indipendenza è la tua bandiera. Ma questa tua voglia di libertà a volte ti porta a scegliere relazioni strane, complicate, impossibili. Forse perché hai paura di impegnarti davvero, di legarti. Così preferisci storie che sai già che finiranno, per non dover affrontare la paura dell'abbandono. Ma intanto resti sola, e ti lamenti. In realtà sogni un amore vero, profondo, che ti accetti per quello che sei senza volerti cambiare. Prova a essere normale, a mostrarti per quello che sei, senza paura. Scoprirai che anche gli altri hanno le tue stesse paure. E che l'amore vero non è una gabbia, è un volo in due.",
                    'consiglio': "⚡ La tua originalità è un dono, ma non deve diventare una fuga. Prova a fidarti, a lasciarti andare, a mostrarti per quello che sei. L'amore vero non ti imprigionerà, ti darà ali per volare insieme. E la normalità non è noia, è il terreno dove crescono le cose vere."
                }
            },

            'luna_nettuno_opposizione': {
                'opposizione': {
                    'titolo': "🌙🌊 Luna in opposizione a Nettuno",
                    'messaggio': "Hai un'anima di artista, una sensibilità che ti permette di vedere la bellezza dove altri non la vedono. Vivi in un mondo di emozioni, di sogni, di intuizioni. A volte però fatichi a distinguere la realtà dalla fantasia, e questo ti porta a illuderti sulle persone. Le vedi migliori di quello che sono, e quando mostrano i loro limiti, crolli. In amore, continui a cercare l'ideale, ma l'ideale non esiste. Forse è ora di accettare che le persone sono imperfette, e che proprio nelle imperfezioni si nasconde la vera bellezza. Impara a vedere con occhi nuovi, a distinguere senza giudicare. La realtà può essere meno affascinante dei sogni, ma è l'unico posto dove puoi trovare l'amore vero.",
                    'consiglio': "🌊 I tuoi sogni sono ali meravigliose, ma per volare hai bisogno anche di piedi per terra. Impara a distinguere l'illusione dalla verità, senza perdere la tua magia. Le persone vanno amate per quello che sono, non per quello che immagini. E l'imperfezione è il luogo dove abita l'autenticità."
                }
            },

            'luna_plutone_opposizione': {
                'opposizione': {
                    'titolo': "🌙🌋 Luna in opposizione a Plutone",
                    'messaggio': "Ami con una intensità che pochi possono capire. Quando dai il cuore, lo dai tutto, senza riserve. Questa tua profondità è meravigliosa, ma a volte diventa possessiva, gelosa. Hai paura di perdere chi ami, e questa paura ti porta a voler controllare, a stringere troppo. Ma l'amore è come l'acqua: più stringi, più ti scivola via. Forse hai dentro di te ferite antiche, che ti hanno insegnato che amare significa soffrire. Ma non è così. L'amore vero è respiro, è spazio, è fiducia. Impara a lasciare andare, a respirare insieme. La tenerezza non è debolezza, è la forma più alta di forza.",
                    'consiglio': "🌋 La tua intensità è un dono, ma non deve diventare una gabbia. Impara a lasciare spazio, a fidarti, a respirare insieme. L'amore non è possesso, è condivisione. Più apri le mani, più puoi ricevere. La vera intimità non è fusione, è danza a due."
                }
            },

            'luna_ascendente_opposizione': {
                'opposizione': {
                    'titolo': "🌙⬆️ Luna in opposizione all'Ascendente",
                    'messaggio': "Hai un cuore grande, sempre pronto ad accogliere gli altri, a capirli, a sostenerli. Ti perdi nei problemi di chi ami, fai tuoi i loro dolori. Questa tua empatia è un dono prezioso, ma a volte ti fa dimenticare di te stessa. Hai bisogno di sentirti utile, necessaria, perché è l'unico modo che conosci per sentirti al sicuro. Ma così facendo, rischi di perdere la tua identità. In amore, accetti compromessi, ti annulli, pur di non essere lasciata. Ma la persona giusta non ti chiederà di rimpicciolirti. Impara a startene in piedi da sola, a bastarti. Solo allora potrai incontrare qualcuno che ti stia accanto senza bisogno che tu ti sacrifichi.",
                    'consiglio': "🌙 La tua bontà è immensa, ma non deve diventare una catena. Non hai bisogno di essere indispensabile per essere amata. Impara a stare bene con te stessa, a coltivare i tuoi interessi, la tua vita. La persona giusta arriverà quando tu sarai pronta a incontrarla da pari a pari."
                }
            },

            # MERCURIO (opposizioni)
            'mercurio_marte_opposizione': {
                'opposizione': {
                    'titolo': "💬🔥 Mercurio in opposizione a Marte",
                    'messaggio': "La tua mente è una fucina di idee, brillante, veloce, creativa. Hai il dono della parola e sai difendere le tue opinioni con passione. A volte però questa tua facilità di parola diventa tagliente, e senza volere ferisci chi ti sta accanto. La gente si mette sulla difensiva, si allontana, e tu non capisci perché. In realtà dietro la tua assertività c'è solo il desiderio di essere ascoltata, riconosciuta. Forse puoi imparare a moderare i toni, a scegliere le parole con più cura, a lasciare spazio anche agli altri. La tua intelligenza è un diamante grezzo: se impari a tagliarlo con dolcezza, brillerà senza ferire.",
                    'consiglio': "🗣️ La tua parola è un dono, ma come ogni dono va usato con cura. Impara ad ascoltare prima di parlare, a dubitare prima di affermare. La vera intelligenza non è avere sempre ragione, ma saper costruire ponti con le parole."
                }
            },

            'mercurio_giove_opposizione': {
                'opposizione': {
                    'titolo': "💬✨ Mercurio in opposizione a Giove",
                    'messaggio': "Sei curiosa, appassionata, sempre pronta a imparare cose nuove. La tua mente spazia in tanti campi, e questo è meraviglioso. A volte però ti butti in troppe cose contemporaneamente, e fatichi a portarle a termine. Inizi con entusiasmo, poi ti stanchi e lasci perdere. In amore, fai promesse che non mantieni, non per cattiveria, ma perché ti lasci trascinare dall'emozione del momento. Hai bisogno di disciplina, di costanza, di imparare a finire ciò che inizi. La cultura è importante, ma da sola non basta. Ci vuole umiltà, ci vuole ascolto. Scegli una strada, una sola, e percorrila con pazienza. I frutti arriveranno, se impari a coltivare.",
                    'consiglio': "📚 La tua sete di conoscenza è preziosa, ma la saggezza sta nell'approfondire, non nel moltiplicare. Impara a portare a termine ciò che inizi, a mantenere le promesse. La tua mente brillerà ancora di più quando saprà concentrarsi."
                }
            },

            'mercurio_saturno_opposizione': {
                'opposizione': {
                    'titolo': "💬⏳ Mercurio in opposizione a Saturno",
                    'messaggio': "Sei una donna seria, profonda, che non si accontenta delle apparenze. Hai una mente analitica e precisa, e questo è un grande dono. A volte però questa tua precisione diventa rigidità: critichi tutto e tutti, e fatichi ad accettare punti di vista diversi. La gente si stanca, si allontana, e tu resti sola con le tue certezze. In realtà hai solo paura di sbagliare, di non essere all'altezza. Per questo tieni tutto sotto controllo. Ma la vita è imprevedibile, e la perfezione non esiste. Impara a lasciar andare, a fidarti un po' di più. A volte l'imperfezione è più bella della precisione. E gli errori sono solo opportunità per crescere.",
                    'consiglio': "⏳ La precisione è una virtù, ma la rigidità è un difetto. Impara a distinguere ciò che è importante da ciò che non lo è. Lascia andare il controllo, fidati della vita. La perfezione è un'illusione, la bellezza sta nell'imperfezione."
                }
            },

            'mercurio_urano_opposizione': {
                'opposizione': {
                    'titolo': "💬⚡ Mercurio in opposizione a Urano",
                    'messaggio': "Hai una mente geniale, originale, capace di vedere oltre. Le tue idee sono innovative, a volte profetiche. Ma questo tuo dono a volte ti isola: la gente non ti capisce, si sente a disagio, e tu resti sola con la tua intelligenza. In realtà hai solo bisogno di imparare a comunicare con più dolcezza, a dosare la tua sincerità. La verità è importante, ma lo è anche il modo in cui la dici. In amore, pretendi che il partner sia sincero, ma a volte le tue parole sono così dirette da ferire. Forse puoi imparare a usare il cuore oltre che la testa. Le persone non sono problemi da risolvere, ma anime da incontrare.",
                    'consiglio': "⚡ La tua mente è un faro, ma non deve accecare. Impara a dire le cose con amore, non solo con lucidità. La verità senza compassione diventa violenza. Usa il tuo dono per illuminare, non per ferire. E ricorda: le parole possono costruire ponti o muri. Scegli con cura."
                }
            },

            'mercurio_nettuno_opposizione': {
                'opposizione': {
                    'titolo': "💬🌊 Mercurio in opposizione a Nettuno",
                    'messaggio': "Hai un'anima di poetessa, una fantasia che vola alta. Vedi la bellezza dove altri non la vedono, e questo è un dono prezioso. A volte però questa tua sensibilità ti rende vulnerabile: fatichi a distinguere la realtà dalla fantasia, e ti lasci ingannare dalle apparenze. La gente ti dice che i tuoi sogni sono irrealizzabili, e tu ci credi. Perdi fiducia, ti chiudi. In amore, hai paura di essere ingannata, e questo ti impedisce di fidarti. In realtà hai solo bisogno di imparare a proteggerti senza chiuderti. La vita è fatta anche di persone sincere. Impara a riconoscerle, a fidarti un po' di più. La felicità è dall'altra parte della paura.",
                    'consiglio': "🌊 La tua anima è un sogno ad occhi aperti, ma i sogni hanno bisogno di aria per volare. Non chiuderti nel tuo mondo: là fuori c'è qualcuno che ti aspetta, con i piedi per terra e il cuore in mano. Impara a fidarti, a rischiare. La felicità merita il coraggio di crederci."
                }
            },

            'mercurio_plutone_opposizione': {
                'opposizione': {
                    'titolo': "💬🌋 Mercurio in opposizione a Plutone",
                    'messaggio': "Hai una mente profonda, capace di andare al cuore delle cose. Vedi ciò che si nasconde sotto la superficie, e questo ti rende una persona acuta e perspicace. A volte però questa tua profondità diventa ossessiva: vuoi capire tutto, controllare tutto, e non dai tregua a te stessa né agli altri. Sul lavoro, questa tua determinazione può portarti lontano, ma rischi di creare conflitti con chi non capisce la tua intensità. In amore, sei passionale e fedele, ma anche possessiva e gelosa. Forse puoi imparare a lasciar andare, a fidarti che non tutto deve essere scoperto, non tutto deve essere controllato. La fiducia si costruisce, non si impone. E a volte i misteri più belli sono quelli che restano tali.",
                    'consiglio': "🌋 La tua profondità è un dono, ma non tutto va dissepolto. Impara a rispettare i misteri, tuoi e altrui. La fiducia si costruisce con il tempo, con la pazienza, con la dolcezza. Non devi vincere ogni battaglia. A volte la vittoria più grande è lasciar perdere."
                }
            },

            'mercurio_ascendente_opposizione': {
                'opposizione': {
                    'titolo': "💬⬆️ Mercurio in opposizione all'Ascendente",
                    'messaggio': "Hai un grande desiderio di piacere, di essere accettata. Per questo ascolti prima cosa dicono gli altri, poi decidi cosa pensare. Ma così facendo, perdi la tua autenticità. La gente non ti prende sul serio, perché non capisce chi sei veramente. In realtà sei simpatica, brillante, quando parli sai incantare. Ma questa tua mania di compiacere ti rende poco credibile. Forse hai paura di essere rifiutata, e allora ti nascondi dietro una maschera. Ma la maschera stanca, prima o poi. Impara a mostrarti per quello che sei, con le tue idee, le tue opinioni, anche se scomode. Chi ti amerà, amerà quella. Chi non lo farà, non era per te.",
                    'consiglio': "💬 La maschera stanca, il trucco cola, e sotto rimani tu. Nuda, vera, imperfetta. Mostrati così, senza paura. Chi ti ama non ha bisogno che tu sia diversa. E tu, finalmente, potrai respirare."
                }
            },

            # VENERE (opposizioni)
            'venere_marte_opposizione': {
                'opposizione': {
                    'titolo': "❤️🔥 Venere in opposizione a Marte",
                    'messaggio': "Sei una donna magnetica, passionale. La tua energia attrae, il tuo sguardo incanta. In amore, però, questa tua intensità a volte diventa travolgente. Vuoi tutto e subito, e quando l'altro non risponde come vorresti, ti senti ferita, tradita. In realtà dentro di te c'è una grande insicurezza: hai paura di non essere abbastanza, e allora usi il fascino per dominare. Ma l'amore non è dominio, è incontro. Forse puoi imparare a rallentare, a dare tempo, a lasciare spazio. La passione è un fuoco che scalda, ma se divampa brucia. L'amore vero ha bisogno di pazienza, di dolcezza, di attesa. E quando arriva, non è una conquista, è un dono.",
                    'consiglio': "🔥 La tua passione è un dono, ma non deve diventare una fiamma che brucia. Impara a dosare la tua energia, a dare spazio, a respirare insieme. L'amore non è una conquista, è un incontro. E gli incontri veri hanno bisogno di tempo, di silenzio, di rispetto."
                }
            },

            'venere_giove_opposizione': {
                'opposizione': {
                    'titolo': "❤️✨ Venere in opposizione a Giove",
                    'messaggio': "Hai un grande bisogno di essere amata, approvata, accettata. Per questo fai di tutto per piacere, per essere all'altezza delle aspettative altrui. Sei sempre d'accordo con tutti, non contraddici mai, ti adatti alle mode, alle idee, ai gusti degli altri. Ma dentro di te non sei così. Dentro di te c'è un mondo di opinioni, di desideri, di voglia di essere te stessa. Hai paura di mostrarti, paura di non piacere. In amore, questo si traduce in relazioni in cui dai tanto, ma forse troppo, e poi resti delusa. Forse è il momento di fare un esame di coscienza: cosa vuoi veramente? L'approvazione degli altri o la tua felicità? La vera libertà è essere te stessa, anche se qualcuno non ti capisce.",
                    'consiglio': "✨ L'approvazione degli altri è come una droga: più ne prendi, più ne vuoi. Ma non riempie il vuoto. Il vuoto si riempie solo con la verità. Quella tua, autentica, senza maschere. Mostrati per quello che sei, e vedrai che qualcuno resterà. E sarà amore vero."
                }
            },

            'venere_saturno_opposizione': {
                'opposizione': {
                    'titolo': "❤️⏳ Venere in opposizione a Saturno",
                    'messaggio': "Hai un cuore grande, ma lo tieni chiuso in una cassaforte. Forse da bambina hai imparato che amare significa soffrire, e ora hai paura di riprovarci. Ti senti inadeguata, meno bella, meno brava delle altre. In ogni relazione ti metti un gradino più in basso, fai concessioni, ti annulli. Speri che così ti ameranno. Ma non funziona. Chi ti ama non vuole una persona che si rimpicciolisce, vuole una donna intera. Forse è il momento di smetterla di confrontarti con le altre, di giudicarti con i loro occhi. Hai talento, hai capacità, hai un cuore meraviglioso. Usali per te, non per comprare l'affetto che non hai mai avuto. L'amore può aspettare: meglio sola che male accompagnata. La persona giusta arriverà quando tu sarai pronta a incontrarla da pari a pari.",
                    'consiglio': "⏳ Non sei quella bambina che si sentiva sbagliata. Oggi sei una donna, e puoi scegliere. Scegli di amarti, di rispettarti, di non accettare briciole. La persona giusta non ti chiederà di rimpicciolirti, ma di stare al suo fianco, grande quanto lei."
                }
            },

            'venere_urano_opposizione': {
                'opposizione': {
                    'titolo': "❤️⚡ Venere in opposizione a Urano",
                    'messaggio': "Sei una donna libera, indipendente, che non si accontenta delle storie ordinarie. Cerchi l'emozione, la scintilla, il brivido. Per questo ti innamori spesso di persone impossibili, già impegnate, o comunque difficili da raggiungere. Forse perché hai paura di legarti davvero, di impegnarti. Così preferisci storie che sai già che finiranno, per non dover affrontare la paura dell'abbandono. Ma intanto accumuli esperienze, ma anche solitudine. In realtà sogni un amore vero, profondo, che ti accetti per quello che sei senza volerti cambiare. Forse è il momento di rallentare, di dare una possibilità alle cose semplici, che durano. L'amore vero non è un fuoco d'artificio, è una fiamma che scalda ogni giorno.",
                    'consiglio': "⚡ La vita non è una corsa, è un viaggio. Se corri sempre, ti perdi il paesaggio. Impara a rallentare, a godere delle cose semplici, a costruire relazioni che durano. L'eccitazione passa, l'amore resta. Scegli cosa vuoi seminare."
                }
            },

            'venere_nettuno_opposizione': {
                'opposizione': {
                    'titolo': "❤️🌊 Venere in opposizione a Nettuno",
                    'messaggio': "Hai un'anima romantica, idealista. Vedi gli altri come vorresti che fossero, non come sono. Dipingi le persone con i colori dei tuoi sogni, e poi, quando la realtà si mostra, crolli. In amore, questa è la tua croce e la tua delizia. Ti innamori dell'idea, non della persona. E poi soffri, e ti chiudi. Inizi a vedere inganni dappertutto, a dubitare di chi ti vuole bene. Ma la colpa non è loro, è tua. Tu li hai idealizzati, loro sono solo umani. Forse è ora di scendere dalle nuvole e guardare le persone negli occhi. Saranno imperfette, ma saranno vere. E la verità, anche se meno affascinante dei sogni, è l'unica base su cui costruire qualcosa di solido.",
                    'consiglio': "🌊 L'ideale è una stella che illumina, ma non scalda. L'amore vero è il fuoco che arde nel camino di casa. Impara a scendere dalle nuvole e a guardare le persone per quello che sono. L'imperfezione è il luogo dove abita l'autenticità. E l'autenticità è l'unica strada per l'amore vero."
                }
            },

            'venere_plutone_opposizione': {
                'opposizione': {
                    'titolo': "❤️🌋 Venere in opposizione a Plutone",
                    'messaggio': "Le tue emozioni sono un oceano profondo. Quando ami, ami in modo totalizzante, senza riserve. Questa tua intensità è meravigliosa, ma a volte diventa opprimente. Pretendi tutto dall'altro, e se non ricevi, ti senti tradita. Sei gelosa, possessiva, e non lo ammetti. In realtà hai paura di perdere, di essere abbandonata. Per questo stringi così forte. Ma l'amore è come l'acqua: più stringi, più ti sfugge. Forse puoi imparare a fidarti, a lasciare spazio, a respirare insieme. La persona che ami non è tua, è con te. Rispetta la sua libertà, le sue differenze. Solo così potrete crescere insieme, senza soffocarvi. La tenerezza non è debolezza, è la forma più alta di amore.",
                    'consiglio': "🌋 L'amore non è una fortezza da difendere, è un giardino da condividere. Impara a non confondere la passione con il possesso. La persona che ami non è tua, è con te. Rispetta il suo spazio, la sua libertà, le sue differenze. Solo così potrete fiorire insieme."
                }
            },

            'venere_ascendente_opposizione': {
                'opposizione': {
                    'titolo': "❤️⬆️ Venere in opposizione all'Ascendente",
                    'messaggio': "Sei affascinata da persone di classe, raffinate, di successo. E fai di tutto per piacere loro. Hai modi gentili, educati, e sai mettere gli altri a loro agio. La gente ti adora, dice che sei squisita. Ma sotto questa facciata perfetta si nasconde una grande insicurezza. Hai bisogno di essere circondata, sostenuta, approvata. Per questo frequenti solo persone che possono esserti utili, che hanno successo. Ma attenta: le relazioni costruite sull'interesse sono fragili come vetro. Quando la situazione cambia, gli amici spariscono. Forse è il momento di mostrarti per quello che sei, senza calcoli. Di scoprire che qualcuno potrebbe amarti anche senza il tuo curriculum. E che tu puoi amare senza dover dimostrare niente.",
                    'consiglio': "💖 La tua gentilezza è un'arte, ma non deve diventare una strategia. Le persone non sono gradini, sono anime. Se le usi per salire, quando cadi non ci sarà nessuno a sostenerti. Prova a essere vera, a mostrarti senza maschere. Chi ti amerà, amerà te, non il tuo biglietto da visita."
                }
            },

            # MARTE (opposizioni)
            'marte_giove_opposizione': {
                'opposizione': {
                    'titolo': "🔥✨ Marte in opposizione a Giove",
                    'messaggio': "Sei una combattiva, una che non molla mai. Le sfide ti elettrizzano, le competizioni ti esaltano. Questa tua energia è contagiosa e ti porta lontano. A volte però ti lanci senza pensare, fai il passo più lungo della gamba, e poi ti ritrovi a rimuginare sugli errori. Non sopporti chi è più bravo di te, e questo ti porta a essere competitiva anche quando non serve. In realtà hai solo bisogno di imparare a moderare la tua foga, a goderti il viaggio senza pensare solo alla meta. In amore, sei passionale e intensa, ma a volte pretendi troppo dal partner. Forse puoi rallentare, respirare, goderti il presente. La vita non è solo traguardi, è anche il paesaggio che attraversi.",
                    'consiglio': "🔥 La tua energia è un cavallo selvaggio. Domarlo non significa spegnerlo, ma dargli una direzione. Impara a scegliere le battaglie, a rispettare i tempi, a goderti il percorso. La vita non è solo traguardi, è anche il paesaggio che attraversi. Rallenta, respira, ammira."
                }
            },

            'marte_saturno_opposizione': {
                'opposizione': {
                    'titolo': "🔥⏳ Marte in opposizione a Saturno",
                    'messaggio': "Sei come un motore che va a scoppio: momenti di grande energia alternati a momenti di stanchezza e apatia. Non c'è equilibrio, non c'è pace. Quando sei su, macini risultati, quando sei giù, non ti muovi. E ti rimproveri, ti senti in colpa. In realtà hai paura di non farcela, e questa paura ti blocca. Guardi le altre donne che ce la fanno e ti sembra che siano migliori. Invece no, sono solo più costanti. Tu hai le stesse capacità, ma non le usi con continuità. In amore, è lo stesso: all'inizio sei tutta fiamma, poi ti stanchi e ti ritiri. Forse è il momento di chiederti cosa vuoi veramente. E poi di impegnarti per ottenerlo, un passo alla volta, senza fretta, ma senza fermarti.",
                    'consiglio': "⏳ La costanza è la virtù dei forti. Non serve a nulla partire in quarta se poi ti fermi al primo ostacolo. Impara a camminare al tuo ritmo, senza confrontarti con le altre. Ogni passo, anche piccolo, è un progresso. L'importante è non fermarsi."
                }
            },

            'marte_urano_opposizione': {
                'opposizione': {
                    'titolo': "🔥⚡ Marte in opposizione a Urano",
                    'messaggio': "Hai un talento naturale per l'originalità, per l'innovazione. Sei una pioniera, una che non sta alle regole. Questo tuo spirito ribelle è affascinante, ma a volte ti porta a essere in conflitto con tutti. La gente si sente sfidata dalla tua energia, e si allontana. In realtà dietro la tua ribellione c'è solo il desiderio di essere libera, di non essere incasellata. Ma la libertà non è combattere contro tutto, è scegliere con saggezza le proprie battaglie. In amore, sei affascinante ma difficile: appena la relazione si fa seria, scappi. Forse hai paura di legarti, di perdere la tua indipendenza. Ma l'amore vero non imprigiona, libera. Prova a fidarti, a lasciarti andare. Scoprirai che puoi essere libera anche in due.",
                    'consiglio': "⚡ La tua ribellione è un vento che spazza, ma senza direzione diventa solo distruzione. Impara a incanalare la tua energia in qualcosa di creativo. L'arte, l'innovazione, la scoperta: lì sì che puoi fare la differenza. E senza dover combattere con nessuno."
                }
            },

            'marte_nettuno_opposizione': {
                'opposizione': {
                    'titolo': "🔥🌊 Marte in opposizione a Nettuno",
                    'messaggio': "Hai un animo complesso, fatto di luce e ombra. Da una parte vorresti agire, buttarti, vivere. Dall'altra ti blocchi, cadi nell'apatia, e non capisci perché. Le tue emozioni sono profonde, a volte confuse. In amore, questo è particolarmente difficile: attiri persone sbagliate, già impegnate, o comunque non disponibili. E poi soffri, e ti senti in colpa. Forse è colpa dell'educazione ricevuta, forse di esperienze passate. Ma puoi cambiare le cose. Hai bisogno di un lavoro che ti permetta di esprimere la tua sensibilità senza farti male: l'arte, la musica, l'assistenza. E in amore, impara a vedere le persone per quello che sono, non per quello che sembrano. La chiarezza è la tua alleata. Cercala, dentro e fuori.",
                    'consiglio': "🌊 La tua anima è un oceano profondo, ma anche l'oceano ha bisogno di calma per riflettere il cielo. Impara a calmare le onde, a cercare la chiarezza. Le persone non sono enigmi da risolvere, sono compagni di viaggio. Guardale con occhi nuovi, senza sospetto, senza paura. La sincerità è l'unica via."
                }
            },

            'marte_plutone_opposizione': {
                'opposizione': {
                    'titolo': "🔥🌋 Marte in opposizione a Plutone",
                    'messaggio': "Sei una donna di una forza straordinaria. La tua energia è potente, magnetica. A volte però questa forza diventa distruttiva, per te e per chi ti sta accanto. Vedi nemici dappertutto, costruisci barriere inutili. In amore, sei passionale e fedele, ma anche possessiva e gelosa. Il potere ti affascina: averlo sugli altri, o subirlo. Sei sempre in bilico tra dominare ed essere dominata. In realtà hai solo paura di essere ferita, e allora attacchi per prima. Ma la guerra stanca anche i vincitori. Forse è il momento di abbassare le armi, di imparare l'arte del compromesso. Non è resa, è intelligenza. La vita non è una battaglia, è un viaggio da condividere. E la pace interiore è la più grande delle vittorie.",
                    'consiglio': "🌋 La tua forza è immensa, ma senza direzione diventa distruttiva. Impara a costruire argini, a canalizzare la tua energia. La vera potenza non è travolgere, è trasformare. Usa la tua passione per creare, non per distruggere. E ricorda: a volte la più grande vittoria è la pace."
                }
            },

            'marte_ascendente_opposizione': {
                'opposizione': {
                    'titolo': "🔥⬆️ Marte in opposizione all'Ascendente",
                    'messaggio': "Sembra che tu attiri sempre persone che ti mettono alla prova, che ti sfidano. Forse è il tuo modo di imparare a difenderti, a crescere. Ma la vita non dovrebbe essere una palestra. Sei polemica, litighi per niente, e poi ti lamenti che nessuno ti capisce. In realtà sei tu che non ti fai capire. Ti piazzi lì, con la tua arroganza, e aspetti che gli altri si adattino a te. Ma le relazioni sono fatte di dare e avere, di scendere a compromessi. Sul lavoro, i superiori non ti sopportano. Parli a sproposito, ti intrometti, fai domande che non dovresti fare. Sembra che tu voglia farti notare a tutti i costi. Ma attenta: a furia di farti notare, potresti farti male. Impara a stare al tuo posto, a rispettare le regole, a controllare la lingua. Non è umiliazione, è educazione. E poi, chissà, forse qualcuno inizierà ad apprezzarti davvero.",
                    'consiglio': "🔥 La tua grinta è una risorsa, ma senza disciplina diventa un difetto. Impara a scegliere le battaglie, a rispettare le regole, a convivere con le differenze. Non devi piacere a tutti, ma nemmeno farti nemici inutilmente. La vita è più semplice se smetti di combattere contro i mulini a vento."
                }
            },

            # GIOVE (opposizioni)
            'giove_saturno_opposizione': {
                'opposizione': {
                    'titolo': "✨⏳ Giove in opposizione a Saturno",
                    'messaggio': "Sei un'altalena di emozioni: un momento ti senti invincibile, quello dopo crolli. Cerchi continuamente qualcuno che ti dica che sei brava, che ce la farai. Ma se non lo fa, ti offendi e ti chiudi. Da piccola qualcuno ti ha fatto sentire inadeguata, e ora non sai più quanto vali. Sul lavoro, eviti le responsabilità come la peste. Preferisci stare nell'ombra, fare il minimo indispensabile. Peccato, perché hai un potenziale enorme. Ma per usarlo, devi prima fare pace con te stessa. In amore, è lo stesso: non dai mai abbastanza, hai paura di essere fregata. Poi, quando qualcuno ti lascia, ci resti male. Come ha potuto? Ma se non hai mai aperto il cuore? Forse è il momento di guardarti dentro, onestamente. Di ammettere che hai paura, che sei fragile. E di iniziare a costruire, un passo alla volta, senza pretendere di essere già arrivata.",
                    'consiglio': "⏳ L'incertezza è il prezzo della crescita. Non devi sapere tutto subito, non devi essere perfetta. Impara a camminare un passo alla volta, a sbagliare, a rialzarti. La fiducia in te stessa non viene dagli applausi, ma dalla consapevolezza che ce la puoi fare, anche cadendo."
                }
            },

            'giove_urano_opposizione': {
                'opposizione': {
                    'titolo': "✨⚡ Giove in opposizione a Urano",
                    'messaggio': "Sei un vulcano di idee, una mente geniale e innovativa. Fin da bambina hai dimostrato di avere qualcosa in più, e forse questo ti ha isolata. Ora sei una combattente, una che non molla. Nelle discussioni sei un leone, la tua intelligenza fulminea ti fa vincere sempre. Sembra che tu possa fare qualsiasi cosa. E forse è vero. Legge, politica, scienza, arte: qualsiasi campo tu scelga, puoi eccellere. Ma attenta a non diventare arrogante. La tua sicurezza a volte si trasforma in superbia, e perdi alleati preziosi. Ti stupisci che gli altri non vedano quello che vedi tu, e li disprezzi. Invece dovresti essere tollerante, capire che non tutti sono come te. La tua intelligenza è un dono, ma anche una responsabilità. Usala per costruire ponti, non per allargare fossati. E impara ad ascoltare, anche chi è più lenta, anche chi è diversa. Potresti scoprire che anche loro hanno qualcosa da insegnarti.",
                    'consiglio': "⚡ La tua mente è un faro, ma non deve accecare. La conoscenza senza umiltà è solo informazione. Usa il tuo dono per illuminare, non per giudicare. E ricorda: il mondo è pieno di luci diverse. Non c'è una più giusta, ci sono solo punti di vista. Impara a rispettarli tutti."
                }
            },

            'giove_nettuno_opposizione': {
                'opposizione': {
                    'titolo': "✨🌊 Giove in opposizione a Nettuno",
                    'messaggio': "Fai promesse che non mantieni. Non per cattiveria, ma perché ti lasci trascinare dall'entusiasmo. Poi, quando devi mantenere, non ce la fai. E allora trovi scuse, ti giustifichi, e intanto la gente si allontana. Pensi che gli altri pretendano troppo da te, e in un certo senso è vero. Ma forse sei tu che prometti troppo. Sul lavoro, ti trovi spesso oberata di responsabilità che non hai chiesto. Ma è perché non sai dire di no. In amore, metti la persona che ami su un piedistallo. La vedi perfetta, meravigliosa. Poi, quando scopri che è umana, crolli. E ti senti tradita. Invece non ti ha tradita nessuno, sei stata tu a illuderti. Impara a vedere le persone per quello che sono, non per quello che sogni. E impara a mantenere le promesse, o a non farle proprio. La parola data è sacra.",
                    'consiglio': "🌊 Le parole sono come uccelli: una volta volate via, non tornano più. Impara a dosare le promesse, a mantenere gli impegni. La fiducia si costruisce giorno per giorno, con i fatti. Le illusioni sono belle, ma la realtà è l'unico posto dove si vive. Scegli la realtà, anche se imperfetta."
                }
            },

            'giove_plutone_opposizione': {
                'opposizione': {
                    'titolo': "✨🌋 Giove in opposizione a Plutone",
                    'messaggio': "Non accetti idee diverse dalle tue. Le combatti, le smonti. Per te la verità è una sola: la tua. Così facendo, ti alieni le persone che potrebbero aiutarti. Ti senti un missionario, qualcuno che deve salvare il mondo. E la gente ti prende per una fanatica. In senso negativo, potresti usare questo tuo potere per dominare gli altri, per arricchirti con mezzi poco puliti. Attenta: le offerte che sembrano troppo belle per essere vere, di solito nascondono tranelli. In senso positivo, hai tutte le carte in regola per combattere le ingiustizie, per smascherare i corrotti. La tua voce è potente, i tuoi toni infuocati. Usali con saggezza. Non pensare di essere indispensabile. Il mondo non si salva da sola, ma nemmeno senza di te. Collabora, ascolta, impara. Solo così lascerai un segno.",
                    'consiglio': "🌋 La tua passione è una fiamma che può illuminare o bruciare. Scegli. L'arroganza è il peggior nemico della verità. Se vuoi cambiare il mondo, inizia da te. Poi, un passo alla volta, con umiltà e perseveranza, potrai davvero fare la differenza. Ma ricorda: non sei sola, e non sei indispensabile. La grandezza sta nel servire, non nel dominare."
                }
            },

            'giove_ascendente_opposizione': {
                'opposizione': {
                    'titolo': "✨⬆️ Giove in opposizione all'Ascendente",
                    'messaggio': "Sei generosa, educata, corretta. Con amici e nemici. La gente a volte pensa che tu abbia secondi fini, ma non è vero. Sei fatta così. Preferisci stare con persone di successo, perché ti motivano, ti spingono a dare il meglio. Sei ottimista, sicura che ce la farai. E forse è vero. Sai giudicare le persone, capisci cosa possono darti. Ma attenta a non diventare troppo egoista. A forza di prendere, senza dare, rischi di restare sola. Non metti radici, perché vuoi essere libera di cogliere le occasioni. Ma così facendo, passi per superficiale. Sei piena di idee, sai come usarle a tuo vantaggio. E sei anche un gran conversatore, simpatica, brillante. Forse tutta questa voglia di fare nasce da un'infanzia difficile, da una famiglia che non ti ha dato abbastanza. Ora cerchi di recuperare, di dimostrare a tutti quanto vali. Ma non dimenticare chi ti ha aiutata lungo il cammino. La gratitudine non è debolezza, è nobiltà.",
                    'consiglio': "🌟 La tua ambizione è la tua forza, ma non deve diventare la tua prigione. Impara a dare senza calcolare, a ringraziare senza vergogna. Le persone che incontri non sono solo mezzi per arrivare, sono fini in sé. Rispettale, amale, e loro faranno lo stesso con te. Il successo condiviso è l'unico che dura."
                }
            },

            # SATURNO (opposizioni)
            'saturno_urano_opposizione': {
                'opposizione': {
                    'titolo': "⏳⚡ Saturno in opposizione a Urano",
                    'messaggio': "Con la gente, hai spesso un atteggiamento di sfida. Sembra che tu voglia dimostrare qualcosa, ma in realtà ottieni solo di allontanare gli altri. Hai bisogno di qualcuno che ti calmi, che ti dia equilibrio, perché da sola tendi a perdere la bussola. Dovresti imparare ad ascoltare i consigli, a fidarti di chi ti vuole bene. Solo così troverai la libertà che cerchi. Sul lavoro, sei preparata: scienza, statistica, ricerca. Ma quando arrivi in alto, non giocare d'astuzia. Gli intrighi si ritorcono contro. E poi, smettila di voler partire dall'alto. La gavetta serve, insegna. Le persone che incontrerai lungo la strada saranno le tue migliori maestre. Con gli anni, imparerai a dare più valore alle cose dello spirito che ai beni materiali. E allora sarai davvero ricca. La persona che ami ti sostiene più di quanto credi. Ringraziala, ogni giorno.",
                    'consiglio': "⚡ La saggezza non sta nel non aver bisogno di nessuno, ma nel saper chiedere aiuto. La libertà non è fare tutto da sola, è scegliere con chi camminare. Impara a fidarti, a lasciarti guidare. Gli altri non sono nemici, sono compagni di viaggio. E il viaggio è più bello in compagnia."
                }
            },

            'saturno_nettuno_opposizione': {
                'opposizione': {
                    'titolo': "⏳🌊 Saturno in opposizione a Nettuno",
                    'messaggio': "Diffidi di tutti. Specialmente quando c'è competizione. Hai una paura irrazionale di fallire, e questa paura ti blocca. Così stai sulla difensiva, e gli altri si insospettiscono. È un cane che si morde la coda. Vorresti arrivare in alto, ma non hai il giudizio giusto per farlo. Vedi furbi e disonesti dappertutto, e così ti senti autorizzata a esserlo anche tu. Ma attenta: spesso fraintendi. La gente non è come la dipingi. Qualche volta ti impegni per cause sociali, per aiutare i deboli. Ma qualcuno mette in dubbio le tue motivazioni. Loro non capiscono che tu hai bisogno di espiare un senso di colpa, di sentirti parte di qualcosa. In amore, non sai distinguere il vero dal falso. E così finisci per essere fregata, o per stare sola. Forse è il caso di smetterla di vedere nemici dappertutto. Di guardare la realtà con occhi nuovi. Non tutti vogliono farti del male. Anzi, qualcuno ti vuole bene. Impara a riconoscerlo.",
                    'consiglio': "🌊 La paura è una lente che deforma tutto. Prova a toglierla, e vedrai il mondo con occhi nuovi. Non tutti sono nemici, non tutti vogliono ingannarti. C'è gente onesta, sincera, che ti vuole bene. Impara a fidarti, a rischiare. La solitudine è una difesa, ma anche una prigione. La vita è fuori."
                }
            },

            'saturno_plutone_opposizione': {
                'opposizione': {
                    'titolo': "⏳🌋 Saturno in opposizione a Plutone",
                    'messaggio': "La tua carriera è un campo minato. Spesso ti trovi in situazioni ambigue, con persone poco raccomandabili. Offerte di guadagni facili, lavori in zone grigie. Attenta: quello che sembra un affare potrebbe costarti caro. Lo stesso in amore: relazioni in cui dai tutto e ricevi niente, o peggio, vieni usata. La tua posizione sociale è instabile, i giochi di potere ti travolgono. Conosci persone che pretendono, che vogliono, che ti prosciugano. E tu cedi, per paura di perdere, per paura di restare sola. La miseria, la perdita dello status ti terrorizzano. E per questo sei disposta a tutto. Ma non è la strada giusta. Devi scegliere: o ti adatti a questo mondo marcio, o lo lasci e ricominci da capo. Non è facile, ma è l'unico modo per salvarti. Definisci i tuoi obiettivi, costruisci giorno per giorno, senza scorciatoie. La sicurezza non si compra, si costruisce. E si costruisce con onestà.",
                    'consiglio': "🌋 Le scorciatoie portano in posti dove non vuoi stare. La vera sicurezza non viene dai soldi facili, ma dalla consapevolezza di aver costruito con le tue mani. Giorno dopo giorno, mattone dopo mattone. Sarà fatica, ma sarà solido. E nessuno potrà portartelo via."
                }
            },

            'saturno_ascendente_opposizione': {
                'opposizione': {
                    'titolo': "⏳⬆️ Saturno in opposizione all'Ascendente",
                    'messaggio': "Hai costruito un muro intorno a te. Per proteggerti, dici. Ma in realtà ti sei imprigionata. La gente ti vede come distaccata, superba, e si tiene alla larga. Tu, dall'altra parte, ti lamenti che nessuno ti capisce. Pensi di non valere abbastanza, che le altre siano più brave, e nemmeno provi a metterti in gioco. Le sfide ti spaventano, le occasioni le lasci passare. Forse è colpa di un inizio difficile, di troppe critiche, di nessun incoraggiamento. Ora ti porti dietro quel peso. Anche le cose semplici, come chiedere un aumento, ti sembrano montagne. Preferisci startene nell'ombra, a fare il tuo dovere, senza disturbare. Ma così non cresci, non vivi. Dovresti provare a fare un passo, a rischiare un no. Potresti scoprire che non è così terribile. E che qualcuno, dall'altra parte, sta aspettando proprio te.",
                    'consiglio': "🛡️ Hai costruito un muro per proteggerti, e ora non vedi più cosa c'è dall'altra parte. Non devi abbatterlo tutto in una volta. Basta una piccola porta. Un passo, poi un altro. La timidezza non è un difetto, ma non deve diventare una prigione. Fuori c'è il mondo. Fuori c'è la vita. Meriti di vederla."
                }
            },

            # URANO (opposizioni)
            'urano_nettuno_opposizione': {
                'opposizione': {
                    'titolo': "⚡🌊 Urano in opposizione a Nettuno",
                    'messaggio': "Non ti rendi conto di quanto sei libera. Forse perché sei cresciuta in un ambiente che ti ha insegnato a ubbidire senza discutere. Ora che la tua libertà è in pericolo, tu non ti muovi. Lasci che siano gli altri a lottare. Ti sei identificata talmente con il tuo gruppo - politico, religioso, sociale - da aver dimenticato che hai il diritto di controllare chi ti rappresenta. I leader possono tradire, possono fare accordi segreti. La storia è piena di esempi. Sei nata in un periodo di grandi cambiamenti, di guerre, di rivoluzioni. L'indifferenza delle masse ha permesso il peggio. Tu percepisci quello che bolle in pentola, hai l'intuito per capire dove sta il pericolo. Allora usalo. Non stare a guardare. Il mondo ha bisogno di chi apre gli occhi. Ma attenta a non cadere nelle mani dei fanatici. La tua sensibilità potrebbe essere strumentalizzata.",
                    'consiglio': "👁️ La libertà non è un diritto che ti viene regalato. Si conquista ogni giorno. Se non la usi, la perdi. La tua intuizione è un radar: accendilo. Non delegare ad altri la difesa di ciò che è tuo. Il mondo cambia se qualcuno ha il coraggio di guardare oltre. Quel qualcuno potresti essere tu."
                }
            },

            'urano_ascendente_opposizione': {
                'opposizione': {
                    'titolo': "⚡⬆️ Urano in opposizione all'Ascendente",
                    'messaggio': "Attrai persone che vogliono essere libere, e la loro libertà finisce per limitare la tua. Ti irriti, ti arrabbi, ma ripeti sempre lo stesso schema. Ammiri chi non si lascia dominare, condividi il loro entusiasmo per l'indipendenza. Ma quando qualcuno cerca di legarti, scappi. I contratti ti sembrano gabbie, il matrimonio una prigione. Vorresti un amore senza vincoli. Ti circondi di amiche che la pensano come te, e con loro ti senti al sicuro. Sul lavoro, non sopporti orari e regole. Sei sempre stata ribelle. Ma questa tua voglia di libertà nasconde una paura: non sei pronta ad assumerti le conseguenze delle tue scelte. Per questo eviti le battaglie. Sogni di cambiare il mondo, ma non fai nulla di concreto. La tua missione potrebbe essere aiutare le altre a conquistare la libertà attraverso la conoscenza. Invece di fuggire, prova a costruire. Rimarrai sorpresa da quello che puoi fare.",
                    'consiglio': "🕊️ La libertà non è scappare, è scegliere dove stare. Puoi amare senza sentirti in gabbia, puoi seguire le regole senza sentirti sconfitta. La vera indipendenza è dentro di te. Se non sei libera nella tua testa, non lo sarai mai. Nemmeno in cima a una montagna."
                }
            },

            # NETTUNO (opposizioni)
            'nettuno_ascendente_opposizione': {
                'opposizione': {
                    'titolo': "🌊⬆️ Nettuno in opposizione all'Ascendente",
                    'messaggio': "Ti lasci influenzare troppo dalle persone che frequenti. Non sai distinguere chi è vera amica e chi è falsa. Qualcuno ne approfitta, gioca sulla tua sensibilità, ti fa sentire in obbligo. Quando scopri la verità, crolli. Per proteggerti, dovresti accertarti del reale bisogno di chi ti chiede aiuto. Tu ami tutti, ti preoccupi per tutti, forse perché non sopporti la solitudine. Hai bisogno di qualcuno che dipenda da te. Essere sola ti fa sentire inutile. Hai molta fantasia, potresti scrivere, dipingere, suonare. Ma dipendi dagli altri per vivere. E tendi a sminuirti, a mettere in luce i tuoi difetti. Non ti accorgi che le amiche ti vogliono bene. In amore, ti lasci affascinare da personalità forti. Prima di impegnarti, accertati che i sentimenti siano sinceri. Da entrambe le parti.",
                    'consiglio': "🌊 La tua anima è trasparente, ma non devi mostrarla a tutti. La sensibilità è un dono, ma va protetta. La solitudine non è un nemico, è lo spazio dove impari a starti bene. Quando ti basterai da sola, non avrai più paura di essere abbandonata. E allora potrai amare senza condizioni."
                }
            },

            # PLUTONE (opposizioni)
            'plutone_ascendente_opposizione': {
                'opposizione': {
                    'titolo': "🌋⬆️ Plutone in opposizione all'Ascendente",
                    'messaggio': "Attrai persone forti, di grande personalità. Ti piace andare in profondità, legare in modo intenso. Ma attenta: molti potrebbero cercarti per interesse. E tu, a tua volta, potresti fare lo stesso. Pretendi molto dagli altri, ma non sopporti che loro pretendano da te. È un gioco pericoloso. I simili si attraggono, e i giochi di potere possono rovinare anche le relazioni più belle. Il tuo vero talento è saper plasmare le persone. Per questo le relazioni pubbliche, la politica, le attività sociali sono il tuo campo. Sai parlare con autorevolezza, sai impressionare. Ottieni quasi sempre quello che vuoi. Se la tua motivazione è nobile, puoi fare miracoli. I tuoi nemici cercheranno di screditarti, ma tu hai informazioni che potresti usare. In amore, invece, le cose vanno peggio. Sei pesante, pedante, metti a disagio. Però sai capire il prossimo. Usa questo dono. Ma senza sopraffare.",
                    'consiglio': "🌋 Il potere è una lama: può tagliare o scolpire. Scegli. La forza non sta nel dominare gli altri, ma nel riconoscere la loro dignità. Le relazioni non sono giochi di potere, sono incontri. Se vuoi essere amata, impara a lasciare spazio. La grandezza non è piegare, è elevare."
                }
            }
        }
            

    def calcola_distanza_angolare(self, long1, long2):
        distanza = abs(long1 - long2)
        distanza = min(distanza, 360 - distanza)
        return distanza

    def trova_aspetto(self, distanza):
        for aspetto in self.aspetti:
            if abs(distanza - aspetto["gradi"]) <= aspetto["tolleranza"]:
                return aspetto
        return None

    def trova_gradi_aspetto(self, tipo_aspetto):
        aspetti = {
            "Congiunzione": 0, "Semisestile": 30, "Sestile": 60, "Trigono": 120,
            "Semiquadrato": 45, "Quadrato": 90, "Sesquiquadrato": 135,
            "Quinconce": 150
        }
        return aspetti.get(tipo_aspetto, 0)

    def calcola_percentuale_graduale(self, tipo_aspetto, distanza):
        gradi_ideali = self.trova_gradi_aspetto(tipo_aspetto)
        orbe_aspetti = {
            "Congiunzione": 7.0, "Sestile": 6.0, "Trigono": 8.0, 
            "Quadrato": 7.0, "Semisestile": 3.0, "Semiquadrato": 3.0, 
            "Sesquiquadrato": 3.0, "Quinconce": 3.0
        }
        orba = orbe_aspetti.get(tipo_aspetto, 5.0)
        scostamento = abs(distanza - gradi_ideali)
        if scostamento <= orba:
            percentuale = 1.0 - (scostamento / orba)
            percentuale = max(0.01, percentuale)
            return percentuale
        return 0.01

    def calcola_bonus_affinita(self, pianeta, segno_cuspide):
        bonus = 1.0
        if pianeta in self.domicili.get(segno_cuspide, []):
            bonus *= 2.0
        elif pianeta in self.esaltazioni.get(segno_cuspide, []):
            bonus *= 1.5
        return bonus

    def calcola_potenza_aspetto(self, pianeta, cuspide, tipo_aspetto, distanza, segno_cuspide=""):
        try:
            peso_pianeta = self.potenze_pianeti.get(pianeta, 10)
            peso_cuspide = self.potenze_case.get(cuspide, 8)
            
            pesi_aspetti = {
                "Congiunzione": 5, "Semisestile": 1, "Sestile": 2, "Trigono": 3,
                "Semiquadrato": -1, "Quadrato": -3, "Sesquiquadrato": -1, "Quinconce": -1
            }
            peso_aspetto = pesi_aspetti.get(tipo_aspetto, 0)
            
            potenza_massima = min(peso_pianeta, peso_cuspide) * peso_aspetto
            percentuale = self.calcola_percentuale_graduale(tipo_aspetto, distanza)
            potenza_base = potenza_massima * percentuale
            
            if segno_cuspide:
                bonus = self.calcola_bonus_affinita(pianeta, segno_cuspide)
                potenza_finale = potenza_base * bonus
            else:
                potenza_finale = potenza_base
            
            return round(potenza_finale, 1)
        except Exception as e:
            return 0

    def trova_aspetti_pianeta_cuspide(self, pianeti, case, segni_case=None):
        aspetti = []
        for p_nome, p_dati in pianeti.items():
            for c_nome, c_dati in case.items():
                distanza = self.calcola_distanza_angolare(
                    p_dati['longitudine_360'],
                    c_dati['cuspide_360']
                )
                aspetto = self.trova_aspetto(distanza)
                if aspetto:
                    segno = ""
                    if segni_case and c_nome in segni_case:
                        segno = segni_case[c_nome]
                    
                    potenza = self.calcola_potenza_aspetto(
                        p_nome, c_nome, aspetto['nome'], distanza, segno
                    )
                    
                    aspetti.append({
                        'pianeta': p_nome,
                        'cuspide': c_nome,
                        'aspetto': aspetto['nome'],
                        'tipo': aspetto['tipo'],
                        'distanza': round(distanza, 2),
                        'potenza': potenza
                    })
        return aspetti


# ============================================
# FUNZIONI DI UTILITÀ
# ============================================

def converti_gradi_in_segno(gradi):
    """
    Converte gradi 0-360 in gradi 0-30 con indicazione del segno
    """
    segni_con_simboli = [
        ("♈ Ariete", 0), ("♉ Toro", 30), ("♊ Gemelli", 60), ("♋ Cancro", 90),
        ("♌ Leone", 120), ("♍ Vergine", 150), ("♎ Bilancia", 180), ("♏ Scorpione", 210),
        ("♐ Sagittario", 240), ("♑ Capricorno", 270), ("♒ Acquario", 300), ("♓ Pesci", 330)
    ]
    
    indice_segno = int(gradi // 30)
    if indice_segno >= len(segni_con_simboli):
        indice_segno = 0
    
    gradi_nel_segno = gradi % 30
    segno_con_simbolo = segni_con_simboli[indice_segno][0]
    
    return f"{gradi_nel_segno:.1f}° {segno_con_simbolo}"

def interpreta_segno(gradi):
    return converti_gradi_in_segno(gradi)

def get_nome_segno(gradi):
    segni = [
        "Ariete", "Toro", "Gemelli", "Cancro", "Leone", "Vergine",
        "Bilancia", "Scorpione", "Sagittario", "Capricorno", "Acquario", "Pesci"
    ]
    indice_segno = int(gradi // 30)
    if indice_segno >= len(segni):
        indice_segno = 0
    return segni[indice_segno]

def get_elemento(segno):
    elementi = {
        'Ariete': 'Fuoco', 'Leone': 'Fuoco', 'Sagittario': 'Fuoco',
        'Toro': 'Terra', 'Vergine': 'Terra', 'Capricorno': 'Terra',
        'Gemelli': 'Aria', 'Bilancia': 'Aria', 'Acquario': 'Aria',
        'Cancro': 'Acqua', 'Scorpione': 'Acqua', 'Pesci': 'Acqua'
    }
    return elementi.get(segno, '')

def get_messaggio_radix(self, pianeta1, pianeta2, aspetto='congiunzione'):
    """
    Restituisce il messaggio radix per una coppia di pianeti
    """
    chiave = f"{pianeta1.lower()}_{pianeta2.lower()}"
    if chiave in self.messaggi_radix:
        return self.messaggi_radix[chiave].get(aspetto, {})
    
    # Prova anche con l'ordine inverso
    chiave_inversa = f"{pianeta2.lower()}_{pianeta1.lower()}"
    if chiave_inversa in self.messaggi_radix:
        return self.messaggi_radix[chiave_inversa].get(aspetto, {})
    
    return None

def interpreta_casa(numero_casa):
    interpretazioni = {
        1: "Personalità, aspetto fisico, come ti presenti",
        2: "Valori, risorse economiche, autostima",
        3: "Comunicazione, fratelli, studi, viaggi brevi",
        4: "Famiglia, origini, casa, genitori",
        5: "Creatività, figli, amore, divertimento",
        6: "Lavoro, salute, routine, servizio",
        7: "Relazioni, matrimonio, soci, partner",
        8: "Trasformazioni, sessualità, eredità, morte",
        9: "Filosofia, viaggi lunghi, studi superiori, spiritualità",
        10: "Carriera, successo, autorità, ruolo sociale",
        11: "Amicizie, progetti, speranze, gruppi",
        12: "Spiritualità, isolamento, sacrificio, subconscio"
    }
    return interpretazioni.get(numero_casa, "")

def pianeta_in_casa(gradi_pianeta, cusps):
    for i in range(12):
        cuspide_inizio = cusps[i]
        cuspide_fine = cusps[(i+1) % 12]
        if cuspide_fine < cuspide_inizio:
            cuspide_fine += 360
        gradi_pianeta_adj = gradi_pianeta
        if gradi_pianeta_adj < cuspide_inizio:
            gradi_pianeta_adj += 360
        if cuspide_inizio <= gradi_pianeta_adj < cuspide_fine:
            return i + 1
    return 1

def calcola_potenze_astrologiche(data_nascita, ora_nascita, lat, lon):
    """
    Calcola le potenze astrologiche usando la classe CalcolatoreAspettiTradizionali
    """
    # 1. Calcola posizioni pianeti e julday
    anno, mese, giorno = map(int, data_nascita.split('-'))
    ora_int, min_int = map(int, ora_nascita.split(':'))
    ora_dec = ora_int + min_int/60.0
    julday = swe.julday(anno, mese, giorno, ora_dec)
    
    # 2. Posizioni pianeti
    pianeti_lista = ['Sole', 'Luna', 'Mercurio', 'Venere', 'Marte', 
                     'Giove', 'Saturno', 'Urano', 'Nettuno', 'Plutone']
    pianeti_ids = {
        'Sole': swe.SUN, 'Luna': swe.MOON, 'Mercurio': swe.MERCURY,
        'Venere': swe.VENUS, 'Marte': swe.MARS, 'Giove': swe.JUPITER,
        'Saturno': swe.SATURN, 'Urano': swe.URANUS, 'Nettuno': swe.NEPTUNE,
        'Plutone': swe.PLUTO
    }
    
    pianeti = {}
    for nome in pianeti_lista:
        pos = swe.calc_ut(julday, pianeti_ids[nome])[0]
        pianeti[nome] = {
            'longitudine_360': pos[0],
            'segno': get_nome_segno(pos[0])
        }
    
    # 3. Calcola case
    cusps, ascmc = swe.houses(julday, lat, lon, b'P')
    
    nomi_case = ['Ascendente', 'II', 'III', 'FC', 'V', 'VI', 
                 'Discendente', 'VIII', 'IX', 'MC', 'XI', 'XII']
    
    case = {}
    segni_case = {}
    for i, nome in enumerate(nomi_case):
        case[nome] = {
            'cuspide_360': cusps[i],
            'segno': get_nome_segno(cusps[i])
        }
        segni_case[nome] = get_nome_segno(cusps[i])
    
    # Aggiungi anche i punti angolari come case speciali
    case['Ascendente'] = {'cuspide_360': ascmc[0], 'segno': get_nome_segno(ascmc[0])}
    case['MC'] = {'cuspide_360': ascmc[1], 'segno': get_nome_segno(ascmc[1])}
    
    # 4. Usa il calcolatore
    calcolatore = CalcolatoreAspettiTradizionali()
    
    # Trova tutti gli aspetti pianeta-cuspide
    aspetti_pc = calcolatore.trova_aspetti_pianeta_cuspide(pianeti, case, segni_case)
    
    # Calcola totali per tipo
    totale_armonici = sum(a['potenza'] for a in aspetti_pc if a['tipo'] == '+')
    totale_disarmonici = sum(a['potenza'] for a in aspetti_pc if a['tipo'] == '-')
    totale_neutri = sum(a['potenza'] for a in aspetti_pc if a['tipo'] == 'N')
    
    return {
        'aspetti_pianeta_cuspide': aspetti_pc,
        'totali': {
            'armonici': round(totale_armonici, 1),
            'disarmonici': round(totale_disarmonici, 1),
            'neutri': round(totale_neutri, 1),
            'totale_complessivo': round(totale_armonici + totale_disarmonici + totale_neutri, 1)
        },
        'pianeti': pianeti,
        'case': case
    }

def calcola_aspetti(posizioni):
    """
    Calcola gli aspetti tra pianeti con debug completo
    """
    print(f"🔵🔵🔵 DENTRO calcola_aspetti 🔵🔵🔵")
    aspetti = []
    orbita_default = 8
    
    # Filtra solo i pianeti (escludi Ascendente e MC)
    pianeti = [p for p in posizioni.keys() 
               if p not in ['Ascendente', 'Medio Cielo']]
    
    print(f"\n{'='*60}")
    print(f"🔍🔍🔍 DEBUG ASPETTI TRA PIANETI 🔍🔍🔍")
    print(f"{'='*60}")
    print(f"📋 Lista pianeti: {pianeti}")
    print(f"🔢 Numero pianeti: {len(pianeti)}")
    print(f"🔄 Combinazioni possibili: {len(pianeti) * (len(pianeti)-1) // 2}")
    print(f"{'-'*60}")
    
    for i in range(len(pianeti)):
        for j in range(i+1, len(pianeti)):
            p1 = pianeti[i]
            p2 = pianeti[j]
            
            # Calcola distanza angolare
            diff = abs(posizioni[p1] - posizioni[p2])
            if diff > 180:
                diff = 360 - diff
            
            # Mostra ogni combinazione
            print(f"   {i+1:2}. {p1:8} - {p2:8} : {diff:6.2f}°", end="")
            
            # Controlla gli aspetti
            if abs(diff - 0) < orbita_default:
                aspetti.append(f"{p1} CONGIUNZIONE {p2} (orbita: {diff:.1f}°)")
                print(f" → ✅ CONGIUNZIONE")
            elif abs(diff - 30) < 3:
                aspetti.append(f"{p1} SEMISESTILE {p2} (orbita: {diff:.1f}°)")
                print(f" → ✅ SEMISESTILE")
            elif abs(diff - 45) < 3:
                aspetti.append(f"{p1} SEMIQUADRATO {p2} (orbita: {diff:.1f}°)")
                print(f" → ✅ SEMIQUADRATO")
            elif abs(diff - 60) < orbita_default:
                aspetti.append(f"{p1} SESTILE {p2} (orbita: {diff:.1f}°)")
                print(f" → ✅ SESTILE")
            elif abs(diff - 90) < orbita_default:
                aspetti.append(f"{p1} QUADRATURA {p2} (orbita: {diff:.1f}°)")
                print(f" → ✅ QUADRATURA")
            elif abs(diff - 120) < orbita_default:
                aspetti.append(f"{p1} TRIGONO {p2} (orbita: {diff:.1f}°)")
                print(f" → ✅ TRIGONO")
            elif abs(diff - 135) < 3:
                aspetti.append(f"{p1} SESQUIQUADRATO {p2} (orbita: {diff:.1f}°)")
                print(f" → ✅ SESQUIQUADRATO")
            elif abs(diff - 150) < 3:
                aspetti.append(f"{p1} QUINCONCE {p2} (orbita: {diff:.1f}°)")
                print(f" → ✅ QUINCONCE")
            elif abs(diff - 180) < orbita_default:
                aspetti.append(f"{p1} OPPOSIZIONE {p2} (orbita: {diff:.1f}°)")
                print(f" → ✅ OPPOSIZIONE")
            else:
                print(f" → ❌ nessun aspetto")
    
    print(f"{'-'*60}")
    print(f"📊 Totale aspetti trovati: {len(aspetti)} su {len(pianeti) * (len(pianeti)-1) // 2} combinazioni")
    print(f"{'='*60}\n")
    
    return aspetti

def calcola_aspetti_pianeta_cuspide(posizioni_pianeti, cuspidi_case, nomi_cuspidi=None):
    """
    Calcola gli aspetti tra pianeti e cuspidi delle case
    """
    aspetti = []
    orbita_default = 8
    
    if nomi_cuspidi is None:
        nomi_cuspidi = [f"Casa {i+1}" for i in range(12)]
    else:
        nomi_cuspidi[0] = "Ascendente"
        nomi_cuspidi[9] = "MC"
    
    for pianeta, grado_pianeta in posizioni_pianeti.items():
        for i, grado_cuspide in enumerate(cuspidi_case):
            nome_cuspide = nomi_cuspidi[i]
            
            diff = abs(grado_pianeta - grado_cuspide)
            if diff > 180:
                diff = 360 - diff
            
            if abs(diff - 0) < orbita_default:
                aspetti.append(f"{pianeta} CONGIUNZIONE {nome_cuspide} (orbita: {diff:.1f}°)")
            elif abs(diff - 30) < 3:
                aspetti.append(f"{pianeta} SEMISESTILE {nome_cuspide} (orbita: {diff:.1f}°)")
            elif abs(diff - 45) < 3:
                aspetti.append(f"{pianeta} SEMIQUADRATO {nome_cuspide} (orbita: {diff:.1f}°)")
            elif abs(diff - 60) < orbita_default:
                aspetti.append(f"{pianeta} SESTILE {nome_cuspide} (orbita: {diff:.1f}°)")
            elif abs(diff - 90) < orbita_default:
                aspetti.append(f"{pianeta} QUADRATURA {nome_cuspide} (orbita: {diff:.1f}°)")
            elif abs(diff - 120) < orbita_default:
                aspetti.append(f"{pianeta} TRIGONO {nome_cuspide} (orbita: {diff:.1f}°)")
            elif abs(diff - 135) < 3:
                aspetti.append(f"{pianeta} SESQUIQUADRATO {nome_cuspide} (orbita: {diff:.1f}°)")
            elif abs(diff - 150) < 3:
                aspetti.append(f"{pianeta} QUINCONCE {nome_cuspide} (orbita: {diff:.1f}°)")
            elif abs(diff - 180) < orbita_default:
                aspetti.append(f"{pianeta} OPPOSIZIONE {nome_cuspide} (orbita: {diff:.1f}°)")
    
    return aspetti


# ============================================
# FUNZIONI DI ANALISI SPECIFICHE
# ============================================

def analisi_luna(posizioni_luna, posizioni_pianeti, cusps, aspetti_pianeti, aspetti_pc):
    """
    Analisi dettagliata della Luna: segno, casa e aspetti
    """
    risultati = []
    risultati.append("🌙 ANALISI DELLA LUNA")
    risultati.append("-" * 40)
    
    # 1. Segno della Luna
    segno_luna = interpreta_segno(posizioni_luna)
    risultati.append(f"📌 La Luna è nel segno: {segno_luna}")
    
    # 2. Casa della Luna
    casa_luna = pianeta_in_casa(posizioni_luna, cusps)
    risultati.append(f"🏠 La Luna è in Casa {casa_luna} - {interpreta_casa(casa_luna)}")
    risultati.append("")
    
    # 3. Aspetti della Luna con altri pianeti
    risultati.append("⚡ ASPETTI DELLA LUNA CON PIANETI:")
    aspetti_luna = [a for a in aspetti_pianeti if "Luna" in a]
    if aspetti_luna:
        for a in aspetti_luna:
            risultati.append(f"   • {a}")
    else:
        risultati.append("   • Nessun aspetto rilevante")
    risultati.append("")
    
    # 4. Aspetti della Luna con cuspidi
    risultati.append("📏 ASPETTI DELLA LUNA CON CUSPIDI:")
    aspetti_luna_cuspidi = [a for a in aspetti_pc if "Luna" in a]
    
    if aspetti_luna_cuspidi:
        cuspidi_principali = ['Ascendente', 'MC', 'FC', 'Discendente']
        altri = []
        
        for a in aspetti_luna_cuspidi:
            if any(c in a for c in cuspidi_principali):
                risultati.append(f"   • {a}")
            else:
                altri.append(a)
        
        if altri:
            risultati.append("   ... altri aspetti con le case ...")
            for a in altri[:3]:
                risultati.append(f"   • {a}")
    else:
        risultati.append("   • Nessun aspetto con le cuspidi")
    
    risultati.append("-" * 40)
    return "\n".join(risultati)

def debug_posizioni_luna(data_nascita, ora_nascita, lat, lon, fuso="Europe/Rome"):
    """
    Funzione di debug per vedere le posizioni reali della Luna con swisseph
    """
    print("\n" + "="*50)
    print("🔍 DEBUG POSIZIONI LUNA CON SWISSEPH")
    print("="*50)
    
    anno, mese, giorno = map(int, data_nascita.split('-'))
    ora_int, min_int = map(int, ora_nascita.split(':'))
    
    # Crea datetime locale
    dt_naive = datetime(anno, mese, giorno, ora_int, min_int)
    timezone = pytz.timezone(fuso)
    dt_local = timezone.localize(dt_naive)
    dt_utc = dt_local.astimezone(pytz.UTC)
    
    ora_utc = dt_utc.hour + dt_utc.minute/60.0
    julday_utc = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, ora_utc)
    
    # Posizione Luna
    pos_luna = swe.calc_ut(julday_utc, swe.MOON)[0]
    
    print(f"📅 Data: {data_nascita} {ora_nascita} ({fuso})")
    print(f"🌙 Luna: {pos_luna[0]:.2f}°")
    print(f"   Segno: {int(pos_luna[0] // 30)}")
    print(f"   Gradi nel segno: {pos_luna[0] % 30:.2f}°")
    print("="*50)
    
    return pos_luna[0]


def determina_fuso_corretto(anno, mese, giorno, fuso_base="Europe/Rome"):
    """
    Determina se applicare ora legale in base alla data
    Per l'Italia: ora legale dall'ultima domenica di marzo all'ultima domenica di ottobre
    """
    # Regole semplificate per l'Italia
    if anno < 1966:
        return fuso_base  # No ora legale prima del 1966
    
    # Per gli anni 1966-1980, l'ora legale andava da fine maggio a fine settembre
    if 1966 <= anno <= 1980:
        if mese > 5 and mese < 10:  # Giugno-Settembre = ora legale
            return "Europe/Rome"  # pytz gestirà come CEST
        elif mese == 5 and giorno >= 28:  # Fine maggio
            return "Europe/Rome"
        elif mese == 10 and giorno <= 1:  # Inizio ottobre
            return "Europe/Rome"
    
    # Regole moderne (1981-oggi)
    if anno >= 1981:
        if mese > 3 and mese < 10:  # Aprile-Settembre = ora legale
            return "Europe/Rome"
        elif mese == 3 and giorno >= 25:  # Fine marzo
            return "Europe/Rome"
        elif mese == 10 and giorno <= 30:  # Fine ottobre
            return "Europe/Rome"
    
    return fuso_base

def calcola_posizioni_e_case(data_nascita, ora_nascita, lat, lon, fuso="Europe/Rome"):
    """
    Calcola solo posizioni e cuspidi per i transiti
    """
    import pytz
    from datetime import datetime
    
    anno, mese, giorno = map(int, data_nascita.split('-'))
    ora_int, min_int = map(int, ora_nascita.split(':'))
    
    dt_naive = datetime(anno, mese, giorno, ora_int, min_int)
    timezone = pytz.timezone(fuso)
    dt_local = timezone.localize(dt_naive)
    dt_utc = dt_local.astimezone(pytz.UTC)
    
    ora_utc = dt_utc.hour + dt_utc.minute/60.0
    julday_utc = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, ora_utc)
    
    # Posizioni pianeti
    pianeti_ids = {
        'Sole': swe.SUN, 'Luna': swe.MOON, 'Mercurio': swe.MERCURY,
        'Venere': swe.VENUS, 'Marte': swe.MARS, 'Giove': swe.JUPITER,
        'Saturno': swe.SATURN, 'Urano': swe.URANUS, 'Nettuno': swe.NEPTUNE,
        'Plutone': swe.PLUTO
    }
    
    posizioni = {}
    for nome, id_pianeta in pianeti_ids.items():
        pos = swe.calc_ut(julday_utc, id_pianeta)[0]
        posizioni[nome] = pos[0]
    
    # Case (usando UTC, come abbiamo scoperto)
    cusps, ascmc = swe.houses(julday_utc, lat, lon, b'P')
    ascendente = ascmc[0]
    mc = ascmc[1]
    
    return posizioni, cusps, ascendente, mc

# ============================================
# FUNZIONI DI SUPPORTO PER IL MOTORE DI SINTESI
# ============================================

def estrai_segno(testo_segno):
    """
    Estrae il simbolo del segno da una stringa come '23.5° ♈ Ariete'
    Restituisce solo la parte del segno (es. 'Ariete')
    """
    if '°' in testo_segno:
        parti = testo_segno.split()
        if len(parti) >= 2:
            return parti[1]  # Restituisce '♈'
    return testo_segno


def trova_dominante_segno(segno):
    """
    Restituisce il pianeta dominante di un segno zodiacale
    """
    dominanti = {
        'Ariete': 'Marte', '♈': 'Marte',
        'Toro': 'Venere', '♉': 'Venere',
        'Gemelli': 'Mercurio', '♊': 'Mercurio',
        'Cancro': 'Luna', '♋': 'Luna',
        'Leone': 'Sole', '♌': 'Sole',
        'Vergine': 'Mercurio', '♍': 'Mercurio',
        'Bilancia': 'Venere', '♎': 'Venere',
        'Scorpione': 'Plutone', '♏': 'Plutone',
        'Sagittario': 'Giove', '♐': 'Giove',
        'Capricorno': 'Saturno', '♑': 'Saturno',
        'Acquario': 'Urano', '♒': 'Urano',
        'Pesci': 'Nettuno', '♓': 'Nettuno'
    }
    return dominanti.get(segno, '')


def calcola_punteggio_aspetto(pianeta, lista_aspetti):
    """
    Calcola se un pianeta ha più aspetti armoniosi o dissonanti
    Restituisce un punteggio positivo (armonioso) o negativo (dissonante)
    """
    punteggio = 0
    for aspetto in lista_aspetti:
        if pianeta in aspetto:
            if 'TRIGONO' in aspetto or 'SESTILE' in aspetto:
                punteggio += 1
            elif 'QUADRATURA' in aspetto or 'OPPOSIZIONE' in aspetto:
                punteggio -= 1
            elif 'QUINCONCE' in aspetto:
                punteggio -= 0.5
    return punteggio


def trova_aspetti_per_pianeta(pianeta, lista_aspetti):
    """
    Restituisce tutti gli aspetti che coinvolgono un pianeta specifico
    """
    return [a for a in lista_aspetti if pianeta in a]


def calcola_tutti_i_dominanti(segni_case, posizioni, cusps):
    """
    Calcola i dominanti di tutte le case
    Restituisce un dizionario con {numero_casa: (pianeta_dominante, casa_dominante)}
    """
    dominanti = {}
    for num_casa, segno in segni_case.items():
        dominante = trova_dominante_segno(segno)
        if dominante and dominante in posizioni:
            casa_dominante = pianeta_in_casa(posizioni[dominante], cusps)
            dominanti[num_casa] = (dominante, casa_dominante)
    return dominanti


def sintesi_ascendente(calcolatore, info_tema):
    """
    Genera un testo che sintetizza Ascendente, suo segno e suo dominante
    """
    risultati = []
    risultati.append("")
    risultati.append("="*60)
    risultati.append("⭐ IL TUO ASCENDENTE E I DOMINANTI")
    risultati.append("="*60)
    
    segno_asc = info_tema['case_segni'][1]
    risultati.append(f"Il tuo Ascendente è in **{segno_asc}**.")
    
    # Significato base del segno sull'Ascendente
    if 1 in calcolatore.segni_sulle_cuspidi and segno_asc in calcolatore.segni_sulle_cuspidi[1]:
        risultati.append("")
        risultati.append(calcolatore.segni_sulle_cuspidi[1][segno_asc])
    
    # Dominante dell'Ascendente
    dominante_asc = trova_dominante_segno(segno_asc)
    if dominante_asc and dominante_asc in info_tema['pianeti_case']:
        casa_dom = info_tema['pianeti_case'][dominante_asc]
        risultati.append("")
        risultati.append(f"Il suo dominante, **{dominante_asc}**, si trova in **Casa {casa_dom}**.")
        
        if 'I' in calcolatore.dominanti_case and casa_dom in calcolatore.dominanti_case['I']:
            risultati.append(calcolatore.dominanti_case['I'][casa_dom])
    
    return "\n".join(risultati)


def sintesi_pianeta_in_casa(calcolatore, pianeta, info_tema):
    """
    Genera un testo che sintetizza un pianeta nella sua casa, considerando anche i suoi aspetti
    """
    risultati = []
    risultati.append("")
    risultati.append("="*60)
    risultati.append(f"🪐 {pianeta.upper()} IN CASA {info_tema['pianeti_case'][pianeta]}")
    risultati.append("="*60)
    
    casa = info_tema['pianeti_case'][pianeta]
    
    # Significato base del pianeta in quella casa
    if pianeta in calcolatore.pianeti_case_radix and casa in calcolatore.pianeti_case_radix[pianeta]:
        # Determina se gli aspetti sono armoniosi o dissonanti
        punteggio = calcola_punteggio_aspetto(pianeta, info_tema['aspetti_pianeti'])
        tipo = 'armonioso' if punteggio >= 0 else 'dissonante'
        
        testo_base = calcolatore.pianeti_case_radix[pianeta][casa][tipo]
        risultati.append("")
        risultati.append(testo_base)
    
    # Aggiungi considerazioni sugli aspetti principali
    aspetti_rilevanti = trova_aspetti_per_pianeta(pianeta, info_tema['aspetti_pianeti'])
    if aspetti_rilevanti:
        risultati.append("")
        risultati.append("**Questo pianeta è in aspetto con:**")
        for aspetto in aspetti_rilevanti[:3]:  # Limita a 3 per non appesantire
            risultati.append(f"  • {aspetto}")
    
    return "\n".join(risultati)


def sintesi_aspetti_principali(calcolatore, info_tema):
    """
    Genera un testo che sintetizza gli aspetti più importanti
    """
    risultati = []
    risultati.append("")
    risultati.append("="*60)
    risultati.append("🔗 ASPETTI PRINCIPALI DEL TUO TEMA")
    risultati.append("="*60)
    
    # Raccogli tutti gli aspetti per tipo
    congiunzioni = []
    sestili = []
    trigoni = []
    quadrature = []
    opposizioni = []
    quinconci = []
    
    for aspetto in info_tema['aspetti_pianeti']:
        if 'CONGIUNZIONE' in aspetto:
            congiunzioni.append(aspetto)
        elif 'SESTILE' in aspetto:
            sestili.append(aspetto)
        elif 'TRIGONO' in aspetto:
            trigoni.append(aspetto)
        elif 'QUADRATURA' in aspetto:
            quadrature.append(aspetto)
        elif 'OPPOSIZIONE' in aspetto:
            opposizioni.append(aspetto)
        elif 'QUINCONCE' in aspetto:
            quinconci.append(aspetto)
    
    # Dai priorità agli aspetti più forti
    if congiunzioni:
        risultati.append("")
        risultati.append("**🔹 CONGIUNZIONI** - Gli aspetti più intensi che fondono le energie:")
        for asp in congiunzioni[:3]:
            risultati.append(f"  • {asp}")
    
    if quadrature or opposizioni:
        risultati.append("")
        risultati.append("**🔸 TENSIONI PRINCIPALI** - Le sfide che ti fanno crescere:")
        for asp in (quadrature + opposizioni)[:4]:
            risultati.append(f"  • {asp}")
    
    if trigoni or sestili:
        risultati.append("")
        risultati.append("**🔹 TALENTI NATURALI** - Le energie che fluiscono con facilità:")
        for asp in (trigoni + sestili)[:4]:
            risultati.append(f"  • {asp}")
    
    if quinconci:
        risultati.append("")
        risultati.append("**🔸 AGGIUSTAMENTI NECESSARI** - Piccole tensioni da armonizzare:")
        for asp in quinconci[:3]:
            risultati.append(f"  • {asp}")
    
    if not (congiunzioni or sestili or trigoni or quadrature or opposizioni or quinconci):
        risultati.append("")
        risultati.append("Non ci sono aspetti particolarmente significativi nel tuo tema natale.")
    
    return "\n".join(risultati)


def analisi_completa_case(calcolatore, info_tema):
    """
    Genera un'analisi di tutte le case con i loro segni e dominanti
    """
    risultati = []
    risultati.append("")
    risultati.append("="*60)
    risultati.append("🏠 ANALISI COMPLETA DELLE CASE")
    risultati.append("="*60)
    
    for num_casa in range(1, 13):
        segno = info_tema['case_segni'][num_casa]
        risultati.append("")
        risultati.append(f"**CASA {num_casa} - {interpreta_casa(num_casa).upper()}**")
        risultati.append(f"Segno sulla cuspide: {segno}")
        
        # Significato del segno in questa casa
        if num_casa in calcolatore.segni_sulle_cuspidi and segno in calcolatore.segni_sulle_cuspidi[num_casa]:
            risultati.append(calcolatore.segni_sulle_cuspidi[num_casa][segno])
        
        # Dominante di questa casa
        dominante = trova_dominante_segno(segno)
        if dominante and dominante in info_tema['pianeti_case']:
            casa_dom = info_tema['pianeti_case'][dominante]
            risultati.append(f"Il suo dominante, {dominante}, si trova in Casa {casa_dom}.")
            
            # Cerca il testo per il dominante della casa X in casa Y
            chiave_casa = str(num_casa)  # '1', '2', ... '12' per il dizionario
            if chiave_casa in calcolatore.dominanti_case and casa_dom in calcolatore.dominanti_case[chiave_casa]:
                risultati.append(calcolatore.dominanti_case[chiave_casa][casa_dom])
    
    return "\n".join(risultati)


def sintesi_finale(calcolatore, info_tema):
    """
    Genera una sintesi finale che combina le informazioni più importanti
    """
    risultati = []
    risultati.append("")
    risultati.append("="*60)
    risultati.append("✨ SINTESI FINALE DEL TUO PROFILO")
    risultati.append("="*60)
    
    # Trova il pianeta più forte (quello con più aspetti armoniosi)
    punteggi = {}
    for pianeta in info_tema['pianeti_case'].keys():
        punteggi[pianeta] = calcola_punteggio_aspetto(pianeta, info_tema['aspetti_pianeti'])
    
    if punteggi:
        pianeta_forte = max(punteggi, key=punteggi.get)
        pianeta_debole = min(punteggi, key=punteggi.get)
        
        risultati.append("")
        risultati.append(f"**{pianeta_forte}** è il pianeta più armonioso nel tuo tema, le sue energie scorrono con facilità.")
        risultati.append(f"**{pianeta_debole}** è il pianeta più teso, le sue aree richiedono più attenzione e lavoro interiore.")
    
    # Considerazioni sull'equilibrio degli elementi
    # (da implementare con i dati già disponibili)
    
    return "\n".join(risultati)

def genera_sezione_donna_avanzata(calcolatore, posizioni, cusps, aspetti):
    """
    Genera una sezione donna avanzata che gestisce:
    - Luna e Venere con le loro case e dominanti
    - Casa 5 e Casa 7 (con o senza pianeti)
    - Aspetti tesi (es. Luna-Saturno)
    - Collegamenti tra tutti gli elementi
    """
    risultati = []
    risultati.append("="*60)
    risultati.append("👩 IL TUO MONDO INTERIORE E LE TUE RELAZIONI")
    risultati.append("="*60)
    risultati.append("")
    
    # ============================================
    # FUNZIONI DI SUPPORTO
    # ============================================
    def get_nome_segno_da_gradi(gradi):
        segni = ["Ariete", "Toro", "Gemelli", "Cancro", "Leone", "Vergine",
                 "Bilancia", "Scorpione", "Sagittario", "Capricorno", "Acquario", "Pesci"]
        indice = int(gradi // 30)
        return segni[indice]
    
    def get_pianeta_dominante(segno):
        dominanti = {
            'Ariete': 'Marte', 'Toro': 'Venere', 'Gemelli': 'Mercurio',
            'Cancro': 'Luna', 'Leone': 'Sole', 'Vergine': 'Mercurio',
            'Bilancia': 'Venere', 'Scorpione': 'Plutone', 'Sagittario': 'Giove',
            'Capricorno': 'Saturno', 'Acquario': 'Urano', 'Pesci': 'Nettuno'
        }
        return dominanti.get(segno, '')
    
    def trova_aspetto_tra(p1, p2):
        for asp in aspetti:
            if p1 in asp and p2 in asp:
                if 'TRIGONO' in asp:
                    return 'trigono'
                elif 'SESTILE' in asp:
                    return 'sestile'
                elif 'QUADRATURA' in asp:
                    return 'quadratura'
                elif 'OPPOSIZIONE' in asp:
                    return 'opposizione'
                elif 'CONGIUNZIONE' in asp:
                    return 'congiunzione'
        return None
    
    def calcola_punteggio_aspetto(pianeta, lista_aspetti):
        punteggio = 0
        for aspetto in lista_aspetti:
            if pianeta in aspetto:
                if 'TRIGONO' in aspetto or 'SESTILE' in aspetto:
                    punteggio += 1
                elif 'QUADRATURA' in aspetto or 'OPPOSIZIONE' in aspetto:
                    punteggio -= 1
        return punteggio
    
    # ============================================
    # 1. LUNA - LE TUE EMOZIONI
    # ============================================
    if 'Luna' in posizioni:
        risultati.append("🌙 LA TUA ANIMA EMOTIVA")
        risultati.append("-" * 30)
        
        grado_luna = posizioni['Luna']
        casa_luna = pianeta_in_casa(grado_luna, cusps)
        segno_luna = get_nome_segno_da_gradi(grado_luna)
        segno_luna_completo = converti_gradi_in_segno(grado_luna)
        
        risultati.append(f"La tua **Luna è in {segno_luna_completo}** e si trova nella **Casa {casa_luna}**, {interpreta_casa(casa_luna)}.")
        risultati.append("")
        
        # Testo base della Luna in questa casa
        if 'Luna' in calcolatore.pianeti_case_radix and casa_luna in calcolatore.pianeti_case_radix['Luna']:
            punteggio = calcola_punteggio_aspetto('Luna', aspetti)
            tipo = 'armonioso' if punteggio >= 0 else 'dissonante'
            risultati.append(calcolatore.pianeti_case_radix['Luna'][casa_luna][tipo])
            risultati.append("")
        
        # Dominante del segno della Luna
        dominante_luna = get_pianeta_dominante(segno_luna)
        if dominante_luna and dominante_luna in posizioni:
            casa_dominante_luna = pianeta_in_casa(posizioni[dominante_luna], cusps)
            risultati.append(f"Il segno della Luna è governato da **{dominante_luna}**, che si trova nella **Casa {casa_dominante_luna}**, {interpreta_casa(casa_dominante_luna)}.")
            
            # Verifica se è in aspetto con Saturno
            if dominante_luna == 'Saturno' or (dominante_luna == 'Luna' and 'Saturno' in posizioni):
                tipo_aspetto_saturno = trova_aspetto_tra('Luna', 'Saturno')
                if tipo_aspetto_saturno in ['quadratura', 'opposizione']:
                    risultati.append("")
                    risultati.append("**Nota importante:** La tua Luna è in aspetto teso con Saturno. Questo crea una dinamica particolare: da un lato hai una sensibilità profonda, dall'altro Saturno ti impone disciplina, controllo, a volte durezza. Potresti essere stata cresciuta in un ambiente dove le emozioni non erano libere di esprimersi, o dove hai imparato che mostrare ciò che senti è segno di debolezza.")
                    risultati.append("")
                    risultati.append("Di conseguenza, a volte fatichi a lasciarti andare nelle relazioni. Tendi a tenere le distanze, a proteggerti, a mostrarti più forte di quanto ti senti. Ma questa corazza, che ti ha protetta in passato, oggi potrebbe impedirti di vivere l'amore con leggerezza.")
            risultati.append("")
    
    # ============================================
    # 2. VENERE - IL TUO MODO DI AMARE
    # ============================================
    if 'Venere' in posizioni:
        risultati.append("💖 IL TUO MODO DI AMARE")
        risultati.append("-" * 30)
        
        grado_venere = posizioni['Venere']
        casa_venere = pianeta_in_casa(grado_venere, cusps)
        segno_venere = get_nome_segno_da_gradi(grado_venere)
        segno_venere_completo = converti_gradi_in_segno(grado_venere)
        
        risultati.append(f"La tua **Venere è in {segno_venere_completo}** e si trova nella **Casa {casa_venere}**, {interpreta_casa(casa_venere)}.")
        risultati.append("")
        
        # Testo base di Venere in questa casa
        if 'Venere' in calcolatore.pianeti_case_radix and casa_venere in calcolatore.pianeti_case_radix['Venere']:
            punteggio = calcola_punteggio_aspetto('Venere', aspetti)
            tipo = 'armonioso' if punteggio >= 0 else 'dissonante'
            risultati.append(calcolatore.pianeti_case_radix['Venere'][casa_venere][tipo])
            risultati.append("")
        
        # Dominante del segno di Venere
        dominante_venere = get_pianeta_dominante(segno_venere)
        if dominante_venere and dominante_venere in posizioni:
            casa_dominante_venere = pianeta_in_casa(posizioni[dominante_venere], cusps)
            risultati.append(f"Il segno di Venere è governato da **{dominante_venere}**, che si trova nella **Casa {casa_dominante_venere}**, {interpreta_casa(casa_dominante_venere)}.")
            
            if casa_dominante_venere == 7:
                risultati.append("Questo è un dato importantissimo: il pianeta che governa il tuo modo di amare si trova proprio nella casa del partner! Significa che la comunicazione è la chiave delle tue relazioni. Cerchi qualcuno con cui parlare, con cui scambiare idee, con cui ridere.")
            risultati.append("")
    
    # ============================================
    # 3. CASA 5 - LA TUA CREATIVITÀ E IL TUO CUORE
    # ============================================
    risultati.append("🎨 LA TUA CREATIVITÀ E IL TUO CUORE")
    risultati.append("-" * 30)
    
    grado_casa5 = cusps[4]
    segno_casa5 = get_nome_segno_da_gradi(grado_casa5)
    segno_casa5_completo = converti_gradi_in_segno(grado_casa5)
    
    risultati.append(f"La tua **Casa 5 è in {segno_casa5_completo}**, {interpreta_casa(5)}.")
    risultati.append("")
    
    # Significato del segno in Casa 5
    if 5 in calcolatore.segni_sulle_cuspidi and segno_casa5 in calcolatore.segni_sulle_cuspidi[5]:
        risultati.append(calcolatore.segni_sulle_cuspidi[5][segno_casa5])
        risultati.append("")
    
    # Dominante della Casa 5
    dominante_c5 = get_pianeta_dominante(segno_casa5)
    if dominante_c5 and dominante_c5 in posizioni:
        casa_dom_c5 = pianeta_in_casa(posizioni[dominante_c5], cusps)
        risultati.append(f"Il segno della Casa 5 è governato da **{dominante_c5}**, che si trova nella **Casa {casa_dom_c5}**, {interpreta_casa(casa_dom_c5)}.")
        
        # Collegamento con Venere se il dominante è Venere
        if 'Venere' in posizioni and dominante_c5 == 'Venere' and casa_dom_c5 == pianeta_in_casa(posizioni['Venere'], cusps):
            risultati.append("Questo crea un collegamento interessante: la tua creatività e la tua capacità di amare si esprimono attraverso le stesse aree della vita.")
        risultati.append("")
    
    # Pianeti in Casa 5
    pianeti_c5 = []
    for p in ['Sole', 'Luna', 'Mercurio', 'Venere', 'Marte', 'Giove', 'Saturno', 'Urano', 'Nettuno', 'Plutone']:
        if p in posizioni and pianeta_in_casa(posizioni[p], cusps) == 5:
            pianeti_c5.append(p)
    
    if pianeti_c5:
        risultati.append(f"In Casa 5 ci sono: {', '.join(pianeti_c5)}. Questo rende la tua vita creativa e amorosa ancora più ricca e complessa.")
    else:
        risultati.append("Non ci sono pianeti in Casa 5, ma questo non significa che la creatività e l'amore siano assenti. È attraverso il suo segno e il suo dominante che questa casa esprime la sua energia.")
    risultati.append("")
    
    # ============================================
    # 4. CASA 7 - LE TUE RELAZIONI SIGNIFICATIVE
    # ============================================
    risultati.append("💑 COSA CERCHI IN UN PARTNER")
    risultati.append("-" * 30)
    
    grado_casa7 = cusps[6]
    segno_casa7 = get_nome_segno_da_gradi(grado_casa7)
    segno_casa7_completo = converti_gradi_in_segno(grado_casa7)
    
    risultati.append(f"La tua **Casa 7 è in {segno_casa7_completo}**, {interpreta_casa(7)}.")
    risultati.append("")
    
    # Significato del segno in Casa 7
    if 7 in calcolatore.segni_sulle_cuspidi and segno_casa7 in calcolatore.segni_sulle_cuspidi[7]:
        risultati.append(calcolatore.segni_sulle_cuspidi[7][segno_casa7])
        risultati.append("")
    
    # Dominante della Casa 7
    dominante_c7 = get_pianeta_dominante(segno_casa7)
    if dominante_c7 and dominante_c7 in posizioni:
        casa_dom_c7 = pianeta_in_casa(posizioni[dominante_c7], cusps)
        risultati.append(f"Il segno della Casa 7 è governato da **{dominante_c7}**, che si trova nella **Casa {casa_dom_c7}**, {interpreta_casa(casa_dom_c7)}.")
        
        if casa_dom_c7 == 7:
            risultati.append("Questo è un caso raro e potente: il dominante della casa si trova nella casa stessa! Significa che l'energia di questo pianeta è doppiamente forte nelle tue relazioni.")
        
        # Collegamento con Luna-Saturno se il dominante è Saturno o Luna
        if 'Luna' in posizioni and 'Saturno' in posizioni:
            tipo_aspetto_saturno = trova_aspetto_tra('Luna', 'Saturno')
            if tipo_aspetto_saturno in ['quadratura', 'opposizione']:
                if dominante_c7 == 'Saturno' or dominante_c7 == 'Luna':
                    risultati.append("")
                    risultati.append("C'è un collegamento importante: il pianeta che governa le tue relazioni è lo stesso che mette in tensione la tua Luna (Saturno). Questo significa che le tue difficoltà emotive si riflettono direttamente su ciò che cerchi in un partner. Potresti essere attratta da persone fredde, distanti, o sentirti sempre inadeguata in amore.")
                    risultati.append("")
                    risultati.append("Ma attenzione: questa stessa dinamica può diventare la tua più grande forza. Se impari a trasformare la disciplina di Saturno in maturità emotiva, potrai costruire relazioni solide e durature, basate su rispetto e consapevolezza, non su dipendenza affettiva.")
        risultati.append("")
    
    # Pianeti in Casa 7
    pianeti_c7 = []
    for p in ['Sole', 'Luna', 'Mercurio', 'Venere', 'Marte', 'Giove', 'Saturno', 'Urano', 'Nettuno', 'Plutone']:
        if p in posizioni and pianeta_in_casa(posizioni[p], cusps) == 7:
            pianeti_c7.append(p)
    
    if pianeti_c7:
        risultati.append(f"In Casa 7 ci sono: {', '.join(pianeti_c7)}. È una concentrazione di energia molto forte!")
        if 'Sole' in pianeti_c7:
            risultati.append("  • Il Sole in Casa 7: le relazioni sono il centro della tua vita. La tua identità si realizza attraverso l'incontro con l'altro.")
        if 'Mercurio' in pianeti_c7:
            risultati.append("  • Mercurio in Casa 7: per te parlare con il partner è fondamentale. La comunicazione è la base del tuo amore.")
    else:
        risultati.append("Non ci sono pianeti in Casa 7, ma questo non rende le tue relazioni meno importanti. Il segno sulla cuspide e il suo dominante raccontano comunque molto su ciò che cerchi in un partner.")
    risultati.append("")
    
    # ============================================
    # 5. SINTESI E COLLEGAMENTI
    # ============================================
    risultati.append("=" * 40)
    risultati.append("✨ IN SINTESI")
    risultati.append("=" * 40)
    risultati.append("")
    
    sintesi = []
    
    # Luna-Saturno
    if 'Luna' in posizioni and 'Saturno' in posizioni:
        tipo = trova_aspetto_tra('Luna', 'Saturno')
        if tipo in ['quadratura', 'opposizione']:
            sintesi.append("Il tuo mondo emotivo è segnato da una tensione con Saturno: tendi a controllare le emozioni, a proteggerti, a mostrarti forte. Questo ti ha aiutata in passato, ma oggi potrebbe impedirti di vivere l'amore con leggerezza. Il lavoro su te stessa è imparare a lasciarti andare.")
    
    # Collegamento Luna-Venere
    if 'Luna' in posizioni and 'Venere' in posizioni:
        tipo = trova_aspetto_tra('Luna', 'Venere')
        if tipo == 'trigono':
            sintesi.append("Il trigono tra Luna e Venere è un dono: le tue emozioni e il tuo modo di amare sono in perfetta armonia. Quello che senti è quello che dai, e questo rende le tue relazioni autentiche e profonde.")
        elif tipo == 'quadratura' or tipo == 'opposizione':
            sintesi.append("C'è tensione tra le tue emozioni e il tuo modo di amare: a volte fatichi a distinguere ciò che senti da ciò che desideri. Questa tensione ti spinge a crescere, ma richiede consapevolezza.")
    
    # Casa 7 vuota ma con dominante significativo
    if not pianeti_c7 and dominante_c7 and dominante_c7 in posizioni:
        sintesi.append(f"Anche se non ci sono pianeti in Casa 7, il suo dominante {dominante_c7} in Casa {casa_dom_c7} indica che le qualità che cerchi in un partner vanno cercate nelle dinamiche di quella casa.")
    
    if not sintesi:
        sintesi.append("Sei una donna complessa, con un mondo interiore ricco e sfaccettato. Le tue emozioni e il tuo modo di amare si intrecciano in modo unico, creando relazioni profonde e significative.")
    
    risultati.extend(sintesi)
    risultati.append("")
    
    # ============================================
    # 6. CONSIGLI PERSONALIZZATI
    # ============================================
    risultati.append("💡 CONSIGLI PER TE")
    risultati.append("-" * 30)
    
    consigli = []
    
    # Consiglio per Luna-Saturno
    if 'Luna' in posizioni and 'Saturno' in posizioni:
        tipo = trova_aspetto_tra('Luna', 'Saturno')
        if tipo in ['quadratura', 'opposizione']:
            consigli.append("• **Per le tue emozioni:** Impara ad accettare le tue fragilità senza giudicarle. La tua tendenza a controllarti viene da lontano, ma oggi puoi scegliere di lasciarti andare un po' di più. Cerca un partner che sappia starti accanto senza invadere i tuoi spazi, ma anche senza farti sentire sola.")
    
    # Consiglio per Venere in Casa 6
    if 'Venere' in posizioni and pianeta_in_casa(posizioni['Venere'], cusps) == 6:
        consigli.append("• **Per il tuo amore:** Non dimenticare che l'amore passa anche attraverso le piccole cose. I gesti quotidiani, la cura, il lavoro fatto insieme sono il tuo linguaggio dell'amore. Cerca qualcuno che apprezzi questo tuo modo di amare.")
    
    # Consiglio per Casa 7 in Gemelli
    if segno_casa7 == 'Gemelli':
        consigli.append("• **Per le tue relazioni:** La comunicazione è tutto per te. Scegli un partner con cui puoi parlare per ore, con cui condividere libri, film, idee. La noia è il tuo peggior nemico in amore.")
    
    # Consiglio generale se non ci sono specifici
    if not consigli:
        consigli.append("• **Per il tuo percorso:** Ascolta il tuo cuore, ma anche la tua testa. Le tue emozioni sono preziose, ma hanno bisogno di essere comprese e guidate. La consapevolezza è la chiave per trasformare le difficoltà in forza.")
    
    risultati.extend(consigli)
    risultati.append("")
    risultati.append("="*60)
    
    return "\n".join(risultati)

def genera_profilo_caratteriale(data_nascita, ora_nascita, luogo, lat, lon, fuso="Europe/Rome"):
    """
    FUNZIONE PRINCIPALE: genera il profilo caratteriale completo
    """
    
    print(f"Calcolo profilo per: {data_nascita} {ora_nascita} (fuso: {fuso})")
    
    import pytz
    from datetime import datetime
    import swisseph as swe
    
    # 1. Converti data e ora con fuso corretto
    anno, mese, giorno = map(int, data_nascita.split('-'))
    ora_int, min_int = map(int, ora_nascita.split(':'))
    
    dt_naive = datetime(anno, mese, giorno, ora_int, min_int)
    timezone = pytz.timezone(fuso)
    
    try:
        dt_local = timezone.localize(dt_naive, is_dst=None)
    except (pytz.exceptions.AmbiguousTimeError, pytz.exceptions.NonExistentTimeError):
        if mese >= 4 and mese <= 9:
            dt_local = timezone.localize(dt_naive, is_dst=True)
        else:
            dt_local = timezone.localize(dt_naive, is_dst=False)
    
    dt_utc = dt_local.astimezone(pytz.UTC)
    ora_utc = dt_utc.hour + dt_utc.minute/60.0 + dt_utc.second/3600.0
    
    julday_utc = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, ora_utc)
    
    # 2. Posizioni pianeti
    pianeti_ids = {
        'Sole': swe.SUN, 'Luna': swe.MOON, 'Mercurio': swe.MERCURY,
        'Venere': swe.VENUS, 'Marte': swe.MARS, 'Giove': swe.JUPITER,
        'Saturno': swe.SATURN, 'Urano': swe.URANUS, 'Nettuno': swe.NEPTUNE,
        'Plutone': swe.PLUTO
    }
    
    posizioni = {}
    for nome, id_pianeta in pianeti_ids.items():
        pos = swe.calc_ut(julday_utc, id_pianeta)[0]
        posizioni[nome] = pos[0]
    
    # 3. Calcola case
    cusps, ascmc = swe.houses(julday_utc, lat, lon, b'P')
    ascendente = ascmc[0]
    mc = ascmc[1]
    
    posizioni['Ascendente'] = ascendente
    posizioni['Medio Cielo'] = mc

    # 4. Calcola aspetti
    aspetti = calcola_aspetti(posizioni)
    
    nomi_case_completi = ['Ascendente', 'II', 'III', 'FC', 'V', 'VI', 
                          'Discendente', 'VIII', 'IX', 'MC', 'XI', 'XII']
    aspetti_pc = calcola_aspetti_pianeta_cuspide(posizioni, cusps, nomi_case_completi)
    
    # 5. Calcola potenze
    try:
        potenze = calcola_potenze_astrologiche(data_nascita, ora_nascita, lat, lon)
    except Exception as e:
        print(f"Errore nel calcolo potenze: {e}")
        potenze = {'totali': {'armonici': 0, 'disarmonici': 0, 'neutri': 0, 'totale_complessivo': 0}}
    
    # 6. Crea calcolatore con tutti i database
    calcolatore = CalcolatoreAspettiTradizionali()
    
    # ============================================
    # RACCOLTA INFORMAZIONI STRUTTURATE
    # ============================================
    info_tema = {
        'posizioni': posizioni,
        'cusps': cusps,
        'aspetti_pianeti': aspetti,
        'aspetti_pc': aspetti_pc,
        'ascendente': ascmc[0],
        'mc': ascmc[1],
        'pianeti_case': {},
        'case_segni': {},
        'case_pianeti': {}
    }
    
    pianeti_ordine = ['Sole', 'Luna', 'Mercurio', 'Venere', 'Marte', 
                      'Giove', 'Saturno', 'Urano', 'Nettuno', 'Plutone']
    
    # Funzioni di supporto (definite internamente)
    def estrai_segno(testo_segno):
        if '°' in testo_segno:
            parti = testo_segno.split()
            if len(parti) >= 2:
                return parti[1]
        return testo_segno
    
    def calcola_punteggio_aspetto(pianeta, lista_aspetti):
        punteggio = 0
        for aspetto in lista_aspetti:
            if pianeta in aspetto:
                if 'TRIGONO' in aspetto or 'SESTILE' in aspetto:
                    punteggio += 1
                elif 'QUADRATURA' in aspetto or 'OPPOSIZIONE' in aspetto:
                    punteggio -= 1
                elif 'QUINCONCE' in aspetto:
                    punteggio -= 0.5
        return punteggio
    
    def pianeta_in_casa(gradi_pianeta, cusps):
        for i in range(12):
            inizio = cusps[i]
            fine = cusps[(i+1) % 12]
            if fine < inizio:
                fine += 360
            pos = gradi_pianeta
            if pos < inizio:
                pos += 360
            if inizio <= pos < fine:
                return i+1
        return 1
    
    def interpreta_casa(numero):
        significati = {
            1: "Personalità, aspetto fisico, come ti presenti",
            2: "Valori, risorse economiche, autostima",
            3: "Comunicazione, fratelli, studi, viaggi brevi",
            4: "Famiglia, origini, casa, genitori",
            5: "Creatività, amore, figli, piacere",
            6: "Lavoro, salute, routine, servizio",
            7: "Relazioni, matrimonio, soci, partner",
            8: "Trasformazioni, sessualità, eredità, morte",
            9: "Filosofia, viaggi lunghi, studi superiori, spiritualità",
            10: "Carriera, successo, autorità, ruolo sociale",
            11: "Amicizie, progetti, speranze, gruppi",
            12: "Spiritualità, isolamento, sacrificio, subconscio"
        }
        return significati.get(numero, f"Casa {numero}")
    
    def converti_gradi_in_segno(gradi):
        segni = ['♈ Ariete', '♉ Toro', '♊ Gemelli', '♋ Cancro', 
                 '♌ Leone', '♍ Vergine', '♎ Bilancia', '♏ Scorpione', 
                 '♐ Sagittario', '♑ Capricorno', '♒ Acquario', '♓ Pesci']
        indice = int(gradi // 30)
        gradi_nel_segno = gradi % 30
        return f"{gradi_nel_segno:.1f}° {segni[indice]}"
    
    for pianeta in pianeti_ordine:
        if pianeta in posizioni:
            info_tema['pianeti_case'][pianeta] = pianeta_in_casa(posizioni[pianeta], cusps)
    
    for i in range(12):
        segno_completo = converti_gradi_in_segno(cusps[i])
        segno_puro = estrai_segno(segno_completo)
        info_tema['case_segni'][i+1] = segno_puro
    
    # Raccogli anche i pianeti per ogni casa
    for casa in range(1, 13):
        info_tema['case_pianeti'][casa] = []
        for pianeta in pianeti_ordine:
            if pianeta in info_tema['pianeti_case'] and info_tema['pianeti_case'][pianeta] == casa:
                info_tema['case_pianeti'][casa].append(pianeta)
    
    # ============================================
    # GENERAZIONE PROFILO
    # ============================================
    profilo = []
    
    # INTESTAZIONE
    profilo.append("="*60)
    profilo.append("🔮 IL TUO VIAGGIO INTERIORE")
    profilo.append("="*60)
    
    mesi_ita = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
                "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]
    nome_mese = mesi_ita[dt_local.month - 1]
    profilo.append(f"📅 Data di nascita: {dt_local.day} {nome_mese} {dt_local.year} - {dt_local.hour:02d}:{dt_local.minute:02d}")
    profilo.append(f"📍 {luogo}")
    profilo.append("")
    
    # PUNTI ANGOLARI
    profilo.append("⭐ PUNTI ANGOLARI:")
    profilo.append(f"   Ascendente: {converti_gradi_in_segno(ascendente)}")
    profilo.append(f"   Medio Cielo: {converti_gradi_in_segno(mc)}")
    profilo.append("")
    
    # PIANETI NEI SEGNI
    profilo.append("🪐 PIANETI NEI SEGNI:")
    for pianeta in pianeti_ordine:
        if pianeta in posizioni:
            profilo.append(f"   {pianeta}: {converti_gradi_in_segno(posizioni[pianeta])}")
    profilo.append("")
    
    # PIANETI NELLE CASE
    profilo.append("🏠 PIANETI NELLE CASE:")
    for pianeta in pianeti_ordine:
        if pianeta in posizioni:
            casa = pianeta_in_casa(posizioni[pianeta], cusps)
            profilo.append(f"   {pianeta}: Casa {casa} - {interpreta_casa(casa)}")
    profilo.append("")
    
    # CUSPIDI DELLE CASE
    profilo.append("📐 CUSPIDI DELLE CASE:")
    for i in range(12):
        profilo.append(f"   Casa {i+1} ({nomi_case_completi[i]}): {converti_gradi_in_segno(cusps[i])}")
    profilo.append("")
    
    # POTENZE ASTROLOGICHE
    profilo.append("⚡ POTENZE ASTROLOGICHE:")
    profilo.append(f"   🔴 Armonici: +{potenze['totali']['armonici']:.1f}")
    profilo.append(f"   🔵 Disarmonici: {potenze['totali']['disarmonici']:.1f}")
    profilo.append(f"   ⚪ Neutri: +{potenze['totali']['neutri']:.1f}")
    profilo.append(f"   🟣 TOTALE: {potenze['totali']['totale_complessivo']:.1f}")
    profilo.append("")
    
    # ============================================
    # PARTE 1: TUTTE LE CASE NEI SEGNI (escluse 5 e 7)
    # ============================================
    profilo.append("🏠 IL SIGNIFICATO DELLE TUE CASE")
    profilo.append("-" * 40)

    case_da_escludere = [5, 7]

    for num_casa in range(1, 13):
        if num_casa in case_da_escludere:
            continue
        
        # Prendi il grado reale della cuspide (cusps[num_casa-1])
        grado_cuspide = cusps[num_casa-1]
        nome_segno = get_nome_segno(grado_cuspide)  # Questo restituisce 'Sagittario', non '♐'
        simbolo_e_gradi = converti_gradi_in_segno(grado_cuspide)  # Per mostrare all'utente
        
        profilo.append(f"\n📌 Casa {num_casa} - {interpreta_casa(num_casa)}")
        profilo.append(f"   Segno: {simbolo_e_gradi}")
        
        # Usa il NOME del segno per cercare nel database
        if num_casa in calcolatore.segni_sulle_cuspidi and nome_segno in calcolatore.segni_sulle_cuspidi[num_casa]:
            profilo.append(f"   {calcolatore.segni_sulle_cuspidi[num_casa][nome_segno]}")
        
        if info_tema['case_pianeti'][num_casa]:
            pianeti_casa = ", ".join(info_tema['case_pianeti'][num_casa])
            profilo.append(f"   Pianeti presenti: {pianeti_casa}")
    
    # ============================================
    # PARTE 2: TUTTI I PIANETI NELLE CASE (esclusi Luna e Venere)
    # ============================================
    profilo.append("🪐 I TUOI PIANETI NELLE CASE")
    profilo.append("-" * 40)
    
    pianeti_da_escludere = ['Luna', 'Venere']
    
    for pianeta in pianeti_ordine:
        if pianeta in pianeti_da_escludere:
            continue
        if pianeta in info_tema['pianeti_case']:
            casa = info_tema['pianeti_case'][pianeta]
            profilo.append(f"\n📌 {pianeta} in Casa {casa}")
            
            if pianeta in calcolatore.pianeti_case_radix and casa in calcolatore.pianeti_case_radix[pianeta]:
                punteggio = calcola_punteggio_aspetto(pianeta, aspetti)
                tipo = 'armonioso' if punteggio >= 0 else 'dissonante'
                profilo.append(f"   {calcolatore.pianeti_case_radix[pianeta][casa][tipo]}")
    
    profilo.append("\n" + "-" * 40)
    profilo.append("")
    
        # ============================================
    # PARTE 3: TUTTI GLI ASPETTI TRA PIANETI (con messaggi)
    # ============================================
    profilo.append("⚡ LE CONNESSIONI TRA I TUOI PIANETI")
    profilo.append("-" * 40)

    # Raccogliamo gli aspetti per tipo
    congiunzioni = []
    trigoni = []
    sestili = []
    quadrature = []
    opposizioni = []
    quinconci = []

    for aspetto in aspetti:
        if 'CONGIUNZIONE' in aspetto:
            congiunzioni.append(aspetto)
        elif 'TRIGONO' in aspetto:
            trigoni.append(aspetto)
        elif 'SESTILE' in aspetto:
            sestili.append(aspetto)
        elif 'QUADRATURA' in aspetto:
            quadrature.append(aspetto)
        elif 'OPPOSIZIONE' in aspetto:
            opposizioni.append(aspetto)
        elif 'QUINCONCE' in aspetto:
            quinconci.append(aspetto)

    def stampa_aspetto_con_messaggio(aspetto, tipo_aspetto):
        """
        Stampa un aspetto con il suo messaggio
        """
        print(f"\n🔍 DEBUG - Elaboro aspetto: {aspetto}")
        print(f"   Tipo aspetto cercato: {tipo_aspetto}")
        
        parti = aspetto.split(' ')
        if len(parti) >= 3:
            p1 = parti[0].lower()
            p2 = parti[2].lower()
            
            print(f"   Pianeta 1: {p1}")
            print(f"   Pianeta 2: {p2}")
            
            # Prova diversi formati
            formati_da_provare = [
                f"{p1}_{p2}",                    # 'sole_marte'
                f"{p1}_{p2}_{tipo_aspetto}",      # 'sole_marte_trigono'
                f"{p2}_{p1}",                    # 'marte_sole'
                f"{p2}_{p1}_{tipo_aspetto}",      # 'marte_sole_trigono'
            ]
            
            print(f"   Formati da provare: {formati_da_provare}")
            
            msg_trovato = None
            
            for i, formato in enumerate(formati_da_provare):
                print(f"   Provo formato {i+1}: '{formato}'")
                if formato in calcolatore.messaggi_radix:
                    print(f"      ✅ Trovato! '{formato}' esiste nel database")
                    possibile_msg = calcolatore.messaggi_radix[formato]
                    print(f"      Tipo di possibile_msg: {type(possibile_msg)}")
                    print(f"      Chiavi disponibili: {list(possibile_msg.keys()) if isinstance(possibile_msg, dict) else 'non è un dict'}")
                    
                    # Se è un dizionario con 'messaggio' direttamente
                    if isinstance(possibile_msg, dict) and 'messaggio' in possibile_msg:
                        print(f"      ✅ Trovato messaggio diretto!")
                        msg_trovato = possibile_msg
                        break
                    
                    # Se è un dizionario con il tipo come chiave
                    if isinstance(possibile_msg, dict) and tipo_aspetto in possibile_msg:
                        print(f"      ✅ Trovato messaggio dentro chiave '{tipo_aspetto}'!")
                        msg_trovato = possibile_msg[tipo_aspetto]
                        break
                else:
                    print(f"      ❌ Formato '{formato}' non trovato")
            
            profilo.append(f"\n   {aspetto}")
            if msg_trovato:
                print(f"   ✅ MESSAGGIO TROVATO! Aggiungo al profilo")
                profilo.append(f"   {msg_trovato.get('messaggio', '')}")
                profilo.append(f"   💡 {msg_trovato.get('consiglio', '')}")
            else:
                print(f"   ❌ NESSUN MESSAGGIO TROVATO")
                profilo.append(f"   (messaggio non disponibile)")
        else:
            print(f"   ❌ Formato aspetto non riconosciuto: {aspetto}")

    # Stampa gli aspetti in ordine di importanza
    if congiunzioni:
        profilo.append("\n🔹 CONGIUNZIONI:")
        for asp in congiunzioni:
            stampa_aspetto_con_messaggio(asp, 'congiunzione')

    if trigoni:
        profilo.append("\n🔹 TRIGONI:")
        for asp in trigoni:
            stampa_aspetto_con_messaggio(asp, 'trigono')

    if sestili:
        profilo.append("\n🔹 SESTILI:")
        for asp in sestili:
            stampa_aspetto_con_messaggio(asp, 'sestile')

    if quadrature:
        profilo.append("\n🔸 QUADRATURE:")
        for asp in quadrature:
            stampa_aspetto_con_messaggio(asp, 'quadratura')

    if opposizioni:
        profilo.append("\n🔸 OPPOSIZIONI:")
        for asp in opposizioni:
            stampa_aspetto_con_messaggio(asp, 'opposizione')

    if quinconci:
        profilo.append("\n🔸 QUINCONCI:")
        for asp in quinconci:
            stampa_aspetto_con_messaggio(asp, 'quinconce')

    profilo.append("\n" + "-" * 40)
    profilo.append("")
    
    # ============================================
    # PARTE 4: SEZIONE DONNA - RACCONTO PERSONALIZZATO
    # ============================================
    
    
    profilo.append(genera_sezione_donna_avanzata(calcolatore, posizioni, cusps, aspetti))
    
        
        
    # ============================================
    # CHIUSURA
    # ============================================
    profilo.append("="*60)
    profilo.append("💫 Grazie per aver esplorato il tuo cielo interiore.")
    profilo.append("="*60)
    
    # DEBUG
    print(f"\n🔴🔴🔴 PROFILO GENERATO - {len(profilo)} righe 🔴🔴🔴")
    
    # Salva su file per sicurezza
    with open("debug_profilo.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(profilo))
    print("📁 Profilo salvato in debug_profilo.txt")
    
    # CONTROLLO FINALE - ASSICURIAMOCI DI NON RESTITUIRE MAI None
    if not profilo:
        print("ERRORE: profilo è una lista vuota!")
        return "Errore: impossibile generare il profilo"
    
    # Alla fine della funzione genera_profilo_caratteriale, PRIMA del return:

    print(f"🔴🔴🔴 DEBUG FINALE - Lunghezza profilo: {len(profilo)}")
    if not profilo:
        print("❌ ERRORE: profilo è vuoto!")
        return "Errore: profilo vuoto"

    print("✅ Prime 5 righe del profilo:")
    for i, riga in enumerate(profilo[:5]):
        print(f"   {i}: {riga}")

    # Poi il return normale
    return "\n".join(profilo)
