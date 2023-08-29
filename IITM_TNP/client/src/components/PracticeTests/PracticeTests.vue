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
// {
//             "practice_test_id" : ""\n
//             "name" : "" \n
//             "tags" : [] \n
//             "question_ids_to_remove" : [] \n
//             "question_ids_to_add" : [] \n
//         }
const edit_test_name = ref("");
const edit_test_id = ref()
const edit_test_tags = ref([]);
const edit_test_ques_ids = ref([])
const showEditTestModal = ref(false)
let current_test_ids = []
let old_test_ids = []

function openEditModal(test_id, test_name, test_tags, test_ques_ids) {
  current_test_ids = [];
  edit_test_id.value = test_id;
  edit_test_name.value = test_name;
  // edit_test_tags.value=test_tags;
  for (const eachid of test_ques_ids) {
    current_test_ids.push(eachid);
    old_test_ids.push(eachid)
  }
  console.log(current_test_ids)
  edit_test_ques_ids.value = test_ques_ids;
  console.log(test_ques_ids)
  if (Array.isArray(test_tags)) {
    edit_test_tags.value = test_tags.join(', '); // Convert array to comma-separated string
  } else if (typeof tags === 'string') {
    edit_test_tags.value = test_tags;
  } else {
    edit_test_tags.value = '';
  }

  showEditTestModal.value = true;
  console.log(edit_test_name.value, edit_test_tags.value, edit_test_ques_ids.value)

}
function closeEditModal() {
  edit_test_name.value = "";
  edit_test_tags.value = [];
  edit_test_ques_ids.value = [];
  showEditTestModal.value = false;
  current_test_ids = []
  old_test_ids = []
}

function submitEditModal(){
  const editedTest = {
    practice_test_id: edit_test_id.value,
    name: edit_test_name.value,
    tags: edit_test_tags.value.split(',').map(tag => tag.trim()),
    question_ids_to_remove: old_test_ids.filter(id => !current_test_ids.includes(id)),
    question_ids_to_add: current_test_ids.filter(id => !old_test_ids.includes(id))
  };
  store.dispatch("editPracticeTest",editedTest)
  closeEditModal();
}
watch(current_test_ids, (new_current_test_ids) => {
  if (new_current_test_ids) {
    current_test_ids = new_current_test_ids;
  }
})
watch(old_test_ids, (new_test_ids) => {
  if (new_test_ids) {
    old_test_ids = new_test_ids;
  }
})

function toggleQuestionSelection(questionId) {
  const index = current_test_ids.indexOf(questionId);
  if (index === -1) {
    current_test_ids.push(questionId);
  } else {
    current_test_ids.splice(index, 1);
  }

}
const testToDelete = ref(null);
const showDeleteModal = ref(false)

function openDeleteModal(testId) {
  showDeleteModal.value = true
  testToDelete.value = testId;

}

function closeDeleteModal() {
  testToDelete.value = null;
  showDeleteModal.value = false;
}

async function confirmDelete() {
  if (testToDelete.value !== null) {
    store.dispatch('deletePracticeTest', testToDelete.value);

    testToDelete.value = null;
    closeDeleteModal();
  }
}
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


            <MDBBtn color="primary" size="sm" class="me-2"
              @click="openEditModal(test.id, test.name, test.tags, test.ques_ids)">
              Edit</MDBBtn>

            <MDBBtn color="danger" size="sm" @click="openDeleteModal(test.id)">Delete</MDBBtn>
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

    <!-- Add Post Modal -->
    <MDBModal v-model="showEditTestModal">
      <MDBModalHeader>Edit Test</MDBModalHeader>
      <MDBModalBody>
        <!-- Input for description -->
        <MDBInput type="textarea" v-model="edit_test_name" label="Name" />
        <br>
        <!-- Input for tags -->
        <MDBInput v-model="edit_test_tags" label="Tags (comma separated)" type="text" />
        <br>
        <!-- Checkbox list for questions -->
        <div>
          <h5>Select Questions:</h5>
          <template v-for="question in AllQuestions" :key="question.id">
            <div class="form-check">
              <input class="form-check-input" type="checkbox" :id="'question_' + question.id" :value="question.id"
                @change="toggleQuestionSelection(question.id)" :checked="current_test_ids.includes(question.id)">
              <label class="form-check-label" :for="'question_' + question.id">
                {{ question.name }}
              </label>
            </div>
          </template>
        </div>
      </MDBModalBody>
      <MDBModalFooter>
        <MDBBtn color="secondary" @click="closeEditModal">Cancel</MDBBtn>
        <MDBBtn color="primary" @click="submitEditModal">Add</MDBBtn>
      </MDBModalFooter>
    </MDBModal>
    <!-- Delete Confirmation Modal -->
    <MDBModal v-model="showDeleteModal">
      <MDBModalHeader>Delete Test</MDBModalHeader>
      <MDBModalBody>
        Are you sure you want to delete this test?
      </MDBModalBody>
      <MDBModalFooter>
        <MDBBtn color="secondary" @click="closeDeleteModal">Cancel</MDBBtn>
        <MDBBtn color="danger" @click="confirmDelete">Delete</MDBBtn>
      </MDBModalFooter>
    </MDBModal>

  </div>
</template>