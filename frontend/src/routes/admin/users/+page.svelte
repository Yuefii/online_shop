<script lang="ts">
  import { onMount } from 'svelte';
  import { listAllUsers, updateUserRole, type User } from '$lib/services/users';

  let users: User[] = $state([]);
  let loading = $state(true);

  onMount(async () => {
    await fetchUsers();
  });

  async function fetchUsers() {
    loading = true;
    try {
      users = await listAllUsers();
    } catch (err) {
      console.error(err);
      alert('Failed to load users');
    } finally {
      loading = false;
    }
  }

  async function handleRoleChange(userId: number, event: Event) {
    const select = event.target as HTMLSelectElement;
    const newRole = select.value;
    
    // Optimistic update? Or wait? Let's wait to be safe.
    const originalRole = users.find(u => u.id === userId)?.role;
    
    try {
        await updateUserRole(userId, newRole);
        // Success
    } catch (err) {
        console.error(err);
        alert('Failed to update role');
        // Revert
        if (originalRole) select.value = originalRole;
    }
  }
</script>

<h1 class="text-2xl font-bold mb-6">User Management</h1>

{#if loading}
	<div class="flex justify-center p-12">
		<div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
	</div>
{:else}
	<div class="bg-white shadow-sm rounded-lg overflow-hidden border border-gray-200">
		<table class="min-w-full divide-y divide-gray-200">
			<thead class="bg-gray-50">
				<tr>
					<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
						>ID</th
					>
					<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
						>Name</th
					>
					<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
						>Email</th
					>
					<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
						>Role</th
					>
				</tr>
			</thead>
			<tbody class="bg-white divide-y divide-gray-200">
				{#each users as user}
					<tr>
						<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">#{user.id}</td>
						<td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
							>{user.full_name || '-'}</td
						>
						<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{user.email}</td>
						<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
							<select
								class="block w-32 pl-3 pr-10 py-1 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
								value={user.role}
								onchange={(e) => handleRoleChange(user.id, e)}
							>
								<option value="user">User</option>
								<option value="admin">Admin</option>
							</select>
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
{/if}
