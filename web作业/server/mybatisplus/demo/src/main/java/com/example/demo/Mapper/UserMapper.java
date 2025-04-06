package com.example.demo.Mapper;



import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.example.demo.Class.User;
import org.apache.ibatis.annotations.*;

import java.beans.Transient;
import java.util.List;
@Mapper
public interface UserMapper extends BaseMapper<User> {
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
