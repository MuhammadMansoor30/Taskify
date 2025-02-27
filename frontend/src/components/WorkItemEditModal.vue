<template>
    <div v-if="showModal" class="modal-overlay">
        <div class="custom-modal rounded-5">
            <div class="d-flex flex-row header">
                <h2 class="mb-4 fw-bold">Edit Work Item </h2>
                <i class="fas fa-close fs-2 icon" @click="modalClose"></i>
            </div>

            <form v-if="!isLoading" @submit.prevent="submitForm" class="text-start">
                <b-form-group class="mb-2 fs-4" label="Work Item Name" label-for="textField"
                    :invalid="form.name.length > 50">
                    <b-form-input type="text" id="textField" class="form-control fs-5" v-model="form.name"
                        placeholder="Enter Work Item Name" :class="{ 'is-invalid': form.name.length > 50 }"
                        required></b-form-input>
                </b-form-group>

                <div class="mb-2">
                    <label for="fileField" class="form-label fs-4">Upload File</label>
                    <input type="file" id="fileField" class="form-control fs-5" @change="handleFileUpload"
                        :class="{ 'is-invalid': isFileSelected }" required>
                    <div v-if="isFileSelected" class="invalid-feedback fs-5">
                        Please select a file.
                    </div>
                </div>

                <b-form-group class="mb-2 fs-4" label="Work Status" label-for="selectField1">
                    <b-form-select id="selectField1" class="form-select fs-5" v-model="form.status">
                        <option v-for="(option, index) in statusOptions" :value="option.value" :key="index">
                            {{ option.label }}</option>
                    </b-form-select>
                </b-form-group>

                <b-form-group class="mb-2 fs-4" label="Is Approved" label-for="booleanField">
                    <b-form-select id="booleanField" class="form-select fs-5" v-model="form.is_approved">
                        <option value="">Please Select</option>
                        <option value="True">True</option>
                        <option value="False">False</option>
                    </b-form-select>
                </b-form-group>

                <b-form-group class="mb-2 fs-4" label="Select Task" label-for="selectField2" :invalid="isTaskSelected"
                    invalid-feedback="Please select a task.">
                    <b-form-select id="selectField2" class="form-select fs-5" v-model="form.selectedTask"
                        :class="{ 'is-invalid': isTaskSelected }" required>
                        <option value="">Please Select</option>
                        <option v-for="(task, index) in tasks" :key="index" :value="task.id">{{ task.title }}
                        </option>
                    </b-form-select>
                </b-form-group>

                <b-button-toolbar class="mt-3 justify-content-end">
                    <button class="btn fs-5 btn-danger clr-1 rounded-5" @click="resetForm">Reset</button>
                    <button type="submit" class="btn clr fs-5 rounded-5 ms-4" @click.prevent="submitForm">Edit</button>
                </b-button-toolbar>
            </form>
            <div v-if="isLoading" class="d-flex justify-content-center align-items-center mb-3 w-100">
                <b-spinner></b-spinner>
            </div>
        </div>
    </div>
</template>

<script>
import Swal from 'sweetalert2';
import { mapActions } from 'vuex';

export default {
    mounted() {
        this.getTasks();
    },
    props: ['showModal', 'data', 'editBtn'],
    data() {
        return {
            form: {
                name: '',
                is_approved: '',
                file: '',
                status: '',
                selectedTask: '',
            },
            tasks: null,
            isFileSelected: false,
            isTaskSelected: false,
            isLoading: false,
            statusOptions: [
                { value: "", label: 'Select Status' },
                { value: "In Progress", label: 'In Progress' },
                { value: "Partially Completeds", label: 'Partially Completed' },
                { value: "Completed", label: 'Completed' },
            ],
        };
    },
    methods: {
        ...mapActions(['addUser', 'editUser', 'getTasksData', 'editWorkItem']),
        async submitForm() {
            if (this.form.selectedTask && this.form.file) {
                this.isFileSelected = false;
                this.isTaskSelected = false;
                this.isLoading = true;
                await this.updateWorkItem(this.form, this.data.id);
                this.isLoading = false;
            }
            else {
                this.isFileSelected = true;
                this.isTaskSelected = true;
                this.isLoading = false;
                Swal.fire({
                    icon: 'error',
                    timer: 1000,
                    title: "Please Fill out all the required fields",
                    showConfirmButton: false,
                });
            }
        },
        resetForm() {
            this.form.name = '';
            this.form.is_approved = '';
            this.form.file = '';
            this.form.status = '';
            this.form.selectedTask = '';
            this.isFileSelected = false;
            this.isTaskSelected = false;
        },
        async updateWorkItem(formData, id) {
            try {
                const finalData = {id, ...formData};
                const data = await this.editWorkItem(finalData);
                if (data) {
                    Swal.fire({
                        icon: 'success',
                        timer: 1500,
                        title: 'Work Item Updated Successfully',
                        showConfirmButton: false,
                    }).then(() => {
                        this.$emit('update:editBtn', false);
                        this.$emit('update:showModal', false);
                        window.location.reload();
                        this.resetForm();
                    });
                }
                else {
                    Swal.fire({
                        icon: 'error',
                        timer: 1500,
                        title: "Could Not update work item some error occurred",
                        showConfirmButton: false,
                    });
                }
            }
            catch (error) {
                console.log(error);
            }
        },
        async getTasks() {
            try {
                const data = await this.getTasksData();
                this.tasks = data;
            }
            catch (error) {
                console.log(error);
            }
        },
        handleFileUpload(event) {
            this.form.file = event.target.files[0];
        },
        modalClose() {
            this.$emit('update:editBtn', false);
            this.$emit('update:showModal', false);
        },
    },
    watch: {
        data(newData) {
            if (newData) {
                this.form.name = newData.name || '';
                this.form.file = newData.file || '';
                this.form.is_approved = newData.is_approved ? "True" : 'False';
                this.form.status = newData.status || '';
                this.form.selectedTask = newData.task || "";
            }
        }
    }
};
</script>

<style scoped>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1;
}

.custom-modal {
    background-color: #ececec;
    padding: 30px;
    border-radius: 8px;
    width: 70%;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.header {
    width: 57%;
    margin-left: 42%;
    justify-content: space-between;
}

.icon:hover {
    cursor: pointer;
}

.clr {
    width: 120px;
    background: #800020;
    color: #ececec;
}

.clr:hover {
    width: 120px;
    background: #630000;
    color: #ececec;
}

.clr-1 {
    width: 120px;
}
</style>