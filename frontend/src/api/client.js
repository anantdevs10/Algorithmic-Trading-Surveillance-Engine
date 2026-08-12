import axios from "axios";

const client = axios.create({
  baseURL: "http://localhost:8000",
});

export default client;

// one shared Axios instance so every component hits the same base URL.