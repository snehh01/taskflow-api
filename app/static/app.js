(() => {
  const modal = document.getElementById('task-modal');
  const openers = [document.getElementById('open-create'), document.getElementById('empty-create')].filter(Boolean);
  const closers = [document.getElementById('close-create'), document.getElementById('cancel-create')].filter(Boolean);
  const titleInput = modal?.querySelector('input[name="title"]');
  function openModal() {
    if (!modal) return;
    modal.classList.add('open'); modal.setAttribute('aria-hidden', 'false');
    window.setTimeout(() => titleInput?.focus(), 100);
  }
  function closeModal() {
    if (!modal) return;
    modal.classList.remove('open'); modal.setAttribute('aria-hidden', 'true');
  }
  openers.forEach(button => button.addEventListener('click', openModal));
  closers.forEach(button => button.addEventListener('click', closeModal));
  modal?.addEventListener('click', event => { if (event.target === modal) closeModal(); });
  document.addEventListener('keydown', event => { if (event.key === 'Escape') closeModal(); });
  const date = document.getElementById('today-label');
  if (date) {
    const parsed = new Date(`${date.textContent.trim()}T12:00:00`);
    if (!Number.isNaN(parsed.getTime())) date.textContent = parsed.toLocaleDateString('en-US', {month:'short', day:'numeric', year:'numeric'});
  }
})();
