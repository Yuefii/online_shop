import { request } from '$lib/api';

export interface Category {
    id: number;
    name: string;
    slug: string;
    created_at?: string;
}

export interface CategoryCreate {
    name: string;
    slug: string;
}

export interface PaginatedResponse<T> {
    items: T[];
    total: number;
    page: number;
    size: number;
    pages: number;
}

export async function getCategories(q?: string): Promise<Category[]> {
    const query = new URLSearchParams();
    if (q) query.append('q', q);
    const queryString = query.toString();
    return request(queryString ? `/categories/?${queryString}` : '/categories/');
}

export async function getPaginatedCategories(params?: {
    q?: string;
    page?: number;
    size?: number;
}): Promise<PaginatedResponse<Category>> {
    const query = new URLSearchParams();
    if (params) {
        if (params.q) query.append('q', params.q);
        if (params.page) query.append('page', params.page.toString());
        if (params.size) query.append('size', params.size.toString());
    }
    const queryString = query.toString();
    return request(queryString ? `/categories/paginated?${queryString}` : '/categories/paginated');
}

export async function createCategory(data: CategoryCreate): Promise<Category> {
    return request('/categories/', {
        method: 'POST',
        body: JSON.stringify(data)
    });
}

export async function updateCategory(id: number, data: CategoryCreate): Promise<Category> {
    return request(`/categories/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data)
    });
}

export async function deleteCategory(id: number): Promise<void> {
    return request(`/categories/${id}`, {
        method: 'DELETE'
    });
}

export async function getCategory(id: number): Promise<Category> {
    return request(`/categories/${id}`);
}
