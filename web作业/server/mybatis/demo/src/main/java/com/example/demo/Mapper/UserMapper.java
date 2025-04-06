package com.example.demo.Mapper;

import org.apache.ibatis.annotations.Mapper;

import com.example.demo.Class.User;

import java.util.List;
@Mapper
// 移除 @MapperScan 注解
// 移除泛型参数，因为 Mapper 不是泛型接口
public interface UserMapper{
    //select
    //查询所有用户
    List<User> selectAllUsers();
    User selectByUserId(int userId);
    //根据手机号查询用户

    User selectByPhone(String phone);
    //update
    int updateByUserId(User user);

    //delete
    //删除用户
    int deleteByUserId(Long userId);
    //insert
    //添加用户
    int insertUser(User user);





}
