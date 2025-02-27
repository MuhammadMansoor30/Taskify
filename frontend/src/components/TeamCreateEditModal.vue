<template>
    <div v-if="showModal" class="modal-overlay">
        <div class="custom-modal rounded-5">
            <div class="d-flex flex-row header">
                <h2 class="mb-4 fw-bold">{{editBtn ? "Edit Team" : "Add New Team"}}</h2>
                <i class="fas fa-close fs-2 icon" @click="modalClose"></i>
            </div>

            <form v-if="!isLoading" @submit.prevent="submitForm" class="text-start">
                <b-form-group label="Name" label-for="name" class="fs-4">
                    <b-form-input id="name" v-model="form.name" required placeholder="Enter team name"
                        :class="{ 'is-invalid': form.name.length > 30, 'fs-5': true }"></b-form-input>
                </b-form-group>

                <b-form-group label="Description" label-for="description" class="fs-4">
                    <b-form-textarea id="description" v-model="form.description" required
                        placeholder="Enter team description....."
                        :class="{ 'is-invalid': form.description.length > 100, 'fs-5': true }" rows="3"
                        no-resize></b-form-textarea>
                </b-form-group>

                <b-form-group label="Project Name" label-for="projectname" class="fs-4">
                    <b-form-input id="projectname" v-model="form.project_name" required placeholder="Enter project name"
                        :class="{ 'is-invalid': form.project_name.length > 30, 'fs-5': true }"></b-form-input>
                </b-form-group>

                <b-form-group label="Select Manager" label-for="manager" class="fs-4">
                    <b-form-select id="manager" v-model="form.manager" class="form-select fs-5" required
                        :class="{ 'is-invalid': isManagerSelected }">
                        <option value="">Please Select</option>
                        <option v-for="(val, index) in allManagers" :key="index" :value="val.id">{{ val.full_name }}
                        </option>
                    </b-form-select>
                    <div v-if="isManagerSelected" class="invalid-feedback fs-5">Please select a Manager.</div>
                </b-form-group>

                <b-form-group label="Select Developers" label-for="developers" class="fs-4">
                    <b-form-select id="developers" v-model="form.developers" class="form-select fs-5" required multiple 
                        :class="{ 'is-invalid': isDeveloperSelected }">
                        <option :value="[]">Please Select</option>
                        <option v-for="(val, index) in allDevelopers" :key="index" :value="val.id">{{ val.full_name }}
                        </option>
                    </b-form-select>
                    <div v-if="isDeveloperSelected" class="invalid-feedback fs-5">Please select a Developer.</div>
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
        this.getDataForManagersAndDevelopers();
    },
    props: ['showModal', 'data', 'editBtn'],
    data() {
        return {
            form: {
                name: '',
                description: '',
                project_name: '',
                manager: '',
                developers: [],
            },
            isLoading: false,
            allManagers: null,
            allDevelopers: null,
            isManagerSelected: false,
            isDeveloperSelected: false,
        };
    },
    methods: {
        ...mapActions(['addTeam', 'getManagersData', 'getDevelopersData', 'editTeam']),
        async submitForm() {
            if (!this.editBtn) {
                if (this.form.name, this.form.description && this.form.project_name && this.form.manager) {
                    this.isManagerSelected = false;
                    this.isDeveloperSelected = false;
                    this.isLoading = true;
                    await this.addNewTeam(this.form);
                    this.isLoading = false;
                }
                else {
                    this.isManagerSelected = true;
                    this.isDeveloperSelected = true;
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
                this.isManagerSelected = false;
                this.isDeveloperSelected = false;
                this.isLoading = true;
                await this.updateTeam(this.form, this.data.id);
                this.isLoading = false;
            }
        },
        resetForm() {
            this.form.name = '';
            this.form.description = '';
            this.form.project_name = '';
            this.form.manager = '';
        },
        async addNewTeam(formData) {
            try {
                const data = await this.addTeam(formData);
                if (data) {
                    Swal.fire({
                        icon: 'success',
                        timer: 1500,
                        title: 'Team Added Successfully',
                        showConfirmButton: false,
                    }).then(() => {
                        this.$emit('update:editBtn', false);
                        this.$emit('update:showModal', false); // Same as done in Table Component.
                        window.location.reload();
                        this.resetForm();
                    });
                }
                else {
                    Swal.fire({
                        icon: 'error',
                        timer: 1500,
                        title: "Could Not add team some error occurred",
                        showConfirmButton: false,
                    });
                }
            }
            catch (error) {
                console.log(error);
            }
        },
        async getDataForManagersAndDevelopers() {
            try {
                const managers = await this.getManagersData();
                this.allManagers = managers;
            }
            catch (error) {
                console.log(error);
            }
            try{
                const developers = await this.getDevelopersData();
                this.allDevelopers = developers
            }
            catch (error){
                console.log(error);
            }
        },
        async updateTeam(formData, id) {
            const finaldata = { id, ...formData };
            try {
                const result = await this.editTeam(finaldata);
                if (result) {
                    Swal.fire({
                        icon: 'success',
                        timer: 1500,
                        title: 'Team Updated Successfully',
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
                        title: "Could Not update team some error occurred",
                        showConfirmButton: false,
                    });
                }
            }
            catch (error) {
                console.log(error);
            }
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
                this.form.project_name = newData.project_name || '';
                this.form.manager = newData.manager || '';
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