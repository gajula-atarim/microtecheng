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
	if ( ! function_exists( 'is_woocommerce' ) || ! ( is_woocommerce() || is_search() || is_page( 'wishlist' ) ) ) {
		return;
	}
	$dir = get_stylesheet_directory();
	$uri = get_stylesheet_directory_uri();

	wp_enqueue_style( 'microtec-pages-fonts', 'https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap', [], null );
	wp_enqueue_style( 'microtec-shop', $uri . '/assets/css/mt-shop.css', [ 'microtec' ], filemtime( $dir . '/assets/css/mt-shop.css' ) );
	// Product page and wishlist page: quantity buttons, wishlist, copy-link sharing.
	if ( is_product() || is_page( 'wishlist' ) ) {
		wp_enqueue_script( 'microtec-product', $uri . '/assets/js/mt-product.js', [], filemtime( $dir . '/assets/js/mt-product.js' ), true );
		wp_localize_script( 'microtec-product', 'mtProduct', [
			'rest'     => esc_url_raw( rest_url() ),
			'wishlist' => home_url( '/wishlist/' ),
			'shop'     => home_url( '/products/' ),
			'ship'     => WC_AJAX::get_endpoint( 'mt_shipping_quote' ),
		] );
	}
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

/* ---- Product page: savings, stock, wishlist and sharing (as on the old site) ---- */

// Percentage saved on a sale product (the largest across a variable product's options).
function microtec_sale_percent( $product ) {
	if ( ! $product || ! $product->is_on_sale() ) {
		return 0;
	}
	$items = $product->is_type( 'variable' ) ? array_filter( array_map( 'wc_get_product', $product->get_children() ) ) : [ $product ];
	$best  = 0;
	foreach ( $items as $item ) {
		$reg  = (float) $item->get_regular_price();
		$sale = (float) $item->get_sale_price();
		if ( $reg > 0 && $sale > 0 && $sale < $reg ) {
			$best = max( $best, (int) round( ( $reg - $sale ) / $reg * 100 ) );
		}
	}
	return $best;
}

// Sale badge: "19% OFF" instead of "Sale!".
add_filter( 'woocommerce_sale_flash', function ( $html, $post, $product ) {
	$pct = microtec_sale_percent( $product );
	return $pct ? '<span class="onsale">' . esc_html( sprintf( '%d%% OFF', $pct ) ) . '</span>' : $html;
}, 10, 3 );

// Under the price: what the customer saves, and whether it is in stock.
add_action( 'woocommerce_single_product_summary', function () {
	global $product;
	$save = '';
	if ( $product->is_type( 'simple' ) && $product->is_on_sale() ) {
		$reg  = (float) $product->get_regular_price();
		$sale = (float) $product->get_sale_price();
		if ( $reg > $sale && $sale > 0 ) {
			$save = sprintf( '<span class="mt-save">Save %s (%d%%)</span>', wc_price( $reg - $sale ), (int) round( ( $reg - $sale ) / $reg * 100 ) );
		}
	}
	$stock = $product->is_in_stock()
		? '<span class="mt-stock is-in">In stock</span>'
		: '<span class="mt-stock is-out">Out of stock</span>';
	echo '<div class="mt-price-meta">' . $save . $stock . '</div>'; // phpcs:ignore WordPress.Security.EscapeOutput
}, 11 );

