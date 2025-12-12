<script lang="ts">
  import { onMount } from 'svelte';
  import { getProducts, type Product } from '$lib/services/products';
  import { getCategories, type Category } from '$lib/services/categories';

  let products: Product[] = [];
  let categories: Category[] = [];
  let loading = true;
  let error = '';
  let selectedCategoryId: number | null = null;

  onMount(async () => {
    try {
      const [productsData, categoriesData] = await Promise.all([
        getProducts(),
        getCategories()
      ]);
      products = productsData;
      categories = categoriesData;
    } catch (e: any) {
      error = e.message || 'Failed to load data';
    } finally {
      loading = false;
    }
  });

  $: filteredProducts = selectedCategoryId
    ? products.filter(p => p.category_id === selectedCategoryId)
    : products;
</script>

<div class="space-y-8">
	<div class="text-center py-12">
		<h1 class="text-4xl font-bold text-gray-900 mb-4">Welcome to OnlineShop</h1>
		<p class="text-lg text-gray-600 max-w-2xl mx-auto">
			Discover our latest collection of amazing products tailored just for you.
		</p>
	</div>

	{#if loading}
		<div class="flex justify-center py-10">
			<div
				class="animate-spin h-8 w-8 text-gray-900 rounded-full border-2 border-t-transparent border-gray-900"
			></div>
		</div>
	{:else if error}
		<div
			class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded relative max-w-2xl mx-auto"
			role="alert"
		>
			<strong class="font-bold">Error:</strong>
			<span class="block sm:inline">{error}</span>
		</div>
	{:else}
		<!-- Category Filter -->
		<div class="flex flex-wrap justify-center gap-2 max-w-4xl mx-auto">
			<button
				class="px-4 py-2 rounded-full text-sm font-medium transition-colors border {selectedCategoryId ===
				null
					? 'bg-gray-900 text-white border-gray-900'
					: 'bg-white text-gray-600 border-gray-200 hover:bg-gray-50'}"
				on:click={() => (selectedCategoryId = null)}
			>
				All
			</button>
			{#each categories as category}
				<button
					class="px-4 py-2 rounded-full text-sm font-medium transition-colors border {selectedCategoryId ===
					category.id
						? 'bg-gray-900 text-white border-gray-900'
						: 'bg-white text-gray-600 border-gray-200 hover:bg-gray-50'}"
					on:click={() => (selectedCategoryId = category.id)}
				>
					{category.name}
				</button>
			{/each}
		</div>

		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
			{#each filteredProducts as product (product.id)}
				<div
					class="glass-panel rounded-lg p-6 hover:shadow-lg transition-all duration-300 flex flex-col group cursor-pointer hover:-translate-y-1"
				>
					<div class="flex justify-between items-start mb-4">
						<h2
							class="text-lg font-bold text-gray-900 group-hover:text-indigo-600 transition-colors"
						>
							{product.name}
						</h2>
					</div>

					{#if product.image_url}
						<div
							class="aspect-w-16 aspect-h-9 mb-4 overflow-hidden rounded-md bg-gray-100 border border-gray-200"
						>
							<img
								src={product.image_url}
								alt={product.name}
								class="w-full h-48 object-cover transform group-hover:scale-105 transition-transform duration-500"
							/>
						</div>
					{:else}
						<div
							class="w-full h-48 bg-gray-100 rounded-md mb-4 flex items-center justify-center text-gray-400 border border-gray-200"
						>
							<span>No Image</span>
						</div>
					{/if}

					<p class="text-gray-500 text-sm mb-4 flex-grow line-clamp-2">
						{product.description || 'No description'}
					</p>

					<div
						class="mt-auto flex justify-between items-center text-sm border-t border-gray-100 pt-4"
					>
						<span class="text-gray-900 font-bold text-xl">${product.price}</span>
						<button
							class="btn-primary px-4 py-2 rounded-md text-sm font-medium opacity-0 group-hover:opacity-100 transition-opacity"
						>
							Add to Cart
						</button>
					</div>
				</div>
			{/each}
		</div>
		{#if filteredProducts.length === 0}
			<div class="text-center py-16">
				<p class="text-gray-500 text-lg">No products found in this category.</p>
			</div>
		{/if}
	{/if}
</div>
