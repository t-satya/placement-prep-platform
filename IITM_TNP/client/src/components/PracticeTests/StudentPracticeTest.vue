<script setup>
// Imports
import {
  MDBBtn,
  MDBInput,
  MDBModal,
  MDBModalHeader,
  MDBModalBody,
  MDBModalFooter
} from 'mdb-vue-ui-kit';
import { GET_QUESTIONS_ADMIN_URL_BACKEND } from "../../utils/constants";
import { ref, onMounted, computed, watch } from 'vue';
import { useStore } from 'vuex';
import axios from 'axios';
import { useRouter } from 'vue-router';


const store = useStore();
const router = useRouter();
// const practice_tests = computed(() => store.getters["get_all_practice_tests"]);
let AllQuestions = ref([])

function redirect(path) {
  router.push(path)
}
onMounted(() => {
  store.dispatch('fetchPracticeTests');
  // console.log(practice_tests.value);

  if (AllQuestions) {
    const config = {
      headers: {
        "Authorization": "Bearer " + localStorage.getItem("jwt_token")
      }
    }

    axios.get(GET_QUESTIONS_ADMIN_URL_BACKEND, config).then((res) => {
      AllQuestions.value = res.data.questions;
      // console.log(AllQuestions.value)
    }).catch((err) => {
      console.log(err)
    })
  }
  //   console.log(AllQuestions)
})

const props = defineProps({
    search: {
        type: String,
        default: ""
    }
})
const practice_tests = computed(() => {
    const allTests = store.getters.get_all_practice_tests;

    if (props.search)
        return allTests.filter(test =>
            test.name.toLowerCase().includes(props.search.toLowerCase()) ||
            test.tags.some(tag => tag.toLowerCase().includes(props.search.toLowerCase()))
        );
    else return allTests;
});
</script>
<template>
  <div>
    <!-- Button to open the "Add Post" modal -->

    <div class="container mt-5 text-center">

      <div class="card mb-4" v-for="test in practice_tests" :key="test.id">
        <div class="card-body">
          <h5 class="card-title">{{ test.name }}</h5>
          <div class="d-flex">
            <small v-for="tag in test.tags" class="text-muted me-2">#{{ tag }}</small>
          </div>
          <div class="card-footer">
            <MDBBtn color="primary" size="sm" class="me-2" @click="redirect(`/student_test/${test.id}`)">
              Take Test</MDBBtn> 
          </div>
        </div>
      </div>
    </div>
    

  </div>
</template>