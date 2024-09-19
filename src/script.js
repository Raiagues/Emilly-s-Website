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
  var fullText = button.nextElementSibling;
  if (fullText.style.display === "none") {
    fullText.style.display = "block";
    button.innerText = "Read Less";
  } else {
    fullText.style.display = "none";
    button.innerText = "Read More";
  }
}