# Raspberry Pi vorbereiten, Projektverzeichnis einbinden.

## Netzwerkumgebung 

Das Projekt kann in unterschiedlichen Netzwerk-Umgebungen und -Konfigurationen 
sinnvoll umgesetzt werden. Der Raspberry Zero2 hat einen WLAN Controller auf dem Board,
der für die Kommunikation mit dem Enntwicklungsrechener genutzt werden soll. 
Dazu wird aber je nach Netzwerk-Umgebung eventuell zusätzliche Hardware benötigt.
Zusätzliche USB Hardware kann über einen Micro-USB-Hub angeschlossen werden.
![Ein Micro USB Hub mit 4 USB Ports](images/mu_usb_hub.jpg)

<!-- p align="left"> <img src="images/mu_usb_hub.jpg" alt="Ein Micro USB Hub mit 4 USB Ports" style="width:30%; height:auto;">
<br/>µUSB Hub</p -->

### (Scheinbar) einfachster Fall: Entwicklungsrechner und Raspi im gleichen lokalen Netz

Bei der [Installation des Betriebssystems](#betriebssystem-installieren) die
Zugangsdaten für das verwendete WLAN (Netzname, Passwort) eingeben. Prinzipiell
geht es auch, wenn der Raspi in einem anderen erreichbaren Netz eingebunden ist.
Dann kann man ihn etwas umständlicher über seine IP Adresse erreichen.

**Vorteil**<br>
Es kann sofort losgehen mit der Entwicklung

**Nachteil**<br>
Wenn der Rover von einem anderen Rechner außerhalb des lokalen Netzes,
z.B. von einem Handy, gesteuert werden soll, muss ein zusätzlicher WLAN Controller
im Raspi installiert und konfiguriert werden.

### Raspi als lokaler Hotspot

Lässt sich nicht direkt über den Raspberry Pi Imager konfigurieren. 
Daher muss zuerst ein Zugang zu Raspi gefunden werden, über den ein Hotspot 
konfiguriert werden kann.

**Vorteil**<br>
Raspi kann direkt von jedem Rechner, der sich mit dem Hotspot verbindet, 
gesteuert werden.

**Nachteile**
- Der Raspi hat keinen Zugang zum Internet. Wenn Python Module installiert werden
sollen, muss die Konfiguration so geändert werden, dass ein Internetzugang möglich ist.
- Der Entwicklungrechner hat nur Zugang zum Raspi, wenn er sich per WiFi mit dem 
 Raspi Hotspot verbindet.

### Flexibelste Lösung mit zusätzlicher Hardware

Mit einem zusätzlichen Mikro-USB-Hub und ein oder zwei USB Netzwerkadaptern kann
der Raspi sowohl als Hotspot konfiguriert werden als auch über das WLAN
mit dem Internet verbunden sein. Die Verbindung mit dem Entwicklungsrechner kann
entweder über das lokale Netz erfolgen oder über eine direkte Verbindung zu Hotspot.
Für die zweite Lösung braucht es ggf. den zusätzlichen Netzwerkadapter 
im Entwicklungsrechner.

**Vorteil**<br>
Alle Vorteile von oben.

**Nachteil**<br>
Zusätzliche Hardware wird benötigt.

## Betriebssystem installieren

Für die bereitgestellten Raspis im Projekt ist Raspbian bookmark bereits installiert. 
So kann man selber eine passende SD-Karte erstellen:

TODO

<p align="left"> 
<img src="images/RaspiImager1.png" alt="Installationstool für Raspi SD Karten" style="width:30%; height:auto;">
<br/>Raspberry Pi Imager</p>

<p align="left"> 
<img src="images/RaspiImagerConfig.png" alt="Installationstool für Raspi SD Karten" style="width:30%; height:auto;">
<br/>Image anpassen</p>

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