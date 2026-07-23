/**
 * Dhanu Decodes — Main JavaScript
 * Scroll animations, mobile menu, theme toggle, scroll-to-top, component loader
 */
(function () {
  'use strict';

  /* ====== DOM READY ====== */
  function domReady(fn) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', fn);
    } else {
      fn();
    }
  }

  /* ====== THEME TOGGLE ====== */
  function initTheme() {
    const saved = localStorage.getItem('dhanu-decodes-theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const theme = saved || (prefersDark ? 'dark' : 'light');
    if (theme === 'light') {
      document.documentElement.setAttribute('data-theme', 'light');
    }
    // else default is dark (no attribute needed since CSS defaults to dark)
  }

  function setupThemeToggle() {
    const toggle = document.querySelector('.theme-toggle');
    if (!toggle) return;
    toggle.addEventListener('click', function () {
      const current = document.documentElement.getAttribute('data-theme');
      if (current === 'light') {
        document.documentElement.removeAttribute('data-theme');
        localStorage.setItem('dhanu-decodes-theme', 'dark');
      } else {
        document.documentElement.setAttribute('data-theme', 'light');
        localStorage.setItem('dhanu-decodes-theme', 'light');
      }
    });
  }

  /* ====== MOBILE MENU ====== */
  function setupMobileMenu() {
    const toggle = document.querySelector('.mobile-menu-toggle');
    const nav = document.querySelector('.nav-links');
    if (!toggle || !nav) return;

    toggle.addEventListener('click', function () {
      const expanded = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!expanded));
      toggle.classList.toggle('active');
      nav.classList.toggle('active');
      document.body.style.overflow = expanded ? '' : 'hidden';
    });

    // Close menu on link click
    nav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        toggle.setAttribute('aria-expanded', 'false');
        toggle.classList.remove('active');
        nav.classList.remove('active');
        document.body.style.overflow = '';
      });
    });
  }

  /* ====== SCROLL ANIMATIONS (Intersection Observer) ====== */
  function setupScrollAnimations() {
    var observerOptions = {
      root: null,
      rootMargin: '0px 0px -60px 0px',
      threshold: 0.1,
    };

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);

    document.querySelectorAll('.article-card, .animate-on-scroll').forEach(function (el) {
      observer.observe(el);
    });
  }

  /* ====== SCROLL TO TOP BUTTON ====== */
  function setupScrollToTop() {
    var btn = document.querySelector('.scroll-top-btn');
    if (!btn) return;

    var ticking = false;
    window.addEventListener('scroll', function () {
      if (!ticking) {
        requestAnimationFrame(function () {
          if (window.scrollY > 400) {
            btn.classList.add('visible');
          } else {
            btn.classList.remove('visible');
          }
          ticking = false;
        });
        ticking = true;
      }
    });

    btn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ====== SMOOTH SCROLL FOR ANCHOR LINKS ====== */
  function setupSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
      anchor.addEventListener('click', function (e) {
        var targetId = this.getAttribute('href');
        if (targetId === '#') return;
        var target = document.querySelector(targetId);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });
  }

  /* ====== INIT ====== */
  domReady(function () {
    initTheme();
    setupThemeToggle();
    setupMobileMenu();
    setupScrollAnimations();
    setupScrollToTop();
    setupSmoothScroll();
  });
})();
