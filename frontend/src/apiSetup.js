import axios from "axios";

export const loginApi = axios.create({
    baseURL: process.env.DJANGO_APP_URL,
    headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer {Token}"
    }
});

export const backendApi = axios.create({
    baseURL: process.env.DJANGO_APP_URL,
    headers: {
        "Content-Type": "application/json",
        Authorization: "Api-Key " + process.env.VUE_APP_API_KEY,
    }
});

export const fileApi = axios.create({
    baseURL: process.env.DJANGO_APP_URL,
    headers: {
        "Content-Type": "multipart/form-data"
    }
});
