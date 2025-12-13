<script lang="ts">
  import '../layout.css';
  import { auth } from '$lib/stores/auth';
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import Sidebar from './components/Sidebar.svelte';
  import Header from './components/Header.svelte';
  
  let { children } = $props();

  onMount(() => {
	const unsubscribe = auth.subscribe(state => {
		if (state.loading) return;

        if (!state.isAuthenticated) {
            goto('/');
            return;
        }

        // Fix Race Condition: If authenticated but user is null (Root layout hasn't fetched yet),
        // we must trigger fetch or wait. 
        if (!state.user) {
            // Trigger fetch if not already loading (which we checked above)
            auth.fetchProfile();
            return; // Wait for next update
        }

        if (state.user.role !== 'admin') {
			goto('/');
		}
	});
	return unsubscribe;
  });
</script>

<div class="min-h-screen bg-gray-50 font-sans text-gray-800 flex">
	<!-- Sidebar -->
	<Sidebar />

	<!-- Main Content Wrapper -->
	<div class="flex-1 flex flex-col pl-64 transition-all duration-300">
		<!-- Header -->
		<Header />

		<!-- Page Content -->
		<main class="p-8 flex-1 overflow-y-auto">
			{@render children()}
		</main>
	</div>
</div>
