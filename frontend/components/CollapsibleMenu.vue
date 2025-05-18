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
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const open = ref(false)
const route = useRoute()

// Close collapsible on every route change
watch(() => route.fullPath, () => {
    open.value = false
})
</script>

<template>
    <USlideover v-model:open="open" class="fixed top-4 right-4 z-50 rounded-full bg-white text-black w-10 h-10 flex items-center justify-center">
        <UButton class="font-bold rounded-full bg-neutral-600 text-white w-10">
            <span class="bi-list" />
        </UButton>

        <template #content>
            <UButton class="font-bold rounded-full bg-neutral-600 text-white w-10" @click="open = false">
                <span class="bi-x-circle-fill" />
            </UButton>
            <AppNavBar />
        </template>
    </USlideover>
</template>
