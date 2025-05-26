/**
 * BrainVenture JavaScript Utilities
 * These functions enhance the user experience with client-side interactivity.
 */

/**
 * Initialize the BrainVenture application
 */
function initializeBrainVenture() {
    console.log('BrainVenture application initialized');
    
    // Set up event listeners
    setupEventListeners();
    
    // Initialize various components
    setupAnimations();
    enhanceAccessibility();
}

/**
 * Set up event listeners for interactive elements
 */
function setupEventListeners() {
    // Listen for clicks on cards to add subtle animation
    document.querySelectorAll('.bv-card').forEach(card => {
        card.addEventListener('click', function() {
            this.style.transform = 'scale(0.98)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 200);
        });
    });
    
    // Track time spent on the page for analytics
    let startTime = new Date();
    window.addEventListener('beforeunload', function() {
        const timeSpent = Math.round((new Date() - startTime) / 1000);
        
        // In a real app, this would send the data to the server
        console.log(`Time spent on page: ${timeSpent} seconds`);
    });
}

/**
 * Set up subtle animations for UI elements
 */
function setupAnimations() {
    // Add fade-in animation to main content
    const mainContent = document.querySelector('.main');
    if (mainContent) {
        mainContent.style.opacity = '0';
        mainContent.style.transition = 'opacity 0.5s ease-in-out';
        
        setTimeout(() => {
            mainContent.style.opacity = '1';
        }, 100);
    }
}

/**
 * Enhance accessibility features
 */
function enhanceAccessibility() {
    // Add focus outlines for keyboard navigation
    document.querySelectorAll('button, a, input, select, textarea').forEach(el => {
        el.addEventListener('focus', function() {
            this.style.outline = '2px solid var(--primary-color)';
        });
        
        el.addEventListener('blur', function() {
            this.style.outline = 'none';
        });
    });
}

/**
 * Calculate reading time for text content
 * @param {string} text - The content to calculate reading time for
 * @return {number} - Reading time in minutes
 */
function calculateReadingTime(text) {
    const wordsPerMinute = 200;
    const words = text.split(/\s+/).length;
    return Math.ceil(words / wordsPerMinute);
}

/**
 * Format datetime in a user-friendly way
 * @param {string} dateString - ISO date string
 * @return {string} - Formatted date
 */
function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

// Initialize the application when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', initializeBrainVenture);
