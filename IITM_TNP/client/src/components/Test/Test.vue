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
import { useRoute } from 'vue-router';

// Use the useRoute function to access the route object
const route = useRoute();
const store = useStore();
const router = useRouter();
const practice_test = computed(() => store.getters.get_current_test);
const test_id = computed(() => route.params.id)
const selectedAnswers = ref({});
const correctAnswers = ref({});
let submitted = false;
const optionColors = ref({}); // Reactive ref to store option colors
const nat_input = ref();
function updateseletedAnswers() {
  watch(practice_test, (newPracticeTest) => {
    if (newPracticeTest) {
      const questionsArray = newPracticeTest.questions;
      for (const ques of questionsArray) {

        selectedAnswers.value[ques.id] = []
      }
    }
  })
}
function redirect(path) {
  router.push(path)
}
onMounted(() => {
  store.dispatch('fetchAPracticeTest', test_id.value);
  updateseletedAnswers();
})
// Watch for changes in practice_test
watch(practice_test, (newPracticeTest) => {
  if (newPracticeTest) {
    const questionsArray = newPracticeTest.questions;
    console.log(questionsArray)
    for (const ques of questionsArray) {
      correctAnswers.value[ques.id] = ques.correct_answers
    }
  }
})
function selectedMCQ(ques_id, opted) {
  selectedAnswers.value[ques_id] = [opted];
}
function selectedMSQ(ques_id, opted) {
  if (!selectedAnswers.value[ques_id]) {
    selectedAnswers.value[ques_id] = []; // Initialize the array if not exists
  }

  const index = selectedAnswers.value[ques_id].indexOf(opted);
  if (index > -1) {
    selectedAnswers.value[ques_id].splice(index, 1); // Remove if already selected
  } else {
    selectedAnswers.value[ques_id].push(opted); // Add if not selected
  }
}

function enteredNAT(ques_id) {
  selectedAnswers.value[ques_id] = [nat_input.value];
  console.log(nat_input.value)
}
function submitTest() {
  submitted = true
  // Iterate through each question and compare the selected answer with the correct answer
  for (const quesId in selectedAnswers.value) {
    if (selectedAnswers.value.hasOwnProperty(quesId)) {
      const selectedAnswerArray = selectedAnswers.value[quesId];
      const correctAnswerArray = correctAnswers.value[quesId];

      if (selectedAnswerArray.length === 0) {
        selectedAnswers.value[quesId].isCorrect = false;
      } else if (arraysAreEqual(selectedAnswerArray, correctAnswerArray)) {
        selectedAnswers.value[quesId].isCorrect = true;

      } else {
        let isPartiallyCorrect = true;
        for (const selectedOption of selectedAnswerArray) {
          if (!correctAnswerArray.includes(selectedOption)) {
            isPartiallyCorrect = false;
            break;
          }
        }
        if (isPartiallyCorrect) {
          console.log(`Question ${quesId}: Partially Correct`);
          selectedAnswers.value[quesId].isCorrect = true;
        } else {
          console.log(`Question ${quesId}: Incorrect`);
          selectedAnswers.value[quesId].isCorrect = false;
        }
      }
      // Call getOptionColor and pass quesId and optionIndex
      for (const optionIndex of selectedAnswerArray) {
        optionColors.value[`${quesId}_${optionIndex}`] = getOptionColor(quesId, optionIndex);
        console.log(optionColors.value[`${quesId}_${optionIndex}`])

      }
      for (const optionIndex of correctAnswerArray) {
        optionColors.value[`${quesId}_${optionIndex}`] = getOptionColor(quesId, optionIndex);
        console.log(optionColors.value[`${quesId}_${optionIndex}`])

      }
    }
  }
}

// Helper function to check if two arrays are equal
function arraysAreEqual(arr1, arr2) {
  if (arr1.length !== arr2.length) {
    return false;
  }
  for (const item of arr1) {
    if (!arr2.includes(item)) {
      return false;
    }
  }
  return true;
}

function getOptionColor(quesId, optionIndex) {
  if (!submitted) {
    return ''; // Default color before submitting
  }

  const selectedAnswer = selectedAnswers.value[quesId];
  const correctAnswer = correctAnswers.value[quesId];

  // if (selectedAnswer.length === 0) {
  //   return ''; // No color for questions not answered
  // }

  if (selectedAnswer.includes(optionIndex)) {
    if (correctAnswer.includes(optionIndex)) {
      return 'green'; // Correctly selected in green
    } else {
      return 'red'; // Incorrectly selected in red
    }
  } else if (correctAnswer.includes(optionIndex)) {
    return 'green'; // Correct option that wasn't selected in green
  }

  return ''; // Default color
}



