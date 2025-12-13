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

  // Category Scrolling Logic
  let categoryScrollContainer: HTMLElement;
  let showLeftArrow = false;
  let showRightArrow = true;
  let showAllCategories = false;

  function checkScroll() {
      if (!categoryScrollContainer) return;
      const { scrollLeft, scrollWidth, clientWidth } = categoryScrollContainer;
      showLeftArrow = scrollLeft > 10;
      showRightArrow = scrollLeft < scrollWidth - clientWidth - 10;
  }

  function scrollCategories(direction: 'left' | 'right') {
      if (!categoryScrollContainer) return;
      const scrollAmount = 300;
      categoryScrollContainer.scrollBy({
          left: direction === 'left' ? -scrollAmount : scrollAmount,
          behavior: 'smooth'
      });
  }

  onMount(() => {
      checkScroll();
      window.addEventListener('resize', checkScroll);
      return () => window.removeEventListener('resize', checkScroll);
  });
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

		<!-- Category Navigation -->
		<div class="relative max-w-full">
			{#if !showAllCategories}
				<!-- Scroll Shadows/Gradients -->
				{#if showLeftArrow}
					<div
						class="absolute left-0 top-0 bottom-0 w-20 bg-gradient-to-r from-white to-transparent z-10 pointer-events-none"
					></div>
					<button
						class="absolute left-0 top-1/2 -translate-y-1/2 z-20 bg-white shadow-md rounded-full p-2 text-gray-600 hover:text-gray-900 focus:outline-none hidden md:block"
						on:click={() => scrollCategories('left')}
						aria-label="Scroll left"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="h-5 w-5"
							viewBox="0 0 20 20"
							fill="currentColor"
						>
							<path
								fill-rule="evenodd"
								d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
								clip-rule="evenodd"
							/>
						</svg>
					</button>
				{/if}

				{#if showRightArrow}
					<div
						class="absolute right-0 top-0 bottom-0 w-20 bg-gradient-to-l from-white to-transparent z-10 pointer-events-none"
					></div>
					<button
						class="absolute right-0 top-1/2 -translate-y-1/2 z-20 bg-white shadow-md rounded-full p-2 text-gray-600 hover:text-gray-900 focus:outline-none hidden md:block"
						on:click={() => scrollCategories('right')}
						aria-label="Scroll right"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="h-5 w-5"
							viewBox="0 0 20 20"
							fill="currentColor"
						>
							<path
								fill-rule="evenodd"
								d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
								clip-rule="evenodd"
							/>
						</svg>
					</button>
				{/if}
			{/if}

			<div
				bind:this={categoryScrollContainer}
				class="flex flex-wrap justify-center gap-2 p-1 {showAllCategories
					? ''
					: 'overflow-x-auto flex-nowrap md:px-10 scrollbar-hide snap-x'}"
				on:scroll={checkScroll}
			>
				<button
					class="px-5 py-2.5 rounded-lg text-sm font-medium transition-all whitespace-nowrap snap-center {selectedCategoryId ===
					null
						? 'bg-gray-900 text-white shadow-md'
						: 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'}"
					on:click={() => selectCategory(null)}
				>
					All Items
				</button>
				{#each categories as category}
					<button
						class="px-5 py-2.5 rounded-lg text-sm font-medium transition-all whitespace-nowrap snap-center {selectedCategoryId ===
						category.id
							? 'bg-gray-900 text-white shadow-md'
							: 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'}"
						on:click={() => selectCategory(category.id)}
					>
						{category.name}
					</button>
				{/each}
			</div>

			<!-- View All Toggle -->
			{#if categories.length > 5}
				<div class="flex justify-center mt-2">
					<button
						on:click={() => (showAllCategories = !showAllCategories)}
						class="text-xs font-medium text-gray-500 hover:text-indigo-600 flex items-center gap-1 transition-colors"
					>
						{showAllCategories ? 'Show Less' : 'View All Categories'}
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="h-4 w-4 transform transition-transform {showAllCategories ? 'rotate-180' : ''}"
							viewBox="0 0 20 20"
							fill="currentColor"
						>
							<path
								fill-rule="evenodd"
								d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
								clip-rule="evenodd"
							/>
						</svg>
					</button>
				</div>
			{/if}
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
		<div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
			{#each products as product (product.id)}
				<div
					class="glass-panel rounded-lg p-4 hover:shadow-lg transition-all duration-300 flex flex-col group cursor-pointer hover:-translate-y-1 bg-white border border-gray-100"
				>
					{#if product.image_url}
						<div
							class="aspect-w-1 aspect-h-1 mb-4 overflow-hidden rounded-md bg-gray-100 border border-gray-200"
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

					<div class="flex justify-between items-start mb-2">
						<h2
							class="text-base font-bold text-gray-900 group-hover:text-indigo-600 transition-colors truncate"
						>
							{product.name}
						</h2>
					</div>

					<p class="text-gray-500 text-xs mb-3 flex-grow line-clamp-2">
						{product.description || 'No description'}
					</p>

					<div class="mt-auto flex flex-col gap-2 text-sm border-t border-gray-100 pt-3">
						<span class="text-gray-900 font-bold text-lg">${product.price}</span>
						<button
							class="btn-primary w-full py-2 rounded-md text-xs font-medium bg-black text-white hover:bg-gray-800 transition-colors"
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
