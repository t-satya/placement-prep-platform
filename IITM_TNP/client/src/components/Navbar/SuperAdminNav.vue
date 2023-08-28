<script setup>
import {
    MDBBtn,
    MDBNavbar,
    MDBNavbarToggler,
    MDBNavbarBrand,
    MDBNavbarNav,
    MDBNavbarItem,
    MDBCollapse,
    MDBTabs,
    MDBTabItem,
    MDBTabNav
} from 'mdb-vue-ui-kit';
import { ref } from 'vue';
import { useStore } from 'vuex';
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const store = useStore();
const router = useRouter();

const loggedIn = computed(() => store.getters.get_login_status);

const collapse1 = ref(false);


function logout() {
    store.dispatch("logoutUser")
}


function login() {
    store.dispatch("loginUser")
}

function redirect(path) {
    router.push(path);
}

</script>

<template>
    <MDBNavbar expand="lg" light bg="light" container class="rounded-4">
        <MDBNavbarBrand href="#">
            <a href="#">
                <img src="logo.png" height="45" alt="IITM Logo" loading="lazy" />
            </a>
        </MDBNavbarBrand>
        <MDBNavbarToggler @click="collapse1 = !collapse1" target="#navbarSupportedContent"></MDBNavbarToggler>
        <MDBCollapse v-model="collapse1" id="navbarSupportedContent">
            <MDBNavbarNav class="mb-2 mb-lg-0" right>
                <MDBTabs>
                    <MDBTabNav pills color="primary">
                        <MDBTabItem tabId="posts" @click="redirect('/posts')">Posts</MDBTabItem>
                        <MDBTabItem tabId="interviews" @click="redirect('/interview')">Interviews</MDBTabItem>
                        <MDBTabItem tabId="practice" @click="redirect('/admin/practice_tests')">Practice</MDBTabItem>
                        <MDBTabItem tabId="questions" @click="redirect('/admin/questions')">Questions</MDBTabItem>
                        <MDBTabItem tabId="logout" v-if="loggedIn" @click="logout">Logout</MDBTabItem>
                        <MDBTabItem tabId="login" v-else @click="login">Logout</MDBTabItem>
                    </MDBTabNav>
                </MDBTabs>
                <!-- <MDBNavbarItem v-if="loggedIn" href="#" @click="logout">
                    Logout
                </MDBNavbarItem> -->
                <!-- <MDBNavbarItem v-else href="#" @click="login">
                    Login
                </MDBNavbarItem> -->
            </MDBNavbarNav>
        </MDBCollapse>
    </MDBNavbar>
</template>