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
	// Technical / Installation Guides: built from Elementor widgets, styled by class.
	wp_enqueue_style( 'microtec-guides', $uri . '/assets/css/mt-guides.css', [ 'microtec-pages' ], filemtime( $dir . '/assets/css/mt-guides.css' ) );
	wp_enqueue_script( 'microtec-guide', $uri . '/assets/js/mt-guide.js', [], filemtime( $dir . '/assets/js/mt-guide.js' ), true );
}, 30 );

// Load the brand CSS inside the Elementor editor preview too, so editing matches the front end.
add_action( 'elementor/preview/enqueue_styles', function () {
	wp_enqueue_style( 'microtec', get_stylesheet_directory_uri() . '/assets/css/microtec.css', [], filemtime( get_stylesheet_directory() . '/assets/css/microtec.css' ) );
	wp_enqueue_style( 'microtec-pages', get_stylesheet_directory_uri() . '/assets/css/mt-pages.css', [ 'microtec' ], filemtime( get_stylesheet_directory() . '/assets/css/mt-pages.css' ) );
} );

/**
 * Shop and product category pages: a sidebar (search, price filter, categories, best sellers)
 * on the left and the breadcrumb, title, sorting and product grid on the right.
 */
function microtec_is_catalog() {
	return function_exists( 'is_shop' ) && ( is_shop() || is_product_taxonomy() );
}

add_action( 'wp_enqueue_scripts', function () {
	// Shop pages, and the site search, which shows products as shop cards (search.php).
	if ( ! function_exists( 'is_woocommerce' ) || ! ( is_woocommerce() || is_search() ) ) {
		return;
	}
	$dir = get_stylesheet_directory();
	$uri = get_stylesheet_directory_uri();

	wp_enqueue_style( 'microtec-pages-fonts', 'https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap', [], null );
	wp_enqueue_style( 'microtec-shop', $uri . '/assets/css/mt-shop.css', [ 'microtec' ], filemtime( $dir . '/assets/css/mt-shop.css' ) );
}, 30 );

// Search popup from the header search icon (every page), and the Cart / Checkout / My account
// pages in the site's colours.
add_action( 'wp_enqueue_scripts', function () {
	$dir = get_stylesheet_directory();
	$uri = get_stylesheet_directory_uri();

	wp_enqueue_style( 'microtec-search', $uri . '/assets/css/mt-search.css', [ 'microtec' ], filemtime( $dir . '/assets/css/mt-search.css' ) );
	wp_enqueue_script( 'microtec-search', $uri . '/assets/js/mt-search.js', [], filemtime( $dir . '/assets/js/mt-search.js' ), true );
	wp_localize_script( 'microtec-search', 'mtSearch', [
		'home' => home_url( '/' ),
		'rest' => esc_url_raw( rest_url() ),
	] );

	if ( function_exists( 'is_cart' ) && ( is_cart() || is_checkout() || is_account_page() ) ) {
		wp_enqueue_style( 'microtec-checkout', $uri . '/assets/css/mt-checkout.css', [ 'microtec' ], filemtime( $dir . '/assets/css/mt-checkout.css' ) );
	}
}, 40 );

add_filter( 'body_class', function ( $classes ) {
	if ( microtec_is_catalog() || is_search() ) {
		$classes[] = 'mt-catalog';
	}
	return $classes;
} );

add_filter( 'loop_shop_columns', function () {
	return 3;
} );

// Open the two-column layout after WooCommerce's page wrapper (priority 10) and before the
// breadcrumb (20), so the breadcrumb sits in the right-hand column.
add_action( 'woocommerce_before_main_content', function () {
	if ( ! microtec_is_catalog() ) {
		return;
	}
	$widget = [
		'before_widget' => '<section class="mt-shop-widget %s">',
		'after_widget'  => '</section>',
		'before_title'  => '<h2 class="mt-shop-widget-title">',
		'after_title'   => '</h2>',
	];
	echo '<div class="mt-shop"><aside class="mt-shop-side">';
	the_widget( 'WC_Widget_Product_Search', [ 'title' => '' ], $widget );
	the_widget( 'WC_Widget_Price_Filter', [ 'title' => 'Filter by Price' ], $widget );
	the_widget( 'WC_Widget_Product_Categories', [ 'title' => 'Categories', 'count' => 1, 'hide_empty' => 1 ], $widget );
	the_widget( 'WC_Widget_Products', [ 'title' => 'Our Best Sellers', 'number' => 5, 'orderby' => 'sales', 'order' => 'desc' ], $widget );
	echo '</aside><div class="mt-shop-main">';
}, 15 );

add_action( 'woocommerce_after_main_content', function () {
	if ( microtec_is_catalog() ) {
		echo '</div></div>';
	}
}, 5 );

// The theme has no shop sidebar of its own; the layout above replaces it.
add_action( 'wp', function () {
	if ( microtec_is_catalog() ) {
		remove_action( 'woocommerce_sidebar', 'woocommerce_get_sidebar', 10 );
	}
} );

// Products sold on enquiry (no price set) show "Call for price" instead of an empty price.
add_filter( 'woocommerce_get_price_html', function ( $html, $product ) {
	if ( '' === $product->get_price() && ! $product->is_type( 'variable' ) ) {
		return '<span class="mt-call-price">Call for price</span>';
	}
	return $html;
}, 10, 2 );

// Category intros: category-intros/<slug>.html in this theme replaces the plain category
// description, so a range page can carry a list, an image and a call to action.
add_action( 'woocommerce_archive_description', function () {
	if ( ! is_product_category() ) {
		return;
	}
	$file = get_stylesheet_directory() . '/category-intros/' . sanitize_file_name( get_queried_object()->slug ) . '.html';
	if ( ! is_readable( $file ) ) {
		return;
	}
	remove_action( 'woocommerce_archive_description', 'woocommerce_taxonomy_archive_description', 10 );
	echo wp_kses_post( file_get_contents( $file ) );
}, 5 );

// Empty categories point visitors to the team rather than a dead end.
add_filter( 'gettext', function ( $text, $original, $domain ) {
	if ( 'woocommerce' === $domain && 'No products were found matching your selection.' === $original ) {
		return 'Products for this range are coming soon. Please contact us or call 03 9792 2243 for parts and availability.';
	}
	return $text;
}, 10, 3 );

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