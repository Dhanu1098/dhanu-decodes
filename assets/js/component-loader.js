/**
 * Dhanu Decodes — Component Loader
 * Fetches header.html and footer.html asynchronously and injects them.
 * All pages need: <div id="site-header"></div> and <div id="site-footer"></div>
 */
(async function () {
  'use strict';

  const BASE = '/dhanu-decodes';

  async function loadComponent(id, filename) {
    const container = document.getElementById(id);
    if (!container) return;

    try {
      const resp = await fetch(`${BASE}/components/${filename}`);
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const html = await resp.text();
      container.innerHTML = html;
    } catch (err) {
      console.error(`Failed to load ${filename}:`, err);
      container.innerHTML = ''; // fail silently, no broken UI
    }
  }

  // Load both in parallel
  await Promise.all([
    loadComponent('site-header', 'header.html'),
    loadComponent('site-footer', 'footer.html'),
  ]);

  // After header loads, dispatch event so main.js can init mobile menu
  document.dispatchEvent(new CustomEvent('components-loaded'));
})();