// Wishlist button (saved in the visitor's browser; listed on /wishlist/) and share links.
add_action( 'woocommerce_single_product_summary', function () {
	global $product;
	$url   = rawurlencode( get_permalink( $product->get_id() ) );
	$title = rawurlencode( $product->get_name() );
	$img   = rawurlencode( (string) wp_get_attachment_url( $product->get_image_id() ) );
	$icon  = function ( $d, $stroke = false ) {
		return $stroke
			? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' . $d . '</svg>'
			: '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">' . $d . '</svg>';
	};
	$links = [
		[ 'Facebook', 'https://www.facebook.com/sharer/sharer.php?u=' . $url, $icon( '<path d="M13.5 21v-7.5h2.6l.4-3h-3V8.6c0-.9.3-1.5 1.5-1.5h1.6V4.4c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 4v2.2H7.8v3h2.6V21z"/>' ) ],
		[ 'X', 'https://twitter.com/intent/tweet?url=' . $url . '&text=' . $title, $icon( '<path d="M17.8 3h3l-6.6 7.6L22 21h-6.1l-4.8-6.3L5.6 21h-3l7.1-8.1L2.2 3h6.2l4.3 5.7zm-1 16.2h1.7L7.3 4.7H5.5z"/>' ) ],
		[ 'LinkedIn', 'https://www.linkedin.com/sharing/share-offsite/?url=' . $url, $icon( '<path d="M6.5 8.6H3.2V20h3.3zM4.9 3.4a1.9 1.9 0 1 0 0 3.8 1.9 1.9 0 0 0 0-3.8zM20.8 13.7c0-3.1-1.7-5.3-4.5-5.3-1.7 0-2.8.9-3.2 1.7V8.6H9.9V20h3.3v-6c0-1.6.7-2.7 2.1-2.7s1.9 1.1 1.9 2.7v6h3.3z"/>' ) ],
		[ 'Pinterest', 'https://pinterest.com/pin/create/button/?url=' . $url . '&media=' . $img . '&description=' . $title, $icon( '<path d="M12 2a10 10 0 0 0-3.6 19.3c-.1-.8-.2-2 0-2.9l1.2-5s-.3-.6-.3-1.5c0-1.4.8-2.4 1.8-2.4.9 0 1.3.7 1.3 1.5 0 .9-.6 2.2-.9 3.4-.2 1 .5 1.9 1.6 1.9 1.9 0 3.3-2 3.3-4.9 0-2.5-1.8-4.3-4.4-4.3-3 0-4.8 2.3-4.8 4.6 0 .9.3 1.9.8 2.4l.1.4-.3 1.1c0 .2-.2.3-.4.2-1.3-.6-2.1-2.5-2.1-4.1 0-3.3 2.4-6.4 7-6.4 3.7 0 6.5 2.6 6.5 6.1 0 3.7-2.3 6.6-5.5 6.6-1.1 0-2.1-.6-2.4-1.2l-.7 2.5c-.2.9-.9 2.1-1.3 2.8A10 10 0 1 0 12 2z"/>' ) ],
		[ 'Email', 'mailto:?subject=' . $title . '&body=' . $url, $icon( '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>', true ) ],
	];
	echo '<div class="mt-product-extras">';
	printf(
		'<button type="button" class="mt-wish" data-id="%d" aria-pressed="false"><span class="mt-wish-heart" aria-hidden="true"></span><span class="mt-wish-label">Add to wishlist</span></button>',
		(int) $product->get_id()
	);
	echo '<div class="mt-share"><span class="mt-share-label">Share</span>';
	foreach ( $links as $l ) {
		printf(
			'<a class="mt-share-link" href="%s" target="_blank" rel="noopener" aria-label="Share on %s" title="%s">%s</a>',
			esc_url( $l[1] ),
			esc_attr( $l[0] ),
			esc_attr( $l[0] ),
			$l[2] // phpcs:ignore WordPress.Security.EscapeOutput
		);
	}
	printf(
		'<button type="button" class="mt-share-link mt-share-copy" data-url="%s" aria-label="Copy link" title="Copy link">%s</button>',
		esc_url( get_permalink( $product->get_id() ) ),
		$icon( '<path d="M10 13a5 5 0 0 0 7.1 0l2.8-2.8a5 5 0 0 0-7.1-7.1L11.5 4.4"/><path d="M14 11a5 5 0 0 0-7.1 0l-2.8 2.8a5 5 0 0 0 7.1 7.1l1.3-1.3"/>', true ) // phpcs:ignore WordPress.Security.EscapeOutput
	);
	echo '</div></div>';
}, 35 );

