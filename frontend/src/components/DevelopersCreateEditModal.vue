<template>
    <div v-if="showModal" class="modal-overlay">
        <div class="custom-modal rounded-5">
            <h2 class="mb-4 fw-bold">Add New Developer</h2>

            <form v-if="!isLoading" @submit.prevent="submitForm" class="text-start">
                <div class="d-flex d-row">
                    <b-form-group label="Username" label-for="username" class="w-50 me-3 fs-4">
                        <b-form-input id="username" v-model="form.username" required placeholder="Enter user name"
                            :class="{ 'is-invalid': form.username.length > 30, 'fs-5': true }"></b-form-input>
                    </b-form-group>
                    <b-form-group label="Full Name" label-for="fullname" class="w-50 ms-3 fs-4">
                        <b-form-input id="fullname" v-model="form.full_name" required placeholder="Enter your full name"
                            :class="{ 'is-invalid': form.full_name.length > 30, 'fs-5': true }"></b-form-input>
                    </b-form-group>
                </div>

                <div class="d-flex d-row">
                    <b-form-group label="Email" label-for="email" class="w-50 me-4 fs-4">
                        <b-form-input id="email" type="email" v-model="form.email" required
                            placeholder="Enter your email"
                            :class="{ 'is-invalid': form.email.length > 40, 'fs-5': true }"></b-form-input>
                    </b-form-group>
                    <b-form-group label="Password" label-for="password" class="w-50 fs-4">
                        <b-input-group class="d-flex d-row">
                            <b-form-input id="password" :type="passwordVisible ? 'text' : 'password'"
                                v-model="form.password" required placeholder="Enter your password" minlength="6"
                                :class="{ 'is-invalid': form.password.length > 20, 'fs-5': true }"></b-form-input>
                            <b-input-group-append>
                                <b-button variant="outline-danger" @click="togglePasswordVisibility"
                                    class="text-decoration-none">
                                    <i class="fas" :class="passwordVisible ? 'fa-eye-slash' : 'fa-eye'"></i>
                                </b-button>
                            </b-input-group-append>
                        </b-input-group>
                    </b-form-group>
                </div>

                <div class="d-flex d-row">
                    <b-form-group label="CNIC" label-for="cnic" class="w-50 me-3 fs-4">
                        <b-form-input id="cnic" v-model="form.cnic" required placeholder="Enter CNIC number"
                            :class="{ 'is-invalid': form.cnic.length > 15, 'fs-5': true }"
                            @input="form.cnic = form.cnic.replace(/[^0-9\-]/g, '')"></b-form-input>
                        <div v-if="form.cnic.length > 15" class="invalid-feedback fs-5">
                            Please enter a valid cnic (format: 12345-1234567-1 or 1234512345671).
                        </div>
                    </b-form-group>
                    <b-form-group label="Contact Number" label-for="mobileNo" class="w-50 ms-3 fs-4">
                        <b-form-input id="mobileNo" v-model="form.mobile_no" required placeholder="Enter contact number"
                            :class="{ 'is-invalid': form.mobile_no.length > 12, 'fs-5': true }"
                            @input="form.mobile_no = form.mobile_no.replace(/[^0-9\-]/g, '')"></b-form-input>
                        <div v-if="form.mobile_no.length > 12" class="invalid-feedback fs-5">
                            Please enter a valid contact no (format: 03XX-1234567 or 03XX1234567).
                        </div>
                    </b-form-group>
                </div>

                <div class="d-flex d-row">
                    <b-form-group label="Experience" label-for="experience" class="w-50 me-3 fs-4">
                        <b-form-input id="experience" v-model="form.experience" required placeholder="Enter experience"
                            :class="{ 'is-invalid': form.experience.length > 10, 'fs-5': true }"></b-form-input>
                    </b-form-group>
                    <b-form-group label="Skill Set" label-for="skillset" class="w-50 ms-3 fs-4">
                        <b-form-input id="skillset" v-model="form.skill_set" required
                            placeholder="Enter developer skill set"
                            :class="{ 'is-invalid': form.skill_set.length > 25, 'fs-5': true }"></b-form-input>
                    </b-form-group>
                </div>

                <div class="d-flex d-row">
                    <b-form-group label="Select Manager" label-for="manager" class="w-50 me-3 fs-4">
                        <b-form-select id="manager" v-model="form.manager" class="form-select fs-5" required>
                            <option value="">Please Select</option>
                            <option v-for="(manager, index) in allManagers" :key="index" :value="manager.id">
                                {{ manager.full_name }}</option>
                        </b-form-select>
                    </b-form-group>
                    <b-form-group label="Select Team" label-for="team" class="w-50 ms-3 fs-4">
                        <b-form-select id="team" v-model="form.team" class="form-select fs-5" required>
                            <option value="">Please Select</option>
                            <option v-for="(team, index) in allTeams" :key="index" :value="team.id">{{ team.name }}
                            </option>
                        </b-form-select>
                    </b-form-group>
                </div>

                <b-button-toolbar class="mt-3 justify-content-end">
                    <button class="btn fs-5 btn-danger clr-1 rounded-5" @click="resetForm">Reset</button>
                    <button type="submit" class="btn clr fs-5 rounded-5 ms-4" @click.prevent="submitForm">{{ editBtn ?
                        "Edit" : "Add"}}</button>
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
        this.getAllManagers();
        this.getAllTeams();
    },
    props: ['showModal', 'data', 'editBtn'],
    data() {
        return {
            form: {
                username: '',
                full_name: '',
                email: '',
                password: '',
                cnic: '',
                mobile_no: '',
                experience: '',
                skill_set: '',
                manager: '',
                team: '',
            },
            passwordVisible: false,
            allManagers: null,
            allTeams: null,
            isLoading: false,
        };
    },
    methods: {
        ...mapActions(['addDeveloper', 'getTeamsData', 'getManagersData', 'editUser', 'editDeveloper']),
        async submitForm() {
            if (!this.editBtn) {
                if (this.form.username && this.form.full_name && this.form.email && this.form.password && this.form.cnic
                    && this.form.mobile_no && this.form.experience && this.form.skill_set && this.form.manager && this.form.team) {
                    this.isLoading = true;
                    await this.addNewDeveloper(this.form);
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
                const userId = this.data.user.id;
                const developerId = this.data.developer.id;
                await this.updateDeveloper(this.form, userId, developerId);
                this.isLoading = false;
            }
        },
        resetForm() {
            this.form.username = '';
            this.form.full_name = '';
            this.form.email = '';
            this.form.password = '';
            this.form.cnic = '';
            this.form.mobile_no = '';
            this.form.experience = '';
            this.form.skill_set = '';
            this.form.manager = '';
            this.form.team = '';
            this.$emit('update:showModal', false);
        },
        async addNewDeveloper(formData) {
            try {
                const data = await this.addDeveloper(formData);
                if (data) {
                    Swal.fire({
                        icon: 'success',
                        timer: 1500,
                        title: 'Developer Added Successfully',
                        showConfirmButton: false,
                    }).then(() => {
                        this.$emit('update:showModal', false);
                        window.location.reload();
                        this.resetForm();
                    });
                }
                else {
                    Swal.fire({
                        icon: 'error',
                        timer: 1500,
                        title: "Could Not add developer some error occurred",
                        showConfirmButton: false,
                    });
                }
            }
            catch (error) {
                console.log(error);
            }
        },
        async getAllManagers() {
            try {
                const managers = await this.getManagersData();
                this.allManagers = managers;
                return managers;
            }
            catch (error) {
                console.log(error);
            }
        },
        async getAllTeams() {
            try {
                const teams = await this.getTeamsData(this.form.manager);
                this.allTeams = teams;
                return teams;
            }
            catch (error) {
                console.log(error);
            }
        },
        async updateDeveloper(formData, userId, developerId) {
            try {
                const userData = {
                    id: userId,
                    username: formData.username,
                    email: formData.email,
                    password: formData.password,
                    cnic: formData.cnic,
                    mobile_no: formData.mobile_no,
                };
                const developerData = {
                    id: developerId,
                    full_name: formData.full_name,
                    experience: formData.experience,
                    skill_set: formData.skill_set,
                    manager: formData.manager,
                    team: formData.team,
                    user: userId
                };

                const user = await this.editUser(userData);
                const developer = await this.editDeveloper(developerData);
                if (user || developer) {
                    Swal.fire({
                        icon: 'success',
                        timer: 1500,
                        title: 'Developer Updated Successfully',
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
                        title: "Could Not update developer some error occurred",
                        showConfirmButton: false,
                    });
                }
            }
            catch (error) {

            }
        },
        togglePasswordVisibility() {
            this.passwordVisible = !this.passwordVisible;
        },
    },
    watch: {
        // Name/key of watch should be same as the item we want to watch for changes. 
        'form.manager': async function (newManager, oldManager) {
            if (newManager !== oldManager) {
                try {
                    console.log('Manager changed:', newManager);
                    const teams = await this.getAllTeams();
                    this.allTeams = teams;
                } catch (error) {
                    console.error(error);
                }
            }
        },
        data(newData) {
            if (newData) {
                this.form.username = newData.user.username || '';
                this.form.full_name = newData.developer.full_name || '';
                this.form.email = newData.user.email || '';
                this.form.cnic = newData.user.cnic || '';
                this.form.mobile_no = newData.user.mobile_no || '';
                this.form.experience = newData.developer.experience || '';
                this.form.skill_set = newData.developer.skill_set || '';
                this.form.manager = newData.developer.manager || '';
                this.form.team = newData.developer.team || '';
            }
        }
    },
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