</script>
<!-- <template>
  <h3>{{ practice_test.name }}</h3>
  <div v-for="tag in practice_test.tags">
    <small>#{{ tag }}</small>
  </div>
  <div v-for="question in practice_test.questions">
    <h5>{{ question.name }}</h5>
    <p>{{ question.description }}</p>
    <div v-if="question.question_type === 'MCQ'">
      <div v-for="(option, optionIndex) in question.options" :key="optionIndex">
        <input
          type="radio"
          
          :name="'question_' + question.id"
          :value="optionIndex"
          @click="selectedMCQ(question.id, optionIndex)"
          :style="{ color: optionColors[`${question.id}_${optionIndex}`] }"

        />
        <label :style="{ color: optionColors[`${question.id}_${optionIndex}`]}">{{ option }}</label>
      </div>
    </div>
  </div>
  <button @click="submitTest">Submit</button>
  <button @click="redirect('/admin/practice_tests')">Close</button>
</template> -->
<template>
  <div class="d-flex justify-content-center align-items-center">
    <div class="w-75">
      <h3 class="mb-4 text-center">{{ practice_test.name }}</h3>
      <div class="d-flex justify-content-center mb-3">
        <div v-for="tag in practice_test.tags" :key="tag" class="badge bg-secondary me-2">#{{ tag }}</div>
      </div>
      <div v-for="question in practice_test.questions" :key="question.id" class="mb-4">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{{ question.name }}</h5>
            <p class="card-text">{{ question.description }}</p>
            <div v-if="question.question_type === 'MCQ'">
              <div v-for="(option, optionIndex) in question.options" :key="optionIndex" class="mb-2">
                <div class="form-check">
                  <input class="form-check-input" type="radio" :name="'question_' + question.id" :value="optionIndex"
                    @click="selectedMCQ(question.id, optionIndex)" :class="{
                      'text-success': optionColors[`${question.id}_${optionIndex}`] === 'green',
                      'text-danger': optionColors[`${question.id}_${optionIndex}`] === 'red'
                    }" />
                  <label class="form-check-label" @click="selectedMCQ(question.id, optionIndex)" :class="{
                    'text-success': optionColors[`${question.id}_${optionIndex}`] === 'green',
                    'text-danger': optionColors[`${question.id}_${optionIndex}`] === 'red'
                  }">
                    {{ option }}


                  </label>

                </div>

              </div>
              <span v-if="submitted && selectedAnswers[question.id]?.isCorrect" class="text-success"> Correct
                answer</span>
              <span v-if="submitted && selectedAnswers[question.id]?.isCorrect === false" class="text-danger"> Incorrect
                answer</span><br>
                <span v-if="submitted" class="text-success">Options - {{ question.correct_answers}}</span>

            </div>
            <div v-if="question.question_type === 'MSQ'">
              <div v-for="(option, optionIndex) in question.options" :key="optionIndex" class="mb-2">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" :name="'question_' + question.id" :value="optionIndex"
                    @click="selectedMSQ(question.id, optionIndex)" :class="{
                      'text-success': optionColors[`${question.id}_${optionIndex}`] === 'green',
                      'text-danger': optionColors[`${question.id}_${optionIndex}`] === 'red'
                    }" />
                  <label class="form-check-label" @click="selectedMSQ(question.id, optionIndex)" :class="{
                    'text-success': optionColors[`${question.id}_${optionIndex}`] === 'green',
                    'text-danger': optionColors[`${question.id}_${optionIndex}`] === 'red'
                  }">
                    {{ option }}


                  </label>

                </div>

              </div>
              <span v-if="submitted && selectedAnswers[question.id]?.isCorrect" class="text-success"> Correct
                answer</span>
              <span v-if="submitted && selectedAnswers[question.id]?.isCorrect === false" class="text-danger"> Incorrect
                answer</span><br>
              <span v-if="submitted" class="text-success">Options - {{ question.correct_answers}}</span>
            </div>

          </div>
          <div v-if="question.question_type === 'NAT'">
            <div class="d-flex align-items-center">
              <input class="form-control flex-grow-1" type="text" :name="'question_' + question.id" v-model="nat_input"
                @input="enteredNAT(question.id)" :class="{
                  'text-success': optionColors[`${question.id}`] === 'green',
                  'text-danger': optionColors[`${question.id}`] === 'red'
                }" />
            </div>

            <span v-if="submitted && selectedAnswers[question.id]?.isCorrect" class="text-success"> Correct
              answer
            </span>
            <span v-if="submitted && selectedAnswers[question.id]?.isCorrect === false" class="text-danger"> Incorrect
              answer</span>
            <br>
              <span v-if="submitted" class="text-success">Answer - {{ question.correct_answers}}</span>

          </div>


        </div>
      </div>
      <div class="d-flex justify-content-center">
        <button @click="submitTest" class="btn btn-primary me-2">Submit</button>
        <button @click="redirect('/admin/practice_tests')" class="btn btn-secondary">Close</button>
      </div>
    </div>
  </div>
</template>