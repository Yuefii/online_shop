<script lang="ts">
  import { onMount } from 'svelte';
  import { getPaginatedProducts, deleteProduct, type Product } from '$lib/services/products';

  let products: Product[] = [];
  let loading = true;
  let error = '';
  let searchQuery = '';
  let deletingId: number | null = null;
  
  // Pagination state
  let page = 1;
  let size = 10;
  let total = 0;
  let totalPages = 0;

  async function loadProducts() {
    loading = true;
    try {
      const response = await getPaginatedProducts({ 
          q: searchQuery, 
          page, 
          size 
      });
      products = response.items;
      total = response.total;
      totalPages = response.pages;
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
      // Refresh current page
      loadProducts();
    } catch (e: any) {
      alert(e.message || 'Failed to delete product');
    } finally {
      deletingId = null;
    }
  }

  function handleSearch() {
      page = 1; // Reset to first page on search
      loadProducts();
  }

  function handlePageChange(newPage: number) {
      if (newPage < 1 || newPage > totalPages) return;
      page = newPage;
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

			{#if products.length > 0}
				<div
					class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6"
				>
					<!-- Mobile Pagination -->
					<div class="flex-1 flex justify-between sm:hidden">
						<button
							on:click={() => handlePageChange(page - 1)}
							disabled={page === 1}
							class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
						>
							Previous
						</button>
						<button
							on:click={() => handlePageChange(page + 1)}
							disabled={page === totalPages}
							class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
						>
							Next
						</button>
					</div>

					<!-- Desktop Pagination -->
					<div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
						<div>
							<p class="text-sm text-gray-700">
								Showing
								<span class="font-medium">{(page - 1) * size + 1}</span>
								to
								<span class="font-medium">{Math.min(page * size, total)}</span>
								of
								<span class="font-medium">{total}</span>
								results
							</p>
						</div>
						<div>
							<nav
								class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px"
								aria-label="Pagination"
							>
								<button
									on:click={() => handlePageChange(page - 1)}
									disabled={page === 1}
									class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
								>
									<span class="sr-only">Previous</span>
									<svg
										class="h-5 w-5"
										xmlns="http://www.w3.org/2000/svg"
										viewBox="0 0 20 20"
										fill="currentColor"
										aria-hidden="true"
									>
										<path
											fill-rule="evenodd"
											d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
											clip-rule="evenodd"
										/>
									</svg>
								</button>
								{#each Array(totalPages) as _, i}
									{@const p = i + 1}
									<!-- Simple logic to show some pages, could be more complex -->
									{#if p === 1 || p === totalPages || (p >= page - 1 && p <= page + 1)}
										<button
											on:click={() => handlePageChange(p)}
											class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium {page ===
											p
												? 'z-10 bg-indigo-50 border-indigo-500 text-indigo-600'
												: 'text-gray-500 hover:bg-gray-50'}"
										>
											{p}
										</button>
									{:else if p === page - 2 || p === page + 2}
										<span
											class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700"
											>...</span
										>
									{/if}
								{/each}
								<button
									on:click={() => handlePageChange(page + 1)}
									disabled={page === totalPages}
									class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
								>
									<span class="sr-only">Next</span>
									<svg
										class="h-5 w-5"
										xmlns="http://www.w3.org/2000/svg"
										viewBox="0 0 20 20"
										fill="currentColor"
										aria-hidden="true"
									>
										<path
											fill-rule="evenodd"
											d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
											clip-rule="evenodd"
										/>
									</svg>
								</button>
							</nav>
						</div>
					</div>
				</div>
			{/if}

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
