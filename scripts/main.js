window.onload = function() {
    const video = document.getElementById('myVideo');
    const image = document.getElementById('myImage');
  
    // Stelle sicher, dass das Video nur einmal abgespielt wird
    video.addEventListener('ended', function() {
      video.style.display = 'none'; // Verstecke das Video
      document.body.style.backgroundImage = `url('imgs/video.png')`; // Setze das Standbild als Hintergrund
      document.body.style.backgroundSize = 'cover'; // Größe des Hintergrundbildes anpassen
      document.body.style.backgroundPosition = 'center'; // Hintergrundbild zentrieren
    });
  
    const videoPlayed = sessionStorage.getItem("video_played") === "true";
  
    if (videoPlayed) {
      video.style.display = 'block';
      video.play();
    }
  
    // Navigation logic
    document.getElementById('link-home').onclick = showHome;
    document.getElementById('link-ki').onclick = navigateToStreamlit;
    document.getElementById('link-quiz').onclick = showQuiz;
    document.getElementById('link-about').onclick = showAbout;
  
    showHome(); // Initial page load
  };
  
  function showHome() {
    sessionStorage.setItem("video_played", "true");
    document.getElementById('content').innerHTML = `
      <div class="center-content">
          <h1>SAP AI ASSISTANT</h1>
          <button onclick="navigateToStreamlit();">Get Started!</button>
      </div>
    `;
  }
  
  function navigateToStreamlit() {
    window.location.href = "http://localhost:8501"; // Ändere die URL, falls nötig
  }
  
  function showKi() {
    document.getElementById('content').innerHTML = `
      <div class="center-content">
          <h1>KI</h1>
          <p>Hier können Sie mit unserer KI interagieren. Geben Sie Ihre Anfragen ein und erhalten Sie die gewünschten Informationen.</p>
          <input type="text" style="width: 80%; padding: 10px; font-size: 16px;" placeholder="Geben Sie Ihre Anfrage ein:">
      </div>
    `;
  }
  
  function showQuiz() {
    document.getElementById('content').innerHTML = `
      <div class="center-content" style="flex-direction: row; align-items: flex-start;">
          <div style="max-width: 400px; text-align: left;">
              <h1>Quiz-Seite</h1>
              <p>Sorry, diese Seite ist momentan nicht verfügbar. Wir arbeiten daran, diese euch bald zur Verfügung zu stellen.</p>
              <button onclick="showHome();" style="margin-top: 20px;">Zurück zur Startseite</button>
          </div>
          <img src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmtmNzc5bDBhbWNmMHd1dDM1amV3aXM3YXQ1a3lvdm9hOGd3bHBweCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/qQdL532ZANbjy/giphy.gif" alt="Trauriges GIF" style="width: 150px; height: auto; margin-left: 20px;">
      </div>
    `;
  }
  
  function showAbout() {
    document.getElementById('content').innerHTML = `
      <div class="center-content">
          <h1>Über die KI</h1>
          <p>Die Welt der SAP-Zertifikate kann überwältigend sein. Aus diesem Grund habe ich diese KI entwickelt, um Lernenden zu helfen, die Herausforderungen der umfangreichen SAP-Literatur zu bewältigen. Ziel ist es, eine Plattform zu bieten, die den Lernprozess vereinfacht und den Zugang zu wertvollem Wissen erleichtert. Mit dieser KI haben Sie einen verlässlichen Partner an Ihrer Seite, der Ihnen hilft, alle Hürden zu meistern.</p>
          <button onclick="showHome();" style="margin-top: 20px;">Zurück zur Startseite</button>
      </div>
    `;
  }
  