/*
 * Microtec Engineering — page behaviour for the sections built from the design handoff.
 * EWP Control Systems: the feature list highlights one item at a time (3s each, with a
 * progress bar), pausing while the pointer is over the list.
 * Homepage: hero slides (5s), component categories (arrows), services slider (5s, 2-up from
 * 760px), "Why choose Microtec" highlight (3.5s) and industry tiles (3.5s), as in the design.
 */
( function () {
	'use strict';

	var STEP = 3000;
	var reduced = window.matchMedia && window.matchMedia( '(prefers-reduced-motion: reduce)' ).matches;

	function initEwp( list ) {
		var items = list.querySelectorAll( '.mtp-ewp-item' );
		if ( ! items.length ) return;
		var current = 0, timer = null;

		function show( i ) {
			items[ current ].classList.remove( 'is-active' );
			current = i % items.length;
			items[ current ].classList.add( 'is-active' );
		}
		function start() {
			if ( reduced || timer ) return;
			timer = setInterval( function () { show( current + 1 ); }, STEP );
		}
		function stop() {
			clearInterval( timer );
			timer = null;
		}

		show( 0 );
		start();
		list.addEventListener( 'mouseenter', stop );
		list.addEventListener( 'mouseleave', start );
	}

	// Mark one item of a group active.
	function activate( items, i ) {
		items.forEach( function ( el, n ) { el.classList.toggle( 'is-active', n === i ); } );
	}

	// Run fn every `ms` unless reduced motion is on or `paused()` says to wait.
	function every( ms, fn, paused ) {
		if ( reduced ) return;
		setInterval( function () { if ( ! paused() ) fn(); }, ms );
	}

	function initHero( hero ) {
		var bgs = hero.querySelectorAll( '.mtp-cyc-hero-bg' ),
			cards = hero.querySelectorAll( '.mtp-cyc-hero-card' ),
			tabs = hero.querySelectorAll( '.mtp-cyc-hero-tab' ),
			slides = JSON.parse( hero.getAttribute( 'data-slides' ) || '[]' ),
			cap = hero.querySelector( '.mtp-hero-cap' ),
			link = hero.querySelector( '.mtp-hero-link' ),
			count = hero.querySelector( '.mtp-hero-count' ),
			current = 0, timer = null;
		if ( ! bgs.length ) return;

		function show( i ) {
			current = ( i + bgs.length ) % bgs.length;
			activate( [].slice.call( bgs ), current );
			activate( [].slice.call( cards ), current );
			activate( [].slice.call( tabs ), current );
			if ( slides[ current ] ) {
				if ( cap ) cap.textContent = slides[ current ].cap;
				if ( link ) link.textContent = slides[ current ].link;
			}
			if ( count ) count.textContent = '0' + ( current + 1 ) + ' / 0' + bgs.length;
		}
		function start() {
			if ( reduced ) return;
			clearInterval( timer );
			timer = setInterval( function () { show( current + 1 ); }, 5000 );
		}
		tabs.forEach( function ( tab, i ) {
			tab.addEventListener( 'click', function () { show( i ); start(); } );
		} );
		start();
	}

	function initCategories( grid ) {
		var cats = JSON.parse( grid.getAttribute( 'data-cats' ) || '[]' ),
			cards = grid.querySelectorAll( '.mtp-cat-card' ),
			dots = [].slice.call( grid.querySelectorAll( '.mtp-cyc-cat-dot' ) ),
			start = 0;
		if ( ! cats.length || ! cards.length ) return;

		function render() {
			cards.forEach( function ( card, i ) {
				var c = cats[ ( start + i ) % cats.length ],
					img = card.querySelector( '.mtp-cat-img' ),
					name = card.querySelector( '.mtp-cat-name' ),
					desc = card.querySelector( '.mtp-cat-desc' );
				if ( c.url ) card.setAttribute( 'href', c.url );
				if ( img ) { img.src = c.img; img.alt = c.name; }
				if ( name ) name.textContent = c.name;
				if ( desc ) desc.textContent = c.desc;
				card.classList.remove( 'is-swapping' );
				void card.offsetWidth;
				card.classList.add( 'is-swapping' );
			} );
			activate( dots, Math.floor( start / 2 ) );
		}
		var prev = grid.querySelector( '.mtp-cat-prev' ), next = grid.querySelector( '.mtp-cat-next' );
		if ( prev ) prev.addEventListener( 'click', function () { start = ( start - 2 + cats.length * 2 ) % cats.length; render(); } );
		if ( next ) next.addEventListener( 'click', function () { start = ( start + 2 ) % cats.length; render(); } );
	}

	function initServices( view ) {
		var track = view.querySelector( '.mtp-svc-track' ),
			section = view.closest( 'section' ) || view.parentNode,
			dotsWrap = section.querySelector( '.mtp-svc-dots' ),
			template = dotsWrap && dotsWrap.querySelector( '.mtp-cyc-svc-dot' ),
			count = track ? track.children.length : 0,
			page = 0, pages = 0, hover = false, dots = [];
		if ( ! track || ! count ) return;

		function perView() { return window.innerWidth >= 760 ? 2 : 1; }
		function build() {
			var n = Math.ceil( count / perView() );
			if ( n === pages || ! template ) return;
			pages = n;
			dotsWrap.innerHTML = '';
			dots = [];
			for ( var i = 0; i < n; i++ ) {
				var d = template.cloneNode( true );
				d.setAttribute( 'aria-label', 'Go to slide ' + ( i + 1 ) );
				d.addEventListener( 'click', go.bind( null, i ) );
				dotsWrap.appendChild( d );
				dots.push( d );
			}
			go( Math.min( page, n - 1 ) );
		}
		function go( i ) {
			page = ( i + pages ) % pages;
			track.style.transform = 'translateX(calc(' + ( -page ) + ' * (100% + 24px)))';
			activate( dots, page );
		}
		var prev = section.querySelector( '.mtp-svc-prev' ), next = section.querySelector( '.mtp-svc-next' );
		if ( prev ) prev.addEventListener( 'click', function () { go( page - 1 ); } );
		if ( next ) next.addEventListener( 'click', function () { go( page + 1 ); } );
		view.addEventListener( 'mouseenter', function () { hover = true; } );
		view.addEventListener( 'mouseleave', function () { hover = false; } );
		window.addEventListener( 'resize', build );
		build();
		every( 5000, function () { go( page + 1 ); }, function () { return hover; } );
	}

	// A group that highlights one item at a time and jumps to the item under the pointer.
	function initHighlight( wrap, itemSelector, ms ) {
		var items = [].slice.call( wrap.querySelectorAll( itemSelector ) ),
			current = 0, hover = false;
		if ( ! items.length ) return;
		items.forEach( function ( item, i ) {
			item.addEventListener( 'mouseenter', function () { hover = true; current = i; activate( items, i ); } );
		} );
		wrap.addEventListener( 'mouseleave', function () { hover = false; } );
		every( ms, function () { current = ( current + 1 ) % items.length; activate( items, current ); }, function () { return hover; } );
	}

	function init() {
		document.querySelectorAll( '.mtp-ewp-list' ).forEach( initEwp );
		document.querySelectorAll( '.mtp-hero-slider' ).forEach( initHero );
		document.querySelectorAll( '.mtp-cats' ).forEach( initCategories );
		document.querySelectorAll( '.mtp-svc' ).forEach( initServices );
		document.querySelectorAll( '.mtp-why' ).forEach( function ( el ) { initHighlight( el, '.mtp-cyc-why', 3500 ); } );
		document.querySelectorAll( '.mtp-ind' ).forEach( function ( el ) { initHighlight( el, '.mtp-cyc-ind', 3500 ); } );
	}

	if ( document.readyState === 'loading' ) {
		document.addEventListener( 'DOMContentLoaded', init );
	} else {
		init();
	}
} )();
