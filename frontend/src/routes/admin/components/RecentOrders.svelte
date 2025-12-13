<script lang="ts">
    import { Eye } from 'lucide-svelte';

    interface Order {
        id: number;
        user_id: number;
        total_price: number;
        status: string;
        created_at: string;
        // extended fields from fetching logic potentially
        user_name?: string; 
    }

    let { orders = [] } = $props<{ orders: Order[] }>();

    function getStatusColor(status: string) {
        switch (status.toLowerCase()) {
            case 'completed': return 'bg-green-100 text-green-800';
            case 'pending': return 'bg-yellow-100 text-yellow-800';
            case 'cancelled': return 'bg-red-100 text-red-800';
            case 'processing': return 'bg-blue-100 text-blue-800';
            default: return 'bg-gray-100 text-gray-800';
        }
    }
    
    function formatDate(dateStr: string) {
        if (!dateStr) return '';
        return new Date(dateStr).toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric'
        });
    }
</script>

<div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
	<div class="p-6 border-b border-gray-100 flex items-center justify-between">
		<h3 class="text-lg font-bold text-gray-900">Recent Orders</h3>
		<a href="/admin/orders" class="text-sm text-indigo-600 hover:text-indigo-800 font-medium"
			>View all</a
		>
	</div>
	<div class="overflow-x-auto">
		<table class="w-full text-left">
			<thead>
				<tr class="bg-gray-50 text-gray-500 text-xs uppercase tracking-wider">
					<th class="px-6 py-3 font-semibold">Order ID</th>
					<th class="px-6 py-3 font-semibold">Customer</th>
					<th class="px-6 py-3 font-semibold">Date</th>
					<th class="px-6 py-3 font-semibold">Amount</th>
					<th class="px-6 py-3 font-semibold">Status</th>
					<th class="px-6 py-3 font-semibold text-right">Action</th>
				</tr>
			</thead>
			<tbody class="divide-y divide-gray-100">
				{#if orders.length === 0}
					<tr>
						<td colspan="6" class="px-6 py-8 text-center text-gray-500">
							No recent orders found.
						</td>
					</tr>
				{:else}
					{#each orders.slice(0, 5) as order}
						<tr class="hover:bg-gray-50 transition-colors">
							<td class="px-6 py-4 text-sm font-medium text-gray-900">#{order.id}</td>
							<td class="px-6 py-4 text-sm text-gray-600">{order.user_id}</td>
							<!-- In real app, replace with name -->
							<td class="px-6 py-4 text-sm text-gray-600">{formatDate(order.created_at)}</td>
							<td class="px-6 py-4 text-sm font-medium text-gray-900">${order.total_price}</td>
							<td class="px-6 py-4">
								<span
									class={`inline-flex px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(order.status)}`}
								>
									{order.status}
								</span>
							</td>
							<td class="px-6 py-4 text-right">
								<button class="text-gray-400 hover:text-indigo-600 transition-colors">
									<Eye size={18} />
								</button>
							</td>
						</tr>
					{/each}
				{/if}
			</tbody>
		</table>
	</div>
</div>
