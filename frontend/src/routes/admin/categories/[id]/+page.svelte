<script lang="ts">
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { getCategory, updateCategory, type Category } from '$lib/services/categories';

  let loading = true;
  let submitting = false;
  let error = '';
  let category: Category | null = null;
  const categoryId = Number($page.params.id);

  let name = '';
  let slug = '';

  onMount(async () => {
    try {
      category = await getCategory(categoryId);
      name = category.name;
      slug = category.slug;
    } catch (e: any) {
      error = e.message || 'Failed to load category';
    } finally {
      loading = false;
    }
  });

  async function handleSubmit() {
    submitting = true;
    error = '';
    
    try {
      await updateCategory(categoryId, {
        name,
        slug
      });
      goto('/admin/categories');
    } catch (e: any) {
      error = e.message || 'Failed to update category';
    } finally {
      submitting = false;
    }
  }

  function generateSlug(text: string) {
      return text
          .toLowerCase()
          .replace(/[^\w ]+/g, '')
          .replace(/ +/g, '-');
  }

  function handleNameInput() {
      if (!category) return; // Should likely not auto-update slug on edit unless explicit
      // slug = generateSlug(name); 
  }
</script>

<div class="max-w-2xl mx-auto">
	<div class="mb-8">
		<a href="/admin/categories" class="text-indigo-600 hover:text-indigo-800 mb-4 inline-block">
			&larr; Back to Categories
		</a>
		<h2 class="text-2xl font-bold text-gray-900">Edit Category</h2>
	</div>

	{#if loading}
		<div class="py-10 text-center text-gray-500">Loading category...</div>
	{:else if error}
		<div class="bg-red-50 text-red-700 p-4 rounded-md border border-red-200 mb-6">
			{error}
		</div>
	{/if}

	{#if !loading && category}
		<form
			on:submit|preventDefault={handleSubmit}
			class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 space-y-6"
		>
			<div>
				<label for="name" class="block text-sm font-medium text-gray-700">Name</label>
				<input
					type="text"
					id="name"
					bind:value={name}
					on:input={handleNameInput}
					required
					class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm border p-2"
				/>
			</div>

			<div>
				<label for="slug" class="block text-sm font-medium text-gray-700">Slug</label>
				<div class="mt-1 flex rounded-md shadow-sm">
					<input
						type="text"
						id="slug"
						bind:value={slug}
						required
						class="flex-1 block w-full rounded-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm border p-2"
					/>
				</div>
				<p class="mt-1 text-xs text-gray-500">URL-friendly version of the name.</p>
			</div>

			<div class="flex justify-end pt-4">
				<button
					type="submit"
					disabled={submitting}
					class="bg-indigo-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 transition-colors"
				>
					{submitting ? 'Saving...' : 'Save Changes'}
				</button>
			</div>
		</form>
	{/if}
</div>
