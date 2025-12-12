<script lang="ts">
  import { cart } from '$lib/stores/cart';
  import { request } from '$lib/api';
  import { goto } from '$app/navigation';

  let shippingAddress = '';
  let loading = false;
  let error = '';

  async function placeOrder() {
    if (!shippingAddress) {
      error = "Shipping address is required";
      return;
    }

    loading = true;
    error = '';

    try {
      await request('/orders/', {
        method: 'POST',
        body: JSON.stringify({ shipping_address: shippingAddress })
      });
      // Clear cart locally (though server handles it, store should re-fetch)
      await cart.fetchCart();
      goto('/orders');
    } catch (e: any) {
      error = e.message || "Failed to place order";
    } finally {
      loading = false;
    }
  }
</script>

<div class="max-w-3xl mx-auto space-y-8">
	<h1 class="text-3xl font-bold text-gray-900">Checkout</h1>

	{#if $cart && $cart.items.length > 0}
		<div class="bg-white shadow overflow-hidden sm:rounded-lg">
			<div class="px-4 py-5 sm:px-6">
				<h3 class="text-lg leading-6 font-medium text-gray-900">Order Summary</h3>
			</div>
			<div class="border-t border-gray-200">
				<dl>
					{#each $cart.items as item}
						<div class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
							<dt class="text-sm font-medium text-gray-500">
								{item.product.name} (x{item.quantity})
							</dt>
							<dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2 text-right">
								${item.product.price * item.quantity}
							</dd>
						</div>
					{/each}
					<div
						class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6 border-t border-gray-200"
					>
						<dt class="text-base font-bold text-gray-900">Total</dt>
						<dd class="mt-1 text-base font-bold text-gray-900 sm:mt-0 sm:col-span-2 text-right">
							${$cart.total_price}
						</dd>
					</div>
				</dl>
			</div>
		</div>

		<!-- Shipping Form -->
		<div class="bg-white shadow sm:rounded-lg p-6">
			<label for="address" class="block text-sm font-medium text-gray-700">Shipping Address</label>
			<div class="mt-1">
				<textarea
					id="address"
					name="address"
					rows="3"
					class="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border border-gray-300 rounded-md p-2"
					placeholder="123 Main St, City, Country"
					bind:value={shippingAddress}
				></textarea>
			</div>
			{#if error}
				<p class="mt-2 text-sm text-red-600">{error}</p>
			{/if}
			<div class="mt-6">
				<button
					type="button"
					class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
					on:click={placeOrder}
					disabled={loading}
				>
					{loading ? 'Processing...' : 'Place Order'}
				</button>
			</div>
		</div>
	{:else}
		<div class="text-center py-12">
			<p class="text-gray-500">Your cart is empty.</p>
			<a href="/" class="text-indigo-600 hover:text-indigo-500 mt-4 inline-block">Go Shopping</a>
		</div>
	{/if}
</div>
