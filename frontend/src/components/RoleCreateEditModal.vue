<template>
    <div v-if="showModal" class="modal-overlay">
        <div class="custom-modal rounded-5">
            <h2 class="mb-4 fw-bold">Add New Role</h2>

            <form v-if="!isLoading" @submit.prevent="handleSubmit" class="text-start">
                <b-form-group label="Name" label-for="name" class="fs-4">
                    <b-form-input id="name" v-model="form.name" required placeholder="Enter role name"
                        :class="{ 'is-invalid': form.name.length > 30, 'fs-5': true }"></b-form-input>
                </b-form-group>

                <b-form-group label="Code Name" label-for="codename" class="fs-4">
                    <b-form-input id="codename" v-model="form.code_name" required placeholder="Enter role code name"
                        :class="{ 'is-invalid': form.code_name.length > 30, 'fs-5': true }"></b-form-input>
                </b-form-group>

                <b-form-group label="Permissions" label-for="permission" class="fs-4">
                    <b-form-select id="permission" class="form-select fs-5" v-model="form.permissions"
                        :class="{ 'is-invalid': isPermSelected }" required multiple>
                        <option :value="[]">Please Select</option>
                        <option v-for="(perm, index) in allPermissions" :key="index" :value="perm.id">{{ perm.name}} </option>
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
    mounted(){
        this.getAllPermissions();
    },
    props: ['showModal'],
    data() {
        return {
            form: {
                name: '',
                code_name: '',
                permissions: [],
            },
            isLoading: false,
            allPermissions: null,
            isPermSelected: false,
        };
    },
    methods: {
        ...mapActions(['addRole', 'getPermissionsData']),
        async submitForm() {
            if (this.form.name && this.form.code_name && this.form.permissions) {
                this.isPermSelected = false;
                console.log(this.form.permissions);
                this.isLoading = true;
                await this.addNewRole(this.form);
                this.isLoading = false;
            }
            else {
                this.isPermSelected = true;
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
            this.form.code_name = '';
            this.form.permissions = [];
            this.isPermSelected = false;
            this.$emit('update:showModal', false);
        },
        async addNewRole(formData) {
            try {
                const data = await this.addRole(formData);
                if (data) {
                    Swal.fire({
                        icon: 'success',
                        timer: 1500,
                        title: 'Role Added Successfully',
                        showConfirmButton: false,
                    }).then(() => {
                        this.$emit('update:showModal', false); // Same as done in Table Component.
                        window.location.reload();
                        this.resetForm();
                    });
                }
                else {
                    Swal.fire({
                        icon: 'error',
                        timer: 1500,
                        title: "Could Not add role some error occurred",
                        showConfirmButton: false,
                    });
                }
            }
            catch (error) {
                console.log(error);
            }
        },
        async getAllPermissions(){
            try{
                const data = await this.getPermissionsData();
                this.allPermissions = data;
            }
            catch(error){
                console.log(error);
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