/**
 * Dhanu Decodes — Main JavaScript
 * Scroll animations, mobile menu, scroll-to-top
 */
(function () {
  'use strict';

  // Wait for components to load before initializing
  function init() {
    initMobileMenu();
    initScrollAnimations();
    initScrollToTop();
    initSmoothScroll();
  }

  // --- Mobile Menu ---
  function initMobileMenu() {
    const toggle = document.querySelector('.mobile-menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    if (!toggle || !navLinks) return;

    toggle.addEventListener('click', function () {
      const expanded = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!expanded));
      toggle.classList.toggle('active');
      navLinks.classList.toggle('active');
    });

    // Close menu on link click
    navLinks.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        toggle.setAttribute('aria-expanded', 'false');
        toggle.classList.remove('active');
        navLinks.classList.remove('active');
      });
    });
  }

  // --- Scroll Animations (fade in cards on scroll) ---
  function initScrollAnimations() {
    var cards = document.querySelectorAll('.article-card:not(.visible)');
    if (!cards.length) return;

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -30px 0px' });

    cards.forEach(function (card, i) {
      card.style.transitionDelay = (i * 0.1) + 's';
      observer.observe(card);
    });
  }

  // --- Scroll to Top Button ---
  function initScrollToTop() {
    var btn = document.querySelector('.scroll-top-btn');
    if (!btn) return;

    var ticking = false;
    window.addEventListener('scroll', function () {
      if (!ticking) {
        requestAnimationFrame(function () {
          btn.classList.toggle('visible', window.scrollY > 500);
          ticking = false;
        });
        ticking = true;
      }
    });

    btn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // --- Smooth Scroll for Anchor Links ---
  function initSmoothScroll() {
    document.addEventListener('click', function (e) {
      var link = e.target.closest('a[href^="#"]');
      if (!link) return;
      var target = document.querySelector(link.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  }

  // Run on DOMContentLoaded (components now baked into HTML)
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
