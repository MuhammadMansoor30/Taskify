<template>
    <div class="d-flex flex-column w-100">
        <div class="p-3">
            <h2 class="my-4">{{ title }}</h2>
        </div>
        <div class="d-flex justify-content-end px-3 " v-if="this.permission">
            <button class="btn clr-1 fs-5 rounded-5 p-1" @click="setShowModal">
                <i class="fas fa-add"></i>
                Create
            </button>
        </div>
        <div class="container-fluid my-5">
            <!-- Can also change the border rounded radius using rounded-4 or rounded-5 so on -->
            <div class="card shadow-sm rounded-4">   
                <div class="card-header rounded-top-4" style="background-color: #800020; color: #ececec;">
                    <h4 class="mb-0">{{ tableTitle }}</h4>
                </div>
                <div class="card-body">
                    <b-table :fields="fields" :items="items" responsive="sm"
                        class="table table-bordered table-hover table-lg">
                        <template #cell(index)="data">
                            <span class=" text-danger font-weight-bold fs-4">{{ data.index + 1 }}</span>
                        </template>

                        <template #cell()="data">
                            <span class="text-dark font-weight-bold fs-4">{{ data.value }}</span>
                        </template>

                        <template #cell(button)="data" v-if="editPermission">
                            <div class="d-flex justify-content-evenly">
                                <button class="btn clr" @click="editData(data.item)" v-if="!this.approvalPermission">Edit</button>
                                <button class="btn btn-danger" @click="deleteItem(data.item)" v-if="!this.approvalPermission">Delete</button>
                                <button class="btn clr-1" @click="approveWork(data.item)" v-if="this.approvalPermission">Approve</button>
                            </div>
                        </template>
                    </b-table>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Swal from 'sweetalert2';
import { mapGetters } from 'vuex';

export default {
    mounted() {
        this.permission = this.hasPermissions(this.hasCreatePermission);
        this.approvalPermission = this.hasPermissions(this.hasApprovalPermission);
        if(this.hasEditPermission){
            this.editPermission = this.hasPermissions(this.hasEditPermission);
        }
    },
    data() {
        return {
            permission: false,
            approvalPermission: false,
            editPermission: true,
            tableItems: null,
        }
    },
    props: ['title', 'tableTitle', 'fields', 'items', 'editData', 'deleteData', 'approveWork', 'hasCreatePermission', 'hasApprovalPermission', 'hasEditPermission','showModal'],
    computed: {
        ...mapGetters(['hasPermissions']),
    },
    methods: {
        setShowModal(){
            this.$emit('update:showModal', true);   // We cannot directly modify the value of props in vue so w ehave to emit event to modify its values from parent.
            // For that we have to pass the props as a v-model property. 
        },
        deleteItem(item){
            Swal.fire({
                icon: 'question',
                text: "Are You Sure You want to Delete!",
                confirmButtonText: "Yes! Delete it",
                showCancelButton: true,
                showConfirmButton: true,
            }).then(async result => {
                if (result.value){
                    await this.deleteData(item);
                }
            });
        }
    },
    watch: {
        items(newItems) {
        },
    },   // Watch is just to track the changes in the props or other elements: helpful if elements have changed as mounted runs after dom is loaded. No need only for learning.
}

</script>

<style scoped>
.clr {
    width: 70px;
    background: #800020;
    color: #ececec;
}

.clr:hover {
    width: 70px;
    background: #630000;
    color: #ececec;
}

.clr-1 {
    width: 120px;
    background: #800020;
    color: #ececec;
}

.clr-1:hover {
    width: 120px;
    background: #630000;
    color: #ececec;
}
</style>