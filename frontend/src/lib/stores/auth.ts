import { writable } from 'svelte/store';
import { browser } from '$app/environment';
import { request } from '$lib/api';
import { goto } from '$app/navigation';

interface User {
	id: number;
	email: string;
	full_name: string;
	is_active: boolean;
	role: string;
}

interface AuthState {
	user: User | null;
	token: string | null;
	isAuthenticated: boolean;
	loading: boolean;
}

const initialState: AuthState = {
	user: null,
	token: null, // Token is now in cookie, this field is less relevant but keeping for type compat or just null
	isAuthenticated: false,
	loading: true // Start loading to check auth status on mount
};

function createAuthStore() {
	const { subscribe, set, update } = writable<AuthState>(initialState);

	return {
		subscribe,
		login: async (email: string, password: string) => {
			update((s) => ({ ...s, loading: true }));
			try {
				const formData = new URLSearchParams();
				formData.append('username', email);
				formData.append('password', password);

				await request('/auth/login', {
					method: 'POST',
					body: formData,
					headers: {
						'Content-Type': 'application/x-www-form-urlencoded'
					}
				});

                // No need to store token manually. Cookie is set.
                // Just fetch profile to confirm and get user data.
                await auth.fetchProfile();
                
                await goto('/profile');
			} catch (error) {
				console.error('Login failed', error);
				throw error;
			} finally {
				update((s) => ({ ...s, loading: false }));
			}
		},
		register: async (email: string, password: string, fullName: string) => {
			update((s) => ({ ...s, loading: true }));
			try {
				await request('/auth/register', {
					method: 'POST',
					body: JSON.stringify({ email, password, full_name: fullName })
				});
                await goto('/auth/login');
			} catch (error) {
				console.error('Registration failed', error);
				throw error;
			} finally {
				update((s) => ({ ...s, loading: false }));
			}
		},
		fetchProfile: async () => {
			update((s) => ({ ...s, loading: true }));
			try {
                // This request will send the cookie automatically
				const user = await request('/users/me');
				update((s) => ({ ...s, user, isAuthenticated: true }));
			} catch (error: any) {
                // If 401, we are just not logged in.
                if (error.status !== 401) {
				    console.error('Fetch profile failed', error);
                }
                update((s) => ({ ...s, user: null, isAuthenticated: false }));
			} finally {
				update((s) => ({ ...s, loading: false }));
			}
		},
		logout: async () => {
            try {
                await request('/auth/logout', { method: 'POST' });
            } catch (err) {
                console.error("Logout failed", err);
            }
            // Clear local state regardless of server response
			set({ ...initialState, loading: false, isAuthenticated: false });
			goto('/auth/login');
		}
	};
}

export const auth = createAuthStore();
