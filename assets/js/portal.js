(function () {
  const key = 'aakaar-theme';
  function setTheme(theme) {
    document.body.classList.toggle('light-mode', theme === 'light');
    const button = document.querySelector('[data-theme-toggle]');
    if (button) {
      button.setAttribute('aria-pressed', String(theme === 'light'));
      button.querySelector('[data-theme-label]').textContent = theme === 'light' ? 'DAY' : 'NIGHT';
      button.title = theme === 'light' ? 'Switch to night mode' : 'Switch to light mode';
    }
    localStorage.setItem(key, theme);
  }
  document.addEventListener('DOMContentLoaded', function () {
    const button = document.querySelector('[data-theme-toggle]');
    if (!button) return;
    setTheme(localStorage.getItem(key) || 'night');
    button.addEventListener('click', function () {
      setTheme(document.body.classList.contains('light-mode') ? 'night' : 'light');
    });
  });
}());
