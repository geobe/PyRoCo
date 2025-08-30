# Raspberry Pi verbinden

## Betriebssystem installieren

Für die Raspis im Projekt ist Raspbian bookmark bereits installiert. 
So kann man selber eine passende SD-Karte erstellen:

TODO

## Raspi Dateisystem lokal einbinden

Der Raspi muss im lokalen Netz erreichbar sein. Hat der Raspi z.B. den Netzwerknamen 'minirover',
dann sollte er mit 'minirover.local' erreichbar sein.
Wenn das nicht klappt, notfalls IP-Adresse verwenden.  Der Befehl 'ping minirover.local' sollte
erfolgreich die Verbindung testen.

Auf dem Raspi muss außerdem der ssh Server installiert sein.
Das ist normalerweise der Fall. Falls nicht, mit `sudo apt install openssh-server` installieren.
1. Auf dem Entwicklungsrechner  das Verzeichnis `~/Development/python/rover` anlegen,
 wenn noch nicht vorhanden:<br/>`mkdir -p ~/Development/python/rover`
2. Jetzt mit dem Befehl `sshfs` das Raspi Dateisystem in das Verzeichnis
 `~/Development/python/rover` einbinden:<br/>
 ```
 sshfs rover@minirover.local:/home/rover/ ~/Development/python/rover \
 -o idmap=user -o uid=$(id -u) -o gid=$(id -g) -o follow_symlinks
 ```
3. 