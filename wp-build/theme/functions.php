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
	// Contact Us: built from Elementor widgets too; styles keyed on mtc-* classes.
	wp_enqueue_style( 'microtec-contact', $uri . '/assets/css/mt-contact.css', [ 'microtec-guides' ], filemtime( $dir . '/assets/css/mt-contact.css' ) );
	wp_enqueue_script( 'microtec-contact', $uri . '/assets/js/mt-contact.js', [], filemtime( $dir . '/assets/js/mt-contact.js' ), true );
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

// 12 per page: four full rows of three, so no page ends on a lone card and the larger
// categories (LCDs, Overlays, Misc Crane Parts, Tadano Parts) still get page numbers.
add_filter( 'loop_shop_per_page', function () {
	return 12;
} );

// Pagination arrows with words, styled as pills in mt-shop.css.
add_filter( 'woocommerce_pagination_args', function ( $args ) {
	$args['prev_text'] = '<span aria-hidden="true">&larr;</span> Previous';
	$args['next_text'] = 'Next <span aria-hidden="true">&rarr;</span>';
	$args['end_size']  = 1;
	$args['mid_size']  = 1;
	return $args;
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
	microtec_stock_filter();
	the_widget( 'WC_Widget_Price_Filter', [ 'title' => 'Filter by Price' ], $widget );
	the_widget( 'WC_Widget_Product_Categories', [ 'title' => 'Categories', 'count' => 1, 'hide_empty' => 1 ], $widget );
	the_widget( 'WC_Widget_Products', [ 'title' => 'Our Best Sellers', 'number' => 5, 'orderby' => 'sales', 'order' => 'desc' ], $widget );
	echo '</aside><div class="mt-shop-main">';
}, 15 );

/**
 * Filter by Stock: "In Stock (n)" in the shop sidebar, as on the old site. Ticking it adds
 * ?stock=instock, which hides out-of-stock products (WooCommerce marks them with the
 * "outofstock" product visibility term, so variable products are covered too).
 */
function microtec_stock_query_on() {
	return isset( $_GET['stock'] ) && 'instock' === $_GET['stock']; // phpcs:ignore WordPress.Security.NonceVerification
}

add_action( 'woocommerce_product_query', function ( $q ) {
	if ( ! microtec_stock_query_on() ) {
		return;
	}
	$tax   = (array) $q->get( 'tax_query' );
	$tax[] = [
		'taxonomy' => 'product_visibility',
		'field'    => 'name',
		'terms'    => [ 'outofstock' ],
		'operator' => 'NOT IN',
	];
	$q->set( 'tax_query', $tax );
} );

function microtec_stock_filter() {
	$tax = [ [ 'taxonomy' => 'product_visibility', 'field' => 'name', 'terms' => [ 'outofstock', 'exclude-from-catalog' ], 'operator' => 'NOT IN' ] ];
	if ( is_product_taxonomy() ) {
		$term  = get_queried_object();
		$tax[] = [ 'taxonomy' => $term->taxonomy, 'field' => 'term_id', 'terms' => [ $term->term_id ] ];
	}
	$count = count( get_posts( [
		'post_type'      => 'product',
		'post_status'    => 'publish',
		'posts_per_page' => -1,
		'fields'         => 'ids',
		'tax_query'      => $tax, // phpcs:ignore WordPress.DB.SlowDBQuery
	] ) );

	$on  = microtec_stock_query_on();
	// Back to page 1, keeping the other filters (price, sorting).
	$url = remove_query_arg( [ 'stock', 'paged' ], get_pagenum_link( 1, false ) );
	$url = $on ? $url : add_query_arg( 'stock', 'instock', $url );

	printf(
		'<section class="mt-shop-widget mt-stock-filter"><h2 class="mt-shop-widget-title">Filter by Stock</h2>'
		. '<a class="mt-stock-option%s" href="%s" role="checkbox" aria-checked="%s"><span class="mt-stock-box" aria-hidden="true"></span>In Stock <span class="count">(%d)</span></a></section>',
		$on ? ' is-active' : '',
		esc_url( $url ),
		$on ? 'true' : 'false',
		(int) $count
	);
}

add_action( 'woocommerce_after_main_content', function () {
	if ( microtec_is_catalog() ) {
		echo '</div></div>';
	}
}, 5 );

// The theme has no shop sidebar of its own; the layout above replaces it.
add_action( 'wp', function () {
	if ( microtec_is_catalog() ) {
		remove_action( 'woocommerce_sidebar', 'woocommerce_get_sidebar', 10 );
		// WooCommerce's own count drops out whenever the URL carries a filter or sort order
		// (?stock=, ?orderby=, ?min_price=); this one is worked out from the query itself.
		remove_action( 'woocommerce_before_shop_loop', 'woocommerce_result_count', 20 );
		add_action( 'woocommerce_before_shop_loop', 'microtec_result_count', 20 );
	}
} );

// "Showing all 3 results" / "Showing 1–12 of 62 results", as WooCommerce words it.
function microtec_result_count() {
	global $wp_query;
	$total = (int) $wp_query->found_posts;
	if ( ! $total ) {
		return;
	}
	$per   = (int) $wp_query->get( 'posts_per_page' );
	$paged = max( 1, (int) get_query_var( 'paged' ) );
	echo '<p class="mt-result-count">';
	if ( 1 === $total ) {
		esc_html_e( 'Showing the single result', 'woocommerce' );
	} elseif ( $per < 1 || $total <= $per ) {
		/* translators: %d: total results */
		printf( esc_html( _n( 'Showing all %d result', 'Showing all %d results', $total, 'woocommerce' ) ), (int) $total );
	} else {
		$first = $per * ( $paged - 1 ) + 1;
		$last  = min( $total, $per * $paged );
		/* translators: 1: first result 2: last result 3: total results */
		printf( esc_html( _nx( 'Showing %1$d&ndash;%2$d of %3$d result', 'Showing %1$d&ndash;%2$d of %3$d results', $total, 'with first and last result', 'woocommerce' ) ), (int) $first, (int) $last, (int) $total );
	}
	echo '</p>';
}

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