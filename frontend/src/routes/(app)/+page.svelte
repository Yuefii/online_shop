<script lang="ts">
  import { onMount } from 'svelte';
  import { getProducts, type Product } from '$lib/services/products';
  import { getCategories, type Category } from '$lib/services/categories';
  import { cart } from '$lib/stores/cart';
  import { slide } from 'svelte/transition';

  let products: Product[] = [];
  let categories: Category[] = [];
  let loading = true;
  let error = '';
  
  // Filter States
  let selectedCategoryId: number | null = null;
  let searchQuery = '';
  let minPrice = '';
  let maxPrice = '';
  let searchTimeout: any;
  let showFilters = false;

  // Load initial data
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

  // Reactive Fetching
  async function fetchFilteredProducts() {
      loading = true;
      try {
          products = await getProducts({
              q: searchQuery,
              category_id: selectedCategoryId || undefined,
              min_price: minPrice ? Number(minPrice) : undefined,
              max_price: maxPrice ? Number(maxPrice) : undefined
          });
      } catch(e: any) {
          error = e.message;
      } finally {
          loading = false;
      }
  }
  
  // Debounced Search
  function handleSearchInput() {
      clearTimeout(searchTimeout);
      searchTimeout = setTimeout(fetchFilteredProducts, 500);
  }

  
  // Let's use a explicit refetch function called by UI events for clarity and consistency
  function applyFilters() {
      fetchFilteredProducts();
  }
  
  function selectCategory(id: number | null) {
      selectedCategoryId = id;
      applyFilters();
  }

  function addToCart(product: Product) {
      cart.addToCart(product);
  }
</script>

