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

export enum ComponentType {
  HARDWARE = "hardware",
  SOFTWARE = "software",
  DATABASE = "database",
  PEOPLE = "people",
  PROCESS = "process"
}

export const componentTypeOptions = Object.values(ComponentType).map(value => ({
  label: value.charAt(0).toUpperCase() + value.slice(1),
  value
}))

export interface Property {
  key: string
  value: string
}

export interface SystemBase {
    name: string
    // description?: string
    properties?: Property[] //Record<string, unknown>
    // metadata?: Record<string, unknown>
}

export interface System extends SystemBase {
    id: string
    // created_at: string
    // updated_at: string
}

export interface ComponentBase {
    name: string
    type: ComponentType
    // description?: string
    // system_id?: string
    properties?: Property[] //Record<string, unknown>
    // metadata?: Record<string, unknown>
}

// Renamed from 'Component' to 'ComponentItem' to avoid conflict with Vue's Component
export interface ComponentItem extends ComponentBase {
    id: string
    // created_at: string
    // updated_at: string
}
