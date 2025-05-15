<link rel="stylesheet" type="text/css" href="/static/content/team-card.css" />

% rebase('layout.tpl', title='Our team', year=year)

<div class="title-wrapper">
    <div class="title-card">
        <h3>{{ message }}</h3>
    </div>
</div>

<canvas id="firework-canvas"></canvas>

% rebase('layout.tpl', title=title, year=year)
<div class="team-card-container">
  % for member in members:
    <div class="team-card">
      <img src="{{ member['photo'] }}" alt="Photo of {{ member['nickname'] }}">
      <div class="team-card-body">
        <div class="team-nickname">{{ member['nickname'] }}</div>
        <div class="team-role">{{ member['role'] }}</div>
        <div class="team-comment">{{ member.get('comment', 'No comments') }}</div>
      </div>
    </div>
  % end
</div>

<script>
  try {
    const canvas = document.getElementById('firework-canvas');
    if (!canvas) throw new Error('Canvas element not found');
    const ctx = canvas.getContext('2d');
    if (!ctx) throw new Error('Canvas context not available');
    let fireworks = [];

    // Set canvas size
    function resizeCanvas() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    // Particle class
    class Particle {
      constructor(x, y, color) {
        this.x = x;
        this.y = y;
        this.color = color;
        this.radius = Math.random() * 2 + 1;
        this.velocity = {
          x: (Math.random() - 0.5) * 8,
          y: (Math.random() - 0.5) * 8
        };
        this.alpha = 1;
        this.friction = 0.98;
        this.life = 100;
      }

      draw() {
        ctx.globalAlpha = this.alpha;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
        ctx.globalAlpha = 1;
      }

      update() {
        this.velocity.x *= this.friction;
        this.velocity.y *= this.friction;
        this.x += this.velocity.x;
        this.y += this.velocity.y;
        this.alpha -= 0.01;
        this.life--;
      }
    }

    // Create firework
    function createFirework(x, y) {
      const colors = ['#FF0000', '#FFA500', '#FFFF00']; // Red, Orange, Yellow
      const particleCount = 30;
      for (let i = 0; i < particleCount; i++) {
        const color = colors[Math.floor(Math.random() * colors.length)];
        fireworks.push(new Particle(x, y, color));
      }
    }

    // Animation loop
    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      fireworks = fireworks.filter(p => p.life > 0);
      fireworks.forEach(p => {
        p.update();
        p.draw();
      });
      requestAnimationFrame(animate);
    }
    animate();

    // Add click event to cards
    const cards = document.querySelectorAll('.team-card');
    console.log('Найдено карточек:', cards.length);
    cards.forEach(card => {
      card.addEventListener('click', (e) => {
        const rect = card.getBoundingClientRect();
        const x = rect.left + rect.width / 2;
        const y = rect.top + rect.height / 2;
        console.log('Клик по карточке на:', x, y);
        createFirework(x, y);
      });
    });
  } catch (error) {
    console.error('Ошибка в скрипте фейерверка:', error);
  }
</script>