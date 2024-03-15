[![Run Tests on Main Push or Merge](https://github.com/enricogoerlitz/WeeklyChef-Backend/actions/workflows/main.yaml/badge.svg)](https://github.com/enricogoerlitz/WeeklyChef-Backend/actions/workflows/main.yaml)

# WeeklyChef REST-API


# NEXT STEPS (Jenkins):

Um eine CI/CD-Pipeline für die beschriebenen Schritte einzurichten, können Sie Jenkins verwenden, da es eine weit verbreitete CI/CD-Plattform ist und eine Vielzahl von Plugins zur Integration mit GitHub und Docker bietet. Hier ist ein allgemeiner Ansatz, wie Sie vorgehen könnten:

1. **Installieren und Konfigurieren von Jenkins**: Installieren Sie Jenkins auf Ihrem Linux-Server und konfigurieren Sie es entsprechend Ihren Anforderungen. Stellen Sie sicher, dass Jenkins auf GitHub zugreifen kann, um Änderungen in Ihrem Code-Repository zu erkennen.

2. **Erstellen Sie ein Jenkins-Projekt**: Erstellen Sie ein neues Jenkins-Projekt, das Ihre CI/CD-Pipeline enthalten wird.

3. **Konfigurieren Sie den GitHub-Webhook**: Konfigurieren Sie einen GitHub-Webhook, um Jenkins über Änderungen in Ihrem Code-Repository zu informieren. Dadurch wird die Pipeline automatisch gestartet, wenn Änderungen in den Main-Branch gepusht werden.

4. **Testausführung**: Konfigurieren Sie Jenkins, um Ihre Tests auszuführen. Sie können einen Build-Schritt hinzufügen, der die erforderlichen Tests ausführt.

5. **Docker-Image-Build**: Fügen Sie einen weiteren Build-Schritt hinzu, um das Docker-Image zu bauen. Verwenden Sie das Docker-Build-Plugin oder das Docker-CLI, um das Image zu erstellen.

6. **Docker-Image-Push zu Docker Hub**: Fügen Sie einen weiteren Schritt hinzu, um das gebaute Docker-Image auf Docker Hub hochzuladen. Sie müssen die Docker-Hub-Anmeldeinformationen in Jenkins konfigurieren, um das Image hochzuladen.

7. **Linux-Server-Deployment**: Konfigurieren Sie einen weiteren Build-Schritt in Jenkins, der nach dem erfolgreichen Hochladen des Docker-Images auf Docker Hub aufgerufen wird. Dieser Schritt sollte SSH-Verbindungen zum Linux-Server verwenden, um das neueste Docker-Image herunterzuladen und Docker Compose auszuführen, um die Anwendung neu zu starten.

Beachten Sie, dass Sie auf Ihrem Linux-Server SSH-Zugriff und die Installation von Docker und Docker Compose benötigen. Außerdem sollten Sie sicherstellen, dass Jenkins Zugriff auf Ihren Docker Hub und den Linux-Server hat, um die erforderlichen Aktionen durchzuführen.

Dies ist ein allgemeiner Leitfaden. Die genaue Implementierung hängt von Ihren spezifischen Anforderungen und Ihrer Infrastruktur ab.