/* ---- Product page: shipping calculator (as on the old site) ----
   Quotes this product × quantity to a country and post code with WooCommerce's own shipping
   zones and methods, so the figures match the cart and checkout. */

// Australian state from a post code, so zones set up by state match as well as by post code.
function microtec_au_state( $postcode ) {
	$pc = (int) $postcode;
	if ( ( $pc >= 200 && $pc <= 299 ) || ( $pc >= 2600 && $pc <= 2618 ) || ( $pc >= 2900 && $pc <= 2920 ) ) {
		return 'ACT';
	}
	if ( $pc >= 800 && $pc <= 999 ) {
		return 'NT';
	}
	if ( ( $pc >= 1000 && $pc <= 2999 ) ) {
		return 'NSW';
	}
	if ( ( $pc >= 3000 && $pc <= 3999 ) || ( $pc >= 8000 && $pc <= 8999 ) ) {
		return 'VIC';
	}
	if ( ( $pc >= 4000 && $pc <= 4999 ) || ( $pc >= 9000 && $pc <= 9999 ) ) {
		return 'QLD';
	}
	if ( $pc >= 5000 && $pc <= 5999 ) {
		return 'SA';
	}
	if ( $pc >= 6000 && $pc <= 6999 ) {
		return 'WA';
	}
	if ( $pc >= 7000 && $pc <= 7999 ) {
		return 'TAS';
	}
	return '';
}

add_action( 'woocommerce_single_product_summary', function () {
	global $product;
	if ( ! $product || ! $product->is_purchasable() || ( ! $product->is_type( 'variable' ) && ! $product->needs_shipping() ) ) {
		return;
	}
	$countries = WC()->countries->get_shipping_countries();
	if ( ! $countries ) {
		return;
	}
	$default = isset( $countries['AU'] ) ? 'AU' : WC()->countries->get_base_country();
	echo '<div class="mt-ship" data-product="' . (int) $product->get_id() . '">';
	echo '<h3 class="mt-ship-title"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 6h11v10H3zM14 9h4l3 3.5V16h-7"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17.5" cy="17.5" r="1.8"/></svg>Calculate shipping</h3>';
	echo '<form class="mt-ship-form" novalidate>';
	echo '<label class="screen-reader-text" for="mt-ship-qty">Quantity</label><input id="mt-ship-qty" class="mt-ship-qty" type="number" name="qty" min="1" step="1" value="1" placeholder="Qty" inputmode="numeric">';
	echo '<label class="screen-reader-text" for="mt-ship-country">Country</label><select id="mt-ship-country" class="mt-ship-country" name="country">';
	foreach ( $countries as $code => $name ) {
		printf( '<option value="%s"%s>%s</option>', esc_attr( $code ), selected( $code, $default, false ), esc_html( $name ) );
	}
	echo '</select>';
	echo '<label class="screen-reader-text" for="mt-ship-postcode">Post code</label><input id="mt-ship-postcode" class="mt-ship-postcode" type="text" name="postcode" placeholder="Post code" autocomplete="postal-code" inputmode="numeric" maxlength="12">';
	echo '<button type="submit" class="mt-ship-btn">Calculate</button>';
	echo '</form><div class="mt-ship-result" aria-live="polite"></div></div>';
}, 32 );

