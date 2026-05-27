(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();
    
    
    // Mobile Menu Management - Bootstrap Collapse Integration with Accessibility
    document.addEventListener('DOMContentLoaded', function() {
        var navbarToggler = document.querySelector('.navbar-toggler');
        var navbarCollapse = document.querySelector('#navbarCollapse');
        
        if (navbarToggler && navbarCollapse) {
            // Allow Bootstrap and responsive CSS to control toggler visibility
            // on large screens, and only show it when the navbar is collapsed.
            
            // Update aria-expanded attribute when collapse state changes
            var updateAriaExpanded = function() {
                var isShown = navbarCollapse.classList.contains('show');
                navbarToggler.setAttribute('aria-expanded', isShown ? 'true' : 'false');
            };
            
            // Listen for collapse events
            navbarCollapse.addEventListener('show.bs.collapse', updateAriaExpanded);
            navbarCollapse.addEventListener('hide.bs.collapse', updateAriaExpanded);
            navbarCollapse.addEventListener('shown.bs.collapse', updateAriaExpanded);
            navbarCollapse.addEventListener('hidden.bs.collapse', updateAriaExpanded);
            
            // Set initial state
            updateAriaExpanded();
            
            // Close mobile menu when a non-dropdown navigation link is clicked
            var directNavLinks = navbarCollapse.querySelectorAll('a.nav-link:not(.dropdown-toggle)');
            directNavLinks.forEach(function(link) {
                link.addEventListener('click', function() {
                    // Only close if on mobile and menu is currently shown
                    if (window.innerWidth <= 991 && navbarCollapse.classList.contains('show')) {
                        navbarToggler.click(); // Trigger the toggle button
                    }
                });
            });
            
            // Close mobile menu when a dropdown item is clicked
            var dropdownItems = navbarCollapse.querySelectorAll('.dropdown-item');
            dropdownItems.forEach(function(item) {
                item.addEventListener('click', function() {
                    if (window.innerWidth <= 991 && navbarCollapse.classList.contains('show')) {
                        navbarToggler.click(); // Trigger the toggle button
                    }
                });
            });
            
            // Keyboard accessibility: Escape key to close menu
            document.addEventListener('keydown', function(event) {
                if (event.key === 'Escape' && window.innerWidth <= 991 && navbarCollapse.classList.contains('show')) {
                    navbarToggler.click();
                    navbarToggler.focus(); // Return focus to toggle button
                }
            });
        }
    });
    
    // Hero Text Typewriter Cycling Animation
    var heroTexts = [
        "Nothing is Impossible",
        "Quality Education for Higher Learning",
        "Science • Conscience • Discipline",
        "SECONDARY PROGRAMS - O LEVEL AND A LEVEL",
        "Excellence in Academic Rigor",
        "Building Tomorrow's Leaders",
        "Sport is a priority and we are winners"
    ];
    
    var currentHeroIndex = 0;
    var heroElement = document.getElementById('heroText');
    
    function resetAnimation(element) {
        // Remove all animation classes
        element.classList.remove('animate-in', 'animate-out');
        // Force a reflow to reset animation state
        void element.offsetWidth;
    }
    
    function cycleHeroText() {
        if (!heroElement) return;
        
        // Fade out current text
        resetAnimation(heroElement);
        heroElement.classList.add('animate-out');
        
        setTimeout(function() {
            // Move to next text
            currentHeroIndex = (currentHeroIndex + 1) % heroTexts.length;
            heroElement.textContent = heroTexts[currentHeroIndex];
            
            // Reset and apply typewriter animation
            resetAnimation(heroElement);
            heroElement.classList.add('animate-in');
            
            // Schedule next cycle (4s animation + 3s reading time + 0.5s fade out)
            setTimeout(cycleHeroText, 7500);
        }, 500);
    }
    
    // Start the animation after a small delay
    if (heroElement) {
        heroElement.classList.add('animate-in');
        setTimeout(cycleHeroText, 7500);
    }
    
    
    // Initiate the wowjs
    new WOW().init();


    // Sticky Navbar
    // Only auto-hide/show on larger screens; keep visible on small screens for easy access
    $(window).scroll(function () {
        var isLargeScreen = window.matchMedia('(min-width: 992px)').matches;

        // On small screens keep the navbar visible (easier access).
        if (!isLargeScreen) {
            if ($(this).scrollTop() >= 0) {
                $('.sticky-top').addClass('shadow-sm').css('top', '0px');
            }
            return;
        }

        // On large screens allow the auto-hide behaviour when scrolled to top
        if ($(this).scrollTop() > 300) {
            $('.sticky-top').addClass('shadow-sm').css('top', '0px');
        } else {
            $('.sticky-top').removeClass('shadow-sm').css('top', '-100px');
        }
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Facts counter (guard plugin availability per page)
    if ($.fn.counterUp) {
        $('[data-toggle="counter-up"]').counterUp({
            delay: 10,
            time: 2000
        });
    }


    // Header carousel + optional hero text nudge (copy stays visible in CSS without JS)
    var $headerCarousel = $(".header-carousel");
    function nlcaHeroTextAnimate() {
        $headerCarousel.find(".nlca-hero-text-block").removeClass("nlca-hero-animate-in");
        var $block = $headerCarousel.find(".owl-item.active .nlca-hero-text-block");
        if (!$block.length) {
            $block = $headerCarousel.find(".owl-item").first().find(".nlca-hero-text-block");
        }
        requestAnimationFrame(function () {
            requestAnimationFrame(function () {
                $block.addClass("nlca-hero-animate-in");
            });
        });
    }
    if ($headerCarousel.length && $.fn.owlCarousel) {
        $headerCarousel.owlCarousel({
            autoplay: true,
            autoplayTimeout: 7000,
            /* Crossfade via Animate.css — avoids the default left/right slide */
            smartSpeed: 1100,
            animateOut: "fadeOut",
            animateIn: "fadeIn",
            items: 1,
            dots: true,
            loop: true,
            margin: 0,
            nav: true,
            navText: [
                '<i class="bi bi-chevron-left"></i>',
                '<i class="bi bi-chevron-right"></i>',
            ],
        });
        $headerCarousel.on("initialized.owl.carousel", function () {
            setTimeout(nlcaHeroTextAnimate, 30);
        });
        $headerCarousel.on("changed.owl.carousel translated.owl.carousel", nlcaHeroTextAnimate);
    }


    // Testimonials carousel
    if ($.fn.owlCarousel) {
        $(".testimonial-carousel").owlCarousel({
            autoplay: true,
            smartSpeed: 1000,
            center: true,
            dots: false,
            loop: true,
            nav : true,
            navText : [
                '<i class="bi bi-arrow-left"></i>',
                '<i class="bi bi-arrow-right"></i>'
            ],
            responsive: {
                0:{
                    items:1
                },
                768:{
                    items:2
                }
            }
        });
    }


    // Portfolio isotope and filter
    if ($.fn.isotope) {
        var portfolioIsotope = $('.portfolio-container').isotope({
            itemSelector: '.portfolio-item',
            layoutMode: 'fitRows'
        });
        $('#portfolio-flters li').on('click', function () {
            $("#portfolio-flters li").removeClass('active');
            $(this).addClass('active');

            portfolioIsotope.isotope({filter: $(this).data('filter')});
        });
    }
    
})(jQuery);

/**
 * Navbar behavior for responsive layouts:
 * - Mobile/tablet: dropdowns open on tap without navigating
 * - Mobile/tablet: close menu after selecting a destination
 * - Desktop: keep Bootstrap default behavior
 */
(function () {
    var hasBootstrapCollapse =
        typeof bootstrap !== "undefined" &&
        bootstrap.Collapse &&
        typeof bootstrap.Collapse.getOrCreateInstance === "function";
    var hasBootstrapDropdown =
        typeof bootstrap !== "undefined" &&
        bootstrap.Dropdown &&
        typeof bootstrap.Dropdown.getOrCreateInstance === "function";

    function isMobileNav() {
        return window.matchMedia("(max-width: 991.98px)").matches;
    }

    function getNavCollapse(nav) {
        if (!nav) {
            return null;
        }
        return nav.querySelector(".navbar-collapse");
    }

    function setCollapseState(nav, isOpen) {
        var collapseEl = getNavCollapse(nav);
        if (!collapseEl) {
            return;
        }
        collapseEl.classList.toggle("show", isOpen);
        collapseEl.style.display = isOpen ? "block" : "";
        collapseEl.setAttribute("aria-hidden", isOpen ? "false" : "true");
        var toggler = nav ? nav.querySelector(".navbar-toggler") : null;
        if (toggler) {
            toggler.setAttribute("aria-expanded", isOpen ? "true" : "false");
        }
    }

    function closeNavbarCollapse(nav) {
        var collapseEl = getNavCollapse(nav);
        if (!collapseEl || !collapseEl.classList.contains("show")) {
            return;
        }
        if (hasBootstrapCollapse) {
            bootstrap.Collapse.getOrCreateInstance(collapseEl).hide();
        }
        setCollapseState(nav, false);
    }

    function toggleNavbarCollapse(toggler) {
        var nav = toggler.closest(".navbar");
        if (!nav) {
            return;
        }
        var target = toggler.getAttribute("data-bs-target");
        var collapseEl = target ? document.querySelector(target) : getNavCollapse(nav);
        if (!collapseEl) {
            return;
        }
        var willOpen = !collapseEl.classList.contains("show");
        if (hasBootstrapCollapse) {
            bootstrap.Collapse.getOrCreateInstance(collapseEl).toggle();
        }
        // Hard fallback: enforce visible state even if Bootstrap handlers fail.
        setCollapseState(nav, willOpen);
    }

    function closeOtherDropdowns(nav, exceptToggle) {
        nav.querySelectorAll(".dropdown-toggle").forEach(function (otherToggle) {
            if (otherToggle === exceptToggle) {
                return;
            }
            var otherParent = otherToggle.closest(".dropdown");
            var otherMenu = otherParent ? otherParent.querySelector(".dropdown-menu") : null;
            if (!otherParent || !otherMenu) {
                return;
            }
            if (hasBootstrapDropdown) {
                bootstrap.Dropdown.getOrCreateInstance(otherToggle).hide();
            }
            otherParent.classList.remove("show");
            otherMenu.classList.remove("show");
        });
    }

    document.addEventListener("click", function (e) {
        var toggler = e.target.closest(".navbar .navbar-toggler");
        if (toggler && isMobileNav()) {
            e.preventDefault();
            toggleNavbarCollapse(toggler);
            return;
        }

        var toggle = e.target.closest(".navbar .dropdown-toggle");
        if (toggle && isMobileNav()) {
            e.preventDefault();
            var nav = toggle.closest(".navbar");
            if (!nav) {
                return;
            }
            var parent = toggle.closest(".dropdown");
            var menu = parent ? parent.querySelector(".dropdown-menu") : null;
            if (!menu) {
                return;
            }

            var isOpen = menu.classList.contains("show");
            closeOtherDropdowns(nav, toggle);

            if (isOpen) {
                if (hasBootstrapDropdown) {
                    bootstrap.Dropdown.getOrCreateInstance(toggle).hide();
                }
                parent.classList.remove("show");
                menu.classList.remove("show");
            } else {
                if (hasBootstrapDropdown) {
                    bootstrap.Dropdown.getOrCreateInstance(toggle).show();
                }
                parent.classList.add("show");
                menu.classList.add("show");
            }
            return;
        }

        var clickedNavLink = e.target.closest(".navbar .navbar-nav a");
        if (
            clickedNavLink &&
            isMobileNav() &&
            !clickedNavLink.classList.contains("dropdown-toggle")
        ) {
            closeNavbarCollapse(clickedNavLink.closest(".navbar"));
        }
    });

    document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") {
            document.querySelectorAll(".navbar").forEach(function (nav) {
                closeNavbarCollapse(nav);
            });
        }
    });

    document.addEventListener("click", function (e) {
        if (!isMobileNav()) {
            return;
        }
        document.querySelectorAll(".navbar").forEach(function (nav) {
            var collapseEl = getNavCollapse(nav);
            if (!collapseEl || !collapseEl.classList.contains("show")) {
                return;
            }
            if (!e.target.closest(".navbar")) {
                closeNavbarCollapse(nav);
            }
        });
    });

    window.addEventListener("resize", function () {
        if (!isMobileNav()) {
            document.querySelectorAll(".navbar .dropdown-toggle").forEach(function (toggle) {
                var parent = toggle.closest(".dropdown");
                var menu = parent ? parent.querySelector(".dropdown-menu") : null;
                if (hasBootstrapDropdown) {
                    bootstrap.Dropdown.getOrCreateInstance(toggle).hide();
                }
                if (parent) {
                    parent.classList.remove("show");
                }
                if (menu) {
                    menu.classList.remove("show");
                }
            });
        }
    });

    /* Update ARIA expanded state when collapse changes */
    function bindAriaSync(nav) {
        var collapseEl = getNavCollapse(nav);
        if (!collapseEl || collapseEl.dataset.nlcaAriaBound === "1") {
            return;
        }
        collapseEl.dataset.nlcaAriaBound = "1";

        if (hasBootstrapCollapse) {
            collapseEl.addEventListener("show.bs.collapse", function () {
                setCollapseState(nav, true);
            });

            collapseEl.addEventListener("hide.bs.collapse", function () {
                setCollapseState(nav, false);
            });
        }
    }

    function bindAllNavs() {
        document.querySelectorAll(".navbar").forEach(function (nav) {
            bindAriaSync(nav);
        });
    }

    document.addEventListener("DOMContentLoaded", bindAllNavs);
    document.addEventListener("livewire:navigated", bindAllNavs);
    bindAllNavs();
})();

