import { writable } from 'svelte/store';
import { browser } from '$app/environment';
import { request } from '$lib/api';
import { goto } from '$app/navigation';

interface User {
	id: number;
	email: string;
	full_name: string;
	is_active: boolean;
}

interface AuthState {
	user: User | null;
	token: string | null;
	isAuthenticated: boolean;
	loading: boolean;
}

const initialState: AuthState = {
	user: null,
	token: browser ? localStorage.getItem('access_token') : null,
	isAuthenticated: browser ? !!localStorage.getItem('access_token') : false,
	loading: false
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

				const res = await request('/auth/login', {
					method: 'POST',
					body: formData,
					headers: {
						'Content-Type': 'application/x-www-form-urlencoded'
					}
				});

				const { access_token } = res;
				
				if (browser) {
					localStorage.setItem('access_token', access_token);
				}

				update((s) => ({ ...s, token: access_token, isAuthenticated: true }));
				
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
                await goto('/login');
			} catch (error) {
				console.error('Registration failed', error);
				throw error;
			} finally {
				update((s) => ({ ...s, loading: false }));
			}
		},
		fetchProfile: async () => {
            const token = browser ? localStorage.getItem('access_token') : null;
            if (!token) return;

			update((s) => ({ ...s, loading: true }));
			try {
				const user = await request('/users/me');
				update((s) => ({ ...s, user }));
			} catch (error: any) {
                if (error.status === 401) {
                    auth.logout();
                }
				console.error('Fetch profile failed', error);
			} finally {
				update((s) => ({ ...s, loading: false }));
			}
		},
		logout: () => {
			if (browser) {
				localStorage.removeItem('access_token');
			}
			set({ ...initialState, token: null, isAuthenticated: false });
			goto('/login');
		}
	};
}

export const auth = createAuthStore();
