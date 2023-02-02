# `rules.py`
Contiene le regole applicabili

# `word_graph.py`
Gestisce il grafo delle parole (classe WordGraph), dove ogni nodo è una
parola del dizionare e ogni arco è una regola valida tra le due parole (le
regole non sono simmetriche).
Utilizziamo la libreria networkx, in particolare la classe MultiDiGraph
(Multi = ogni coppia di nodi può avere più archi (regole), Di = Directional: le regole non sono simmetriche).
E' dotato di funzioni per leggere da file un grafo se esiste già, altrimenti crea i file mancanti.

# `dictionaries.py`
Legge e scrive su file i vari dizionari, ha metodi utili per ottenere la lista dei dizionari disponibili, ecc...

# `preferences.py`
Legge e escrive su file le preferenze dell'utente, nel nostro caso abbiamo solamente il dizionario che deve partire
in automatico quando viene startata l'applicazione. In pratica gestisce il "Ricorda la scelta" nel menu iniziale.

# `active_rules.py`
Legge e escrive su file le impostazioni delle regole di un determinato dizionario, nel nostro caso
ogni regola ha associato il suo peso, o `None` se la regola è disabilitata.

# `files.py`
Funzioni utili per leggere-scrivere su file.

# `gui.py`
Main del programma, starta la gui, utilizza il framework *tkinter* per le interfacce grafiche.
Se "Ricorda la scelta" è attivo l'utente viene rimandato subito a `dictionary_loading_widget`,
altrimenti viene fatto scegliere all'utente il dizionario da utilizzare (`dictionaries_widget`).

# `dictionaries_widget.py`
Schermata di scelta del dizionario.

# `dictionary_loading_widget.py`
Schermata di caricamento.

# `word_graph_widget.py`
Schermata di ricerca del percorso minimo.

# `word_graph_settings_widget.py`
Schermata di selezione delle regole per il percorso minimo.

# `widgets.py`
Funzioni e widget utili per la gui.
