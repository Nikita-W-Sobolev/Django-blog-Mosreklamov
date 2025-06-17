// Показываем модальное окно
function showDeleteModal(articleId) {
  const modal = document.getElementById(`deleteModal-${articleId}`);
  modal.style.display = "block";

  // Закрытие при клике вне окна
  modal.addEventListener('click', function(e) {
    if (e.target === modal) {
      closeModal(articleId);
    }
  });
}

// Закрываем модальное окно
function closeModal(articleId) {
  const modal = document.getElementById(`deleteModal-${articleId}`);
  modal.style.display = "none";
}

// Закрытие по Escape
document.addEventListener('keydown', function(e) {
  if (e.key === "Escape") {
    document.querySelectorAll('.modal').forEach(modal => {
      modal.style.display = "none";
    });
  }
});