/**
 * Microtec Engineering — search popup.
 *
 * The header search icon (.mt-header-search) opens a popup instead of the small inline box:
 * a large search field, live suggestions as you type (products with photo and price from the
 * WooCommerce Store API, pages and guides from the WordPress REST API) and quick links.
 * Enter, or "See all results", goes to the full results page (search.php).
 */
( function () {
	'use strict';

	var cfg = window.mtSearch || { home: '/', rest: '/wp-json/' };
	var LINKS = [
		[ 'Tadano Parts', 'product-category/tadano-parts/' ],
		[ 'Kato Parts', 'product-category/kato-parts/' ],
		[ 'LCDs', 'product-category/lcds/' ],
		[ 'Overlays', 'product-category/overlays/' ],
		[ 'Warning Lights', 'product-category/warning-lights-accessories/' ],
		[ 'Technical Guides', 'guides/' ]
	];
	var ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>';

	var modal, input, results, timer, lastFocus, seq = 0;

	function esc( s ) {
		var d = document.createElement( 'div' );
		d.textContent = s == null ? '' : String( s );
		return d.innerHTML;
	}

	function build() {
		modal = document.createElement( 'div' );
		modal.className = 'mt-sp';
		modal.setAttribute( 'role', 'dialog' );
		modal.setAttribute( 'aria-modal', 'true' );
		modal.setAttribute( 'aria-label', 'Search' );
		modal.hidden = true;
		modal.innerHTML =
			'<div class="mt-sp-backdrop" data-close></div>' +
			'<div class="mt-sp-panel">' +
				'<form class="mt-sp-form" role="search" method="get" action="' + esc( cfg.home ) + '">' +
					'<span class="mt-sp-icon" aria-hidden="true">' + ICON + '</span>' +
					'<input class="mt-sp-input" type="search" name="s" autocomplete="off" placeholder="Search products, part numbers and guides…" aria-label="Search">' +
					'<button class="mt-sp-submit" type="submit">Search</button>' +
					'<button class="mt-sp-close" type="button" data-close aria-label="Close search">&times;</button>' +
				'</form>' +
				'<div class="mt-sp-results" aria-live="polite"></div>' +
			'</div>';
		document.body.appendChild( modal );
		input = modal.querySelector( '.mt-sp-input' );
		results = modal.querySelector( '.mt-sp-results' );

		modal.addEventListener( 'click', function ( e ) {
			if ( e.target.closest( '[data-close]' ) ) close();
		} );
		input.addEventListener( 'input', function () {
			clearTimeout( timer );
			timer = setTimeout( suggest, 250 );
		} );
		modal.addEventListener( 'keydown', function ( e ) {
			if ( e.key === 'Escape' ) { close(); return; }
			if ( e.key !== 'Tab' ) return;
			// Keep keyboard focus inside the popup.
			var f = modal.querySelectorAll( 'input, button, a[href]' );
			var first = f[ 0 ], last = f[ f.length - 1 ];
			if ( e.shiftKey && document.activeElement === first ) { last.focus(); e.preventDefault(); }
			else if ( ! e.shiftKey && document.activeElement === last ) { first.focus(); e.preventDefault(); }
		} );
		quickLinks();
	}

	function quickLinks() {
		results.innerHTML = '<p class="mt-sp-label">Popular</p><div class="mt-sp-chips">' +
			LINKS.map( function ( l ) {
				return '<a class="mt-sp-chip" href="' + esc( cfg.home + l[ 1 ] ) + '">' + esc( l[ 0 ] ) + '</a>';
			} ).join( '' ) + '</div>';
	}

	function open() {
		if ( ! modal ) build();
		lastFocus = document.activeElement;
		modal.hidden = false;
		document.documentElement.classList.add( 'mt-sp-open' );
		requestAnimationFrame( function () {
			modal.classList.add( 'is-open' );
			input.focus();
			input.select();
		} );
	}

	function close() {
		modal.classList.remove( 'is-open' );
		document.documentElement.classList.remove( 'mt-sp-open' );
		setTimeout( function () { modal.hidden = true; }, 200 );
		if ( lastFocus && lastFocus.focus ) lastFocus.focus();
	}

	function getJSON( url ) {
		return fetch( url, { credentials: 'same-origin' } ).then( function ( r ) {
			return r.ok ? r.json() : [];
		} ).catch( function () { return []; } );
	}

	function suggest() {
		var q = input.value.trim();
		if ( q.length < 2 ) { quickLinks(); return; }
		var mine = ++seq;
		results.innerHTML = '<p class="mt-sp-label">Searching…</p>';
		// WordPress search (titles and descriptions, as on the results page) finds the matches;
		// the Store API then supplies photos and prices for the products, in the same order.
		getJSON( cfg.rest + 'wp/v2/search?type=post&subtype=product,page&per_page=12&search=' + encodeURIComponent( q ) ).then( function ( hits ) {
			var ids = [], pages = [];
			( hits || [] ).forEach( function ( h ) {
				if ( h.subtype === 'product' && ids.length < 6 ) ids.push( h.id );
				if ( h.subtype === 'page' && pages.length < 4 ) pages.push( h );
			} );
			var products = ids.length ? getJSON( cfg.rest + 'wc/store/v1/products?per_page=6&include=' + ids.join( ',' ) ) : Promise.resolve( [] );
			return products.then( function ( list ) {
				var byId = {};
				( list || [] ).forEach( function ( p ) { byId[ p.id ] = p; } );
				return [ ids.map( function ( id ) { return byId[ id ]; } ).filter( Boolean ), pages ];
			} );
		} ).then( function ( r ) {
			if ( mine !== seq ) return; // a newer search has started
			render( q, r[ 0 ], r[ 1 ] );
		} );
	}

	function render( q, products, pages ) {
		var html = '';
		if ( products.length ) {
			html += '<p class="mt-sp-label">Products</p><div class="mt-sp-products">' + products.map( function ( p ) {
				var img = p.images && p.images[ 0 ] ? ( p.images[ 0 ].thumbnail || p.images[ 0 ].src ) : '';
				var price = p.price_html ? p.price_html : '';
				return '<a class="mt-sp-product" href="' + esc( p.permalink ) + '">' +
					'<span class="mt-sp-thumb">' + ( img ? '<img src="' + esc( img ) + '" alt="" loading="lazy">' : '' ) + '</span>' +
					'<span class="mt-sp-pname">' + p.name +
						( price ? '<span class="mt-sp-price">' + price + '</span>' : '' ) +
					'</span></a>';
			} ).join( '' ) + '</div>';
		}
		if ( pages.length ) {
			html += '<p class="mt-sp-label">Pages &amp; guides</p><div class="mt-sp-pages">' + pages.map( function ( p ) {
				return '<a class="mt-sp-page" href="' + esc( p.url ) + '">' + p.title + ' <span aria-hidden="true">→</span></a>';
			} ).join( '' ) + '</div>';
		}
		if ( ! html ) {
			html = '<p class="mt-sp-empty">No matches for “' + esc( q ) + '”. Try a part number or brand, or call <a href="tel:0397922243">03 9792 2243</a>.</p>';
		} else {
			html += '<a class="mt-sp-all" href="' + esc( cfg.home + '?s=' + encodeURIComponent( q ) ) + '">See all results for “' + esc( q ) + '” →</a>';
		}
		results.innerHTML = html;
	}

	// The header search icon opens the popup. Capture phase, so the widget's own inline box
	// never opens.
	document.addEventListener( 'click', function ( e ) {
		var trigger = e.target.closest( '.mt-header-search' );
		if ( ! trigger || document.body.classList.contains( 'elementor-editor-active' ) ) return;
		e.preventDefault();
		e.stopImmediatePropagation();
		open();
	}, true );

	// A link ending in #search opens the popup straight away.
	if ( window.location.hash === '#search' ) open();
} )();
