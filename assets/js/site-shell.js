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
  }

  document.addEventListener('DOMContentLoaded', function () {
    
    const saved = localStorage.getItem('aakaar-theme') || (current === 'day.html' ? 'day' : 'night');
    setTheme(saved);
    const themeBtn = document.querySelector('[data-site-theme]');
    if (themeBtn) {
      themeBtn.addEventListener('click', function () {
        const target = (localStorage.getItem('aakaar-theme') || saved) === 'night' ? 'day' : 'night';
        setTheme(target);
        if (current === 'index.html' || current === 'day.html') location.href = target === 'day' ? 'day.html' : 'index.html';
        else {
          document.body.classList.toggle('night-mode', target === 'night');
          document.body.classList.toggle('light-mode', target === 'day');
          document.body.classList.toggle('dark', target === 'night');
        }
      });
    }
  });
})();
