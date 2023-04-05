
// FUNCTION TO COUNT DOWN ACHIEVEMNTS IN THE COUNTER SECTION OF MISSION PAGE STARTS //
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

  // FUNCTION TO COUNT DOWN ACHIEVEMNTS IN THE COUNTER SECTION OF MISSION PAGE ENDS //



 // FUNCTION TO CHECK IF DIFFERENT SESSIONS ARE IN VIEWPORTS THEN PERFROM ANIMATIONS  STARTS //
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


  window.addEventListener('scroll', function() {
    const section = document.querySelector('.partners');
    const sectionPosition = section.getBoundingClientRect().top;
    const screenPosition = window.innerHeight / 1.5;
  
    if (sectionPosition < screenPosition) {
      section.classList.add('animate__animated', 'animate__slideInLeft');
    } else {
      section.classList.remove('animate__animated', 'animate__slideInLeft');
    }
  });
  

  window.addEventListener('scroll', function() {
    const section = document.querySelector('.faq');
    const sectionPosition = section.getBoundingClientRect().top;
    const screenPosition = window.innerHeight / 1.5;
  
    if (sectionPosition < screenPosition) {
      section.classList.add('animate__animated', 'animate__slideInRight');
    } else {
      section.classList.remove('animate__animated', 'animate__slideInRight');
    }
  });
  

  window.addEventListener('scroll', function() {
    const section = document.querySelector('.contact');
    const sectionPosition = section.getBoundingClientRect().top;
    const screenPosition = window.innerHeight / 1.5;
  
    if (sectionPosition < screenPosition) {
      section.classList.add('animate__animated', 'animate__slideInLeft');
    } else {
      section.classList.remove('animate__animated', 'animate__slideInLeft');
    }
  });
  
 // FUNCTION TO CHECK IF DIFFERENT SESSIONS ARE IN VIEWPORTS THEN PERFROM ANIMATIONS  STARTS //



// FUNCTION TO SEND MAIL VIA EMAIL JS

  (function(){
    emailjs.init('ij4GaCYFg6LQ5hbOU');
 })();

  function sendEmail(contactForm) {
    emailjs.send("service_123v6yh","template_zgwwr1i", {
       "from_name": contactForm.name.value,
       "from_email": contactForm.email.value,
       "subject": contactForm.subject.value,
       "message": contactForm.message.value
    })
    .then(function(response) {
       // Display success message
       swal({
          title: "Success!",
          text: "Your message has been sent.",
          icon: "success",
       });
       // Clear form fields
       contactForm.reset();
    }, function(error) {
       // Display error message
       swal({
          title: "Oops...",
          text: "Something went wrong. Please try again later.",
          icon: "error",
       });
    });
    return false; // Prevent page reload on submit
 }
 


