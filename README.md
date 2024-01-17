# Spotify Shuffler

Crea una playlist che ha le stesse canzoni di un'altra playlist, ma in un ordine diverso.

Purtroppo non è possibile farlo in-place/nella coda, perché le API di Spotify non lo permettono :unamused:

# Guida a setup del progetto

1. Eseguire **pip install**
2. Seguire questo video per il file .env: (prima o poi scrivo anche questa parte)

   - https://www.youtube.com/watch?v=-FsFT6OwE1A

# Guida sull'utilizzo

Eseguire **main.py** da terminale e seguire le istruzioni.

Aggiungere un artista nella **lista tra i preferiti**, aumenterà le possibilità delle tracce di quest'ultimo di uscire nell'estrazione casuale. Ovvero, risulteranno più in cima.

Aggiungere un artista od un album alla **lista da ignorare** farà in modo che le canzoni che abbiamo quell'artista tra i crediti o che si trovino nell'album non possano venire inserite nella playlist.

