<script lang="ts">
	import { auth } from '$lib/stores/auth';
	
	let email = $state('');
	let password = $state('');
	let fullName = $state('');
	let error = $state<string | null>(null);

	async function handleSubmit(e: Event) {
		e.preventDefault();
		error = null;

        if (password.length < 8) {
            error = 'Password must be at least 8 characters long.';
            return;
        }
        if (!/\d/.test(password)) {
            error = 'Password must contain at least one number.';
            return;
        }
		
		try {
			await auth.register(email, password, fullName);
		} catch (err: any) {
			error = err.message || 'Registration failed.';
		}
	}
</script>

<div class="flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
	<div class="max-w-md w-full glass-panel p-8 rounded-lg">
		<div>
			<h2 class="mt-6 text-center text-3xl font-bold text-gray-900">Create account</h2>
			<p class="mt-2 text-center text-sm text-gray-600">
				Or
				<a
					href="/login"
					class="font-medium text-gray-900 hover:text-gray-700 underline transition-colors"
				>
					sign in to existing account
				</a>
			</p>
		</div>
		<form class="mt-8 space-y-6" onsubmit={handleSubmit}>
			{#if error}
				<div
					class="bg-red-50 border border-red-200 rounded-md p-3 text-sm text-red-600 text-center whitespace-pre-line"
				>
					{error}
				</div>
			{/if}

			<div class="space-y-4">
				<div>
					<label for="full-name" class="block text-sm font-medium text-gray-700 mb-1"
						>Full Name</label
					>
					<input
						id="full-name"
						name="full_name"
						type="text"
						autocomplete="name"
						required
						class="input-field appearance-none rounded-md relative block w-full px-3 py-2 placeholder-gray-400 focus:z-10 sm:text-sm"
						placeholder="John Doe"
						bind:value={fullName}
					/>
				</div>
				<div>
					<label for="email-address" class="block text-sm font-medium text-gray-700 mb-1"
						>Email address</label
					>
					<input
						id="email-address"
						name="email"
						type="email"
						autocomplete="email"
						required
						class="input-field appearance-none rounded-md relative block w-full px-3 py-2 placeholder-gray-400 focus:z-10 sm:text-sm"
						placeholder="you@example.com"
						bind:value={email}
					/>
				</div>
				<div>
					<label for="password" class="block text-sm font-medium text-gray-700 mb-1">Password</label
					>
					<input
						id="password"
						name="password"
						type="password"
						autocomplete="new-password"
						required
						class="input-field appearance-none rounded-md relative block w-full px-3 py-2 placeholder-gray-400 focus:z-10 sm:text-sm"
						placeholder="8+ characters, 1 number"
						bind:value={password}
					/>
				</div>
			</div>

			<div>
				<button
					type="submit"
					class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white btn-primary focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-900 disabled:opacity-50 disabled:cursor-not-allowed"
					disabled={$auth.loading}
				>
					{#if $auth.loading}
						<svg
							class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
						>
							<circle
								class="opacity-25"
								cx="12"
								cy="12"
								r="10"
								stroke="currentColor"
								stroke-width="4"
							></circle>
							<path
								class="opacity-75"
								fill="currentColor"
								d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
							></path>
						</svg>
						Creating account...
					{:else}
						Create Account
					{/if}
				</button>
			</div>
		</form>
	</div>
</div>
