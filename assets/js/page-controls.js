(function () {
  const storageKey = 'aakaar-theme';
  const routes = {
    home: 'index.html', about: 'about.html', 'roles-quests': 'roles.html',
    'incentives-loot': 'incentives.html', 'scores-leaderboard': 'leaderboard.html',
    faqs: 'faq.html', 'team-contact': 'team.html', 'login-portal': 'index.html#portal-access'
  };
  const nightStyles = `
    body.night-mode { background:#0c0e14 !important;color:#e2e2eb !important;background-image:linear-gradient(to right,rgba(36,255,205,.05) 1px,transparent 1px),linear-gradient(to bottom,rgba(255,208,38,.05) 1px,transparent 1px) !important;background-size:24px 24px!important; }
    body.night-mode header,body.night-mode footer,body.night-mode [class*="bg-surface"]{background-color:#161822!important}
    body.night-mode [class*="bg-primary-container"]{background-color:#ffd026!important;color:#08090d!important}
    body.night-mode [class*="bg-secondary"],body.night-mode [class*="bg-tertiary"]{background-color:#1f2333!important}
    body.night-mode [class*="text-on-surface"],body.night-mode [class*="text-on-background"],body.night-mode [class*="text-on-surface-variant"]{color:#e2e2eb!important}
    body.night-mode [class*="border-on-surface"]{border-color:#2a2f45!important}
    body.night-mode .pixel-box-shadow{box-shadow:4px 4px #000!important}body.night-mode .pixel-box-shadow-sm{box-shadow:2px 2px #000!important}
  `;
  function setTheme(theme) {
    document.body.classList.toggle('night-mode', theme === 'night');
    const button = document.querySelector('[data-page-theme]');
    if (button) {
      button.textContent = theme === 'night' ? 'NIGHT: ON' : 'DAY: ON';
      button.setAttribute('aria-pressed', String(theme === 'night'));
      button.title = theme === 'night' ? 'Switch to day mode' : 'Switch to night mode';
    }
    localStorage.setItem(storageKey, theme);
  }
  document.addEventListener('DOMContentLoaded', function () {
    const style = document.createElement('style');
    style.textContent = nightStyles;
    document.head.appendChild(style);
    document.querySelectorAll('[data-path]').forEach(function (link) {
      const target = routes[link.dataset.path];
      if (target) link.href = target;
    });
    setTheme(localStorage.getItem(storageKey) || 'night');
  });
}());
