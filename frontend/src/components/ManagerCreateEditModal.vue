<template>
    <div v-if="showModal" class="modal-overlay">
        <div class="custom-modal rounded-5">
            <h2 class="mb-4 fw-bold">Add New Role</h2>

            <form v-if="!isLoading" @submit.prevent="handleSubmit" class="text-start">
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
                    <b-form-group label="Experience" label-for="ecperience" class="w-50 me-3 fs-4">
                        <b-form-input id="ecperience" v-model="form.experience" required placeholder="Enter experience"
                            :class="{ 'is-invalid': form.experience.length > 8, 'fs-5': true }"></b-form-input>
                    </b-form-group>
                    <b-form-group label="Department" label-for="department" class="w-50 ms-3 fs-4">
                        <b-form-input id="department" v-model="form.department" required
                            placeholder="Enter your department"
                            :class="{ 'is-invalid': form.department.length > 30, 'fs-5': true }"></b-form-input>
                    </b-form-group>
                </div>

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
                department: '',
            },
            passwordVisible: false,
            isLoading: false,
        };
    },
    methods: {
        ...mapActions(['addManager', 'editManager', 'editUser']),
        async submitForm() {
            if (!this.editBtn) {
                if (this.form.username && this.form.full_name && this.form.email && this.form.password && this.form.cnic
                    && this.form.mobile_no && this.form.experience && this.form.department) {
                    this.isLoading = true;
                    await this.addNewManager(this.form);
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
                const managerId = this.data.data.id;
                await this.updateManager(this.form, userId, managerId);
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
            this.form.department = '';
            this.$emit('update:editBtn', false);
            this.$emit('update:showModal', false);
        },
        async addNewManager(formData) {
            try {
                const data = await this.addManager(formData);
                if (data) {
                    Swal.fire({
                        icon: 'success',
                        timer: 2000,
                        title: 'Manager Added Successfully',
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
                        timer: 2000,
                        title: "Could Not add manager some error occurred",
                        showConfirmButton: false,
                    });
                }
            }
            catch (error) {
                console.log(error);
            }
        },
        async updateManager(formData, userId, managerId) {
            try {
                const userData = {
                    id: userId,
                    username: formData.username,
                    email: formData.email,
                    password: formData.password,
                    cnic: formData.cnic,
                    mobile_no: formData.mobile_no,
                };
                const managerData = {
                    id: managerId,
                    full_name: formData.full_name,
                    experience: formData.experience,
                    department: formData.department,
                    user: userId
                };

                const user = await this.editUser(userData);
                const manager = await this.editManager(managerData);
                if (user || manager) {
                    Swal.fire({
                        icon: 'success',
                        timer: 1500,
                        title: 'Manager Updated Successfully',
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
                        title: "Could Not update manager some error occurred",
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
        // Watching for data prop for changes so that they are rendered asap.
        data(newData) {
            if (newData) {
                this.form.username = newData.user.username || '';
                this.form.full_name = newData.data.full_name || '';
                this.form.email = newData.user.email || '';
                this.form.cnic = newData.user.cnic || '';
                this.form.mobile_no = newData.user.mobile_no || '';
                this.form.experience = newData.data.experience || '';
                this.form.department = newData.data.department || '';
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