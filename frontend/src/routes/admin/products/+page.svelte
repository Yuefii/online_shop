<script lang="ts">
  import { onMount } from 'svelte';
  import { getProducts, deleteProduct, type Product } from '$lib/services/products';

  let products: Product[] = [];
  let loading = true;
  let error = '';
  let searchQuery = '';
  let deletingId: number | null = null;

  async function loadProducts() {
    loading = true;
    try {
      products = await getProducts({ q: searchQuery });
    } catch (e: any) {
      error = e.message || 'Failed to load products';
    } finally {
      loading = false;
    }
  }

  async function handleDelete(id: number) {
    if(!confirm('Are you sure you want to delete this product?')) return;
    
    deletingId = id;
    try {
      await deleteProduct(id);
      products = products.filter(p => p.id !== id);
    } catch (e: any) {
      alert(e.message || 'Failed to delete product');
    } finally {
      deletingId = null;
    }
  }

  function handleSearch() {
      loadProducts();
  }

  onMount(() => {
    loadProducts();
  });
</script>

<div class="space-y-6">
	<div
		class="flex flex-col sm:flex-row justify-between items-start sm:items-center border-b border-gray-200 pb-4 gap-4"
	>
		<div>
			<h2 class="text-2xl font-bold text-gray-900">Products</h2>
			<p class="mt-1 text-sm text-gray-500">Manage your product inventory.</p>
		</div>
		<div class="flex gap-2 w-full sm:w-auto">
			<div class="relative rounded-md shadow-sm flex-1 sm:flex-none">
				<input
					type="text"
					bind:value={searchQuery}
					on:keydown={(e) => e.key === 'Enter' && handleSearch()}
					placeholder="Search products..."
					class="focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:w-64 pl-4 pr-10 sm:text-sm border-gray-300 rounded-md py-2 border"
				/>
				<button
					on:click={handleSearch}
					aria-label="Search"
					class="absolute inset-y-0 right-0 pr-3 flex items-center cursor-pointer text-gray-400 hover:text-gray-600"
				>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="h-5 w-5"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
						/>
					</svg>
				</button>
			</div>
			<a
				href="/admin/products/new"
				class="bg-indigo-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-indigo-700 transition-colors shadow-sm whitespace-nowrap"
			>
				+ Add Product
			</a>
		</div>
	</div>

	{#if loading}
		<div class="py-10 text-center text-gray-500">Loading products...</div>
	{:else if error}
		<div class="bg-red-50 text-red-700 p-4 rounded-md border border-red-200">
			{error}
		</div>
	{:else}
		<div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
			<div class="overflow-x-auto">
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
								>Image</th
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
								>Category</th
							>
							<th
								scope="col"
								class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
								>Actions</th
							>
						</tr>
					</thead>
					<tbody class="bg-white divide-y divide-gray-200">
						{#each products as product}
							<tr class="hover:bg-gray-50 transition-colors">
								<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-mono"
									>#{product.id}</td
								>
								<td class="px-6 py-4 whitespace-nowrap">
									{#if product.image_url}
										<img
											src={product.image_url}
											alt={product.name}
											class="h-10 w-10 rounded-md object-cover bg-gray-100"
										/>
									{:else}
										<div
											class="h-10 w-10 rounded-md bg-gray-100 flex items-center justify-center text-gray-400"
										>
											<svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
												<path
													stroke-linecap="round"
													stroke-linejoin="round"
													stroke-width="2"
													d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
												/>
											</svg>
										</div>
									{/if}
								</td>
								<td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
									>{product.name}</td
								>
								<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-medium"
									>${product.price}</td
								>
								<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
									<span
										class="{product.stock > 10
											? 'bg-green-100 text-green-800'
											: product.stock > 0
												? 'bg-yellow-100 text-yellow-800'
												: 'bg-red-100 text-red-800'} px-2.5 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full"
									>
										{product.stock}
									</span>
								</td>
								<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
									>{product.category_name || product.category_id}</td
								>
								<td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
									<div class="flex justify-end space-x-2">
										<a
											href="/admin/products/{product.id}"
											class="text-indigo-600 hover:text-indigo-900 bg-indigo-50 hover:bg-indigo-100 px-3 py-1 rounded-md transition-colors"
											>Edit</a
										>
										<button
											on:click={() => handleDelete(product.id)}
											class="text-red-600 hover:text-red-900 bg-red-50 hover:bg-red-100 px-3 py-1 rounded-md transition-colors disabled:opacity-50"
											disabled={deletingId === product.id}
										>
											{deletingId === product.id ? '...' : 'Delete'}
										</button>
									</div>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
			{#if products.length === 0}
				<div class="text-center py-12 text-gray-500">
					<p class="text-lg">No products found.</p>
					{#if searchQuery}
						<p class="text-sm mt-2">Try adjusting your search query.</p>
					{/if}
				</div>
			{/if}
		</div>
	{/if}
</div>