/**
 * Vision / mission band: scroll-linked parallax on background (full-bleed section).
 * Desktop: stronger motion. Mobile: gentler motion so the image stays pleasant and readable.
 */
(function () {
    var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reducedMotion) {
        return;
    }

    var mqDesktop = window.matchMedia('(min-width: 992px)');
    var ticking = false;

    function parallaxFactor() {
        return mqDesktop.matches ? 0.16 : 0.085;
    }

    function updateParallaxBg() {
        ticking = false;
        var factor = parallaxFactor();
        document.querySelectorAll('[data-parallax-bg]').forEach(function (el) {
            var band = el.closest('.nlca-vision-band') || el.closest('.nlca-core-values-band');
            if (!band) {
                return;
            }
            var rect = band.getBoundingClientRect();
            var y = rect.top * factor;
            el.style.setProperty('--nlca-parallax-y', y + 'px');
        });
    }

    function onScrollOrResize() {
        if (!ticking) {
            ticking = true;
            requestAnimationFrame(updateParallaxBg);
        }
    }

    window.addEventListener('scroll', onScrollOrResize, { passive: true });
    window.addEventListener('resize', onScrollOrResize);
    if (mqDesktop.addEventListener) {
        mqDesktop.addEventListener('change', onScrollOrResize);
    } else if (mqDesktop.addListener) {
        mqDesktop.addListener(onScrollOrResize);
    }
    document.addEventListener('livewire:navigated', onScrollOrResize);
    updateParallaxBg();
})();

