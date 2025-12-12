<script lang="ts">
  import { cart } from '$lib/stores/cart';
  import { fade, slide } from 'svelte/transition';
  
  export let isOpen = false;
  
  function close() {
      isOpen = false;
  }
</script>

{#if isOpen}
	<!-- Overlay -->
	<div
		class="fixed inset-0 bg-black bg-opacity-50 z-40 transition-opacity"
		on:click={close}
		transition:fade
	></div>

	<!-- Drawer -->
	<div
		class="fixed inset-y-0 right-0 max-w-md w-full bg-white shadow-xl z-50 flex flex-col transform transition-transform"
		transition:slide={{ axis: 'x', duration: 300 }}
	>
		<div class="flex items-center justify-between p-4 border-b">
			<h2 class="text-lg font-medium text-gray-900">Shopping Cart</h2>
			<button type="button" class="-mr-2 text-gray-400 hover:text-gray-500 p-2" on:click={close}>
				<span class="sr-only">Close panel</span>
				<svg
					class="h-6 w-6"
					fill="none"
					viewBox="0 0 24 24"
					stroke-width="1.5"
					stroke="currentColor"
				>
					<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
				</svg>
			</button>
		</div>

		<div class="flex-1 overflow-y-auto p-4">
			{#if $cart && $cart.items.length > 0}
				<div class="flow-root">
					<ul role="list" class="-my-6 divide-y divide-gray-200">
						{#each $cart.items as item (item.id)}
							<li class="flex py-6">
								<div
									class="h-24 w-24 flex-shrink-0 overflow-hidden rounded-md border border-gray-200 bg-gray-50"
								>
									{#if item.product.image_url}
										<img
											src={item.product.image_url}
											alt={item.product.name}
											class="h-full w-full object-cover object-center"
										/>
									{:else}
										<div
											class="h-full w-full flex items-center justify-center text-xs text-gray-400"
										>
											No Image
										</div>
									{/if}
								</div>

								<div class="ml-4 flex flex-1 flex-col">
									<div>
										<div class="flex justify-between text-base font-medium text-gray-900">
											<h3>{item.product.name}</h3>
											<p class="ml-4">${item.product.price * item.quantity}</p>
										</div>
										<p class="mt-1 text-sm text-gray-500">
											{item.product.description?.substring(0, 50)}...
										</p>
									</div>
									<div class="flex flex-1 items-end justify-between text-sm">
										<p class="text-gray-500">Qty {item.quantity}</p>

										<div class="flex">
											<button
												type="button"
												class="font-medium text-indigo-600 hover:text-indigo-500"
												on:click={() => cart.removeFromCart(item.id)}
											>
												Remove
											</button>
										</div>
									</div>
								</div>
							</li>
						{/each}
					</ul>
				</div>
			{:else}
				<div class="h-full flex flex-col items-center justify-center text-gray-500">
					<p>Your cart is empty.</p>
				</div>
			{/if}
		</div>

		{#if $cart && $cart.items.length > 0}
			<div class="border-t border-gray-200 p-4 sm:px-6">
				<div class="flex justify-between text-base font-medium text-gray-900">
					<p>Subtotal</p>
					<p>${$cart.total_price}</p>
				</div>
				<p class="mt-0.5 text-sm text-gray-500">Shipping and taxes calculated at checkout.</p>
				<div class="mt-6">
					<a
						href="/checkout"
						class="flex items-center justify-center rounded-md border border-transparent bg-indigo-600 px-6 py-3 text-base font-medium text-white shadow-sm hover:bg-indigo-700"
						on:click={close}
					>
						Checkout
					</a>
				</div>
			</div>
		{/if}
	</div>
{/if}
