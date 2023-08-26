<script setup>
import {
    MDBBtn,
    MDBNavbar,
    MDBNavbarToggler,
    MDBNavbarBrand,
    MDBNavbarNav,
    MDBNavbarItem,
    MDBCollapse
} from 'mdb-vue-ui-kit';
import { ref } from 'vue';
import { useStore } from 'vuex';
import { computed } from 'vue';

const store = useStore();

const loggedIn = computed(() => store.getters.get_login_status);

const collapse1 = ref(false);


function logout() {
    store.dispatch("logoutUser")
}


function login() {
    store.dispatch("loginUser")
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
                <MDBNavbarItem v-if="loggedIn" href="#">
                    Practice
                </MDBNavbarItem>
                <MDBNavbarItem to="#" active>
                    Posts
                </MDBNavbarItem>
                <MDBNavbarItem href="#">
                    Interviews
                </MDBNavbarItem>
                <MDBNavbarItem v-if="loggedIn" href="#" @click="logout">
                    Logout
                </MDBNavbarItem>
                <MDBNavbarItem v-else href="#" @click="login">
                    Login
                </MDBNavbarItem>
            </MDBNavbarNav>
        </MDBCollapse>
    </MDBNavbar>
</template>