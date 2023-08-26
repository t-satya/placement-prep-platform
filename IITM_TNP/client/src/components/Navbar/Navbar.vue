<script setup>
import {
    MDBBtn,
    MDBNavbar,
    MDBNavbarToggler,
    MDBNavbarBrand,
    MDBNavbarNav,
    MDBNavbarItem,
    MDBCollapse,
    MDBTabNav,
    MDBTabItem,
    MDBTabs
} from 'mdb-vue-ui-kit';
import { ref, provide } from 'vue';
import { useStore } from 'vuex';
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const store = useStore();
const router = useRouter();

console.log(store)


// States for the component
const loggedIn = computed(() => store.getters.get_login_status);
const collapse1 = ref(false);

// Functions
function logout() {
    store.dispatch("logoutUser");
}

function redirect(path) {
    router.push(path);
}

</script>

<template>
    <MDBNavbar expand="lg" light bg="light" container class="rounded-4">
        <MDBNavbarBrand href="#">
            <a href="/">
                <img src="logo.png" height="45" alt="IITM Logo" loading="lazy" />
            </a>
        </MDBNavbarBrand>
        <MDBNavbarToggler @click="collapse1 = !collapse1" target="#navbarSupportedContent"></MDBNavbarToggler>
        <MDBCollapse v-model="collapse1" id="navbarSupportedContent">
            <MDBNavbarNav class="mb-2 mb-lg-0" right>
                <MDBTabs>
                    <MDBTabNav pills color="primary">
                        <MDBTabItem tabId="practice" v-if="loggedIn" @click="redirect('/practice')">Practice</MDBTabItem>
                        <MDBTabItem tabId="posts" @click="redirect('/posts')">Posts</MDBTabItem>
                        <MDBTabItem tabId="interviews" @click="redirect('/interview')">Interviews</MDBTabItem>
                        <MDBTabItem tabId="logout" v-if="loggedIn" @click="logout">Logout</MDBTabItem>
                        <MDBTabItem tabId="login" v-if="!loggedIn" @click="redirect('/login')">Login</MDBTabItem>
                        <MDBTabItem tabId="register" v-if="!loggedIn" @click="redirect('/register')">Register</MDBTabItem>

                    </MDBTabNav>
                </MDBTabs>
            </MDBNavbarNav>
        </MDBCollapse>
    </MDBNavbar>
</template>