package com.example.demo.Service;

import com.example.demo.Class.User;
import com.example.demo.Config.RedisConfig;
import com.example.demo.Mapper.UserMapper;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.CacheManager;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.CachePut;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class UserService {

    @Autowired
    private UserMapper userMapper;

    private final CacheManager cacheManager;

    @Autowired
    public UserService(RedisConfig redisConfig) {
        this.cacheManager = redisConfig.cacheManager(redisConfig.redisConnectionFactory(), 2);
    }

    @Cacheable(value = "users", cacheManager = "cacheManager")
    public List<User> getAllUsers() {
        return userMapper.selectAllUsers();
    }

    @Cacheable(value = "users", key = "#id", cacheManager = "cacheManager")
    public User getUserById(int id) {
        return userMapper.selectByUserId(id);
    }

    @CacheEvict(value = "users", allEntries = true, cacheManager = "cacheManager")
    public int addUser(User user) {
        return userMapper.insertUser(user);
    }

    @CachePut(value = "users", key = "#user.userId", cacheManager = "cacheManager")
    public int updateUser(User user) {
        return userMapper.updateByUserId(user);
    }

    @CacheEvict(value = "users", key = "#id", cacheManager = "cacheManager")
    public int deleteUser(Long id) {
        return userMapper.deleteByUserId(id);
    }
}