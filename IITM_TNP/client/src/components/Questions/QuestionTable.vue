<script setup>
import {
    MDBTable,
    MDBBadge
} from 'mdb-vue-ui-kit';
import { computed, onMounted, ref, watch } from 'vue';
import axios from 'axios';
import { GET_QUESTIONS_ADMIN_URL_BACKEND } from "../../utils/constants";
import { useStore } from 'vuex';
import EditQuestion from './EditQuestion.vue';
import DeleteQuestion from './DeleteQuestion.vue';
const store = useStore();

const props = defineProps({
    search: {
        type: String,
        default: ""
    }
})

const questions = computed(() => {
    const allQuestions = store.getters.get_questions;

    if (props.search)
        return allQuestions.filter(question =>
            question.name.toLowerCase().includes(props.search.toLowerCase()) ||
            question.tags.some(tag => tag.toLowerCase().includes(props.search.toLowerCase()))
        );
    else return allQuestions;
});

onMounted(() => {
    if (questions.value.length == 0) {
        const config = {
            headers: {
                "Authorization": "Bearer " + localStorage.getItem("jwt_token")
            }
        }

        axios.get(GET_QUESTIONS_ADMIN_URL_BACKEND, config).then((res) => {
            // questions.value = res.data.questions;
            store.dispatch("addQuestionAction", { data: { question: res.data.questions } })
        }).catch((err) => {
            console.log(err)
        })
    }
})
</script>

<template>
    <MDBTable class="align-middle mb-0 bg-white" hover responsive>
        <thead class="bg-light">
            <tr>
                <th>#</th>
                <th>Name</th>
                <th>Tags</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="(question, index) in questions" :key="question.id">
                <td>
                    <p class="fw-normal mb-1">{{ index + 1 }}</p>
                </td>
                <td>
                    <p class="fw-normal mb-1">{{ question.name }}</p>
                </td>
                <td>
                    <MDBBadge badge="success" pill class="d-inline" v-for="tag in question.tags" :key="tag">
                        {{ tag }}
                    </MDBBadge>
                </td>
                <td>
                    <EditQuestion :id="index" />
                    <DeleteQuestion :id="index" :name="question.name" />
                </td>
            </tr>
        </tbody>
    </MDBTable>
</template>