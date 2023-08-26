<script setup>
import { onMounted } from 'vue';
import { RouterView } from 'vue-router';
import Navbar from './components/Navbar/Navbar.vue';
import Auth from './components/Auth/Auth.vue';

</script>

<template>
  <Auth />
  <div class="app-container">
    <div class="navbar-view-container">
      <Navbar />
    </div>
    <div class="router-view-container">
      <main>
        <RouterView />
      </main>
    </div>

  </div>
</template>
