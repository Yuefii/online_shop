<script lang="ts">
  import { onMount } from 'svelte';
  import { listAllOrdersAdmin, updateOrderStatus, cancelOrder, type Order } from '$lib/services/orders';

  let orders: Order[] = [];
  let loading = true;
  let error = '';

  onMount(async () => {
      await fetchOrders();
  });

  async function fetchOrders() {
      loading = true;
      try {
          orders = await listAllOrdersAdmin();
      } catch (e: any) {
          error = e.message || 'Failed to load orders';
      } finally {
          loading = false;
      }
  }

  async function handleStatusChange(order: Order, newStatus: string) {
      if (order.status === newStatus) return;
      
      const originalStatus = order.status;
      // Optimistic update
      order.status = newStatus;
      orders = [...orders]; 

      try {
          await updateOrderStatus(order.id, newStatus);
      } catch (e: any) {
          alert('Failed to update status: ' + e.message);
          order.status = originalStatus;
          orders = [...orders];
      }
  }

  async function handleCancel(order: Order) {
      if (!confirm(`Are you sure you want to cancel Order #${order.id}?`)) return;
      
      const originalStatus = order.status;
      try {
          // Optimistic
          order.status = 'cancelled';
          orders = [...orders];
          
          await cancelOrder(order.id);
      } catch (e: any) {
          alert('Failed to cancel: ' + e.message);
          order.status = originalStatus;
          orders = [...orders];
      }
  }

  function formatDate(dateString: string) {
      return new Date(dateString).toLocaleString();
  }
</script>

<div class="space-y-6">
	<div class="flex justify-between items-center">
		<h1 class="text-2xl font-bold text-gray-900">Manage Orders</h1>
		<button on:click={fetchOrders} class="text-indigo-600 hover:text-indigo-900 text-sm"
			>Refresh</button
		>
	</div>

	{#if loading}
		<div class="flex justify-center py-10">
			<div
				class="animate-spin h-6 w-6 text-indigo-600 rounded-full border-2 border-t-transparent border-indigo-600"
			></div>
		</div>
	{:else if error}
		<div class="bg-red-50 p-4 rounded-md text-red-700">{error}</div>
	{:else}
		<div class="bg-white shadow overflow-hidden sm:rounded-lg">
			<table class="min-w-full divide-y divide-gray-200">
				<thead class="bg-gray-50">
					<tr>
						<th
							scope="col"
							class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
							>ID</th
						>
						<th
							scope="col"
							class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
							>Date</th
						>
						<th
							scope="col"
							class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
							>Customer</th
						>
						<th
							scope="col"
							class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
							>Total</th
						>
						<th
							scope="col"
							class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
							>Status</th
						>
						<th
							scope="col"
							class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
							>Actions</th
						>
					</tr>
				</thead>
				<tbody class="bg-white divide-y divide-gray-200">
					{#each orders as order}
						<tr>
							<td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
								>#{order.id}</td
							>
							<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
								>{formatDate(order.created_at)}</td
							>
							<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">User {order.user_id}</td
							>
							<td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-900"
								>${order.total_price}</td
							>
							<td class="px-6 py-4 whitespace-nowrap">
								<span
									class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full
                                  {order.status === 'completed'
										? 'bg-green-100 text-green-800'
										: order.status === 'pending'
											? 'bg-yellow-100 text-yellow-800'
											: order.status === 'processing'
												? 'bg-blue-100 text-blue-800'
												: order.status === 'shipped'
													? 'bg-indigo-100 text-indigo-800'
													: order.status === 'cancelled'
														? 'bg-red-100 text-red-800'
														: 'bg-gray-100 text-gray-800'}"
								>
									{order.status}
								</span>
							</td>
							<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
								{#if order.status === 'processing'}
									<button
										class="text-indigo-600 hover:text-indigo-900 font-medium mr-2"
										on:click={() => handleStatusChange(order, 'shipped')}
									>
										Ship Order
									</button>
									<button
										class="text-red-600 hover:text-red-900 font-medium"
										on:click={() => handleCancel(order)}
									>
										Cancel
									</button>
								{:else if order.status === 'pending'}
									<button
										class="text-red-600 hover:text-red-900 font-medium"
										on:click={() => handleCancel(order)}
									>
										Cancel
									</button>
								{:else}
									<span class="text-gray-400">-</span>
								{/if}
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	{/if}
</div>
