<script lang="ts">
  import { onMount } from 'svelte';
  import { createProduct } from '$lib/services/products';
  import { getCategories, type Category } from '$lib/services/categories';
  import { goto } from '$app/navigation';

  let name = '';
  let description = '';
  let price = 0;
  let stock = 0;
  let category_id: number | null = null;
  let image_url = '';
  
  let categories: Category[] = [];
  let loadingContent = true;
  let error = '';
  let submitting = false;

  onMount(async () => {
    try {
      categories = await getCategories();
      if (categories.length > 0) {
        // default to first category
        category_id = categories[0].id;
      }
    } catch (e: any) {
        error = "Failed to load categories: " + (e.message || 'Unknown error');
    } finally {
        loadingContent = false;
    }
  });

  async function handleSubmit() {
    if (!category_id) {
        error = "Please select a category";
        return;
    }

    submitting = true;
    error = '';
    try {
      await createProduct({ 
        name, 
        description, 
        price, 
        stock, 
        category_id,
        image_url: image_url || undefined
      });
      goto('/products');
    } catch (e: any) {
      error = e.message || 'Failed to create product';
    } finally {
      submitting = false;
    }
  }
</script>

<div class="max-w-2xl mx-auto">
	<div class="mb-8">
		<a
			href="/admin/products"
			class="text-indigo-600 hover:text-indigo-800 mb-4 inline-block text-sm font-medium"
			>&larr; Back to Products</a
		>
		<h1 class="text-2xl font-bold text-gray-900">Create Product</h1>
	</div>

	{#if error}
		<div
			class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded relative mb-6"
			role="alert"
		>
			<strong class="font-bold">Error:</strong>
			<span class="block sm:inline">{error}</span>
		</div>
	{/if}

	{#if loadingContent}
		<div class="py-10 text-center text-gray-500">Loading form dependencies...</div>
	{:else}
		<form
			on:submit|preventDefault={handleSubmit}
			class="bg-white border border-gray-200 p-8 rounded-lg shadow-sm space-y-6"
		>
			<div>
				<label for="name" class="block text-sm font-medium text-gray-700 mb-1">Name</label>
				<input
					type="text"
					id="name"
					bind:value={name}
					required
					class="input-field block w-full rounded-md px-4 py-2 sm:text-sm border-gray-300 focus:border-indigo-500 focus:ring-indigo-500"
				/>
			</div>

			<div>
				<label for="category" class="block text-sm font-medium text-gray-700 mb-1">Category</label>
				<select
					id="category"
					bind:value={category_id}
					required
					class="input-field block w-full rounded-md px-4 py-2 sm:text-sm border-gray-300 focus:border-indigo-500 focus:ring-indigo-500"
				>
					{#each categories as cat}
						<option value={cat.id}>{cat.name}</option>
					{/each}
				</select>
				{#if categories.length === 0}
					<p class="text-yellow-600 text-xs mt-1">
						No categories available. Please create a category first.
					</p>
				{/if}
			</div>

			<div>
				<label for="price" class="block text-sm font-medium text-gray-700 mb-1">Price</label>
				<input
					type="number"
					step="0.01"
					id="price"
					bind:value={price}
					required
					class="input-field block w-full rounded-md px-4 py-2 sm:text-sm border-gray-300 focus:border-indigo-500 focus:ring-indigo-500"
				/>
			</div>

			<div>
				<label for="stock" class="block text-sm font-medium text-gray-700 mb-1">Stock</label>
				<input
					type="number"
					id="stock"
					bind:value={stock}
					required
					class="input-field block w-full rounded-md px-4 py-2 sm:text-sm border-gray-300 focus:border-indigo-500 focus:ring-indigo-500"
				/>
			</div>

			<div>
				<label for="description" class="block text-sm font-medium text-gray-700 mb-1"
					>Description</label
				>
				<textarea
					id="description"
					bind:value={description}
					rows="3"
					class="input-field block w-full rounded-md px-4 py-2 sm:text-sm border-gray-300 focus:border-indigo-500 focus:ring-indigo-500"
				></textarea>
			</div>

			<div>
				<label for="image_url" class="block text-sm font-medium text-gray-700 mb-1"
					>Image URL (Optional)</label
				>
				<input
					type="url"
					id="image_url"
					bind:value={image_url}
					class="input-field block w-full rounded-md px-4 py-2 sm:text-sm border-gray-300 focus:border-indigo-500 focus:ring-indigo-500"
					placeholder="https://example.com/image.jpg"
				/>
			</div>

			<div class="pt-4">
				<button
					type="submit"
					disabled={submitting || categories.length === 0}
					class="w-full bg-indigo-600 text-white font-bold py-2 px-4 rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition duration-150"
				>
					{#if submitting}
						Creating...
					{:else}
						Create Product
					{/if}
				</button>
			</div>
		</form>
	{/if}
</div>
