<script lang="ts">
	import './layout.css';
    import { onMount } from 'svelte';
    import { auth } from '$lib/stores/auth';
    import { get } from 'svelte/store';

	let { children } = $props();

    onMount(() => {
        // Always try to fetch profile on mount to check cookie session
        auth.fetchProfile();
    });
</script>

{@render children()}
