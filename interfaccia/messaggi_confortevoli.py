"""
Messaggi confortevoli per i transiti lunari
Un'amica che ti accompagna durante la giornata
"""


MESSAGGI_TRANSITI = {
    # ============================================
    # LUNA IN CASA (dalla 1 alla 12)
    # ============================================
    'luna_in_casa': {
        1: {
            'titolo': "🌙 Luna in prima casa",
            'messaggio': "Per un paio di giorni, le considerazioni personali saranno più importanti. Senti il bisogno di appartenere e avere rapporti con amici e persone care. La tua sensibilità è al massimo e sei ricettiva verso chi ti sta vicino.",
            'consiglio': "💖 Dedicati a te stessa, ma attenzione a non pretendere troppo dagli altri. Un bagno caldo e una crema preferita possono fare miracoli."
        },
        2: {
            'titolo': "🏠 Luna in seconda casa",
            'messaggio': "Ti identifichi emotivamente con ciò che possiedi. Puoi essere più restia a separarti dagli oggetti o più attaccata alla tua scala di valori. Se qualcuno ti chiede qualcosa in prestito, ascolta il cuore.",
            'consiglio': "☕ Circondati di oggetti familiari che ti ricordano bei momenti. Goditi una tazza nella tua tazza preferita."
        },
        3: {
            'titolo': "💬 Luna in terza casa",
            'messaggio': "Le comunicazioni sono più soggettive e profonde. Conversazioni casuali possono assumere significati importanti. Non sei soddisfatta della superficialità, cerchi veri contatti.",
            'consiglio': "📝 Scrivi o chiama qualcuno con cui hai un legame vero. Evita discussioni superficiali."
        },
        4: {
            'titolo': "🏡 Luna in quarta casa",
            'messaggio': "Momento di ritiro e introspezione. Cerchi conforto nel tuo nido, nella famiglia, nei ricordi. È il momento giusto per riflettere su te stessa e sulle tue radici.",
            'consiglio': "🕯️ Accendi una candela profumata, guarda vecchie foto, concediti del tempo in casa."
        },
        5: {
            'titolo': "❤️ Luna in quinta casa",
            'messaggio': "Difficile nascondere i sentimenti. Sei te stessa senza filtri. Le relazioni amorose sono più intense, la creatività è alle stelle. I bambini ti cercano e tu sei più protettiva.",
            'consiglio': "🎨 Dedica tempo alla creatività. Se hai una relazione, un gesto spontaneo farà la differenza."
        },
        6: {
            'titolo': "📋 Luna in sesta casa",
            'messaggio': "Tendenza a posporre le emozioni per le necessità immediate. Puoi essere ipercritica o fare la martire. Meglio usare questa energia per riordinare la casa e la vita.",
            'consiglio': "🧹 Organizza una cosa sola, non di più. Poi premiati. Evita di reprimere le emozioni."
        },
        7: {
            'titolo': "🤝 Luna in settima casa",
            'messaggio': "Le relazioni sono al centro. Cerchi sicurezza e appoggio nel partner o negli amici stretti. Se ci sono conflitti, ti coinvolgono emotivamente più del solito.",
            'consiglio': "👭 Evita discussioni importanti, cerca la compagnia di chi ti vuole bene. Un tè con un'amica è l'ideale."
        },
        8: {
            'titolo': "🌊 Luna in ottava casa",
            'messaggio': "Emozioni più intense, attrazione per persone e situazioni forti. Puoi sentirti più attaccata alle cose che possiedi o desiderare cose altrui. Attenzione ai conflitti su proprietà comuni.",
            'consiglio': "📓 Scrivi cosa senti, anche le emozioni più forti. Rileggile tra qualche giorno."
        },
        9: {
            'titolo': "✈️ Luna in nona casa",
            'messaggio': "Voglia di evadere dalla routine, di andare via. Un'irrequietezza difficile da spiegare. Un viaggio fisico o mentale ti farà bene. Nuove amicizie possibili.",
            'consiglio': "🎵 Crea una playlist di musiche lontane, guarda un documentario, leggi qualcosa di diverso."
        },
        10: {
            'titolo': "🌟 Luna in decima casa",
            'messaggio': "La tua vita emotiva è in mostra. Difficile nascondere qualcosa. Sul lavoro, la tua sensibilità può essere un'arma in più. Attenzione a mescolare personale e professionale.",
            'consiglio': "💼 Dedica 10 minuti a riordinare la scrivania. Un ambiente ordinato porta chiarezza."
        },
        11: {
            'titolo': "👯 Luna in undicesima casa",
            'messaggio': "Le amiche sono importanti. Confidenze, contatti più intensi, bisogno di condividere. Puoi essere più protettiva o cercare protezione. Occhio alla gelosia.",
            'consiglio': "💌 Scrivi un messaggio dolce a un'amica. Organizza una videochiamata con quelle lontane."
        },
        12: {
            'titolo': "🌌 Luna in dodicesima casa",
            'messaggio': "Tendenza a nascondere i sentimenti. Paure e atteggiamenti inconsci possono emergere. Hai bisogno di confidarti con qualcuno di cui ti fidi. Momento di introspezione.",
            'consiglio': "🌿 Fatti un infuso rilassante e stai in silenzio. Ascolta cosa emerge, senza giudizio."
        }
    },
    
    # ============================================
    # LUNA IN ASPETTO CON IL SOLE
    # ============================================
    'luna_sole': {
        'congiunzione': {
            'titolo': "☀️ Luna congiunta al Sole",
            'messaggio': "La tua Luna Nuova personale. Mente e corpo si ricaricano, sentimenti ed emozioni sono in armonia. I rapporti con gli altri, specialmente con l'altro sesso, scorrono meglio.",
            'consiglio': "✨ Prendi un impegno con te stessa per il prossimo mese. Evita operazioni chirurgiche oggi."
        },
        'sestile': {
            'titolo': "😊 Luna in sestile al Sole",
            'messaggio': "Periodo di serenità interiore. Puoi fare il punto su te stessa senza inquietudini. I rapporti sono buoni, sei in grado di capire i bisogni degli altri senza dimenticare i tuoi.",
            'consiglio': "🚶‍♀️ Fai una passeggiata lenta, goditi il momento. Contatta qualcuno che ami."
        },
        'quadratura': {
            'titolo': "🌓 Luna in quadratura al Sole",
            'messaggio': "Emergono tensioni nascoste. Piccole crisi, disagio interiore, difficoltà nei rapporti, specialmente con l'altro sesso. Niente di grave, ma meglio prestare attenzione.",
            'consiglio': "🧘 Affronta i piccoli problemi subito, non dar loro più peso di quanto meritano. Respira."
        },
        'trigono': {
            'titolo': "🌈 Luna in trigono al Sole",
            'messaggio': "Sei in armonia con te stessa. Le energie fluiscono senza opposizioni, la vita sembra più facile. I rapporti sono migliori, gli altri percepiscono la tua serenità.",
            'consiglio': "🎶 Goditi questa giornata di benessere. Fai qualcosa che ami, con chi ami."
        },
        'opposizione': {
            'titolo': "⚖️ Luna in opposizione al Sole",
            'messaggio': "Energie in conflitto. Difficile conciliare vita familiare e professionale, ragione e sentimento. Possibili tensioni con l'altro sesso. Attenzione alle nuove conoscenze.",
            'consiglio': "🤸‍♀️ Cerca di mediare tra le diverse esigenze. Non prendere decisioni impulsive oggi."
        }
    },
    
    # ============================================
    # LUNA IN ASPETTO CON MERCURIO
    # ============================================
    'luna_mercurio': {
        'congiunzione': {
            'titolo': "💭 Luna congiunta a Mercurio",
            'messaggio': "Logica e sensazioni si fondono. Facile esprimere i sentimenti, comunicare con le donne. Repentini cambiamenti d'umore. Non è il momento per decisioni importanti.",
            'consiglio': "📝 Scrivi ciò che senti, ma aspetta a decidere. Le informazioni che raccogli oggi saranno utili dopo."
        },
        'sestile': {
            'titolo': "🗣️ Luna in sestile a Mercurio",
            'messaggio': "Ritmo sociale accelerato. Chiacchiere, pettegolezzi, contatti con amici. Facile esprimere i sentimenti a parole. Notizie, lettere, telefonate in arrivo.",
            'consiglio': "📞 Chiama un amico, scrivi una lettera. Oggi le parole arrivano al cuore."
        },
        'quadratura': {
            'titolo': "⚡ Luna in quadratura a Mercurio",
            'messaggio': "Crisi nella comunicazione con chi ti è vicino. Emozioni sopraffanno la ragione. Forte bisogno di parlare, ma rischio di peggiorare le cose. Meglio aspettare.",
            'consiglio': "😮‍💨 Se devi affrontare un problema, rimanda. Oggi è facile fraintendere e essere fraintese."
        },
        'trigono': {
            'titolo': "💫 Luna in trigono a Mercurio",
            'messaggio': "Equilibrio tra sentimento e ragione. Grande sensibilità emotiva ma pensiero logico. Puoi ricevere notizie importanti sul passato o sulla famiglia.",
            'consiglio': "💌 Scrivi a chi ami. Le parole non ti tradiranno. Ottimo per messaggi profondi."
        },
        'opposizione': {
            'titolo': "🔄 Luna in opposizione a Mercurio",
            'messaggio': "Conflitto tra sentimenti e ragione. Possibile introspezione proficua se gestita con calma. Altrimenti, pregiudizi e vecchie abitudini offuscano la lucidità.",
            'consiglio': "🧘 Appartati con te stessa a fare il punto. Distingui le emozioni dai giudizi razionali."
        }
    },
    
    # ============================================
    # LUNA IN ASPETTO CON VENERE
    # ============================================
    'luna_venere': {
        'congiunzione': {
            'titolo': "🌸 Luna congiunta a Venere",
            'messaggio': "Periodo perfetto per socializzare. Irraggi calore, gli altri amano starti vicino. Ottimo per la persona amata, per abbellire casa, per ricevere ospiti. Attenzione alla spesa.",
            'consiglio': "💅 Regalati una coccola, ma con moderazione. Se esci, sarà una bella serata."
        },
        'sestile': {
            'titolo': "💕 Luna in sestile a Venere",
            'messaggio': "Bisogno di stare con amici e persone amate. Relazioni amorose favorite. Momento propizio per uscire. Attenzione a non diventare troppo passiva e aspettare tutto dagli altri.",
            'consiglio': "👭 Invita un'amica. Goditi la compagnia, ma mantieniti attiva."
        },
        'quadratura': {
            'titolo': "🍰 Luna in quadratura a Venere",
            'messaggio': "Periodo piacevole nonostante l'aspetto. Godi della compagnia, dei contatti sociali. Più affettuosa con chi ami. Attenzione a non diventare troppo possessiva o a esagerare con cibo e bevande.",
            'consiglio': "🍫 Concediti un piccolo sfizio, ma con moderazione. Goditi i ricordi, ma non trascurare il presente."
        },
        'trigono': {
            'titolo': "💖 Luna in trigono a Venere",
            'messaggio': "Sensazioni gradevoli per te e chi ti sta accanto. Perfetto per stare con gli amici. Piacere di mangiare e bere, ma senza eccedere. Pigrizia, ma anche voglia di abbellire casa.",
            'consiglio': "🎨 Dedicati a un hobby creativo o a rendere più bella la tua casa. L'amore è protettivo, non possessivo."
        },
        'opposizione': {
            'titolo': "✨ Luna in opposizione a Venere",
            'messaggio': "Periodo soddisfacente, ma attenzione a non eccedere. Desiderio di intensi rapporti emotivi. I legami sono buoni, le tensioni si allentano. Controlla la tendenza a fare acquisti impulsivi.",
            'consiglio': "🛍️ Se compri qualcosa, aspetta un giorno prima di decidere. Approfitta per capire meglio le tue relazioni."
        }
    },
    
    # ============================================
    # LUNA IN ASPETTO CON MARTE
    # ============================================
    'luna_marte': {
        'congiunzione': {
            'titolo': "🔥 Luna congiunta a Marte",
            'messaggio': "Ti senti irritabile, impulsiva. Rischio di perdere la calma per cose da poco. Agisci d'impulso senza ragionare. Se controllata, questa energia può diventare intraprendenza.",
            'consiglio': "💃 Sfoga l'energia ballando o facendo attività fisica. Conta fino a tre prima di reagire."
        },
        'sestile': {
            'titolo': "💪 Luna in sestile a Marte",
            'messaggio': "Efficiente nel lavoro, da sola o in gruppo. Piena di iniziativa, coraggio, fiducia in te stessa. Comunichi apertamente, senza essere offensiva. Attrai persone forti.",
            'consiglio': "✅ Inizia quel progetto che rimandavi. La tua energia è costruttiva oggi."
        },
        'quadratura': {
            'titolo': "⚡ Luna in quadratura a Marte",
            'messaggio': "Rischio di liti senza motivo, irritabilità, passionalità eccessiva. Rapporti difficili. Meglio sfogarsi senza trascendere. Attenzione a incidenti domestici con oggetti taglienti.",
            'consiglio': "🧘 Respira. Se senti rabbia, allontanati dalla situazione. Tornerà la calma."
        },
        'trigono': {
            'titolo': "💫 Luna in trigono a Marte",
            'messaggio': "Sai farti valere in modo positivo. Coraggiosa e sicura, prendi iniziative senza essere offensiva. Buona per funzioni direttive. Energia fisica alta. Attenzione a non iniziare cose che poi non finisci.",
            'consiglio': "🏋️‍♀️ Sfrutta l'energia per attività fisica. Inizia, ma assicurati di poter portare a termine."
        },
        'opposizione': {
            'titolo': "🤺 Luna in opposizione a Marte",
            'messaggio': "Emotivamente eccitabile e irritabile. Poca tolleranza, ti secchi per inezie. Rapporti tesi, specialmente con le donne. Meglio mantenere la calma a tutti i costi.",
            'consiglio': "🚶‍♀️ Evita movimenti improvvisi. Se ci sono problemi familiari, affrontali a mente più serena."
        }
    },
    
    # ============================================
    # LUNA IN ASPETTO CON GIOVE
    # ============================================
    'luna_giove': {
        'congiunzione': {
            'titolo': "🎉 Luna congiunta a Giove",
            'messaggio': "Momenti di buone intenzioni e generosità. Sensazione che tutto vada bene. Difficile irritarti, tolleri anche la scontrosità altrui. Ottime relazioni femminili.",
            'consiglio': "🤗 Fai un gesto gentile per qualcuno. Ti tornerà indietro moltiplicato."
        },
        'sestile': {
            'titolo': "🌟 Luna in sestile a Giove",
            'messaggio': "Ti senti a posto, stai bene con chi ti è simpatico. Ideale con vecchi amici, ma aperta a nuove conoscenze. Reciproco sostegno e dedizione. Ottimo per attività collettive.",
            'consiglio': "👭 Condividi un'attività con amici. Lavorare insieme oggi dà soddisfazione."
        },
        'quadratura': {
            'titolo': "✨ Luna in quadratura a Giove",
            'messaggio': "Transito molto positivo. Ti senti benevola e generosa. Interesse per religione o filosofia. Attenzione a non diventare presuntuosa o arrogante, gli altri lo notano.",
            'consiglio': "📚 Coltiva i tuoi interessi spirituali, ma resta umile. Osserva le reazioni degli altri."
        },
        'trigono': {
            'titolo': "🌈 Luna in trigono a Giove",
            'messaggio': "Peccato sia breve, perché infonde gran benessere. Calore, amicizia, desiderio di aiutare. Gli altri ricambiano. Attrai persone di buon umore. Condivisione vera.",
            'consiglio': "🌳 Goditi la giornata. Il benessere degli altri è anche il tuo oggi."
        },
        'opposizione': {
            'titolo': "🔄 Luna in opposizione a Giove",
            'messaggio': "Generalmente positivo, ma richiede scelte. Sei generosa, ma solo se spontanea. Se qualcuno ti forza, resisti. Nei rapporti, non tolleri la possessività. Inquietudine spirituale.",
            'consiglio': "❓ Chiediti cosa vuoi veramente. Le risposte possono essere importanti."
        }
    },
    
    # ============================================
    # LUNA IN ASPETTO CON SATURNO
    # ============================================
    'luna_saturno': {
        'congiunzione': {
            'titolo': "🌑 Luna congiunta a Saturno",
            'messaggio': "Tendenza a tenere per te i sentimenti. Senso di solitudine, isolamento, pessimismo. Niente di grave, passa. Problemi domestici possibili. Rapporti con le donne difficili.",
            'consiglio': "😴 Non prendere decisioni sulla vita affettiva oggi. Domani tutto sarà più chiaro."
        },
        'sestile': {
            'titolo': "🧘 Luna in sestile a Saturno",
            'messaggio': "Desiderio di stare in pace a meditare. Preferisci compagnia seria e conversazioni impegnative. Equilibrio tra impulsi emotivi e dovere. Cautela e ponderazione.",
            'consiglio': "📖 Cerca il consiglio di una persona saggia. Il suo punto di vista ti aiuterà."
        },
        'quadratura': {
            'titolo': "☁️ Luna in quadratura a Saturno",
            'messaggio': "Passeggera depressione, sensazione di solitudine e abbandono. Difficoltà a comunicare emozioni. Incomprensioni. Non è tutto nero come sembra, è solo una prospettiva distorta.",
            'consiglio': "🧠 Renditi conto che oggi vedi tutto peggio. Non prendere decisioni. Domani passa."
        },
        'trigono': {
            'titolo': "🌳 Luna in trigono a Saturno",
            'messaggio': "Pieno controllo delle emozioni, senza reprimerle. Visione sobria e realistica. Risorse interiori di forza. Sicura di te. Attrazione per il passato e la conservazione.",
            'consiglio': "📦 Circondati di oggetti familiari che ami. La stabilità interiore si riflette fuori."
        },
        'opposizione': {
            'titolo': "🌧️ Luna in opposizione a Saturno",
            'messaggio': "Effetti catastrofici sulle relazioni. Ti senti isolata, come se nessuno volesse comunicare. Depressione senza motivo. Meglio non fare nulla, non prendere decisioni.",
            'consiglio': "🫂 Non starti addosso. Spiega agli altri che sei di pessimo umore, ti capiranno. Passa."
        }
    },
    
    # ============================================
    # LUNA IN ASPETTO CON URANO
    # ============================================
    'luna_urano': {
        'congiunzione': {
            'titolo': "⚡ Luna congiunta a Urano",
            'messaggio': "Impulsiva, avventata. Stati d'animo cambiano rapidamente. Insofferenza per la routine. Meglio seguire l'impulso, ma attenzione a non pentirtene dopo. Dura poche ore.",
            'consiglio': "🎨 Fai qualcosa di completamente diverso oggi. Sperimenta, ma con cautela."
        },
        'sestile': {
            'titolo': "🌀 Luna in sestile a Urano",
            'messaggio': "Piacevole bisogno di movimento, desiderio di eccitamento. Vuoi scuotere il prossimo o sei tu ad essere scossa. Insofferenza in casa. Nuove amicizie stimolanti.",
            'consiglio': "🔄 Cambia qualcosa in casa, anche piccolo. Nuove idee stimolano la fantasia."
        },
        'quadratura': {
            'titolo': "🌪️ Luna in quadratura a Urano",
            'messaggio': "Attenzione a non essere precipitosi. Spirito di indipendenza e ribellione. Fai il contrario di ciò che ti dicono. Bisogno di libertà, di fare qualcosa di selvaggio. Irrequietezza emotiva.",
            'consiglio': "🚶‍♀️ Se hai voglia di cambiare, ricordati che è passeggero. Non stravolgere tutto."
        },
        'trigono': {
            'titolo': "✨ Luna in trigono a Urano",
            'messaggio': "Cerchi eccitazione, novità, compagnia nuova. Impulsiva ma non irrazionale. Puoi apportare utili modifiche alla vita e all'ambiente domestico. Possibili sorprese.",
            'consiglio': "🏠 Modifica qualcosa in casa. I cambiamenti oggi sono costruttivi."
        },
        'opposizione': {
            'titolo': "🌋 Luna in opposizione a Urano",
            'messaggio': "Eccitabile e impulsiva. Evita mosse decisive. Cerchi stimoli, attrai gente diversa. Comportamento provocatorio. Periodo burrascoso. Se qualcuno ti condiziona, reagisci male.",
            'consiglio': "😮‍💨 Controlla le reazioni inconsulte. Se puoi, stai da sola fino a che passa."
        }
    },
    
    # ============================================
    # LUNA IN ASPETTO CON NETTUNO
    # ============================================
    'luna_nettuno': {
        'congiunzione': {
            'titolo': "🌊 Luna congiunta a Nettuno",
            'messaggio': "Sensibilità accentuata. Assorbi gli stati d'animo altrui come una spugna. Evita persone negative. Fantasia stimolata. Rischio di eccedere con alcol o stimolanti. Comunicazione confusa.",
            'consiglio': "🎶 Ascolta musica, lasciati trasportare. Attenzione alle auto-illusioni."
        },
        'sestile': {
            'titolo': "💫 Luna in sestile a Nettuno",
            'messaggio': "Molto sensibile agli umori altrui. Stai bene con i cari amici. Altruista, compassionevole. Desiderio di ritirarti nel tuo mondo interiore. Interesse per l'occulto o lo spirituale.",
            'consiglio': "🔮 Se hai interessi spirituali, oggi è un buon giorno per coltivarli."
        },
        'quadratura': {
            'titolo': "☁️ Luna in quadratura a Nettuno",
            'messaggio': "Stati d'animo sognanti, fantasia e illusione prevalgono. Non prendere decisioni. Influenze subconsce forti. Sensibilità accresciuta. Rischio di eccedere con alcol o droghe.",
            'consiglio': "📓 Scrivi i tuoi sogni, ma non prendere decisioni. Interpretali in seguito."
        },
        'trigono': {
            'titolo': "🌈 Luna in trigono a Nettuno",
            'messaggio': "Emergono fantasie del subconscio. Fantasticare fa bene. Stimola l'immaginazione, utile per attività artistiche. Compassione vera, altruismo. Ricettiva agli stati d'animo altrui.",
            'consiglio': "🎨 Dedicati all'arte o alla creatività. Le tue intuizioni oggi sono preziose."
        },
        'opposizione': {
            'titolo': "🌫️ Luna in opposizione a Nettuno",
            'messaggio': "Umore strano. Sensibile ma percezioni poco chiare. Dubbi e sospetti immotivati. Incomprensioni. Emergono complessi dal subconscio. Evita alcol e droghe.",
            'consiglio': "🧘 Stai in silenzio. Quello che senti oggi è frutto di processi interiori, non della realtà."
        }
    },
    
    # ============================================
    # LUNA IN ASPETTO CON PLUTONE
    # ============================================
    'luna_plutone': {
        'congiunzione': {
            'titolo': "🌋 Luna congiunta a Plutone",
            'messaggio': "Esperienze emotive intense. Energie profonde emergono. Seduta di auto-analisi proficua. Idee ossessive possibili. Rapporti con donne intensi. Attenzione a gelosia e possessività.",
            'consiglio': "🔍 Scrivi cosa senti. Non sopravvalutare l'importanza di queste emozioni, sono di breve durata."
        },
        'sestile': {
            'titolo': "💫 Luna in sestile a Plutone",
            'messaggio': "Risveglia sentimenti profondi. Cerchi esperienze impegnative, non superficiali. Interesse per il misterioso, l'occulto, la psicologia. Bisogno di cambiamenti in casa.",
            'consiglio': "📚 Leggi qualcosa che stimoli la mente. Attenzione a non fissarti su un'unica idea."
        },
        'quadratura': {
            'titolo': "🌪️ Luna in quadratura a Plutone",
            'messaggio': "Emozioni prepotenti, difficile resistere agli impulsi. Opportunità di vedere dentro te stessa. Confronti emotivi utili ma non sempre piacevoli. Conflitti di potere emotivo.",
            'consiglio': "🫂 Se senti gelosia o sensi di colpa, osservali come onde. Non agire d'impulso."
        },
        'trigono': {
            'titolo': "💖 Luna in trigono a Plutone",
            'messaggio': "Emozioni intense ma non distruttive. Relazioni profonde. Esperienze spirituali ed emozionali. Rapporti sessuali arricchiti. Attenzione a non diventare maniacale su un'idea.",
            'consiglio': "🤗 Cerca la vera essenza dei sentimenti. Le relazioni oggi si rafforzano."
        },
        'opposizione': {
            'titolo': "🌑 Luna in opposizione a Plutone",
            'messaggio': "Emozioni profonde e non armoniose. Conflitti emotivi con gli altri e dentro di te. Sensi di colpa, gelosia, passionalità, possessività. Difficile vedere chiaramente.",
            'consiglio': "📓 Se hai sensazioni forti, esprimile (scrivendo). Reprimerle peggiora le cose. Non prendere decisioni."
        }
    }
}