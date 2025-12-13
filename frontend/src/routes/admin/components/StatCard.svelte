<script lang="ts">
	import type { ComponentType } from 'svelte';
    import { TrendingUp, TrendingDown, Minus } from 'lucide-svelte';

    interface Props {
        title: string;
        value: string | number;
        icon: ComponentType;
        trend?: number; // percentage, positive or negative
        color?: 'indigo' | 'green' | 'blue' | 'purple' | 'orange';
    }

    let { title, value, icon: Icon, trend = 0, color = 'indigo' }: Props = $props();

    const colorClasses: Record<string, string> = {
        indigo: 'bg-indigo-50 text-indigo-600',
        green: 'bg-green-50 text-green-600',
        blue: 'bg-blue-50 text-blue-600',
        purple: 'bg-purple-50 text-purple-600',
        orange: 'bg-orange-50 text-orange-600'
    };

    let activeColorClass = $derived(colorClasses[color] || colorClasses['indigo']);
</script>

<div
	class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow"
>
	<div class="flex items-start justify-between">
		<div>
			<p class="text-sm font-medium text-gray-500 mb-1">{title}</p>
			<h3 class="text-2xl font-bold text-gray-900">{value}</h3>
		</div>
		<div class={`p-3 rounded-lg ${activeColorClass}`}>
			<Icon size={24} />
		</div>
	</div>

	{#if trend !== undefined}
		<div class="mt-4 flex items-center text-sm">
			{#if trend > 0}
				<span class="text-green-600 flex items-center font-medium">
					<TrendingUp size={16} class="mr-1" />
					+{trend}%
				</span>
			{:else if trend < 0}
				<span class="text-red-600 flex items-center font-medium">
					<TrendingDown size={16} class="mr-1" />
					{trend}%
				</span>
			{:else}
				<span class="text-gray-400 flex items-center font-medium">
					<Minus size={16} class="mr-1" />
					0%
				</span>
			{/if}
			<span class="text-gray-400 ml-2">from last month</span>
		</div>
	{/if}
</div>
