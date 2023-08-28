<script setup>
import {
    MDBModal,
    MDBModalHeader,
    MDBModalTitle,
    MDBModalBody,
    MDBModalFooter,
    MDBBtn,
    MDBInput,
    MDBTextarea,
    MDBRadio,
} from 'mdb-vue-ui-kit';
import { computed, onMounted, ref } from "vue";
import axios from 'axios';
import { DELETE_QUESTIONS_ADMIN_URL_BACKEND } from "../../utils/constants";
import { useStore } from 'vuex';


const deleteQuestionModal = ref(false);


const store = useStore();
const questions = computed(() => store.getters.get_questions);

const props = defineProps({
    id: Number,
    name: String
});

function deleteQuestion() {
    const question = questions.value[props.id];
    if (question) {
        const config = {
            headers: {
                "Authorization": "Bearer " + localStorage.getItem("jwt_token")
            }


        }
        const url = `${DELETE_QUESTIONS_ADMIN_URL_BACKEND}/${question.id}`;

        axios.delete(url, config).then((res) => {
            store.dispatch("deleteQuestionAction", { data: { index: props.id } })
        }).catch(() => {
            alert("Something went wrong")
        });
    }
}

// function submitQuestion() {
//     const convertedOptions = {};

//     options.value.forEach((option, index) => {
//         convertedOptions[index + 1] = option;
//     });

//     const data = {
//         name: name.value,
//         tags: tags.value,
//         description: description.value,
//         question_type: ques_type.value,
//         options: convertedOptions,
//         correct_answers: correct_answers.value
//     }
//     const config = {
//         headers: {
//             "Authorization": "Bearer " + localStorage.getItem("jwt_token")
//         }
//     }
//     axios.post(ADD_QUESTION_URL_BACKEND, data, config).then((res) => {
//         store.dispatch("addQuestionAction", { data: { question: [data] } })
//         deleteQuestionModal.value = false;
//     }).catch((err) => {
//         if (err.response) {
//             if (err.response.data.msg) error.value = err.response.data.msg;
//             else error.value = "Something went wrong!";
//         }
//         else error.value = "Something went wrong!";
//         loadingButton.value = false;
//     })
// }



</script>

<template>
    <MDBBtn color="link" size="sm" rounded aria-controls="deleteQuestionModalTitle" @click="deleteQuestionModal = true">
        Delete
    </MDBBtn>
    <MDBModal id="deleteQuestionModal" tabindex="-1" labelledby="deleteQuestionModalTitle" v-model="deleteQuestionModal"
        scrollable>
        <MDBModalHeader>
            <MDBModalTitle id="deleteQuestionModalTitle"> Delete Question </MDBModalTitle>
        </MDBModalHeader>
        <MDBModalBody>
            <div class="alert alert-danger d-flex align-items-center" role="alert">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-trash3"
                    viewBox="0 0 16 16">
                    <path
                        d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5ZM11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H2.506a.58.58 0 0 0-.01 0H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1h-.995a.59.59 0 0 0-.01 0H11Zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5h9.916Zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47ZM8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5Z" />
                </svg>
                <div class="ms-4">
                    Are you sure you want to proceed with the deletion?
                    <br />
                    You are going to delete question <strong>{{ name }}</strong>.
                </div>
            </div>
        </MDBModalBody>
        <MDBModalFooter>
            <MDBBtn color="secondary" @click="deleteQuestionModal = false"> Close </MDBBtn>
            <MDBBtn color="danger" @click="deleteQuestion"> Delete </MDBBtn>
        </MDBModalFooter>
    </MDBModal>
</template>

<style></style>