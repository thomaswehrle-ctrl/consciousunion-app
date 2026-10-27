# Conscious Union App – automatisch aktualisiert

Die App (`index.html`) liest stündlich Deine Seiten **Aktuell**, **Programme** und **Shop** auf consciousunion.ch und baut sich selbst neu. Termine, Preise, Programme und Produkte werden also nur noch auf Deiner Homepage gepflegt. Start-Text, Grundsätze und „Wer wir sind" bleiben fest in `template.html`.

## Einrichten (einmalig, ca. 15 Minuten, kostenlos)

1. Auf github.com ein Konto anlegen und ein neues **öffentliches** Repository erstellen, zum Beispiel `conscious-union-app`.
2. Die Dateien `index.html`, `template.html`, `build.py` und `README.md` hochladen (Add file → Upload files).
3. Add file → Create new file. Als Dateiname `.github/workflows/update.yml` eingeben (die Schrägstriche legen die Ordner an) und den Inhalt der Datei `update.yml` aus diesem Paket einfügen. Speichern (Commit).
4. Settings → Pages: Source „Deploy from a branch", Branch `main`, Ordner `/ (root)`. Nach etwa einer Minute steht oben die Adresse der App, zum Beispiel `https://DEINNAME.github.io/conscious-union-app/`.
5. Reiter Actions → „App aktualisieren" → Run workflow. Das ist der erste Probelauf. Wird er grün, funktioniert alles.

Die Adresse kann ohne Anmeldung geöffnet werden. Auf dem iPhone in Safari: Teilen → Zum Home-Bildschirm. Wer eine eigene Adresse wie app.consciousunion.ch möchte, trägt sie unter Settings → Pages → Custom domain ein.

## Was passiert bei Problemen?

Findet das Skript zu wenige Einträge (zum Beispiel weil Jimdo den Seitenaufbau ändert), bricht der Lauf rot ab und `index.html` bleibt unverändert. Die App zeigt dann einfach den letzten guten Stand. GitHub schickt Dir dazu eine E-Mail. Geplante Läufe schaltet GitHub in Repositories ohne Aktivität nach 60 Tagen ab. Bleibt die App stehen, im Reiter Actions den Workflow wieder aktivieren.

## Anpassen

- Aktuelle Termine, Programme, Shop: nur auf der Homepage ändern.
- Texte der App, Titelbild, Farben: in `template.html`.
- Sofort aktualisieren: Actions → App aktualisieren → Run workflow.
