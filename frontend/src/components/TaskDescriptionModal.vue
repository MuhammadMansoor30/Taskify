<template>
    <div v-if="descModal" class="modal-overlay">
        <div class="custom-modal rounded-5">
            <div class="d-flex flex-row header">
                <h2 class="mb-4 fw-bold">Task Description</h2>
                <i class="fas fa-close fs-2 icon" @click="modalClose"></i>
            </div>
            <div class="fs-4 text-start text-dark">
                <p>{{ task.description }}</p>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    props: ['descModal', 'task'],
    methods: {
        modalClose() {
            this.$emit('update:descModal', false);
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