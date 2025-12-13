<script lang="ts">
	import { auth } from '$lib/stores/auth';
    import { cart } from '$lib/stores/cart';
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import CartDrawer from '$lib/components/CartDrawer.svelte';

	let { children } = $props();

    $effect(() => {
        const _ = $page.url.pathname;
        mobileMenuOpen = false;
        cartDrawerOpen = false;
    });

    let mobileMenuOpen = $state(false);
    let cartDrawerOpen = $state(false);

    function toggleMobileMenu() {
        mobileMenuOpen = !mobileMenuOpen;
    }
    
    function toggleCartDrawer() {
        cartDrawerOpen = !cartDrawerOpen;
    }
    
    onMount(() => {
        if ($auth.isAuthenticated) {
            cart.fetchCart();
        }
    });
</script>

<div class="min-h-screen flex flex-col bg-gray-50">
	<nav class="bg-white border-b border-gray-200 sticky top-0 z-50">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
			<div class="flex items-center justify-between h-16">
				<div class="flex items-center">
					<a href="/" class="text-xl font-bold text-gray-900 tracking-tight"> OnlineShop </a>
				</div>
				<div class="hidden md:block">
					<div class="ml-10 flex items-center space-x-4">
						<a
							href="/"
							class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium transition-colors"
							>Home</a
						>

						{#if $auth.isAuthenticated}
							<a
								href="/orders"
								class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium transition-colors"
								>Orders</a
							>

							<a
								href="/profile"
								class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium transition-colors"
								>Profile</a
							>

							{#if $auth.user && $auth.user.role === 'admin'}
								<a
									href="/admin"
									class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium transition-colors"
									>Admin</a
								>
							{/if}

							<!-- Cart Button -->
							<button
								class="relative text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium transition-colors"
								onclick={toggleCartDrawer}
							>
								<svg
									xmlns="http://www.w3.org/2000/svg"
									fill="none"
									viewBox="0 0 24 24"
									stroke-width="1.5"
									stroke="currentColor"
									class="w-6 h-6"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z"
									/>
								</svg>
								{#if $cart && $cart.items.length > 0}
									<span
										class="absolute top-1 right-1 inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white transform translate-x-1/4 -translate-y-1/4 bg-red-600 rounded-full"
										>{$cart.items.length}</span
									>
								{/if}
							</button>

							<button
								onclick={() => auth.logout()}
								class="text-gray-600 hover:text-red-600 px-3 py-2 rounded-md text-sm font-medium transition-colors cursor-pointer"
								>Logout</button
							>
						{:else}
							<a
								href="/auth/login"
								class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium transition-colors"
								>Login</a
							>
							<a
								href="/auth/register"
								class="bg-gray-900 hover:bg-gray-800 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors shadow-sm"
								>Sign Up</a
							>
						{/if}
					</div>
				</div>
				<div class="-mr-2 flex md:hidden">
					{#if $auth.isAuthenticated}
						<button
							class="relative text-gray-600 hover:text-gray-900 p-2 mr-2"
							onclick={toggleCartDrawer}
						>
							<svg
								xmlns="http://www.w3.org/2000/svg"
								fill="none"
								viewBox="0 0 24 24"
								stroke-width="1.5"
								stroke="currentColor"
								class="w-6 h-6"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z"
								/>
							</svg>
							{#if $cart && $cart.items.length > 0}
								<span
									class="absolute top-1 right-1 inline-flex items-center justify-center px-1.5 py-0.5 text-xs font-bold leading-none text-white transform translate-x-1/4 -translate-y-1/4 bg-red-600 rounded-full"
									>{$cart.items.length}</span
								>
							{/if}
						</button>
					{/if}

					<button
						onclick={toggleMobileMenu}
						type="button"
						class="inline-flex items-center justify-center p-2 rounded-md text-gray-500 hover:text-gray-900 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-gray-500"
					>
						<span class="sr-only">Open main menu</span>
						<svg
							class="h-6 w-6"
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
							aria-hidden="true"
						>
							{#if mobileMenuOpen}
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M6 18L18 6M6 6l12 12"
								/>
							{:else}
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M4 6h16M4 12h16M4 18h16"
								/>
							{/if}
						</svg>
					</button>
				</div>
			</div>
		</div>

		{#if mobileMenuOpen}
			<div class="md:hidden bg-white border-b border-gray-200">
				<div class="px-2 pt-2 pb-3 space-y-1 sm:px-3">
					<a
						href="/"
						class="text-gray-600 hover:text-gray-900 hover:bg-gray-50 block px-3 py-2 rounded-md text-base font-medium"
						>Home</a
					>

					{#if $auth.isAuthenticated}
						<a
							href="/orders"
							class="text-gray-600 hover:text-gray-900 hover:bg-gray-50 block px-3 py-2 rounded-md text-base font-medium"
							>Orders</a
						>
						<a
							href="/profile"
							class="text-gray-600 hover:text-gray-900 hover:bg-gray-50 block px-3 py-2 rounded-md text-base font-medium"
							>Profile</a
						>
						{#if $auth.user && $auth.user.role === 'admin'}
							<a
								href="/admin"
								class="text-gray-600 hover:text-gray-900 hover:bg-gray-50 block px-3 py-2 rounded-md text-base font-medium"
								>Admin</a
							>
						{/if}
						<button
							onclick={() => auth.logout()}
							class="text-gray-600 hover:text-red-600 hover:bg-red-50 block w-full text-left px-3 py-2 rounded-md text-base font-medium"
							>Logout</button
						>
					{:else}
						<a
							href="/auth/login"
							class="text-gray-600 hover:text-gray-900 hover:bg-gray-50 block px-3 py-2 rounded-md text-base font-medium"
							>Login</a
						>
						<a
							href="/auth/register"
							class="text-gray-600 hover:text-gray-900 hover:bg-gray-50 block px-3 py-2 rounded-md text-base font-medium"
							>Sign Up</a
						>
					{/if}
				</div>
			</div>
		{/if}
	</nav>

	<main class="flex-grow container mx-auto px-4 sm:px-6 lg:px-8 py-12 relative">
		{@render children()}
	</main>

	<CartDrawer bind:isOpen={cartDrawerOpen} />
</div>
