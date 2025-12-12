<script lang="ts">
  import '../layout.css';
  let { children } = $props();
</script>

<div class="min-h-screen bg-gray-100 flex font-sans text-gray-800">
	<!-- Sidebar -->
	<aside
		class="w-64 bg-white border-r border-gray-200 min-h-screen fixed inset-y-0 left-0 z-10 flex flex-col shadow-sm"
	>
		<div class="p-6 border-b border-gray-100">
			<h1 class="text-xl font-bold tracking-tight text-gray-900">Shop Admin</h1>
		</div>
		<nav class="flex-1 p-4 space-y-1">
			<a
				href="/admin"
				class="flex items-center px-4 py-2 rounded-md hover:bg-gray-50 transition-colors text-gray-600 hover:text-gray-900 font-medium"
			>
				Dashboard
			</a>

			<div class="pt-6 pb-2 px-4 text-xs font-semibold text-gray-400 uppercase tracking-wider">
				Catalog
			</div>
			<a
				href="/admin/products"
				class="flex items-center px-4 py-2 rounded-md hover:bg-gray-50 transition-colors text-gray-600 hover:text-gray-900 font-medium"
			>
				Products
			</a>
			<a
				href="/admin/categories"
				class="flex items-center px-4 py-2 rounded-md hover:bg-gray-50 transition-colors text-gray-600 hover:text-gray-900 font-medium"
			>
				Categories
			</a>

			<div class="pt-8 border-t border-gray-100 mt-4">
				<a
					href="/"
					class="flex items-center px-4 py-2 rounded-md hover:bg-gray-50 transition-colors text-gray-500 hover:text-gray-700 text-sm font-medium"
				>
					&larr; Back to Shop Website
				</a>
			</div>
		</nav>
	</aside>

	<!-- Main Content -->
	<div class="flex-1 ml-64">
		<main class="p-8 max-w-7xl mx-auto">
			{@render children()}
		</main>
	</div>
</div>
