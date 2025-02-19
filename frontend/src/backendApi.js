import axios from "axios";

export const backendApi = axios.create({
    baseURL: process.env.VUE_APP_BACKEND_URL,
    // baseURL: 'http://localhost:8000/taskify/',
    headers: {
        "Content-Type": "application/json",
    },
    withCredentials: true,   // TO include cookies in request as well.
});

export const loginApi = axios.create({
    // baseURL: process.env.VUE_APP_BACKEND_URL,
    baseURL: 'http://localhost:8000/taskify/',
    headers: {
        "Content-Type": "application/json",
        Authorization: "Api-Key " + process.env.VUE_APP_API_KEY,
    },
    withCredentials: true
});

export const fileApi = axios.create({
    baseURL: process.env.VUE_APP_BACKEND_URL,
    headers: {
        "Content-Type": "multipart/form-data"
    },
    withCredentials: true
    
});
