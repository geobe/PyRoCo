# Raspberry Pi verbinden, Projekt von github holen.

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
2. **Nur dieser Schritt muss zu Beginn einer Entwicklungs-Session ausgeführt werden!**<br/>
 Mit dem Befehl `sshfs` das Raspi Dateisystem in das Verzeichnis
 `~/Development/python/rover` einbinden:<br/>
 ```
 sshfs rover@minirover.local:/home/rover/ ~/Development/python/rover \
 -o idmap=user -o uid=$(id -u) -o gid=$(id -g) -o follow_symlinks
 ```
3. Mit dem Befehl `cd ~/Development/python/rover` sind wir jetzt im Raspi Dateisystem. 
 Dort können wir jetzt mit `mkdir pydev` das Basisverzeichnis für unsere Python Entwicklung anlegen,
 wenn wir das nicht schon gemacht haben und mit `cd pydev` in dieses Verzeichnis wechseln.
5. Hier können wir jetzt die Startversion des Projekts von github in das Verzeichnis `rover` herunterladen.<br/>
 ```
 git clone https://github.com/geobe/PyRoCo.git rover
 ```
6. 