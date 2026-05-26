import axios from 'axios';

const API_BASE = 'http://localhost:5001/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' }
});

export const validatePlate = (plateNumber) => 
  api.post('/validate_plate', { plate_number: plateNumber });

export const searchPlate = (partialPlate) => 
  api.post('/search_plate', { partial_plate: partialPlate });

export const checkOwnership = (ownerId) => 
  api.post('/check_ownership', { owner_id: ownerId });

export const verifyComplete = (plateNumber, ownerId) => 
  api.post('/verify_complete', { plate_number: plateNumber, owner_id: ownerId });

export const getVehicles = (page = 1, perPage = 20) => 
  api.get(`/vehicles?page=${page}&per_page=${perPage}`);

export const getChallans = (page = 1, perPage = 20) => 
  api.get(`/challans?page=${page}&per_page=${perPage}`);

export const getVehicle = (plate) => 
  api.get(`/vehicle/${plate}`);

export const getOwner = (ownerId) => 
  api.get(`/owner/${ownerId}`);

export const getStatsOverview = () => 
  api.get('/stats/overview');

export const getStatsViolations = () => 
  api.get('/stats/violations');

export const getStatsPayment = () => 
  api.get('/stats/payment');

export const getStatsStates = () => 
  api.get('/stats/states');

export const getCameraOptimization = () => 
  api.get('/camera/optimization');

export const getCameraCostBenefit = () => 
  api.get('/camera/costbenefit');

export const getOwnershipGraph = () => 
  api.get('/network/graph');

export default api;