document.getElementById('seeMoreBtn').addEventListener('click', function() {
  const hiddenItems = document.querySelectorAll('.gallery-item.hidden');
  const allItems = document.querySelectorAll('.gallery-item');

  if (hiddenItems.length > 0) {
      hiddenItems.forEach(item => {
          item.classList.remove('hidden'); 
      });
      this.textContent = 'See Less'; 
  } else {
      document.querySelectorAll('.gallery-item').forEach((item, index) => {
          if (index > 2) { 
              item.classList.add('hidden'); 
          }
      });
      this.textContent = 'See More'; 
  }
});
