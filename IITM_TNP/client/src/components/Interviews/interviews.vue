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

import { ref, onMounted, computed } from 'vue';
import { useStore } from 'vuex';


const store = useStore();
const curr_user_id = computed(() => store.getters.get_user_id);
const props = defineProps({
    search: {
        type: String,
        default: ""
    }
})
const interviews = computed(() => {
    const allInterviews = store.getters.get_all_interviews;

    if (props.search)
        return allInterviews.filter(interview =>
            interview.user_name.toLowerCase().includes(props.search.toLowerCase()) ||
            interview.description.toLowerCase().includes(props.search.toLowerCase()) ||
            interview.job_role.toLowerCase().includes(props.search.toLowerCase()) ||
            interview.job_type.toLowerCase().includes(props.search.toLowerCase()) ||
            interview.company.toLowerCase().includes(props.search.toLowerCase()) 
        );
    else return allInterviews;
});
// const interviews = computed(() => store.getters.get_all_interviews);
const showAddInterviewModal = ref(false);
// {
//                     "id" : interview.id,
//                     "company" : interview.company,
//                     "job_role" : interview.job_role,
//                     "job_type" : interview.job_type,
//                     "description" : interview.description,
//                     "user_id":interview.user_id,
//                     "user_name" : interview.created_by.name if not interview.anonymous else "Anonymous"
//                 } 
const addCompany = ref("")
const add_job_role = ref("")
const add_job_type = ref("")
const description = ref("")
const anonymous = ref(false)

onMounted(() => { store.dispatch("fetchInterviews"); })

function closeAddInterviewModal() {
  showAddInterviewModal.value=false;
  description.value = '';
  addCompany.value = "";
  add_job_role.value = "";
  add_job_type.value = "";
  anonymous.value = false;
}

function submitModal() {
  store.dispatch("addInterview", {
    description: description.value,
    job_type: add_job_type.value,
    job_role: add_job_role.value,
    anonymous: anonymous.value,
    company: addCompany.value
  })
  closeAddInterviewModal();
}
const showEditModal=ref(false)
const editCompany = ref("")
const edit_job_role = ref("")
const edit_job_type = ref("")
const edit_description = ref("")
const edit_anonymous = ref(false)
const edit_interview_id=ref(null)
const interview_user_name=ref("")

function openEditModal(interview_id,interview_description,
 interview_job_role,interview_user_name,
            interview_job_type,interview_company){
  showEditModal.value=true;
  edit_interview_id.value=interview_id;
  editCompany.value=interview_company;
  edit_job_role.value = interview_job_role;
  edit_job_type.value = interview_job_type;
  edit_description.value = interview_description;
  if (interview_user_name==="Anonymous"){
    edit_anonymous.value = true;
  }
  else{
    edit_anonymous.value = false;
  }
}

function closeEditModal(){
  showEditModal.value=false;
  edit_interview_id.value=null;
  editCompany.value="";
  edit_job_role.value = "";
  edit_job_type.value = "";
  edit_description.value = "";
  edit_anonymous.value = false;
}

function submitEdit(){
  store.dispatch("editInterview",{
    interview_id : edit_interview_id.value,
    company: editCompany.value,
    job_role: edit_job_role.value,
    job_type: edit_job_type.value,
    anonymous: edit_anonymous.value,
    description: edit_description.value
  });
  closeEditModal();
}

const showDeleteModal=ref(false);
const deleteInterview = ref(null);
function openDeleteModal(interview_id){
  showDeleteModal.value=true;
  deleteInterview.value=interview_id;
}
function closeDeleteModal(){
  showDeleteModal.value=false;
  deleteInterview.value=null;
}
function submitDelete(){
  store.dispatch("deleteInterview",
  deleteInterview.value)
  closeDeleteModal();
}
</script>

