// Copyright 2025 James G Willmore
// 
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// 
//     https://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

export const useApi = () => {
    const config = useRuntimeConfig()
    const baseURL = config.public.apiBaseUrl

    const $apiFetch = <T>(url: string, options?: any): Promise<T> => {
        return $fetch<T>(url, {
            baseURL,
            headers: {
                'Content-Type': 'application/json'
            },
            ...options
        }).catch(handleError)
    }

    const handleError = (error: any): never => {
        console.error('API Error:', error)
        let message = 'An error occurred while communicating with the server.'

        if (error.data?.detail) {
            message = error.data.detail
        } else if (error.status) {
            message = `Server error: ${error.status}`
        } else if (error.message) {
            message = error.message
        }

        throw new Error(message)
    }

    const systemsApi = {
        getAll: () => $apiFetch<System[]>('/systems/'),
        get: (id: string) => $apiFetch<System>(`/systems/${id}`),
        create: (system: SystemBase) => $apiFetch<System>('/systems/', { method: 'POST', body: system }),
        update: (id: string, system: SystemBase) => $apiFetch<System>(`/systems/${id}`, { method: 'PUT', body: system }),
        delete: (id: string) => $apiFetch(`/systems/${id}`, { method: 'DELETE' }).then(() => true)
    }

    const componentsApi = {
        getAll: () => $apiFetch<ComponentItem[]>('/components/'),
        get: (id: string) => $apiFetch<ComponentItem>(`/components/${id}`),
        create: (component: ComponentBase) => $apiFetch<ComponentItem>('/components/', { method: 'POST', body: component }),
        update: (id: string, component: ComponentBase) => $apiFetch<ComponentItem>(`/components/${id}`, { method: 'PUT', body: component }),
        delete: (id: string) => $apiFetch(`/components/${id}`, { method: 'DELETE' }).then(() => true)
    }

    return {
        systemsApi,
        componentsApi
    }
}
