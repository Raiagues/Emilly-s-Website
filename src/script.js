// script.js

const menuIcon = document.getElementById('menu-icon');
const navbar = document.getElementById('navbar');
const hamburgerIcon = document.getElementById('hamburger-icon');
const closeIcon = document.getElementById('close-icon');

menuIcon.addEventListener('click', function () {
  navbar.classList.toggle('active'); 

  if (navbar.classList.contains('active')) {
    hamburgerIcon.style.display = 'none';  
    closeIcon.style.display = 'block';     
  } else {
    hamburgerIcon.style.display = 'block'; 
    closeIcon.style.display = 'none';      
  }
});

function toggleText(button) {
  var fullText = button.parentNode.previousElementSibling; 
  
  if (fullText.style.display === "none" || fullText.style.display === "") {
      fullText.style.display = "block";  
      button.innerText = "Read Less";   
  } else {
      fullText.style.display = "none";  
      button.innerText = "Read More";   
  }
}
document.addEventListener('DOMContentLoaded', function() {
  const filterGroups = document.querySelectorAll('.filter-group input[type="checkbox"]');
  const projects = document.querySelectorAll('.projects-box');
  const toggleBtn = document.getElementById('toggleBtn');
  const deselectAllBtn = document.getElementById('deselectAllBtn');
  const toggleFilterBtn = document.getElementById('toggleFilterBtn');
  const filterBar = document.getElementById('filterBar');
  const selectedFiltersDiv = document.getElementById('selectedFilters');

  // Initializes to show only the first 3 projects
  showInitialProjects();

  // Set up click listeners for each filter header
  const filterHeaders = document.querySelectorAll('.filter-header');
  filterHeaders.forEach(header => {
      header.addEventListener('click', function() {
          const content = this.nextElementSibling; // Get the next sibling (filter-content)
          content.style.display = content.style.display === 'block' ? 'none' : 'block'; // Toggle display
      });
  });

  filterGroups.forEach(checkbox => {
      checkbox.addEventListener('change', function() {
          filterProjects();
          updateSelectedFilters(); // Update the selected filters display
      });
  });

  toggleBtn.addEventListener('click', function() {
      const hiddenProjects = document.querySelectorAll('.projects-box.hidden-more3');

      if (hiddenProjects.length > 0) {
          hiddenProjects.forEach(project => {
              project.classList.remove('hidden-more3');
              project.style.display = 'grid'; // Shows the project
          });

          this.textContent = 'Show Less';
      } else {
          hideExtraProjects();
          this.textContent = 'Show More';
      }

      // Updates the button visibility after the action
      updateToggleButtonVisibility();
  });

  // Deselect all checkboxes when the button is clicked
  deselectAllBtn.addEventListener('click', function() {
      filterGroups.forEach(checkbox => {
          checkbox.checked = false; // Uncheck each checkbox
      });
      filterProjects(); // Call filterProjects to update the project visibility
      updateSelectedFilters(); // Update the selected filters display
  });

  // Toggle the visibility of the filter bar
  toggleFilterBtn.addEventListener('click', function() {
      const isVisible = !filterBar.classList.contains('hidden'); // Check if the filter bar is currently visible
      filterBar.classList.toggle('hidden'); // Toggle the hidden class
      this.textContent = isVisible ? 'Show Filters' : 'Hide Filters'; // Change button text accordingly
  });

  function filterProjects() {
      const selectedKeywords = Array.from(filterGroups)
          .filter(checkbox => checkbox.checked)
          .map(checkbox => checkbox.value);

      let visibleCount = 0;

      projects.forEach(project => {
          const keywords = project.getAttribute('data-keywords').split(', ');
          const isMatch = selectedKeywords.length === 0 || selectedKeywords.every(keyword => keywords.includes(keyword));

          if (isMatch) {
              project.style.display = 'grid'; // Shows the project if there's a match
              project.classList.remove('hidden-not-selected'); // Removes the hidden-not-selected class
              visibleCount++; // Counts visible projects
          } else {
              project.style.display = 'none'; // Hides the project if there's no match
              project.classList.add('hidden-not-selected'); // Adds the hidden-not-selected class
          }
      });

      // Logic for the hidden-more3 class
      if (selectedKeywords.length > 0) {
          // If there is any selection, remove the hidden-more3 class
          projects.forEach(project => project.classList.remove('hidden-more3'));

          // If there are more than 3 visible projects, apply hidden-more3
          if (visibleCount > 3) {
              const visibleProjects = Array.from(projects).filter(p => p.style.display === 'grid');
              visibleProjects.slice(3).forEach(project => {
                  project.classList.add('hidden-more3');
                  project.style.display = 'none'; // Hides those projects
              });
          }
      } else {
          // If there is no selection, just apply the hidden-more3 logic
          hideExtraProjects();
      }

      // Updates the button visibility
      updateToggleButtonVisibility();
  }

  function showInitialProjects() {
      projects.forEach((project, index) => {
          if (index < 3) {
              project.classList.remove('hidden-more3'); // Removes the hidden-more3 class
              project.style.display = 'grid'; // Shows the first 3 projects
          } else {
              project.classList.add('hidden-more3'); // Adds the hidden-more3 class
              project.style.display = 'none'; // Hides the others
          }
      });

      // Updates the button visibility after initializing
      updateToggleButtonVisibility();
  }

  function hideExtraProjects() {
      projects.forEach((project, index) => {
          if (index > 2) {
              project.classList.add('hidden-more3'); // Adds the hidden-more3 class
              project.style.display = 'none'; // Hides all beyond the first 3
          }
      });

      // Updates the button visibility after hiding projects
      updateToggleButtonVisibility();
  }

  function updateToggleButtonVisibility() {
      // Count the total number of projects, regardless of visibility
      const totalCount = projects.length;

      // If there are no filter selections
      if (Array.from(filterGroups).every(checkbox => !checkbox.checked)) {
          // The button should only be displayed if there are 4 or more projects available
          toggleBtn.style.display = totalCount >= 4 ? 'inline-block' : 'none';
      } else {
          // If there are filter selections, check the total selected
          const totalSelectedCount = Array.from(projects).filter(project => {
          const keywords = project.getAttribute('data-keywords').split(', ');
            return Array.from(filterGroups)
                .filter(checkbox => checkbox.checked)
                .every(checkbox => keywords.includes(checkbox.value));
          }).length;

          // The button should be displayed if there are 4 or more selected projects
          toggleBtn.style.display = totalSelectedCount >= 4 ? 'inline-block' : 'none';
      }
  }

  function updateSelectedFilters() {
      const selectedKeywords = Array.from(filterGroups)
          .filter(checkbox => checkbox.checked)
          .map(checkbox => checkbox.value);

      // Update the selected filters display
      selectedFiltersDiv.innerHTML = selectedKeywords.length > 0
          ? `<strong>Selected Filters:</strong> ${selectedKeywords.join(', ')}`
          : '<strong>No filters selected.</strong>';
  }
});


document.addEventListener('DOMContentLoaded', function () {
    const toggleFilterBtn = document.getElementById('toggleFilterBtn');
    const filterBar = document.getElementById('filterBar');
    const deselectAllBtn = document.getElementById('deselectAllBtn');
  
    toggleFilterBtn.addEventListener('click', function () {

        
      if (!filterBar.classList.contains('hidden')) {
        deselectAllBtn.classList.remove('hidden');
      } else {
        deselectAllBtn.classList.add('hidden');
      }
    });
  });
  