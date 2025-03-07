(function ($) {

    "use strict";

    $(window).on('load', function () {
        $('#js-preloader').addClass('loaded');
    });

    $(window).scroll(function () {
        var scroll = $(window).scrollTop();
        var box = $('.header-text').height();
        var header = $('header').height();

        if (scroll >= box - header) {
            $("header").addClass("background-header");
        } else {
            $("header").removeClass("background-header");
        }
    });

    var width = $(window).width();
    $(window).resize(function () {
        if (width > 767 && $(window).width() < 767) {
            location.reload();
        } else if (width < 767 && $(window).width() > 767) {
            location.reload();
        }
    });

    // Initialize Isotope on page load
    var $grid = $('.trending-box').isotope({
        itemSelector: '.trending-items',
        layoutMode: 'masonry'
    });

    const filtersElem = document.querySelector('.trending-filter');
    if (filtersElem) {
        filtersElem.addEventListener('click', function (event) {
            event.preventDefault();
            // Only handle clicks on <a> elements
            if (!event.target.matches('a')) {
                return;
            }

            // Get the data-filter value (e.g., ".Adventure" or "*")
            const filterValue = event.target.getAttribute('data-filter');
            // Remove the dot if present, except for the "show all" case
            let category = filterValue === "*" ? "all" : filterValue.replace('.', '');

            // AJAX request to fetch filtered games
            $.ajax({
                url: "/filter_games/",  // Adjust URL if necessary
                type: "GET",
                data: { category: category },
                success: function (response) {
                    // Update the games container with the new HTML
                    const $container = $('#games-container');
                    $container.html(response.html);

                    // Reinitialize Isotope on the new items
                    $grid.isotope('reloadItems').isotope({ sortBy: 'original-order' });
                },
                error: function (xhr, status, error) {
                    console.error("Error fetching games:", error);
                }
            });

            // Update the active state for filtering links
            const currentActive = filtersElem.querySelector('.is_active');
            if (currentActive) {
                currentActive.classList.remove('is_active');
            }
            event.target.classList.add('is_active');
        });
    }



    // Menu Dropdown Toggle
    if ($('.menu-trigger').length) {
        $(".menu-trigger").on('click', function () {
            $(this).toggleClass('active');
            $('.header-area .nav').slideToggle(200);
        });
    }


    // Menu elevator animation
    $('.scroll-to-section a[href*=\\#]:not([href=\\#])').on('click', function () {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            if (target.length) {
                var width = $(window).width();
                if (width < 991) {
                    $('.menu-trigger').removeClass('active');
                    $('.header-area .nav').slideUp(200);
                }
                $('html,body').animate({
                    scrollTop: (target.offset().top) - 80
                }, 700);
                return false;
            }
        }
    });


    // Page loading animation
    $(window).on('load', function () {
        if ($('.cover').length) {
            $('.cover').parallax({
                imageSrc: $('.cover').data('image'),
                zIndex: '1'
            });
        }

        $("#preloader").animate({
            'opacity': '0'
        }, 600, function () {
            setTimeout(function () {
                $("#preloader").css("visibility", "hidden").fadeOut();
            }, 300);
        });
    });


})(window.jQuery);