/**
 * Microtec Engineering — interactive installation guides (the Bronto guide).
 *
 * Step cards (.mtb-step) are tap-to-tick. Ticking updates the "Your progress" count and bar,
 * the per-phase counts beside the phase links (.mtb-phases), and shows the "All steps complete"
 * note. Progress is remembered in this browser for the page. A "#print" link prints the guide,
 * which the browser can save as a PDF. Nothing runs inside the Elementor editor.
 */
( function () {
	'use strict';

	function init() {
		var wrap = document.querySelector( '.mtb-steps' );
		if ( ! wrap || document.body.classList.contains( 'elementor-editor-active' ) ) return;

		var steps = [].slice.call( wrap.querySelectorAll( '.mtb-step' ) );
		var phases = [].slice.call( wrap.querySelectorAll( '.mtb-phase' ) );
		var count = document.querySelector( '.mtb-count .elementor-heading-title' );
		var bar = document.querySelector( '.mtb-bar-fill' );
		var allDone = document.querySelector( '.mtb-alldone' );
		var links = [].slice.call( document.querySelectorAll( '.mtb-phases .elementor-icon-list-item a' ) );
		var key = 'mtb-done:' + window.location.pathname;
		var done = {};

		try { done = JSON.parse( window.localStorage.getItem( key ) || '{}' ) || {}; } catch ( e ) { done = {}; }

		// A count beside each phase link, e.g. "0/6".
		var counts = links.map( function ( a ) {
			var span = document.createElement( 'span' );
			span.className = 'mtb-pcount';
			a.appendChild( span );
			return span;
		} );

		function render() {
			var total = 0;
			steps.forEach( function ( s, i ) {
				var d = !! done[ i + 1 ];
				s.classList.toggle( 'is-done', d );
				s.setAttribute( 'aria-pressed', d ? 'true' : 'false' );
				if ( d ) total++;
			} );
			phases.forEach( function ( p, i ) {
				var mine = p.querySelectorAll( '.mtb-step' ), n = 0;
				[].forEach.call( mine, function ( s ) { if ( s.classList.contains( 'is-done' ) ) n++; } );
				if ( counts[ i ] ) {
					counts[ i ].textContent = n + '/' + mine.length;
					counts[ i ].classList.toggle( 'is-complete', n === mine.length );
				}
			} );
			if ( count ) count.textContent = total + ' / ' + steps.length;
			if ( bar ) bar.style.setProperty( '--mtb-pct', Math.round( total / steps.length * 100 ) + '%' );
			if ( allDone ) allDone.classList.toggle( 'is-visible', total === steps.length );
		}

		function toggle( i ) {
			done[ i + 1 ] = ! done[ i + 1 ];
			if ( ! done[ i + 1 ] ) delete done[ i + 1 ];
			try { window.localStorage.setItem( key, JSON.stringify( done ) ); } catch ( e ) {}
			render();
		}

		steps.forEach( function ( s, i ) {
			s.setAttribute( 'role', 'button' );
			s.setAttribute( 'tabindex', '0' );
			s.addEventListener( 'click', function ( e ) {
				if ( e.target.closest( 'a' ) ) return;
				toggle( i );
			} );
			s.addEventListener( 'keydown', function ( e ) {
				if ( e.key === 'Enter' || e.key === ' ' ) { e.preventDefault(); toggle( i ); }
			} );
		} );
		render();
	}

	document.addEventListener( 'click', function ( e ) {
		var a = e.target.closest( 'a[href="#print"]' );
		if ( ! a ) return;
		e.preventDefault();
		window.print();
	} );

	if ( document.readyState === 'loading' ) {
		document.addEventListener( 'DOMContentLoaded', init );
	} else {
		init();
	}
} )();
