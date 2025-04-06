
import axios from "axios";


export  function getUserList() {
  return  axios({
            url: `http://localhost:8080/user/list`,
            method: "GET"
        })
}
export function deleteUserById(id) {
    return axios({
        url: `http://localhost:8080/user/delete/${id}`, // 将 id 添加到 URL 路径
        method: "DELETE",
    });
}
export function updateUserAPI(userData) {
    return axios({
        url: `http://localhost:8080/user/update`,
        method: 'post',
        data: userData
    });
}

export function addUser(userData) {
  return axios({
    url: 'http://localhost:8080/user/add',
    method: 'POST',
    data: userData
  });
}
