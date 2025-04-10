
import axios from 'axios';

export const renameRedisKey = (oldKey, newKey) => {
  return axios.post('http://localhost:8080/data/rename', { oldKey, newKey });
}

export function getRedisList(){
  return axios({
    url: "http://localhost:8080/data/list",
    method: "GET"
  });
}

export function addRedisItem(data){
  return axios({
   
    url: "http://localhost:8080/data/set",
    method: "POST",
    data: data
  }) 
}
export function getRedisItem(key){
  
}
export function deleteRedisItem(key) {
  return axios({
    url: "http://localhost:8080/data/delete",
    method: "post",
    data: {key: key}
  });
}

export function updateRedisItem(data) 
{
  return axios({
    url: "http://localhost:8080/data/update",
    method: "post",
    data: data
  });
}

