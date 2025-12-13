import { request } from '$lib/api';

export interface Product {
    id: number;
    name: string;
    description?: string;
    price: number;
    image_url?: string;
    stock: number;
    category_id: number;
    category_name?: string;
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

export async function getProducts(params?: {
    q?: string;
    min_price?: number;
    max_price?: number;
    category_id?: number;
}): Promise<Product[]> {
    const query = new URLSearchParams();
    if (params) {
        if (params.q) query.append('q', params.q);
        if (params.min_price) query.append('min_price', params.min_price.toString());
        if (params.max_price) query.append('max_price', params.max_price.toString());
        if (params.category_id) query.append('category_id', params.category_id.toString());
    }
    const queryString = query.toString();
    return request(queryString ? `/products/?${queryString}` : '/products/');
}

export interface PaginatedResponse<T> {
    items: T[];
    total: number;
    page: number;
    size: number;
    pages: number;
}

export async function getPaginatedProducts(params?: {
    q?: string;
    min_price?: number;
    max_price?: number;
    category_id?: number;
    page?: number;
    size?: number;
}): Promise<PaginatedResponse<Product>> {
    const query = new URLSearchParams();
    if (params) {
        if (params.q) query.append('q', params.q);
        if (params.min_price) query.append('min_price', params.min_price.toString());
        if (params.max_price) query.append('max_price', params.max_price.toString());
        if (params.category_id) query.append('category_id', params.category_id.toString());
        if (params.page) query.append('page', params.page.toString());
        if (params.size) query.append('size', params.size.toString());
    }
    const queryString = query.toString();
    return request(queryString ? `/products/paginated?${queryString}` : '/products/paginated');
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

export async function updateProduct(id: number, data: ProductCreate): Promise<Product> {
    return request(`/products/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data)
    });
}

export async function deleteProduct(id: number): Promise<void> {
    return request(`/products/${id}`, {
        method: 'DELETE'
    });
}
