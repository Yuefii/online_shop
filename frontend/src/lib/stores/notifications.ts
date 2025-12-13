import { writable } from 'svelte/store';
import { request } from '$lib/api';
import { browser } from '$app/environment';

interface NotificationState {
    count: number;
    loading: boolean;
}

const initialState: NotificationState = {
    count: 0,
    loading: false
};

function createNotificationStore() {
    const { subscribe, set, update } = writable<NotificationState>(initialState);
    let pollInterval: ReturnType<typeof setInterval> | null = null;

    async function fetchStats() {
        if (!browser) return; 
        
        try {
            // We assume this is called only when user is admin (guaranteed by layout)
            const data = await request('/orders/admin/stats', { method: 'GET' });
            if (data) {
                update(s => ({ ...s, count: data.pending_count }));
            }
        } catch (e) {
            console.error("Failed to fetch notification stats", e);
        }
    }

    return {
        subscribe,
        startPolling: (intervalMs = 10000) => {
            if (pollInterval) return; // Already polling
            fetchStats(); // Initial fetch
            pollInterval = setInterval(fetchStats, intervalMs);
        },
        stopPolling: () => {
            if (pollInterval) {
                clearInterval(pollInterval);
                pollInterval = null;
            }
        },
        refresh: fetchStats
    };
}

export const notifications = createNotificationStore();
