window.onload = function() {
  const video = document.getElementById('myVideo');
  const image = document.getElementById('myImage');

  // Verwende ein statisches Bild als Hintergrund, wenn das Video endet
  video.addEventListener('ended', function() {
    video.style.display = 'none'; // Verstecke das Video
    image.style.display = 'block'; // Zeige das Bild
  });

  const videoPlayed = sessionStorage.getItem("video_played") === "true";

  if (videoPlayed) {
    video.style.display = 'block';
    video.play();
  }

  // Navigation logic
  document.getElementById('link-home').onclick = showHome;
  document.getElementById('link-ki').onclick = showKi;
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


function showKi() {
  window.location.href = "http://localhost:8501";
}

function showQuiz() {
  document.getElementById('content').innerHTML = `
    <div class="center-content" style="padding-top: 40px;">
        <h1 style="font-size: 36px; margin-bottom: 10px;">Quiz-Seite</h1>
        <p style="font-size: 24px; text-align: center; margin-bottom: 5px;">
          <strong><u>Sorry</u>, diese Seite ist momentan nicht verfügbar.</strong>
        </p>
        <p style="font-size: 18px; text-align: center; margin-bottom: 20px;">
          Wir arbeiten daran, diese euch bald zur Verfügung zu stellen.
        </p>
        <img src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmtmNzc5bDBhbWNmMHd1dDM1amV3aXM3YXQ1a3lvdm9hOGd3bHBweCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/qQdL532ZANbjy/giphy.gif" alt="Trauriges GIF" style="width: 150px; height: auto; margin-top: 20px;">
        <button onclick="showHome();" style="margin-top: 20px;">Zurück zur Startseite</button>
    </div>
  `;
}

function showAbout() {
  document.getElementById('content').innerHTML = `
    <div class="about-container">
      <h1 class="about-title">About Us</h1>
      <div class="about-section">
        <div class="about-text-left">
          <h3 class="about-subtitle">Welcome to my platform</h3>
          <p class="about-benefits-text">
            Your AI chatbot for SAP certification support
          </p>
          <p class="about-text">
            This platform is dedicated to helping learners prepare for SAP certifications. Our mission is to facilitate access to complex knowledge and provide effective help to learners.
          </p>
          <p class="about-text">
            This AI chatbot specializes in simplifying learning content on SAP certifications and helping you answer your questions. The platform is designed to act as an interactive tutor that customizes the learning process to your needs. We offer quizzes, interactive learning modules, and a user-friendly interface to facilitate your learning.
          </p>
        </div>
        <div class="about-image-right">
          <img src="imgs/about_image_1.png" alt="About Us Image" class="about-image">
        </div>
      </div>
      <div class="about-section">
        <div class="about-image-left">
          <img src="imgs/about_image_2.png" alt="Project Image" class="about-image">
        </div>
        <div class="about-text-right">
          <h3 class="sub-title">The Project</h3>
          <h3 class="about-subtitle">Our Motivation</h3>
          <p class="about-text">
            The world of SAP certificates can be overwhelming and complex. The sheer volume of material and the complexity of the topics present many with significant challenges. There is often a lack of easily accessible resources or experts to turn to when questions arise. This is why I developed this AI chatbot. I am a student of [your degree programme] and have experienced first-hand how difficult it can be to navigate the abundance of information. This experience motivated me to develop a solution that allows everyone to learn more efficiently and with more confidence.
          </p>
          <p class="about-text">
            This project was created as part of my bachelor's thesis and is an expression of my commitment to education and technology. I want to help make the world of learning more accessible and supportive for everyone. By combining my knowledge of [your degree programme] and passion for innovative technology, I hope to make a small but significant contribution to the education community.
          </p>
        </div>
      </div>
      <div class="benefits-section">
        <h3 class="sub-title">Our Benefits</h3>
        <p class="about-benefits-text">
          By using CertifyAI,
          <br>one can avail a lot of benefits.
        </p>
        <div class="benefit-list">
          <div class="benefit-item">
            <h4 class="benefit-title">Personalized Support</h4>
            <p class="benefit-text">
              CertifyAI offers you customized support by adapting to your individual learning needs. So you always get the answers you need to make effective progress.
            </p>
          </div>
          <div class="benefit-item">
            <h4 class="benefit-title">Reduced Costs</h4>
            <p class="benefit-text">
              Avoid the high costs of expensive books and seminars. Our platform offers an affordable alternative that still provides extensive and high-quality learning material.
            </p>
          </div>
          <div class="benefit-item">
            <h4 class="benefit-title">Time Saving</h4>
            <p class="benefit-text">
              Complex content can be learned quickly and in easy-to-understand sections. The interactive modules allow you to prepare efficiently for exams without wasting time on unnecessary material.
            </p>
          </div>
          <div class="benefit-item">
            <h4 class="benefit-title">Flexibility and Accessibility</h4>
            <p class="benefit-text">
              Our platform is completely web-based, which means you can learn wherever you have access to the internet. Whether you're at your desk, in a café, or at home, you can access all learning resources with our user-friendly interface.
            </p>
          </div>
          <div class="benefit-item">
            <h4 class="benefit-title">Learner Satisfaction</h4>
            <p class="benefit-text">
              Our users report high satisfaction rates and an improved understanding of SAP topics. The positive learning experience motivates and empowers you to achieve your goals.
            </p>
          </div>
          <div class="benefit-item">
            <h4 class="benefit-title">Extensive Knowledge Database</h4>
            <p class="benefit-text">
              Benefit from our comprehensive knowledge base that covers a wide range of topics and frequently asked questions about SAP certifications. Our platform provides you with detailed explanations and practical tips to deepen your understanding and expand your knowledge.
            </p>
          </div>
        </div>
      </div>
    </div>
  `;
}
