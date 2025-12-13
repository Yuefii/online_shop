<script lang="ts">
	import { Bell, Search, User } from 'lucide-svelte';
	import { auth } from '$lib/stores/auth';

	let { title = 'Dashboard' } = $props();
	let user = $derived($auth.user);
</script>

<header
	class="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-8 sticky top-0 z-10 shadow-sm"
>
	<div class="flex items-center gap-4">
		<h2 class="text-xl font-semibold text-gray-800">{title}</h2>
	</div>

	<div class="flex items-center gap-6">
		<!-- Search (Optional placeholder) -->
		<div class="relative hidden md:block">
			<Search class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
			<input
				type="text"
				placeholder="Search..."
				class="pl-10 pr-4 py-2 border border-gray-200 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent w-64"
			/>
		</div>

		<!-- Actions -->
		<div class="flex items-center gap-3">
			<button class="p-2 rounded-full hover:bg-gray-100 text-gray-500 relative">
				<Bell size={20} />
				<span class="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full border border-white"
				></span>
			</button>

			<div class="pl-4 border-l border-gray-200 flex items-center gap-3">
				<div class="text-right hidden sm:block">
					<p class="text-sm font-medium text-gray-900">{user?.email || 'Admin'}</p>
					<p class="text-xs text-gray-500 capitalize">{user?.role || 'Administrator'}</p>
				</div>
				<div
					class="h-9 w-9 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-600 border border-indigo-200"
				>
					<User size={18} />
				</div>
			</div>
		</div>
	</div>
</header>
