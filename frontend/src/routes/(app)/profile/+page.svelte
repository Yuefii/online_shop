<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';

	$effect(() => {
		if (browser && !$auth.isAuthenticated && !$auth.loading) {
			goto('/auth/login');
		}
	});

	onMount(() => {
		auth.fetchProfile();
	});
</script>

<div class="max-w-3xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
	{#if $auth.loading && !$auth.user}
		<div class="flex justify-center items-center h-64">
			<svg
				class="animate-spin h-8 w-8 text-gray-500"
				xmlns="http://www.w3.org/2000/svg"
				fill="none"
				viewBox="0 0 24 24"
			>
				<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"
				></circle>
				<path
					class="opacity-75"
					fill="currentColor"
					d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
				></path>
			</svg>
		</div>
	{:else if $auth.user}
		<div class="space-y-6">
			<div>
				<h3 class="text-2xl font-bold leading-6 text-gray-900">Profile</h3>
				<p class="mt-2max-w-2xl text-sm text-gray-500">Your personal information.</p>
			</div>

			<div class="glass-panel overflow-hidden rounded-lg">
				<div class="px-4 py-5 sm:p-0">
					<dl class="divide-y divide-gray-200">
						<div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
							<dt class="text-sm font-medium text-gray-500">Full name</dt>
							<dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
								{$auth.user.full_name}
							</dd>
						</div>
						<div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
							<dt class="text-sm font-medium text-gray-500">Email address</dt>
							<dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
								{$auth.user.email}
							</dd>
						</div>
						<div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
							<dt class="text-sm font-medium text-gray-500">User ID</dt>
							<dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
								{$auth.user.id}
							</dd>
						</div>
						<div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
							<dt class="text-sm font-medium text-gray-500">Account Status</dt>
							<dd class="mt-1 text-sm sm:mt-0 sm:col-span-2">
								{#if $auth.user.is_active}
									<span
										class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800"
									>
										Active
									</span>
								{:else}
									<span
										class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800"
									>
										Inactive
									</span>
								{/if}
							</dd>
						</div>
					</dl>
				</div>
			</div>

			<div class="flex justify-end pt-4">
				<button
					onclick={() => auth.logout()}
					class="px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-colors"
				>
					Sign out
				</button>
			</div>
		</div>
	{/if}
</div>
