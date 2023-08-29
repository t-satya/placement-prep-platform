<script setup>
import {
    MDBBtn,
    MDBRow,
    MDBCol,
    MDBInput,
    MDBCheckbox,
    MDBRadio
} from 'mdb-vue-ui-kit';
import { ref, watch } from 'vue';
import Select from '../General/Select.vue';
import { ADMIN_REGISTER_URL_BACKEND } from "../../utils/constants.js";
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();

const email = ref("");
const name = ref("");
const username = ref("");
const password = ref("");
const confirm_password = ref("");
const github_link = ref("");
const linkedin_link = ref("");

const check = ref(false);
const passwordType = ref("password");
const selectedOption = ref(0);
const error = ref("");

const option_list = [
    {
        id: 0,
        name: "SupportStaff"
    }
]

function register() {
    const data = {
        email: email.value,
        password: password.value,
        confirm_password: confirm_password.value,
        name: name.value,
        username: username.value,
        level: option_list[selectedOption.value].name,
        github_link: github_link.value,
        linkedin_link: linkedin_link.value
    }

    const options = {
        headers: {
            "content-type": "application/json",
            "Authorization":`Bearer ${localStorage.getItem("jwt_token")}`
        }
    }
    axios.post(ADMIN_REGISTER_URL_BACKEND, data, options).then((res) => {
        console.log(res.data)
        alert("Admin Registered Successfully");
        router.push("/posts")
    }).catch((err) => {
        if (err.response.data.msg) error.value = err.response.data.msg;
        else error.value = "Something went wrong!"
    })

}

watch(check, (newVal, oldVal) => {
    if (newVal) {
        passwordType.value = "text";
    }
    else {
        passwordType.value = "password";
    }
})


</script>

<template>
    <div class="d-flex justify-content-center align-items-center">
        <form class="p-4 rounded bg-white" style="width: 75%; max-width: 500px; min-height: 500px;">
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
                <!-- Name input -->
                <MDBInput type="text" label="Full Name" id="name" v-model="name" wrapperClass="mb-4" />
                <!-- Username input -->
                <MDBInput type="text" label="Username" id="username" v-model="username" wrapperClass="mb-4" />
                <!-- Password input -->
                <MDBInput :type="passwordType" label="Password" id="password" v-model="password" wrapperClass="mb-4" />
                <!-- Confirm Password input -->
                <MDBInput :type="passwordType" label="Confirm Password" id="confirm_password" v-model="confirm_password"
                    wrapperClass="mb-4" />
                <!-- Github URL input -->
                <MDBInput type="text" label="Github URL" id="github_link" v-model="github_link" wrapperClass="mb-4" />
                <!-- LinkedIn URL input -->
                <MDBInput type="text" label="LinkedIn URL" id="linkedin_link" v-model="linkedin_link" wrapperClass="mb-4" />
                <!-- Select Levels input -->
                <Select v-model="selectedOption" title="Choose Your Level" :option_list="option_list" />

                <MDBRow class="mb-4">
                    <MDBCol>
                        <MDBCheckbox label="Show Password" id="check" v-model="check" wrapperClass="mb-3 mb-md-0"/>
                    </MDBCol>
                </MDBRow>
                <!-- Submit button -->
                <div class="text-center">
                    <MDBBtn color="primary" class="text-center" @click="register"> Register </MDBBtn>
                </div>
            </div>
        </form>
    </div>
</template>