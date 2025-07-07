document.addEventListener('DOMContentLoaded', function() {

    // Contact Form Variables
    const contactLink = document.querySelector('#contact-link');
    const contactForm = document.querySelector('#contact-form');
    const closeFormButton = document.querySelector('#close-form');

    // Features Page Variables
    const featuresLink = document.querySelector('#features-link');
    const featuresPage = document.querySelector('#features-page');
    const homeLink = document.querySelector('#home-link');

    // Function to show the contact form
    function showContactForm(event) {
        event.preventDefault();
        contactForm.classList.add('open');
    }

    // Function to hide the contact form
    function hideContactForm(event) {
        event.preventDefault();
        contactForm.classList.remove('open');
    }

   // Function to show the features page and fade in images
// Function to show the features page and fade in images
function showFeaturesPage(event) {
    event.preventDefault();

    if (!featuresPage.classList.contains('open')) {
        featuresPage.style.display = 'block';
        setTimeout(() => {
            featuresPage.classList.add('open');
            fadeImagesIn(); // Trigger the image fade-in function
        }, 100); // Add a slight delay before adding the 'open' class
    }
}

// Event listener for the "Features" link
if (featuresLink) featuresLink.addEventListener('click', showFeaturesPage);

// Function to fade in images one by one
function fadeImagesIn() {
    const images = document.querySelectorAll('.fade-in-image');
    let delay = 0;

    images.forEach((image) => {
        setTimeout(() => {
            image.style.opacity = '1';
        }, delay);

        // Increase the delay for the next image
        delay += 1000; // Adjust this delay (in milliseconds) as needed
    });
}

    // Function to handle the "Home" click (hiding features and contact form)
    function onHomeClick(event) {
        event.preventDefault();
        if (featuresPage) {
            featuresPage.classList.remove('open');
            featuresPage.style.display = 'none';
        }
        if (contactForm) {
            contactForm.classList.remove('open');
        }
    }

    // Event listeners
    if (contactLink) contactLink.addEventListener('click', showContactForm);
    if (closeFormButton) closeFormButton.addEventListener('click', hideContactForm);
    if (featuresLink) featuresLink.addEventListener('click', showFeaturesPage);
    if (homeLink) homeLink.addEventListener('click', onHomeClick);
});
