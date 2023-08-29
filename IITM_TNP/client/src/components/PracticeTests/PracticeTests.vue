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
import { ref, onMounted, computed } from 'vue';
import { useStore } from 'vuex';
import axios from 'axios';
import { useRouter } from 'vue-router';


const store = useStore();
const router = useRouter();
const practice_tests = computed(() => store.getters["get_all_practice_tests"]);
let AllQuestions = ref([])

function redirect(path){
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
// {
//             "name" : "" \n
//             "tags" : [] \n
//             "question_ids" : [] \n
//         }
const showAddTestModal = ref(false);
const newTags = ref([]);
const newName = ref('');
const newQuestionIds = ref([]);
const selectedQuestionIds = computed(() => {
  return newQuestionIds.value;
});
// each question in AllQuestions contains this data
// {
//                     "id" : question.id,
//                     "name" : question.name,
//                     "tags" : question.tags,
//                     "description" : question.description,
//                     "question_type" : question.question_type,
//                     "options" : question.options if question.question_type in ['MCQ','MSQ'] else None,
//                     "correct_answers" : question.correct_answers if question.question_type in ['MCQ','MSQ','NAT'] else None
//                 }
function addTest() {
  // Extract tags into an array
  const tagsArray = newTags.value.split(',').map(tag => tag.trim());
  const selectedIds = selectedQuestionIds.value.map(id => id);

  // Call the createPost action with the new post data
  store.dispatch('addPracticeTest', {
    name: newName.value,
    tags: tagsArray,
    question_ids: selectedIds
  });

  // Reset modal inputs and hide modal
  newName.value = '';
  newTags.value = [];
  showAddTestModal.value = false;
  newQuestionIds.value = []

}

</script>
<template>
  <div>
    <!-- Button to open the "Add Post" modal -->

    <div class="container mt-5">
      <MDBBtn color="primary" class="mb-3" @click="showAddTestModal = true">Add Test</MDBBtn>

      <div class="card mb-4" v-for="test in practice_tests" :key="test.id">
        <div class="card-body">
          <h5 class="card-title">{{ test.name }}</h5>
          <div class="d-flex">
            <small v-for="tag in test.tags" class="text-muted me-2">#{{ tag }}</small>
          </div>
          <div class="card-footer">
            <MDBBtn color="primary" size="sm" class="me-2" @click="redirect(`/test/${test.id}`)">
              Take Test</MDBBtn>
            <MDBBtn color="primary" size="sm" class="me-2">
              Edit</MDBBtn>
            
            <MDBBtn color="danger" size="sm">Delete</MDBBtn>
          </div>
        </div>
      </div>
    </div>
    <!-- Add Post Modal -->
    <MDBModal v-model="showAddTestModal">
      <MDBModalHeader>Add New Test</MDBModalHeader>
      <MDBModalBody>
        <!-- Input for description -->
        <MDBInput type="textarea" v-model="newName" label="Name" />
        <br>
        <!-- Input for tags -->
        <MDBInput v-model="newTags" label="Tags (comma separated)" type="text" />
        <br>
        <!-- Checkbox list for questions -->
        <div>
          <h5>Select Questions:</h5>
          <template v-for="question in AllQuestions" :key="question.id">
            <div class="form-check">
              <input class="form-check-input" type="checkbox" :id="'question_' + question.id" :value="question.id"
                v-model="newQuestionIds">
              <label class="form-check-label" :for="'question_' + question.id">
                {{ question.name }}
              </label>
            </div>
          </template>
        </div>
      </MDBModalBody>
      <MDBModalFooter>
        <MDBBtn color="secondary" @click="showAddTestModal = false">Cancel</MDBBtn>
        <MDBBtn color="primary" @click="addTest">Add</MDBBtn>
      </MDBModalFooter>
    </MDBModal>
  </div>
</template>