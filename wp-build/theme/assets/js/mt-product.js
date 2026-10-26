/**
 * Microtec Engineering — product page and wishlist.
 *
 * - Quantity: − / + buttons either side of the number (the browser's own spinner arrows
 *   covered the digits).
 * - Wishlist: "Add to wishlist" saves the product id in this browser (localStorage); the
 *   /wishlist/ page ([mt_wishlist]) lists the saved products from the WooCommerce Store API,
 *   with Add to cart / View product and Remove.
 * - Share: "Copy link" copies the product address.
 */
( function () {
	'use strict';

	var cfg = window.mtProduct || { rest: '/wp-json/', wishlist: '/wishlist/', shop: '/products/' };
	var KEY = 'mtWishlist';

	/* ---- Wishlist storage ---- */
	function readList() {
		try {
			var v = JSON.parse( window.localStorage.getItem( KEY ) || '[]' );
			return Array.isArray( v ) ? v.map( Number ).filter( Boolean ) : [];
		} catch ( e ) { return []; }
	}
	function writeList( list ) {
		try { window.localStorage.setItem( KEY, JSON.stringify( list ) ); } catch ( e ) {}
	}

	/* ---- Quantity buttons ---- */
	function initQuantity( root ) {
		[].forEach.call( root.querySelectorAll( 'form.cart .quantity' ), function ( q ) {
			var input = q.querySelector( 'input.qty' );
			if ( ! input || input.type === 'hidden' || q.classList.contains( 'mt-qty' ) ) return;
			q.classList.add( 'mt-qty' );
			function step( dir ) {
				var min = parseFloat( input.min ) || 1;
				var max = parseFloat( input.max ) || Infinity;
				var st = parseFloat( input.step ) || 1;
				var val = ( parseFloat( input.value ) || min ) + dir * st;
				input.value = Math.min( max, Math.max( min, val ) );
				input.dispatchEvent( new Event( 'change', { bubbles: true } ) );
			}
			[ [ -1, '−', 'Decrease quantity' ], [ 1, '+', 'Increase quantity' ] ].forEach( function ( b ) {
				var btn = document.createElement( 'button' );
				btn.type = 'button';
				btn.className = 'mt-qty-btn ' + ( b[ 0 ] < 0 ? 'mt-qty-minus' : 'mt-qty-plus' );
				btn.textContent = b[ 1 ];
				btn.setAttribute( 'aria-label', b[ 2 ] );
				btn.addEventListener( 'click', function () { step( b[ 0 ] ); } );
				if ( b[ 0 ] < 0 ) q.insertBefore( btn, input ); else q.appendChild( btn );
			} );
		} );
	}

	/* ---- Wishlist button on the product page ---- */
	function initWishButton() {
		var btn = document.querySelector( '.mt-wish' );
		if ( ! btn ) return;
		var id = Number( btn.dataset.id );
		var label = btn.querySelector( '.mt-wish-label' );
		var view = document.createElement( 'a' );
		view.className = 'mt-wish-view';
		view.href = cfg.wishlist;
		view.textContent = 'View wishlist →';
		btn.insertAdjacentElement( 'afterend', view );

		function render() {
			var on = readList().indexOf( id ) !== -1;
			btn.classList.toggle( 'is-on', on );
			btn.setAttribute( 'aria-pressed', on ? 'true' : 'false' );
			label.textContent = on ? 'In your wishlist' : 'Add to wishlist';
			view.hidden = ! on;
		}
		btn.addEventListener( 'click', function () {
			var list = readList();
			var i = list.indexOf( id );
			if ( i === -1 ) list.unshift( id ); else list.splice( i, 1 );
			writeList( list );
			render();
		} );
		render();
	}

	/* ---- Copy link ---- */
	document.addEventListener( 'click', function ( e ) {
		var b = e.target.closest( '.mt-share-copy' );
		if ( ! b ) return;
		var url = b.dataset.url;
		var done = function () {
			b.classList.add( 'is-copied' );
			b.setAttribute( 'title', 'Link copied' );
			setTimeout( function () { b.classList.remove( 'is-copied' ); b.setAttribute( 'title', 'Copy link' ); }, 1800 );
		};
		if ( navigator.clipboard ) navigator.clipboard.writeText( url ).then( done, function () { window.prompt( 'Copy this link:', url ); } );
		else window.prompt( 'Copy this link:', url );
	} );

	/* ---- Wishlist page ---- */
	function esc( s ) {
		var d = document.createElement( 'div' );
		d.textContent = s == null ? '' : String( s );
		return d.innerHTML;
	}
	function initWishlistPage() {
		var box = document.querySelector( '.mt-wishlist' );
		if ( ! box ) return;
		function empty() {
			box.innerHTML = '<div class="mt-wishlist-none"><p>Your wishlist is empty.</p>' +
				'<p>Tap <strong>Add to wishlist</strong> on any product to save it here.</p>' +
				'<a class="mt-wishlist-btn" href="' + esc( cfg.shop ) + '">Browse products →</a></div>';
		}
		function load() {
			var list = readList();
			if ( ! list.length ) { empty(); return; }
			fetch( cfg.rest + 'wc/store/v1/products?per_page=100&include=' + list.join( ',' ), { credentials: 'same-origin' } )
				.then( function ( r ) { return r.ok ? r.json() : []; } )
				.catch( function () { return []; } )
				.then( function ( products ) {
					var byId = {};
					( products || [] ).forEach( function ( p ) { byId[ p.id ] = p; } );
					var items = list.map( function ( id ) { return byId[ id ]; } ).filter( Boolean );
					if ( ! items.length ) { empty(); return; }
					box.innerHTML = '<p class="mt-wishlist-count">' + items.length + ' saved product' + ( items.length === 1 ? '' : 's' ) + '</p>' +
						'<ul class="mt-wishlist-grid">' + items.map( function ( p ) {
							var img = p.images && p.images[ 0 ] ? ( p.images[ 0 ].thumbnail || p.images[ 0 ].src ) : '';
							var buy = p.is_purchasable && p.is_in_stock && p.type === 'simple'
								? '<a class="mt-wishlist-btn" href="' + esc( p.permalink ) + '?add-to-cart=' + p.id + '">Add to cart</a>'
								: '<a class="mt-wishlist-btn" href="' + esc( p.permalink ) + '">View product</a>';
							return '<li class="mt-wishlist-item">' +
								'<a class="mt-wishlist-img" href="' + esc( p.permalink ) + '">' + ( img ? '<img src="' + esc( img ) + '" alt="" loading="lazy">' : '' ) + '</a>' +
								'<div class="mt-wishlist-info"><a class="mt-wishlist-name" href="' + esc( p.permalink ) + '">' + p.name + '</a>' +
								'<span class="mt-wishlist-price">' + ( p.price_html || '' ) + '</span></div>' +
								'<div class="mt-wishlist-actions">' + buy +
								'<button type="button" class="mt-wishlist-remove" data-id="' + p.id + '">Remove</button></div></li>';
						} ).join( '' ) + '</ul>';
				} );
		}
		box.addEventListener( 'click', function ( e ) {
			var r = e.target.closest( '.mt-wishlist-remove' );
			if ( ! r ) return;
			writeList( readList().filter( function ( id ) { return id !== Number( r.dataset.id ); } ) );
			load();
		} );
		load();
	}

	function init() {
		initQuantity( document );
		initWishButton();
		initWishlistPage();
	}
	if ( document.readyState === 'loading' ) document.addEventListener( 'DOMContentLoaded', init );
	else init();
} )();
