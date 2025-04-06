package com.example.demo.Service;

import com.example.demo.Class.User;
import com.example.demo.Mapper.UserMapper;

import org.apache.ibatis.annotations.Mapper;
import org.mybatis.spring.annotation.MapperScan;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Mapper
@Service

@MapperScan("com.example.demo.Mapper")
public class UserService {

    @Autowired
    private UserMapper userMapper;

    // 获取所有用户

    public List<User> getAllUsers() {
        return userMapper.selectAllUsers();
    }

    // 根据ID获取用户

    public User getUserById(int id) {
        return userMapper.selectByUserId(id);
    }

    // 添加用户

    public int addUser(User user) {
        return userMapper.insertUser(user);
    }

    // 更新用户

    public int updateUser(User user) {
        return userMapper.updateByUserId(user);
    }

    // 删除用户

    public int deleteUser(Long id) {
        return userMapper.deleteByUserId(id);
    }
}
