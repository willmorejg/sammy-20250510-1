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

<template>
  <UContainer>
    <UNavigationMenu
      color="neutral"
      variant="link"
      orientation="vertical"
      :items="navItems"
      class="w-64 text-black bg-white"
    />
  </UContainer>
</template>

<script setup lang="ts">
import type { NavigationMenuItem } from '@nuxt/ui'
import { ref } from 'vue'

const navItems = ref<NavigationMenuItem[][]>([
  [
    { label: 'Home', icon: 'bi-house-door-fill', to: '/' },
    { label: 'About', icon: 'bi-question-circle-fill', to: '/about' },
    { label: 'Systems', icon: 'bi-diagram-2-fill', to: '/systems' },
    { label: 'Components', icon: 'bi-laptop-fill', to: '/components' }
  ]
])
</script>
