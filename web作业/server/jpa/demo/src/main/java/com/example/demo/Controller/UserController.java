package com.example.demo.Controller;

import com.example.demo.Entity.User;
import com.example.demo.Service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.repository.query.Param;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@CrossOrigin(origins = "*")
@RequestMapping("/user")
public class UserController {

    @Autowired
    private UserService userService;

    // 获取所有用户
    @GetMapping("/list")
    public ResponseEntity<List<User>> getAllUsers() {
        return ResponseEntity.ok().body(userService.getAllUsers());
    }
    // 根据ID获取用户
    @GetMapping("/{id}")
    public ResponseEntity<User> getUserById(@PathVariable int id) {
        User user = userService.getUserById(id);
        return ResponseEntity.ok().body(user);
    }

    // 添加用户
    @PostMapping("/add")
    public ResponseEntity<User> addUser(@RequestBody User user) {

        return ResponseEntity.ok().body(userService.addUser(user));
    }

    // 更新用户
    @PostMapping("/update")
    public int updateUser(@RequestBody User userDetails) {

        return   userService.updateUser(userDetails);

    }

    // 删除用户
    @DeleteMapping("/delete/{id}") // 使用路径变量
    public ResponseEntity<Integer> deleteUser(@PathVariable Long id) {
        System.out.println(id);
        return ResponseEntity.ok().body(userService.deleteUser(id));
    }

}