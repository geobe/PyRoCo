# Projekt von github herunterladen, eigenes Repository verbinden

## Eigenen github account und Repository anlegen

Für die Entwicklung braucht jeder Teilnehmer, alternativ jedes Team, einen eigenen Account
auf der Versionsverwaltungs-Plattform github. 
1. Hier lässt sich der [Account anlegen](https://github.com/signup). 
2. Mit dem Button New auf der `Repositories' Seite legen Sie ein neues Repository an.
 Vergeben Sie einen sinnvollen Namen, lasen aber alle anderen Werte auf den Voreinstellungen.
3. Auf der Folgeseite, eventuell unter dem Button `Code`, finden Sie eine URL, die gleich
 noch gebraucht wird. Sie sieht etwa so aus: `https://github.com/<login-name>/<repo-name>.git`

## Startversion des Projekts herunterladen

**Voraussetzung:** Raspberry Pi ist verbunden und das 
[Filesystem wie beschrieben eingebunden](raspi-setup.md#raspi-dateisystem-lokal-einbinden)

1. Mit dem Befehl `cd ~/Development/python/rover` wechseln wir jetzt 
 auf dem Entwicklungsrechner ins Raspi Dateisystem. 
 Dort können wir einmalig mit `mkdir pydev` das Basisverzeichnis für unsere Python Entwicklung anlegen,
 wenn wir das nicht schon gemacht haben und mit `cd pydev` in dieses Verzeichnis wechseln.
2. Hier kann jetzt die Startversion des Projekts von github in das 
 Verzeichnis `rover` heruntergeladen werden.<br/>
 ```
 git clone https://github.com/geobe/PyRoCo.git rover
 ```

## Heruntergeladenes Projekt mit eigenem Repository verbinden