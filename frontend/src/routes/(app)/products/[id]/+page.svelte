<script lang="ts">
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import { getProduct, type Product } from '$lib/services/products';
  import { getProductReviews, type Review } from '$lib/services/orders';
  import { cart } from '$lib/stores/cart';

  let loading = true;
  let error = '';
  let product: Product | null = null;
  const productId = Number($page.params.id);

  let reviews: Review[] = [];
  
  onMount(async () => {
    try {
      const [productData, reviewsData] = await Promise.all([
          getProduct(productId),
          getProductReviews(productId)
      ]);
      product = productData;
      reviews = reviewsData;
    } catch (e: any) {
      error = e.message || 'Failed to load product';
    } finally {
      loading = false;
    }
  });

  function addToCart() {
    if (product) {
      cart.addToCart(product);
    }
  }
</script>

<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
	{#if loading}
		<div class="flex justify-center py-20">
			<div
				class="animate-spin h-10 w-10 text-gray-900 rounded-full border-2 border-t-transparent border-gray-200"
			></div>
		</div>
	{:else if error}
		<div class="bg-red-50 text-red-700 p-6 rounded-lg border border-red-200 text-center">
			<h3 class="text-lg font-medium mb-2">Error</h3>
			<p>{error}</p>
			<a href="/" class="inline-block mt-4 text-indigo-600 hover:text-indigo-800 font-medium">
				&larr; Back to Shop
			</a>
		</div>
	{:else if product}
		<div class="lg:grid lg:grid-cols-2 lg:gap-x-12 lg:items-start">
			<!-- Image Gallery -->
			<div class="flex flex-col-reverse">
				<div
					class="w-full aspect-w-1 aspect-h-1 bg-gray-100 rounded-2xl overflow-hidden sm:aspect-w-2 sm:aspect-h-3 shadow-sm border border-gray-100"
				>
					{#if product.image_url}
						<img
							src={product.image_url}
							alt={product.name}
							class="w-full h-full object-center object-cover hover:scale-105 transition-transform duration-500"
						/>
					{:else}
						<div class="w-full h-full flex items-center justify-center text-gray-400">
							<span class="text-lg">No Image Available</span>
						</div>
					{/if}
				</div>
			</div>

			<!-- Product Info -->
			<div class="mt-10 px-4 sm:px-0 sm:mt-16 lg:mt-0">
				<nav class="flex mb-4" aria-label="Breadcrumb">
					<ol role="list" class="flex items-center space-x-2">
						<li>
							<a href="/" class="text-gray-400 hover:text-gray-500 text-sm">Home</a>
						</li>
						<li class="text-gray-300">/</li>
						<li>
							<span class="text-gray-500 text-sm font-medium"
								>{product.category_name || 'Category ' + product.category_id}</span
							>
						</li>
					</ol>
				</nav>

				<h1 class="text-4xl font-extrabold tracking-tight text-gray-900 mb-4">{product.name}</h1>

				<div class="mt-3">
					<h2 class="sr-only">Product information</h2>
					<p class="text-3xl text-gray-900 font-bold">${product.price}</p>
				</div>

				<div class="mt-6">
					<h3 class="sr-only">Description</h3>
					<div class="text-base text-gray-700 space-y-6 leading-relaxed">
						<p>{product.description || 'No description available for this product.'}</p>
					</div>
				</div>

				<div class="mt-8 border-t border-gray-200 pt-8">
					<div class="flex items-center justify-between mb-6">
						<span class="text-sm font-medium text-gray-500">Availability</span>
						<span
							class="{product.stock > 10
								? 'bg-green-100 text-green-800'
								: product.stock > 0
									? 'bg-yellow-100 text-yellow-800'
									: 'bg-red-100 text-red-800'} px-3 py-1 inline-flex text-sm font-semibold rounded-full"
						>
							{product.stock > 0 ? `${product.stock} in stock` : 'Out of Stock'}
						</span>
					</div>

					<button
						type="button"
						on:click={addToCart}
						disabled={product.stock === 0}
						class="w-full bg-black border border-transparent rounded-xl py-4 px-8 flex items-center justify-center text-lg font-medium text-white hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-900 disabled:bg-gray-300 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl transform active:scale-95"
					>
						{product.stock > 0 ? 'Add to Cart' : 'Out of Stock'}
					</button>

					<div class="mt-6 text-center">
						<a
							href="/"
							class="text-sm text-gray-500 hover:text-indigo-600 font-medium transition-colors"
						>
							&larr; Continue Shopping
						</a>
					</div>
				</div>

				<!-- Reviews Section -->
				<div class="mt-16 border-t border-gray-200 pt-10">
					<h3 class="text-2xl font-bold text-gray-900 mb-6">Customer Reviews</h3>
					{#if reviews.length === 0}
						<p class="text-gray-500 italic">No reviews yet. Be the first to review this product!</p>
					{:else}
						<div class="space-y-8">
							{#each reviews as review}
								<div class="border-b border-gray-100 pb-6">
									<div class="flex items-center mb-2">
										<div class="text-yellow-400 text-lg mr-2">
											{'★'.repeat(review.rating)}{'☆'.repeat(5 - review.rating)}
										</div>
										<span class="font-medium text-gray-900 mr-2"
											>{review.user_name || 'Anonymous'}</span
										>
										<span class="text-sm text-gray-500"
											>{new Date(review.created_at).toLocaleDateString()}</span
										>
									</div>
									<p class="text-gray-600">{review.comment}</p>
								</div>
							{/each}
						</div>
					{/if}
				</div>
			</div>
		</div>
	{/if}
</div>
