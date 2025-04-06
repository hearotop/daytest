package com.example.demo.Class;


import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

// 假设这里根据MyBatis改动更新注解和方法调用，例如添加MyBatis相关注解


@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class User {
    

    private int userId;
  
    private String password;
 
    private String phone;
    private String email;
    private int sex;
    private String nickName;
    // 添加 user 属性及其 getter 和 setter 方法




    @Override
    public String toString() {
        return "User{" +
                "userId=" + userId +
                ", password='" + password + '\'' +
                ", phone='" + phone + '\'' +
                ", email='" + email + '\'' +
                ", sex=" + sex +
                ", nickName='" + nickName + '\'' +
                '}';

    }
}
