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

import { ref, watch, onMounted, computed } from 'vue';
import { routerKey } from 'vue-router';
import { useStore } from 'vuex';
import { useRouter, useRoute } from 'vue-router';
const router = useRouter();
const route = useRoute();
const store = useStore();
const curr_user_id = computed(() => store.getters.get_user_id);



onMounted(() => {
  // if (store.getters.get_login_status == true) router.push("/posts");
  store.dispatch('fetchPosts');

})
const posts = computed(() => store.getters.get_all_posts); // Use a computed property
const editedDescription = ref('');
const editingPostId = ref(null);
const showEditModal = ref(false); // Reactive variable to control modal visibility
const editedTags = ref([]); // Add a ref for edited tags

function edit_current_post(tagsArray) {
  store.dispatch("editPost", { postid: editingPostId.value, postData: editedDescription.value, tags: tagsArray });
}
function openEditModal(postId, description, tags) {
  editedDescription.value = description;
  editingPostId.value = postId;
  showEditModal.value = true;
  if (Array.isArray(tags)) {
    editedTags.value = tags.join(', '); // Convert array to comma-separated string
  } else if (typeof tags === 'string') {
    editedTags.value = tags;
  } else {
    editedTags.value = '';
  }
}

function closeEditModal() {
  editedDescription.value = '';
  editingPostId.value = null;
  showEditModal.value = false;
  editedTags.value = [];// Set the showEditModal value to false to close the modal
}

function submitEdit() {
  const tagsArray = editedTags.value.split(',').map(tag => tag.trim()); // Extract the array value

  edit_current_post(tagsArray);
  closeEditModal();
}

const showAddModal = ref(false); // Reactive variable to control modal visibility
const newTags = ref([]);
const newDescription = ref('');

function addNewPost() {
  // Extract tags into an array
  const tagsArray = newTags.value.split(',').map(tag => tag.trim());

  // Call the createPost action with the new post data
  store.dispatch('createPost', {
    description: newDescription.value,
    tags: tagsArray
  });

  // Reset modal inputs and hide modal
  newDescription.value = '';
  newTags.value = '';
  showAddModal.value = false;

}


const postToDelete = ref(null);
const showDeleteModal = ref(false)

function openDeleteModal(postId) {
  showDeleteModal.value = true
  postToDelete.value = postId;

}

function closeDeleteModal() {
  postToDelete.value = null;
  showDeleteModal.value = false;
}

async function confirmDelete() {
  if (postToDelete.value !== null) {
    store.dispatch('deletePost', postToDelete.value);

    postToDelete.value = null;
    closeDeleteModal();
  }
}

const showAddReplyModal = ref(false); // Reactive variable to control modal visibility
const newReplyDescription = ref('');
const ReplyToPostId = ref(null);

function openAddReplyModal(post_id) {
  showAddReplyModal.value = true;
  ReplyToPostId.value = post_id;

}
function dispatchCreateReply() {
  store.dispatch('createReply', {
    description: newReplyDescription.value,
    postid: ReplyToPostId.value
  });

  // Reset modal inputs and hide modal
  newReplyDescription.value = '';
  showAddReplyModal.value = false;
  ReplyToPostId.value = null;
}
const editedReplyDescription = ref('');
const editingReplyId = ref(null);
const showEditReplyModal = ref(false); // Reactive variable to control modal visibility


function openEditReplyModal(reply_id, reply_description) {
  editedReplyDescription.value = reply_description;
  editingReplyId.value = reply_id;
  showEditReplyModal.value = true;
}

function closeEditReplyModal() {
  editedReplyDescription.value = '';
  editingReplyId.value = null;
  showEditReplyModal.value = false;
}

function submitReplyEdit() {
  store.dispatch("editReply", {
    description: editedReplyDescription.value,
    reply_id:editingReplyId.value
   })
  closeEditReplyModal();
}

const replyToDelete = ref(null);
const showDeleteReplyModal = ref(false)

function openDeleteReplyModal(replyId) {
  showDeleteReplyModal.value = true;
  replyToDelete.value = replyId;

}

function closeDeleteReplyModal() {
  replyToDelete.value = null;
  showDeleteReplyModal.value = false;
}

async function confirmReplyDelete() {
  if (replyToDelete.value != null) {
    store.dispatch('deleteReply', replyToDelete.value);

    replyToDelete.value = null;
    closeDeleteReplyModal();
  }
}

