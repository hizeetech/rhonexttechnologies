// Theme toggle and reveal animations
(function () {
  const body = document.body;
  const toggle = document.getElementById('themeToggle');
  const icon = document.getElementById('themeIcon');

  // Initialize theme from localStorage
  const saved = localStorage.getItem('theme');
  if (saved === 'light') {
    body.classList.remove('theme-dark');
    body.classList.add('theme-light');
    if (icon) icon.className = 'fa-solid fa-sun';
  } else {
    body.classList.remove('theme-light');
    body.classList.add('theme-dark');
    if (icon) icon.className = 'fa-solid fa-moon';
  }

  // Toggle handler
  if (toggle) {
    toggle.addEventListener('click', function () {
      const isLight = body.classList.contains('theme-light');
      if (isLight) {
        body.classList.remove('theme-light');
        body.classList.add('theme-dark');
        localStorage.setItem('theme', 'dark');
        if (icon) icon.className = 'fa-solid fa-moon';
      } else {
        body.classList.remove('theme-dark');
        body.classList.add('theme-light');
        localStorage.setItem('theme', 'light');
        if (icon) icon.className = 'fa-solid fa-sun';
      }
    });
  }

  // IntersectionObserver for reveal animations
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));

  // Lightweight testimonials slider
  const slider = document.querySelector('.testimonials-slider');
  if (slider) {
    const slidesEl = slider.querySelector('.slides');
    const slides = Array.from(slidesEl.children);
    const dotsContainer = slider.querySelector('.slider-dots');
    let index = 0;

    // Create dots
    if (dotsContainer) {
      slides.forEach((_, i) => {
        const dot = document.createElement('button');
        dot.className = 'slider-dot';
        dot.setAttribute('aria-label', `Go to slide ${i + 1}`);
        dot.addEventListener('click', () => { index = i; update(true); });
        dotsContainer.appendChild(dot);
      });
    }

    const updateDots = () => {
      if (!dotsContainer) return;
      const dots = Array.from(dotsContainer.children);
      dots.forEach((d, i) => d.classList.toggle('is-active', i === index));
    };

    const update = (instant = false) => {
      slides.forEach((s, i) => {
        s.classList.toggle('is-active', i === index);
        if (instant) {
          s.style.transition = 'none';
          requestAnimationFrame(() => s.style.transition = '');
        }
      });
      updateDots();
    };
    const next = () => { index = (index + 1) % slides.length; update(); };
    const prev = () => { index = (index - 1 + slides.length) % slides.length; update(); };

    let intervalId = setInterval(next, 6000);
    const pause = () => { if (intervalId) { clearInterval(intervalId); intervalId = null; } };
    const resume = () => { if (!intervalId) { intervalId = setInterval(next, 6000); } };
    slider.addEventListener('mouseenter', pause);
    slider.addEventListener('mouseleave', resume);
    slider.querySelectorAll('[data-action="next"]').forEach(btn => btn.addEventListener('click', () => { pause(); next(); }));
    slider.querySelectorAll('[data-action="prev"]').forEach(btn => btn.addEventListener('click', () => { pause(); prev(); }));
    update(true);
  }

  // Subtle parallax for angled dividers
  const dividers = document.querySelectorAll('.angled-divider[data-parallax]');
  if (dividers.length) {
    let ticking = false;
    dividers.forEach(d => d.setAttribute('data-parallax-active', 'true'));
    const onScroll = () => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          dividers.forEach(div => {
            const rect = div.getBoundingClientRect();
            const viewportH = window.innerHeight || document.documentElement.clientHeight;
            const progress = Math.max(0, Math.min(1, 1 - rect.top / viewportH));
            const y = 20 + progress * 12; // move a bit as it scrolls
            div.style.setProperty('--parallax-y', y);
            const pseudo = div;
            // Adjust via inline style on ::before through transform property on the element
            // We can simulate by toggling a CSS variable and using it in CSS if needed
            // For simplicity, apply transform to before via style attribute is not possible, so tweak using dataset
            // Instead, apply transform to a child overlay if present (not used here)
            div.style.setProperty('--divider-translate', `${y}%`);
          });
          ticking = false;
        });
        ticking = true;
      }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
  }
  
  // Featured Projects carousel with controls, dots, hover pause, and swipe
  const projectsCarousel = document.querySelector('.projects-carousel');
  if (projectsCarousel) {
    const track = projectsCarousel.querySelector('.track');
    const items = Array.from(track ? track.children : []);
    const dotsContainer = projectsCarousel.querySelector('.slider-dots');
    const prevBtn = projectsCarousel.querySelector('[data-action="prev-projects"]');
    const nextBtn = projectsCarousel.querySelector('[data-action="next-projects"]');
    if (track && items.length > 0) {
      const intervalSec = parseInt(projectsCarousel.getAttribute('data-interval-seconds') || '5', 10) || 5;
      let timer = null;

      const getGap = () => {
        const style = getComputedStyle(track);
        return parseFloat(style.columnGap || style.gap || '0');
      };
      const getItemWidth = () => items[0].getBoundingClientRect().width + getGap();
      // Add one gap to numerator to account for no trailing gap on the last item
      const getItemsPerView = () => Math.max(1, Math.round((track.clientWidth + getGap()) / getItemWidth()));
      const getPages = () => Math.max(1, Math.ceil(items.length / getItemsPerView()));
      const getCurrentPage = () => Math.round(track.scrollLeft / track.clientWidth);

      const goToPage = (page) => {
        const pages = getPages();
        const clamped = Math.max(0, Math.min(page, pages - 1));
        track.scrollTo({ left: clamped * track.clientWidth, behavior: 'smooth' });
        updateDots(clamped);
      };
      const nextPage = () => goToPage(getCurrentPage() + 1 >= getPages() ? 0 : getCurrentPage() + 1);
      const prevPage = () => goToPage(getCurrentPage() - 1 < 0 ? getPages() - 1 : getCurrentPage() - 1);

      // Dots
      const renderDots = () => {
        if (!dotsContainer) return;
        dotsContainer.innerHTML = '';
        const pages = getPages();
        for (let i = 0; i < pages; i++) {
          const dot = document.createElement('button');
          dot.className = 'slider-dot';
          dot.setAttribute('aria-label', `Go to slide ${i + 1}`);
          dot.addEventListener('click', () => { stop(); goToPage(i); });
          dotsContainer.appendChild(dot);
        }
        updateDots(getCurrentPage());
      };
      const updateDots = (activeIndex) => {
        if (!dotsContainer) return;
        Array.from(dotsContainer.children).forEach((d, i) => d.classList.toggle('is-active', i === activeIndex));
      };

      // Auto scroll per page
      const start = () => { if (!timer) timer = setInterval(nextPage, Math.max(1, intervalSec) * 1000); };
      const stop = () => { if (timer) { clearInterval(timer); timer = null; } };

      // Controls
      if (nextBtn) nextBtn.addEventListener('click', () => { stop(); nextPage(); });
      if (prevBtn) prevBtn.addEventListener('click', () => { stop(); prevPage(); });

      // Hover pause
      projectsCarousel.addEventListener('mouseenter', stop);
      projectsCarousel.addEventListener('mouseleave', start);

      // Swipe support
      let touchStartX = null; let touchStartTime = 0;
      const threshold = 40; // px
      projectsCarousel.addEventListener('touchstart', (e) => {
        const t = e.changedTouches[0]; touchStartX = t.clientX; touchStartTime = Date.now(); stop();
      }, { passive: true });
      projectsCarousel.addEventListener('touchend', (e) => {
        const t = e.changedTouches[0]; const dx = t.clientX - (touchStartX ?? t.clientX);
        const dt = Date.now() - touchStartTime; if (Math.abs(dx) > threshold && dt < 800) { dx < 0 ? nextPage() : prevPage(); }
        start();
      }, { passive: true });

      // Initialize
      renderDots();
      window.addEventListener('resize', () => { renderDots(); updateDots(getCurrentPage()); });
      start();
    }
  }
})();