import axios from "axios";

const api = axios.create({ baseURL: "http://127.0.0.1:8000/api" });

export const getEmployees = (params) => api.get("/employees/", { params });
export const createEmployee = (data) => api.post("/employees/", data);
export const updateEmployee = (id, data) => api.put(`/employees/${id}/`, data);
export const deleteEmployee = (id) => api.delete(`/employees/${id}/`);
export const getInsightsByCountry = () => api.get("/insights/by-country/");
export const getInsightsByJobTitle = () => api.get("/insights/by-job-title/");