<template>
    <div class="d-flex flex-column w-100">
        <div class="p-3">
            <h2 class="my-4">{{ title }}</h2>
        </div>
        <div class="d-flex justify-content-end px-3" v-if="this.permission">
            <button class="btn clr-1 fs-5 rounded p-1">
                <i class="fas fa-add"></i>
                Create
            </button>
        </div>
        <div class="container-fluid my-5">
            <div class="card shadow-sm">
                <div class="card-header" style="background-color: #800020; color: #ececec;">
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

                        <template #cell(button)="data">
                            <div class="d-flex justify-content-evenly">
                                <button class="btn clr" @click="editData(data.item)">Edit</button>
                                <button class="btn btn-danger" @click="deleteData(data.item)">Delete</button>
                            </div>
                        </template>
                    </b-table>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
    mounted() {
        this.permission = this.hasPermissions(this.hasCreatePermission);
    },
    data() {
        return {
            permission: false,
            tableItems: null,
        }
    },
    props: ['title', 'tableTitle', 'fields', 'items', 'editData', 'deleteData', 'hasCreatePermission'],
    computed: {
        ...mapGetters(['hasPermissions']),
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

.clr-1 {
    width: 120px;
    background: #800020;
    color: #ececec;
}
</style>