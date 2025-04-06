package com.example.demo.Repository;

import com.example.demo.Entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface UserRepository extends JpaRepository<User, Integer> {
    //select
    //查询所有用户
    @Modifying
    @Query("select u from User u")
    List<User> selectAllUsers();
    //查询单个用户
    @Query("select u from User u where u.userId = ?1")
    User selectByUserId(int userId);
    //根据手机号查询用户
    @Modifying
    @Query("select u from User u where u.phone = ?1")
    User selectByPhone(String phone);
    //update
    //修改用户信息
    @Modifying
    @Query("update User u set u.password = ?1, u.phone = ?2, u.email = ?3, u.sex = ?4, u.nickName = ?5 where u.userId = ?6")
    int updateByUserId(String password, String phone, String email, int sex, String nickName, int userId);


    //delete
    //删除用户
    @Modifying
    @Query("delete from User u where u.userId = ?1")
    int deleteByUserId(Long userId);
    //insert
    //添加用户

    @Modifying
    @Query("insert into User(password, phone, email, sex, nickName) values(?1, ?2, ?3, ?4, ?5)")
    int insertUser(User user);





}
