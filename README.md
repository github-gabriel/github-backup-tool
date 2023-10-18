# GitHub Backup Tool v2.1 (Bug Fix)

In dieser Version wird ein "Fehler" behoben, der beim Anfragen der GitHub API
entstehen kann, da der /repos Endpoint nur 30 Repositorys returnen kann. Für 
Nutzer, die mehr als 30 Repositorys haben kann dies ein Problem sein, daher wird der Code in diesem Bug Fix um eine Methode erweitert, die ALLE Repositorys
eines Nutzers listet und diese dann herunterlädt. Der Rest des Programms funktioniert weiterhin so wie in v2 beschrieben und erwartet.

***Ich bin mir bewusst, dass diese Versionen keiner bestimmten [Konvention](https://semver.org/) folgen***
