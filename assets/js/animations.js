/**
 * PREMIUM ANIMATIONS JAVASCRIPT
 * Handles scroll progress, parallax, form interactions, and micro-animations
 * Load AFTER all libraries but BEFORE main.js
 */

(function () {
    'use strict';

    // ========================================================================
    // OPTION 4: SCROLL PROGRESS BAR
    // ========================================================================
    function initScrollProgressBar() {
        var progressBar = document.createElement('div');
        progressBar.id = 'scrollProgressBar';
        document.body.appendChild(progressBar);

        window.addEventListener('scroll', function () {
            var scrollTop = window.scrollY;
            var docHeight = document.documentElement.scrollHeight - window.innerHeight;
            var scrollPercent = (scrollTop / docHeight) * 100;
            progressBar.style.width = scrollPercent + '%';
        }, { passive: true });
    }

    // ========================================================================
    // OPTION 6: PARALLAX EFFECTS
    // ========================================================================
    function initParallaxEffects() {
        var parallaxElements = document.querySelectorAll('[data-parallax-bg]');
        if (parallaxElements.length === 0) return;

        var isReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        if (isReducedMotion) return;

        function updateParallax() {
            parallaxElements.forEach(function (el) {
                var rect = el.getBoundingClientRect();
                var scrollPercentage = (window.innerHeight - rect.top) / (window.innerHeight + rect.height);
                var yOffset = (scrollPercentage - 0.5) * 30; // Gentle parallax

                if (window.innerWidth > 768) {
                    el.style.transform = 'translateY(' + yOffset + 'px)';
                } else {
                    el.style.transform = 'translateY(' + (yOffset * 0.5) + 'px)'; // Half effect on mobile
                }
            });
        }

        window.addEventListener('scroll', updateParallax, { passive: true });
        window.addEventListener('resize', updateParallax);
        updateParallax();
    }

    // ========================================================================
    // OPTION 8: FORM MICRO-INTERACTIONS
    // ========================================================================
    function initFormInteractions() {
        var inputs = document.querySelectorAll('input, textarea, select');
        
        inputs.forEach(function (input) {
            input.addEventListener('focus', function () {
                this.classList.add('animate-glow');
            });

            input.addEventListener('blur', function () {
                this.classList.remove('animate-glow');
            });

            // Add animation on valid input
            input.addEventListener('change', function () {
                if (this.value.trim() !== '') {
                    var parent = this.closest('.form-group') || this.parentElement;
                    if (parent) {
                        parent.style.animation = 'fadeIn 0.3s ease-out';
                    }
                }
            });
        });

        // Enhance contact form success
        var contactForm = document.querySelector('form[id*="contact"], form[id*="message"]');
        if (contactForm) {
            contactForm.addEventListener('submit', function (e) {
                var successMsg = this.querySelector('[class*="success"], [class*="alert-success"]');
                if (successMsg) {
                    successMsg.classList.add('form-success');
                }
            });
        }
    }

    // ========================================================================
    // OPTION 5: HEADING ANIMATIONS WITH INTERSECTION OBSERVER
    // ========================================================================
    function initHeadingAnimations() {
        var headings = document.querySelectorAll('.section-title h2, .nlca-section-title, h1');
        
        if (!('IntersectionObserver' in window)) {
            headings.forEach(function (el) {
                el.style.animation = 'slideInLeft 0.6s ease-out';
            });
            return;
        }

        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.style.animation = 'slideInLeft 0.6s ease-out forwards';
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        headings.forEach(function (heading) {
            observer.observe(heading);
        });
    }

    // ========================================================================
    // OPTION 3: CARD STAGGER ANIMATION ON SCROLL
    // ========================================================================
    function initCardStaggerAnimation() {
        var cards = document.querySelectorAll('.service-item, .portfolio-item, .faq-item');
        
        if (!('IntersectionObserver' in window)) {
            cards.forEach(function (el) {
                el.classList.add('animate-fade');
            });
            return;
        }

        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry, index) {
                if (entry.isIntersecting) {
                    setTimeout(function () {
                        entry.target.classList.add('stagger-item');
                    }, index * 50);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        cards.forEach(function (card) {
            observer.observe(card);
        });
    }

    // ========================================================================
    // OPTION 2: ENHANCED NAVBAR LINK ANIMATIONS
    // ========================================================================
    function initNavbarLinkAnimations() {
        var navLinks = document.querySelectorAll('.nav-link, .dropdown-item');
        
        navLinks.forEach(function (link) {
            // Add checkmark on hover
            link.addEventListener('mouseenter', function () {
                if (!this.querySelector('[data-animated="true"]')) {
                    var span = document.createElement('span');
                    span.textContent = '✓ ';
                    span.style.color = 'var(--nlca-secondary)';
                    span.style.fontWeight = 'bold';
                    span.style.marginRight = '6px';
                    span.setAttribute('data-animated', 'true');
                    this.insertBefore(span, this.firstChild);
                    
                    setTimeout(function () {
                        if (span.parentNode) {
                            span.remove();
                        }
                    }, 800);
                }
            });
        });
    }

    // ========================================================================
    // OPTION 8: TOOLTIP ANIMATIONS
    // ========================================================================
    function initTooltips() {
        var tooltipElements = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        tooltipElements.forEach(function (el) {
            el.addEventListener('mouseenter', function () {
                var tooltip = document.querySelector('[role="tooltip"]');
                if (tooltip) {
                    tooltip.style.animation = 'fadeInUp 0.3s ease-out';
                }
            });
        });
    }

    // ========================================================================
    // OPTION 8: SUCCESS FEEDBACK ANIMATION
    // ========================================================================
    function initSuccessFeedback() {
        var alerts = document.querySelectorAll('.alert-success');
        alerts.forEach(function (alert) {
            alert.style.animation = 'fadeInUp 0.5s ease-out, successPulse 0.6s ease-out 0.5s';
            
            var closeBtn = alert.querySelector('.btn-close');
            if (closeBtn) {
                closeBtn.addEventListener('click', function () {
                    alert.style.animation = 'fadeOut 0.3s ease-out';
                });
            }
        });
    }

    // ========================================================================
    // OPTION 7: ANIMATED COUNTER (if exists)
    // ========================================================================
    function initAnimatedCounters() {
        var counters = document.querySelectorAll('[data-toggle="counter-up"]');
        if (counters.length === 0) return;

        counters.forEach(function (counter) {
            counter.style.animation = 'slideInLeft 0.6s ease-out';
        });
    }

    // ========================================================================
    // OPTION 5: TYPEWRITER EFFECT FOR HERO TEXT (Optional)
    // ========================================================================
    function initTypewriterEffect() {
        var heroTexts = document.querySelectorAll('.nlca-hero-title, h1');
        
        heroTexts.forEach(function (el) {
            var originalText = el.textContent;
            if (originalText.length > 5) {
                // Only apply to longer text
                el.style.overflow = 'hidden';
                el.style.borderRight = '2px solid var(--nlca-secondary)';
                el.style.whiteSpace = 'nowrap';
                el.style.animation = 'typewriter 1.5s steps(40, end)';
            }
        });
    }

    // ========================================================================
    // OPTION 4: SCROLL POSITION INDICATOR
    // ========================================================================
    function initScrollIndicator() {
        var sections = document.querySelectorAll('main section, main > div');
        
        if (sections.length < 2) return;

        window.addEventListener('scroll', function () {
            var scrollPos = window.scrollY + window.innerHeight / 2;

            sections.forEach(function (section) {
                var sectionPos = section.offsetTop;
                var sectionHeight = section.offsetHeight;

                if (scrollPos >= sectionPos && scrollPos <= sectionPos + sectionHeight) {
                    section.style.opacity = '1';
                    section.style.transform = 'scale(1)';
                } else {
                    section.style.opacity = '0.95';
                    section.style.transform = 'scale(0.98)';
                }
            });
        }, { passive: true });
    }

    // ========================================================================
    // OPTION 2: BUTTON CLICK FEEDBACK
    // ========================================================================
    function initButtonClickFeedback() {
        var buttons = document.querySelectorAll('.btn, button:not(.navbar-toggler)');
        
        buttons.forEach(function (btn) {
            btn.addEventListener('click', function (e) {
                // Create ripple effect
                var ripple = document.createElement('span');
                ripple.style.position = 'absolute';
                ripple.style.borderRadius = '50%';
                ripple.style.background = 'rgba(255, 255, 255, 0.6)';
                ripple.style.width = ripple.style.height = '20px';
                ripple.style.animation = 'buttonRipple 0.6s ease-out';
                ripple.style.pointerEvents = 'none';

                this.style.position = 'relative';
                this.style.overflow = 'hidden';

                var rect = this.getBoundingClientRect();
                ripple.style.left = (e.clientX - rect.left) + 'px';
                ripple.style.top = (e.clientY - rect.top) + 'px';

                this.appendChild(ripple);

                setTimeout(function () {
                    ripple.remove();
                }, 600);
            });
        });
    }

    // Add ripple animation
    var style = document.createElement('style');
    style.textContent = `
        @keyframes buttonRipple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);

    // ========================================================================
    // INITIALIZATION
    // ========================================================================
    function init() {
        // Wait for DOM to be fully loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', function () {
                initScrollProgressBar();
                initParallaxEffects();
                initFormInteractions();
                initHeadingAnimations();
                initCardStaggerAnimation();
                initNavbarLinkAnimations();
                initTooltips();
                initSuccessFeedback();
                initAnimatedCounters();
                initTypewriterEffect();
                initScrollIndicator();
                initButtonClickFeedback();
            });
        } else {
            initScrollProgressBar();
            initParallaxEffects();
            initFormInteractions();
            initHeadingAnimations();
            initCardStaggerAnimation();
            initNavbarLinkAnimations();
            initTooltips();
            initSuccessFeedback();
            initAnimatedCounters();
            initTypewriterEffect();
            initScrollIndicator();
            initButtonClickFeedback();
        }
    }

    // Initialize when document is ready
    init();

})();
