<!--
 Copyright 2025 James G Willmore
 
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
 
     https://www.apache.org/licenses/LICENSE-2.0
 
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
-->

<script setup lang="ts">

const props = defineProps<{
  modelValue: Property[]
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: Property[]): void
}>()

const model = computed({
  get: () => props.modelValue as Property[],
  set: (val: Property[]) => emit('update:modelValue', val)
})

const newProperty = reactive<Property>({
  key: '',
  value: ''
})

const addProperty = () => {
  if (!newProperty.key.trim()) return
  model.value.push({ key: newProperty.key, value: newProperty.value })
  newProperty.key = ''
  newProperty.value = ''
}

const deleteProperty = (index: number) => {
  model.value.splice(index, 1)
}
</script>

<template>
  <div class="space-y-4 p-4 bg-white shadow rounded">
    <h2 class="text-lg font-semibold">Manage Properties</h2>

    <form class="flex gap-2 items-end" @submit.prevent="addProperty">
      <UInput v-model="newProperty.key" placeholder="Key" class="flex-1" required />
      <UInput v-model="newProperty.value" placeholder="Value" class="flex-1" />
      <UButton type="submit" class="bg-blue-600 text-white">Add</UButton>
    </form>

    <div class="divide-y border-t mt-4">
        <template v-if="model.length">
            <ul>
            <li
            v-for="(prop, index) in model"
            :key="`${index}-${prop.key}`"
            class="flex gap-2 items-center py-2"
            >
            <UInput
                v-model="prop.key"
                type="text"
                placeholder="Key"
                class="flex-1"
            />
            <UInput
                v-model="prop.value"
                type="text"
                placeholder="Value"
                class="flex-1"
            />
            <UButton
                icon="bi-trash"
                @click="deleteProperty(index)"
            />
            </li>
            </ul>
        </template>
        <template v-else>
            <div class="text-gray-400 text-sm py-4">No properties added.</div>
        </template>
    </div>
  </div>
</template>
