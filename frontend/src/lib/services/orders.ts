import { request } from '$lib/api';

export interface OrderItem {
    id: number;
    product_id: number;
    product_name: string;
    quantity: number;
    price_at_purchase: number;
}

export interface Order {
    id: number;
    user_id: number;
    status: string;
    total_price: number;
    shipping_address: string;
    created_at: string;
    items: OrderItem[];
}

export async function getOrders(): Promise<Order[]> {
    return request('/orders/');
}

export async function getOrder(id: number): Promise<Order> {
    return request(`/orders/${id}`);
}

export async function listAllOrdersAdmin(): Promise<Order[]> {
    return request('/orders/admin/all');
}

export async function updateOrderStatus(id: number, status: string): Promise<Order> {
    return request(`/orders/${id}/status`, {
        method: 'PUT',
        body: JSON.stringify({ status })
    });
}

export async function payOrder(id: number): Promise<Order> {
    return request(`/orders/${id}/pay`, {
        method: 'POST'
    });
}
