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
import { BaseTransitionPropsValidators, computed, onMounted, ref } from "vue";
import axios from 'axios';
import { ADD_QUESTION_URL_BACKEND } from "../../utils/constants";
import { useStore } from 'vuex';


const viewQuestionModal = ref(false);
const name = ref("");
const tag = ref("");
const tags = ref([]);
const ques_type = ref("");
const description = ref("");
const option = ref("");
const options = ref([]);
const correct_option = ref("");
const correct_answers = ref([]);

const error = ref("");
const loadingButton = ref(false);

const store = useStore();
const questions = computed(() => store.getters.get_questions);

const props = defineProps({
    id: Number
});


function addTags() {
    if (tag.value != "") tags.value.push(tag.value);
    tag.value = ""
}

function addOptions() {
    if (option.value != "") options.value.push(option.value);
    option.value = "";
}

function addCorrectAnswers() {
    if (correct_option.value != "") correct_answers.value.push(correct_option.value);
    correct_option.value = "";
}

function editQuestion() {
    const convertedOptions = {};

    options.value.forEach((option, index) => {
        convertedOptions[index + 1] = option;
    });

    const data = {
        question_id: questions.value[props.id].id,
        name: name.value,
        tags: tags.value,
        description: description.value,
        question_type: ques_type.value,
        options: convertedOptions,
        correct_answers: correct_answers.value
    }

    console.log(data)
    const config = {
        headers: {
            "Authorization": "Bearer " + localStorage.getItem("jwt_token")
        }
    }
    axios.put(ADD_QUESTION_URL_BACKEND, data, config).then((res) => {
        data.id = questions.value[props.id].id;
        delete data.question_id;

        store.dispatch("updateQuestionAction", { data: { question: data, index: props.id } })
        viewQuestionModal.value = false;
    }).catch((err) => {
        if (err.response) {
            if (err.response.data.msg) error.value = err.response.data.msg;
            else error.value = "Something went wrong!";
        }
        else error.value = "Something went wrong!";
        loadingButton.value = false;
    })
}

onMounted(() => {
    const question = questions.value[props.id];
    if (question) {
        name.value = question.name;
        tags.value = question.tags;
        ques_type.value = question.question_type;
        description.value = question.description;
        if (question.options) options.value = Object.values(question.options);
        if (question.correct_answers) correct_answers.value = question.correct_answers;

    }
});

</script>

<template>
    <MDBBtn color="link" size="sm" rounded aria-controls="viewQuestionModalTitle" @click="viewQuestionModal = true">
        Edit
    </MDBBtn>
    <MDBModal id="viewQuestionModal" tabindex="-1" labelledby="viewQuestionModalTitle" v-model="viewQuestionModal"
        scrollable>
        <MDBModalHeader>
            <MDBModalTitle id="viewQuestionModalTitle"> Edit Question </MDBModalTitle>
        </MDBModalHeader>
        <MDBModalBody>
            <form>
                <MDBInput type="text" label="Name of Question" id="name" v-model="name" wrapperClass="mb-4" />
                <MDBInput v-model="tag" inputGroup :formOutline="false" wrapperClass="mb-4" placeholder="Add Tags"
                    aria-label="tags" aria-describedby="button-addon1">
                    <MDBBtn color="primary" @click="addTags">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                            class="bi bi-plus-circle" viewBox="0 0 16 16">
                            <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z" />
                            <path
                                d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z" />
                        </svg>
                    </MDBBtn>
                </MDBInput>
                <div v-if="tags.length != 0" class="m-2">
                    <h6>Tags</h6>
                    <MDBInput type="text" v-for="(tag, index) in tags" :key="index" :label="index + 1 + '. ' + tag"
                        id="tags" disabled wrapperClass="mb-1" />
                </div>

                <MDBRadio label="MSQ" value="MSQ" v-model="ques_type" inline name="inlineRadioOptions" />
                <MDBRadio label="MCQ" value="MCQ" v-model="ques_type" inline name="inlineRadioOptions" />
                <MDBRadio label="NAT" value="NAT" v-model="ques_type" inline name="inlineRadioOptions" />
                <MDBRadio label="Coding" value="Coding" v-model="ques_type" inline name="inlineRadioOptions"
                    wrapperClass="mb-4" />
                <MDBTextarea label="Description" id="description" v-model="description" wrapperClass="mb-4" />

                <MDBInput v-if="ques_type == 'MSQ' || ques_type == 'MCQ'" v-model="option" inputGroup :formOutline="false"
                    wrapperClass="mb-4" placeholder="Add Option" aria-label="Option" aria-describedby="button-addon2">
                    <MDBBtn color="primary" @click="addOptions">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                            class="bi bi-plus-circle" viewBox="0 0 16 16">
                            <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z" />
                            <path
                                d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z" />
                        </svg>
                    </MDBBtn>
                </MDBInput>
                <div v-if="options.length != 0" class="m-2">
                    <h6>Options</h6>
                    <MDBInput type="text" v-for="(option, index) in options" :key="index" :label="index + 1 + '. ' + option"
                        id="options" disabled wrapperClass="mb-1" />
                </div>
                <MDBInput v-if="ques_type == 'MSQ' || ques_type == 'MCQ' || ques_type == 'NAT'" v-model="correct_option"
                    inputGroup :formOutline="false" wrapperClass="mb-4" placeholder="Correct Option(s) / Answer(s)"
                    aria-label="answer" aria-describedby="button-addon3">
                    <MDBBtn color="primary" @click="addCorrectAnswers">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                            class="bi bi-plus-circle" viewBox="0 0 16 16">
                            <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z" />
                            <path
                                d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z" />
                        </svg>
                    </MDBBtn>
                </MDBInput>
                <div v-if="correct_answers.length != 0" class="m-2">
                    <h6>Answers</h6>
                    <MDBInput type="text" v-for="(answer, index) in correct_answers" :key="index" :label="answer"
                        id="answer" disabled wrapperClass="mb-1" />
                </div>
            </form>
        </MDBModalBody>
        <MDBModalFooter>
            <MDBBtn color="secondary" @click="viewQuestionModal = false"> Close </MDBBtn>
            <MDBBtn color="primary" @click="editQuestion"> Save edits </MDBBtn>
        </MDBModalFooter>
    </MDBModal>
</template>