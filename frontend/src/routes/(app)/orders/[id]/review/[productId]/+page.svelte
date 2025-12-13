<script lang="ts">
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { getOrder, submitReview, type Order, type OrderItem } from '$lib/services/orders';
  import { getProduct, type Product } from '$lib/services/products';

  const orderId = Number($page.params.id);
  const productId = Number($page.params.productId);

  let loading = true;
  let error = '';
  let order: Order | null = null;
  let product: Product | null = null;
  
  let rating = 5;
  let comment = '';
  let submitting = false;

  onMount(async () => {
    try {
      const [orderData, productData] = await Promise.all([
        getOrder(orderId),
        getProduct(productId)
      ]);
      order = orderData;
      product = productData;

      if (order.status !== 'completed') {
        throw new Error("Order is not completed");
      }
      
      const item = order.items.find(i => i.product_id === productId);
      if (!item) {
        throw new Error("Product not found in this order");
      }

    } catch (e: any) {
      error = e.message || 'Failed to load details';
    } finally {
      loading = false;
    }
  });

  async function handleSubmit() {
    if (!order || !product) return;
    
    submitting = true;
    try {
      await submitReview(orderId, productId, rating, comment);
      goto(`/products/${productId}`);
    } catch (e: any) {
      alert('Failed to submit review: ' + e.message);
    } finally {
      submitting = false;
    }
  }

  function handleCancel() {
    goto(`/orders/${orderId}`);
  }
</script>

<div class="min-h-screen py-16 px-4 sm:px-6 lg:px-8">
	<div class="max-w-xl mx-auto">
		{#if loading}
			<div class="flex justify-center py-20">
				<div
					class="animate-spin h-6 w-6 text-gray-900 rounded-full border-2 border-t-transparent border-gray-200"
				></div>
			</div>
		{:else if error}
			<div class="text-center py-12">
				<p class="text-red-500 mb-4">{error}</p>
				<a
					href="/orders/{orderId}"
					class="text-sm font-medium text-gray-900 border-b border-gray-900 pb-0.5 hover:text-gray-600 hover:border-gray-600 transition-colors"
				>
					Return to Order
				</a>
			</div>
		{:else if product && order}
			<div class="space-y-12 animate-in fade-in slide-in-from-bottom-4 duration-500">
				<!-- Minimal Header -->
				<div class="text-center space-y-2">
					<h1 class="text-3xl font-bold text-gray-900 tracking-tight">Write a Review</h1>
					<p class="text-gray-500">How was your product?</p>
				</div>

				<!-- Product Context -->
				<div class="flex items-center gap-4 py-4 border-b border-gray-100">
					<div class="h-16 w-16 flex-shrink-0 bg-gray-50 rounded-lg overflow-hidden">
						{#if product.image_url}
							<img
								src={product.image_url}
								alt={product.name}
								class="h-full w-full object-cover grayscale opacity-80 hover:grayscale-0 transition-all"
							/>
						{:else}
							<div class="h-full w-full flex items-center justify-center text-gray-300 text-xs">
								No Img
							</div>
						{/if}
					</div>
					<div>
						<h2 class="text-lg font-medium text-gray-900">{product.name}</h2>
						<p class="text-sm text-gray-500">${product.price}</p>
					</div>
				</div>

				<div class="space-y-10">
					<!-- Star Rating -->
					<div class="flex flex-col items-center gap-4">
						<div class="flex gap-1">
							{#each [1, 2, 3, 4, 5] as star}
								<button
									type="button"
									class="p-2 transition-transform hover:-translate-y-1 focus:outline-none"
									on:click={() => (rating = star)}
									aria-label="Rate {star} of 5 stars"
								>
									<svg
										class="w-8 h-8 {rating >= star
											? 'text-gray-900 fill-current'
											: 'text-gray-200'}"
										fill="currentColor"
										viewBox="0 0 24 24"
										stroke="currentColor"
										stroke-width={rating >= star ? '0' : '1.5'}
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"
										/>
									</svg>
								</button>
							{/each}
						</div>
						<span class="text-sm font-medium text-gray-500">
							{#if rating === 5}Excellent{:else if rating === 4}Good{:else if rating === 3}Average{:else if rating === 2}Fair{:else}Poor{/if}
						</span>
					</div>

					<!-- Comment Area -->
					<div class="space-y-4">
						<label for="comment" class="block text-sm font-medium text-gray-700"
							>Write your review</label
						>
						<div class="relative">
							<textarea
								id="comment"
								rows="5"
								bind:value={comment}
								class="block w-full bg-gray-50 border border-gray-200 rounded-xl p-4 text-gray-900 placeholder-gray-400 focus:ring-2 focus:ring-gray-900 focus:border-transparent focus:bg-white transition-all resize-none text-base leading-relaxed"
								placeholder="What did you like or dislike? What should other shoppers know?"
							></textarea>
							<div class="absolute bottom-3 right-3 text-xs text-gray-400 pointer-events-none">
								{comment.length} characters
							</div>
						</div>
					</div>
				</div>

				<!-- Action Buttons -->
				<div class="flex flex-col gap-3">
					<button
						type="button"
						class="w-full py-4 bg-gray-900 text-white text-sm font-bold tracking-widest uppercase rounded-lg hover:bg-black transition-colors disabled:opacity-70 disabled:cursor-not-allowed"
						on:click={handleSubmit}
						disabled={submitting}
					>
						{submitting ? 'Submitting...' : 'Submit Review'}
					</button>
					<button
						type="button"
						class="w-full py-4 text-gray-500 text-sm font-medium hover:text-gray-900 transition-colors"
						on:click={handleCancel}
					>
						Cancel
					</button>
				</div>
			</div>
		{/if}
	</div>
</div>