// ?wc-ajax=mt_shipping_quote — runs as a front-end request, so WooCommerce's session and cart
// are loaded for the shipping methods that look at them.
add_action( 'wc_ajax_mt_shipping_quote', function () {
	$contact = 'Call <a href="tel:0397922243">03 9792 2243</a> or email <a href="mailto:enquiries@microteceng.com.au">enquiries@microteceng.com.au</a> and we&rsquo;ll quote shipping for you.';
	// phpcs:disable WordPress.Security.NonceVerification.Recommended -- read-only quote.
	$product_id   = isset( $_GET['product_id'] ) ? absint( $_GET['product_id'] ) : 0;
	$variation_id = isset( $_GET['variation_id'] ) ? absint( $_GET['variation_id'] ) : 0;
	$qty          = isset( $_GET['qty'] ) ? max( 1, min( 999, absint( $_GET['qty'] ) ) ) : 1;
	$country      = isset( $_GET['country'] ) ? strtoupper( sanitize_text_field( wp_unslash( $_GET['country'] ) ) ) : '';
	$postcode     = isset( $_GET['postcode'] ) ? sanitize_text_field( wp_unslash( $_GET['postcode'] ) ) : '';
	// phpcs:enable

	$product = $variation_id ? wc_get_product( $variation_id ) : wc_get_product( $product_id );
	if ( ! $product || ( $variation_id && $product->get_parent_id() !== $product_id ) || ! $product->is_purchasable() ) {
		wp_send_json_error( [ 'message' => 'This product can&rsquo;t be quoted online. ' . $contact ] );
	}
	if ( $product->is_type( 'variable' ) ) {
		wp_send_json_error( [ 'message' => 'Choose an option above first, then calculate shipping.' ] );
	}
	if ( ! $product->needs_shipping() ) {
		wp_send_json_success( [ 'rates' => [], 'message' => 'No shipping needed for this item.' ] );
	}
	$countries = WC()->countries->get_shipping_countries();
	if ( ! isset( $countries[ $country ] ) ) {
		wp_send_json_error( [ 'message' => 'We don&rsquo;t ship to that country online. ' . $contact ] );
	}
	$postcode = wc_format_postcode( $postcode, $country );
	// WooCommerce has no Australian post code pattern, so check for four digits here.
	if ( '' === $postcode || ! WC_Validation::is_postcode( $postcode, $country ) || ( 'AU' === $country && ! preg_match( '/^\d{4}$/', $postcode ) ) ) {
		wp_send_json_error( [ 'message' => 'Please check the post code.', 'field' => 'postcode' ] );
	}

	$price   = (float) wc_get_price_excluding_tax( $product );
	$total   = $price * $qty;
	$package = [
		'contents'        => [
			'mt_quote' => [
				'key'               => 'mt_quote',
				'product_id'        => $variation_id ? $product_id : $product->get_id(),
				'variation_id'      => $variation_id,
				'variation'         => $variation_id ? $product->get_variation_attributes() : [],
				'quantity'          => $qty,
				'data'              => $product,
				'line_total'        => $total,
				'line_tax'          => 0,
				'line_subtotal'     => $total,
				'line_subtotal_tax' => 0,
			],
		],
		'contents_cost'   => $total,
		'applied_coupons' => [],
		'user'            => [ 'ID' => get_current_user_id() ],
		'destination'     => [
			'country'   => $country,
			'state'     => 'AU' === $country ? microtec_au_state( $postcode ) : '',
			'postcode'  => $postcode,
			'city'      => '',
			'address'   => '',
			'address_1' => '',
			'address_2' => '',
		],
		'cart_subtotal'   => $total,
	];

	$rates = [];
	if ( wc_shipping_enabled() ) {
		// Its own package key, so the customer's cart shipping stays as it was.
		$result = WC()->shipping()->calculate_shipping_for_package( $package, 'mt_quote' );
		foreach ( (array) ( $result['rates'] ?? [] ) as $rate ) {
			$cost    = (float) $rate->get_cost() + (float) array_sum( (array) $rate->get_taxes() );
			$rates[] = [
				'label' => wp_strip_all_tags( $rate->get_label() ),
				'cost'  => $cost > 0 ? html_entity_decode( wp_strip_all_tags( wc_price( $cost ) ) ) : 'Free',
			];
		}
	}
	if ( ! $rates ) {
		wp_send_json_success( [ 'rates' => [], 'message' => 'We don&rsquo;t have an online shipping rate for ' . esc_html( $postcode ) . ' yet. ' . $contact ] );
	}
	wp_send_json_success( [
		'rates' => $rates,
		'note'  => sprintf( 'Estimate for %d &times; to %s, %s. Shipping is confirmed at checkout.', $qty, esc_html( $postcode ), esc_html( $countries[ $country ] ) ),
	] );
} );

