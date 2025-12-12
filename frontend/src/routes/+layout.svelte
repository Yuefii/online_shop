<script lang="ts">
	import './layout.css';
    import { onMount } from 'svelte';
    import { auth } from '$lib/stores/auth';
    import { get } from 'svelte/store';

	let { children } = $props();

    onMount(() => {
        const state = get(auth);
        if (state.isAuthenticated) {
            auth.fetchProfile();
        }
    });
</script>

{@render children()}
