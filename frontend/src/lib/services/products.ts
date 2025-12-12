import { request } from '$lib/api';

export interface Product {
    id: number;
    name: string;
    description?: string;
    price: number;
    image_url?: string;
    stock: number;
    category_id: number;
    created_at?: string;
}

export interface ProductCreate {
    name: string;
    description?: string;
    price: number;
    image_url?: string;
    stock: number;
    category_id: number;
}

export async function getProducts(): Promise<Product[]> {
    return request('/products/');
}

export async function createProduct(data: ProductCreate): Promise<Product> {
    return request('/products/', {
        method: 'POST',
        body: JSON.stringify(data)
    });
}

export async function getProduct(id: number): Promise<Product> {
    return request(`/products/${id}`);
}