// "Others Also Bought" under the product (as on the old site), from the product's cross-sells.
// The same products also appear as WooCommerce's cross-sells on the cart page.
add_action( 'woocommerce_after_single_product_summary', function () {
	global $product;
	if ( ! $product ) {
		return;
	}
	$items = array_filter( array_map( 'wc_get_product', $product->get_cross_sell_ids() ), function ( $p ) {
		return $p && $p->is_visible();
	} );
	if ( ! $items ) {
		return;
	}
	wc_set_loop_prop( 'name', 'also-bought' );
	wc_set_loop_prop( 'columns', 4 );
	echo '<section class="upsells products mt-also-bought"><h2>Others Also Bought</h2>';
	woocommerce_product_loop_start();
	foreach ( $items as $item ) {
		$GLOBALS['post'] = get_post( $item->get_id() ); // phpcs:ignore WordPress.WP.GlobalVariablesOverride
		setup_postdata( $GLOBALS['post'] );
		wc_get_template_part( 'content', 'product' );
	}
	woocommerce_product_loop_end();
	echo '</section>';
	wp_reset_postdata();
}, 15 );

/* ---- Redirects from the old store (www.microteceng.com.au, Neto) ----
   Old product addresses don't always match the product (e.g. /kato-ms-15-acs-graphic-lcd was the
   Kobelco tile), so each maps to a product ID rather than a slug. Runs before WordPress's own
   404 "guess", which would send some of them to the wrong product. */
