/**
 * Microtec Engineering — Contact page enquiry form.
 *
 * The photo upload is a styled drop box (.mtc-file) with the real file input hidden inside it, so
 * this shows the chosen file's name in the box, and puts the hint back when the form is sent and
 * Contact Form 7 clears it.
 */
( function () {
	'use strict';

	document.addEventListener( 'change', function ( e ) {
		var input = e.target;
		if ( ! input.matches || ! input.matches( '.mtc-file input[type="file"]' ) ) return;
		var box = input.closest( '.mtc-file' );
		var name = box && box.querySelector( '.mtc-file-name' );
		if ( ! name ) return;
		if ( ! name.dataset.hint ) name.dataset.hint = name.textContent;
		name.textContent = input.files && input.files.length ? input.files[ 0 ].name : name.dataset.hint;
	} );

	document.addEventListener( 'wpcf7mailsent', function ( e ) {
		[].forEach.call( e.target.querySelectorAll( '.mtc-file-name' ), function ( name ) {
			if ( name.dataset.hint ) name.textContent = name.dataset.hint;
		} );
	} );
} )();
