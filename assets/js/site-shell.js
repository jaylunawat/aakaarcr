(function () {
  const current = location.pathname.split('/').pop() || 'index.html';
  
  function renderHeader() {}
  
  function setTheme(theme) {
    const button = document.querySelector('[data-site-theme]');
    if (button) {
      button.textContent = theme === 'night' ? 'NIGHT: ON' : 'DAY: ON';
      button.setAttribute('aria-pressed', String(theme === 'night'));
    }
    localStorage.setItem('aakaar-theme', theme);
    document.body.classList.toggle('light-mode', theme === 'day');
    document.body.classList.toggle('night-mode', theme === 'night');
    document.documentElement.classList.toggle('dark', theme === 'night');
  }

  document.addEventListener('DOMContentLoaded', function () {
    
    const saved = localStorage.getItem('aakaar-theme') || (current === 'day.html' ? 'day' : 'night');
    setTheme(saved);
    const themeBtn = document.querySelector('[data-site-theme]');
    if (themeBtn) {
      themeBtn.addEventListener('click', function () {
        const target = (localStorage.getItem('aakaar-theme') || saved) === 'night' ? 'day' : 'night';
        setTheme(target);
        setTheme(target);
      });
    }
  });
})();
