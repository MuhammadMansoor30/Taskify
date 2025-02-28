<template>
    <div v-for="(item, index) in fields" :key="index" class="card rounded-5 border-3 border-danger m-3 ">
        <div class="card-body d-flex justify-content-evenly align-items-center">
            <i class="me-4 text-success" :class="item.iconClass"></i>
            <div>
                <h5 class="card-title mb-2 fs-3 fw-bold">{{item.title}}</h5>
                <p class="card-text fs-3">Count: {{ item.count }}</p>
            </div>
        </div>
    </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
    mounted() {
        this.getDataCount();
        
    },
    data() {
        return {
            fields: [],
        };
    },
    methods: {
        ...mapActions(['getManagersData', 'getTeamsData', 'getWorkItemsData', 'getDevelopersData', 'getTasksData', 'getUsersData']),
        ...mapGetters(['getUser']),
        async getDataCount() {
            try {
                const user = await this.getUser();

                if (user.permissions.includes('manager_get')){
                    const managerCount = await this.getManagersData();
                    this.fields.push({ iconClass: 'fas fa-user fa-3x', title: "Total Managers", count: managerCount.length });
                }
                if (user.permissions.includes('teams_get')){
                    const teamsCount = await this.getTeamsData();
                    this.fields.push({ iconClass: 'fas fa-users fa-3x', title: "Total Teams", count: teamsCount.length });
                }
                if (user.permissions.includes('work_get')){
                    const approved_workItemsCount = await this.getWorkItemsData({ is_approved: true });
                    this.fields.push({ iconClass: 'fas fa-check-double fa-3x', title: "Approved Work Items", count: approved_workItemsCount.length });

                    const notApproved_workItemsCount = await this.getWorkItemsData({ is_approved: false });
                    this.fields.push( { iconClass: 'fas fa-file-circle-plus fa-3x', title: "Not Approved Work Items", count: notApproved_workItemsCount.length });
                }
                if (user.permissions.includes('developers_get')){
                    const developersCount = await this.getDevelopersData();
                    this.fields.push({ iconClass: 'fas fa-users fa-3x', title: "Total Developers", count: developersCount.length });
                }
                if (user.permissions.includes('tasks_get')){
                    const tasksCount = await this.getTasksData();
                    this.fields.push({ iconClass: 'fas fa-list-check fa-3x', title: "Total Tasks", count: tasksCount.length });
                }
                if (user.permissions.includes('users_get')){
                    const usersCount = await this.getUsersData();
                    this.fields.push({ iconClass: 'fas fa-users fa-3x', title: "Total Users", count: usersCount.length });
                }

                console.log(this.fields);
            }
            catch (error) {
                console.log(error);
            }
        }
    }
};
</script>

<style scoped>
.card {
    display: flex;
    align-items: center;
    min-width: 30%;
    max-width: 30%;
    background-color: #e2dbd4;
}

.card-body{
    width: 100%;
}

</style>