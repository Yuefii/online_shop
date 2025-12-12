<script lang="ts">
  import { onMount } from 'svelte';
  import { getProducts, type Product } from '$lib/services/products';

  let products: Product[] = [];
  let loading = true;
  let error = '';

  onMount(async () => {
    try {
      products = await getProducts();
    } catch (e: any) {
      error = e.message || 'Failed to load products';
    } finally {
      loading = false;
    }
  });
</script>

<div class="space-y-6">
	<div class="flex justify-between items-center border-b border-gray-200 pb-4">
		<div>
			<h2 class="text-2xl font-bold text-gray-900">Products</h2>
			<p class="mt-1 text-sm text-gray-500">Manage your product inventory.</p>
		</div>
		<a
			href="/admin/products/new"
			class="bg-indigo-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-indigo-700 transition-colors shadow-sm"
		>
			+ Add Product
		</a>
	</div>

	{#if loading}
		<div class="py-10 text-center text-gray-500">Loading products...</div>
	{:else if error}
		<div class="bg-red-50 text-red-700 p-4 rounded-md border border-red-200">
			{error}
		</div>
	{:else}
		<div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
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
							>Name</th
						>
						<th
							scope="col"
							class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
							>Price</th
						>
						<th
							scope="col"
							class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
							>Stock</th
						>
						<th
							scope="col"
							class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
							>Category ID</th
						>
					</tr>
				</thead>
				<tbody class="bg-white divide-y divide-gray-200">
					{#each products as product}
						<tr class="hover:bg-gray-50">
							<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-mono"
								>#{product.id}</td
							>
							<td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
								>{product.name}</td
							>
							<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${product.price}</td>
							<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
								<span
									class="{product.stock > 0
										? 'bg-green-100 text-green-800'
										: 'bg-red-100 text-red-800'} px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
								>
									{product.stock}
								</span>
							</td>
							<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
								>{product.category_id}</td
							>
						</tr>
					{/each}
				</tbody>
			</table>
			{#if products.length === 0}
				<div class="text-center py-12 text-gray-500">No products found.</div>
			{/if}
		</div>
	{/if}
</div>