function microtec_old_site_target( $path ) {
	$products = [
		'aml-ca' => 691, 'anemometer' => 648, 'cups-to-suit-lsi-anemometer' => 649,
		'battery-lithium-d-size-3.6v' => 650, 'brass-adapter-bush' => 651, 'brass-gear-for-kato-reeler' => 579,
		'bronto-skylift-screen-overlay' => 692, 'circular-bubble-level-4-deg-chrome-plated-aluminiu' => 627,
		'circular-bubble-level-4-deg-chrome-plated-aluminium' => 627, 'cobo-cls-lcd-display' => 499,
		'cobo-3b6-acq-mac-25-cable-reeler-please-call-for-p' => 500, 'cobo-3b6-lcd-display-older-metal-case' => 501,
		'eproms' => 580, 'tera-7-display' => 502, 'tadano-length-cable-price-per-meter' => 581,
		'kato-ms-16-acs-lcd-display-tile~262' => 609, 'kato-ms-10-acs-lcd-display-tile-99960462010' => 610,
		'kato-ms-16-acs-lcd-display-tile~261' => 608, 'kato-ms-16-display-push-buttons' => 611, 'kato-ms16-lcd' => 693,
		'kato-ms-15-acs-graphic-lcd' => 607, 'kobelco-overlay-rk160m-2-fly-jib' => 694,
		'kobelco-overlay-rk70m-2-no-fly-jib' => 695, 'kobelco-overlay-rk70m-2' => 696, 'l2-b-overlay' => 697,
		'lcd-display' => 582, 'lcd-tile-robway-1502-1445' => 612, 'level-bubble-3cm-6-deg' => 628,
		'inclinometer' => 652, 'liebherr-membrane-keypad-overlay' => 698, 'light-control-module' => 710,
		'ms16-kato-overlay' => 699, 'overlay-aml-k' => 700, 'plug-base-relay-5a-12v-24v-dc' => 657,
		'pots-10-turn' => 503, 'pressure-transducer' => 504, 'radio-control-systems' => 653,
		'robway-1502-overlay' => 701, 'sauer-danfoss-157b4735-proportional-solenoid' => 569,
		'scanreco-g5-antenna' => 654, 'servo-pots~239' => 658, 'switch-atb-microtec-battery-powered' => 655,
		'tadano-overlay' => 702, 'tadano-aml-k-lcd' => 613, 'tadano-aml-la-replacement-overlay' => 703,
		'tadano-aml-lc-replacement-overlay' => 704, 'tadano-aml-le-replacement-overlay' => 705,
		'tadano-aml-m1-replacement-overlay' => 706, 'tadano-aml-m1-lcd-tile-display' => 618,
		'tadano-aml-m2-replacement-overlay' => 707, 'tadano-aml-m2-lcd-tile-display' => 615,
		'tadano-lcd-control-panel-replacement' => 619, 'tadano-exchange-load-cell-a' => 656,
		'tadano-faun-10.4-touch-screen' => 620, 'lcd-aml-l-replacement' => 622, 'tadano-length-cable' => 708,
		'length-potentiometer' => 709, 'thiess-spec-latching-light-control-module' => 711,
	];
	$categories = [
		'cobo' => 'cobo-components', 'cobo-components' => 'cobo-components', 'hetronic' => 'hetronic',
		'hydraulic-parts' => 'hydraulic-parts', 'kato-parts' => 'kato-parts', 'lcds' => 'lcds',
		'level-bubbles' => 'level-bubbles', 'miscellaneous-crane-parts' => 'misc-crane-parts',
		'overlays' => 'overlays', 'tadano-parts' => 'tadano-parts',
		'external-warning-lights-accessories' => 'warning-lights-accessories',
	];
	$pages = [
		'page/design-services' => 111, 'page/radio-control-systems' => 355, 'page/system-intergration' => 354,
		'page/system-integration' => 354, 'page/bronto-lcd-display-keypad-overlay-replacement' => 757,
		'page/tadano-cranes-technical-information' => 756, 'page/job-information-sheet' => 52,
		'page/external-warning-light-and-light-control-module-mk' => 51, 'page/about-us' => 49,
		'page/contact-us' => 52, 'robway' => 8,
	];
	if ( isset( $products[ $path ] ) ) {
		return get_permalink( $products[ $path ] );
	}
	if ( isset( $categories[ $path ] ) ) {
		$link = get_term_link( $categories[ $path ], 'product_cat' );
		return is_wp_error( $link ) ? '' : $link;
	}
	if ( isset( $pages[ $path ] ) ) {
		return get_permalink( $pages[ $path ] );
	}
	// Neto's short product addresses: /~266 or /some-name~266 (266 = the product's SKU).
	if ( preg_match( '/~(\d+)$/', $path, $m ) ) {
		$id = wc_get_product_id_by_sku( $m[1] );
		return $id ? get_permalink( $id ) : '';
	}
	// Other old /page/<name>/ addresses: a page of the same name on this site, else the guides hub
	// for the guide pages (/page/<name>/~-118 and the like).
	if ( 0 === strpos( $path, 'page/' ) ) {
		$name  = strtok( substr( $path, 5 ), '/' );
		$found = get_posts( [ 'name' => $name, 'post_type' => 'page', 'post_status' => 'publish', 'numberposts' => 1, 'fields' => 'ids' ] );
		if ( $found ) {
			return get_permalink( $found[0] );
		}
		if ( isset( $pages[ 'page/' . $name ] ) ) {
			return get_permalink( $pages[ 'page/' . $name ] );
		}
	}
	return '';
}
add_action( 'template_redirect', function () {
	$path = strtolower( trim( rawurldecode( (string) wp_parse_url( $_SERVER['REQUEST_URI'] ?? '', PHP_URL_PATH ) ), '/' ) ); // phpcs:ignore WordPress.Security.ValidatedSanitizedInput
	// Only addresses this site doesn't serve itself (an image's attachment page can share an old name).
	if ( '' === $path || ( ! is_404() && ! is_attachment() ) ) {
		return;
	}
	$url = microtec_old_site_target( $path );
	if ( $url ) {
		wp_safe_redirect( $url, 301, 'Microtec' );
		exit;
	}
}, 1 );

// [mt_wishlist]: the wishlist page; mt-product.js fills it from the visitor's saved products.
add_shortcode( 'mt_wishlist', function () {
	return '<div class="mt-wishlist" aria-live="polite"><p class="mt-wishlist-empty">Loading your wishlist&hellip;</p></div>';
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