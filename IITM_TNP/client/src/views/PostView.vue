<script setup>
import { useStore } from 'vuex';
import { computed } from 'vue';
import Posts from "../components/Posts/Post.vue"
import { MDBInput, MDBBtn } from 'mdb-vue-ui-kit';
import { ref } from 'vue';

const search = ref("");
const store = useStore();
const loggedIn = computed(() => store.getters.get_login_status);
const loading = computed(() => store.getters.get_loading_status);
const role = computed(() => store.getters.get_role);
console.log(loggedIn.value)

</script>
<template>
    <div class="d-flex justify-content-end mb-2">
        <div>
            <MDBInput v-model="search" inputGroup :formOutline="false" wrapperClass="mb-3" placeholder="Search"
                aria-label="Search" aria-describedby="button-addon2">
                <MDBBtn color="primary">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-search"
                        viewBox="0 0 16 16">
                        <path
                            d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z" />
                    </svg>
                </MDBBtn>
            </MDBInput>
        </div>
        
    </div>
    <Posts :search="search"/>
</template>