import { writable, get } from 'svelte/store';
import { request } from '$lib/api';
import type { Product } from '$lib/services/products';

export interface CartItem {
    id: number;
    quantity: number;
    product: Product;
}

export interface Cart {
    id: number;
    user_id: number;
    total_price: number;
    items: CartItem[];
}

function createCartStore() {
    const { subscribe, set, update } = writable<Cart | null>(null);

    return {
        subscribe,
        
        async fetchCart() {
            try {
                const data = await request('/cart/');
                set(data);
            } catch (e) {
                console.error("Failed to fetch cart", e);
                set(null);
            }
        },
        
        async addToCart(product: Product) {
            try {
                const data = await request('/cart/items', {
                    method: 'POST',
                    body: JSON.stringify({ product_id: product.id, quantity: 1 })
                });
                set(data);
                // Optional: Show toast
            } catch (e) {
                console.error("Failed to add to cart", e);
            }
        },
        
        async removeFromCart(itemId: number) {
            try {
                const data = await request(`/cart/items/${itemId}`, {
                    method: 'DELETE'
                });
                set(data);
            } catch (e) {
                console.error("Failed to remove from cart", e);
            }
        }
    };
}

export const cart = createCartStore();
