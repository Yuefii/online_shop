import { browser } from '$app/environment';

export const BASE_URL = 'http://localhost:8000';

interface RequestOptions extends RequestInit {
	token?: string;
}

export async function request(endpoint: string, options: RequestOptions = {}) {
	const url = `${BASE_URL}${endpoint}`;
	const headers = new Headers(options.headers);

	if (options.token) {
		headers.set('Authorization', `Bearer ${options.token}`);
	} else if (browser) {
		const token = localStorage.getItem('access_token');
		if (token) {
			headers.set('Authorization', `Bearer ${token}`);
		}
	}

	if (!headers.has('Content-Type') && !(options.body instanceof FormData)) {
		headers.set('Content-Type', 'application/json');
	}

	const response = await fetch(url, {
		...options,
		headers
	});

    let data;
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
        data = await response.json();
    } else {
        data = await response.text();
    }

	if (!response.ok) {
        let message = data.message || 'Something went wrong';
        
        if (data.detail) {
            if (typeof data.detail === 'string') {
                message = data.detail;
            } else if (Array.isArray(data.detail)) {
                message = data.detail.map((err: any) => `${err.loc.join('.')}: ${err.msg}`).join('\n');
            }
        }

		return Promise.reject({
            status: response.status,
            message: message,
            data
        });
	}

	return data;
}
