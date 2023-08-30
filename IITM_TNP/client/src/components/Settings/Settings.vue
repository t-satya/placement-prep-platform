<script setup>
import {
    MDBBtn,
    MDBRow,
    MDBCol,
    MDBInput,
    MDBCheckbox
} from 'mdb-vue-ui-kit';
import { ref, watch,onMounted,computed } from 'vue';
import { useRouter } from 'vue-router';
import {useStore} from "vuex"
const router = useRouter();
const store = useStore()
const github_link = ref("");
const linkedin_link = ref("");
const name = ref("")
const user_id = computed(()=>store.getters.get_user_id)
const user_data = computed(()=>store.getters.get_user_data)
watch(user_data, (newUserData) => {
    if (newUserData) {
        github_link.value = newUserData.github_link
        linkedin_link.value = newUserData.linkedin_link
        name.value = newUserData.name
    }
})

onMounted(() => {
    github_link.value="";
    linkedin_link.value="";
    name.value="";
    console.log(user_id)
    console.log(user_data.value)
    store.dispatch("fetchUserData",user_id.value)
})

function update_profile(){
    store.dispatch("updateUserData",{
        "name":name.value,
        "linkedin_link":linkedin_link.value,
        "github_link":github_link.value
    },user_id.value)
    alert("Updated Successfully")
}
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
                <MDBInput type="email" label="Email address" id="email" disabled v-model="user_data.email" wrapperClass="mb-4" />
                <!-- Name input -->
                <MDBInput type="text" label="Full Name" id="name" v-model="name" wrapperClass="mb-4" />
                <!-- Username input -->
                <MDBInput type="text" label="Username" id="username" disabled v-model="user_data.username" wrapperClass="mb-4" />
                
                <!-- Github URL input -->
                <MDBInput type="text" label="Github URL" id="github_link" v-model="github_link" wrapperClass="mb-4" />
                <!-- LinkedIn URL input -->
                <MDBInput type="text" label="LinkedIn URL" id="linkedin_link" v-model="linkedin_link" wrapperClass="mb-4" />
                
                <!-- Submit button -->
                <div class="text-center">
                    <MDBBtn color="primary" class="text-center" @click="update_profile"> Update Profile </MDBBtn>
                </div>
            </div>
        </form>
    </div>
</template>