(function () {
  const stylesheet = document.createElement('link');
  stylesheet.rel = 'stylesheet';
  stylesheet.href = 'assets/css/portal-theme.css';
  document.head.appendChild(stylesheet);
  document.body.classList.add('night-page');
  const pages = {
    home: 'index.html', about: 'about.html', 'roles-quests': 'roles.html',
    'incentives-loot': 'incentives.html', 'scores-leaderboard': 'leaderboard.html',
    faqs: 'faq.html', 'team-contact': 'team.html', 'login-portal': 'index.html#portal-access'
  };
  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-path]').forEach(function (item) {
      if (pages[item.dataset.path]) item.href = pages[item.dataset.path];
    });
  });
}());
