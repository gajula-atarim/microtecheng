/**
 * Microtec Engineering — homepage motion.
 *
 * Every card and slide is a normal Elementor element; this file only adds the
 * behaviour from the design handoff, keyed on CSS classes set in Elementor:
 *   .mt-cat-section   category grid, 4 visible, prev/next by 2, dots
 *   .mt-svc-section   services slider, 2 per view (1 < 760px), 5s autoplay, pause on hover
 *   .mt-why-grid      4 cards, auto-highlight every 3.5s with progress bar, hover pauses
 *   .mt-ind           industry tiles, auto-expand every 3.5s (>= 1100px)
 * Nothing runs inside the Elementor editor, so every element stays visible there.
 */
( function () {
	'use strict';

	var reduceMotion = window.matchMedia && window.matchMedia( '(prefers-reduced-motion: reduce)' ).matches;

	function children( parent, cls ) {
		return Array.prototype.filter.call( parent.children, function ( el ) {
			return el.classList.contains( cls );
		} );
	}

	/* ---------- Categories ---------- */
	function initCategories( section ) {
		var grid = section.querySelector( '.mt-cat-grid' );
		if ( ! grid ) return;
		var cards = children( grid, 'mt-cat-card' );
		var n = cards.length;
		var perView = 4;
		if ( n <= perView ) return;

		var start = 0;
		var pages = Math.ceil( n / 2 );
		var dotsWrap = section.querySelector( '.mt-cat-dots' );
		var dots = [];
		if ( dotsWrap ) {
			dotsWrap.innerHTML = '';
			for ( var d = 0; d < pages; d++ ) {
				dots.push( dotsWrap.appendChild( document.createElement( 'span' ) ) );
			}
		}

		function render( animate, dir ) {
			var shown = [];
			cards.forEach( function ( c ) {
				c.classList.add( 'is-hidden' );
				c.style.order = '';
				c.classList.remove( 'mt-card-in', 'mt-card-in--back' );
			} );
			for ( var i = 0; i < perView; i++ ) {
				var card = cards[ ( start + i ) % n ];
				card.classList.remove( 'is-hidden' );
				card.style.order = String( i + 1 );
				shown.push( card );
			}
			var page = Math.floor( start / 2 );
			dots.forEach( function ( dot, i ) {
				dot.classList.toggle( 'is-active', i === page );
			} );
			if ( animate && ! reduceMotion ) {
				/* Cards slide in from the side they come from, staggered left to right. */
				shown.forEach( function ( c, i ) {
					void c.offsetWidth;
					c.style.animationDelay = ( i * 70 ) + 'ms';
					c.classList.add( dir < 0 ? 'mt-card-in--back' : 'mt-card-in' );
				} );
			}
		}

		var prev = section.querySelector( '.mt-cat-prev' );
		var next = section.querySelector( '.mt-cat-next' );
		if ( prev ) prev.addEventListener( 'click', function () { start = ( start - 2 + n * 2 ) % n; render( true, -1 ); restart(); } );
		if ( next ) next.addEventListener( 'click', function () { start = ( start + 2 ) % n; render( true, 1 ); restart(); } );

		/* Auto-advance every 3s. Being on screen never pauses it — it holds only while
		   the pointer or keyboard focus is on a visible card. The hold is recomputed on
		   each tick rather than tracked with mouseenter/mouseleave, because a card can be
		   hidden out from under the pointer and never fire its mouseleave, which would
		   otherwise leave the carousel stuck for good. */
		function held() {
			for ( var i = 0; i < n; i++ ) {
				if ( cards[ i ].classList.contains( 'is-hidden' ) ) continue;
				if ( cards[ i ].matches( ':hover' ) ) return true;
				if ( cards[ i ].contains( document.activeElement ) ) return true;
			}
			return false;
		}
		var timer = null;
		function play() {
			if ( timer ) return;
			timer = window.setInterval( function () {
				if ( document.hidden || held() ) return;
				start = ( start + 2 ) % n;
				render( true, 1 );
			}, 3000 );
		}
		function stop() { window.clearInterval( timer ); timer = null; }
		function restart() { stop(); play(); }

		render( false );
		play();
	}

	/* ---------- Services slider ---------- */
	function initServices( section ) {
		var viewport = section.querySelector( '.mt-svc-viewport' );
		var track = section.querySelector( '.mt-svc-track' );
		if ( ! viewport || ! track ) return;
		var slides = children( track, 'mt-svc-card' );
		if ( ! slides.length ) return;

		var dotsWrap = section.querySelector( '.mt-svc-dots' );
		var page = 0;
		var pages = 1;
		var hover = false;

		function perView() { return window.innerWidth >= 760 ? 2 : 1; }

		function buildDots() {
			if ( ! dotsWrap ) return;
			dotsWrap.innerHTML = '';
			for ( var i = 0; i < pages; i++ ) {
				var b = document.createElement( 'button' );
				b.type = 'button';
				b.setAttribute( 'aria-label', 'Go to slide ' + ( i + 1 ) );
				b.addEventListener( 'click', go.bind( null, i ) );
				dotsWrap.appendChild( b );
			}
		}

		function render() {
			track.style.transform = 'translateX(calc(' + ( -page ) + ' * (100% + 24px)))';
			if ( dotsWrap ) {
				Array.prototype.forEach.call( dotsWrap.children, function ( b, i ) {
					b.classList.toggle( 'is-active', i === page );
				} );
			}
		}

		function go( i ) {
			page = ( i + pages ) % pages;
			render();
		}

		function layout() {
			var p = Math.ceil( slides.length / perView() );
			if ( p !== pages ) {
				pages = p;
				page = page % pages;
				buildDots();
			}
			render();
		}

		var prev = section.querySelector( '.mt-svc-prev' );
		var next = section.querySelector( '.mt-svc-next' );
		if ( prev ) prev.addEventListener( 'click', function () { go( page - 1 ); } );
		if ( next ) next.addEventListener( 'click', function () { go( page + 1 ); } );
		viewport.addEventListener( 'mouseenter', function () { hover = true; } );
		viewport.addEventListener( 'mouseleave', function () { hover = false; } );
		window.addEventListener( 'resize', layout );

		pages = 0;
		layout();
		if ( ! reduceMotion ) {
			setInterval( function () { if ( ! hover ) go( page + 1 ); }, 5000 );
		}
	}

	/* ---------- Why Microtec ---------- */
	function initWhy( grid ) {
		var cards = children( grid, 'mt-why-card' );
		if ( ! cards.length ) return;
		var active = 0;
		var hover = false;

		function set( k, paused ) {
			cards.forEach( function ( c, j ) {
				c.classList.remove( 'is-running' );
				c.classList.toggle( 'is-active', j === k );
			} );
			if ( ! paused && ! reduceMotion ) {
				void cards[ k ].offsetWidth; // restart the progress bar
				cards[ k ].classList.add( 'is-running' );
			}
		}

		cards.forEach( function ( c, j ) {
			c.addEventListener( 'mouseenter', function () {
				hover = true;
				active = j;
				set( j, true );
			} );
		} );
		grid.addEventListener( 'mouseleave', function () { hover = false; } );

		set( 0, false );
		if ( ! reduceMotion ) {
			setInterval( function () {
				if ( hover ) return;
				active = ( active + 1 ) % cards.length;
				set( active, false );
			}, 3500 );
		}
	}

	/* ---------- Industries ---------- */
	function initIndustries( wrap ) {
		var tiles = children( wrap, 'mt-ind-tile' );
		if ( ! tiles.length ) return;
		var active = 0;
		var hover = false;

		function set( k ) {
			tiles.forEach( function ( t, j ) { t.classList.toggle( 'is-active', j === k ); } );
		}

		tiles.forEach( function ( t, j ) {
			t.addEventListener( 'mouseenter', function () {
				hover = true;
				active = j;
				set( j );
			} );
		} );
		wrap.addEventListener( 'mouseleave', function () { hover = false; } );

		set( 0 );
		if ( ! reduceMotion ) {
			setInterval( function () {
				if ( hover || window.innerWidth < 1100 ) return;
				active = ( active + 1 ) % tiles.length;
				set( active );
			}, 3500 );
		}
	}

	function init() {
		if ( document.body.classList.contains( 'elementor-editor-active' ) ) return;
		document.querySelectorAll( '.mt-cat-section' ).forEach( initCategories );
		document.querySelectorAll( '.mt-svc-section' ).forEach( initServices );
		document.querySelectorAll( '.mt-why-grid' ).forEach( initWhy );
		document.querySelectorAll( '.mt-ind' ).forEach( initIndustries );
	}

	if ( document.readyState === 'loading' ) {
		document.addEventListener( 'DOMContentLoaded', init );
	} else {
		init();
	}
} )();