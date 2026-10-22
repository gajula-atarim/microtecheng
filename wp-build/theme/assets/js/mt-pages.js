/*
 * Microtec Engineering — inner page behaviour.
 * EWP Control Systems: the feature list highlights one item at a time (3s each, with a
 * progress bar), pausing while the pointer is over the list.
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

	function init() {
		document.querySelectorAll( '.mtp-ewp-list' ).forEach( initEwp );
	}

	if ( document.readyState === 'loading' ) {
		document.addEventListener( 'DOMContentLoaded', init );
	} else {
		init();
	}
} )();
