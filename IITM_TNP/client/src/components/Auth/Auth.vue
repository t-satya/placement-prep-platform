<script setup>
import { onMounted } from 'vue';
import { useStore } from 'vuex';
import { VERIFY_TOKEN_URL_BACKEND } from '../../utils/constants';
import axios from 'axios';

const store = useStore();

onMounted(() => {

    const token = localStorage.getItem("jwt_token");

    if (token) {
        const options = {
            headers: {
                "Authorization": "Bearer " + token
            }
        }
        axios.get(VERIFY_TOKEN_URL_BACKEND, options).then((res) => {
            store.dispatch("loginUser", { data: { name: res.data.name, role: res.data.role } })
        })
            .catch((err) => {
                store.dispatch("setLoadingStatus", { data: { loading: false } })
            })
    }
    else {
        store.dispatch("setLoadingStatus", { data: { loading: false } })
    }
})
</script>

<template>
    <div></div>
</template>
