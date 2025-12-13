<script lang="ts">
	import { page } from '$app/stores';
	import { 
		LayoutDashboard, 
		Package, 
		Tags, 
		ShoppingCart, 
		Users, 
		LogOut,
		Store
	} from 'lucide-svelte';

	let currentPath = $derived($page.url.pathname);

	const links = [
		{ href: '/admin', label: 'Dashboard', icon: LayoutDashboard },
		{ href: '/admin/products', label: 'Products', icon: Package },
		{ href: '/admin/categories', label: 'Categories', icon: Tags },
		{ href: '/admin/orders', label: 'Orders', icon: ShoppingCart },
		{ href: '/admin/users', label: 'Users', icon: Users }
	];
</script>

<aside class="w-64 bg-white border-r border-gray-200 min-h-screen flex flex-col fixed inset-y-0 left-0 z-20 shadow-sm transition-all duration-300">
	<!-- Logo/Brand -->
	<div class="h-16 flex items-center px-6 border-b border-gray-100">
		<div class="flex items-center gap-2 text-indigo-600">
			<Store size={24} />
			<span class="text-xl font-bold tracking-tight text-gray-900">Shop Admin</span>
		</div>
	</div>

	<!-- Navigation -->
	<nav class="flex-1 p-4 space-y-1 overflow-y-auto">
		<div class="mb-4 px-2 text-xs font-semibold text-gray-400 uppercase tracking-wider">
			Menu
		</div>
		
		{#each links as link}
			{@const isActive = currentPath === link.href}
			<a
				href={link.href}
				class="flex items-center px-3 py-2.5 rounded-lg text-sm font-medium transition-colors duration-200
				{isActive 
					? 'bg-indigo-50 text-indigo-700' 
					: 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'}"
			>
				<link.icon size={20} class="mr-3 {isActive ? 'text-indigo-600' : 'text-gray-400 group-hover:text-gray-500'}" />
				{link.label}
			</a>
		{/each}
	</nav>

	<!-- Footer / Bottom Links -->
	<div class="p-4 border-t border-gray-100">
		<a
			href="/"
			class="flex items-center px-3 py-2.5 rounded-lg text-sm font-medium text-gray-600 hover:bg-red-50 hover:text-red-600 transition-colors"
		>
			<LogOut size={20} class="mr-3" />
			Back to Shop
		</a>
	</div>
</aside>
