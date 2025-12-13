<script lang="ts">
  import { createCategory } from '$lib/services/categories';
  import { goto } from '$app/navigation';

  let name = '';
  let slug = '';
  let error = '';
  let submitting = false;

  async function handleSubmit() {
    submitting = true;
    error = '';
    try {
      await createCategory({ name, slug });
      goto('/admin/categories');
    } catch (e: any) {
      error = e.message || 'Failed to create category';
    } finally {
      submitting = false;
    }
  }

  // Auto-generate slug from name
  $: slug = name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)+/g, '');
</script>

<div class="max-w-2xl mx-auto">
	<div class="mb-8">
		<a
			href="/admin/categories"
			class="text-indigo-600 hover:text-indigo-800 mb-4 inline-block text-sm font-medium"
			>&larr; Back to Categories</a
		>
		<h1 class="text-2xl font-bold text-gray-900">Create Category</h1>
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
				placeholder="e.g. Electronics"
			/>
		</div>

		<div>
			<label for="slug" class="block text-sm font-medium text-gray-700 mb-1">Slug</label>
			<input
				type="text"
				id="slug"
				bind:value={slug}
				required
				class="input-field block w-full rounded-md px-4 py-2 sm:text-sm border-gray-300 focus:border-indigo-500 focus:ring-indigo-500"
				placeholder="e.g. electronics"
			/>
		</div>

		<div class="pt-4">
			<button
				type="submit"
				disabled={submitting}
				class="w-full bg-indigo-600 text-white font-bold py-2 px-4 rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition duration-150"
			>
				{#if submitting}
					Creating...
				{:else}
					Create Category
				{/if}
			</button>
		</div>
	</form>
</div>
