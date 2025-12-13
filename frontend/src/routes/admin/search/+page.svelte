<script lang="ts">
    import { page } from '$app/stores';
    import { request } from '$lib/api';
    import { onMount } from 'svelte';
    import { derived } from 'svelte/store';
    import { Package, ShoppingCart, Users, Search, ArrowRight } from 'lucide-svelte';

    // Get search query from URL
    let query = $derived($page.url.searchParams.get('q') || '');
    
    let products: any[] = $state([]);
    let orders: any[] = $state([]);
    let users: any[] = $state([]);
    
    let loading = $state(false);
    let performedSearch = $state(''); // Track what current results are for

    // Reactively fetch when query changes
    // using an effect since we need async
    $effect(() => {
        if (query && query !== performedSearch) {
            performSearch(query);
        }
    });

    async function performSearch(q: string) {
        if (!q.trim()) return;
        
        loading = true;
        performedSearch = q;
        
        try {
            const [p, o, u] = await Promise.all([
                request(`/products/?q=${q}`),
                request(`/orders/admin/all?q=${q}`),
                request(`/users/?q=${q}`)
            ]);
            
            products = p;
            orders = o.length ? o : []; // sometimes returns null if error in some APIs but ours returns list
            users = u;
        } catch (e) {
            console.error("Search failed", e);
        } finally {
            loading = false;
        }
    }

    function formatDate(dateStr: string) {
        return new Date(dateStr).toLocaleDateString();
    }
    
    function formatCurrency(amount: number) {
        return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount);
    }
</script>

<div class="space-y-8">
	<div class="border-b border-gray-200 pb-5">
		<h2 class="text-2xl font-bold text-gray-900">Search Results</h2>
		<p class="mt-1 text-gray-500">
			Showing results for "<span class="font-medium text-gray-900">{query}</span>"
		</p>
	</div>

	{#if loading}
		<div class="flex items-center justify-center py-20">
			<div class="animate-spin rounded-full h-10 w-10 border-b-2 border-indigo-600"></div>
		</div>
	{:else if !products.length && !orders.length && !users.length}
		<div class="text-center py-20 bg-white rounded-lg border border-gray-200 dashed">
			<Search class="mx-auto h-12 w-12 text-gray-300" />
			<h3 class="mt-2 text-sm font-medium text-gray-900">No results found</h3>
			<p class="mt-1 text-sm text-gray-500">
				We couldn't find anything matching your search query.
			</p>
		</div>
	{:else}
		<!-- Products Section -->
		{#if products.length > 0}
			<section>
				<div class="flex items-center justify-between mb-4">
					<h3 class="text-lg font-semibold text-gray-900 flex items-center gap-2">
						<Package size={20} class="text-indigo-600" />
						Products ({products.length})
					</h3>
				</div>
				<div class="bg-white rounded-lg border border-gray-200 overflow-hidden shadow-sm">
					<table class="min-w-full divide-y divide-gray-200">
						<thead class="bg-gray-50">
							<tr>
								<th
									class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>Name</th
								>
								<th
									class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>Price</th
								>
								<th
									class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>Stock</th
								>
								<th
									class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
									>Action</th
								>
							</tr>
						</thead>
						<tbody class="bg-white divide-y divide-gray-200">
							{#each products as product}
								<tr class="hover:bg-gray-50">
									<td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
										>{product.name}</td
									>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
										>{formatCurrency(product.price)}</td
									>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{product.stock}</td>
									<td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
										<a
											href="/admin/products/{product.id}"
											class="text-indigo-600 hover:text-indigo-900 flex items-center justify-end gap-1"
										>
											View <ArrowRight size={14} />
										</a>
									</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			</section>
		{/if}

		<!-- Orders Section -->
		{#if orders.length > 0}
			<section>
				<div class="flex items-center justify-between mb-4">
					<h3 class="text-lg font-semibold text-gray-900 flex items-center gap-2">
						<ShoppingCart size={20} class="text-blue-600" />
						Orders ({orders.length})
					</h3>
				</div>
				<div class="bg-white rounded-lg border border-gray-200 overflow-hidden shadow-sm">
					<table class="min-w-full divide-y divide-gray-200">
						<thead class="bg-gray-50">
							<tr>
								<th
									class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>Order ID</th
								>
								<th
									class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>Total</th
								>
								<th
									class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>Status</th
								>
								<th
									class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>Date</th
								>
								<th
									class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
									>Action</th
								>
							</tr>
						</thead>
						<tbody class="bg-white divide-y divide-gray-200">
							{#each orders as order}
								<tr class="hover:bg-gray-50">
									<td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
										>#{order.id}</td
									>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
										>{formatCurrency(order.total_price)}</td
									>
									<td class="px-6 py-4 whitespace-nowrap">
										<span
											class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full
                                            {order.status === 'completed'
												? 'bg-green-100 text-green-800'
												: order.status === 'pending'
													? 'bg-yellow-100 text-yellow-800'
													: 'bg-gray-100 text-gray-800'}"
										>
											{order.status}
										</span>
									</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
										>{formatDate(order.created_at)}</td
									>
									<td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
										<a
											href="/admin/orders/{order.id}"
											class="text-indigo-600 hover:text-indigo-900 flex items-center justify-end gap-1"
										>
											View <ArrowRight size={14} />
										</a>
									</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			</section>
		{/if}

		<!-- Users Section -->
		{#if users.length > 0}
			<section>
				<div class="flex items-center justify-between mb-4">
					<h3 class="text-lg font-semibold text-gray-900 flex items-center gap-2">
						<Users size={20} class="text-purple-600" />
						Users ({users.length})
					</h3>
				</div>
				<div class="bg-white rounded-lg border border-gray-200 overflow-hidden shadow-sm">
					<table class="min-w-full divide-y divide-gray-200">
						<thead class="bg-gray-50">
							<tr>
								<th
									class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>Email</th
								>
								<th
									class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>Name</th
								>
								<th
									class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>Role</th
								>
								<th
									class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
									>Joined</th
								>
							</tr>
						</thead>
						<tbody class="bg-white divide-y divide-gray-200">
							{#each users as user}
								<tr class="hover:bg-gray-50">
									<td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
										>{user.email}</td
									>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
										>{user.full_name || '-'}</td
									>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 capitalize"
										>{user.role}</td
									>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
										>{formatDate(user.created_at)}</td
									>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			</section>
		{/if}
	{/if}
</div>