/** Program / facility detail: thumbnail row (delegated, works with Livewire navigate) */
(function () {
    document.addEventListener("click", function (e) {
        var btn = e.target.closest(".nlca-detail-thumb[data-nlca-detail-src]");
        if (!btn) {
            return;
        }
        var hero = document.getElementById("nlca-detail-hero");
        if (!hero) {
            return;
        }
        e.preventDefault();
        var src = btn.getAttribute("data-nlca-detail-src");
        if (src) {
            hero.setAttribute("src", src);
        }
        document.querySelectorAll(".nlca-detail-thumb").forEach(function (b) {
            b.classList.remove("is-active");
        });
        btn.classList.add("is-active");
    });
})();

/** Share strip (activity detail): copy link + Web Share API */
(function () {
    function copyText(text) {
        if (navigator.clipboard && navigator.clipboard.writeText) {
            return navigator.clipboard.writeText(text);
        }
        var ta = document.createElement("textarea");
        ta.value = text;
        ta.setAttribute("readonly", "");
        ta.style.position = "fixed";
        ta.style.left = "-9999px";
        document.body.appendChild(ta);
        ta.select();
        try {
            document.execCommand("copy");
        } catch (err) {}
        document.body.removeChild(ta);
        return Promise.resolve();
    }

    function showFeedback(wrap, msg) {
        var el = wrap.querySelector(".nlca-share-feedback");
        if (!el) {
            return;
        }
        el.textContent = msg;
        el.classList.remove("d-none");
        window.clearTimeout(wrap._nlcaShareT);
        wrap._nlcaShareT = window.setTimeout(function () {
            el.classList.add("d-none");
        }, 2800);
    }

    document.addEventListener("click", function (e) {
        var copyBtn = e.target.closest(".nlca-share-copy");
        if (copyBtn) {
            var wrap = copyBtn.closest("[data-nlca-share]");
            if (!wrap) {
                return;
            }
            e.preventDefault();
            var url = wrap.getAttribute("data-share-url") || "";
            copyText(url).then(
                function () {
                    showFeedback(wrap, "Link copied!");
                },
                function () {
                    showFeedback(wrap, "Could not copy — select the address bar.");
                }
            );
            return;
        }
        var nativeBtn = e.target.closest(".nlca-share-native");
        if (nativeBtn && navigator.share) {
            var wrapN = nativeBtn.closest("[data-nlca-share]");
            if (!wrapN) {
                return;
            }
            e.preventDefault();
            var u = wrapN.getAttribute("data-share-url") || "";
            var t = wrapN.getAttribute("data-share-title") || "";
            navigator.share({ title: t, url: u }).catch(function () {});
        }
    });

    function toggleNativeShare() {
        document.querySelectorAll(".nlca-share-native").forEach(function (btn) {
            if (navigator.share) {
                btn.classList.remove("d-none");
            } else {
                btn.classList.add("d-none");
            }
        });
    }
    document.addEventListener("DOMContentLoaded", toggleNativeShare);
    document.addEventListener("livewire:navigated", toggleNativeShare);
})();

