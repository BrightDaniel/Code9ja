function counter(element) {
    const count = parseInt(element.getAttribute("data-count"));
    const speed = Math.round(count / 200);

    const timer = setInterval(() => {
      const value = parseInt(element.innerText);
      if (value < count) {
        element.innerText = value + speed;
      } else {
        element.innerText = count;
        clearInterval(timer);
      }
    }, 50);
  }

  // Start counter when user scrolls up to the section
  const counters = document.querySelectorAll(".counter");
  let counterStarted = false;
  window.addEventListener("scroll", () => {
    if (!counterStarted && window.scrollY + window.innerHeight >= document.querySelector(".muse-section").offsetTop) {
      counters.forEach(counter);
      counterStarted = true;
    }
  });


 // Function to check if element is in viewport

 window.addEventListener('scroll', function() {
    const section = document.querySelector('.think');
    const sectionPosition = section.getBoundingClientRect().top;
    const screenPosition = window.innerHeight / 1.5;
  
    if (sectionPosition < screenPosition) {
      section.classList.add('animate__animated', 'animate__slideInLeft');
    } else {
      section.classList.remove('animate__animated', 'animate__slideInLeft');
    }
  });
  
  

//

window.addEventListener('scroll', function() {
    const section = document.querySelector('.courses');
    const sectionPosition = section.getBoundingClientRect().top;
    const screenPosition = window.innerHeight / 1.5;
  
    if (sectionPosition < screenPosition) {
      section.classList.add('animate__animated', 'animate__slideInRight');
    } else {
      section.classList.remove('animate__animated', 'animate__slideInRight');
    }
  });








// const slideRightElements = document.querySelectorAll('.slide-right');

// function slideRight() {
//   slideRightElements.forEach(slideRightElement => {
//     if (isElementInViewport(slideRightElement)) {
//       slideRightElement.classList.add('show');
//     }
//   });
// }

// function isElementInViewport(el) {
//   const rect = el.getBoundingClientRect();
//   return (
//     rect.top >= 0 &&
//     rect.left >= 0 &&
//     rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
//     rect.right <= (window.innerWidth || document.documentElement.clientWidth)
//   );
// }

// window.addEventListener('scroll', slideRight);

