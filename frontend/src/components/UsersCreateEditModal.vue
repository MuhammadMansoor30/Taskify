<template>
    <div v-if="showModal" class="modal-overlay">
        <div class="custom-modal rounded-5">
            <h2 class="mb-4 fw-bold">Add New User</h2>

            <form v-if="!isLoading" @submit.prevent="submitForm" class="text-start">
                <b-form-group label="Username" label-for="username" class="fs-4">
                    <b-form-input id="username" v-model="form.username" required placeholder="Enter user name"
                        :class="{ 'is-invalid': form.username.length > 30, 'fs-5': true }"></b-form-input>
                </b-form-group>

                <b-form-group label="Email" label-for="email" class="fs-4">
                    <b-form-input id="email" type="email" v-model="form.email" required placeholder="Enter your email"
                        :class="{ 'is-invalid': form.email.length > 40, 'fs-5': true }"></b-form-input>
                </b-form-group>

                <b-form-group label="Password" label-for="password" class="fs-4">
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

                <b-form-group label="CNIC" label-for="cnic" class="fs-4">
                    <b-form-input id="cnic" v-model="form.cnic" required placeholder="Enter CNIC number"
                        :class="{ 'is-invalid': form.cnic.length > 15, 'fs-5': true }"
                        @input="form.cnic = form.cnic.replace(/[^0-9\-]/g, '')"></b-form-input>
                    <div v-if="form.cnic.length > 15" class="invalid-feedback fs-5">
                        Please enter a valid cnic (format: 12345-1234567-1 or 1234512345671).
                    </div>
                </b-form-group>

                <b-form-group label="Contact Number" label-for="mobileNo" class="fs-4">
                    <b-form-input id="mobileNo" v-model="form.mobile_no" required placeholder="Enter contact number"
                        :class="{ 'is-invalid': form.mobile_no.length > 12, 'fs-5': true }"
                        @input="form.mobile_no = form.mobile_no.replace(/[^0-9\-]/g, '')"></b-form-input>
                    <div v-if="form.mobile_no.length > 12" class="invalid-feedback fs-5">
                        Please enter a valid contact no (format: 03XX-1234567 or 03XX1234567).
                    </div>
                </b-form-group>

                <b-form-group label="Add Roles" label-for="roles" class="fs-4">
                    <b-form-select id="roles" v-model="form.roles" class="form-select fs-5" required multiple>
                        <option :value="[]" class="fw-bold">Please Select One or Multiple</option>
                        <option v-for="(role, index) in allRoles" :key="index" :value="role.id"> {{ role.name }}</option>
                    </b-form-select>
                </b-form-group>

                <b-button-toolbar class="mt-3 justify-content-end">
                    <button class="btn fs-5 btn-danger clr-1 rounded-5" @click="resetForm">Reset</button>
                    <button type="submit" class="btn clr fs-5 rounded-5 ms-4"
                        @click.prevent="submitForm">Submit</button>
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
        this.getAllRoles();
    },
    props: ['showModal'],
    data() {
        return {
            form: {
                username: '',
                email: '',
                password: '',
                cnic: '',
                mobile_no: '',
                roles: [],
            },
            passwordVisible: false,
            allRoles: null,
            isLoading: false,
        };
    },
    methods: {
        ...mapActions(['addUser', 'getRolesData']),
        async submitForm() {
            if (this.form.username && this.form.email && this.form.password && this.form.cnic && this.form.mobile_no && this.form.roles) {
                this.isLoading = true;
                await this.addNewUser(this.form);
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
        },
        resetForm() {
            this.form.username = '';
            this.form.full_name = '';
            this.form.email = '';
            this.form.password = '';
            this.form.cnic = '';
            this.form.mobile_no = '';
            this.form.roles = '';
            this.$emit('update:showModal', false);
        },
        async addNewUser(formData) {
            try {
                const data = await this.addUser(formData);
                if (data) {
                    Swal.fire({
                        icon: 'success',
                        timer: 1500,
                        title: 'User Added Successfully',
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
                        title: "Could Not add user some error occurred",
                        showConfirmButton: false,
                    });
                }
            }
            catch (error) {
                console.log(error);
            }
        },
        async getAllRoles() {
            try {
                const roles = await this.getRolesData();
                this.allRoles = roles;
                return roles;
            }
            catch (error) {
                console.log(error);
            }
        },
        togglePasswordVisibility() {
            this.passwordVisible = !this.passwordVisible;
        },
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