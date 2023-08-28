<script setup>
import { computed, onMounted } from 'vue';
import { RouterView } from 'vue-router';
import UserNavbar from './components/Navbar/UserNav.vue';
import AdminNavbar from "./components/Navbar/AdminNav.vue";
import SuperAdminNavbar from "./components/Navbar/SuperAdminNav.vue";
import { useStore } from 'vuex';
import Auth from './components/Auth/Auth.vue';

const store = useStore();
const loggedIn = computed(() => store.getters.get_login_status);
const role = computed(() => store.getters.get_role);


</script>

<template>
  <Auth></Auth>
  <div class="app-container">
    <div class="navbar-view-container">
      <AdminNavbar v-if="role == 'admin' && loggedIn" />
      <SuperAdminNavbar v-else-if="role == 'super admin' && loggedIn" />
      <UserNavbar v-else />
    </div>
    <div class="router-view-container">
      <main>
        <RouterView />
      </main>
    </div>

  </div>
</template>