<template>
  <div>
    <!-- Button to open the "Add Post" modal -->

    <div class="container mt-5">
      <MDBBtn color="primary" class="mb-3" @click="showAddInterviewModal = true">Add Interview</MDBBtn>

      <div class="card mb-4" v-for="interview in interviews" :key="interview.id">
        <div class="card-body">
          <h5 class="card-title">{{ interview.user_name }}</h5>

          <p class="card-text">Company - {{ interview.company }}</p>
          <p class="card-text">Job Role - {{ interview.job_role }}</p>
          <p class="card-text">Job Type - {{ interview.job_type }}</p>


          <p class="card-text">Description:</p>
          <p class="card-text">{{ interview.description }}</p>

          <small class="text-muted">{{ interview.timestamp }}</small>

          <div class="card-footer" v-if="interview.user_id === curr_user_id">
            <MDBBtn color="primary" size="sm" class="me-2" @click="openEditModal(interview.id,
             interview.description, interview.job_role,interview.user_name,
            interview.job_type,interview.company)">
              Edit</MDBBtn>
            <MDBBtn color="danger" size="sm" @click="openDeleteModal(interview.id)">Delete</MDBBtn>
          </div>
        </div>
      </div>
    </div>

    <MDBModal v-model="showEditModal">
        <MDBModalHeader>Edit Interview</MDBModalHeader>
        <MDBModalBody>
          <MDBInput type="textarea" v-model="editCompany" label="Company" />
        <br>
        <MDBInput type="textarea" v-model="edit_job_role" label="Job Role" />
        <br>
        <label>Job Type:</label>
        <!-- Default radio -->
        <div class="form-check">
          <input class="form-check-input" type="radio" name="flexRadioDefaulta" id="flexRadioDefault1" value="Full Time"
            v-model="edit_job_type" :checked="edit_job_type==='Full Time'"/>
          <label class="form-check-label" for="flexRadioDefault1">Full Time</label>
        </div>

        <!-- Default checked radio -->
        <div class="form-check">
          <input class="form-check-input" type="radio" name="flexRadioDefaulta" id="flexRadioDefault2" value="Internship"
            v-model="edit_job_type" :checked="edit_job_type==='Internship'" />
          <label class="form-check-label" for="flexRadioDefault2">Internship</label>
        </div>        
        <br>
        <MDBInput type="textarea" v-model="edit_description" label="Description" />
        <br>
        
        <label>Anonymous:</label>
        <!-- Default radio -->
        <div class="form-check">
          <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault3" :value=true
          :checked="edit_anonymous === true"
            v-model="edit_anonymous" />
          <label class="form-check-label" for="flexRadioDefault1">Yes</label>
        </div>

        <!-- Default checked radio -->
        <div class="form-check">
          <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault4" :value=false            
          v-model="edit_anonymous" :checked="edit_anonymous === false" />
          <label class="form-check-label" for="flexRadioDefault2">No</label>
        </div>
           </MDBModalBody>
        <MDBModalFooter>
          <MDBBtn color="secondary" @click="closeEditModal">Cancel</MDBBtn>
          <MDBBtn color="primary" @click="submitEdit">Submit</MDBBtn>
        </MDBModalFooter>
      </MDBModal>



    <!-- Add Interview Modal -->
    <MDBModal v-model="showAddInterviewModal">
      <MDBModalHeader>Add New Interview Details</MDBModalHeader>
      <MDBModalBody>
        
        <MDBInput type="textarea" v-model="addCompany" label="Company" />
        <br>
        <MDBInput type="textarea" v-model="add_job_role" label="Job Role" />
        <br>
        <label>Job Type:</label>
        <!-- Default radio -->
        <div class="form-check">
          <input class="form-check-input" type="radio" name="flexRadioDefaulta" id="flexRadioDefault6" value="Full Time"
            v-model="add_job_type" />
          <label class="form-check-label" for="flexRadioDefault1">Full Time</label>
        </div>

        <!-- Default checked radio -->
        <div class="form-check">
          <input class="form-check-input" type="radio" name="flexRadioDefaulta" id="flexRadioDefault7" value="Internship"
            v-model="add_job_type" checked />
          <label class="form-check-label" for="flexRadioDefault2">Internship</label>
        </div>
        <br>
        <MDBInput type="textarea" v-model="description" label="Description" />
        <br>
        
        <label>Anonymous:</label>
        <!-- Default radio -->
        <div class="form-check">
          <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault1" :value=true
            v-model="anonymous" />
          <label class="form-check-label" for="flexRadioDefault1">Yes</label>
        </div>

        <!-- Default checked radio -->
        <div class="form-check">
          <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault2" :value=false
            v-model="anonymous" checked />
          <label class="form-check-label" for="flexRadioDefault2">No</label>
        </div>
      </MDBModalBody>
      <MDBModalFooter>
        <MDBBtn color="secondary" @click="showAddInterviewModal = false">Cancel</MDBBtn>
        <MDBBtn color="primary" @click="submitModal">Submit</MDBBtn>
      </MDBModalFooter>
    </MDBModal>

    <!-- Delete Confirmation Modal -->
      <MDBModal v-model="showDeleteModal">
        <MDBModalHeader>Delete Interview</MDBModalHeader>
        <MDBModalBody>
          Are you sure you want to delete this Interview?
        </MDBModalBody>
        <MDBModalFooter>
          <MDBBtn color="secondary" @click="closeDeleteModal">Cancel</MDBBtn>
          <MDBBtn color="danger" @click="submitDelete">Delete</MDBBtn>
        </MDBModalFooter>
      </MDBModal>


  </div>
</template>