import { request } from '$lib/api';

export interface User {
    id: number;
    email: string;
    full_name: string;
    role: string;
    is_active: boolean;
    created_at: string;
}

export async function listAllUsers(): Promise<User[]> {
    return request('/users/');
}

export async function updateUserRole(userId: number, role: string): Promise<any> {
    return request(`/users/${userId}/role`, {
        method: 'PUT',
        body: JSON.stringify({ role })
    });
}
