<script lang="ts">
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { getOrder, payOrder, type Order } from '$lib/services/orders';

  let order: Order | null = null;
  let loading = true;
  let error = '';
  let paymentProcessing = false;
  
  const id = Number($page.params.id);

  onMount(async () => {
    try {
      order = await getOrder(id);
    } catch (e: any) {
      error = e.message || "Failed to load order";
    } finally {
      loading = false;
    }
  });

  async function handlePayment() {
      if (!order) return;
      paymentProcessing = true;
      try {
          // Simulate network delay for effect
          await new Promise(r => setTimeout(r, 1500));
          const updatedOrder = await payOrder(order.id);
          order = updatedOrder;
          alert('Payment Successful!');
      } catch (e: any) {
          alert('Payment failed: ' + e.message);
      } finally {
          paymentProcessing = false;
      }
  }

  function formatDate(dateString: string) {
    return new Date(dateString).toLocaleString();
  }
</script>

<div class="max-w-3xl mx-auto space-y-8">
	<div class="flex items-center justify-between">
		<h1 class="text-3xl font-bold text-gray-900">Order #{id}</h1>
		<a href="/orders" class="text-indigo-600 hover:text-indigo-500 font-medium">← Back to Orders</a>
	</div>

	{#if loading}
		<div class="flex justify-center py-12">
			<div
				class="animate-spin h-8 w-8 text-indigo-600 rounded-full border-2 border-t-transparent border-indigo-600"
			></div>
		</div>
	{:else if error}
		<div class="bg-red-50 text-red-700 p-4 rounded-md">
			{error}
		</div>
	{:else if order}
		<div class="bg-white shadow overflow-hidden sm:rounded-lg">
			<div class="px-4 py-5 sm:px-6 flex justify-between items-center">
				<div>
					<h3 class="text-lg leading-6 font-medium text-gray-900">Order Details</h3>
					<p class="mt-1 max-w-2xl text-sm text-gray-500">
						Placed on {formatDate(order.created_at)}
					</p>
				</div>
				<span
					class="px-3 py-1 inline-flex text-sm font-semibold rounded-full
          {order.status === 'completed' ||
					order.status === 'shipped' ||
					order.status === 'processing'
						? 'bg-green-100 text-green-800'
						: order.status === 'pending'
							? 'bg-yellow-100 text-yellow-800'
							: 'bg-gray-100 text-gray-800'}"
				>
					{order.status.toUpperCase()}
				</span>
				{#if order.status === 'pending'}
					<button
						on:click={handlePayment}
						disabled={paymentProcessing}
						class="ml-4 px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
					>
						{paymentProcessing ? 'Processing...' : 'Pay Now'}
					</button>
				{/if}
			</div>
			<div class="border-t border-gray-200">
				<dl>
					<div class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
						<dt class="text-sm font-medium text-gray-500">Shipping Address</dt>
						<dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
							{order.shipping_address}
						</dd>
					</div>
					<div class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
						<dt class="text-sm font-medium text-gray-500">Total Amount</dt>
						<dd class="mt-1 text-sm font-bold text-gray-900 sm:mt-0 sm:col-span-2">
							${order.total_price}
						</dd>
					</div>
				</dl>
			</div>
		</div>

		<div class="bg-white shadow sm:rounded-lg overflow-hidden">
			<div class="px-4 py-5 sm:px-6">
				<h3 class="text-lg leading-6 font-medium text-gray-900">Items</h3>
			</div>
			<ul role="list" class="divide-y divide-gray-200">
				{#each order.items as item}
					<li class="px-4 py-4 sm:px-6 flex justify-between items-center">
						<div>
							<p class="text-sm font-medium text-indigo-600 truncate">
								{item.product_name || 'Product ' + item.product_id}
							</p>
							<p class="text-sm text-gray-500">Qty: {item.quantity}</p>
						</div>
						<div class="text-sm font-bold text-gray-900">
							${item.price_at_purchase * item.quantity}
						</div>
					</li>
				{/each}
			</ul>
		</div>
	{:else}
		<p>Order not found.</p>
	{/if}
</div>
