<script setup>

// Imports
import {
    MDBBtn,
    MDBRow,
    MDBCol,
    MDBInput,
    MDBCheckbox
} from 'mdb-vue-ui-kit';
import { ref, watch, onMounted } from 'vue';
import { routerKey } from 'vue-router';
import { useStore } from 'vuex';
import axios from 'axios';
import { LOGIN_URL_BACKEND } from '../../utils/constants';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();
const store = useStore();


// States
const email = ref("");
const password = ref("");

const check = ref(false);
const passwordType = ref("password");
const error = ref("");
const message = ref(null);

message.value = route.query.msg || null;

// Functions
function login() {
    const data = {
        email: email.value,
        password: password.value
    }

    const options = {
        headers: {
            "content-type": "application/json"
        }
    }

    axios.post(LOGIN_URL_BACKEND, data, options).then((res) => {
        store.dispatch("loginUser", { data: res.data });
        console.log(store.getters.jwt_token,"login") 
        router.push("/posts");
    }).catch((err) => {
        if (err.response.data.msg) error.value = err.response.data.msg;
        else error.value = "Something went wrong!"
    })

}


// Hooks
watch(check, (newVal, oldVal) => {
    if (newVal) {
        passwordType.value = "text";
    }
    else {
        passwordType.value = "password";
    }
})

onMounted(() => {
    if (store.getters.get_login_status == true) router.push("/posts");

})

</script>

<template>
    <div class="d-flex justify-content-center align-items-center">

        <form class="p-4 rounded bg-white" style="width: 75%; max-width: 500px;">
            <div class="alert alert-success" role="alert" v-if="message">
                {{ message }}
            </div>
            <div class="d-flex flex-column justify-content-center align-items-center h-100">
                <a href="/">
                    <img src="logo.png" height="70" alt="IITM Logo" loading="lazy" />
                </a>
                <br />
                <div class="alert alert-danger" role="alert" v-if="error">
                    {{ error }}
                </div>

                <!-- Email input -->
                <MDBInput type="email" label="Email address" id="email" v-model="email" wrapperClass="mb-4" />
                <!-- Password input -->
                <MDBInput :type="passwordType" label="Password" id="password" v-model="password" wrapperClass="mb-4" />
                <!-- 2 column grid layout for inline styling -->
                <MDBRow class="mb-4">
                    <MDBCol>
                        <!-- Checkbox -->
                        <MDBCheckbox label="Show Password" id="check" v-model="check" wrapperClass="mb-3 mb-md-0" />
                    </MDBCol>
                    <MDBCol>
                        <!-- Simple link -->
                        <a href="#!">Forgot password?</a>
                    </MDBCol>
                </MDBRow>
                <!-- Submit button -->
                <div class="text-center">
                    <MDBBtn color="primary" class="text-center" @click="login"> Login </MDBBtn>
                </div>
            </div>
        </form>
    </div>
</template>