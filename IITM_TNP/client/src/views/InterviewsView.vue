<script setup>
import { useStore } from 'vuex';
import { computed } from 'vue';
import Interviews from "../components/Interviews/interviews.vue"

const store = useStore();
const loggedIn = computed(() => store.getters.get_login_status);
console.log(loggedIn.value)

</script>
<template>
    <Interviews/>
</template>