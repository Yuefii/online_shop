<script lang="ts">
  import { onMount } from 'svelte';
  import { request } from '$lib/api';

  interface OrderItem {
      id: number;
      product_name: string;
      quantity: number;
      price_at_purchase: number;
  }

  interface Order {
      id: number;
      status: string;
      total_price: number;
      created_at: string;
      items?: OrderItem[]; // Might be fetched separately or included
  }
  
  // We need to fetch items for each order or the backend returns them. 
  // Based on verify_features.py output `get_orders_by_user` returns orders list.
  // api/db/orders.py `get_orders_by_user` -> SELECT * FROM orders ...
  // It does NOT join items.
  // But `GET /orders/` endpoint implementation:
  // router.get("/", response_model=List[OrderResponse])
  // def list_orders(...):
  //    orders = get_orders_by_user(db, user['id'])
  //    # The schema OrderResponse includes `items: List[OrderItemResponse]`
  //    # If `get_orders_by_user` returns simpledicts without items, validation might fail or items be empty.
  //    # Let's check `verify_features.py` or logic.
  //    # In `verify_features.py`, it prints `List Orders: OK. Count: 1`. 
  //    # If I look at `api/routers/orders.py`, checks implementation.
  //    # Wait, I implemented `get_orders_by_user` in `api/db/orders.py`. Let's check if it fetches items.
  //    # Actually, I should just implement the frontend to display what it gets.
  //    # If items are missing, I might need to fetch details for each, or rely on `GET /orders/{id}`.
  
  let orders: Order[] = [];
  let loading = true;
  let error = '';

  onMount(async () => {
      try {
          // The list endpoint might not return full items details to save bandwidth, 
          // but for now let's assume it might or we fetch details on expand.
          // Actually, for a simple implementation, let's fetch list, and if user wants details we can implement expand.
          // Or for now, just list ID, Date, Total, Status.
          orders = await request('/orders/');
      } catch (e: any) {
          error = e.message || 'Failed to load orders';
      } finally {
          loading = false;
      }
  });

  function formatDate(dateString: string) {
      return new Date(dateString).toLocaleDateString() + ' ' + new Date(dateString).toLocaleTimeString();
  }
</script>

<div class="max-w-4xl mx-auto space-y-8">
	<h1 class="text-3xl font-bold text-gray-900">My Orders</h1>

	{#if loading}
		<div class="flex justify-center py-10">
			<div
				class="animate-spin h-8 w-8 text-indigo-600 rounded-full border-2 border-t-transparent border-indigo-600"
			></div>
		</div>
	{:else if error}
		<div class="bg-red-50 text-red-700 p-4 rounded-md">
			{error}
		</div>
	{:else if orders.length === 0}
		<div class="text-center py-12 bg-white rounded-lg shadow">
			<p class="text-gray-500">You haven't placed any orders yet.</p>
			<a href="/" class="text-indigo-600 hover:text-indigo-500 mt-4 inline-block font-medium"
				>Start Shopping</a
			>
		</div>
	{:else}
		<div class="bg-white shadow overflow-hidden sm:rounded-md">
			<ul role="list" class="divide-y divide-gray-200">
				{#each orders as order}
					<li>
						<div class="px-4 py-4 sm:px-6">
							<div class="flex items-center justify-between">
								<p class="text-sm font-medium text-indigo-600 truncate">
									Order #{order.id}
								</p>
								<div class="ml-2 flex-shrink-0 flex">
									<p
										class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full
                                    {order.status === 'completed'
											? 'bg-green-100 text-green-800'
											: order.status === 'pending'
												? 'bg-yellow-100 text-yellow-800'
												: 'bg-gray-100 text-gray-800'}"
									>
										{order.status}
									</p>
								</div>
							</div>
							<div class="mt-2 sm:flex sm:justify-between">
								<div class="sm:flex">
									<p class="flex items-center text-sm text-gray-500">
										Placed on {formatDate(order.created_at)}
									</p>
								</div>
								<div class="mt-2 flex items-center text-sm text-gray-900 font-bold sm:mt-0">
									${order.total_price}
								</div>
							</div>
						</div>
					</li>
				{/each}
			</ul>
		</div>
	{/if}
</div>