<div class="space-y-8">
	<div class="text-center py-12">
		<h1 class="text-4xl font-bold text-gray-900 mb-4">Welcome to OnlineShop</h1>
		<p class="text-lg text-gray-600 max-w-2xl mx-auto">
			Discover our latest collection of amazing products tailored just for you.
		</p>
	</div>

	<!-- Minimalist Search and Filter Section -->
	<div class="max-w-4xl mx-auto space-y-8">
		<!-- Search Bar -->
		<div class="relative group">
			<div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
				<svg
					class="h-5 w-5 text-gray-400 group-focus-within:text-indigo-600 transition-colors"
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 20 20"
					fill="currentColor"
				>
					<path
						fill-rule="evenodd"
						d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
						clip-rule="evenodd"
					/>
				</svg>
			</div>
			<input
				type="text"
				placeholder="Search for products..."
				class="block w-full pl-11 pr-20 py-4 bg-white border-0 rounded-2xl shadow-[0_4px_20px_-4px_rgba(0,0,0,0.1)] text-gray-900 placeholder-gray-400 focus:ring-2 focus:ring-indigo-100 transition-shadow text-lg"
				bind:value={searchQuery}
				on:input={handleSearchInput}
			/>

			<!-- Price Filter Toggle (integrated inside search bar) -->
			<div class="absolute inset-y-0 right-0 pr-3 flex items-center">
				<button
					class="p-2 rounded-xl text-gray-400 hover:text-indigo-600 hover:bg-gray-50 transition-all font-medium text-sm flex items-center gap-2"
					on:click={() => (showFilters = !showFilters)}
				>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="h-5 w-5"
						viewBox="0 0 20 20"
						fill="currentColor"
					>
						<path
							fill-rule="evenodd"
							d="M3 3a1 1 0 011-1h12a1 1 0 011 1v3a1 1 0 01-.293.707L12 11.414V15a1 1 0 01-.293.707l-2 2A1 1 0 018 17v-5.586L3.293 6.707A1 1 0 013 6V3z"
							clip-rule="evenodd"
						/>
					</svg>
					<span class="hidden sm:inline">Filters</span>
				</button>
			</div>
		</div>

		<!-- Expandable Filters -->
		{#if showFilters}
			<div
				transition:slide={{ duration: 200, axis: 'y' }}
				class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex flex-wrap gap-4 items-center justify-center animate-in fade-in slide-in-from-top-2"
			>
				<span class="text-sm font-medium text-gray-500 uppercase tracking-wider">Price Range</span>
				<div class="flex items-center gap-4">
					<div class="relative">
						<span class="absolute inset-y-0 left-0 pl-3 flex items-center text-gray-400">$</span>
						<input
							type="number"
							placeholder="Min"
							class="pl-7 pr-4 py-2 w-32 rounded-lg border-gray-200 focus:border-indigo-500 focus:ring-indigo-500 text-sm"
							bind:value={minPrice}
							on:change={applyFilters}
						/>
					</div>
					<span class="text-gray-300">—</span>
					<div class="relative">
						<span class="absolute inset-y-0 left-0 pl-3 flex items-center text-gray-400">$</span>
						<input
							type="number"
							placeholder="Max"
							class="pl-7 pr-4 py-2 w-32 rounded-lg border-gray-200 focus:border-indigo-500 focus:ring-indigo-500 text-sm"
							bind:value={maxPrice}
							on:change={applyFilters}
						/>
					</div>
				</div>
			</div>
		{/if}

		<!-- Category Pills (Horizontal Scroll) -->
		<div class="flex justify-center">
			<div
				class="inline-flex rounded-xl bg-white p-1 shadow-sm border border-gray-100 overflow-x-auto max-w-full"
			>
				<button
					class="px-5 py-2.5 rounded-lg text-sm font-medium transition-all whitespace-nowrap {selectedCategoryId ===
					null
						? 'bg-gray-900 text-white shadow-md'
						: 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'}"
					on:click={() => selectCategory(null)}
				>
					All Items
				</button>
				{#each categories as category}
					<button
						class="px-5 py-2.5 rounded-lg text-sm font-medium transition-all whitespace-nowrap {selectedCategoryId ===
						category.id
							? 'bg-gray-900 text-white shadow-md'
							: 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'}"
						on:click={() => selectCategory(category.id)}
					>
						{category.name}
					</button>
				{/each}
			</div>
		</div>
	</div>

	{#if loading}
		<div class="flex justify-center py-10">
			<div
				class="animate-spin h-8 w-8 text-gray-900 rounded-full border-2 border-t-transparent border-gray-100"
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
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
			{#each products as product (product.id)}
				<div
					class="glass-panel rounded-lg p-6 hover:shadow-lg transition-all duration-300 flex flex-col group cursor-pointer hover:-translate-y-1 bg-white border border-gray-100"
				>
					{#if product.image_url}
						<div
							class="aspect-w-16 aspect-h-9 mb-4 overflow-hidden rounded-md bg-gray-100 border border-gray-200"
						>
							<img
								src={product.image_url}
								alt={product.name}
								class="w-full h-64 object-cover transform group-hover:scale-105 transition-transform duration-500"
							/>
						</div>
					{:else}
						<div
							class="w-full h-64 bg-gray-100 rounded-md mb-4 flex items-center justify-center text-gray-400 border border-gray-200"
						>
							<span>No Image</span>
						</div>
					{/if}

					<div class="flex justify-between items-start mb-4">
						<h2
							class="text-lg font-bold text-gray-900 group-hover:text-indigo-600 transition-colors truncate"
						>
							{product.name}
						</h2>
					</div>

					<p class="text-gray-500 text-sm mb-4 flex-grow line-clamp-2">
						{product.description || 'No description'}
					</p>

					<div
						class="mt-auto flex justify-between items-center text-sm border-t border-gray-100 pt-4"
					>
						<span class="text-gray-900 font-bold text-xl">${product.price}</span>
						<button
							class="btn-primary px-4 py-2 rounded-md text-sm font-medium bg-black text-white hover:bg-gray-800 transition-colors"
							on:click={() => addToCart(product)}
						>
							Add to Cart
						</button>
					</div>
				</div>
			{/each}
		</div>
		{#if products.length === 0}
			<div class="text-center py-16">
				<p class="text-gray-500 text-lg">No products found matching your criteria.</p>
			</div>
		{/if}
	{/if}
</div>