</script>
<template>
  <div>
    <!-- Button to open the "Add Post" modal -->
    <MDBBtn color="primary" class="mb-3" @click="showAddModal = true">Add Post</MDBBtn>

    <div class="container mt-5">
      <div class="card mb-4" v-for="post in posts" :key="post.id">
        <div class="card-body">
          <h5 class="card-title">{{ post.username }}</h5>
          <p class="card-text">{{ post.description }}</p>
          <div class="d-flex">
            <small v-for="tag in post.tags" class="text-muted me-2">#{{ tag }}</small>
          </div>
          <small class="text-muted">{{ post.timestamp }}</small>

          <div class="card-footer" v-if="post.user_id === curr_user_id">
            <MDBBtn color="primary" size="sm" class="me-2" @click="openEditModal(post.id, post.description, post.tags)">
              Edit</MDBBtn>
            <MDBBtn color="danger" size="sm" @click="openDeleteModal(post.id)">Delete</MDBBtn>
          </div>
        </div>
        <ul class="list-group list-group-flush">
          <li class="list-group-item">
            <h6 class="mb-0">Replies</h6> &nbsp;
            <MDBBtn color="primary" size="sm" class="me-2" @click="openAddReplyModal(post.id)">Add Reply</MDBBtn>

          </li>
          <li class="list-group-item" v-for="(reply, index) in post.replies" :key="reply.id">
            <div class="d-flex">
              <div class="flex-grow-1">
                <h6 class="mb-0">{{ reply.username }}</h6>
                <p>{{ reply.description }}</p>
                <div class="card-footer" v-if="reply.user_id === curr_user_id">
                  <MDBBtn color="primary" size="sm" class="me-2"
                    @click="openEditReplyModal(reply.id, reply.description)">Edit</MDBBtn>
                  <MDBBtn color="danger" size="sm" class="me-2" @click="openDeleteReplyModal(reply.id)">Delete</MDBBtn>
                </div>
                <small class="text-muted">{{ reply.timestamp }}</small>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>

    <MDBModal v-model="showEditModal">
      <MDBModalHeader>Edit Post</MDBModalHeader>
      <MDBModalBody>
        <!-- Edit input for description -->
        <MDBInput type="textarea" v-model="editedDescription" label="Edit Description" />
        <br>
        <!-- Edit input for tags -->
        <MDBInput v-model="editedTags" label="Edit Tags (comma separated)" type="text"
          @input="editedTags = $event.target.value.split(',').map(tag => tag.trim())" />
      </MDBModalBody>
      <MDBModalFooter>
        <MDBBtn color="secondary" @click="closeEditModal">Cancel</MDBBtn>
        <MDBBtn color="primary" @click="submitEdit">Submit</MDBBtn>
      </MDBModalFooter>
    </MDBModal>



    <!-- Add Post Modal -->
    <MDBModal v-model="showAddModal">
      <MDBModalHeader>Add New Post</MDBModalHeader>
      <MDBModalBody>
        <!-- Input for description -->
        <MDBInput type="textarea" v-model="newDescription" label="Description" />
        <br>
        <!-- Input for tags -->
        <MDBInput v-model="newTags" label="Tags (comma separated)" type="text" />
      </MDBModalBody>
      <MDBModalFooter>
        <MDBBtn color="secondary" @click="showAddModal = false">Cancel</MDBBtn>
        <MDBBtn color="primary" @click="addNewPost">Add</MDBBtn>
      </MDBModalFooter>
    </MDBModal>

    <!-- Delete Confirmation Modal -->
    <MDBModal v-model="showDeleteModal">
      <MDBModalHeader>Delete Post</MDBModalHeader>
      <MDBModalBody>
        Are you sure you want to delete this post?
      </MDBModalBody>
      <MDBModalFooter>
        <MDBBtn color="secondary" @click="closeDeleteModal">Cancel</MDBBtn>
        <MDBBtn color="danger" @click="confirmDelete">Delete</MDBBtn>
      </MDBModalFooter>
    </MDBModal>

    <!-- Add Reply Modal -->
    <MDBModal v-model="showAddReplyModal">
      <MDBModalHeader>Add New Reply</MDBModalHeader>
      <MDBModalBody>
        <!-- Input for description -->
        <MDBInput type="textarea" v-model="newReplyDescription" label="Description" />
      </MDBModalBody>
      <MDBModalFooter>
        <MDBBtn color="secondary" @click="showAddReplyModal = false">Cancel</MDBBtn>
        <MDBBtn color="primary" @click="dispatchCreateReply">Add</MDBBtn>
      </MDBModalFooter>
    </MDBModal>
    <!-- Edit Reply Modal -->
    <MDBModal v-model="showEditReplyModal">
      <MDBModalHeader>Edit Reply</MDBModalHeader>
      <MDBModalBody>
        <!-- Input for description -->
        <MDBInput type="textarea" v-model="editedReplyDescription" label="Description" />
      </MDBModalBody>
      <MDBModalFooter>
        <MDBBtn color="secondary" @click="showEditReplyModal = false">Cancel</MDBBtn>
        <MDBBtn color="primary" @click="submitReplyEdit">Add</MDBBtn>
      </MDBModalFooter>
    </MDBModal>
    <!-- Delete Confirmation Modal -->
    <MDBModal v-model="showDeleteReplyModal">
      <MDBModalHeader>Delete Reply</MDBModalHeader>
      <MDBModalBody>
        Are you sure you want to delete this reply?
      </MDBModalBody>
      <MDBModalFooter>
        <MDBBtn color="secondary" @click="closeDeleteReplyModal">Cancel</MDBBtn>
        <MDBBtn color="danger" @click="confirmReplyDelete">Delete</MDBBtn>
      </MDBModalFooter>
    </MDBModal>
  </div>
</template>