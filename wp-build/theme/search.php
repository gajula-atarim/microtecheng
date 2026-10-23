<?php
/**
 * Site search (the header search icon): matching products as shop cards, then matching pages
 * and guides as cards. Product-only searches (the shop sidebar) use WooCommerce's own results.
 */

defined( 'ABSPATH' ) || exit;

get_header();

$term = get_search_query();

$products = new WP_Query( [
	'post_type'      => 'product',
	'post_status'    => 'publish',
	's'              => $term,
	'posts_per_page' => 48,
] );

$page_results = new WP_Query( [
	'post_type'      => 'page',
	'post_status'    => 'publish',
	's'              => $term,
	'posts_per_page' => 12,
	'post__not_in'   => array_filter( [
		(int) get_option( 'woocommerce_cart_page_id' ),
		(int) get_option( 'woocommerce_checkout_page_id' ),
		(int) get_option( 'woocommerce_myaccount_page_id' ),
	] ),
] );

/**
 * Page excerpt without the breadcrumb and repeated title the built pages start with
 * ("Home/Our Services/Load Systems Load Systems ...").
 */
function microtec_search_excerpt( $post ) {
	// Built from the saved text, not get_the_excerpt(), which renders the whole Elementor page.
	$raw   = '' !== $post->post_excerpt ? $post->post_excerpt : strip_shortcodes( $post->post_content );
	$text  = trim( preg_replace( '/\s+/', ' ', wp_strip_all_tags( $raw ) ) );
	$title = get_the_title( $post );
	if ( 0 === strpos( $text, 'Home/' ) ) {
		$first = strpos( $text, $title );
		$again = false === $first ? false : strpos( $text, $title, $first + strlen( $title ) );
		$text  = false === $again ? '' : trim( substr( $text, $again + strlen( $title ) ) );
	}
	return wp_trim_words( $text, 22, '…' );
}
?>
<main id="content" class="site-main mt-search-page">
	<div class="mt-shop mt-search">
		<header class="mt-search-head">
			<nav class="woocommerce-breadcrumb"><a href="<?php echo esc_url( home_url( '/' ) ); ?>">Home</a>&nbsp;/&nbsp;Search</nav>
			<h1 class="mt-search-title">
				<?php echo $term ? 'Search results: “' . esc_html( $term ) . '”' : 'Search'; ?>
			</h1>
			<form role="search" method="get" class="woocommerce-product-search mt-search-form" action="<?php echo esc_url( home_url( '/' ) ); ?>">
				<label class="screen-reader-text" for="mt-search-field">Search for:</label>
				<input type="search" id="mt-search-field" class="search-field" placeholder="Search products, parts and guides…" value="<?php echo esc_attr( $term ); ?>" name="s">
				<button type="submit">Search</button>
			</form>
		</header>

		<?php if ( $products->have_posts() ) : ?>
			<section class="mt-search-section">
				<h2 class="mt-search-section-title">Products <span><?php echo (int) $products->found_posts; ?></span></h2>
				<?php
				wc_set_loop_prop( 'columns', 4 );
				woocommerce_product_loop_start();
				while ( $products->have_posts() ) {
					$products->the_post();
					wc_get_template_part( 'content', 'product' );
				}
				woocommerce_product_loop_end();
				wp_reset_postdata();
				?>
				<?php if ( $products->found_posts > $products->post_count ) : ?>
					<p class="mt-search-more"><a href="<?php echo esc_url( add_query_arg( [ 's' => $term, 'post_type' => 'product' ], home_url( '/' ) ) ); ?>">View all <?php echo (int) $products->found_posts; ?> products →</a></p>
				<?php endif; ?>
			</section>
		<?php endif; ?>

		<?php if ( $page_results->have_posts() ) : ?>
			<section class="mt-search-section">
				<h2 class="mt-search-section-title">Pages &amp; guides <span><?php echo (int) $page_results->found_posts; ?></span></h2>
				<div class="mt-search-pages">
					<?php
					while ( $page_results->have_posts() ) :
						$page_results->the_post();
						$parent  = wp_get_post_parent_id( get_the_ID() );
						$section = $parent ? get_the_title( $parent ) : 'Page';
						$excerpt = microtec_search_excerpt( get_post() );
						?>
						<a class="mt-search-card" href="<?php the_permalink(); ?>">
							<span class="mt-search-card-kicker"><?php echo esc_html( $section ); ?></span>
							<span class="mt-search-card-title"><?php the_title(); ?></span>
							<?php if ( $excerpt ) : ?>
								<span class="mt-search-card-text"><?php echo esc_html( $excerpt ); ?></span>
							<?php endif; ?>
							<span class="mt-search-card-link">View page →</span>
						</a>
					<?php endwhile; ?>
				</div>
				<?php wp_reset_postdata(); ?>
			</section>
		<?php endif; ?>

		<?php if ( ! $products->found_posts && ! $page_results->found_posts ) : ?>
			<div class="mt-search-empty">
				<h2>No results<?php echo $term ? ' for “' . esc_html( $term ) . '”' : ''; ?></h2>
				<p>Try a different word, a part number or a brand, or browse the <a href="<?php echo esc_url( home_url( '/products/' ) ); ?>">product range</a>. For parts and availability, <a href="<?php echo esc_url( home_url( '/contact/' ) ); ?>">contact us</a> or call <a href="tel:0397922243">03 9792 2243</a>.</p>
			</div>
		<?php endif; ?>
	</div>
</main>
<?php
get_footer();
