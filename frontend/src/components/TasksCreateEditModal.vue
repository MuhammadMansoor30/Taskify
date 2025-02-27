<template>
    <div v-if="showModal" class="modal-overlay">
        <div class="custom-modal rounded-5">
            <div class="d-flex flex-row header">
                <h2 class="mb-4 fw-bold">Add New Task</h2>
                <i class="fas fa-close fs-2 icon" @click="modalClose"></i>
            </div>

            <form v-if="!isLoading" @submit.prevent="submitForm" class="text-start">
                <b-form-group label="Task Title" label-for="title" class="fs-4">
                    <b-form-input id="title" v-model="form.title" required placeholder="Enter title"
                        :class="{ 'is-invalid': form.title.length > 30, 'fs-5': true }"></b-form-input>
                </b-form-group>

                <b-form-group label="Description" label-for="description" class="fs-4">
                    <b-form-textarea id="description" v-model="form.description" required
                        placeholder="Enter task description ....."
                        :class="{ 'is-invalid': form.description.length > 350, 'fs-5': true }" rows="2"
                        no-resize=""></b-form-textarea>
                </b-form-group>

                <b-form-group label="Select Team" label-for="team" class="fs-4">
                    <b-form-select id="team" v-model="form.team" required class="form-select fs-5">
                        <option value="">Please Select</option>
                        <option v-for="(team, index) in allTeams" :key="index" :value="team.id">{{ team.name }}</option>
                    </b-form-select>
                </b-form-group>

                <b-form-group label="Task Completed" label-for="iscompleted" class="fs-4">
                    <b-form-select id="iscompleted" v-model="form.is_completed" class="form-select fs-5">
                        <option value="">Please Select</option>
                        <option value="True">True</option>
                        <option value="False">False</option>
                    </b-form-select>
                </b-form-group>

                <b-form-group label="Task Priority" label-for="priority" class="fs-4">
                    <b-form-select id="priority" v-model="form.priority" required class="form-select fs-5">
                        <option value="">Please Select</option>
                        <option value="Low">Low</option>
                        <option value="Medium">Medium</option>
                        <option value="High">High</option>
                    </b-form-select>
                </b-form-group>

                <b-form-group label="Select Deadline" label-for="deadline" class="fs-4">
                    <input type="date" id="deadline" class="form-control fs-5" v-model="form.task_deadline" />
                </b-form-group>

                <b-form-group label="Assign To" label-for="assignto" class="fs-4">
                    <b-form-select id="assignto" v-model="form.assigned_to" required class="form-select fs-5">
                        <option value="">Please Select</option>
                        <option v-for="(user, index) in allUsers" :key="index" :value="user.id">{{ user.username }}
                        </option>
                    </b-form-select>
                </b-form-group>

                <b-button-toolbar class="mt-3 justify-content-end">
                    <button class="btn fs-5 btn-danger clr-1 rounded-5" @click="resetForm">Reset</button>
                    <button type="submit" class="btn clr fs-5 rounded-5 ms-4" @click.prevent="submitForm">{{ editBtn ?
                        "Edit" : "Add" }}</button>
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
        this.getAllUsers();
        this.getAllTeams();
    },
    props: ['showModal', 'data', 'editBtn'],
    data() {
        return {
            form: {
                title: '',
                description: '',
                team: '',
                is_completed: '',
                priority: '',
                assigned_to: '',
                task_deadline: '',
            },
            passwordVisible: false,
            allTeams: null,
            allUsers: null,
            isLoading: false,
        };
    },
    methods: {
        ...mapActions(['addTask', 'getTeamsData', 'getUsersData', 'editTask']),
        async submitForm() {
            if (!this.editBtn) {
                if (this.form.title && this.form.description && this.form.team && this.form.priority && this.form.assigned_to && this.form.task_deadline) {
                    this.isLoading = true;
                    await this.addNewTask(this.form);
                    this.isLoading = false;
                }
                else {
                    this.isLoading = false;
                    Swal.fire({
                        icon: 'error',
                        timer: 1000,
                        title: "Please Fill out all the required fields",
                        showConfirmButton: false,
                    });
                }
            }
            else {
                this.isLoading = true;
                await this.updateTask(this.form, this.data.id);
                this.isLoading = false;
            }
        },
        resetForm() {
            this.form.title = '';
            this.form.description = '';
            this.form.team = '';
            this.form.is_completed = '';
            this.form.priority = '';
            this.form.assigned_to = '';
            this.form.task_deadline = '';
        },
        async addNewTask(formData) {
            try {
                const data = await this.addTask(formData);
                if (data) {
                    Swal.fire({
                        icon: 'success',
                        timer: 1500,
                        title: 'Task Added Successfully',
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
                        title: "Could Not add task some error occurred",
                        showConfirmButton: false,
                    });
                }
            }
            catch (error) {
                console.log(error);
            }
        },
        async getAllUsers() {
            try {
                let users = await this.getUsersData();
                users = users.filter((user) => user.id !== 2);   // Removing the Admin user as task cannot be assigned to him.
                this.allUsers = users;
                return users;
            }
            catch (error) {
                console.log(error);
            }
        },
        async getAllTeams() {
            try {
                const teams = await this.getTeamsData();
                this.allTeams = teams;
                return teams;
            }
            catch (error) {
                console.log(error);
            }
        },
        async updateTask(formData, id) {
            try {
                const finalData = { id, ...formData };
                const result = await this.editTask(finalData);
                if (result) {
                    Swal.fire({
                        icon: 'success',
                        timer: 1500,
                        title: 'Task Updated Successfully',
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
                        title: "Could Not update task some error occurred",
                        showConfirmButton: false,
                    });
                }
            }
            catch (error) {
                console.log(error);
            }
        },
        togglePasswordVisibility() {
            this.passwordVisible = !this.passwordVisible;
        },
        modalClose() {
            this.$emit('update:editBtn', false);
            this.$emit('update:showModal', false);
        },
    },
    watch: {
        data(newData) {
            if (newData) {
                this.form.title = newData.title || '';
                this.form.team = newData.team || '';
                this.form.is_completed = newData.is_completed ? 'True' : 'False';
                this.form.priority = newData.priority || '';
                this.form.assigned_to = newData.assigned_to || '';
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

.icon:hover{
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