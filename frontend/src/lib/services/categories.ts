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

export async function getCategories(): Promise<Category[]> {
    return request('/categories/');
}

export async function createCategory(data: CategoryCreate): Promise<Category> {
    return request('/categories/', {
        method: 'POST',
        body: JSON.stringify(data)
    });
}

export async function getCategory(id: number): Promise<Category> {
    return request(`/categories/${id}`);
}
