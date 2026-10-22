<?php
/**
 * Microtec Engineering child theme.
 */

defined( 'ABSPATH' ) || exit;

define( 'MICROTEC_CHILD_VERSION', '1.0.0' );

add_action( 'wp_enqueue_scripts', function () {
	$dir = get_stylesheet_directory();
	$uri = get_stylesheet_directory_uri();

	wp_enqueue_style( 'hello-elementor-parent', get_template_directory_uri() . '/style.css', [], MICROTEC_CHILD_VERSION );
	wp_enqueue_style( 'microtec', $uri . '/assets/css/microtec.css', [ 'hello-elementor-parent' ], filemtime( $dir . '/assets/css/microtec.css' ) );
	wp_enqueue_script( 'microtec', $uri . '/assets/js/microtec.js', [], filemtime( $dir . '/assets/js/microtec.js' ), true );
}, 20 );

// Pages built from the design handoff (Home, About, Services, Load Systems): their own type,
// section styles and the slider / highlight behaviour.
add_action( 'wp_enqueue_scripts', function () {
	if ( ! is_page() ) {
		return;
	}
	$dir = get_stylesheet_directory();
	$uri = get_stylesheet_directory_uri();

	wp_enqueue_style( 'microtec-pages-fonts', 'https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap', [], null );
	wp_enqueue_style( 'microtec-pages', $uri . '/assets/css/mt-pages.css', [ 'microtec' ], filemtime( $dir . '/assets/css/mt-pages.css' ) );
	wp_enqueue_script( 'microtec-pages', $uri . '/assets/js/mt-pages.js', [], filemtime( $dir . '/assets/js/mt-pages.js' ), true );
}, 30 );

// Load the brand CSS inside the Elementor editor preview too, so editing matches the front end.
add_action( 'elementor/preview/enqueue_styles', function () {
	wp_enqueue_style( 'microtec', get_stylesheet_directory_uri() . '/assets/css/microtec.css', [], filemtime( get_stylesheet_directory() . '/assets/css/microtec.css' ) );
	wp_enqueue_style( 'microtec-pages', get_stylesheet_directory_uri() . '/assets/css/mt-pages.css', [ 'microtec' ], filemtime( get_stylesheet_directory() . '/assets/css/mt-pages.css' ) );
} );

// Contact Form 7: no auto <p>/<br>, so the enquiry form keeps its grid markup.
add_filter( 'wpcf7_autop_or_not', '__return_false' );

/**
 * [mt_cart_link label="Cart"] — text cart link with live item count, used in the header top bar.
 */
add_shortcode( 'mt_cart_link', function ( $atts ) {
	$atts  = shortcode_atts( [ 'label' => 'Cart' ], $atts );
	$count = ( function_exists( 'WC' ) && WC()->cart ) ? WC()->cart->get_cart_contents_count() : 0;
	$url   = function_exists( 'wc_get_cart_url' ) ? wc_get_cart_url() : home_url( '/cart/' );
	return sprintf(
		'<a class="mt-cart-link" href="%s">%s (<span class="mt-cart-count">%d</span>)</a>',
		esc_url( $url ),
		esc_html( $atts['label'] ),
		(int) $count
	);
} );

// Keep the top-bar count in sync when products are added via AJAX.
add_filter( 'woocommerce_add_to_cart_fragments', function ( $fragments ) {
	$fragments['span.mt-cart-count'] = '<span class="mt-cart-count">' . (int) WC()->cart->get_cart_contents_count() . '</span>';
	return $fragments;
} );