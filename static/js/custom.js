/*!
 *	Template Functions
*/

(function($){

	"use strict";

	/* ---------------------------------------------- /*
	 * Preloader
	/* ---------------------------------------------- */

	$(window).load(function() {
		$('.page-loader').delay(350).fadeOut('slow');
	});

	$(document).ready(function() {

		var header     = $('.header'),
			moduleHero = $('.module-hero'),
			mobileTest;

		/* ---------------------------------------------- /*
		 * Mobile detect
		/* ---------------------------------------------- */

		if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
			mobileTest = true;
		} else {
			mobileTest = false;
		}

		/* ---------------------------------------------- /*
		 * Transparent navbar animation
		/* ---------------------------------------------- */

		function navbarAnimation() {
			if ( $(window).scrollTop() > 10 ) {
				header.addClass('header-small');
				$('.header-fixed').removeClass('header-transparent');
			} else {
				header.removeClass('header-small');
				$('.header-fixed').addClass('header-transparent');
			}
		}

		navbarAnimation();

		$(window).scroll(function() {
			navbarAnimation();
		});

		$('.js-stick').stick_in_parent();

		$('.nav-icon-toggle').on('click', function() {
			$(this).toggleClass('open');
		});

		/* ---------------------------------------------- /*
		 * One Page Nav
		/* ---------------------------------------------- */

		$('.onepage-nav').singlePageNav({
			currentClass: 'active'
		});

		/* ---------------------------------------------- /*
		 * Collapse navbar on click
		/* ---------------------------------------------- */

		$(document).on('click', '.main-nav.in', function(e) {
			if ( $(e.target).is('a') && !$(e.target).parent().hasClass('has-submenu') ) {
				$(this).collapse('hide');
				$('.nav-icon-toggle').toggleClass('open');
			}
		});

		/* ---------------------------------------------- /*
		 * FlexSlider
		/* ---------------------------------------------- */

		$('.flexslider').flexslider({
			animation: "fade",
			prevText: '<i class="icon-arrow-left icons"></i>',
			nextText: '<i class="icon-arrow-right icons"></i>',
			before: function(slider) {
				$('.hero-caption').fadeOut().animate({top:'-80px'},{queue:false, easing: 'swing', duration: 700});
				slider.slides.eq(slider.currentSlide).delay(500);
				slider.slides.eq(slider.animatingTo).delay(500);
			},
			after: function(slider) {
				$('.hero-caption').fadeIn().animate({top:'0'},{queue:false, easing: 'swing', duration: 700});
			},
			useCSS: true
		});

		/* ---------------------------------------------- /*
		 * Setting background of modules
		/* ---------------------------------------------- */

		var modules = $('.module-hero, .module, .module-sm, .module-xs, .background-side, .footer');

		modules.each(function() {
			if ($(this).attr('data-background')) {
				$(this).css('background-image', 'url(' + $(this).attr('data-background') + ')');
			}
		});

		/* ---------------------------------------------- /*
		 * Open & Close shop cart
		/* ---------------------------------------------- */

		$('#open-cart, #cart-toggle').on('click', function() {
			$('body').toggleClass('off-canvas-cart-open');
			return false;
		});

		$(document).on('click', function(e) {
			var container = $('.off-canvas-cart');
			if (!container.is(e.target) && container.has(e.target).length === 0) {
				$('body').removeClass('off-canvas-cart-open');
			}
		});

		function getScrollBarWidth() {
			var inner = document.createElement('p');
			inner.style.width = "100%";
			inner.style.height = "200px";

			var outer = document.createElement('div');
			outer.style.position = "absolute";
			outer.style.top = "0px";
			outer.style.left = "0px";
			outer.style.visibility = "hidden";
			outer.style.width = "200px";
			outer.style.height = "150px";
			outer.style.overflow = "hidden";
			outer.appendChild (inner);

			document.body.appendChild (outer);
			var w1 = inner.offsetWidth;
			outer.style.overflow = 'scroll';
			var w2 = inner.offsetWidth;
			if (w1 == w2) w2 = outer.clientWidth;

			document.body.removeChild (outer);

			return (w1 - w2);
		};

		$('.off-canvas-cart-wrapper').css('margin-right', '-' + getScrollBarWidth() + 'px');

		/* ---------------------------------------------- /*
		 * Open & Close header search
		/* ---------------------------------------------- */

		$('#modal-search, .form-close-btn').on('click', function() {
			$('.header-search-form').toggleClass('opened');
			return false;
		});

		/* ---------------------------------------------- /*
		 * Parallax
		/* ---------------------------------------------- */

		$('.parallax').jarallax({
			speed: 0.7
		});

		/* ---------------------------------------------- /*
		 * Twitter
		/* ---------------------------------------------- */

		$('.twitter-feed').each(function (index) {
			$(this).attr('id', 'twitter-' + index);

			var twitterID      = $(this).data('twitter');
			var twitter_config = {
				'id':             twitterID,
				'domId':          'twitter-' + index,
				'maxTweets':      2,
				'enableLinks':    true,
				'showPermalinks': false
			};
			twitterFetcher.fetch(twitter_config);
		});

		/* ---------------------------------------------- /*
		 * Shop Product Zoom
		/* ---------------------------------------------- */

		$('.product-slider .item').zoom();

		/* ---------------------------------------------- /*
		 * Shop product carousel
		/* ---------------------------------------------- */

		var owl;
		owl = $('.product-slider');

		owl.owlCarousel({
			navigation: false,
			slideSpeed: 300,
			paginationSpeed: 400,
			singleItem: true,
			afterInit: afterOWLinit,
			afterUpdate: afterOWLinit,
			touchDrag: false,
			mouseDrag: false
		});

		function afterOWLinit() {
			$('.owl-controls .owl-page').append('<a class="item-link" href="#"/>');

			var pafinatorsLink = $('.owl-controls .item-link');

			$.each(this.owl.userItems, function (i) {
				$(pafinatorsLink[i]).css({
					'background': 'url(' + $(this).find('img').attr('src') + ') center center no-repeat',
					'-webkit-background-size': 'cover',
					'-moz-background-size': 'cover',
					'-o-background-size': 'cover',
					'background-size': 'cover'
				}).click(function () {
					owl.trigger('owl.goTo', i);
					return false;
				});
			});

		}

		/* ---------------------------------------------- /*
		 * Carousels & Sliders
		/* ---------------------------------------------- */

		$('.images-carousel').each(function () {
			$(this).owlCarousel($.extend({
				stopOnHover: true,
				navigation: false,
				pagination: true,
				autoPlay: 3000,
				items: 5,
				navigationText: [
					'<i class="fa fa-angle-left"></i>',
					'<i class="fa fa-angle-right"></i>'
				],
			}, $(this).data('carousel-options')));
		});

		$('.box-carousel').each(function () {
			$(this).owlCarousel($.extend({
				stopOnHover: true,
				navigation: false,
				pagination: true,
				autoPlay: 3000,
				items: 3,
				navigationText: [
					'<i class="fa fa-angle-left"></i>',
					'<i class="fa fa-angle-right"></i>'
				],
			}, $(this).data('carousel-options')));
		});

		$('.clients-carousel').each(function () {
			$(this).owlCarousel($.extend({
				navigation: false,
				pagination: false,
				autoPlay: 3000,
				items: 6,
				navigationText: [
					'<i class="fa fa-angle-left"></i>',
					'<i class="fa fa-angle-right"></i>'
				],
			}, $(this).data('carousel-options')));
		});

		$('.image-slider').each(function () {
			$(this).owlCarousel($.extend({
				stopOnHover: true,
				navigation: true,
				pagination: true,
				autoPlay: 3000,
				singleItem: true,
				items: 1,
				navigationText: [
					'<i class="fa fa-angle-left"></i>',
					'<i class="fa fa-angle-right"></i>'
				],

			}, $(this).data('carousel-options')));
		});

		$('.slider-testimonial').owlCarousel({
			paginationSpeed:  400,
			slideSpeed:       300,
			navigation:       true,
			pagination:       true,
			singleItem:       true,
			transitionStyle : 'backSlide',
			navigationText: [
				'<i class="icon-arrow-left icons"></i>',
				'<i class="icon-arrow-right icons"></i>'
			],
		});

		/* ---------------------------------------------- /*
		 * Portfolio
		/* ---------------------------------------------- */

		var filters        = $('#filters'),
			worksgrid      = $('#works-grid'),
			worksgrid_mode = 'masonry';

		if (worksgrid.hasClass('works-grid-masonry')) {
			worksgrid_mode = 'masonry';
		} else {
			worksgrid_mode = 'fitRows';
		}

		$('a', filters).on('click', function() {
			var selector = $(this).attr('data-filter');
			$('.current', filters).removeClass('current');
			$(this).addClass('current');
			worksgrid.isotope({
				filter: selector
			});
			return false;
		}).scroll();

		$(window).on('resize', function() {
			worksgrid.imagesLoaded(function() {
				worksgrid.isotope({
					layoutMode: worksgrid_mode,
					itemSelector: '.work-item',
				});
			});
		}).resize();

		/* ---------------------------------------------- /*
		 * Blog masonry
		/* ---------------------------------------------- */

		$(window).on('resize', function() {
			setTimeout( function() {
				$('.post-masonry').masonry();
			}, 1000);
		}).resize();

		/* ---------------------------------------------- /*
		 * Progress bars, counters animations
		/* ---------------------------------------------- */

		$('.progress-bar').each(function() {
			$(this).appear(function() {
				var percent = $(this).attr('aria-valuenow');
				$(this).animate({'width' : percent + '%'});
				$(this).parent('.progress').prev('.progress-title').find('span span').countTo({
					from: 0,
					to: percent,
					speed: 900,
					refreshInterval: 30
				});
			});
		});

		$('.counter-timer').each(function() {
			$(this).appear(function() {
				var number = $(this).attr('data-to');
				$(this).countTo({
					from: 0,
					to: number,
					speed: 1500,
					refreshInterval: 10,
					formatter: function (number, options) {
						number = number.toFixed(options.decimals);
						number = number.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
						return number;
					}
				});

			});
		});

		/* ---------------------------------------------- /*
		 * Lightbox, Gallery
		/* ---------------------------------------------- */

		$('.lightbox').magnificPopup({
			type: 'image'
		});

		$('.gallery').each(function() {
			$(this).magnificPopup({
				delegate: 'a',
				type: 'image',
				gallery: {
					enabled:true,
					navigateByImgClick: true,
					preload: [0,1]
				},
				image: {
					titleSrc: 'title',
					tError: 'The image could not be loaded.',
				},
				zoom: {
					enabled: true,
					duration: 300
				}
			});
		});

		$(window).on('resize', function() {
			$('.gallery').imagesLoaded(function() {
				$('.gallery').isotope({
					layoutMode: 'fitRows',
					itemSelector: '.gallery-item',
				});
			});
		}).resize();

		$('.video-pop-up').magnificPopup({
			type: 'iframe',
		});

		/* ---------------------------------------------- /*
		 * A jQuery plugin for fluid width video embeds
		/* ---------------------------------------------- */

		$('body').fitVids();

		/* ---------------------------------------------- /*
		 * WOW Animation
		/* ---------------------------------------------- */

		var wow = new WOW({
			mobile: false
		});
		wow.init();

		/* ---------------------------------------------- /*
		 * Google Map
		/* ---------------------------------------------- */

		var reg_exp = /\[[^(\]\[)]*\]/g;

		var map_div      = $('#map');
		var is_draggable = Math.max($(window).width(), window.innerWidth) > 736 ? true : false;

		if (map_div.length > 0) {

			var markers_addresses = map_div[0].getAttribute('data-addresses').match(reg_exp),
				markers_info      = map_div.data('info').match(reg_exp),
				markers_icon      = map_div.data('icon'),
				map_zoom          = map_div.data('zoom');

			var	markers_values = [], map_center;

			markers_addresses.forEach( function(marker_address, index) {
				var marker_value = '{'
				marker_value    += '"latLng":' + marker_address;
				if (index == 0) {
					map_center = JSON.parse(marker_address);
				};
				if (markers_info != null) {
					if (markers_info[index]) {
						var marker_data = markers_info[index].replace(/\[|\]/g, '');
						marker_value   += ', "data":"' + marker_data + '"';
					}
				};
				marker_value += '}';
				markers_values.push(JSON.parse(marker_value));
			});

			var map_options = {
				scrollwheel: false,
				styles: [{"featureType":"water","elementType":"geometry","stylers":[{"color":"#e9e9e9"},{"lightness":17}]},{"featureType":"landscape","elementType":"geometry","stylers":[{"color":"#f5f5f5"},{"lightness":20}]},{"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"color":"#ffffff"},{"lightness":17}]},{"featureType":"road.highway","elementType":"geometry.stroke","stylers":[{"color":"#ffffff"},{"lightness":29},{"weight":0.2}]},{"featureType":"road.arterial","elementType":"geometry","stylers":[{"color":"#ffffff"},{"lightness":18}]},{"featureType":"road.local","elementType":"geometry","stylers":[{"color":"#ffffff"},{"lightness":16}]},{"featureType":"poi","elementType":"geometry","stylers":[{"color":"#f5f5f5"},{"lightness":21}]},{"featureType":"poi.park","elementType":"geometry","stylers":[{"color":"#dedede"},{"lightness":21}]},{"elementType":"labels.text.stroke","stylers":[{"visibility":"on"},{"color":"#ffffff"},{"lightness":16}]},{"elementType":"labels.text.fill","stylers":[{"saturation":36},{"color":"#333333"},{"lightness":40}]},{"elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"transit","elementType":"geometry","stylers":[{"color":"#f2f2f2"},{"lightness":19}]},{"featureType":"administrative","elementType":"geometry.fill","stylers":[{"color":"#fefefe"},{"lightness":20}]},{"featureType":"administrative","elementType":"geometry.stroke","stylers":[{"color":"#fefefe"},{"lightness":17},{"weight":1.2}]}]
			};

			map_options.center    = map_center;
			map_options.zoom      = map_zoom;
			map_options.draggable = is_draggable;

			var markers_options  = {};
			markers_options.icon = markers_icon;

			map_div.gmap3({
				map:{
					options:
						map_options
				},
				marker:{
					values: markers_values,
					options: markers_options,
					events:{
						click: function(marker, event, context) {
							if (context.data) {
								var map        = $(this).gmap3("get"),
									infowindow = $(this).gmap3({get:{name:"infowindow"}});
								if (infowindow) {
									infowindow.open(map, marker);
									infowindow.setContent(context.data);
								} else {
									$(this).gmap3({
										infowindow:{
											anchor:marker,
											options:{content: context.data}
										}
									});
								}
							}
						}
					}
				}
			});

		};

		/* ---------------------------------------------- /*
		 * Tooltips
		/* ---------------------------------------------- */

		$(function () {
			$('[data-toggle="tooltip"]').tooltip({
				trigger: 'hover'
			})
		})

		/* ---------------------------------------------- /*
		 * Scroll Animation
		/* ---------------------------------------------- */

		$('.smoothscroll').on('click', function(e) {
			var target  = this.hash;
			var $target = $(target);

			$('html, body').stop().animate({
				'scrollTop': $target.offset().top - header.height()
			}, 600, 'swing');

			e.preventDefault();
		});

		/* ---------------------------------------------- /*
		 * Scroll top
		/* ---------------------------------------------- */

		$('a[href="#top"]').on('click', function() {
			$('html, body').animate({ scrollTop: 0 }, 'slow');
			return false;
		});

		/* ---------------------------------------------- /*
		 * Disable hover on scroll
		/* ---------------------------------------------- */

		var body = document.body,
			timer;
		window.addEventListener('scroll', function() {
			clearTimeout(timer);
			if (!body.classList.contains('disable-hover')) {
				body.classList.add('disable-hover')
			}
			timer = setTimeout(function() {
				body.classList.remove('disable-hover')
			}, 100);
		}, false);

	});

})(jQuery);
