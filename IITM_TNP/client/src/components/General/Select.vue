<script setup>
import { MDBDropdown, MDBDropdownToggle, MDBDropdownMenu, MDBDropdownItem } from "mdb-vue-ui-kit";
import { ref, defineEmits } from 'vue';

const dropdown = ref(false);
const chosen = ref(0);

const props = defineProps({
    title: {
        type: String
    },
    option_list: {
        type: Array,
        default: []
    },
    modelValue: {
        type: Number,
        default: 0
    }
});

const emit = defineEmits();

const selectOption = (optionId) => {
    chosen.value = optionId;
    emit('update:modelValue', optionId);
};

</script>

<template>
    <div class="form-outline mb-4">
        <MDBDropdown v-model="dropdown" id="dropdown" class="p-0 form-control select-input active custom-dropdown">
            <MDBDropdownToggle @click="dropdown = !dropdown" color="light">
                {{ option_list[chosen].name }}
            </MDBDropdownToggle>
            <MDBDropdownMenu aria-labelledby="dropdownMenuButton">
                <MDBDropdownItem v-for="option in option_list" :key="option.id" href="#" @click="selectOption(option.id)">
                    {{ option.name }}
                </MDBDropdownItem>
            </MDBDropdownMenu>
        </MDBDropdown>
        <label class="form-label select-label" for="dropdown">{{ title }}</label>
        <div class="form-notch" @click="dropdown = !dropdown">
            <div class="form-notch-leading" style="width: 9px;"></div>
            <div class="form-notch-middle" style="width: 112.8px;"></div>
            <div class="form-notch-trailing"></div>
        </div>
    </div>
</template>

<style scoped>
.custom-dropdown .btn {
    margin: 0 0rem;
}
</style>
