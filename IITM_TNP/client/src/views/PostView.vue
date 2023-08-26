<script setup>
import { useStore } from 'vuex';
import { computed } from 'vue';
import Posts from "../components/Posts/Post.vue"
const store = useStore();
const loggedIn = computed(() => store.getters.get_login_status);
const loading = computed(() => store.getters.get_loading_status);
const role = computed(() => store.getters.get_role);
console.log(loggedIn.value)

</script>
<template>
    <div v-if="loading">
        loading...
    </div>
    <div v-else>
        <p v-if="loggedIn">
            <p v-if="role">{{ role }}</p>
            LoggedIn
        </p>
        <p v-else>LoggedOut</p>

    </div>
    <Posts/>
</template>