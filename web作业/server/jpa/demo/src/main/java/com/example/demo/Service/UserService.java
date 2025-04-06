package com.example.demo.Service;

import com.example.demo.Entity.User;
import com.example.demo.Repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    // 获取所有用户
    @Transactional
    public List<User> getAllUsers() {
        return userRepository.selectAllUsers();
    }

    // 根据ID获取用户
    @Transactional
    public User getUserById(int id) {
        return userRepository.selectByUserId(id);
    }

    // 添加用户
    @Transactional
    public User addUser(User user) {
        return userRepository.save(user);
    }

    // 更新用户
    @Transactional
    public int updateUser(User user) {


        return userRepository.updateByUserId(user.getPassword(), user.getPhone(), user.getEmail(), user.getSex(), user.getNickName(), user.getUserId());
    }

    // 删除用户
    @Transactional // 确保事务支持
    public int deleteUser(Long id) {
      return  userRepository.deleteByUserId(id);
    }
}
