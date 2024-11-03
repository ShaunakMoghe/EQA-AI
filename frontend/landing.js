// Wait for the DOM to fully load

document.addEventListener('DOMContentLoaded', function () {
    // Smooth scroll for navigation links
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            document.querySelector(targetId).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Custom cursor effect
    const customCursor = document.createElement('div');
    customCursor.classList.add('custom-cursor');
    document.body.appendChild(customCursor);

    let cursorX = 0, cursorY = 0;
    let delayX = 0, delayY = 0;

    document.addEventListener('mousemove', function (e) {
        cursorX = e.clientX;
        cursorY = e.clientY;
    });

    function animateCursor() {
        delayX += (cursorX - delayX) * 0.05;
        delayY += (cursorY - delayY) * 0.05;
        customCursor.style.left = delayX + 'px';
        customCursor.style.top = delayY + 'px';
        requestAnimationFrame(animateCursor);
    }

    animateCursor();

    document.querySelectorAll('a, button').forEach(element => {
        element.addEventListener('mouseenter', () => {
            customCursor.classList.add('custom-cursor-hover');
        });
        element.addEventListener('mouseleave', () => {
            customCursor.classList.remove('custom-cursor-hover');
        });
    });

    // Intersection Observer for scroll animations
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.5
    });

    document.querySelectorAll('.service-item, .hero-title, .hero-subtitle').forEach(element => {
        observer.observe(element);
    });

    // Animated gradient background blobs
    const blobCount = 5;
    const blobContainer = document.createElement('div');
    blobContainer.classList.add('blob-container');
    document.querySelector('.hero-section').appendChild(blobContainer);

    for (let i = 0; i < blobCount; i++) {
        const blob = document.createElement('div');
        blob.classList.add('blob');
        blob.style.animationDelay = `${Math.random() * 5}s`;
        blobContainer.appendChild(blob);
    }

    // Custom cursor hover effect for links and buttons
    document.querySelectorAll('a, button').forEach(element => {
        element.addEventListener('mouseenter', () => {
            customCursor.style.transform = 'scale(1.75)';
            customCursor.style.background = 'radial-gradient(circle, #87CEEB, #00bfff)';
        });
        element.addEventListener('mouseleave', () => {
            customCursor.style.transform = 'scale(1)';
            customCursor.style.background = 'radial-gradient(circle, rgb(135, 206, 235), #0088cc)';
        });
    });
});

// Helper function to generate random values
function randomValue(min, max) {
    return Math.random() * (max - min) + min;
}
