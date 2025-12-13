<script lang="ts">
    import { onMount } from 'svelte';
    import { request } from '$lib/api';
    import { DollarSign, ShoppingCart, Package, Users, TrendingUp } from 'lucide-svelte';
    import StatCard from './components/StatCard.svelte';
    import SalesChart from './components/SalesChart.svelte';
    import RecentOrders from './components/RecentOrders.svelte';

    interface Order {
        id: number;
        user_id: number;
        total_price: number;
        status: string;
        created_at: string;
    }
    
    interface Product {
        id: number;
        stock: number;
    }

    interface User {
        id: number;
        role: string;
    }

    let orders: Order[] = $state([]);
    let products: Product[] = $state([]);
    let users: User[] = $state([]);
    
    let loading = $state(true);
    let error = $state<string | null>(null);

    // Derived Stats
    let totalRevenue = $derived(orders.reduce((sum, order) => sum + (order.status !== 'cancelled' ? order.total_price : 0), 0));
    let totalOrders = $derived(orders.length);
    let totalProducts = $derived(products.length);
    let totalUsers = $derived(users.length);

    // Chart Data Preparation
    let salesData = $derived.by(() => {
        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        const currentYear = new Date().getFullYear();
        const monthlySales = new Array(12).fill(0);

        orders.forEach(order => {
             if (order.status !== 'cancelled') {
                 const date = new Date(order.created_at);
                 if (date.getFullYear() === currentYear) {
                     monthlySales[date.getMonth()] += order.total_price;
                 }
             }
        });

        return {
            labels: months,
            data: monthlySales
        };
    });

    onMount(async () => {
        try {
            loading = true;
            const [ordersData, productsData, usersData] = await Promise.all([
                request('/orders/admin/all'),
                request('/products/'),
                request('/users/')
            ]);
            
            orders = ordersData;
            products = productsData;
            users = usersData;
        } catch (e: any) {
            console.error(e);
            error = e.message || 'Failed to load dashboard data';
        } finally {
            loading = false;
        }
    });

    function formatCurrency(amount: number) {
        return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount);
    }
</script>

<div class="space-y-6">
	<div class="flex items-center justify-between">
		<div>
			<h2 class="text-2xl font-bold text-gray-900">Dashboard Overview</h2>
			<p class="mt-1 text-sm text-gray-500">Welcome back! Here's what's happening today.</p>
		</div>
		<div class="flex gap-3">
			<button
				class="px-4 py-2 bg-white border border-gray-200 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
			>
				Download Report
			</button>
			<button
				class="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
			>
				View Analytics
			</button>
		</div>
	</div>

	{#if loading}
		<div class="flex items-center justify-center h-64">
			<div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
		</div>
	{:else if error}
		<div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg" role="alert">
			<p class="font-bold">Error</p>
			<p>{error}</p>
		</div>
	{:else}
		<!-- Stats Grid -->
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
			<StatCard
				title="Total Revenue"
				value={formatCurrency(totalRevenue)}
				icon={DollarSign}
				trend={12}
				color="green"
			/>
			<StatCard
				title="Total Orders"
				value={totalOrders}
				icon={ShoppingCart}
				trend={5}
				color="blue"
			/>
			<StatCard
				title="Total Products"
				value={totalProducts}
				icon={Package}
				trend={0}
				color="orange"
			/>
			<StatCard title="Total Users" value={totalUsers} icon={Users} trend={8} color="purple" />
		</div>

		<!-- Charts & Recent Orders -->
		<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
			<div class="lg:col-span-2">
				<SalesChart labels={salesData.labels} data={salesData.data} />
			</div>
			<div class="lg:col-span-1">
				<RecentOrders {orders} />
			</div>
		</div>
	{/if}
</div>
