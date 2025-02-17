<template>
    <div class="d-flex flex-column justify-content-center align-items-center" style="height: 100vh;">
        <h1 class="my-4">Welcome To Taskify</h1>
        <h3 class="my-4">Login to continue</h3>
        <b-form @submit.prevent="submitForm()" class="w-50">
            <b-form-group id="email" label="Enter Your Email" label-for="email-input" label-class="text-left" class="fs-4">
                <div>
                    <b-form-input id="email-input" type="email" v-model="email" required placeholder="test@email.com" :class="{'is-invalid': emailError, 'fs-5': true}" />
                    <b-form-invalid-feedback v-if="emailError">{{ emailErrorMessage }}</b-form-invalid-feedback>
                </div>
            </b-form-group>

            <b-form-group id="password" label="Enter Your Password" label-for="password-input" label-class="text-left" class="fs-4">
                <div class="d-flex">
                    <b-input-group class="w-100">
                        <b-form-input id="password-input" :type="passwordVisible ? 'text' : 'password'"
                            v-model="password" required placeholder="*********"  :class="{'is-invalid': passwordError, 'fs-5': true}"/>
                        <b-input-group-append>
                            <b-button variant="outline-danger" @click="togglePasswordVisibility"
                                class="text-decoration-none">
                                <i class="fas" :class="passwordVisible ? 'fa-eye-slash' : 'fa-eye'"></i>
                            </b-button>
                        </b-input-group-append>
                        <b-form-invalid-feedback v-if="passwordError">{{ passwordErrorMessage }}</b-form-invalid-feedback>
                    </b-input-group>
                </div>
            </b-form-group>

            <b-button type="submit" class="btn-1 fs-4">Log In</b-button>
        </b-form>
    </div>
</template>

<script>
import router from '@/router';
import { mapActions, mapGetters } from 'vuex';

export default {
    name: "LoginView",
    data() {
        return {
            email: '',
            password: '',
            passwordVisible: false,
            emailError: false,
            passwordError: false,
            emailErrorMessage: '',
            passwordErrorMessage: '',
        };
    },
    computed: {
        ...mapGetters([
            'getIsLoggedIn',
        ])
    },
    methods: {
        ...mapActions([
            'login'
        ]),
        async submitForm() {
            console.log('Form submitted with:', this.email, this.password);
            console.log(this.getIsLoggedIn);
            this.validateFields(this.email, this.password);

            try{
                const data = await this.login({email: this.email, password: this.password});
                console.log("dta", data);
            }
            catch(error){
                console.log("In", error);
            }
            if (!this.emailError && !this.passwordError) {
                console.log(this.getIsLoggedIn);
                router.push('/home');
            }
        },
        validateFields(email, password){
            const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
            if (!emailRegex.test(email)){
                this.emailError = true;
                this.emailErrorMessage = "Email Is invalid. Please provide a valid email!"
            }
            else{
                this.emailError = false;
                this.emailErrorMessage = ""
            }
            if(password.length < 6){
                console.log("In");
                this.passwordError = true;
                this.passwordErrorMessage = "Password must be atleast 6 characters";
            }
            else{
                this.passwordError = false;
                this.passwordErrorMessage = "";
            }
        },
        togglePasswordVisibility() {
            this.passwordVisible = !this.passwordVisible;
        }
    }
};
</script>

<style scoped>
h1 {
    font-size: 2.5rem;
    font-weight: bold;
    color: #800020;
}

h3 {
    font-size: 2rem;
    font-weight: 500;
    color: #242124;
}

.btn-1{
    width: 200px;
    background: #800020;
    border: none;
}
.btn-1:hover{
    background: #242124;
    color: #e2dbd4;
}

</style>