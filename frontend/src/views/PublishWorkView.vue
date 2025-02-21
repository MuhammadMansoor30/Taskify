<template>
    <div class="home d-flex flex-row">
        <sidebar class="col-12 col-lg-2" />

        <div class="d-flex flex-column w-100">
            <div class="p-3">
                <h2 class="my-4">Publish Work Items</h2>
            </div>

            <div class="container-fluid my-3">
                <div class="shadow-lg p-4 border rounded-5 bg-light">
                    <h4 class="mb-0 rounded-5" style="background-color: #800020; color: #ececec; padding: 10px;">
                        Add New Work Item
                    </h4>
                    <div class="mt-3 text-start">
                        <b-form @submit.prevent="submitForm">
                            <b-form-group class="mb-2 fs-4" label="Work Item Name" label-for="textField"
                                :invalid="name.length > 50">
                                <b-form-input type="text" id="textField" class="form-control fs-5" v-model="name"
                                    placeholder="Enter Work Item Name" :class="{ 'is-invalid': name.length > 50 }"
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
                                <b-form-select id="selectField1" class="form-select fs-5" v-model="status">
                                    <option v-for="(option, index) in statusOptions" :value="option.value" :key="index">
                                        {{ option.label }}</option>
                                </b-form-select>
                            </b-form-group>

                            <b-form-group class="mb-2 fs-4" label="Is Approved" label-for="booleanField">
                                <b-form-select id="booleanField" class="form-select fs-5" v-model="is_approved">
                                    <option value="">Please Select</option>
                                    <option value="True">True</option>
                                    <option value="False">False</option>
                                </b-form-select>
                            </b-form-group>

                            <b-form-group class="mb-2 fs-4" label="Select Task" label-for="selectField2"
                                :invalid="isTaskSelected" invalid-feedback="Please select a task.">
                                <b-form-select id="selectField2" class="form-select fs-5" v-model="selectedTask"
                                    :class="{ 'is-invalid': isTaskSelected }" required>
                                    <option value="">Please Select</option>
                                    <option v-for="(task, index) in tasks" :key="index" :value="task.id">{{ task.title }}
                                    </option>
                                </b-form-select>
                            </b-form-group>

                            <div class="d-flex justify-content-end">
                                <button type="submit" class="btn btn-outline-danger fs-5 mt-4 rounded-5 p-2 me-4 clr"
                                    @click.prevent="resetForm">Reset</button>
                                <button type="submit" class="btn clr-1 fs-5 mt-4 rounded-5 p-2"
                                    @click.prevent="submitForm">Submit</button>
                            </div>
                        </b-form>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>
<script>
import Sidebar from '@/components/Sidebar.vue';
import DataTable from '@/components/DataTable.vue';
import { mapActions, mapGetters } from 'vuex';
import Swal from 'sweetalert2';

export default {
    components: {
        Sidebar,
        DataTable
    },
    async mounted() {
        this.getTasks();
    },
    data() {
        return {
            name: '',
            file: '',
            status: '',
            is_approved: '',
            selectedTask: '',
            tasks: null,
            isFileSelected: false,
            isTaskSelected: false,
            statusOptions: [
                { value: "", label: 'Select Status' },
                { value: "In Progress", label: 'In Progress' },
                { value: "Partially Completeds", label: 'Partially Completed' },
                { value: "Completed", label: 'Completed' },
            ],
            fields: [
                { key: 'index', label: "Id", thStyle: { width: '200px', fontSize: "20px", color: "#242124", } },
                { key: 'username', label: 'Name', thStyle: { fontSize: "20px", color: "#242124", } },
                { key: 'email', label: "Email Address", thStyle: { fontSize: "20px", color: "#242124", } },
                { key: 'cnic', label: "CNIC", thStyle: { fontSize: "20px", color: "#242124", } },
                { key: 'mobile_no', label: "Contact Number", thStyle: { fontSize: "20px", color: "#242124", } },
                { key: 'button', label: "Action", thStyle: { width: '200px', fontSize: "20px", color: "#242124", } },
            ],
        }
    },
    methods: {
        ...mapActions(['getTasksData', 'addWorkItem']),
        async getTasks() {
            try {
                const data = await this.getTasksData();
                this.tasks = data;
            }
            catch (error) {
                console.log(error);
            }
        },
        async submitForm() {
            try {
                if (this.selectedTask && this.file) {
                    this.isFileSelected = false;
                    this.isTaskSelected = false;
                    const payload = {
                        name: this.name,
                        file: this.file,
                        status: this.status,
                        is_approved: this.is_approved,
                        task: this.selectedTask
                    };
                    const data = await this.addWorkItem(payload);
                    if(data){
                        Swal.fire({
                            icon: 'success',
                            title: "Work Item Added Successfully!",
                            timer: 2000,
                            showConfirmButton: false,
                        }).then(() => {
                            this.$router.push('approveWork');
                            this.resetForm();
                        });
                    }
                    else{
                        Swal.fire({
                            icon: 'error',
                            title: "Some Error Occurred",
                            timer: 2000,
                            showConfirmButton: false,
                        })
                    }
                }
                else {
                    this.isFileSelected = true;
                    this.isTaskSelected = true;
                }
            }
            catch (error){
                console.log(error);
            }
        },
        resetForm() {
            this.name = '';
            this.file = '';
            this.status = '';
            this.is_approved = '';
            this.selectedTask = '';
            this.isFileSelected = false;
            this.isTaskSelected = false;
        },
        handleFileUpload(event) {
            this.file = event.target.files[0];
        }
    },
    computed: {
        ...mapGetters(['hasPermissions']),
    },
};
</script>

<style scoped>
.home {
    display: flex;
    min-height: 100vh;
}

.clr {
    width: 120px;
}

.clr-1 {
    width: 120px;
    background: #800020;
    color: #ececec;
}
</style>